"""python reference_capture.py <out_dir> <name> <url> [<url>...]

For each url: screenshots at 390 and 1440 px (full page, capped at 6000 px) into <out_dir>/<name>/, runs
design_audit.js at 1440 px and saves <out_dir>/<name>/<n>/metrics.json (or {"error": ...} if the url fails).
Then rewrites <out_dir>/ranges.json: {metric: [min, max]} across every metrics.json under <out_dir>
(the file `design_audit.py --compare` reads). Exit 0, 3 no Playwright.
"""
import json
import os
import sys

from design_audit import HERE, flat

CAP = 6000


def main(argv):
    if len(argv) < 4:
        print(__doc__)
        return 2
    out, name, urls = argv[1], argv[2], argv[3:]
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("reference_capture: Python Playwright is missing (pip install playwright && playwright install chromium)")
        return 3
    with open(os.path.join(HERE, "design_audit.js"), encoding="utf-8") as f:
        js = f.read()
    with sync_playwright() as p:
        b = p.chromium.launch()
        for i, url in enumerate(urls, 1):
            d = os.path.join(out, name, str(i))
            os.makedirs(d, exist_ok=True)
            res = {"url": url}
            try:
                for w in (390, 1440):
                    pg = b.new_page(viewport={"width": w, "height": 900})
                    pg.goto(url, timeout=30000)
                    pg.wait_for_timeout(500)
                    h = pg.evaluate("document.documentElement.scrollHeight")
                    pg.set_viewport_size({"width": w, "height": min(h, CAP)})
                    pg.screenshot(path=os.path.join(d, f"{w}.png"), clip={"x": 0, "y": 0, "width": w, "height": min(h, CAP)})
                    if w == 1440:
                        r = pg.evaluate(js)
                        res.update(metrics=flat(r["metrics"], r["premium"]), premium_warns=r["premium"]["warns"])
                    pg.close()
            except Exception as e:  # network or page error: record it, go on
                res["error"] = str(e).splitlines()[0]
                print(f"reference_capture: {url}: {res['error']}", file=sys.stderr)
            with open(os.path.join(d, "metrics.json"), "w", encoding="utf-8") as f:
                json.dump(res, f, indent=2)
        b.close()
    vals = {}
    for root, _, files in os.walk(out):
        if "metrics.json" in files:
            with open(os.path.join(root, "metrics.json"), encoding="utf-8") as f:
                for k, v in json.load(f).get("metrics", {}).items():
                    vals.setdefault(k, []).append(v)
    with open(os.path.join(out, "ranges.json"), "w", encoding="utf-8") as f:
        json.dump({k: [min(v), max(v)] for k, v in sorted(vals.items())}, f, indent=2)
    print(f"reference_capture: {len(urls)} url(s) -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
