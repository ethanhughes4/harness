import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "risk.py"


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=cwd, check=True,
                   capture_output=True)


def repo(tmp_path, files, risky=None, branch="main"):
    git(tmp_path, "init", "-b", branch)
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "harness.json").write_text(json.dumps({"risky": risky} if risky else {}))
    (tmp_path / "a.txt").write_text("a")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-m", "base")
    git(tmp_path, "checkout", "-b", "factory/F1")
    for f in files:
        (tmp_path / f).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / f).write_text("x")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-m", "job")
    git(tmp_path, "checkout", branch)  # the project root stays on its own branch; jobs live in worktrees
    r = subprocess.run([sys.executable, str(SCRIPT), "F1"], cwd=tmp_path, text=True, capture_output=True)
    return r, json.loads(r.stdout)


def test_low(tmp_path):
    r, out = repo(tmp_path, ["src/app.py", "docs/a.md"])
    assert r.returncode == 0 and out == {"risk": "low", "files": []}


def test_high_defaults(tmp_path):
    _, out = repo(tmp_path, ["src/app.py", "src/auth/login.py", "web/package.json", ".github/workflows/ci.yml"])
    assert out["risk"] == "high"
    assert out["files"] == [".github/workflows/ci.yml", "src/auth/login.py", "web/package.json"]


def test_custom_globs(tmp_path):
    _, out = repo(tmp_path, ["src/auth/login.py", "billing/x.py"], risky=["billing/*"])
    assert out == {"risk": "high", "files": ["billing/x.py"]}


def test_base_is_checked_out_branch(tmp_path):
    # smoke 2026-10-14: a project whose branch isn't main/master made risk.py fail
    r, out = repo(tmp_path, ["src/auth/login.py"], branch="trunk")
    assert r.returncode == 0 and out["files"] == ["src/auth/login.py"]
