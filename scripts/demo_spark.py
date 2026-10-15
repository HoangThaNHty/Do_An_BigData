"""Read-only guided Spark demo. Training results are explicitly saved evidence."""
import argparse
import json
from urllib.parse import urlsplit

from pyspark.sql import functions as F
from src.config.spark import ROOT, session


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-pause', action='store_true', help='Run verification without interactive stops')
    args = parser.parse_args()
    spark = session('HCM-demo-data-ETL-split')

    def step(name, description):
        spark.sparkContext.setJobGroup(name, description)
        print('\n' + name + ': ' + description, flush=True)

    def pause():
        url = spark.sparkContext.uiWebUrl
        local_url = f'http://127.0.0.1:{urlsplit(url).port}' if url else 'disabled'
        print('Spark UI (on this machine): ' + local_url, flush=True)
        if not args.no_pause:
            input('Xem Spark UI / trinh bay, sau do nhan Enter de tiep tuc... ')

    try:
        print('Master:', spark.sparkContext.master, 'Spark:', spark.version, flush=True)
        step('01-SOURCE', 'Read all raw Parquet and count actual source/scope records')
        paths = sorted((ROOT/'data/raw/oceanng').glob('shard_*.parquet'))
        if len(paths) != 10:
            raise FileNotFoundError('Research-machine demo requires all 10 raw shards, not just clone serving.')
        raw = spark.read.parquet(*[str(p) for p in paths])
        raw.printSchema()
        count = raw.count()
        assert count == 3500744 and len(raw.columns) == 19, (count, len(raw.columns))
        scope = raw.where((F.col('province_name') == 'Hồ Chí Minh') & F.col('property_type_name').isin('Nhà', 'Căn hộ chung cư'))
        scope_count = scope.count()
        assert scope_count == 1122870, scope_count
        print(f'All source: {count:,}; HCM houses/apartments: {scope_count:,}', flush=True)
        scope.select('property_type_name','province_name','district_name','price','area','published_at').show(5, truncate=35)
        pause()
        step('02-ETL-OUTPUT', 'Read persisted ETL output and group actual dispositions; NOT rerunning ETL')
        etl = spark.read.parquet(str(ROOT/'data/processed/etl_v4/listings'))
        etl.groupBy('disposition').count().orderBy('disposition').show(truncate=False)
        print('Rules: src/etl/rules.py; quality: src/etl/quality.py; execution: src/etl/build.py', flush=True)
        pause()
        step('03-TEMPORAL-SPLIT', 'Read cohort and count actual train/validation/test by month/type')
        core = spark.read.parquet(str(ROOT/'data/processed/core_v1/listings'))
        core.groupBy('split','property_type_name').count().orderBy('split','property_type_name').show(truncate=False)
        core.groupBy('split','published_month').count().orderBy('published_month','split').show(30, truncate=False)
        actual = {r['split']:r['count'] for r in core.groupBy('split').count().collect()}
        assert actual == {'train':78048, 'validation':17886, 'test':37845}, actual
        pause()
        step('04-SAVED-EXPERIMENT', 'Inspect saved training/evaluation evidence; NOT live training')
        models = ROOT/'artifacts/models/v1'
        selection = json.loads((models/'selection.json').read_text(encoding='utf-8'))
        results = json.loads((models/'results.json').read_text(encoding='utf-8'))
        print(json.dumps(selection, ensure_ascii=False, indent=2), flush=True)
        for row in results['models']:
            if row['id'] == selection['selected'][row['kind']]:
                print(row['id'], 'validation:', row['validation'], 'test:', row['test'], flush=True)
        print('Training source: src/models/train.py; saved pipelines: artifacts/models/v1', flush=True)
        print('No new Spark training jobs in this step. For real training use a fresh --output experiment.', flush=True)
        pause()
        print('DEMO PASS. This Spark context will stop. Start API next; API creates its own Spark context.', flush=True)
    finally:
        spark.stop()


if __name__ == '__main__':
    main()
