"""Verify the generated ZIP and run its extracted model using the existing runtime."""
import argparse,hashlib,json,os,shutil,subprocess,sys,zipfile
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    target=(args.output or ROOT/'.runtime'/('handoff_check_'+datetime.now().strftime('%Y%m%d_%H%M%S'))).resolve()
    target.relative_to((ROOT/'.runtime').resolve())
    if target.exists():raise FileExistsError('Use a new verification folder; do not overwrite.')
    target.mkdir()
    archive=ROOT/'deliverables/DO_AN_BIGDATA_NHOM18_BAN_GIAO.zip'
    with zipfile.ZipFile(archive) as z:
        manifest=json.loads(z.read('HANDOFF_MANIFEST.json'))
        for entry in manifest['files']:
            name=entry['path'];destination=(target/name).resolve();destination.relative_to(target.resolve())
            assert hashlib.sha256(z.read(name)).hexdigest()==entry['sha256']
        z.extractall(target)
    runtime=target/'.runtime';runtime.mkdir()
    shutil.copy2(ROOT/'.runtime/project-local-fs.jar',runtime/'project-local-fs.jar')
    env=dict(os.environ)
    java=(ROOT/'.runtime/java_home.txt').read_text().strip()
    env.update(JAVA_HOME=java,PATH=str(Path(java)/'bin')+os.pathsep+env['PATH'],
               PYSPARK_PYTHON=sys.executable,PYSPARK_DRIVER_PYTHON=sys.executable,
               PYSPARK_SUBMIT_ARGS='--driver-memory 2g pyspark-shell',SPARK_LOCAL_IP='127.0.0.1',
               PYTHONIOENCODING='utf-8',REAL_ESTATE_ROOT=str(target),
               TEMP=str(runtime/'temp'),TMP=str(runtime/'temp'),SPARK_LOCAL_DIRS=str(runtime/'spark-tmp'))
    (runtime/'temp').mkdir();(runtime/'spark-tmp').mkdir()
    check=subprocess.run([sys.executable,'-m','src.models.predict','--input','artifacts/models/v1/demo_input.json'],cwd=target,env=env,capture_output=True,text=True,encoding='utf-8',timeout=180)
    if check.returncode:raise RuntimeError(check.stdout+'\n'+check.stderr)
    (runtime/'prediction_stdout.txt').write_text(check.stdout,encoding='utf-8')
    prediction,_=json.JSONDecoder().raw_decode(check.stdout[check.stdout.index('{'):])
    assert prediction['model_id']=='apartment_lr'
    assert abs(prediction['estimated_asking_price_vnd']-3728469791.732773)/3728469791.732773<1e-6
    # New product pages must also work from the compact packaged artifacts,
    # without depending on the excluded full raw or ETL Parquet folders.
    packaged_data_check="""from types import SimpleNamespace
from src.api.main import Market
from src.api.explore import pipeline,search,reference,error_examples
market=Market()
request=SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(market=market)))
assert pipeline()['cohort_rows']==133779
assert search(request,kind='apartment',price_min=3e9,price_max=4e9,area_min=60,area_max=80,month=None,district_code=None)['data']['summary']['count']==14110
assert reference(request,kind='apartment',district_code='769',area=70)['count']>0
assert len(error_examples(request,kind='apartment')['rows'])==10
print('PASS: packaged pipeline, search, reference and error examples')
"""
    metadata_check=subprocess.run([sys.executable,'-c',packaged_data_check],cwd=target,env=env,capture_output=True,text=True,encoding='utf-8',timeout=60)
    if metadata_check.returncode:raise RuntimeError(metadata_check.stdout+'\n'+metadata_check.stderr)
    report={'passed':True,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'files_verified':len(manifest['files']),
            'method':'Extracted source + saved model at a new path; original Python/JDK runtime reused, no retraining.',
            'prediction':prediction,'product_v4_packaged_data':True}
    (ROOT/'artifacts/verification/handoff_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS: extracted package inference, verified fingerprints, same real prediction at a new path.')

if __name__=='__main__':main()
