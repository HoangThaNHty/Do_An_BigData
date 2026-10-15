// Local UI verification fallback when the desktop Browser connection cannot initialize.
const {chromium}=require('../.runtime/qa/node_modules/playwright');
const fs=require('node:fs');const path=require('node:path');const assert=require('node:assert/strict');
const base=process.env.WEB_BASE_URL||'http://127.0.0.1:3000';
(async()=>{
 const output=path.resolve(__dirname,'../artifacts/verification/web');fs.mkdirSync(output,{recursive:true});
 const browser=await chromium.launch({channel:'msedge',headless:true});globalThis.qaBrowser=browser;
 const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1,reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.stack));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('response',r=>{if(r.status()>=400)errors.push(r.status()+' '+r.url());});
 await page.goto(base+'/');await page.locator('.stat-value').first().waitFor();
 await page.screenshot({path:path.join(output,'01-overview.png'),fullPage:true});
 await page.getByRole('combobox',{name:'Lọc khu vực'}).selectOption('769');
 await page.getByRole('combobox',{name:'Lọc tháng'}).selectOption('2026-01');
 await page.locator('.stat-value').first().waitFor();
 const expected=await page.request.get(base+'/api/v1/overview?kind=apartment&district_code=769&month=2026-01');
 const n=(await expected.json()).data.count;await page.waitForFunction(n=>document.querySelector('.stat-value')?.textContent===new Intl.NumberFormat('vi-VN').format(n),n);
 await page.getByRole('button',{name:'Đặt lại bộ lọc',exact:true}).click();await page.locator('.stat-value').first().waitFor();
 const download=page.waitForEvent('download');await page.getByRole('button',{name:'Xuất thống kê',exact:true}).click();await(await download).saveAs(path.join(output,'export.csv'));
 for(const [label,file] of [['Tìm khu vực','02-market.png'],['Bản đồ giá','03-map.png'],['Độ chính xác dự đoán','05-models.png'],['Dữ liệu & phương pháp','06-method.png']]){
  await page.getByRole('navigation').getByRole('button',{name:label,exact:true}).click();
  if(label==='Bản đồ giá'){await page.locator('.leaflet-interactive').first().waitFor();assert.equal(await page.locator('.leaflet-interactive').count(),22);await page.locator('.leaflet-interactive').first().click({force:true});await page.waitForFunction(()=>document.querySelector('select[aria-label="Chọn khu vực trên bản đồ"]')?.value!=='');}
  if(label==='Độ chính xác dự đoán'){await page.locator('.model-reference>summary').click();await page.locator('.selected-row').waitFor();assert((await page.locator('.selected-row').textContent()).includes('CĂN HỘ'));}
  await page.screenshot({path:path.join(output,file),fullPage:true});
 }
 await page.getByRole('navigation').getByRole('button',{name:'Ước tính giá rao bán',exact:true}).click();
 await page.locator('.predict-submit').waitFor({state:'visible'});
 await page.waitForFunction(()=>!document.querySelector('.predict-submit')?.disabled);
 await page.locator('.predict-submit').click();await page.locator('.has-result').waitFor({timeout:90000});
 assert((await page.locator('.estimate-range').textContent()).includes('tỷ'));
 await page.screenshot({path:path.join(output,'04-predict.png'),fullPage:true});
 await page.setViewportSize({width:390,height:844});
 await page.screenshot({path:path.join(output,'07-mobile-predict.png'),fullPage:true});
 await page.getByRole('button',{name:'Mở menu',exact:true}).click();await page.getByRole('navigation').getByRole('button',{name:'Tổng quan',exact:true}).click();await page.locator('.stat-value').first().waitFor();
 await page.screenshot({path:path.join(output,'08-mobile-overview.png'),fullPage:true});
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),'Mobile horizontal overflow');
 assert.deepEqual(errors,[]);
 fs.writeFileSync(path.join(output,'checks.json'),JSON.stringify({passed:true,errors,desktop:[1440,1000],mobile:[390,844],checks:['six pages','exact filtered count','CSV download','22 polygons and click filter','selected model','real prediction','mobile menu and no page overflow']},null,2));
 console.log('PASS: desktop/mobile pages, filters, CSV, map click and real prediction; no browser errors.');await browser.close();
})().catch(async e=>{console.error(e);await globalThis.qaBrowser?.close();process.exit(1);});
