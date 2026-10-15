"""On-demand local demo tile relay; no prefetch and no distributable tile archive."""
import json
import math
import os
import threading
import time
from pathlib import Path
import requests
from fastapi import APIRouter,HTTPException,Request
from fastapi.responses import Response
from src.config.spark import ROOT

router=APIRouter(prefix='/api/v1/map')
cache_root=ROOT/'.runtime/tile-cache'
locks=[threading.Lock() for _ in range(32)]
PNG=b'\x89PNG\r\n\x1a\n'


def ttl(headers):
    import re
    from email.utils import parsedate_to_datetime
    match=re.search(r'(?:s-maxage|max-age)=(\d+)',headers.get('Cache-Control',''),re.I)
    if match:return max(0,int(match.group(1))-int(headers.get('Age','0') or 0))
    try:return max(0,int(parsedate_to_datetime(headers['Expires']).timestamp()-time.time()))
    except (KeyError,ValueError,TypeError):return 7*86400


def response_bytes(content,meta):
    remaining=max(0,int(meta['expires_at']-time.time()))
    return Response(content,media_type='image/png',headers={'Cache-Control':f'public, max-age={remaining}',
        **{k:meta[k] for k in ['ETag','Last-Modified'] if k in meta}})


@router.get('/tiles/{z}/{x}/{y}.png')
def tile(z:int,x:int,y:int,request:Request):
    if not 7<=z<=16 or not 0<=x<2**z or not 0<=y<2**z:raise HTTPException(422,'Ô bản đồ ngoài phạm vi hỗ trợ.')
    n=2**z
    west,east=x/n*360-180,(x+1)/n*360-180
    north=math.degrees(math.atan(math.sinh(math.pi*(1-2*y/n))))
    south=math.degrees(math.atan(math.sinh(math.pi*(1-2*(y+1)/n))))
    if east<105.5 or west>108 or north<9.4 or south>12:raise HTTPException(422,'Bản đồ chỉ hỗ trợ vùng lân cận địa bàn nghiên cứu.')
    cache_root.mkdir(parents=True,exist_ok=True)
    key=f'{z}_{x}_{y}';image=cache_root/(key+'.png');record=cache_root/(key+'.json')
    with locks[hash(key)%len(locks)]:
        meta={}
        if record.exists() and image.exists():
            try:meta=json.loads(record.read_text(encoding='utf-8'))
            except (ValueError,OSError):meta={}
            if meta.get('expires_at',0)>time.time():return response_bytes(image.read_bytes(),meta)
        headers={'User-Agent':'HUIT-Group18-RealEstateResearchDemo/1.2 (local academic project)',
            'Referer':request.headers.get('referer') or 'http://localhost:3000/'}
        for name in ['ETag','Last-Modified']:
            if name in meta:headers['If-None-Match' if name=='ETag' else 'If-Modified-Since']=meta[name]
        try:
            remote=requests.get(f'https://tile.openstreetmap.org/{z}/{x}/{y}.png',headers=headers,timeout=(5,12),stream=True)
            with remote:
                if remote.status_code==304 and image.exists():
                    meta.update(expires_at=time.time()+ttl(remote.headers));record.write_text(json.dumps(meta),encoding='utf-8')
                    return response_bytes(image.read_bytes(),meta)
                if remote.status_code!=200:raise HTTPException(503,'Nguồn nền bản đồ tạm thời không tải được.')
                content=b''
                for chunk in remote.iter_content(65536):
                    content+=chunk
                    if len(content)>1024*1024:raise HTTPException(503,'Ô nền bản đồ không hợp lệ.')
                if not content.startswith(PNG):raise HTTPException(503,'Nguồn không trả ảnh nền bản đồ hợp lệ.')
                meta={'expires_at':time.time()+ttl(remote.headers),**{k:remote.headers[k] for k in ['ETag','Last-Modified'] if k in remote.headers}}
                temporary=image.with_suffix('.tmp');temporary.write_bytes(content);os.replace(temporary,image)
                record.write_text(json.dumps(meta),encoding='utf-8')
                return response_bytes(content,meta)
        except requests.RequestException as error:raise HTTPException(503,'Không kết nối được nguồn nền bản đồ; vẫn dùng được lớp địa bàn nghiên cứu.') from error
