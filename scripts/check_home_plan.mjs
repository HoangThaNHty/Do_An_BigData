/** Independent numeric oracles and invariants for financial scenario calculations. */
import assert from 'node:assert/strict';
import {calculatePlan,mortgage,validatePlan,defaultPlan} from '../web/lib/home-plan.ts';
let checks=0;
const close=(a,b,tol=.1)=>{assert.ok(Math.abs(a-b)<=tol,`${a} != ${b}`);checks++;};
const cash={...defaultPlan,price:3.5e9,low:2.8e9,high:4.2e9,savings:600e6,reserve:100e6,income:40e6,expenses:20e6,debt:0,feePercent:0,savingRate:0,priceGrowth:0,incomeGrowth:0,expenseGrowth:0};
const simple=calculatePlan(cash);
assert.deepEqual(simple.scenarios.map(s=>s.cashMonth),[115,150,185]);checks++;
for(const s of simple.scenarios){const m=s.cashMonth;assert.ok(m!==null);assert.ok(s.points[m].funds>=s.points[m].target);if(m>0)assert.ok(s.points[m-1].funds<s.points[m-1].target);checks++;}
close(simple.usableSavings,500e6);close(simple.monthlySurplus,20e6);
const zero=mortgage(120e6,0,12,'annuity');close(zero.first,10e6);close(zero.total,120e6);close(zero.totalInterest,0);
const fixed=mortgage(1e9,12,12,'annuity');
// Fixed numeric benchmark: monthly P&I 88,848,788.6783416 VND.
close(fixed.first,88848788.6783416);close(fixed.total,fixed.first*12);
const equal=mortgage(120e6,12,12,'principal');close(equal.first,11.2e6);close(equal.last,10.1e6);close(equal.totalInterest,7.8e6);
for(const method of ['annuity','principal'])for(const rate of [0,0.001,8,50]){
 const p=mortgage(2.1e9,rate,240,method);
 close(p.schedule.reduce((sum,r)=>sum+r.principal,0),2.1e9,1);
 close(p.schedule.at(-1).balance,0);
 assert.ok(p.schedule.every(r=>r.balance>=0&&r.payment>=0));checks++;
 if(method==='annuity')close(p.first,p.last,1);
 assert.ok(mortgage(2.1e9,rate+2,240,method).first>=p.first);checks++;
}
const noCash=calculatePlan({...cash,savings:0,reserve:0,income:0,expenses:1e6});assert.ok(noCash.scenarios.every(s=>s.cashMonth===null&&s.downMonth===null&&s.loanMonth===null));checks++;
const already=calculatePlan({...cash,savings:5e9,reserve:100e6});assert.deepEqual(already.scenarios.map(s=>s.cashMonth),[0,0,0]);checks++;
assert.ok(calculatePlan({...cash,priceGrowth:10}).scenarios[1].cashMonth===null);checks++;
const compound=calculatePlan({...cash,income:0,expenses:0,savingRate:12});close(compound.scenarios[1].points[12].funds,500e6*1.12,1);
for(const bad of [{low:4e9},{reserve:1e9},{loanYears:0},{horizonYears:1.5},{income:NaN},{loanRate:-1}]){assert.ok(validatePlan({...cash,...bad}).length);assert.throws(()=>calculatePlan({...cash,...bad}));checks++;}
for(const s of simple.scenarios){if(s.loanMonth!==null){assert.ok(s.loanMonth>=s.downMonth);assert.ok(s.remaining>=-.01);checks++;}}
console.log(`PASS: ${checks} financial oracle/invariant checks. No model training or network calls.`);
