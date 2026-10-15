"""Load published local experiment artifacts and serve price estimates."""
import json
import math
from pathlib import Path
from pyspark.sql import types as T
from pyspark.ml import PipelineModel
from src.models.features import prepare, NUMERIC, FEATURE_INPUTS
from src.models.train import KINDS


class Estimator:
    def __init__(self, spark, directory):
        self.spark=spark; self.directory=Path(directory)
        self.results=json.loads((self.directory/'results.json').read_text(encoding='utf-8'))
        selection=json.loads((self.directory/'selection.json').read_text(encoding='utf-8'))
        if selection['selected']!=self.results['selected'] or selection['test_used_for_selection']:
            raise ValueError('Selection artifacts inconsistent')
        self.domain=json.loads((self.directory/'input_domain.json').read_text(encoding='utf-8'))
        self.baseline=json.loads((self.directory/'baseline.json').read_text(encoding='utf-8'))
        self.models={item:PipelineModel.load(str(self.directory/item)) for item in set(selection['selected'].values()) if item!='baseline'}

    def estimate(self, inputs):
        kind=inputs['kind']; area=float(inputs['area'])
        if kind not in KINDS or not math.isfinite(area) or not 0<area<=10000:
            raise ValueError('Invalid property type or area')
        district=str(inputs['district_code'])
        if district not in self.domain[kind]['districts']:
            raise ValueError('District has no training support for this property type')
        row={c:inputs.get(c) for c in FEATURE_INPUTS}
        row.update(property_type_name=KINDS[kind],area=area,district_code=district)
        schema=T.StructType([T.StructField(c,T.DoubleType() if c in NUMERIC+['area'] else T.StringType(),True) for c in FEATURE_INPUTS])
        for c in NUMERIC:
            if row[c] is not None:
                value=float(row[c])
                if not math.isfinite(value): raise ValueError('Nonfinite numeric input')
                row[c]=value
        for c in ['ward_code','project_name']:
            if row[c] is not None: row[c]=str(row[c])
        identifier=self.results['selected'][kind]
        if identifier=='baseline':
            groups=[g for g in self.baseline['groups'] if g['property_type_name']==KINDS[kind] and g['district_code']==district and g['n']>=20]
            fallback=next(r['median_price_vnd'] for r in self.baseline['fallback'] if r['property_type_name']==KINDS[kind])
            value=groups[0]['median_price_vnd'] if groups else fallback
        else:
            frame=prepare(self.spark.createDataFrame([row],schema))
            log_value=self.models[identifier].transform(frame).select('prediction').first()[0]
            value=math.exp(log_value)
        if not math.isfinite(value) or value<=0: raise ValueError('Model returned invalid price')
        radius=self.results['bands'][kind]['log_radius']
        qlow,qhigh=self.domain[kind]['area_quantiles']
        warnings=[]
        if not qlow<=area<=qhigh: warnings.append('Diện tích nằm ngoài khoảng 1%–99% của tập huấn luyện; ước tính có thể kém tin cậy.')
        if not inputs.get('project_name'): warnings.append('Chưa cung cấp dự án; mô hình sử dụng nhóm dự án thiếu thông tin.')
        return {'model_id':identifier,'estimated_asking_price_vnd':float(value),
                'reference_range_vnd':[value*math.exp(-radius),value*math.exp(radius)],
                'range_method':'validation log residual 90th percentile; no guaranteed coverage',
                'test_empirical_range_coverage':self.results['bands'][kind]['test_empirical_coverage'],
                'warnings':warnings,'target':'Giá rao bán, không phải giá giao dịch được xác minh.'}
