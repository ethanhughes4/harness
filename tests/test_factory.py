import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WHEN = ("always", "ui", "high_risk", "milestone")
REVIEWERS = json.loads((ROOT / "factory.json").read_text(encoding="utf-8"))["reviewers"]


def test_has_code_reviewer():
    assert any(r["name"] == "code" and r["when"] == "always" for r in REVIEWERS)


def test_entries_valid():
    names = [r["name"] for r in REVIEWERS]
    assert len(names) == len(set(names))
    for r in REVIEWERS:
        assert r["when"] in WHEN, r
        assert isinstance(r["browser"], bool), r
        agent = r["agent"].removeprefix("harness:")
        assert (ROOT / "agents" / f"{agent}.md").exists(), r



def by_name(name):
    return next(r for r in REVIEWERS if r["name"] == name)


def test_when_and_batch_values_valid():
    for r in REVIEWERS:
        assert r["when"] in WHEN, r
        assert type(r.get("batch", False)) is bool, r  # optional; a browser reviewer cannot be batched
        assert not (r.get("batch") and r["browser"]), r
        assert set(r) <= {"name", "agent", "when", "browser", "batch"}, r


def test_review_policy():
    assert by_name("code")["batch"] is True  # one code review per batch of features
    assert by_name("security")["when"] == "high_risk"  # D65: security only on risky changes
    for name in ("user", "visual"):  # expensive browser AI reviews: milestones, not every feature
        assert by_name(name)["when"] == "milestone" and by_name(name)["browser"] is True
    assert not any(r["when"] == "ui" for r in REVIEWERS)


def test_docs_and_organiser_match_factory_json():
    decisions = (ROOT / "docs" / "prd" / "factory-decisions.md").read_text(encoding="utf-8")
    organiser = (ROOT / "agents" / "organiser.md").read_text(encoding="utf-8")
    for text in (decisions, organiser):
        assert "milestone" in text and "batch" in text
    assert "merge.py" in organiser and "needs-human" in organiser
    assert "merged\n     automatically" not in organiser and "merged automatically" not in organiser
    # D65 names the security reviewer high_risk, and so does the file
    d65 = decisions[decisions.index("D65:"):decisions.index("D66:")]
    assert "`security`\n(`harness:security`, opus, high_risk)" in d65


def test_setup_template_allows_the_new_scripts():
    setup = (ROOT / "skills" / "setup" / "SKILL.md").read_text(encoding="utf-8")
    start = setup.rindex("{", 0, setup.index('"permissions"'))
    block = setup[start:setup.index("```", start)]
    allow = json.loads(block)["permissions"]["allow"]  # a missing comma would fail here
    for script in ("init_features", "merge", "mark_pass", "status", "gates", "risk", "build"):
        assert any(f"scripts/{script}.py" in a for a in allow), script
