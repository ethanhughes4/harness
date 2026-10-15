// Design audit: run in the page (page.evaluate). Self-contained, no dependencies.
// Returns metrics and tell detectors (N-numbers from reports/Design guideline against AI look.md).
() => {
  const cs = (e, p) => getComputedStyle(e);
  const vis = (e) => {
    const r = e.getBoundingClientRect(), s = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility === 'visible';
  };
  const sel = (e) => (e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') +
    (typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : ''));
  const rgb = (s) => { const m = /rgba?\(([^)]+)\)/.exec(s || ''); if (!m) return null;
    const v = m[1].split(/[ ,\/]+/).map(Number); return { r: v[0], g: v[1], b: v[2], a: v.length > 3 ? v[3] : 1 }; };
  const sat = (c) => (Math.max(c.r, c.g, c.b) - Math.min(c.r, c.g, c.b)) / 255;
  const hue = (c) => { const mx = Math.max(c.r, c.g, c.b), mn = Math.min(c.r, c.g, c.b), d = mx - mn; if (!d) return 0;
    const h = mx === c.r ? ((c.g - c.b) / d) % 6 : mx === c.g ? (c.b - c.r) / d + 2 : (c.r - c.g) / d + 4;
    return (h * 60 + 360) % 360; };
  const tells = {};
  const used = new Set(), usedFonts = new Set();
  const tell = (n, e, why) => { (tells[n] = tells[n] || { why, elements: [] }).elements.push(typeof e === 'string' ? e : sel(e)); };
  const uniq = (a) => [...new Set(a)];

  const els = [...document.body.querySelectorAll('*')].filter(vis);
  const fams = new Set(), sizes = new Set(), weights = new Set(), radii = new Set(), shadows = new Set();
  const colours = new Set(), spaces = [];
  const sized = []; // [el, radius, width] for N8
  let infinite = 0, motion = 0;
  const anim = {};
  const GENERIC = /^(serif|sans-serif|monospace|cursive|fantasy|ui-.*|-apple-system|blinkmacsystemfont)$/i;
  const MONO = /mono|courier|consolas|menlo|code/i;

  for (const e of els) {
    const s = getComputedStyle(e);
    if ([...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) {
      const f = s.fontFamily.split(',')[0].trim().replace(/["']/g, '');
      if (!GENERIC.test(f) && !MONO.test(f)) fams.add(f);
      sizes.add(s.fontSize); weights.add(s.fontWeight);
      usedFonts.add(s.fontFamily.split(',')[0].trim().replace(/["']/g, ''));
      const tc = rgb(s.color); if (tc && tc.a > 0.05) used.add([tc.r, tc.g, tc.b].map(Math.round).join());
      const c = rgb(s.color); if (c) colours.add([c.r, c.g, c.b].map((x) => Math.round(x / 24)).join());
    }
    const bg = rgb(s.backgroundColor);
    if (bg && bg.a > 0.1) colours.add([bg.r, bg.g, bg.b].map((x) => Math.round(x / 24)).join());
    if (bg && bg.a > 0.05) used.add([bg.r, bg.g, bg.b].map(Math.round).join());
    for (const side of ['Top', 'Right', 'Bottom', 'Left']) {
      const bc = rgb(s['border' + side + 'Color']);
      if (bc && bc.a > 0.05 && parseFloat(s['border' + side + 'Width']) > 0 && s['border' + side + 'Style'] !== 'none') used.add([bc.r, bc.g, bc.b].map(Math.round).join());
    }
    for (const p of ['marginTop', 'marginBottom', 'marginLeft', 'marginRight', 'paddingTop', 'paddingBottom', 'paddingLeft', 'paddingRight', 'rowGap', 'columnGap']) {
      const v = parseFloat(s[p]); if (v > 0) spaces.push(Math.round(v));
    }
    const rad = parseFloat(s.borderTopLeftRadius) || 0;
    if (rad > 0) { radii.add(Math.round(rad)); sized.push([e, Math.round(rad), e.getBoundingClientRect().width]); }
    const shs = s.boxShadow === 'none' ? [] : s.boxShadow.split(/,(?![^(]*\))/);
    for (const sh of shs) {
      shadows.add(sh.trim());
      const L = sh.match(/-?[\d.]+px/g) || [], blur = parseFloat(L[2]) || 0, col = rgb(sh);
      if (parseFloat(s.borderTopWidth) > 0 && s.borderTopStyle !== 'none' && blur >= 16) tell('N8', e, 'border plus blur >= 16px');
      if (col && col.a > 0 && sat(col) > 0.25 && blur >= 20) tell('N9', e, 'coloured glow blur >= 20px');
    }
    if ((s.backdropFilter || s.webkitBackdropFilter || 'none') !== 'none' && /blur/.test(s.backdropFilter || s.webkitBackdropFilter)) tell('N9', e, 'backdrop-filter blur');
    if (/gradient/.test(s.backgroundImage)) {
      for (const m of s.backgroundImage.match(/rgba?\([^)]+\)/g) || []) {
        const c = rgb(m); if (c && sat(c) > 0.15 && hue(c) >= 240 && hue(c) <= 290) { tell('N3', e, 'indigo-violet gradient (hue 240-290)'); break; }
      }
    }
    if ((s.webkitBackgroundClip || s.backgroundClip) === 'text' && /gradient/.test(s.backgroundImage)) tell('N4', e, 'gradient text');
    for (const side of ['Left', 'Top']) {
      const w = parseFloat(s['border' + side + 'Width']), other = parseFloat(s['border' + (side === 'Left' ? 'Right' : 'Bottom') + 'Width']);
      const c = rgb(s['border' + side + 'Color']);
      if (w >= 2 && w > other && s['border' + side + 'Style'] !== 'none' && c && sat(c) > 0.2 && rad > 0) { tell('N7', e, 'coloured ' + side.toLowerCase() + ' border on rounded box'); break; }
    }
    if (s.animationName !== 'none') {
      anim[s.animationName] = (anim[s.animationName] || 0) + (e.matches('section, main > *, article') ? 1 : 0);
      if (s.animationIterationCount === 'infinite') { infinite++; tell('N13', e, 'infinite animation'); }
      if (parseFloat(s.animationDuration) > 0.01) motion++;
    }
    if (parseFloat(s.transitionDuration) > 0.01 && s.transitionProperty !== 'none') motion++;
    if (/\p{Extended_Pictographic}/u.test(e.textContent) && e.matches('nav *, button, a[role=button], h1, h2, h3, h4, h5, h6') &&
        [...e.childNodes].some((n) => n.nodeType === 3 && /\p{Extended_Pictographic}/u.test(n.textContent))) tell('N11', e, 'emoji as icon');
  }
  if (infinite <= 2) delete tells.N13;
  const anames = Object.entries(anim).filter(([, n]) => n >= 3);
  if (anames.length) tell('N13', 'section', 'same animation on >= 3 sections: ' + anames.map((a) => a[0]).join());

  // N1 / N2 fonts
  const first = (e) => getComputedStyle(e).fontFamily.split(',')[0].trim().replace(/["']/g, '');
  const h1 = document.querySelector('h1');
  for (const e of [document.body, h1].filter(Boolean)) {
    if (/^(inter|geist|roboto|arial|open sans|lato|system-ui)$/i.test(first(e))) tell('N1', e, 'default font ' + first(e));
  }
  for (const f of fams) if (/space grotesk|instrument serif|fraunces/i.test(f)) tell('N2', 'font:' + f, 'next-default font');

  // N8: one radius on very different sizes; N10 eyebrows
  const rounded = sized.filter((x) => x[1] >= 4);
  if (rounded.length >= 4 && uniq(rounded.map((x) => x[1])).length === 1) {
    const w = rounded.map((x) => x[2]);
    if (Math.max(...w) / Math.min(...w) > 3) rounded.slice(0, 5).forEach((x) => tell('N8', x[0], 'identical radius on very different sizes'));
  }
  let eyebrows = [];
  for (const h of document.querySelectorAll('h2')) {
    const p = h.previousElementSibling; if (!p || !vis(p)) continue;
    const s = getComputedStyle(p);
    if (s.textTransform === 'uppercase' && parseFloat(s.letterSpacing) / parseFloat(s.fontSize) > 0.05 && p.textContent.trim().length < 40) eyebrows.push(p);
  }
  if (eyebrows.length >= 2) eyebrows.forEach((p) => tell('N10', p, 'tracked uppercase eyebrow before h2'));

  // N18 copy
  const text = document.body.innerText || '', words = text.split(/\s+/).filter(Boolean).length || 1;
  const bz = text.match(/\b(unlock|unleash|supercharge|empower\w*|world-class|game-changer|revolutioni[sz]e|the future of|seamless(ly)?)\b/gi);
  const dashes = (text.match(/—/g) || []).length;
  if (bz) tell('N18', 'text', 'buzzwords: ' + uniq(bz.map((x) => x.toLowerCase())).join(', '));
  if (dashes / words * 100 > 2) tell('N18', 'text', 'em-dashes per 100 words: ' + (dashes / words * 100).toFixed(1));

  // metrics
  const bs = getComputedStyle(document.body), lh = parseFloat(bs.lineHeight), bfs = parseFloat(bs.fontSize);
  const mult4 = spaces.filter((v) => v % 4 === 0).length;
  const btns = els.filter((e) => e.matches('button, input[type=submit], a[role=button], a.btn, a.button, .btn, .button') &&
    e.getBoundingClientRect().top < innerHeight && (() => { const c = rgb(getComputedStyle(e).backgroundColor); return c && c.a > 0.5 && sat(c) > 0.25; })());
  const NUM = /^[\s$€£+-]*\d[\d,.\s%]*$/;
  const nums = els.filter((e) => e.children.length === 0 && NUM.test(e.textContent) && e.matches('td, th, .price, .stat, .num, [class*=price], [class*=stat]'));
  const noTab = nums.filter((e) => !/tabular-nums/.test(getComputedStyle(e).fontVariantNumeric));
  const caps = els.filter((e) => { const s = getComputedStyle(e); return s.textTransform === 'uppercase' && e.children.length === 0 && e.textContent.trim() &&
    parseFloat(s.letterSpacing) / parseFloat(s.fontSize) < 0.05; }).map(sel);
  const chroma = new Set([...colours].map((k) => k.split(',').map((x) => x * 24)).filter((c) => sat({ r: c[0], g: c[1], b: c[2] }) > 0.25)
    .map((c) => Math.round(hue({ r: c[0], g: c[1], b: c[2] }) / 30)));
  // measure: average characters per rendered line of multi-line paragraphs
  const lineChars = [];
  for (const p of document.querySelectorAll('p')) {
    const t = p.textContent.trim(); if (!vis(p) || t.length < 20) continue;
    const r = document.createRange(); r.selectNodeContents(p);
    const lines = new Set([...r.getClientRects()].filter((q) => q.width > 0).map((q) => Math.round(q.top / 4)));
    if (lines.size >= 2) lineChars.push([sel(p), Math.round(t.length / lines.size)]);
  }
  for (const k of Object.keys(tells)) tells[k].elements = uniq(tells[k].elements).slice(0, 5);
  // Premium checks (premium report D1-D10): warn-level defaults, the brand sheet may override.
  const pw = [];
  const med = (a) => { a = a.slice().sort((x, y) => x - y); return a.length ? a[Math.floor((a.length - 1) / 2)] : null; };
  const em = (s) => (parseFloat(s.letterSpacing) || 0) / parseFloat(s.fontSize);
  const texts = els.filter((e) => [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()) && !e.closest('script, style'));
  const big = texts.filter((e) => parseFloat(getComputedStyle(e).fontSize) >= 24);
  const loose = big.filter((e) => em(getComputedStyle(e)) >= 0);
  if (loose.length) pw.push('text >= 24px with tracking >= 0 (want about -0.01 to -0.04em): ' + uniq(loose.map(sel)).slice(0, 5));
  const pureTxt = texts.filter((e) => { const c = rgb(getComputedStyle(e).color); return c && c.a > 0.5 && [0, 255].some((v) => c.r === v && c.g === v && c.b === v); });
  const pgBg = [document.documentElement, document.body].map((e) => rgb(getComputedStyle(e).backgroundColor)).filter((c) => c && c.a > 0.5).pop();
  const pureBg = pgBg && [0, 255].some((v) => pgBg.r === v && pgBg.g === v && pgBg.b === v);
  if (pureTxt.length) pw.push('pure #000/#fff text (use off-black / off-white): ' + uniq(pureTxt.map(sel)).slice(0, 5));
  if (pureBg) pw.push('pure #000/#fff page background');
  // borders vs rings, shadows
  let opaque = 0, alphaB = 0, layersMax = 0; const balpha = [], heavy = [];
  for (const e of els) {
    const s = getComputedStyle(e), rad = parseFloat(s.borderTopLeftRadius) || 0;
    if (parseFloat(s.borderTopWidth) > 0 && parseFloat(s.borderTopWidth) <= 1.5 && s.borderTopStyle === 'solid' && (rad > 0 || e.matches('input, select, textarea'))) {
      const c = rgb(s.borderTopColor); if (c && c.a >= 0.99) opaque++; else if (c && c.a > 0) { alphaB++; balpha.push(c.a); }
    }
    const shs = s.boxShadow === 'none' ? [] : s.boxShadow.split(/,(?![^(]*\))/);
    layersMax = Math.max(layersMax, shs.length);
    for (const sh of shs) {
      const L = (sh.match(/-?[\d.]+px/g) || []).map(parseFloat), c = rgb(sh);
      if (L[0] === 0 && L[1] === 0 && !L[2] && L[3] > 0 && c && c.a < 1) { alphaB++; balpha.push(c.a); }
    }
    if (shs.length === 1 && !/inset/.test(s.boxShadow)) {
      const L = (shs[0].match(/-?[\d.]+px/g) || []).map(parseFloat), c = rgb(shs[0]);
      if (c && (c.a > 0.2 || (L[2] || 0) >= 8)) heavy.push(e);
    }
  }
  if (opaque + alphaB && opaque / (opaque + alphaB) > 0.5) pw.push(`opaque 1px borders on ${opaque} of ${opaque + alphaB} cards/inputs (prefer low-alpha rings)`);
  if (heavy.length) pw.push('single-layer heavy shadow (alpha > .2 or blur >= 8px; use 2+ soft layers): ' + uniq(heavy.map(sel)).slice(0, 5));
  // easing and durations
  const curves = new Set(), durs = new Set(), ms = (v) => parseFloat(v) * (/ms$/.test(v.trim()) ? 1 : 1000);
  for (const e of els) {
    const s = getComputedStyle(e);
    for (const [d, f] of [[s.transitionDuration, s.transitionTimingFunction], [s.animationName !== 'none' ? s.animationDuration : '0s', s.animationTimingFunction]]) {
      const fl = f.split(/,(?![^(]*\))/);
      d.split(',').forEach((x, i) => { const v = Math.round(ms(x)); if (v > 0) { durs.add(v); curves.add(fl[i % fl.length].replace(/\s/g, '')); } });
    }
  }
  const dv = [...durs].sort((a, b) => a - b);
  if (curves.size > 1) pw.push(`${curves.size} distinct easing curves (want one main curve): ${[...curves].slice(0, 4)}`);
  if (durs.size > 3) pw.push(`${durs.size} distinct durations (max 3): ${dv}ms`);
  if (dv.some((v) => v < 100 || v > 500)) pw.push(`durations outside 100-500ms: ${dv.filter((v) => v < 100 || v > 500)}`);
  // text-wrap, quotes
  const unbal = [...document.querySelectorAll('h1, h2, h3')].filter((e) => vis(e) && !/balance/.test(getComputedStyle(e).textWrapStyle || getComputedStyle(e).textWrap || ''));
  if (unbal.length) pw.push('h1-h3 without text-wrap: balance: ' + uniq(unbal.map(sel)).slice(0, 5));
  const badQ = texts.filter((e) => !e.closest('code, pre, kbd, samp, textarea') && [...e.childNodes].some((n) => n.nodeType === 3 && /["']|\.\.\./.test(n.textContent)));
  if (badQ.length) pw.push('straight quotes or "..." in visible text (use curly quotes and the ellipsis character): ' + uniq(badQ.map(sel)).slice(0, 5));
  // nested radius: child radius <= parent radius - padding (+2px margin)
  const nest = [];
  for (const e of els) {
    const p = e.parentElement; if (!p || p === document.body) continue;
    const r = parseFloat(getComputedStyle(e).borderTopLeftRadius) || 0, ps = getComputedStyle(p), pr = parseFloat(ps.borderTopLeftRadius) || 0;
    if (r > 0 && pr > 0 && r > Math.max(pr - Math.min(parseFloat(ps.paddingTop), parseFloat(ps.paddingLeft)), 0) + 2) nest.push(e);
  }
  if (nest.length) pw.push('nested radius above parent radius minus padding: ' + uniq(nest.map(sel)).slice(0, 5));
  // buttons without an :active rule
  const actSel = [];
  const walk = (rules) => { for (const r of rules) { if (r.selectorText !== undefined) { if (/:active/.test(r.selectorText)) actSel.push(...r.selectorText.split(',').filter((x) => /:active/.test(x)).map((x) => x.replace(/:active/g, ''))); } if (r.cssRules) walk(r.cssRules); } };
  for (const ss of document.styleSheets) { try { walk(ss.cssRules); } catch (x) { /* cross-origin sheet */ } }
  const hasActive = (e) => actSel.some((x) => { try { return e.matches(x.trim() || '*'); } catch (z) { return false; } });
  const noActive = els.filter((e) => e.matches('button, input[type=submit], a[role=button], .btn, .button') && !hasActive(e));
  if (noActive.length) pw.push('buttons without an :active/pressed style: ' + uniq(noActive.map(sel)).slice(0, 5));
  const hd = document.querySelector('h1, h2, h3');
  const premium = {
    bodyTracking: em(bs), headingWeight: hd ? parseFloat(getComputedStyle(hd).fontWeight) : null,
    bigTextTracking: big.length ? Math.min(...big.map((e) => em(getComputedStyle(e)))) : null,
    borderAlpha: med(balpha), opaqueBorderShare: opaque + alphaB ? opaque / (opaque + alphaB) : null,
    shadowLayers: layersMax, easingCurves: curves.size, durationCount: durs.size,
    durationMin: dv.length ? dv[0] : null, durationMax: dv.length ? dv[dv.length - 1] : null,
    warns: pw,
  };
  return {
    tells, premium,
    metrics: {
      fontFamilies: [...fams], fontSizes: [...sizes], fontWeights: [...weights],
      colourClusters: colours.size, chromaticHues: chroma.size,
      spacingDistinct: uniq(spaces).length, spacingMultiple4Share: spaces.length ? mult4 / spaces.length : 1,
      radii: [...radii], shadows: [...shadows],
      bodyFontSize: bfs, bodyLineHeight: isNaN(lh) ? 1.2 : lh / bfs,
      overflowX: document.documentElement.scrollWidth > innerWidth + 1,
      primaryButtons: btns.length, numericCells: nums.length, numericWithoutTabular: noTab.map(sel).slice(0, 5),
      usedColours: [...used], usedFonts: [...usedFonts], lineChars,
      untrackedUppercase: caps.slice(0, 5), motionElements: motion,
    },
  };
}
