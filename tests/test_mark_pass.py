import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "mark_pass.py"
TEXT = ('[\n  {"id": "a", "title": "x",  "steps": ["s"], "passes": false},\r\n'
        '{"id":"b","passes":false,"steps":[]},\n  {"id": 3, "passes": false}\n]\n')


def run(cwd, fid):
    return subprocess.run([sys.executable, str(SCRIPT), fid], cwd=cwd, capture_output=True, text=True)


def test_flips_one_only(tmp_path):
    f = tmp_path / "feature_list.json"
    f.write_bytes(TEXT.encode())
    assert run(tmp_path, "b").returncode == 0
    assert f.read_bytes().decode() == TEXT.replace('"passes":false,"steps"', '"passes":true,"steps"')
    assert run(tmp_path, "3").returncode == 0
    assert f.read_bytes().decode().count("true") == 2


def test_unknown_id_fails(tmp_path):
    f = tmp_path / "feature_list.json"
    f.write_bytes(TEXT.encode())
    r = run(tmp_path, "zzz")
    assert r.returncode == 1 and "unknown" in r.stderr
    assert f.read_bytes().decode() == TEXT
