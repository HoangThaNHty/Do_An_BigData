'use client';
import {useEffect,useRef,useState} from 'react';
import {X,BookmarkCheck,ArrowRight} from 'lucide-react';
import {Button} from './ui/button';
import {useWorkspace} from './workspace-state';
import {billions,percent} from '@/lib/types';

export default function PropertyComparison(){
 const {saved,scenario,setSaved,setNotice}=useWorkspace();const [open,setOpen]=useState(false);
 const dialog=useRef<HTMLDialogElement>(null);const trigger=useRef<HTMLButtonElement>(null);
 const second=scenario&&scenario!==saved?scenario:null;
 useEffect(()=>{const node=dialog.current;if(!node)return;if(open&&!node.open)node.showModal();if(!open&&node.open){node.close();trigger.current?.focus();}},[open]);
 useEffect(()=>{if(!saved)setOpen(false);},[saved]);
 if(!saved)return null;
 const next=()=>{const input=document.querySelector<HTMLInputElement>('input[aria-label="Diện tích ước tính"]');input?.focus();input?.select();input?.scrollIntoView({block:'center',behavior:'auto'});setNotice('Căn đầu tiên đã lưu. Thay thông tin rồi chạy ước tính cho căn tiếp theo.');};
 return <><aside className="saved-property-inline" aria-label="Căn đã lưu"><div><BookmarkCheck size={19}/><strong>Căn đã lưu để so sánh</strong></div><h3>{saved.title}</h3><p>{saved.inputs}</p><strong className="saved-price">{billions(saved.result.estimated_asking_price_vnd)} tỷ VND</strong><div className="feature-actions"><Button variant="outline" onClick={next}>Ước tính căn tiếp theo<ArrowRight size={16}/></Button><Button ref={trigger} disabled={!second} onClick={()=>setOpen(true)}>Xem so sánh căn</Button><Button variant="ghost" onClick={()=>{setSaved(null);setNotice('Đã xóa căn đã lưu.');}}>Xóa căn đã lưu</Button></div><p>{second?'Đã có kết quả căn tiếp theo. Mở so sánh để đối chiếu hai căn.':'Chưa tính căn thứ hai. Đổi thông tin ở form rồi bấm Ước tính.'}</p></aside>
 <dialog ref={dialog} className="comparison-dialog property-dialog" aria-labelledby="property-comparison-title" onCancel={e=>{e.preventDefault();setOpen(false);}}><div className="dialog-heading"><div><span className="eyebrow">SO SÁNH HAI CĂN / PHƯƠNG ÁN ĐẦU VÀO</span><h2 id="property-comparison-title">So sánh giá rao bán tham khảo</h2><p>Theo dữ liệu 06/2025–03/2026; chưa phải giá giao dịch hoặc giá hiện tại.</p></div><Button autoFocus variant="outline" onClick={()=>setOpen(false)} aria-label="Đóng so sánh căn"><X size={20}/></Button></div><div className="scenario-grid">{[{label:'Căn đã lưu',data:saved},{label:'Căn vừa ước tính',data:second}].map(({label,data})=><article className="scenario-card" key={label}><span className="eyebrow">{label}</span>{data?<><h3>{data.title}</h3><p>{data.inputs}</p><strong>{billions(data.result.estimated_asking_price_vnd)} tỷ VND</strong><p>Dải {billions(data.result.reference_range_vnd[0])}–{billions(data.result.reference_range_vnd[1])} tỷ VND</p></>:<p>Chưa có kết quả.</p>}</article>)}</div>{second&&<p className="body-copy">Căn vừa ước tính {second.result.estimated_asking_price_vnd>=saved.result.estimated_asking_price_vnd?'cao hơn':'thấp hơn'} căn đã lưu {billions(Math.abs(second.result.estimated_asking_price_vnd-saved.result.estimated_asking_price_vnd))} tỷ VND ({percent(Math.abs(second.result.estimated_asking_price_vnd/saved.result.estimated_asking_price_vnd-1))}).</p>}<p className="caption">Hai kết quả phản ánh đầu vào bạn nhập. Chênh lệch không chứng minh tác động nhân quả của từng yếu tố, hay kết luận căn nào đáng mua hơn.</p><Button variant="outline" onClick={()=>setOpen(false)}>Quay lại thông tin căn nhà</Button></dialog></>;
}
