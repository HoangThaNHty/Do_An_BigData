"""Verify served aggregates against Parquet and saved inference via the web proxy."""
import argparse,json,math,urllib.request,urllib.error
from pathlib import Path
import numpy as np
import pyarrow.dataset as ds

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--base',default='http://127.0.0.1:3000');args=parser.parse_args()
    checks=[]
    def call(path,payload=None,status=200):
        body=json.dumps(payload).encode() if payload is not None else None
        req=urllib.request.Request(args.base+'/api/v1/'+path,data=body,headers={'Content-Type':'application/json'})
        try:
            with urllib.request.urlopen(req,timeout=90) as r: actual=r.status;data=json.load(r)
        except urllib.error.HTTPError as e: actual=e.code;data=json.load(e)
        assert actual==status,(path,actual,data)
        checks.append({'path':path,'status':actual});return data
    table=ds.dataset(str(ROOT/'artifacts/market/serving'),format='parquet').to_table()
    arrays={c:np.asarray(table[c].to_pylist()) for c in table.column_names}
    assert call('health')['analysis_rows']==table.num_rows
    for kind,label in [('house','Nhà'),('apartment','Căn hộ chung cư')]:
        for district,month in [(None,None),('769',None),('769','2026-01')]:
            query='kind='+kind+('&district_code='+district if district else '')+('&month='+month if month else '')
            mask=arrays['property_type_name']==label
            if district:mask&=arrays['district_code']==district
            if month:mask&=arrays['published_month']==month
            result=call('overview?'+query)['data'];assert result['count']==int(mask.sum())
            for key,column in [('median_price_vnd','price'),('median_area_m2','area'),('median_unit_price_vnd','unit_price_vnd')]:
                assert result[key]==(float(np.median(arrays[column][mask])) if mask.any() else None),(query,key)
            assert sum(r['count'] for r in result['area_histogram'])==result['count']
            assert sum(r['count'] for r in call('market/trends?'+query)['data'])==result['count']
            assert sum(r['count'] for r in call('market/districts?'+query)['data'])==result['count']
        geo=call('map/districts?kind='+kind)['data'];assert len(geo['features'])==22
        assert sum(f['properties']['count'] for f in geo['features'])==int((arrays['property_type_name']==label).sum())
        filters=call('filters?kind='+kind+'&district_code=769');assert filters['catalog_split']=='train'
        assert all(r['district_code']=='769' for r in filters['wards'])
        pred=call('predict',{'kind':kind,'area':70,'district_code':'769','bedroom_count':2,'bathroom_count':2})
        assert math.isfinite(pred['estimated_asking_price_vnd'])
        assert pred['reference_range_vnd'][0]<pred['estimated_asking_price_vnd']<pred['reference_range_vnd'][1]
    base={'kind':'apartment','area':70,'district_code':'769'}
    for change in [{'area':0},{'area':10001},{'district_code':'999'},{'ward_code':'99999'},{'kind':'land'},{'price':123},{'bedroom_count':-2}]:
        call('predict',{**base,**change},status=422)
    call('overview?kind=house&month=2024-01',status=422)
    call('overview?kind=land',status=422)
    metrics=call('models/metrics');assert metrics['selected']==json.loads((ROOT/'artifacts/models/v1/selection.json').read_text())['selected']
    output=ROOT/'artifacts/verification';output.mkdir(exist_ok=True)
    (output/'api_checks.json').write_text(json.dumps({'base':args.base,'checks':checks,'count':len(checks),'passed':True},indent=2),encoding='utf-8')
    print(f'PASS: {len(checks)} API calls, exact Parquet medians, counts, map, saved models and invalid input checks.')

if __name__=='__main__':main()
