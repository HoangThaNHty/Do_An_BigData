"""Generate measured figures and inspect error tails without retuning test."""
import json
from pathlib import Path
import numpy as np
import pyarrow.dataset as ds
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
MODELS=ROOT/'artifacts/models/v1'
OUT=ROOT/'artifacts/figures'


def main():
    results=json.loads((MODELS/'results.json').read_text(encoding='utf-8'))
    OUT.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white'})
    fig,axes=plt.subplots(1,2,figsize=(12,4.4),constrained_layout=True)
    diagnostics={}
    for ax,kind,title in zip(axes,['house','apartment'],['Nhà riêng','Căn hộ']):
        rows=sorted([r for r in results['models'] if r['kind']==kind],key=lambda r:r['test']['mae_vnd'])
        values=[r['test']['mae_vnd']/1e9 for r in rows]
        ax.barh([r['id'] for r in rows],values,color=['#0f766e' if r['id']==results['selected'][kind] else '#94a3b8' for r in rows])
        ax.invert_yaxis(); ax.set_xlabel('MAE trên test (tỷ VND)'); ax.set_title(title)
        ax.set_xlim(0,max(values)*1.22)
        for i,value in enumerate(values):ax.text(value+max(values)*.02,i,f'{value:.2f}',va='center')
        table=ds.dataset(str(MODELS/('test_predictions_'+kind)),format='parquet').to_table()
        data={c:table[c].to_pylist() for c in table.column_names}
        error=np.asarray(data['absolute_error_vnd']); order=np.argsort(error)[::-1][:10]
        price=np.asarray(data['price']); pred=np.asarray(data['predicted_price_vnd'])
        diagnostics[kind]={'largest_errors':[{c:data[c][int(i)] for c in data} for i in order],
                           'test_price_quantiles_vnd':np.quantile(price,[0,.5,.9,.99,.999,1]).tolist(),
                           'squared_error_fraction_top10':float(np.sum(error[order]**2)/np.sum(error**2)),
                           'selection_unchanged':True}
        scatter=json.loads((MODELS/('scatter_'+kind+'.json')).read_text(encoding='utf-8'))
        fig2,ax2=plt.subplots(figsize=(5.8,5.3),constrained_layout=True)
        x=[r['price']/1e9 for r in scatter]; y=[r['predicted_price_vnd']/1e9 for r in scatter]
        ax2.scatter(x,y,s=15,alpha=.5,color='#0f766e')
        low=min(x+y); high=max(x+y); ax2.plot([low,high],[low,high],color='#f97316',lw=1.2)
        ax2.set_xscale('log'); ax2.set_yscale('log'); ax2.set_xlabel('Giá rao nguồn (tỷ VND, log)'); ax2.set_ylabel('Giá ước tính (tỷ VND, log)')
        ax2.set_title(title+' — mẫu test theo hash')
        fig2.savefig(OUT/('scatter_'+kind+'.png'),dpi=180);plt.close(fig2)
    fig.savefig(OUT/'model_test_mae.png',dpi=180);plt.close(fig)
    (MODELS/'error_tail_diagnostics.json').write_text(json.dumps(diagnostics,ensure_ascii=False,indent=2),encoding='utf-8')
    # Cohort funnel uses actual manifests, not expected counts.
    etl=json.loads((ROOT/'data/processed/etl_v4/manifest.json').read_text(encoding='utf-8'))
    core=json.loads((ROOT/'data/processed/core_v1/manifest.json').read_text(encoding='utf-8'))
    labels=['Nguồn nhà/căn hộ HCM','Ứng viên qua bộ lọc','Sau loại mẫu review','Tập nghiên cứu sau tin lặp']
    counts=[etl['source_rows'],core['protected_before_geo'],core['protected_after_review_exclusion'],core['cohort_rows']]
    fig,ax=plt.subplots(figsize=(9,4),constrained_layout=True)
    ax.barh(labels,counts,color=['#cbd5e1','#64748b','#0d9488','#0f766e']);ax.invert_yaxis();ax.set_xlabel('Số tin');ax.set_xlim(0,max(counts)*1.18)
    for i,n in enumerate(counts):ax.text(n+max(counts)*.015,i,f'{n:,}',va='center')
    fig.savefig(OUT/'cohort_funnel.png',dpi=180);plt.close(fig)
    print('Figures and error-tail diagnostics generated from completed test artifacts.')


if __name__=='__main__':main()
