import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_log.py"


def run(tmp_path, text):
    log = tmp_path / "build-log.jsonl"
    log.write_text(text, encoding="utf-8")
    return subprocess.run([sys.executable, str(SCRIPT), str(log)], capture_output=True, text=True)


def test_clean_log(tmp_path):
    r = run(tmp_path, '{"type":"result","permission_denials":[]}\n{"type":"assistant"}\n')
    assert r.returncode == 0 and r.stdout == ""


def test_denial(tmp_path):
    r = run(tmp_path, '{"type":"result","permission_denials":[{"tool_name":"Bash"}]}\n')
    assert r.returncode == 1 and "Bash" in r.stdout


def test_broken_line_skipped(tmp_path):
    r = run(tmp_path, 'not json\n{"type":"result","permission_denials":[]}\n{bad\n')
    assert r.returncode == 0
