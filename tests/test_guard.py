import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "guard.py"


def run(cwd, tool, **tool_input):
    return subprocess.run([sys.executable, str(SCRIPT)], text=True, capture_output=True,
                          input=json.dumps({"hook_event_name": "PreToolUse", "cwd": str(cwd),
                                            "tool_name": tool, "tool_input": tool_input}))


def setup(tmp_path):
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "harness.json").write_text(json.dumps({"protected": ["data/raw/**"]}))


def test_list_blocked(tmp_path):
    setup(tmp_path)
    for r in (run(tmp_path, "Edit", file_path=str(tmp_path / "feature_list.json")),
              run(tmp_path, "Write", file_path="feature_list.json"),
              run(tmp_path, "Bash", command="rm feature_list.json"),
              run(tmp_path, "Bash", command="sed -i s/a/b/ .\\feature_list.json")):
        assert r.returncode == 2 and "mark_pass" in r.stderr


def test_protected_blocked(tmp_path):
    setup(tmp_path)
    assert run(tmp_path, "Write", file_path=str(tmp_path / "data" / "raw" / "a" / "b.csv")).returncode == 2
    assert run(tmp_path, "Bash", command="echo x > data/raw/b.csv").returncode == 2


def test_other_allowed(tmp_path):
    setup(tmp_path)
    assert run(tmp_path, "Edit", file_path=str(tmp_path / "src" / "a.py")).returncode == 0
    assert run(tmp_path, "Bash", command="ls src").returncode == 0
    assert run(tmp_path, "Read", file_path="feature_list.json").returncode == 0


def test_mark_pass_allowed(tmp_path):
    setup(tmp_path)
    ok = "python /p/scripts/mark_pass.py F1"
    assert run(tmp_path, "Bash", command=ok).returncode == 0
    assert run(tmp_path, "Bash", command='python "C:\\my plugin\\scripts\\mark_pass.py" 3').returncode == 0
    assert run(tmp_path, "Bash", command=ok + "; rm feature_list.json").returncode == 2


def test_no_config_allowed(tmp_path):
    assert run(tmp_path, "Bash", command="rm feature_list.json").returncode == 0


def test_status_allowed(tmp_path):
    setup(tmp_path)
    ok = "python /p/scripts/status.py F1 needs-human"
    assert run(tmp_path, "Bash", command=ok).returncode == 0
    assert run(tmp_path, "Bash", command=ok + "; rm feature_list.json").returncode == 2
    assert run(tmp_path, "Bash", command="sed -i s/a/b/ feature_list.json").returncode == 2


def run_as(cwd, agent, tool, **tool_input):
    return subprocess.run([sys.executable, str(SCRIPT)], text=True, capture_output=True,
                          input=json.dumps({"hook_event_name": "PreToolUse", "cwd": str(cwd), "agent_type": agent,
                                            "agent_id": "a1", "tool_name": tool, "tool_input": tool_input}))


def test_reviewer_writes_only_own_review(tmp_path):
    setup(tmp_path)
    rev = ".harness/jobs/F1/round-1/review-code.md"
    assert run_as(tmp_path, "harness:reviewer", "Write", file_path=rev).returncode == 0
    assert run_as(tmp_path, "harness:reviewer", "Write", file_path=str(tmp_path / rev)).returncode == 0
    for bad in (".harness/jobs/F1/round-1/review-visual.md", "src/a.py", ".harness/jobs/F1/decision.md",
                ".harness/jobs/F1/round-1/../../../../x.md"):
        assert run_as(tmp_path, "harness:reviewer", "Edit", file_path=bad).returncode == 2, bad
    # other agents are not limited to review files
    assert run_as(tmp_path, "harness:builder", "Write", file_path="src/a.py").returncode == 0
