const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const errs=[];
const p=await b.newPage({viewport:{width:1100,height:900}});p.on('pageerror',e=>errs.push(e.message));
for (const [ref,id,word] of [['bereishit/1:2','v1-2','תהומא'],['toldot/25:27','v25-27','נחשירכן'],['bo/12:19','v12-19','מחמעא']]){
await p.goto('about:blank');await p.goto('http://localhost:8765/bereishit-onkelos.html#'+ref);await p.waitForTimeout(2500);
const k=await p.evaluate(([id,word])=>{const ws=[...document.querySelectorAll('#'+id+' .tw')];return ws.findIndex(w=>w.textContent.normalize('NFD').replace(/[^א-ת]/g,'')===word);},[id,word]);
await p.locator('#'+id+' .tw').nth(k).click();await p.waitForTimeout(700);await p.click('.gl-jas');await p.waitForTimeout(1200);
console.log(ref,'| title',await p.locator('#jas-t').textContent(),'| note',await p.locator('#jas-note').textContent(),'| tabs',(await p.locator('#jas-tabs').innerText()).replace(/\n/g,' / ').slice(0,200));
console.log('   jx links',await p.locator('#jas-body a.jx').count(),'| onkelos links',await p.locator('#jas-body a.jonk').count(),'| body',(await p.locator('#jas-body').innerText()).slice(0,160).replace(/\n/g,' '));
}
await p.screenshot({path:'../jas7.png'});
console.log(errs);await b.close();})();
