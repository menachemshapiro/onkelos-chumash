const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const errs=[];
const p=await b.newPage({viewport:{width:700,height:900}});p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/bereishit-onkelos.html#bereishit/1:1');await p.waitForTimeout(2500);
for (const [r,shot] of [['A03092','../jas16a.png'],['P01197',null],['K01002','../jas16k.png'],['O01711',null],['B00329',null]]){
 await p.evaluate(async r=>{await showJas(r,'word',[],[],null);},r);await p.waitForTimeout(900);
 console.log(r,'| headings',await p.locator('#jas-body .jent').allTextContents(),'| binyan labels',(await p.locator('#jas-body .jg').allTextContents()).join(' '));
 if(r==='A03092'){const el=p.locator('#jas-body .jbrick').first(); await el.scrollIntoViewIfNeeded(); await p.locator('.jas-card').screenshot({path:shot});}
 if(r==='K01002') await p.locator('.jas-card').screenshot({path:shot});
}
console.log(errs);await b.close();})();
