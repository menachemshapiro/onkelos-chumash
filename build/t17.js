const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await b.newContext({ viewport: { width: 1300, height: 900 }, acceptDownloads: true });
  await ctx.route(/cdn\.jsdelivr\.net\/npm\/docx/, r => r.fulfill({ path: 'package/build/index.umd.js', contentType: 'application/javascript' }));
  await ctx.route(/fonts\.googleapis/, r => r.fulfill({ body: '', contentType: 'text/css' }));
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  const t0 = Date.now();
  await p.goto(process.argv[2].startsWith('http') ? process.argv[2] : 'file://' + process.argv[2]); await p.waitForTimeout(800);
  console.log('load ms', Date.now() - t0);
  const books = await p.$$eval('#sefer-sel option', o => o.map(x => x.value));
  console.log('sefarim', books.join(','));
  const only = process.argv[3] ? process.argv[3].split(',') : null;
  for (const bk of books) {
    await p.selectOption('#sefer-sel', bk); await p.waitForTimeout(350);
    const ids = await p.$$eval('#par-sel option', o => o.map(x => x.value));
    for (const id of ids) {
      if (only && !only.includes(id)) continue;
      await p.selectOption('#par-sel', id); await p.waitForTimeout(350);
      const r = await p.evaluate(() => ({ v: document.querySelectorAll('#text .verse').length, al: document.querySelectorAll('#al-sel option').length,
        alnames: [...document.querySelectorAll('#al-sel option')].map(o => o.text).join(','), pe: [...document.querySelectorAll('#pe-sel option')].map(o=>o.text).join(' '),
        rashi: document.querySelectorAll('#text .rashi p').length, sefer: document.querySelector('#sefer-sel').value }));
      console.log(r.sefer, id, r.v, r.al, r.alnames, '|', r.pe, '| rashi', r.rashi);
    }
  }
  if (process.argv[4]) {
    const [id, pe, pa, shot] = process.argv[4].split(':');
    await p.evaluate(id => { const P = PARSHIYOT.find(x => x.id === id); document.querySelector('#sefer-sel').value = P.book; document.querySelector('#sefer-sel').dispatchEvent(new Event('change')); }, id);
    await p.selectOption('#par-sel', id); await p.selectOption('#pe-sel', { label: `פרק ${pe}׳` }); await p.selectOption('#pa-sel', { label: `פסוק ${pa}׳` }); await p.waitForTimeout(250);
    await p.screenshot({ path: shot });
    await p.click('#t-export'); await p.check('input[name=xp-fmt][value=docx]');
    const [dl] = await Promise.all([p.waitForEvent('download'), p.click('#xp-go')]);
    console.log('docx', dl.suggestedFilename(), 'xp-par', await p.$eval('#xp-par', s => s.value));
  }
  console.log('errors', JSON.stringify(errs));
  await b.close();
})();
