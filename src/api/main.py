"""Local/LAN API: compact analytics and one resident Spark inference worker."""
from contextlib import asynccontextmanager
from functools import lru_cache
import copy
import json
import os
import logging
import signal
import threading
import time
from typing import Literal
import numpy as np
import pyarrow.dataset as ds
from fastapi import FastAPI,HTTPException,Query
from pydantic import BaseModel,ConfigDict,Field
from src.config.spark import ROOT,session
from src.models.inference import Estimator
from py4j.protocol import Py4JError

KINDS={'house':'Nhà','apartment':'Căn hộ chung cư'}
lock=threading.Lock()


def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))


class Market:
    def __init__(self):
        table=ds.dataset(str(ROOT/'artifacts/market/serving'),format='parquet').to_table()
        self.data={c:np.asarray(table[c].to_pylist()) for c in table.column_names}
        self.metadata=read('artifacts/market/metadata.json')
        self.results=read('artifacts/models/v1/results.json')
        self.catalog=read('artifacts/market/input_catalog.json')
        self.geometry=read('artifacts/geography/hcm_districts.geojson')
        self.months=sorted(set(self.data['published_month']))
        self.districts=sorted({(str(code),str(label)) for code,label in zip(self.data['district_code'],self.data['district_label'])},key=lambda x:x[1])

    def mask(self,kind,district,month):
        if district and district not in [r[0] for r in self.districts]:raise HTTPException(422,'Khu vực không được hỗ trợ.')
        if month and month not in self.months:raise HTTPException(422,'Tháng không nằm trong dữ liệu nghiên cứu.')
        selected=self.data['property_type_name']==KINDS[kind]
        if district:selected&=self.data['district_code']==district
        if month:selected&=self.data['published_month']==month
        return selected

    def summary(self,mask):
        n=int(np.count_nonzero(mask))
        return {'count':n,'median_price_vnd':float(np.median(self.data['price'][mask])) if n else None,
                'median_area_m2':float(np.median(self.data['area'][mask])) if n else None,
                'median_unit_price_vnd':float(np.median(self.data['unit_price_vnd'][mask])) if n else None}

    def envelope(self,kind,district,month,data):
        return {'scope':'Tập tin rao bán được chọn tại 22 nhóm địa bàn TP.HCM trước hợp nhất 2025',
                'data_version':'core_v1','kind':kind,'district_code':district,'month':month,
                'period':'06/2025–03/2026','asking_prices_only':True,'data':data}


@asynccontextmanager
async def lifespan(app):
    app.state.market=Market()
    # Spark installs its own SIGINT handler. Keep Uvicorn's handler so Ctrl+C
    # requests a normal API shutdown rather than interrupting the event loop.
    api_sigint=signal.getsignal(signal.SIGINT)
    try:
        app.state.spark=session('HCM-web-inference')
    finally:
        signal.signal(signal.SIGINT,api_sigint)
    try:
        app.state.estimator=Estimator(app.state.spark,ROOT/'artifacts/models/v1')
        yield
    finally:
        try:
            app.state.spark.stop()
        except (Py4JError,OSError):
            # Windows console Ctrl+C can also terminate the Java child process.
            logging.getLogger(__name__).warning('Spark JVM already disconnected during API shutdown.')


app=FastAPI(title='Nhà ở TP.HCM — Giá rao bán',version='1.2.1',lifespan=lifespan)
from src.api.explore import router as explore_router
app.include_router(explore_router)
from src.api.tiles import router as tiles_router
app.include_router(tiles_router)


@app.middleware('http')
async def local_connection_lifetime(request,call_next):
    response=await call_next(request)
    # The local Next/httpxy proxy can reuse an idle socket just as Uvicorn
    # expires it, causing intermittent ECONNRESET during A/B requests.
    # Close each backend connection explicitly for this single-worker LAN API.
    response.headers['Connection']='close'
    return response


@app.get('/api/v1/health')
def health():
    spark=getattr(app.state,'spark',None)
    try:
        if spark is None or spark.sparkContext._jsc is None or spark.sparkContext._jsc.sc().isStopped():
            raise HTTPException(503,'Spark chưa sẵn sàng hoặc đã dừng. Khởi động lại API để ước tính/phân tích tin.')
    except (Py4JError,OSError) as error:
        raise HTTPException(503,'Không kết nối được Spark. Dừng phiên cũ rồi khởi động lại API.') from error
    return {'status':'ready','data_version':'core_v1','model_version':'v1','analysis_rows':len(app.state.market.data['price'])}


@app.get('/api/v1/metadata')
def metadata():return app.state.market.metadata


@app.get('/api/v1/filters')
def filters(kind:Literal['house','apartment']='apartment',district_code:str|None=None):
    market=app.state.market
    market.mask(kind,district_code,None)
    wards=[r for r in market.catalog['wards'] if r['property_type_name']==KINDS[kind] and (not district_code or r['district_code']==district_code)]
    projects=[r for r in market.catalog['projects'] if r['property_type_name']==KINDS[kind] and (not district_code or r['district_code']==district_code)]
    return {'kinds':KINDS,'months':market.months,'districts':[{'code':c,'label':n} for c,n in market.districts],
            'wards':sorted(wards,key=lambda x:x['ward_name']),'projects':sorted(projects,key=lambda x:x['project_name']),
            'catalog_split':'train','area_input_basis':{'house':'Diện tích đất (m²)','apartment':'Diện tích căn hộ (m²); nhập cùng cơ sở đo của tin nguồn'}}


@app.get('/api/v1/overview')
def overview(kind:Literal['house','apartment']='apartment',district_code:str|None=None,month:str|None=None):
    market=app.state.market;mask=market.mask(kind,district_code,month)
    summary=market.summary(mask)
    # Histograms include open-ended tails; no silently discarded expensive ads.
    edges=[0,30,50,70,90,120,160,250,np.inf]
    values=np.histogram(market.data['area'][mask],bins=edges)[0]
    summary['area_histogram']=[{'label':f'{edges[i]}–{edges[i+1]}' if i<len(edges)-2 else '250+', 'count':int(v)} for i,v in enumerate(values)]
    return market.envelope(kind,district_code,month,summary)


@app.get('/api/v1/market/trends')
def trends(kind:Literal['house','apartment']='apartment',district_code:str|None=None,month:str|None=None):
    market=app.state.market;mask=market.mask(kind,district_code,month)
    rows=[{'month':m,**market.summary(mask&(market.data['published_month']==m))} for m in market.months if not month or m==month]
    return market.envelope(kind,district_code,month,rows)


@app.get('/api/v1/market/districts')
def districts(kind:Literal['house','apartment']='apartment',district_code:str|None=None,month:str|None=None):
    market=app.state.market;mask=market.mask(kind,district_code,month)
    rows=[{'district_code':c,'district_label':n,**market.summary(mask&(market.data['district_code']==c))} for c,n in market.districts if not district_code or c==district_code]
    for row in rows:row['small_sample']=row['count']<20
    rows.sort(key=lambda x:-(x['median_unit_price_vnd'] or 0))
    return market.envelope(kind,district_code,month,rows)


@app.get('/api/v1/map/districts')
def map_districts(kind:Literal['house','apartment']='apartment',month:str|None=None):
    market=app.state.market;values={r['district_code']:r for r in districts(kind,None,month)['data']}
    geo=copy.deepcopy(market.geometry)
    for feature in geo['features']:feature['properties'].update(values.get(feature['properties']['district_code'],{}))
    return market.envelope(kind,None,month,geo)


@app.get('/api/v1/models/metrics')
def model_metrics():
    return {'model_version':'v1',**app.state.market.results}


@app.get('/api/v1/models/diagnostics')
def model_diagnostics(kind:Literal['house','apartment']='apartment'):
    return {'districts':read('artifacts/models/v1/test_by_district_'+kind+'.json'),
            'price_bands':read('artifacts/models/v1/test_by_price_'+kind+'.json'),
            'scatter':read('artifacts/models/v1/scatter_'+kind+'.json')}


class PredictionInput(BaseModel):
    model_config=ConfigDict(extra='forbid',allow_inf_nan=False)
    kind:Literal['house','apartment']
    area:float=Field(gt=0,le=10000)
    district_code:str=Field(pattern=r'^\d{3}$')
    ward_code:str|None=Field(default=None,pattern=r'^\d{5}$')
    project_name:str|None=Field(default=None,max_length=200)
    bedroom_count:float|None=Field(default=None,gt=0,le=50)
    bathroom_count:float|None=Field(default=None,gt=0,le=50)
    floor_count:float|None=Field(default=None,gt=0,le=100)
    frontage_width:float|None=Field(default=None,gt=0,le=1000)
    house_depth:float|None=Field(default=None,gt=0,le=1000)
    road_width:float|None=Field(default=None,gt=0,le=1000)


@app.post('/api/v1/predict')
def estimate(inputs:PredictionInput):
    market=app.state.market;data=inputs.model_dump()
    market.mask(inputs.kind,inputs.district_code,None)
    if inputs.ward_code and not any(r['ward_code']==inputs.ward_code and r['district_code']==inputs.district_code and r['property_type_name']==KINDS[inputs.kind] for r in market.catalog['wards']):
        raise HTTPException(422,'Phường không có hỗ trợ trong tập train của khu vực và loại hình đã chọn.')
    if not lock.acquire(timeout=1):raise HTTPException(429,'Đang xử lý một ước tính khác. Vui lòng thử lại sau ít giây.')
    tick=time.perf_counter()
    try:
        result=app.state.estimator.estimate(data)
        project=(inputs.project_name or '').strip().casefold()
        if project and not any(r['project_name'].strip().casefold()==project and r['district_code']==inputs.district_code and r['property_type_name']==KINDS[inputs.kind] for r in market.catalog['projects']):
            result['warnings'].append('Dự án chưa có hỗ trợ tại khu vực trong tập train; ước tính dùng nhóm dự án chưa thấy.')
        result.update(model_version='v1',data_version='core_v1',data_period='06/2025–03/2026',elapsed_ms=round((time.perf_counter()-tick)*1000))
        return result
    except (ValueError,OverflowError) as error:raise HTTPException(422,str(error)) from error
    except (Py4JError,ConnectionError) as error:
        raise HTTPException(503,'Spark không còn sẵn sàng. Dừng phiên cũ rồi khởi động lại API để ước tính.') from error
    finally:lock.release()
