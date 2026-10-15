'use client';
import {createContext,useContext,useState,type ReactNode,type Dispatch,type SetStateAction} from 'react';
import type {Kind,Estimate,District} from '@/lib/types';
import {defaultPlan,type PlanInput} from '@/lib/home-plan';

export type Criteria={price_min:number;price_max:number;area_min:number;area_max:number};
export type Region=District&{price_quartiles_vnd?:[number,number,number]|null};
export type Reference={count:number;median_price_vnd:number|null;price_quartiles_vnd:[number,number,number]|null;area_range_m2:[number,number];small_sample:boolean;criteria:string};
export type EstimateDraft={kind:Kind;district:string;area:string;ward:string;project:string;quoted:string;optional:Record<string,string>};
export type Scenario={result:Estimate;title:string;inputs:string;reference:Reference|null};
type State={
 planInput:PlanInput;setPlanInput:Dispatch<SetStateAction<PlanInput>>;
 planApplied:PlanInput|null;setPlanApplied:Dispatch<SetStateAction<PlanInput|null>>;
 planSource:string;setPlanSource:Dispatch<SetStateAction<string>>;
 exploreMetric:'median_unit_price_vnd'|'median_price_vnd'|'count';setExploreMetric:Dispatch<SetStateAction<'median_unit_price_vnd'|'median_price_vnd'|'count'>>;
 exploreView:'map'|'list';setExploreView:Dispatch<SetStateAction<'map'|'list'>>;
 criteria:Criteria;setCriteria:Dispatch<SetStateAction<Criteria>>;
 budgetActive:boolean;setBudgetActive:Dispatch<SetStateAction<boolean>>;
 searchDraft:{min:string;max:string;amin:string;amax:string};setSearchDraft:Dispatch<SetStateAction<{min:string;max:string;amin:string;amax:string}>>;
 selectedRegions:string[];setSelectedRegions:Dispatch<SetStateAction<string[]>>;
 comparisonOpen:boolean;setComparisonOpen:Dispatch<SetStateAction<boolean>>;
 estimateDraft:EstimateDraft;setEstimateDraft:Dispatch<SetStateAction<EstimateDraft>>;
 scenario:Scenario|null;setScenario:Dispatch<SetStateAction<Scenario|null>>;
 saved:Scenario|null;setSaved:Dispatch<SetStateAction<Scenario|null>>;
 estimateBusy:boolean;setEstimateBusy:Dispatch<SetStateAction<boolean>>;
 estimateError:string;setEstimateError:Dispatch<SetStateAction<string>>;
 referenceError:string;setReferenceError:Dispatch<SetStateAction<string>>;
 notice:string;setNotice:Dispatch<SetStateAction<string>>;
};
const Context=createContext<State|null>(null);
export function WorkspaceProvider({children}:{children:ReactNode}){
 const [planInput,setPlanInput]=useState<PlanInput>({...defaultPlan});const [planApplied,setPlanApplied]=useState<PlanInput|null>(null);
 const [planSource,setPlanSource]=useState('Ba mức giá giả định minh họa, không phải dải do mô hình đã tính.');
 const [exploreMetric,setExploreMetric]=useState<'median_unit_price_vnd'|'median_price_vnd'|'count'>('median_unit_price_vnd');
 const [exploreView,setExploreView]=useState<'map'|'list'>('map');
 const [criteria,setCriteria]=useState<Criteria>({price_min:0,price_max:1e15,area_min:0,area_max:10000});
 const [budgetActive,setBudgetActive]=useState(false);
 const [searchDraft,setSearchDraft]=useState({min:'',max:'',amin:'',amax:''});
 const [selectedRegions,setSelectedRegions]=useState<string[]>([]);const [comparisonOpen,setComparisonOpen]=useState(false);
 const [estimateDraft,setEstimateDraft]=useState<EstimateDraft>({kind:'apartment',district:'769',area:'70',ward:'',project:'',quoted:'',optional:{bedroom_count:'2',bathroom_count:'2'}});
 const [scenario,setScenario]=useState<Scenario|null>(null);const [saved,setSaved]=useState<Scenario|null>(null);const [notice,setNotice]=useState('');
 const [estimateBusy,setEstimateBusy]=useState(false);const [estimateError,setEstimateError]=useState('');const [referenceError,setReferenceError]=useState('');
 return <Context.Provider value={{planInput,setPlanInput,planApplied,setPlanApplied,planSource,setPlanSource,exploreMetric,setExploreMetric,exploreView,setExploreView,criteria,setCriteria,budgetActive,setBudgetActive,searchDraft,setSearchDraft,selectedRegions,setSelectedRegions,comparisonOpen,setComparisonOpen,estimateDraft,setEstimateDraft,scenario,setScenario,saved,setSaved,notice,setNotice,estimateBusy,setEstimateBusy,estimateError,setEstimateError,referenceError,setReferenceError}}>{children}</Context.Provider>;
}
export function useWorkspace(){const context=useContext(Context);if(!context)throw new Error('WorkspaceProvider is required');return context;}
export function useRegionSelection(){
 const {selectedRegions,setSelectedRegions,setNotice}=useWorkspace();
 const toggle=(code:string)=>{if(selectedRegions.includes(code)){setSelectedRegions(selectedRegions.filter(c=>c!==code));setNotice('Đã bỏ một khu vực khỏi so sánh.');}else if(selectedRegions.length<3){setSelectedRegions([...selectedRegions,code]);setNotice(`Đã chọn ${selectedRegions.length+1}/3 khu vực.${selectedRegions.length===0?' Chọn thêm một khu vực để đối chiếu.':''}`);}else setNotice('Đã chọn đủ 3 khu vực. Bỏ một khu vực trước khi thêm khu vực khác.');};
 return {selectedRegions,toggle};
}
