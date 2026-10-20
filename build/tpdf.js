const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await b.newContext({ viewport: { width: 390, height: 820 }, acceptDownloads: true });
  await ctx.route(/html-to-image@/, r => r.fulfill({ path: 'node_modules/html-to-image/dist/html-to-image.js', contentType: 'application/javascript' }));
  await ctx.route(/jspdf@/, r => r.fulfill({ path: 'node_modules/jspdf/dist/jspdf.umd.min.js', contentType: 'application/javascript' }));
  await ctx.route(/fonts\.googleapis/, r => r.fulfill({ body: '', contentType: 'text/css' }));
  await ctx.addInitScript(() => { window.claude = { use: async () => null }; });  // act like claude.ai
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(process.argv[2]); await p.waitForSelector('#text .verse');
  await p.fill('#goto-in', process.argv[3] || 'Haazinu 32:1'); await p.press('#goto-in', 'Enter'); await p.waitForTimeout(500);
  await p.click('#t-export'); await p.check('input[name=xp-fmt][value=pdf]');
  if (process.argv[4]) await p.selectOption('#xp-what', process.argv[4]).catch(() => {});
  const t0 = Date.now();
  const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 180000 }), p.click('#xp-go')]);
  await dl.saveAs('out.pdf');
  console.log('pdf', dl.suggestedFilename(), Date.now() - t0, 'ms', await p.textContent('#xp-msg'), errs);
  await b.close();
})();
