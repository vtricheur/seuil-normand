// Usage : node tools/guide_cards.js  (depuis la racine du projet)
// Lit tools/guides.json [{slug, short, h1}] et crée src/kit/guides/<slug>.jpg (1080x1350) s'il n'existe pas.
const {chromium} = require('playwright'); const fs = require('fs'); const path = require('path');
const root = path.resolve(__dirname, '..');
const list = JSON.parse(fs.readFileSync(path.join(root, 'tools/guides.json'), 'utf8'));
const logo = '<svg viewBox="0 0 64 64" width="84" height="84"><rect width="64" height="64" rx="14" fill="#fbfbf9"/><path d="M20 50V27a12 12 0 0 1 24 0v23" fill="none" stroke="#2e5a4c" stroke-width="4.5" stroke-linecap="round"/><rect x="12" y="49" width="40" height="5" rx="2.5" fill="#d1a46c"/></svg>';
const esc = s => s.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport: {width: 1080, height: 1350}});
  for (const g of list) {
    const out = path.join(root, 'src/kit/guides', g.slug + '.jpg');
    if (fs.existsSync(out) && !process.argv.includes('--force')) continue;
    await p.setContent(`<html><body style="margin:0;width:1080px;height:1350px;background:#2e5a4c;color:#fbfbf9;font-family:'DejaVu Sans',sans-serif;display:flex;flex-direction:column;justify-content:space-between;padding:90px 84px;box-sizing:border-box">
<div style="display:flex;align-items:center;gap:24px">${logo}<span style="font:700 44px 'DejaVu Serif',serif">Seuil Normand</span></div>
<div><div style="letter-spacing:.18em;font-size:30px;color:#d1a46c;font-weight:700;margin-bottom:34px">GUIDE · ${esc(g.short.toUpperCase())}</div>
<div style="font:700 74px/1.12 'DejaVu Serif',serif">${esc(g.h1)}</div></div>
<div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:32px;opacity:.9">Guide 2026</span>
<span style="background:#d1a46c;color:#1f2b33;font-weight:700;font-size:34px;padding:22px 34px;border-radius:999px;white-space:nowrap">Lire sur seuilnormand.fr</span></div></body></html>`);
    await p.screenshot({path: out, type: 'jpeg', quality: 88}); console.log('créé', out);
  }
  await b.close();
})();
