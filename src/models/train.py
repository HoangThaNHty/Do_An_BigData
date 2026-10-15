"""Train-only preprocessing, validation selection, then locked temporal test."""
import argparse
import hashlib
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path
from pyspark import StorageLevel
from pyspark.sql import functions as F
from pyspark.ml import PipelineModel
from pyspark.ml.regression import LinearRegression, RandomForestRegressor, GBTRegressor
from src.config.spark import ROOT, session
from src.models.features import prepare, preprocessor, FEATURE_INPUTS

KINDS = {'house':'nhà','apartment':'căn hộ chung cư'}
# Freeze settings before any validation/test metrics. Limited experiment budget.
CONFIGS = {'lr':dict(maxIter=80, regParam=0.05, elasticNetParam=0.0),
           'rf':dict(numTrees=30, maxDepth=7, maxBins=32, minInstancesPerNode=10, seed=20261012),
           'gbt':dict(maxIter=30, maxDepth=5, maxBins=32, minInstancesPerNode=10, stepSize=0.1, seed=20261012)}


def metrics(df):
    error = F.col('predicted_price_vnd') - F.col('price')
    ape = F.abs(error) / F.col('price')
    row = df.agg(F.count('*').alias('count'), F.avg(F.abs(error)).alias('mae_vnd'),
                 F.sqrt(F.avg(error*error)).alias('rmse_vnd'), F.avg(ape).alias('mape'),
                 F.percentile_approx(ape, 0.5, 10000).alias('median_ape'),
                 F.sum(error*error).alias('sse'), F.var_pop('price').alias('variance')).first().asDict()
    sst = (row.pop('variance') or 0) * row['count']
    row['r2'] = 1-row.pop('sse')/sst if sst else None
    if not row['count'] or any(not math.isfinite(row[k]) for k in ['mae_vnd','rmse_vnd','mape','median_ape']):
        raise ValueError('Empty or nonfinite evaluation')
    return row


def predict(model, frame):
    # Exponentiating log prediction estimates a typical asking price, not an
    # unbiased arithmetic mean. No correction fitted on test targets.
    return model.transform(frame).withColumn('predicted_price_vnd', F.exp('prediction'))


def baseline_fit(train):
    median = lambda c:F.percentile_approx(c,0.5,10000)
    groups = [r.asDict() for r in train.groupBy('property_type_name','district_code').agg(F.count('*').alias('n'), median('price').alias('median_price_vnd')).collect()]
    fallback = [r.asDict() for r in train.groupBy('property_type_name').agg(median('price').alias('median_price_vnd')).collect()]
    return {'groups':groups,'fallback':fallback,'minimum_group_count':20}


def baseline_predict(df, spec, spark):
    local = [r for r in spec['groups'] if r['n'] >= spec['minimum_group_count']]
    table = spark.createDataFrame([(r['property_type_name'],r['district_code'],float(r['median_price_vnd'])) for r in local], 'property_type_name string, district_code string, district_median double')
    fallback = spark.createDataFrame([(r['property_type_name'],float(r['median_price_vnd'])) for r in spec['fallback']], 'property_type_name string, type_median double')
    return df.join(F.broadcast(table),['property_type_name','district_code'],'left').join(F.broadcast(fallback),'property_type_name','left').withColumn('predicted_price_vnd',F.coalesce('district_median','type_median'))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--core',type=Path,default=ROOT/'data/processed/core_v1')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts/models/v1')
    args=parser.parse_args()
    output=args.output.resolve(); output.relative_to((ROOT/'artifacts/models').resolve())
    if output.exists(): raise FileExistsError('Use a fresh experiment output directory')
    cohort_manifest=json.loads((args.core/'manifest.json').read_text(encoding='utf-8'))
    output.mkdir(parents=True)
    def save(name,value): (output/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
    save('experiment_plan.json',{'created_at_utc':datetime.now(timezone.utc).isoformat(),'configs':CONFIGS,'feature_inputs':FEATURE_INPUTS,
        'selection_metric':'validation MAE in VND, per property type; ties by model ID',
        'label':'log(price_vnd)','baseline':'district/type median total price from train, min20; type fallback',
        'train_period':'2025-06..2025-11','validation_period':'2025-12','test_period':'2026-01..2026-03',
        'source_core_manifest_sha256':hashlib.sha256((args.core/'manifest.json').read_bytes()).hexdigest(),
        'code_sha256':{name:hashlib.sha256((ROOT/'src/models'/name).read_bytes()).hexdigest() for name in ['features.py','train.py']},
        'cohort_status':cohort_manifest['status']})
    spark=session('HCM-price-model-comparison'); started=time.perf_counter()
    try:
        raw=spark.read.parquet(str(args.core/'listings'))
        frame=prepare(raw.select('row_id','repost_group','split','price',*FEATURE_INPUTS)).withColumn('label',F.log('price')).persist(StorageLevel.DISK_ONLY)
        split_counts=[r.asDict() for r in frame.groupBy('split','property_type_name').count().collect()]
        save('split_counts.json',split_counts)
        train=frame.where("split='train'"); validation=frame.where("split='validation'")
        baseline=baseline_fit(train); save('baseline.json',baseline)
        rows=[]; model_objects={}; validation_predictions={}
        base_val=baseline_predict(validation,baseline,spark).persist(StorageLevel.DISK_ONLY)
        for kind,label in KINDS.items():
            rows.append({'id':'baseline','kind':kind,'validation':metrics(base_val.where(F.col('property_type_name')==label))})
        validation_predictions['baseline']=base_val
        for scope in ['house','apartment','common']:
            selected_train=train if scope=='common' else train.where(F.col('property_type_name')==KINDS[scope])
            selected_validation=validation if scope=='common' else validation.where(F.col('property_type_name')==KINDS[scope])
            prep=preprocessor(selected_train,common=scope=='common')
            transformed=prep.transform(selected_train).select('features','label').persist(StorageLevel.DISK_ONLY)
            print(f'Training {scope}: {transformed.count()} rows',flush=True)
            for algorithm,settings in CONFIGS.items():
                identifier=f'{scope}_{algorithm}'; tick=time.perf_counter()
                cls={'lr':LinearRegression,'rf':RandomForestRegressor,'gbt':GBTRegressor}[algorithm]
                reg=cls(featuresCol='features',labelCol='label',predictionCol='prediction',**settings).fit(transformed)
                pipeline=PipelineModel(stages=prep.stages+[reg]); pipeline.write().save(str(output/identifier))
                # Reload from disk to validate the exact artifact used by inference.
                loaded=PipelineModel.load(str(output/identifier)); model_objects[identifier]=loaded
                predicted=predict(loaded,selected_validation).persist(StorageLevel.DISK_ONLY)
                validation_predictions[identifier]=predicted
                for kind,label in KINDS.items():
                    if scope not in [kind,'common']: continue
                    rows.append({'id':identifier,'kind':kind,'validation':metrics(predicted.where(F.col('property_type_name')==label)),
                                 'fit_seconds':time.perf_counter()-tick})
                save('validation_results.json',rows)
                print(json.dumps(rows[-1],ensure_ascii=False),flush=True)
            transformed.unpersist()
        selected={kind:min([r for r in rows if r['kind']==kind],key=lambda r:(r['validation']['mae_vnd'],r['id']))['id'] for kind in KINDS}
        # Written before test is transformed/evaluated. No subsequent selection.
        save('selection.json',{'selected':selected,'metric':'validation_mae_vnd','test_used_for_selection':False})
        # Held-out multiplicative residual band learned from validation only;
        # empirical temporal-shift coverage, not a guaranteed 90% interval.
        bands={}
        for kind,identifier in selected.items():
            validation_frame=validation_predictions[identifier].where(F.col('property_type_name')==KINDS[kind])
            residual=F.abs(F.log(F.col('price')/F.col('predicted_price_vnd')))
            bands[kind]=float(validation_frame.agg(F.percentile_approx(residual,0.90,10000)).first()[0])
        save('residual_bands.json',{'log_radius':bands,'fit_split':'validation','nominal_fraction':0.90,'guaranteed_coverage':False})
        for df in validation_predictions.values(): df.unpersist()
        test=frame.where("split='test'")
        for identifier in ['baseline']+list(model_objects):
            predicted=baseline_predict(test,baseline,spark) if identifier=='baseline' else predict(model_objects[identifier],test)
            if identifier!='baseline' and not identifier.startswith('common_'):
                target_kind=identifier.split('_')[0]; predicted=predicted.where(F.col('property_type_name')==KINDS[target_kind])
            predicted=predicted.persist(StorageLevel.DISK_ONLY)
            for row in rows:
                if row['id']==identifier:
                    row['test']=metrics(predicted.where(F.col('property_type_name')==KINDS[row['kind']]))
            chosen=[kind for kind,item in selected.items() if item==identifier]
            for kind in chosen:
                part=predicted.where(F.col('property_type_name')==KINDS[kind]).withColumn('absolute_error_vnd',F.abs(F.col('price')-F.col('predicted_price_vnd')))
                part.select('row_id','property_type_name','district_code','area','price','predicted_price_vnd','absolute_error_vnd').write.mode('errorifexists').parquet(str(output/('test_predictions_'+kind)))
                radius=bands[kind]
                band_metrics=part.agg(F.avg((F.abs(F.log(F.col('price')/F.col('predicted_price_vnd')))<=radius).cast('double')).alias('test_empirical_coverage')).first().asDict()
                bands[kind]={'log_radius':radius,**band_metrics}
                breakdown=[]
                for district in sorted(r['district_code'] for r in part.select('district_code').distinct().collect()):
                    group=part.where(F.col('district_code')==district)
                    breakdown.append({'district_code':district,**metrics(group)})
                save('test_by_district_'+kind+'.json',breakdown)
                priced=part.withColumn('price_band', F.when(F.col('price')<3e9,'under_3b').when(F.col('price')<6e9,'3b_to_6b').when(F.col('price')<12e9,'6b_to_12b').otherwise('12b_plus'))
                save('test_by_price_'+kind+'.json',[{'price_band':band,**metrics(priced.where(F.col('price_band')==band))}
                    for band in sorted(r['price_band'] for r in priced.select('price_band').distinct().collect())])
                sampled=part.orderBy(F.sha2('row_id',256)).limit(300).select('area','price','predicted_price_vnd','district_code')
                save('scatter_'+kind+'.json',[r.asDict() for r in sampled.collect()])
            predicted.unpersist()
        save('results.json',{'models':rows,'selected':selected,'bands':bands,'split_counts':split_counts,
                             'elapsed_seconds':time.perf_counter()-started,'test_selection_locked':True,
                             'limitations':cohort_manifest['limitations']+['Asking prices, not verified transaction prices.','Log-price retransformation estimates a typical price.','Fixed small model comparison, no exhaustive tuning.','Same-asset duplicates with different text can remain.']})
        # Feature input limits are from train only, for API extrapolation signals.
        domain={}
        for kind,label in KINDS.items():
            part=train.where(F.col('property_type_name')==label)
            domain[kind]={'area_quantiles':part.approxQuantile('area',[0.01,0.99],0.001),
                          'districts':[r['district_code'] for r in part.select('district_code').distinct().collect()]}
        save('input_domain.json',domain)
        frame.unpersist(); print('Model comparison and saved-artifact inference complete',flush=True)
    finally: spark.stop()


if __name__=='__main__': main()
