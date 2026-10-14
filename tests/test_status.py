import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "status.py"

LIST = """[
  {
    "id": "F1",
    "title": "a",
    "steps": ["x"],
    "passes": false
  },
  {
    "id": "F2",
    "status": "todo",
    "title": "b",
    "passes": false
  }
]
"""


def run(tmp_path, *args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=tmp_path, text=True, capture_output=True)


def read(tmp_path):
    return (tmp_path / "feature_list.json").read_bytes().decode()


def test_adds_and_replaces_status_in_place(tmp_path):
    (tmp_path / "feature_list.json").write_bytes(LIST.replace("\n", "\r\n").encode())
    assert run(tmp_path, "F1", "building").returncode == 0
    assert run(tmp_path, "F2", "review").returncode == 0
    want = LIST.replace("{\n    \"id\": \"F1\"", "{\n    \"status\": \"building\",\n    \"id\": \"F1\"") \
               .replace('"status": "todo"', '"status": "review"').replace("\n", "\r\n")
    assert read(tmp_path) == want


def test_done_sets_passes(tmp_path):
    (tmp_path / "feature_list.json").write_bytes(LIST.encode())
    assert run(tmp_path, "F2", "done").returncode == 0
    assert '"status": "done",\n    "title": "b",\n    "passes": true' in read(tmp_path)
    assert '"passes": false' in read(tmp_path)  # F1 untouched


def test_bad_args(tmp_path):
    (tmp_path / "feature_list.json").write_bytes(LIST.encode())
    assert run(tmp_path, "F9", "done").returncode == 1
    assert run(tmp_path, "F1", "bogus").returncode == 1
    assert read(tmp_path) == LIST
