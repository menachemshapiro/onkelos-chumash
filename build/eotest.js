const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1200, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  const pids = process.argv.slice(2);
  for (const pid of pids) {
    await p.goto('about:blank'); await p.goto('http://localhost:8765/bereishit-onkelos.html#' + pid); await p.waitForSelector('#text .tw');
    await p.selectOption('#t-enmode', 'onk').catch(()=>{});
    await p.waitForTimeout(400);
    const r = await p.evaluate(() => {
      const n = document.querySelectorAll('.wbd').length;
      const onk = [...document.querySelectorAll('.wbd summary')].filter(s => /Onkelos/.test(s.textContent)).length;
      const raw = [...document.querySelectorAll('#text')].map(t => t.innerText).join('').match(/\[\{|\{[a-z]/g);
      return { n, onk, braces: raw ? raw.length : 0 };
    });
    console.log(pid, JSON.stringify(r));
  }
  console.log('errors', errs);
  await b.close();
})();
