"""Export a compact analysis table and train-only input catalog for the API."""
import argparse,json
from pathlib import Path
from pyspark.sql import functions as F
from src.config.spark import ROOT,session


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--core',type=Path,default=ROOT/'data/processed/core_v1')
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts/market/serving')
    args=parser.parse_args()
    manifest=json.loads((args.core/'manifest.json').read_text(encoding='utf-8'))
    output=args.output.resolve()
    output.relative_to((ROOT/'artifacts').resolve())
    if output.exists():raise FileExistsError('Preserve exported analysis artifact')
    spark=session('compact-market-serving-export')
    try:
        data=spark.read.parquet(str(args.core/'listings'))
        # No full ad texts, phones, exact street addresses or row IDs exposed.
        columns=['property_type_name','district_code','district_label','published_month','area','price','unit_price_vnd']
        data.select(*columns).coalesce(2).write.mode('errorifexists').parquet(str(output))
        saved=spark.read.parquet(str(output))
        assert saved.count()==manifest['cohort_rows']
        train=data.where("split='train'")
        wards=[r.asDict() for r in train.where('ward_code IS NOT NULL').groupBy('property_type_name','district_code','ward_code','ward_name').count().collect()]
        projects=[r.asDict() for r in train.where("project_name IS NOT NULL AND trim(project_name) != ''").groupBy('property_type_name','district_code','project_name').count().collect()]
        (output.parent/'input_catalog.json').write_text(json.dumps({'fit_split':'train','wards':wards,'projects':projects},ensure_ascii=False,indent=2),encoding='utf-8')
        overview=[r.asDict() for r in data.groupBy('property_type_name').agg(F.count('*').alias('count'),F.percentile_approx('price',.5,10000).alias('median_price_vnd'),F.percentile_approx('area',.5,10000).alias('median_area_m2'),F.percentile_approx('unit_price_vnd',.5,10000).alias('median_unit_price_vnd')).collect()]
        (output.parent/'overview.json').write_text(json.dumps(overview,ensure_ascii=False,indent=2),encoding='utf-8')
        (output.parent/'metadata.json').write_text(json.dumps({'core_manifest':manifest,'analysis_columns':columns,'analysis_rows':manifest['cohort_rows'],'period':'2025-06..2026-03','source':'oceanNG/vietnam-real-estates','asking_prices_only':True,'geometry_year':2020,'administrative_reference':'pre-merger 2025, 22 historical district groups'},ensure_ascii=False,indent=2),encoding='utf-8')
        print(f'Exported compact analysis: {manifest["cohort_rows"]} rows; train-only input catalog.',flush=True)
    finally:spark.stop()


if __name__=='__main__':main()
