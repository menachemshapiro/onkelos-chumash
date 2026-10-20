const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  for (const f of process.argv.slice(2)) {
    const p = await b.newPage({ viewport: { width: 390, height: 800 } });
    const cdp = await p.context().newCDPSession(p);
    await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });   // rough phone CPU
    const t0 = Date.now();
    await p.goto(f.startsWith('http') ? f : 'file://' + f, { waitUntil: 'load' }); await p.waitForSelector('#text .verse');
    const t1 = Date.now();
    const m = await p.evaluate(() => { const n = performance.getEntriesByType('navigation')[0]; return { dcl: Math.round(n.domContentLoadedEventEnd), load: Math.round(n.loadEventEnd), nodes: document.getElementsByTagName('*').length }; });
    console.log(f.split('/').pop(), 'wall', t1 - t0, 'ms', JSON.stringify(m));
    await p.close();
  }
  await b.close();
})();
