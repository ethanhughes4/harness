"""python design_audit.py <url> [--sheet docs/design/design-system.md] [--tokens FILE] [--json-out FILE]

Audits a running page at 360, 768 and 1440 px (computed styles, no AI) and prints JSON
{"result": "pass"|"review"|"fail", "fails", "warns", "tells", "metrics"}. Exit 0 pass/review, 1 fail, 3 no Playwright.
A tell whose N-number has a reason line "N3: <reason>" in the sheet is justified (D96).
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WIDTHS = (360, 768, 1440)
FOCUS_STYLE = """(el) => { const s = getComputedStyle(el); return [s.outlineStyle, s.outlineWidth, s.outlineColor, s.boxShadow].join('|'); }"""
INTERACTIVE = "a[href], button, input, select, textarea, [tabindex]"
ACTIVE = """([sel, fn]) => { const f = eval(fn), all = [...document.querySelectorAll(sel)], a = document.activeElement;
  return [all.indexOf(a), a && a !== document.body ? f(a) : null, a ? a.tagName.toLowerCase() + (a.id ? '#' + a.id : '') : '']; }"""


def focus_pass(page):
    """Tab through the page; return selectors whose computed outline/box-shadow does not change on focus."""
    base = page.evaluate("([sel, fn]) => { const f = eval(fn); return [...document.querySelectorAll(sel)].map(f); }",
                         [INTERACTIVE, FOCUS_STYLE])
    bad = []
    for _ in range(min(len(base), 40)):
        page.keyboard.press("Tab")
        i, style, name = page.evaluate(ACTIVE, [INTERACTIVE, FOCUS_STYLE])
        if i >= 0 and style == base[i]:
            bad.append(name)
    return sorted(set(bad))


def justified(sheet):
    if not sheet:
        return set()
    with open(sheet, encoding="utf-8") as f:
        return set(re.findall(r"^\W*(N\d+)\s*[:–-]\s*\S", f.read(), re.M))


def hex_rgb(v):
    v = v.strip().lower()
    m = re.fullmatch(r"#([0-9a-f]{3,8})", v)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        return ",".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4)) if len(h) in (6, 8) else None
    m = re.fullmatch(r"rgba?\(([^)]+)\)", v)
    if m:
        n = re.findall(r"[\d.]+", m.group(1))[:3]
        return ",".join(str(round(float(x))) for x in n) if len(n) == 3 else None


def token_values(path):
    """-> (set of rgb strings, set of lowercase first font names) from `--name: value;` lines."""
    cols, fonts = set(), set()
    with open(path, encoding="utf-8") as f:
        for v in re.findall(r"^\W*--[\w-]+\s*:\s*([^;]+?)\s*;?\s*$", f.read(), re.M):
            c = hex_rgb(v)
            if c:
                cols.add(c)
            else:
                fonts.add(v.split(",")[0].strip().strip("\"'").lower())
    return cols, fonts


def stray(m, tokens):
    cols, fonts = token_values(tokens)
    near = lambda c, t: all(abs(int(a) - t) <= 8 for a in c.split(","))
    bad = [f"rgb({c})" for c in m["usedColours"] if c not in cols and not near(c, 255) and not near(c, 0)]
    bad += [f for f in m["usedFonts"] if f.lower() not in fonts and not re.fullmatch(GENERIC, f, re.I)]
    return sorted(bad)


GENERIC = r"serif|sans-serif|monospace|cursive|fantasy|ui-.*|-apple-system|blinkmacsystemfont|system-ui"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--sheet")
    ap.add_argument("--tokens", help="tokens.md (default: tokens.md next to the sheet, if it exists)")
    ap.add_argument("--json-out")
    a = ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("design_audit: Python Playwright is missing (pip install playwright && playwright install chromium)")
        return 3
    with open(os.path.join(HERE, "design_audit.js"), encoding="utf-8") as f:
        js = f.read()
    tells, metrics, overflow = {}, None, []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w in WIDTHS:
            pg = b.new_page(viewport={"width": w, "height": 900})
            pg.goto(a.url)
            pg.wait_for_timeout(300)
            r = pg.evaluate(js)
            if r["metrics"]["overflowX"]:
                overflow.append(w)
            for k, v in r["tells"].items():
                t = tells.setdefault(k, {"why": v["why"], "elements": []})
                t["elements"] = sorted(set(t["elements"] + v["elements"]))[:5]
            if w == WIDTHS[-1]:
                metrics = r["metrics"]
                nofocus = focus_pass(pg)
            pg.close()
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
        pg = ctx.new_page()
        pg.goto(a.url)
        pg.wait_for_timeout(300)
        reduced = pg.evaluate(js)["metrics"]["motionElements"]
        b.close()

    m, fails, warns = metrics, [], []
    m["overflowAtWidths"], m["reducedMotionElements"], m["noFocusStyle"] = overflow, reduced, nofocus
    if overflow:
        fails.append(f"horizontal overflow at {overflow}")
    if len(m["fontFamilies"]) > 2:
        fails.append(f"{len(m['fontFamilies'])} font families: {m['fontFamilies']}")
    if len(m["fontSizes"]) > 10:
        fails.append(f"{len(m['fontSizes'])} font sizes")
    if nofocus:
        fails.append(f"no visible focus style on {nofocus}")
    if reduced:
        fails.append(f"{reduced} elements still animate under prefers-reduced-motion")
    tokens = a.tokens or (a.sheet and os.path.join(os.path.dirname(os.path.abspath(a.sheet)), "tokens.md"))
    if tokens and os.path.exists(tokens):
        bad = stray(m, tokens)
        if bad:
            fails.append(f"token drift: {len(bad)} values not in tokens.md: {bad[:10]}")
    ok = justified(a.sheet)
    unj = sorted(k for k in tells if k not in ok)
    if len(unj) >= 4:
        fails.append(f"{len(unj)} unjustified tells: {unj}")
    checks = [
        (len(m["fontSizes"]) > 8, f"{len(m['fontSizes'])} font sizes (max 8)"),
        (len(m["fontWeights"]) > 3, f"{len(m['fontWeights'])} font weights (max 3)"),
        (not 16 <= m["bodyFontSize"] <= 20, f"body size {m['bodyFontSize']}px (16-20)"),
        (not 1.3 <= m["bodyLineHeight"] <= 1.6, f"body line height {m['bodyLineHeight']:.2f} (1.3-1.6)"),
        (m["spacingMultiple4Share"] < 0.9, f"only {m['spacingMultiple4Share']:.0%} of spacing is a multiple of 4"),
        (m["spacingDistinct"] > 12, f"{m['spacingDistinct']} distinct spacing values (max 12)"),
        (len(m["radii"]) > 3, f"{len(m['radii'])} radii (max 3)"),
        (len(m["shadows"]) > 4, f"{len(m['shadows'])} shadows (max 4)"),
        (m["chromaticHues"] > 4, f"{m['chromaticHues']} chromatic hue groups"),
        (m["primaryButtons"] > 1, f"{m['primaryButtons']} filled primary buttons in first viewport"),
        (bool(m["numericWithoutTabular"]), f"numeric cells without tabular-nums: {m['numericWithoutTabular']}"),
        (bool(m["untrackedUppercase"]), f"uppercase text without tracking >= 0.05em: {m['untrackedUppercase']}"),
    ]
    checks.append((bool(m["lineChars"]) and any(not 45 <= n <= 90 for _, n in m["lineChars"]),
                   f"paragraph line length outside 45-90 characters at 1440 px: {[x for x in m['lineChars'] if not 45 <= x[1] <= 90][:5]}"))
    warns = [msg for bad, msg in checks if bad]
    result = "fail" if fails else "review" if len(unj) >= 2 else "pass"
    out = {"result": result, "fails": fails, "warns": warns,
           "tells": {k: {**v, "justified": k in ok} for k, v in tells.items()}, "metrics": m}
    text = json.dumps(out, indent=2)
    if a.json_out:
        with open(a.json_out, "w", encoding="utf-8") as f:
            f.write(text)
    print(text)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
