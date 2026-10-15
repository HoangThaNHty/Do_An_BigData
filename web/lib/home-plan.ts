/** Deterministic scenarios, not price forecasts or lending approval. All money is VND. */
export interface PlanInput {
  price: number; low: number; high: number; savings: number; reserve: number;
  income: number; expenses: number; debt: number; ownerCosts: number;
  downPercent: number; feePercent: number; loanYears: number; loanRate: number;
  stressPoints: number; savingRate: number; priceGrowth: number; incomeGrowth: number;
  expenseGrowth: number; horizonYears: number; repayment: 'annuity'|'principal';
}
export const defaultPlan: PlanInput = {
  price:3.5e9, low:2.8e9, high:4.2e9, savings:600e6, reserve:100e6,
  income:40e6, expenses:20e6, debt:0, ownerCosts:2e6,
  downPercent:30, feePercent:0, loanYears:20, loanRate:8, stressPoints:2,
  savingRate:0, priceGrowth:0, incomeGrowth:0, expenseGrowth:0,
  horizonYears:30, repayment:'annuity',
};
export interface Payment {month:number; payment:number; principal:number; interest:number; balance:number}
export function mortgage(principal:number, annualRate:number, months:number, method:'annuity'|'principal') {
  if(!Number.isFinite(principal)||principal<0||!Number.isFinite(annualRate)||annualRate<0||annualRate>100||!Number.isInteger(months)||months<1||months>600||!['annuity','principal'].includes(method)) throw new Error('Thông số khoản vay không hợp lệ.');
  const r=annualRate/1200;
  const fixed=principal===0?0:r===0?principal/months:principal*r/(-Math.expm1(-months*Math.log1p(r)));
  let balance=principal, total=0, totalInterest=0;
  const schedule:Payment[]=[];
  for(let month=1;month<=months;month++) {
    const interest=balance*r;
    const paidPrincipal=month===months?balance:Math.min(balance,method==='principal'?principal/months:Math.max(0,fixed-interest));
    const payment=paidPrincipal+interest;
    balance=Math.max(0,balance-paidPrincipal);total+=payment;totalInterest+=interest;
    schedule.push({month,payment,principal:paidPrincipal,interest,balance});
  }
  return {first: schedule[0].payment, last:schedule.at(-1)!.payment,total,totalInterest,schedule};
}
export function validatePlan(p:PlanInput):string[] {
  const errors:string[]=[];
  if(Object.values(p).some(v=>typeof v==='number'&&!Number.isFinite(v))) return ['Vui lòng nhập đầy đủ các số hữu hạn.'];
  if(!(p.low>0&&p.low<=p.price&&p.price<=p.high&&p.high<=1e15)) errors.push('Giá phải dương và theo thứ tự thấp ≤ tham chiếu ≤ cao (tối đa 1 triệu tỷ VND).');
  for(const key of ['savings','reserve','income','expenses','debt','ownerCosts'] as const) if(p[key]<0||p[key]>1e15) errors.push('Các khoản tiền phải từ 0 đến 1 triệu tỷ VND.');
  if(p.reserve>p.savings) errors.push('Tiền dự phòng không được lớn hơn tiền hiện có.');
  if(!(p.downPercent>=1&&p.downPercent<=100)) errors.push('Tỷ lệ vốn tự có tối thiểu phải từ 1% đến 100%.');
  if(!(p.feePercent>=0&&p.feePercent<=50)) errors.push('Chi phí mua giả định phải từ 0% đến 50%.');
  if(!(p.loanRate>=0&&p.loanRate<=50&&p.stressPoints>=0&&p.stressPoints<=20)) errors.push('Lãi vay từ 0–50%; mức tăng kiểm tra từ 0–20 điểm %.');
  if(!(Number.isInteger(p.loanYears)&&p.loanYears>=1&&p.loanYears<=50&&Number.isInteger(p.horizonYears)&&p.horizonYears>=1&&p.horizonYears<=50)) errors.push('Kỳ hạn và thời hạn mô phỏng là số năm nguyên từ 1 đến 50.');
  for(const key of ['savingRate','priceGrowth','incomeGrowth','expenseGrowth'] as const) if(p[key]<-50||p[key]>50) errors.push('Các tốc độ tăng/lãi tích lũy giả định phải trong khoảng −50% đến 50%/năm.');
  if(!['annuity','principal'].includes(p.repayment)) errors.push('Phương thức trả nợ không hợp lệ.');
  return [...new Set(errors)];
}
export interface PlanPoint {month:number; funds:number; target:number; initialTarget:number}
export function calculatePlan(p:PlanInput) {
  const errors=validatePlan(p);if(errors.length) throw new Error(errors.join(' '));
  const months=p.horizonYears*12;
  const growth=(annual:number,m:number)=>Math.pow(1+annual/100,m/12);
  const scenarios=([['Thấp hơn',p.low],['Tham chiếu',p.price],['Cao hơn',p.high]] as const).map(([label,price])=>{
    let funds=p.savings-p.reserve;
    let cashMonth:number|null=null, downMonth:number|null=null, loanMonth:number|null=null;
    let candidate:null|{month:number;price:number;principal:number;available:number;funds:number}=null;
    const points:PlanPoint[]=[];
    for(let m=0;m<=months;m++) {
      const housePrice=price*growth(p.priceGrowth,m), target=housePrice*(1+p.feePercent/100);
      const initialTarget=housePrice*(p.downPercent+p.feePercent)/100;
      const available=p.income*growth(p.incomeGrowth,m)-(p.expenses+p.debt)*growth(p.expenseGrowth,m);
      points.push({month:m,funds,target,initialTarget});
      if(cashMonth===null&&funds>=target-0.01) cashMonth=m;
      if(funds>=initialTarget-0.01) {
        if(downMonth===null) downMonth=m;
        const principal=Math.max(0,target-funds);
        // First payment is the largest for equal-principal; no schedule needed in the search loop.
        const n=p.loanYears*12,r=p.loanRate/1200;
        const first=principal===0?0:r===0?principal/n:p.repayment==='principal'?principal/n+principal*r:principal*r/(-Math.expm1(-n*Math.log1p(r)));
        const point={month:m,price:housePrice,principal,available:available-p.ownerCosts*growth(p.expenseGrowth,m),funds};
        if(!candidate) candidate=point;
        if(loanMonth===null&&point.available>=first-0.01) {loanMonth=m;candidate=point;}
      }
      if(m<months) funds=Math.max(0,funds*growth(p.savingRate,1)+available);
    }
    const loan=candidate?mortgage(candidate.principal,p.loanRate,p.loanYears*12,p.repayment):null;
    const stressed=candidate?mortgage(candidate.principal,p.loanRate+p.stressPoints,p.loanYears*12,p.repayment):null;
    return {label,price,cashMonth,downMonth,loanMonth,points,candidate,loan,stressed,
      remaining:loan&&candidate?candidate.available-loan.first:null,
      stressRemaining:stressed&&candidate?candidate.available-stressed.first:null};
  });
  return {scenarios,monthlySurplus:p.income-p.expenses-p.debt,usableSavings:p.savings-p.reserve};
}
export const monthLabel=(m:number|null)=>m===null?'Chưa đạt trong thời hạn xét':m===0?'Đã đạt ở thời điểm đầu':`${Math.floor(m/12)} năm ${m%12} tháng`;
