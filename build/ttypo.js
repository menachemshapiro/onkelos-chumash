const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const w of [390, 1200]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto(process.argv[2]); await p.waitForSelector('#text .rashi');
    const cc = () => p.$eval('#text .rashi-body', el => getComputedStyle(el).columnCount);
    const sel = await p.evaluate(() => [...document.querySelectorAll('#tp label')].find(l => l.textContent === 'Columns').htmlFor);
    console.log(w, 'default', await cc(), 'control', await p.$eval('#' + sel, s => s.value));
    await p.click('#t-panel'); await p.selectOption('#' + sel, '2'); await p.waitForTimeout(100);
    console.log(w, 'after 2', await cc());
    if (w === 390) { await p.click('#tp-close'); await p.evaluate(() => document.querySelector('#text .rashi').scrollIntoView()); await p.screenshot({ path: 'rc-phone.png' }); }
    await p.click('#t-export').catch(()=>{}); console.log('export default', await p.$eval('#xp-rcols', s => s.value), errs);
    await p.close();
  }
  await b.close();
})();
