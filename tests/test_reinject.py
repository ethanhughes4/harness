import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "reinject.py"


def run(cwd):
    r = subprocess.run([sys.executable, str(SCRIPT)], input=json.dumps({"hook_event_name": "SessionStart",
                       "source": "compact", "cwd": str(cwd)}), text=True, capture_output=True)
    assert r.returncode == 0
    return json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"] if r.stdout else ""


def setup(tmp_path):
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "harness.json").write_text("{}")


def test_no_config_prints_nothing(tmp_path):
    (tmp_path / "progress.md").write_text("x\n")
    assert run(tmp_path) == ""


def test_content(tmp_path):
    setup(tmp_path)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "brief.md").write_text("## Problem\np\n## Must never\nLose data\n## Out of scope\nzzz\n")
    (tmp_path / "docs" / "owner.md").write_text("o")
    (tmp_path / "docs" / "decisions.md").write_text("d")
    feats = [{"id": "a", "title": "A", "depends_on": [], "passes": True},
             {"id": "b", "title": "B", "depends_on": ["a"], "passes": False},
             {"id": "c", "title": "C", "depends_on": ["b"], "passes": False}]
    (tmp_path / "feature_list.json").write_text(json.dumps(feats))
    (tmp_path / "progress.md").write_text("\n".join(f"line{i}" for i in range(30)) + "\n")
    t = run(tmp_path)
    assert "Lose data" in t and "zzz" not in t
    assert "b: B" in t and "c: C" not in t and "a: A" not in t
    assert "docs/owner.md" in t and "docs/decisions.md" in t
    assert "line29" in t and "line10" in t and "line9\n" not in t


def test_missing_files(tmp_path):
    setup(tmp_path)
    assert run(tmp_path) == ""
    (tmp_path / "progress.md").write_text("only\n")
    assert "only" in run(tmp_path)


def test_cap(tmp_path):
    setup(tmp_path)
    (tmp_path / "progress.md").write_text("é" * 500 + "\n" + "\n".join("x" * 200 for _ in range(30)), encoding="utf-8")
    assert len(run(tmp_path).encode()) <= 2048
