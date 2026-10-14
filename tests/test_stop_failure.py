import ast
import json
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
SCRIPT = SCRIPTS / "stop_failure.py"
EVENT = {"hook_event_name": "StopFailure", "error": "rate_limit", "error_details": "429 Too Many Requests"}


def run(cwd):
    return subprocess.run([sys.executable, str(SCRIPT)], input=json.dumps({**EVENT, "cwd": str(cwd)}),
                          text=True, capture_output=True)


def test_no_config_writes_nothing(tmp_path):
    assert run(tmp_path).returncode == 0
    assert not (tmp_path / "progress.md").exists()


def test_with_config_appends(tmp_path):
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "harness.json").write_text("{}")
    (tmp_path / "progress.md").write_text("# Progress\n")
    assert run(tmp_path).returncode == 0
    assert run(tmp_path).returncode == 0
    text = (tmp_path / "progress.md").read_text()
    assert text.startswith("# Progress")
    assert text.count("error: rate_limit") == 2 and "429 Too Many Requests" in text


def test_stdlib_only():
    allowed = sys.stdlib_module_names | {"common"}
    for name in ("common.py", "stop_failure.py"):
        for n in ast.walk(ast.parse((SCRIPTS / name).read_text())):
            if isinstance(n, ast.Import):
                mods = [a.name for a in n.names]
            elif isinstance(n, ast.ImportFrom):
                mods = [n.module]
            else:
                continue
            for m in mods:
                assert m.split(".")[0] in allowed, m
