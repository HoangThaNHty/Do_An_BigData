import type {ReactNode} from 'react';
export function ExplorePanel({title,note,children}:{title:string;note?:string;children:ReactNode}){return <section className="panel feature-panel"><div className="panel-heading"><div><h2>{title}</h2>{note&&<p>{note}</p>}</div></div>{children}</section>;}
export function ResearchScope(){return <div className="research-scope"><strong>TP.HCM trước hợp nhất</strong><span>Tin đăng 06/2025–03/2026 · có cả trước và sau sáp nhập</span><span>Chưa bao phủ Bình Dương/Bà Rịa–Vũng Tàu cũ · không phải giá hiện tại</span></div>;}
