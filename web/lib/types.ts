export type Kind='house'|'apartment';
export type Page='overview'|'market'|'map'|'predict'|'models'|'method';
export interface Summary {count:number;median_price_vnd:number|null;median_area_m2:number|null;median_unit_price_vnd:number|null;}
export interface Overview extends Summary {area_histogram:{label:string;count:number}[];}
export interface District extends Summary {district_code:string;district_label:string;small_sample:boolean;}
export interface Trend extends Summary {month:string;}
export interface Envelope<T>{data:T;scope:string;period:string;data_version:string;}
export interface Filters {months:string[];districts:{code:string;label:string}[];wards:{district_code:string;ward_code:string;ward_name:string;count:number}[];projects:{district_code:string;project_name:string;count:number}[];}
export interface Metrics {count:number;mae_vnd:number;rmse_vnd:number;r2:number|null;mape:number;median_ape:number;}
export interface ModelRow {id:string;kind:Kind;validation:Metrics;test:Metrics;}
export interface ModelResults {models:ModelRow[];selected:Record<Kind,string>;bands:Record<Kind,{log_radius:number;test_empirical_coverage:number}>;elapsed_seconds:number;}
export interface Estimate {model_id:string;estimated_asking_price_vnd:number;reference_range_vnd:[number,number];warnings:string[];elapsed_ms:number;test_empirical_range_coverage:number;}
export const count=(n:number)=>new Intl.NumberFormat('vi-VN').format(n);
export const decimal=(n:number,d=1)=>new Intl.NumberFormat('vi-VN',{maximumFractionDigits:d}).format(n);
export const billions=(n:number|null)=>n===null?'—':decimal(n/1e9,2);
export const millions=(n:number|null)=>n===null?'—':decimal(n/1e6,1);
export const percent=(n:number)=>decimal(n*100,1)+'%';
export async function request<T>(path:string,options:RequestInit={}):Promise<T>{
  const response=await fetch('/api/v1/'+path,{...options,signal:options.signal??AbortSignal.timeout(30000)});
  if(!response.ok){const error=await response.json().catch(()=>({}));throw new Error(typeof error.detail==='string'?error.detail:'Không thể tải dữ liệu. Kiểm tra API và thử lại.');}
  return response.json();
}
