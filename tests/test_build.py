import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "build.py"

# stub session: mark the first todo feature done (and print a line for the log)
DONE_ONE = """
import json
fs = json.load(open("feature_list.json"))
for f in fs:
    if f.get("status", "todo") == "todo":
        f["status"] = "done"; f["passes"] = True
        break
json.dump(fs, open("feature_list.json", "w"))
print('{"type": "result"}')
"""
NOTHING = "print('{\"type\": \"result\"}')"


def project(tmp_path, features, stub):
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "harness.json").write_text("{}")
    (tmp_path / "feature_list.json").write_text(json.dumps(features))
    (tmp_path / "stub.py").write_text(stub)


def build(tmp_path, env=None):
    return subprocess.run([sys.executable, str(SCRIPT), "--session-cmd", sys.executable, str(tmp_path / "stub.py")],
                          cwd=tmp_path, text=True, capture_output=True, env=env)


def feats(*specs):
    return [{"id": f"F{i}", "depends_on": d, "passes": False, "status": s} for i, (d, s) in enumerate(specs, 1)]


def test_stops_when_done(tmp_path):
    project(tmp_path, feats(([], "todo"), (["F1"], "todo")), DONE_ONE)
    r = build(tmp_path)
    assert r.returncode == 0
    assert r.stdout.splitlines()[-1] == "feature_list: 2/2 done, 0 needs-human"
    assert (tmp_path / "build-log.jsonl").read_text().count('"result"') == 2


def test_stops_after_two_idle_sessions(tmp_path):
    project(tmp_path, feats(([], "todo")), NOTHING)
    r = build(tmp_path)
    assert (tmp_path / "build-log.jsonl").read_text().count('"result"') == 2
    assert r.stdout.splitlines()[-1] == "feature_list: 0/1 done, 0 needs-human"


def test_nothing_ready(tmp_path):
    project(tmp_path, feats(([], "needs-human"), (["F1"], "todo")), NOTHING)
    r = build(tmp_path)
    assert r.stdout.splitlines()[-1] == "feature_list: 0/2 done, 1 needs-human"
    assert not (tmp_path / "build-log.jsonl").exists()


def test_plugin_dir_added_only_when_not_installed():
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
    from build import with_plugin_dir
    assert with_plugin_dir(["claude"], "  ❯ ponytail@ponytail\n", "C:/h") == ["claude", "--plugin-dir", "C:/h"]
    assert with_plugin_dir(["claude"], "  ❯ harness@local\n", "C:/h") == ["claude"]
    assert with_plugin_dir(["claude"], "", None) == ["claude"]


def test_session_cmd_needs_no_claude_cli(tmp_path):
    # PATH holds only an empty folder, so `claude` cannot be found: the override must not look for it
    project(tmp_path, feats(([], "todo")), DONE_ONE)
    empty = tmp_path / "empty"
    empty.mkdir()
    r = build(tmp_path, env={**os.environ, "PATH": str(empty)})
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines()[-1] == "feature_list: 1/1 done, 0 needs-human"


def test_failed_session_stops_the_build(tmp_path):
    project(tmp_path, feats(([], "todo"), (["F1"], "todo")),
            "import sys; print('boom: partial output'); sys.exit(3)")
    r = build(tmp_path)
    assert r.returncode == 1
    assert "session failed (3)" in r.stderr
    assert "feature_list: 0/2 done" in r.stderr
    log = (tmp_path / "build-log.jsonl").read_text()
    assert log.count("boom") == 1  # stopped after the first failure, not retried as an idle session


def test_session_that_cannot_start_stops_the_build(tmp_path):
    project(tmp_path, feats(([], "todo")), NOTHING)
    r = subprocess.run([sys.executable, str(SCRIPT), "--session-cmd", str(tmp_path / "no-such-program")],
                       cwd=tmp_path, text=True, capture_output=True)
    assert r.returncode == 1 and "could not start" in r.stderr


def test_session_cmd_without_command_is_usage_error(tmp_path):
    project(tmp_path, feats(([], "todo")), NOTHING)
    r = subprocess.run([sys.executable, str(SCRIPT), "--session-cmd"], cwd=tmp_path, text=True, capture_output=True)
    assert r.returncode == 1 and "usage" in r.stderr
