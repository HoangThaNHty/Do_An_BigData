"""Research-cohort search and educational diagnostics; no personal listing data."""
import json
from py4j.protocol import Py4JError
import copy
import unicodedata
import numpy as np
import pyarrow.dataset as ds
from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from src.config.spark import ROOT

router=APIRouter(prefix='/api/v1')


@router.get('/map/explore')
def map_explore(request:Request,kind:Literal['house','apartment']='apartment',month:str|None=None,
                price_min:float=Query(0,ge=0,le=1e15),price_max:float=Query(1e15,gt=0,le=1e15),
                area_min:float=Query(0,ge=0,le=10000),area_max:float=Query(10000,gt=0,le=10000)):
    if price_min>price_max or area_min>area_max:raise HTTPException(422,'Cận dưới phải nhỏ hơn hoặc bằng cận trên.')
    m=request.app.state.market;mask=m.mask(kind,None,month)
    mask &= (m.data['price']>=price_min)&(m.data['price']<=price_max)&(m.data['area']>=area_min)&(m.data['area']<=area_max)
    geometry=copy.deepcopy(m.geometry)
    for feature in geometry['features']:
        part=mask&(m.data['district_code']==feature['properties']['district_code'])
        feature['properties'].update(m.summary(part),small_sample=int(part.sum())<20)
    return m.envelope(kind,None,month,geometry)


def quantiles(market, mask):
    prices=market.data['price'][mask]
    return {'price_quartiles_vnd':[float(v) for v in np.quantile(prices,[.25,.5,.75])] if len(prices) else None}


@router.get('/market/search')
def search(request:Request, kind:Literal['house','apartment']='apartment',
           price_min:float=Query(0,ge=0,le=1e15),price_max:float=Query(1e15,gt=0,le=1e15),
           area_min:float=Query(0,ge=0,le=10000),area_max:float=Query(10000,gt=0,le=10000),
           month:str|None=None,district_code:str|None=None):
    if price_min>price_max or area_min>area_max:raise HTTPException(422,'Cận dưới phải nhỏ hơn hoặc bằng cận trên.')
    m=request.app.state.market;mask=m.mask(kind,district_code,month)
    mask &= (m.data['price']>=price_min)&(m.data['price']<=price_max)&(m.data['area']>=area_min)&(m.data['area']<=area_max)
    rows=[]
    for code,label in m.districts:
        part=mask&(m.data['district_code']==code)
        if part.any():rows.append({'district_code':code,'district_label':label,**m.summary(part),**quantiles(m,part),'small_sample':int(part.sum())<20})
    rows.sort(key=lambda r:(-r['count'],r['district_code']))
    return m.envelope(kind,district_code,month,{'summary':m.summary(mask),'districts':rows,
        'criteria':{'price_min':price_min,'price_max':price_max,'area_min':area_min,'area_max':area_max},
        'listing_availability':'historical_not_verified_available','counts_are_unique_properties':False})


@router.get('/market/reference')
def reference(request:Request,kind:Literal['house','apartment'],district_code:str,
              area:float=Query(gt=0,le=10000)):
    m=request.app.state.market;mask=m.mask(kind,district_code,None)
    # Fixed visible criterion, no silent widening when few rows match.
    lo,hi=area*.85,area*1.15;mask &= (m.data['area']>=lo)&(m.data['area']<=hi)
    return {'kind':kind,'district_code':district_code,'area_range_m2':[lo,hi],
        **m.summary(mask),**quantiles(m,mask),'small_sample':int(mask.sum())<20,
        'criteria':'Cùng loại hình, khu vực lịch sử và diện tích ±15%; không lọc dự án, phòng, pháp lý hay tình trạng.',
        'period':'06/2025–03/2026','source':'selected_research_cohort_not_current_listings'}


def normalized(value):
    return ''.join(c for c in unicodedata.normalize('NFD',value.lower().replace('đ','d')) if unicodedata.category(c)!='Mn').strip()


@router.get('/geography/lookup')
def geography(request:Request,q:str=Query(min_length=2,max_length=120)):
    m=request.app.state.market;query=normalized(q);hits=[]
    for code,label in m.districts:
        if query in normalized(label):hits.append({'district_code':code,'label':label,'match':'historical_district'})
    if query in ['quan 2','q2','quan 9','q9','thu duc','tp thu duc']:
        hits=[{'district_code':'769','label':'Thành phố Thủ Đức (nhóm nghiên cứu lịch sử)','match':'historical_group',
            'note':'Quận 2, Quận 9 và Thủ Đức cũ được gộp; không xác định phường hiện hành từ tên quận.'}]
    seen=set()
    for row in m.catalog['wards']:
        key=(row['district_code'],row['ward_code'])
        if query in normalized(row['ward_name']) and key not in seen:
            seen.add(key);hits.append({'district_code':row['district_code'],'ward_code':row['ward_code'],
                'label':row['ward_name'],'match':'historical_ward',
                'district_label':dict(m.districts).get(row['district_code'])})
    return {'matches':hits[:30],'total_matches':len(hits),'mapping_status':'historical_lookup_only',
        'notice':'Tên có thể trùng phường hiện hành. Đây là tra cứu địa danh lịch sử, chưa phải chuyển đổi địa chỉ mới/cũ. Không có GPS để phân giải địa bàn bị chia tách.',
        'scope':'Phạm vi TP.HCM trước hợp nhất; chưa bao phủ Bình Dương và Bà Rịa–Vũng Tàu cũ.',
        'period':'06/2025–03/2026','last_listing_month':'2026-03'}


@router.get('/models/error-examples')
def error_examples(request:Request,kind:Literal['house','apartment']='apartment'):
    # Saved selected model predictions on test, no retuning or personal fields.
    table=ds.dataset(str(ROOT/f'artifacts/models/v1/test_predictions_{kind}'),format='parquet').to_table(
        columns=['district_code','area','price','predicted_price_vnd','absolute_error_vnd'])
    idx=np.argsort(np.asarray(table['absolute_error_vnd']))[-10:][::-1]
    rows=table.to_pylist();labels=dict(request.app.state.market.districts)
    return {'model_id':request.app.state.market.results['selected'][kind],
        'rows':[{**rows[int(i)],'district_label':labels.get(str(rows[int(i)]['district_code'])),
                 'absolute_percentage_error':rows[int(i)]['absolute_error_vnd']/rows[int(i)]['price']} for i in idx],
        'source':'largest_absolute_errors_selected_model_test','prices_verified':False}


@router.get('/method/pipeline')
def pipeline():
    etl=json.loads((ROOT/'artifacts/etl/etl_v4/summary.json').read_text(encoding='utf-8'))
    core=json.loads((ROOT/'data/processed/core_v1/manifest.json').read_text(encoding='utf-8'))
    results=json.loads((ROOT/'artifacts/models/v1/results.json').read_text(encoding='utf-8'))
    return {'source_rows':etl['source_rows'],'unique_source_rows':etl['unique_source_records'],
        'routes':etl['dispositions'],'protected_rows':core['protected_before_geo'],
        'review_excluded_rows':core['protected_before_geo']-core['protected_after_review_exclusion'],
        'removed_reposts_or_outside_period':core['removed_reposts_or_outside_period'],
        'cohort_rows':core['cohort_rows'],'split_counts':core['split_counts'],
        'selected':results['selected'],'training_seconds':results['elapsed_seconds'],
        'spark_master':'local[4]','dataset_license':'CC BY-NC 4.0','reference_labels':'AI_not_independent_human_ground_truth'}


class ListingCheck(BaseModel):
    model_config=ConfigDict(extra='forbid',allow_inf_nan=False)
    kind:Literal['house','apartment']='apartment'
    title:str=Field(min_length=1,max_length=300)
    description:str=Field(default='',max_length=10000)
    price:float=Field(gt=0,le=1e15)
    area:float=Field(gt=0,le=10000)


@router.post('/method/check-listing')
def check_listing(request:Request,inputs:ListingCheck):
    from pyspark.sql.types import StructType,StructField,StringType,DoubleType
    from src.etl.rules import enrich
    from src.etl.quality import check
    from src.api.main import lock
    if not lock.acquire(timeout=1):raise HTTPException(429,'Spark đang bận. Thử lại sau ít giây.')
    try:
        strings=['name','description','property_type_name','province_name','district_name','ward_name','published_at','price']
        numerics=['area','floor_count','frontage_width','house_depth','road_width','bedroom_count','bathroom_count']
        schema=StructType([StructField(c,StringType(),True) for c in strings]+[StructField(c,DoubleType(),True) for c in numerics])
        row={c:None for c in strings+numerics}
        row.update(name=inputs.title,description=inputs.description,property_type_name='Nhà' if inputs.kind=='house' else 'Căn hộ chung cư',
            province_name='Hồ Chí Minh',district_name='Thủ Đức',ward_name='',published_at='2025-10-01',price=str(inputs.price),area=inputs.area)
        df=request.app.state.spark.createDataFrame([row],schema)
        result=check(enrich(df)).select('transaction_label','transaction_reason','area_kind','area_evidence',
            'price_check','area_check','scope_check','quality_reasons','protected_candidate','residential_scope_reason').first().asDict()
        return {**result,'saved':False,'example_location_and_date':'Địa bàn Thủ Đức và ngày 01/10/2025 cố định chỉ để chạy minh họa quy tắc; không xác minh địa chỉ/ngày của nội dung nhập.',
            'notice':'Chạy bộ quy tắc ETL thực bằng Spark, không phát hiện tin giả và không tự thêm nội dung vào tập huấn luyện.'}
    except (ConnectionError, Py4JError) as error:
        raise HTTPException(503,'Spark không còn sẵn sàng. Dừng phiên cũ rồi khởi động lại API để phân tích tin.') from error
    finally:lock.release()
