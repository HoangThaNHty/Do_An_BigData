"""Verify new user tasks against Parquet and frozen Spark rules, through web proxy."""
import argparse,hashlib,json,urllib.request,urllib.error
from pathlib import Path
import numpy as np
import pyarrow.dataset as ds

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--base',default='http://127.0.0.1:3000');args=parser.parse_args()
    calls=[]
    def call(path,payload=None,status=200):
        req=urllib.request.Request(args.base+'/api/v1/'+path,data=json.dumps(payload).encode() if payload is not None else None,headers={'Content-Type':'application/json'})
        try:
            with urllib.request.urlopen(req,timeout=90) as r:code=r.status;data=json.load(r)
        except urllib.error.HTTPError as e:code=e.code;data=json.load(e)
        assert code==status,(path,code,data);calls.append({'path':path,'status':code});return data
    table=ds.dataset(str(ROOT/'artifacts/market/serving'),format='parquet').to_table()
    arr={c:np.asarray(table[c].to_pylist()) for c in table.column_names}
    for kind,label in [('apartment','Căn hộ chung cư'),('house','Nhà')]:
        for limits in [(3e9,4e9,60,80),(0,1e15,0,10000),(3e9,3e9,70,70)]:
            low,high,amin,amax=limits
            query=f'kind={kind}&price_min={low}&price_max={high}&area_min={amin}&area_max={amax}'
            mask=(arr['property_type_name']==label)&(arr['price']>=low)&(arr['price']<=high)&(arr['area']>=amin)&(arr['area']<=amax)
            result=call('market/search?'+query)['data'];assert result['summary']['count']==int(mask.sum())
            assert sum(r['count'] for r in result['districts'])==int(mask.sum())
            for r in result['districts']:
                part=mask&(arr['district_code']==r['district_code']);assert r['count']==int(part.sum())
                assert np.allclose(r['price_quartiles_vnd'],np.quantile(arr['price'][part],[.25,.5,.75]))
            geo=call('map/explore?'+query)['data'];assert len(geo['features'])==22
            assert sum(f['properties']['count'] for f in geo['features'])==int(mask.sum())
        for area in [70,10000]:
            ref=call(f'market/reference?kind={kind}&district_code=769&area={area}')
            mask=(arr['property_type_name']==label)&(arr['district_code']=='769')&(arr['area']>=area*.85)&(arr['area']<=area*1.15)
            assert ref['count']==int(mask.sum());assert ref['small_sample']==(int(mask.sum())<20)
        errors=call('models/error-examples?kind='+kind)['rows'];saved=ds.dataset(str(ROOT/f'artifacts/models/v1/test_predictions_{kind}'),format='parquet').to_table()
        expected=np.sort(np.asarray(saved['absolute_error_vnd']))[-10:][::-1]
        assert np.allclose([r['absolute_error_vnd'] for r in errors],expected)
        assert all('row_id' not in r and 'description' not in r for r in errors)
    for route in ['market/search','map/explore']:
        for q in ['price_min=5&price_max=3','area_min=80&area_max=60','price_min=-1','area_max=inf','kind=land','month=2020-01']:
            call(route+'?'+q,status=422)
    for q in ['area=0&district_code=769','area=inf&district_code=769','area=70&district_code=999']:
        call('market/reference?kind=house&'+q,status=422)
    assert call('geography/lookup?q=Quan%209')['matches'][0]['district_code']=='769'
    assert call('geography/lookup?q=unknownxyz')['matches']==[]
    assert call('geography/lookup?q=Thu%20Duc')['mapping_status']=='historical_lookup_only'
    pipeline=call('method/pipeline');assert pipeline['cohort_rows']==133779
    assert sum(r['count'] for r in pipeline['routes'])==1122868
    assert sum(r['count'] for r in pipeline['split_counts'])==133779
    examples=[('sale','Bán căn hộ 70m2, 2 phòng ngủ','Chính chủ bán căn hộ diện tích 70m2, 2 phòng ngủ, 2 WC. Giá bán 3.5 tỷ.',3.5e9),
        ('rent','Cho thuê căn hộ 70m2','Cho thuê căn hộ diện tích 70m2. Giá thuê 12 triệu/tháng.',12e6),
        ('sale','Bán căn hộ 70m2 chỉ cần trả trước 500 triệu','Căn hộ diện tích 70m2, 2 phòng ngủ. Giá bán 3.5 tỷ, chỉ cần trả trước 500 triệu.',.5e9)]
    for expected,title,body,price in examples:
        result=call('method/check-listing',{'title':title,'description':body,'price':price,'area':70})
        assert result['transaction_label']==expected,result
        if price!=3.5e9:assert not result['protected_candidate'],result
        assert result['saved'] is False
    call('method/check-listing',{'title':'test','price':1,'area':70,'description':'x'*10001},status=422)
    frozen={'rules.py':'a2b7d760d9507f807edfbae6d414b575235ef399376581d018fda35b01a35b8e','quality.py':'715b5b317087f9f347813d029f6114df7743dc3374dc158d46b9f5d58beb92d4'}
    for name,digest in frozen.items():assert hashlib.sha256((ROOT/'src/etl'/name).read_bytes()).hexdigest()==digest
    receipt={'passed':True,'base':args.base,'calls':calls,'count':len(calls),'checks':['search exact Parquet counts/quartiles/inclusive bounds','map-search coherence','reference no silent widening','actual largest test absolute errors','invalid input','historical geographic lookup','manifest accounting','Spark ETL examples','frozen methodology hashes']}
    (ROOT/'artifacts/verification/product_features_api.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    print(f'PASS: {len(calls)} calls for product features and frozen ETL methodology.')


if __name__=='__main__':main()
