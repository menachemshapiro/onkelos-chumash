const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await b.newContext({ viewport: { width: 1200, height: 900 }, acceptDownloads: true });
  await ctx.route(/html-to-image@/, r => r.fulfill({ path: 'node_modules/html-to-image/dist/html-to-image.js', contentType: 'application/javascript' }));
  await ctx.route(/jspdf@/, r => r.fulfill({ path: 'node_modules/jspdf/dist/jspdf.umd.min.js', contentType: 'application/javascript' }));
  await ctx.route(/cdn\.jsdelivr\.net\/npm\/docx/, r => r.fulfill({ path: 'package/build/index.umd.js', contentType: 'application/javascript' }));
  await ctx.route(/fonts\.googleapis/, r => r.fulfill({ body: '', contentType: 'text/css' }));
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(process.argv[2]); await p.waitForSelector('#text .verse');
  await p.fill('#goto-in', 'Haazinu 32:1'); await p.press('#goto-in', 'Enter'); await p.waitForTimeout(500);
  await p.click('#t-export');
  console.log('default rcols', await p.$eval('#xp-rcols', s => s.value));
  for (const [fmt, rc] of [['pdf', '1'], ['pdf', '2'], ['docx', '2'], ['html', '4']]) {
    await p.check(`input[name=xp-fmt][value=${fmt}]`); await p.selectOption('#xp-rcols', rc);
    await p.check('input[name=xp-scope][value=aliyah]').catch(() => {});
    const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 180000 }), p.click('#xp-go')]);
    const out = `rc${rc}.${fmt}`; await dl.saveAs(out); console.log(fmt, rc, dl.suggestedFilename(), '->', out);
    await p.waitForTimeout(300);
  }
  console.log(errs); await b.close();
})();
