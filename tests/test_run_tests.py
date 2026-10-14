import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "run_tests.py"
PY = sys.executable


def run(cwd, test=None, limit=30):
    if test is not None:
        (cwd / ".claude").mkdir(exist_ok=True)
        (cwd / ".claude" / "harness.json").write_text(json.dumps({"test": test, "test_limit_s": limit}))
    return subprocess.run([PY, str(SCRIPT)], input=json.dumps({"hook_event_name": "Stop", "cwd": str(cwd)}),
                          text=True, capture_output=True)


def test_no_config(tmp_path):
    r = run(tmp_path)
    assert r.returncode == 0 and r.stderr == ""


def test_pass(tmp_path):
    assert run(tmp_path, [[PY, "-c", "pass"]]).returncode == 0


def test_fail_blocks_with_tail(tmp_path):
    r = run(tmp_path, [[PY, "-c", "pass"], [PY, "-c", "print('boom'); raise SystemExit(1)"]])
    assert r.returncode == 2 and "boom" in r.stderr


def test_timeout(tmp_path):
    r = run(tmp_path, [[PY, "-c", "import time; time.sleep(30)"]], limit=1)
    assert r.returncode == 2 and "killed after 1s" in r.stderr


def test_slow_warns(tmp_path):
    r = run(tmp_path, [[PY, "-c", "import time; time.sleep(16.5)"]], limit=20)
    assert r.returncode == 0 and "warning" in r.stderr
