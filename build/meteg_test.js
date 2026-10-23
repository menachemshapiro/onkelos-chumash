// meteg_test.js : the meteg must not be drawn inside a vowel (tzeirei + meteg looking like kamatz, Bereishis 16:8).
// Renders every vowel + meteg, as the page shows it (its METEG function), in the page's Hebrew fonts, and fails if the
// meteg falls between the vowel's left and right edges. Also checks the page shows the pasuk with the joiner.
const {chromium} = require('playwright'), fs = require('fs'), path = require('path');
const SP = path.join(__dirname, '..'), page = fs.readFileSync(path.join(SP, 'bereishit-onkelos.html'), 'utf8');
const METEG = eval(page.match(/const METEG = (s => .*?);\n/)[1]);
const F = path.join(__dirname, 'test-fonts');
(async () => {
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium'}); const p = await b.newPage();
  const css = [['N', 'noto-serif-hebrew'], ['F', 'frank-ruhl-libre'], ['D', 'david-libre']].map(([k, f]) => `@font-face{font-family:${k};src:url(data:font/woff2;base64,${fs.readFileSync(`${F}/${f}-hebrew-400-normal.woff2`).toString('base64')})}`).join('');
  await p.setContent(`<style>${css}</style><span style="font-family:N">ב</span><span style="font-family:F">ב</span><span style="font-family:D">ב</span>`);
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  const loaded = await p.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').length);
  if (loaded < 3) { console.log('test fonts did not load'); process.exit(2); }
  const V = {shva: 'ְ', 'hataf segol': 'ֱ', 'hataf patach': 'ֲ', 'hataf kamatz': 'ֳ', hiriq: 'ִ', tzeirei: 'ֵ', segol: 'ֶ', patach: 'ַ', kamatz: 'ָ', holam: 'ֹ', kubutz: 'ֻ'};
  const cases = Object.entries(V).map(([n, v]) => [n, 'ב' + v, METEG('ב' + v + 'ֽ')]);
  const bad = await p.evaluate(cases => {
    const c = document.createElement('canvas'); c.width = 300; c.height = 300; const x = c.getContext('2d', {willReadFrequently: true});
    const px = (f, s) => { x.clearRect(0, 0, 300, 300); x.font = `160px ${f}`; x.direction = 'rtl'; x.textAlign = 'center'; x.fillText(s, 150, 180);
      const d = x.getImageData(0, 0, 300, 300).data, o = new Uint8Array(90000); for (let i = 0; i < 90000; i++) o[i] = d[i * 4 + 3] > 100 ? 1 : 0; return o; };
    const box = m => { let a = [300, -1]; for (let i = 0; i < 90000; i++) if (m[i]) { const X = i % 300; a = [Math.min(a[0], X), Math.max(a[1], X)]; } return a; };
    const out = [];
    for (const f of ['N', 'F', 'D']) { const L = px(f, 'ב');
      for (const [n, withV, shown] of cases) { const A = px(f, withV), B = px(f, shown);
        const vb = box(A.map((q, i) => q && !L[i] ? 1 : 0)), mb = box(B.map((q, i) => q && !A[i] ? 1 : 0));
        if (vb[1] >= 0 && mb[1] >= 0 && mb[0] > vb[0] + 2 && mb[1] < vb[1] - 2) out.push(`${f}: ${n}`); } }
    return out; }, cases);
  const shown = METEG('אֵֽי־מִזֶּ֥ה');
  const ok16 = shown.includes('ֵ‍ֽ');
  console.log(bad.length ? 'METEG INSIDE VOWEL: ' + bad.join(', ') : 'meteg: no clash in Noto Serif Hebrew, Frank Ruhl Libre, David Libre', '| 16:8 shown with joiner:', ok16);
  await b.close(); process.exit(bad.length || !ok16 ? 1 : 0);
})();
