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
