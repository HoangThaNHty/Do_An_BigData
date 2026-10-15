'use client';
import {useEffect,useState} from 'react';
import {ArrowUpRight,Check,LoaderCircle,Info} from 'lucide-react';
import {Button} from '@/components/ui/button';
import {ExplorePanel} from './explore-ui';
import PropertyComparison from './property-comparison';
import PriceScale from './price-scale';
import {useWorkspace,type EstimateDraft,type Reference} from './workspace-state';
import {request,type Kind,type Filters,type Estimate,billions,percent,count,decimal} from '@/lib/types';
export default function PredictForm(){
 const {estimateDraft,setEstimateDraft,scenario,setScenario,saved,setSaved,setNotice,estimateBusy:busy,setEstimateBusy:setBusy,estimateError:error,setEstimateError:setError,referenceError:refError,setReferenceError:setRefError}=useWorkspace();
 const {kind,district,area,ward,project,quoted,optional}=estimateDraft;
 const update=(changes:Partial<EstimateDraft>)=>setEstimateDraft(d=>({...d,...changes}));
 const setKind=(kind:Kind)=>update({kind,ward:'',project:'',optional:{bedroom_count:'2',bathroom_count:'2'}});
 const setDistrict=(district:string)=>update({district,ward:'',project:''});
 const setArea=(area:string)=>update({area});const setWard=(ward:string)=>update({ward});const setProject=(project:string)=>update({project});const setQuoted=(quoted:string)=>update({quoted});const setOptional=(optional:Record<string,string>)=>update({optional});
 const [filters,setFilters]=useState<Filters|null>(null);const [retry,setRetry]=useState(0);
 useEffect(()=>{const c=new AbortController();setFilters(null);
 request<Filters>('filters?kind='+kind+'&district_code='+district,{signal:c.signal}).then(setFilters).catch(e=>{if(!c.signal.aborted)setError(e.message);});return()=>c.abort();},[kind,district,retry]);
 const fields=[['bedroom_count','Phòng ngủ'],['bathroom_count','Phòng tắm / WC'],...(kind==='house'?[['floor_count','Số tầng'],['frontage_width','Chiều ngang (m)'],['house_depth','Chiều sâu (m)'],['road_width','Đường trước nhà (m)']]:[])];
 const invalidate=()=>{setScenario(null);setRefError('');setError('');};
 async function submit(e:React.FormEvent){e.preventDefault();if(busy)return;setBusy(true);setError('');setRefError('');setScenario(null);
 const payload:Record<string,string|number|null>={kind,area:Number(area),district_code:district,ward_code:ward||null,project_name:project||null};for(const [key] of fields)payload[key]=optional[key]?Number(optional[key]):null;
 const title=(kind==='house'?'Nhà riêng':'Căn hộ')+' · '+(filters?.districts.find(d=>d.code===district)?.label||district);
 const inputs=area+' m² · '+fields.map(([key,label])=>label+': '+(optional[key]||'chưa biết')).join(' · ')+(ward?' · '+filters?.wards.find(w=>w.ward_code===ward)?.ward_name:'')+(project?' · '+project:'');
 try{const [prediction,reference]=await Promise.allSettled([request<Estimate>('predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}),request<Reference>('market/reference?'+new URLSearchParams({kind,district_code:district,area}))]);
 if(prediction.status==='rejected')throw prediction.reason;
 setScenario({result:prediction.value,title,inputs,reference:reference.status==='fulfilled'?reference.value:null});setNotice('Đã tính giá rao bán tham khảo. Kết quả và dải giá nằm cạnh thông tin căn nhà.');if(reference.status==='rejected')setRefError('Chưa tải được nhóm dữ liệu tham khảo; giá mô hình vẫn được tính thành công.');
 }catch(e){setError((e as Error).message);}finally{setBusy(false);}}
 const result=scenario?.result;const asking=Number(quoted)*1e9;const difference=result&&quoted&&asking>0&&Number.isFinite(asking)?asking/result.estimated_asking_price_vnd-1:null;
 return <><div className="predict-layout"><form className="panel predict-panel" onSubmit={submit}>
 <div className="panel-heading"><div><h2>Thông tin căn nhà bạn muốn tham khảo</h2><p>Người mua đối chiếu giá đang rao; người bán tham khảo giá đăng. Cùng một mô hình giá rao, theo dữ liệu 06/2025–03/2026.</p></div><span className="step-badge">01</span></div>
 <fieldset disabled={busy} className="input-fieldset"><div className="segmented" aria-label="Loại nhà ước tính">{(['apartment','house'] as Kind[]).map(k=><button type="button" className={kind===k?'active':''} key={k} onClick={()=>{setKind(k);setOptional({bedroom_count:'2',bathroom_count:'2'});invalidate();}}>{k==='house'?'Nhà riêng':'Căn hộ'}</button>)}</div>
 <div className="form-grid"><label>{kind==='house'?'Diện tích đất':'Diện tích căn hộ'} (m²)<input aria-label="Diện tích ước tính" required type="number" min="0.1" max="10000" step="0.1" value={area} onChange={e=>{setArea(e.target.value);invalidate();}}/></label>
 <label>Khu vực lịch sử<select aria-label="Khu vực ước tính" value={district} onChange={e=>{setDistrict(e.target.value);invalidate();}}>{!filters&&<option value={district}>Đang tải khu vực…</option>}{filters?.districts.map(r=><option key={r.code} value={r.code}>{r.label}</option>)}</select></label>
 <label>Phường theo địa giới tham chiếu<select value={ward} onChange={e=>{setWard(e.target.value);invalidate();}}><option value="">Chưa xác định</option>{filters?.wards.filter((r,i,all)=>all.findIndex(x=>x.ward_code===r.ward_code)===i).map(r=><option key={r.ward_code} value={r.ward_code}>{r.ward_name}</option>)}</select></label>
 <label>Dự án (nếu có)<input list="project-options" maxLength={200} placeholder="Chọn hoặc nhập tên dự án" value={project} onChange={e=>{setProject(e.target.value);invalidate();}}/><datalist id="project-options">{filters?.projects.map(r=><option key={r.project_name} value={r.project_name}/>)}</datalist></label>
 {fields.map(([key,label])=><label key={key}>{label} (tùy chọn)<input type="number" min={key.includes('count')?1:0.1} max={key.includes('count')?key==='floor_count'?100:50:1000} step={key.includes('count')?'1':'0.1'} placeholder="Chưa biết" value={optional[key]||''} onChange={e=>{setOptional({...optional,[key]:e.target.value});invalidate();}}/></label>)}
 <label>Giá đang rao / bạn dự định đăng (tỷ VND)<input aria-label="Giá rao đang cân nhắc" type="number" min="0.001" max="1000000" step="0.001" placeholder="Tùy chọn, ví dụ 4.2" value={quoted} onChange={e=>setQuoted(e.target.value)}/></label></div></fieldset>
 <p className="form-note"><Info size={15}/> Căn hộ dùng diện tích theo tin nguồn; chưa đồng nhất thông thủy/tim tường. Giá đang cân nhắc chỉ để đối chiếu, không đưa vào đầu vào mô hình.</p>
 {error&&<div role="alert" className="error-box">{error}<Button type="button" variant="outline" onClick={()=>{setError('');setRetry(v=>v+1);}}>Tải lại danh mục</Button></div>}<Button type="submit" className="predict-submit" disabled={busy||!filters}>{busy?<LoaderCircle className="spin" size={18}/>:<ArrowUpRight size={18}/>} {busy?'Đang ước tính…':'Ước tính giá rao bán'}</Button>
 </form><div className="result-column"><PropertyComparison/><div className={'estimate-card '+(result?'has-result':'')}><span className="eyebrow">GIÁ THEO DỮ LIỆU 06/2025–03/2026</span><h2>{result?<>{billions(result.estimated_asking_price_vnd)} <span>tỷ VND</span></>:<>Một góc nhìn<br/>từ dữ liệu.</>}</h2>
 {result?<><div className="estimate-range"><span>Dải tham khảo</span><strong>{billions(result.reference_range_vnd[0])} – {billions(result.reference_range_vnd[1])} tỷ</strong></div><p>Dải chứa {percent(result.test_empirical_range_coverage)} giá nguồn trong tập test cùng loại nhà. Không bảo đảm cho từng tài sản.</p><PriceScale estimated={result.estimated_asking_price_vnd} range={result.reference_range_vnd} asking={difference===null?null:asking}/><div className="result-meta"><Check size={15}/> Mô hình đã huấn luyện · {result.elapsed_ms} ms</div></>:<p>Nhập thông tin để xem giá ước tính, đối chiếu giá rao và lưu căn này rồi ước tính căn tiếp theo để so sánh.</p>}</div>
 {result&&difference!==null&&<ExplorePanel title="Đối chiếu giá rao bạn nhập"><div className="price-comparison"><strong>{billions(asking)} tỷ VND</strong><p>{difference>=0?'Cao hơn':'Thấp hơn'} ước tính mô hình <b>{percent(Math.abs(difference))}</b> ({billions(Math.abs(asking-result.estimated_asking_price_vnd))} tỷ).</p><p>{asking<result.reference_range_vnd[0]?'Nằm dưới':asking>result.reference_range_vnd[1]?'Nằm trên':'Nằm trong'} dải tham khảo mô hình.</p></div><p className="caption">Không kết luận tài sản rẻ/đắt hoặc giá hợp lý hiện tại. Mô hình chưa biết đầy đủ pháp lý, chất lượng, vị trí chi tiết và tình trạng.</p></ExplorePanel>}
 {scenario&&scenario!==saved&&<Button variant="outline" className="save-property-button" onClick={()=>{setSaved(scenario);setNotice('Đã lưu căn để so sánh. Thẻ căn đã lưu hiện ngay cạnh kết quả. Đổi đầu vào rồi ước tính căn tiếp theo.');}}>{saved?'Thay căn đã lưu bằng căn này':'Lưu căn này để so sánh'}</Button>}
 {result?.warnings.map(w=><div className="notice" key={w}><Info size={17}/><p>{w}</p></div>)}<div className="panel small-panel"><h3>Đọc đúng phạm vi</h3><p>Khu vực TP.HCM trước hợp nhất; chưa bao phủ Bình Dương/Bà Rịa–Vũng Tàu cũ. Không tự chuyển phường mới sang phường lịch sử.</p><p>Nhà diện tích lớn, dự án mới hoặc ít mẫu có thể có sai số cao. Không dùng kết quả như chứng thư thẩm định.</p></div></div></div>
 {refError&&<div className="notice"><p>{refError}</p></div>}
 {scenario?.reference&&<ExplorePanel title="Nhóm dữ liệu tham khảo" note={scenario.reference.criteria}><div className="reference-summary"><strong>{count(scenario.reference.count)} tin</strong><span>Diện tích {decimal(scenario.reference.area_range_m2[0])}–{decimal(scenario.reference.area_range_m2[1])} m²</span><span>Giá trung vị: {billions(scenario.reference.median_price_vnd)} tỷ</span><span>50% giá giữa: {scenario.reference.price_quartiles_vnd?billions(scenario.reference.price_quartiles_vnd[0])+'–'+billions(scenario.reference.price_quartiles_vnd[2])+' tỷ':'Chưa có mẫu'}</span></div><p className="caption">{scenario.reference.small_sample?'Ít hơn 20 mẫu; kết quả cần đọc thận trọng. ':''}Tin lịch sử, không xác nhận còn bán. Đây là nhóm tham khảo theo ba tiêu chí, chưa phải các tài sản tương đương đã xác minh.</p></ExplorePanel>}

 </>;
}
