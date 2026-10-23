const {chromium,devices}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const errs=[];
for (const mode of ['desktop','phone']){
const ctx=await b.newContext(mode==='phone'?{...devices['Pixel 5']}:{viewport:{width:1000,height:850}});
const p=await ctx.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/bereishit-onkelos.html#bereishit/1:1');await p.waitForTimeout(2500);
await p.evaluate(async()=>{await showJas('O01195','word',[],[],null);});await p.waitForTimeout(1200);
const n=await p.locator('#jas-body abbr.jab').count();
console.log(mode,'abbr marked',n,(await p.locator('#jas-body abbr.jab').allTextContents()).slice(0,25).join(' | '));
// pick one inside a link and one outside
const inLink=p.locator('#jas-body a abbr.jab').first(), plain=p.locator('#jas-body abbr.jab:not(a abbr)').nth(3);
const url0=p.url();
if(mode==='desktop'){ await plain.hover(); await p.waitForTimeout(300); console.log(' hover:',await p.locator('.jas-tip').innerText(), await p.locator('.jas-tip').isVisible());
  await p.mouse.move(5,5); await p.waitForTimeout(200); console.log(' after leave visible:',await p.locator('.jas-tip').isVisible());
  await plain.hover(); await p.waitForTimeout(200); await p.locator('.jas-card').screenshot({path:'../jas13d.png'}); }
else { await inLink.scrollIntoViewIfNeeded(); await inLink.tap(); await p.waitForTimeout(400);
  console.log(' tap in link:',await p.locator('.jas-tip').innerText(),'| popup still open',await p.locator('#jas').isVisible(),'| url same',p.url()===url0);
  await p.screenshot({path:'../jas13p.png'});
  await p.locator('#jas-t').tap(); await p.waitForTimeout(200); console.log(' after tap elsewhere visible:',await p.locator('.jas-tip').isVisible());
  await p.locator('#jas-q').tap(); await p.waitForTimeout(200); await inLink.tap().catch(()=>{}); await p.waitForTimeout(300);
  console.log(' off mode: tip visible',await p.locator('.jas-tip').isVisible().catch(()=>false)); }
await ctx.close();}
console.log(errs);await b.close();})();
