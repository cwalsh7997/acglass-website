/* ACG launch-edition QA gate runner.
   node qa/qa.js   (expects a static server on http://127.0.0.1:8099) */
const { chromium } = require('playwright');
const fs = require('fs');

const BASE = 'http://127.0.0.1:8099';
const PAGES = [
  ['index', '/index.html'],
  ['work', '/work.html'],
  ['ocean-prime', '/work/ocean-prime-fort-lauderdale.html'],
  ['federal', '/federal.html'],
  ['contact', '/contact.html'],
  ['storefront-guide', '/reference/storefront-glazing-systems.html'],
];
const VIEWPORTS = [['desktop', 1440, 900, 1500], ['mobile', 390, 844, 900]];
const OUT = 'qa/out';
fs.mkdirSync(OUT, { recursive: true });

const audit = () => {
  const res = {};
  const de = document.documentElement;
  res.overflow = { scrollWidth: de.scrollWidth, innerWidth: window.innerWidth, offenders: [] };
  if (de.scrollWidth > window.innerWidth + 1) {
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      if (r.width === 0) continue;
      if (r.right > window.innerWidth + 1 || r.left < -1) {
        const cs = getComputedStyle(el);
        if (cs.position === 'fixed' && cs.visibility === 'hidden') continue;
        res.overflow.offenders.push({
          sel: el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).join('.') : ''),
          left: Math.round(r.left), right: Math.round(r.right),
        });
      }
    }
    res.overflow.offenders = res.overflow.offenders.slice(0, 12);
  }

  res.images = { broken: [], missingAlt: [], upscaled: [], rendered: [] };
  for (const img of document.images) {
    const r = img.getBoundingClientRect();
    const name = (img.currentSrc || img.src).split('/').pop();
    if (img.complete && img.naturalWidth === 0) res.images.broken.push(name);
    if (!img.hasAttribute('alt')) res.images.missingAlt.push(name);
    // naturalWidth is density-corrected for srcset w descriptors and the rect
    // includes CSS transforms, so record the chosen file and the layout width
    // and verify against the real file dimensions on disk after the run.
    if (img.offsetWidth > 0) res.images.rendered.push({ file: (img.currentSrc || img.src).replace(location.origin, ''), layoutWidth: img.offsetWidth });
  }

  const ids = {}; res.duplicateIds = [];
  for (const el of document.querySelectorAll('[id]')) {
    ids[el.id] = (ids[el.id] || 0) + 1;
    if (ids[el.id] === 2) res.duplicateIds.push(el.id);
  }
  res.deadAnchors = [];
  for (const a of document.querySelectorAll('a[href^="#"]')) {
    const h = a.getAttribute('href');
    if (h === '#') { res.deadAnchors.push(h); continue; }
    if (!document.getElementById(decodeURIComponent(h.slice(1)))) res.deadAnchors.push(h);
  }

  res.tinyText = [];
  for (const el of document.querySelectorAll('body *')) {
    if (!el.firstChild) continue;
    let hasText = false;
    for (const n of el.childNodes) if (n.nodeType === 3 && n.textContent.trim()) hasText = true;
    if (!hasText) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    const fs2 = parseFloat(cs.fontSize);
    if (fs2 < 11) res.tinyText.push({ sel: el.tagName.toLowerCase() + '.' + (typeof el.className === 'string' ? el.className : ''), size: fs2, text: el.textContent.trim().slice(0, 30) });
  }

  const levels = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => +h.tagName[1]);
  res.headings = { seq: levels, skips: [] };
  for (let i = 1; i < levels.length; i++) if (levels[i] - levels[i - 1] > 1) res.headings.skips.push(`${levels[i - 1]}->${levels[i]}`);

  res.wrappedCaptions = [];
  // single-line-by-design caption lines only. .ux__i and .tl__c stack a name and
  // a meta line on purpose, so the meta line itself is what gets measured.
  for (const el of document.querySelectorAll('.tl__w, .wh__cap, .ap__cap, .pj__sub, .ux__i i')) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.2;
    const lines = Math.round(el.getBoundingClientRect().height / lh);
    const allowed = (el.classList.contains('ap__cap') || el.classList.contains('pj__sub') || el.tagName === 'I') ? (window.innerWidth <= 640 ? 2 : 1) : 1;
    if (lines > allowed) res.wrappedCaptions.push({ sel: el.className || el.tagName, lines, allowed, text: el.textContent.trim().slice(0, 40) });
  }

  // clipped text: a text box whose content is wider than the box itself while
  // overflow is not a deliberate scroller (catches nowrap captions running off
  // the frame inside a section that has overflow:hidden)
  res.clippedText = [];
  for (const el of document.querySelectorAll('body *')) {
    let hasText = false;
    for (const n of el.childNodes) if (n.nodeType === 3 && n.textContent.trim()) hasText = true;
    if (!hasText) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    if (cs.overflowX === 'auto' || cs.overflowX === 'scroll') continue;
    if (el.classList.contains('vh')) continue; // screen-reader-only 1px clip box
    if (el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 4) {
      res.clippedText.push({ sel: el.tagName.toLowerCase() + '.' + (typeof el.className === 'string' ? el.className : ''), scrollW: el.scrollWidth, clientW: el.clientWidth, text: el.textContent.trim().slice(0, 40) });
    }
  }

  res.hiddenRevealBlocks = [...document.querySelectorAll('.rv')]
    .filter(e => +getComputedStyle(e).opacity < 0.05).length;

  res.jsonld = [];
  for (const s of document.querySelectorAll('script[type="application/ld+json"]')) {
    try { JSON.parse(s.textContent); res.jsonld.push('ok'); } catch (e) { res.jsonld.push('PARSE FAIL: ' + e.message); }
  }
  return res;
};

(async () => {
  const browser = await chromium.launch();
  const report = {};
  for (const [vname, w, h, budgetKB] of VIEWPORTS) {
    for (const [pname, path] of PAGES) {
      const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
      const page = await ctx.newPage();
      let bytes = 0; const perRes = [];
      page.on('response', async r => {
        try {
          const h2 = await r.allHeaders();
          let len = parseInt(h2['content-length'] || '0', 10);
          if (!len) { const b = await r.body().catch(() => null); len = b ? b.length : 0; }
          bytes += len; if (len > 20000) perRes.push([r.url().split('/').pop(), Math.round(len / 1024)]);
        } catch (e) { }
      });
      await page.goto(BASE + path, { waitUntil: 'load' });
      await page.waitForTimeout(1400);
      const initialBytes = bytes;
      // scroll to trigger lazy images and reveals, then return to top
      await page.evaluate(async () => {
        const step = window.innerHeight * 0.8;
        for (let y = 0; y < document.body.scrollHeight; y += step) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 90)); }
        window.scrollTo(0, 0);
      });
      await page.waitForTimeout(1200);
      const a = await page.evaluate(audit);
      a.weightKB = Math.round(initialBytes / 1024);
      a.fullScrollKB = Math.round(bytes / 1024);
      a.budgetKB = budgetKB;
      a.heavy = perRes.sort((x, y) => y[1] - x[1]).slice(0, 8);
      report[`${pname}@${vname}`] = a;
      await page.screenshot({ path: `${OUT}/${pname}-${vname}.png`, fullPage: true });
      await page.screenshot({ path: `${OUT}/${pname}-${vname}-fold.png` });
      await ctx.close();
    }
  }

  // no-JS pass
  for (const [vname, w, h] of [['mobile', 390, 844], ['desktop', 1440, 900]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, javaScriptEnabled: false });
    for (const [pname, path] of PAGES) {
      const page = await ctx.newPage();
      await page.goto(BASE + path, { waitUntil: 'load' });
      await page.waitForTimeout(400);
      const r = await page.evaluate(() => {
        const navLinks = [...document.querySelectorAll('.hd__nav a')];
        const vis = navLinks.filter(a => {
          const cs = getComputedStyle(a); const rect = a.getBoundingClientRect();
          return cs.visibility !== 'hidden' && cs.display !== 'none' && +cs.opacity > 0.05 && rect.width > 0 && rect.height > 0;
        });
        const mb = document.querySelector('.hd__mb');
        const mbcs = mb ? getComputedStyle(mb) : null;
        const hidden = [...document.querySelectorAll('.rv')].filter(e => +getComputedStyle(e).opacity < 0.05).length;
        return {
          navTotal: navLinks.length, navVisible: vis.length,
          navCase: vis.length ? getComputedStyle(vis[0]).textTransform : null,
          navRendered: vis.map(a => a.textContent.trim()),
          hamburgerHidden: mbcs ? (mbcs.display === 'none') : null,
          hiddenRevealBlocks: hidden,
          scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth,
        };
      });
      report[`${pname}@${vname}-nojs`] = r;
      await page.screenshot({ path: `${OUT}/${pname}-${vname}-nojs.png` });
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();
  fs.writeFileSync('qa/report.json', JSON.stringify(report, null, 2));

  // console summary
  let fails = 0;
  for (const [k, v] of Object.entries(report)) {
    const p = [];
    if (k.endsWith('-nojs')) {
      if (v.navVisible !== v.navTotal) p.push(`nav ${v.navVisible}/${v.navTotal} reachable`);
      if (v.navCase !== 'uppercase') p.push(`nav case ${v.navCase}`);
      if (v.hamburgerHidden === false) p.push('hamburger visible');
      if (v.hiddenRevealBlocks) p.push(`${v.hiddenRevealBlocks} hidden .rv blocks`);
      if (v.scrollWidth > v.innerWidth + 1) p.push(`overflow ${v.scrollWidth}>${v.innerWidth}`);
    } else {
      if (v.overflow.scrollWidth > v.overflow.innerWidth + 1) p.push(`overflow ${v.overflow.scrollWidth}>${v.overflow.innerWidth} ${JSON.stringify(v.overflow.offenders)}`);
      if (v.images.broken.length) p.push(`broken ${v.images.broken}`);
      if (v.images.missingAlt.length) p.push(`noalt ${v.images.missingAlt}`);
      if (v.images.upscaled.length) p.push(`upscaled ${JSON.stringify(v.images.upscaled)}`);
      if (v.duplicateIds.length) p.push(`dupid ${v.duplicateIds}`);
      if (v.deadAnchors.length) p.push(`deadanchor ${v.deadAnchors}`);
      if (v.tinyText.length) p.push(`tiny ${JSON.stringify(v.tinyText.slice(0, 4))}`);
      if (v.headings.skips.length) p.push(`headingskip ${v.headings.skips}`);
      if (v.wrappedCaptions.length) p.push(`wrapped ${JSON.stringify(v.wrappedCaptions)}`);
      if (v.weightKB > v.budgetKB) p.push(`weight ${v.weightKB}KB > ${v.budgetKB}KB ${JSON.stringify(v.heavy)}`);
      if (v.jsonld.some(x => x !== 'ok')) p.push(`jsonld ${v.jsonld}`);
      if (v.hiddenRevealBlocks) p.push(`${v.hiddenRevealBlocks} reveal blocks still hidden`);
      if (v.clippedText && v.clippedText.length) p.push(`clipped ${JSON.stringify(v.clippedText.slice(0, 6))}`);
    }
    if (p.length) { fails++; console.log(`FAIL ${k}\n   ` + p.join('\n   ')); }
    else console.log(`PASS ${k}` + (v.weightKB ? ` (${v.weightKB}KB initial, ${v.fullScrollKB}KB fully scrolled)` : ''));
  }
  console.log(fails ? `\n${fails} contexts with findings` : '\nALL GATES PASS');
})();
