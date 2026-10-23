const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const errs=[];
const ctx=await b.newContext({viewport:{width:1000,height:850}});const p=await ctx.newPage();p.on('pageerror',e=>errs.push(e.message));
let pops=0; ctx.on('page',()=>pops++);
await p.goto('http://localhost:8765/bereishit-onkelos.html#bereishit/1:1');await p.waitForTimeout(2500);
await p.evaluate(async()=>{const ix=await jIndex();const m=ix['malka'];await showJas(m[0],m[1],m[2],m[3],null);});await p.waitForTimeout(1200);
console.log('tabs:',(await p.locator('#jas-tabs').innerText()).replace(/\n/g,' / '));
for (const t of ['M01575','M01556']){
  await p.click(`#jas-tabs button[data-r="${t}"]`); await p.waitForTimeout(800);
  console.log(t,'title',await p.locator('#jas-t').textContent(),'| headings',await p.locator('#jas-body .jent').allTextContents());
}
await p.click('#jas-tabs button[data-r="M01575"]'); await p.waitForTimeout(600);
await p.locator('#jas-body a.jx').first().click(); await p.waitForTimeout(800);
console.log('after link click: title',await p.locator('#jas-t').textContent(),'| new windows',pops,'| back button',await p.locator('.jback').count());
console.log(errs);await b.close();})();
