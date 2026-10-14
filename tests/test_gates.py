import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "gates.py"
PY = sys.executable


def setup(tmp_path, **cfg):
    subprocess.run(["git", "init", "-b", "main"], cwd=tmp_path, check=True, capture_output=True)
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "harness.json").write_text(json.dumps(cfg))


def gates(tmp_path):
    r = subprocess.run([PY, str(SCRIPT), "F1", "1"], cwd=tmp_path, text=True, capture_output=True)
    return r, (tmp_path / ".harness" / "jobs" / "F1" / "gates-1.md").read_text()


def test_pass_with_empty_acceptance(tmp_path):
    setup(tmp_path, test=[[PY, "-c", "pass"]], gates=[[PY, "-c", "pass"]])
    r, text = gates(tmp_path)
    assert r.returncode == 0 and text.startswith("GATES: PASS")


def test_failing_gate_and_cap(tmp_path):
    noisy = "print('\\n'.join(str(i) for i in range(500))); raise SystemExit(1)"
    setup(tmp_path, test=[[PY, "-c", "pass"]], gates=[[PY, "-c", noisy]])
    r, text = gates(tmp_path)
    assert r.returncode == 1 and text.startswith("GATES: FAIL")
    assert "499" in text and len(text.splitlines()) <= 100


def test_acceptance_tamper(tmp_path):
    setup(tmp_path)
    acc = tmp_path / "tests" / "acceptance" / "F1"
    acc.mkdir(parents=True)
    (acc / "test_a.py").write_text("1")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-m", "tests"], cwd=tmp_path,
                   check=True, capture_output=True)
    assert gates(tmp_path)[0].returncode == 0
    (acc / "test_a.py").write_text("2")
    r, text = gates(tmp_path)
    assert r.returncode == 1 and "test_a.py" in text
