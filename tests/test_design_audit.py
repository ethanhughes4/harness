"""Step 2: design_audit.py on fixture pages (browser tests skip without Python Playwright)."""
import json
import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "scripts", "design_audit.py")
FIX = os.path.join(HERE, "fixtures", "design")


def audit(name, *extra):
    url = "file:///" + os.path.join(FIX, name).replace("\\", "/")
    r = subprocess.run([sys.executable, SCRIPT, url, *extra], capture_output=True, text=True, timeout=120)
    return r.returncode, json.loads(r.stdout)


def test_slop_page_fails_with_tells():
    pytest.importorskip("playwright")
    code, out = audit("slop.html")
    assert code == 1 and out["result"] == "fail"
    assert len(out["tells"]) >= 4
    assert {"N1", "N3", "N4", "N9", "N11"} <= set(out["tells"])


def test_clean_page_passes():
    pytest.importorskip("playwright")
    code, out = audit("clean.html")
    assert code == 0 and out["result"] == "pass", out["fails"]
    assert out["tells"] == {}


def test_sheet_justifies_tells(tmp_path):
    pytest.importorskip("playwright")
    sheet = tmp_path / "ds.md"
    sheet.write_text("\n".join(f"- {n}: brand owns it" for n in ["N1", "N3", "N4", "N9", "N11", "N10", "N7", "N13", "N18", "N8", "N2"]))
    _, out = audit("slop.html", "--sheet", str(sheet))
    assert not any("unjustified" in f for f in out["fails"])


def page(tmp_path, css, body):
    f = tmp_path / "p.html"
    f.write_text(f"<!doctype html><style>body{{font-family:Georgia,serif;font-size:18px;line-height:1.5;color:#222;background:#fff}}{css}</style>{body}")
    return "file:///" + str(f).replace("\\", "/")


def run(url, *extra):
    r = subprocess.run([sys.executable, SCRIPT, url, *extra], capture_output=True, text=True, timeout=120)
    return json.loads(r.stdout)


def test_token_drift(tmp_path):
    pytest.importorskip("playwright")
    url = page(tmp_path, "h1{color:#ff0000;font-family:Verdana,sans-serif}", "<h1>Hi</h1><p>text</p>")
    (tmp_path / "design-system.md").write_text("x")
    (tmp_path / "tokens.md").write_text("--ink: #222;\n--font: Georgia, serif\n")
    out = run(url, "--sheet", str(tmp_path / "design-system.md"))
    drift = [f for f in out["fails"] if "token drift" in f]
    assert drift and "rgb(255,0,0)" in drift[0] and "Verdana" in drift[0] and "34,34,34" not in drift[0]
    (tmp_path / "tokens.md").write_text("--ink: #222;\n--red: rgb(255, 0, 0);\n--font: georgia, serif;\n--h: VERDANA\n")
    out = run(url, "--sheet", str(tmp_path / "design-system.md"))
    assert not any("token drift" in f for f in out["fails"])


def test_measure_warns(tmp_path):
    pytest.importorskip("playwright")
    long = "word " * 400
    out = run(page(tmp_path, "p{margin:0}", f"<p>{long}</p>"))
    assert any("line length" in w for w in out["warns"])
    out = run(page(tmp_path, "p{margin:0;max-width:34em}", f"<p>{long}</p>"))
    assert not any("line length" in w for w in out["warns"])


def fixture_url(name):
    return "file:///" + os.path.join(FIX, name).replace("\\", "/")


def test_premium_page_has_no_premium_warns():
    pytest.importorskip("playwright")
    _, out = audit("premium.html")
    assert out["premium"]["warns"] == [], out["premium"]["warns"]
    assert out["premium"]["shadowLayers"] == 3 and out["premium"]["easingCurves"] == 1


def test_competent_page_raises_premium_warns():
    pytest.importorskip("playwright")
    _, out = audit("competent.html")
    w = " ".join(out["premium"]["warns"])
    for key in ("tracking", "pure", "opaque", "single-layer", "easing curves", "durations", "text-wrap", "quotes", "nested radius", ":active"):
        assert key in w, (key, w)
    assert set(out["premium"]["warns"]) <= set(out["warns"])


def test_compare_flags_out_of_range(tmp_path):
    pytest.importorskip("playwright")
    rng = tmp_path / "r.json"
    rng.write_text(json.dumps({"headingWeight": [300, 500], "shadowLayers": [2, 3], "bodyTracking": [-0.02, -0.005]}))
    _, ok = audit("premium.html", "--compare", str(rng))
    assert ok["compare"]["headingWeight"]["in_range"] and ok["compare"]["shadowLayers"]["in_range"]
    assert not ok["compare"]["bodyTracking"]["in_range"] and any("bodyTracking" in w for w in ok["warns"])
    _, bad = audit("competent.html", "--compare", str(rng))
    assert not bad["compare"]["headingWeight"]["in_range"] and not bad["compare"]["shadowLayers"]["in_range"]


def test_reference_capture(tmp_path):
    pytest.importorskip("playwright")
    cap = os.path.join(HERE, "..", "scripts", "reference_capture.py")
    r = subprocess.run([sys.executable, cap, str(tmp_path), "ref", fixture_url("premium.html"), fixture_url("competent.html"),
                        "file:///nonexistent/x.html"], capture_output=True, text=True, timeout=200)
    assert r.returncode == 0, r.stderr
    for n in ("1", "2"):
        assert (tmp_path / "ref" / n / "390-1.png").exists() and (tmp_path / "ref" / n / "1440-1.png").exists()
    assert "error" in json.loads((tmp_path / "ref" / "3" / "metrics.json").read_text())
    rng = json.loads((tmp_path / "ranges.json").read_text())
    assert rng["headingWeight"] == [450, 700] and rng["shadowLayers"] == [1, 3]
    _, out = audit("premium.html", "--compare", str(tmp_path / "ranges.json"))
    assert all(c["in_range"] for c in out["compare"].values())
