const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const ctx = await b.newContext({ viewport: { width: 390, height: 820 }, permissions: ['clipboard-read','clipboard-write'] });
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(process.argv[2]); await p.waitForTimeout(800);
  await p.fill('#goto-in', 'Haazinu 32:13'); await p.press('#goto-in', 'Enter'); await p.waitForTimeout(500);
  await p.click('#v32-13 .vt-orig'); await p.waitForTimeout(200);
  console.log('orig visible', await p.isVisible('#v32-13 .orig'), await p.textContent('#v32-13 .vt-orig'));
  await p.evaluate(() => document.querySelector('#v32-13 .orig').scrollIntoView({block:'center'}));
  await p.screenshot({ path: 'orig.png' });
  await p.click('#v32-13 .vt-rep'); await p.click('.rep-parts [data-p="english"]'); await p.fill('#rep-note', 'test note');
  await p.screenshot({ path: 'rep.png' });
  await p.click('#rep-send'); await p.waitForTimeout(300);
  console.log('msg', await p.textContent('#rep-msg'), 'clip', await p.evaluate(() => navigator.clipboard.readText()));
  console.log('orig buttons', await p.locator('.vt-orig').count(), 'report buttons', await p.locator('.vt-rep').count());
  console.log(errs); await b.close();
})();
