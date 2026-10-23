const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const errs=[];
const p=await b.newPage({viewport:{width:1100,height:900}});p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/bereishit-onkelos.html#bereishit/1:1');await p.waitForTimeout(2500);
for (const l of ['be','le','shwa']){
await p.evaluate(async l=>{const ix=await jIndex();const m=ix[l];await showJas(m[0],m[1],m[2],m[3],null);},l);await p.waitForTimeout(900);
console.log(l,'| title',await p.locator('#jas-t').textContent(),'| tabs',(await p.locator('#jas-tabs').innerText()).replace(/\n/g,' / '),'| hidden-first + headings',await p.locator('#jas-body .jent').allTextContents());}
await p.locator('.jas-card').screenshot({path:'../jas11.png'});
console.log(errs);await b.close();})();
