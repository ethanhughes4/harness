import copy
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INIT = ROOT / "scripts" / "init_features.py"
GUARD = ROOT / "scripts" / "guard.py"
CANDIDATE = "init-features-candidate.tmp"
# the repo's own smoke list is the schema fixture: two real features, F2 depends on F1
SMOKE = json.loads((ROOT / "skills" / "smoke" / "feature_list.json").read_text(encoding="utf-8"))


def feature(fid, deps=(), **over):
    f = copy.deepcopy(SMOKE[0])
    f.update(id=fid, title=f"feature {fid}", depends_on=list(deps), **over)
    return f


def project(tmp_path, existing=None, candidate=None, raw=None):
    if existing is not None:
        (tmp_path / "feature_list.json").write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
    if raw is not None:
        (tmp_path / CANDIDATE).write_text(raw, encoding="utf-8")
    elif candidate is not None:
        (tmp_path / CANDIDATE).write_text(json.dumps(candidate), encoding="utf-8")


def run(tmp_path, mode="--check", name=CANDIDATE):
    return subprocess.run([sys.executable, str(INIT), mode, name], cwd=tmp_path, text=True, capture_output=True)


def listed(tmp_path):
    return json.loads((tmp_path / "feature_list.json").read_text(encoding="utf-8"))


def rejects(tmp_path, existing, candidate, message=""):
    """Both --check and --apply fail with `message`, and the list is byte-for-byte as it was."""
    path = tmp_path / "feature_list.json"
    path.unlink(missing_ok=True)
    project(tmp_path, existing, candidate)
    before = path.read_bytes() if path.exists() else None
    for mode in ("--check", "--apply"):
        r = run(tmp_path, mode)
        assert r.returncode == 1 and message in r.stderr, (mode, r.stderr)
    assert (path.read_bytes() if path.exists() else None) == before


def test_creates_list_when_none_exists(tmp_path):
    project(tmp_path, None, SMOKE)
    r = run(tmp_path, "--apply")
    assert r.returncode == 0, r.stderr
    assert listed(tmp_path) == SMOKE
    assert not (tmp_path / "feature_list.json.tmp").exists()  # the atomic-replace temp file is gone


def test_appends_without_losing_existing_records(tmp_path):
    existing = copy.deepcopy(SMOKE)
    existing[0].update(status="done", passes=True, extra_key="kept")
    project(tmp_path, existing, [feature("F3", ["F2"]), feature("F4", ["F3", "F1"])])
    assert run(tmp_path, "--apply").returncode == 0
    now = listed(tmp_path)
    assert now[:2] == existing  # untouched, including status, passes and unknown keys
    assert [f["id"] for f in now] == ["F1", "F2", "F3", "F4"]
    assert all(f["status"] == "todo" and f["passes"] is False for f in now[2:])


def test_check_does_not_change_the_list(tmp_path):
    project(tmp_path, SMOKE, [feature("F3")])
    before = (tmp_path / "feature_list.json").read_bytes()
    r = run(tmp_path, "--check")
    assert r.returncode == 0 and "F3" in r.stdout and "No changes" in r.stdout
    assert (tmp_path / "feature_list.json").read_bytes() == before
    # and it creates nothing when there was no list
    fresh = tmp_path / "fresh"
    fresh.mkdir()
    project(fresh, None, [feature("F1")])
    assert run(fresh, "--check").returncode == 0
    assert not (fresh / "feature_list.json").exists()


def test_rejects_duplicate_ids_in_candidate(tmp_path):
    rejects(tmp_path, SMOKE, [feature("F3"), feature("F3")], "Duplicate feature ID: F3")


def test_rejects_id_already_in_list(tmp_path):
    rejects(tmp_path, SMOKE, [feature("F2")], "Duplicate feature ID: F2")


def test_rejects_unknown_dependency(tmp_path):
    rejects(tmp_path, SMOKE, [feature("F3", ["F9"])], "unknown dependency F9")


def test_accepts_dependency_on_new_feature_in_same_candidate(tmp_path):
    project(tmp_path, SMOKE, [feature("F4", ["F3"]), feature("F3")])
    assert run(tmp_path).returncode == 0


def test_rejects_self_dependency_and_cycles(tmp_path):
    rejects(tmp_path, SMOKE, [feature("F3", ["F3"])], "cannot depend on itself")
    rejects(tmp_path, SMOKE, [feature("F3", ["F4"]), feature("F4", ["F3"])], "cycle")


def test_rejects_missing_required_field(tmp_path):
    for key in ("id", "stage", "title", "ui", "depends_on", "steps", "status", "passes"):
        f = feature("F3")
        del f[key]
        rejects(tmp_path, SMOKE, [f], "missing required field")


def test_rejects_malformed_values(tmp_path):
    rejects(tmp_path, SMOKE, [feature("F3", steps=[])], "step")
    rejects(tmp_path, SMOKE, [feature("F3", ui="yes")], "ui must be")
    rejects(tmp_path, SMOKE, [feature("F3", **{"owner-writes": False})], "owner-writes")
    rejects(tmp_path, SMOKE, [], "at least one")
    rejects(tmp_path, SMOKE, {"id": "F3"}, "at least one")
    rejects(tmp_path, SMOKE, ["F3"], "object")


def test_rejects_malformed_json(tmp_path):
    project(tmp_path, SMOKE, raw="[{not json")
    r = run(tmp_path, "--apply")
    assert r.returncode == 1 and "valid JSON" in r.stderr
    assert listed(tmp_path) == SMOKE


def test_rejects_corrupt_existing_list(tmp_path):
    (tmp_path / "feature_list.json").write_text("{broken", encoding="utf-8")
    project(tmp_path, None, [feature("F3")])
    assert run(tmp_path, "--apply").returncode == 1
    assert (tmp_path / "feature_list.json").read_text() == "{broken"


def test_rejects_wrong_initial_status_and_passes(tmp_path):
    for status in ("done", "building", "review", "rework", "needs-human", "bogus"):
        rejects(tmp_path, SMOKE, [feature("F3", status=status)], "must start as todo")
    for passes in (True, "false", 0, None):
        rejects(tmp_path, SMOKE, [feature("F3", passes=passes)], "passes must start as false")


def test_rejects_wrong_candidate_location_or_name(tmp_path):
    project(tmp_path, SMOKE)
    (tmp_path / "other.json").write_text(json.dumps([feature("F3")]))
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / CANDIDATE).write_text(json.dumps([feature("F3")]))
    for name in ("other.json", f"sub/{CANDIDATE}", "feature_list.json", f"../{CANDIDATE}"):
        r = run(tmp_path, "--apply", name)
        assert r.returncode == 1 and "designated" in r.stderr, name
    r = run(tmp_path, "--apply")  # right name, but the file is missing
    assert r.returncode == 1 and "does not exist" in r.stderr
    assert listed(tmp_path) == SMOKE


# ---- the guard: who may run it ----

def guard(cwd, tool, agent=None, **tool_input):
    data = {"hook_event_name": "PreToolUse", "cwd": str(cwd), "tool_name": tool, "tool_input": tool_input}
    if agent:
        data.update(agent_type=agent, agent_id="a1")
    return subprocess.run([sys.executable, str(GUARD)], text=True, capture_output=True, input=json.dumps(data))


def harness(tmp_path):
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "harness.json").write_text("{}")


CHECK = f"python /p/scripts/init_features.py --check {CANDIDATE}"
APPLY = f'python "C:\\my plugin\\scripts\\init_features.py" --apply {CANDIDATE}'


def test_direct_write_and_edit_of_the_list_stay_blocked(tmp_path):
    harness(tmp_path)
    r = guard(tmp_path, "Write", None, file_path="feature_list.json")
    assert r.returncode == 2 and "init_features" in r.stderr  # the message points at the intended route
    for agent in (None, "harness:builder", "harness:organiser", "harness:test-writer"):
        for tool in ("Write", "Edit"):
            r = guard(tmp_path, tool, agent, file_path=str(tmp_path / "feature_list.json"))
            assert r.returncode == 2 and "Blocked" in r.stderr, (agent, tool)
        assert guard(tmp_path, "Bash", agent, command="echo [] > feature_list.json").returncode == 2


def test_interactive_session_may_run_the_init_command(tmp_path):
    harness(tmp_path)
    for cmd in (CHECK, APPLY, CHECK.replace("python", "python3")):
        assert guard(tmp_path, "Bash", None, command=cmd).returncode == 0, cmd
    # writing the candidate is an ordinary file write
    assert guard(tmp_path, "Write", None, file_path=str(tmp_path / CANDIDATE)).returncode == 0


def test_subagents_cannot_use_the_init_command(tmp_path):
    harness(tmp_path)
    for agent in ("harness:builder", "harness:organiser", "harness:reviewer", "harness:security",
                  "harness:test-writer", "harness:resolver", "general-purpose"):
        for cmd in (CHECK, APPLY):
            assert guard(tmp_path, "Bash", agent, command=cmd).returncode == 2, (agent, cmd)


def test_init_command_must_be_exact(tmp_path):
    harness(tmp_path)
    for cmd in (CHECK + "; rm feature_list.json", CHECK + " && echo x",
                "python /p/init_features.py --apply other.json",
                f"python /p/init_features.py --apply ../{CANDIDATE}", "python /p/scripts/init_features.py",
                f"cat x | python /p/scripts/init_features.py --apply {CANDIDATE}",
                f"python /p/scripts/init_features.py --apply {CANDIDATE} > feature_list.json"):
        assert guard(tmp_path, "Bash", None, command=cmd).returncode == 2, cmd


def test_end_to_end_interactive_flow(tmp_path):
    """Write candidate, check, apply through the guard-approved commands exactly as init-build instructs."""
    harness(tmp_path)
    project(tmp_path, None, SMOKE)
    for mode, word in (("--check", "No changes"), ("--apply", "Applied")):
        cmd = f'python "{INIT.as_posix()}" {mode} {CANDIDATE}'
        assert guard(tmp_path, "Bash", None, command=cmd).returncode == 0, cmd
        r = run(tmp_path, mode)
        assert r.returncode == 0 and word in r.stdout
    assert listed(tmp_path) == SMOKE
