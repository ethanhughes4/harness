import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "merge.py"
GUARD = ROOT / "scripts" / "guard.py"
ENV = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
       "GIT_COMMITTER_EMAIL": "t@t"}


def git(cwd, *args):
    r = subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True, env=ENV)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def feature(fid, ui=False):
    return {"id": fid, "stage": "s", "title": fid, "ui": ui, "depends_on": [], "steps": ["x"],
            "status": "review", "passes": False}


def project(tmp_path, branches, test=None):
    """A git repo on main with one branch factory/<id> per entry {id: file it adds}."""
    git(tmp_path, "init", "-q", "-b", "main")
    (tmp_path / ".claude").mkdir()
    cfg = {"test": [test or [sys.executable, "-c", "pass"]]}
    (tmp_path / ".claude" / "harness.json").write_text(json.dumps(cfg))
    (tmp_path / "feature_list.json").write_text(json.dumps([feature(f) for f in branches], indent=2))
    (tmp_path / ".gitignore").write_text("*.pyc\n")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "base")
    for fid, path in branches.items():
        git(tmp_path, "checkout", "-q", "-b", f"factory/{fid}", "main")
        (tmp_path / path).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / path).write_text(fid)
        git(tmp_path, "add", path)
        git(tmp_path, "commit", "-qm", f"build {fid}")
        git(tmp_path, "checkout", "-q", "main")


def job(tmp_path, fid, rnd, gates="PASS", **verdicts):
    folder = tmp_path / ".harness" / "jobs" / fid
    (folder / f"round-{rnd}").mkdir(parents=True, exist_ok=True)
    (folder / f"gates-{rnd}.md").write_text(f"GATES: {gates}\n")
    for name, verdict in verdicts.items():
        (folder / f"round-{rnd}" / f"review-{name}.md").write_text(f"VERDICT: {verdict}\n")


def merge(tmp_path, fid, rnd=1):
    return subprocess.run([sys.executable, str(SCRIPT), fid, str(rnd)], cwd=tmp_path, text=True,
                          capture_output=True, env=ENV)


def status(tmp_path, fid):
    return next(f["status"] for f in json.loads((tmp_path / "feature_list.json").read_text()) if f["id"] == fid)


def test_low_risk_with_passing_reviews_merges(tmp_path):
    project(tmp_path, {"F1": "src/a.py"})
    job(tmp_path, "F1", 1, code="PASS")
    r = merge(tmp_path, "F1")
    assert r.returncode == 0, r.stdout + r.stderr
    assert (tmp_path / "src" / "a.py").exists()
    assert status(tmp_path, "F1") == "done"
    assert "Merge factory/F1" in git(tmp_path, "log", "-1", "--format=%s")


def test_high_risk_is_never_merged_even_when_every_review_passes(tmp_path):
    project(tmp_path, {"F1": "src/auth.py"})
    job(tmp_path, "F1", 1, code="PASS", security="PASS")
    head = git(tmp_path, "rev-parse", "HEAD")
    r = merge(tmp_path, "F1")
    assert r.returncode == 3 and "high risk" in r.stdout
    assert git(tmp_path, "rev-parse", "HEAD") == head and not (tmp_path / "src" / "auth.py").exists()
    assert status(tmp_path, "F1") == "needs-human"
    assert git(tmp_path, "rev-parse", "--verify", "factory/F1")  # branch kept
    note = (tmp_path / ".harness" / "jobs" / "F1" / "decision.md").read_text()
    assert "NOT merged" in note and "src/auth.py" in note and "/harness:approve F1" in note


def test_high_risk_needs_the_security_review_before_it_is_parked(tmp_path):
    project(tmp_path, {"F1": "src/auth.py"})
    job(tmp_path, "F1", 1, code="PASS")  # code reviewer passed, security never ran
    r = merge(tmp_path, "F1")
    assert r.returncode == 2 and "review-security.md" in r.stdout
    assert status(tmp_path, "F1") == "review"  # not parked yet: the organiser must run the security reviewer
    job(tmp_path, "F1", 1, code="PASS", security="CHANGES")
    assert merge(tmp_path, "F1").returncode == 2


def test_not_ready_cases_change_nothing(tmp_path):
    project(tmp_path, {"F1": "src/a.py"})
    head = git(tmp_path, "rev-parse", "HEAD")
    assert merge(tmp_path, "F1").returncode == 2  # no job folder at all
    job(tmp_path, "F1", 1, gates="FAIL", code="PASS")
    assert merge(tmp_path, "F1").returncode == 2
    job(tmp_path, "F1", 1, code="CHANGES")
    assert merge(tmp_path, "F1").returncode == 2
    job(tmp_path, "F1", 1, code="PASS", stray="CHANGES")  # any review file in the round counts
    assert merge(tmp_path, "F1").returncode == 2
    assert git(tmp_path, "rev-parse", "HEAD") == head and status(tmp_path, "F1") == "review"


def test_batch_of_two_gives_independent_results_and_targeted_rework(tmp_path):
    """One batch review wrote one file per feature: F1 passes and merges, F2 needs changes and is the only
    one reworked and re-reviewed (round 2); F1 is not touched again."""
    project(tmp_path, {"F1": "src/a.py", "F2": "src/b.py"})
    job(tmp_path, "F1", 1, code="PASS")
    job(tmp_path, "F2", 1, code="CHANGES")
    assert merge(tmp_path, "F1").returncode == 0
    assert merge(tmp_path, "F2").returncode == 2  # round 1 stays CHANGES
    assert (status(tmp_path, "F1"), status(tmp_path, "F2")) == ("done", "review")
    assert not (tmp_path / "src" / "b.py").exists()
    # rework of F2 only: new gates and a new review in round 2
    job(tmp_path, "F2", 2, code="PASS")
    assert merge(tmp_path, "F2", 2).returncode == 0
    assert (tmp_path / "src" / "a.py").exists() and (tmp_path / "src" / "b.py").exists()
    assert not (tmp_path / ".harness" / "jobs" / "F1" / "round-2").exists()
    assert status(tmp_path, "F2") == "done"


def test_ui_feature_needs_its_ui_reviewers_only_if_factory_json_says_so(tmp_path):
    # factory.json ships user and visual as milestone reviewers, so a UI feature merges on code review alone
    project(tmp_path, {"F1": "src/a.py"})
    fl = json.loads((tmp_path / "feature_list.json").read_text())
    fl[0]["ui"] = True
    (tmp_path / "feature_list.json").write_text(json.dumps(fl))
    job(tmp_path, "F1", 1, code="PASS")
    assert merge(tmp_path, "F1").returncode == 0


def test_red_tests_undo_the_merge_and_keep_uncommitted_files(tmp_path):
    project(tmp_path, {"F1": "src/a.py"}, test=[sys.executable, "-c", "import sys; sys.exit(1)"])
    job(tmp_path, "F1", 1, code="PASS")
    head = git(tmp_path, "rev-parse", "HEAD")
    r = merge(tmp_path, "F1")
    assert r.returncode == 5 and "merge undone" in r.stdout
    assert git(tmp_path, "rev-parse", "HEAD") == head and not (tmp_path / "src" / "a.py").exists()
    assert (tmp_path / ".harness" / "jobs" / "F1" / "gates-1.md").exists()  # job files survive
    assert status(tmp_path, "F1") == "review"


def test_conflict_is_aborted(tmp_path):
    project(tmp_path, {"F1": "src/a.py"})
    (tmp_path / "src").mkdir(exist_ok=True)
    (tmp_path / "src" / "a.py").write_text("other")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "main also adds a.py")
    job(tmp_path, "F1", 1, code="PASS")
    r = merge(tmp_path, "F1")
    assert r.returncode == 4
    assert git(tmp_path, "status", "--porcelain", "--untracked-files=no") == ""  # merge aborted cleanly


def guard(cwd, agent, command):
    data = {"hook_event_name": "PreToolUse", "cwd": str(cwd), "tool_name": "Bash", "tool_input": {"command": command}}
    if agent:
        data.update(agent_type=agent, agent_id="a1")
    return subprocess.run([sys.executable, str(GUARD)], text=True, capture_output=True, input=json.dumps(data))


def test_guard_stops_the_organiser_merging_by_hand(tmp_path):
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "harness.json").write_text("{}")
    for cmd in ("git merge --no-ff factory/F1", "git add -A && git merge factory/F1", "git merge --abort"):
        r = guard(tmp_path, "harness:organiser", cmd)
        assert r.returncode == 2 and "merge.py" in r.stderr, cmd
    ok = f"python {SCRIPT.as_posix()} F1 1"
    assert guard(tmp_path, "harness:organiser", ok).returncode == 0
    assert guard(tmp_path, "harness:organiser", "git commit -m 'merge notes'").returncode == 0
    # the owner's /harness:approve runs in the interactive session and still merges
    assert guard(tmp_path, None, "git merge --no-ff factory/F1").returncode == 0
