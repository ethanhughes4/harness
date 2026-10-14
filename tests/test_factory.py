import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEWERS = json.loads((ROOT / "factory.json").read_text(encoding="utf-8"))["reviewers"]


def test_has_code_reviewer():
    assert any(r["name"] == "code" and r["when"] == "always" for r in REVIEWERS)


def test_entries_valid():
    names = [r["name"] for r in REVIEWERS]
    assert len(names) == len(set(names))
    for r in REVIEWERS:
        assert r["when"] in ("always", "ui", "high_risk"), r
        assert isinstance(r["browser"], bool), r
        agent = r["agent"].removeprefix("harness:")
        assert (ROOT / "agents" / f"{agent}.md").exists(), r
