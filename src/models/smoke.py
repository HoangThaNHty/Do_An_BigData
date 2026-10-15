"""Meaningful ML boundary checks: train medians, unseen categories, save/load."""
from pathlib import Path
import time
from pyspark.sql import types as T
from pyspark.ml import PipelineModel
from pyspark.ml.regression import LinearRegression
from src.config.spark import ROOT,session
from src.models.features import prepare,preprocessor,NUMERIC,FEATURE_INPUTS


def main():
    spark=session('model-boundary-smoke')
    try:
        schema=T.StructType([T.StructField(c,T.DoubleType() if c in NUMERIC+['area'] else T.StringType(),True) for c in FEATURE_INPUTS]+[T.StructField('label',T.DoubleType(),False)])
        rows=[]
        for i in range(12):
            rows.append(dict(property_type_name='Nhà',area=40.+i,bedroom_count=2. if i<7 else 4.,bathroom_count=2.,floor_count=None,frontage_width=4.,house_depth=None,road_width=None,district_code='769',ward_code='26734',project_name='A',label=22.+i*0.01))
        train=prepare(spark.createDataFrame(rows,schema)); prep=preprocessor(train,common=True)
        row={**rows[0],'area':80.,'bedroom_count':None,'project_name':'unseen','district_code':'999','ward_code':None,'label':30.}
        test=prepare(spark.createDataFrame([row],schema))
        transformed=prep.transform(test).first()
        assert transformed.bedroom_count_imputed==2.,transformed
        assert transformed.bedroom_count_missing==1.
        reg=LinearRegression(maxIter=10,regParam=0.1).fit(prep.transform(train))
        model=PipelineModel(stages=prep.stages+[reg])
        path=ROOT/'.runtime'/('model-smoke-'+str(time.time_ns()))
        model.write().save(str(path)); loaded=PipelineModel.load(str(path))
        a=model.transform(test).select('prediction').first()[0]
        b=loaded.transform(test).select('prediction').first()[0]
        assert abs(a-b)<1e-10
        print('PASS: train median, missing indicator, absent train columns, unseen categories, identical loaded-model prediction.')
    finally:spark.stop()


if __name__=='__main__':main()
