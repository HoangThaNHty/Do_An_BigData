import {billions} from '@/lib/types';
export default function PriceScale({estimated,range,asking}:{estimated:number;range:[number,number];asking:number|null}){
 const low=Math.max(0,Math.min(range[0]*.7,asking===null?range[0]*.7:asking*.8));
 const high=Math.max(range[1]*1.15,asking===null?0:asking*1.1);
 const position=(n:number)=>(n-low)/(high-low)*100;
 return <div className="price-scale" aria-label="Vị trí giá ước tính, dải tham khảo và giá bạn nhập"><div className="price-scale-track"><span className="price-scale-band" style={{left:position(range[0])+'%',width:position(range[1])-position(range[0])+'%'}}/><i className="price-scale-model" style={{left:position(estimated)+'%'}}/>{asking!==null&&<i className="price-scale-asking" style={{left:position(asking)+'%'}}/>}</div><div className="price-scale-limits"><span>{billions(low)} tỷ</span><span>{billions(high)} tỷ</span></div><div className="price-scale-keys"><span><i className="key-model"/>Ước tính {billions(estimated)} tỷ</span>{asking!==null&&<span><i className="key-asking"/>Bạn nhập {billions(asking)} tỷ</span>}<span><i className="key-band"/>Dải {billions(range[0])}–{billions(range[1])} tỷ</span></div><p>Thang giá chỉ đặt các mức cạnh nhau; dải không bảo đảm cho từng căn.</p></div>;
}
