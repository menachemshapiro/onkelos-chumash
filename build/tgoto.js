const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 390, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(process.argv[2]); await p.waitForTimeout(800);
  for (const q of ['37:10', 'לב יג', 'Vayechi 49:11', 'haazinu 32:13', 'דברים לג:ז', 'וזאת הברכה לג ז', 'שמות טו יא', 'Bamidbar 23:19', 'Exodus 15:11', '99:99', 'נח ט ו', 'בא י י']) {
    await p.fill('#goto-in', q); await p.press('#goto-in', 'Enter'); await p.waitForTimeout(400);
    const r = await p.evaluate(() => [parSel.value, peSel.value, paSel.options[paSel.selectedIndex]?.text, document.getElementById('goto-in').classList.contains('bad')]);
    console.log(q, '=>', r.join(' '));
  }
  await p.fill('#goto-in', 'Vayechi 49:11'); await p.press('#goto-in', 'Enter'); await p.waitForTimeout(500);
  await p.screenshot({ path: 'goto.png' });
  console.log(errs); await b.close();
})();
