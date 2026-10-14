"""python gates.py <id> <round>: run the checks with no AI and write .harness/jobs/<id>/gates-<round>.md (D62).

Runs every `test` command, every `gates` command and the acceptance tamper check, in the job's
worktree .harness/wt/<id> (or here if there is none). Exit 0 if all pass, 1 if not.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import config, setting  # noqa: E402

CAP = 100  # lines of output kept


def run(cmd, cwd, limit):
    try:
        r = subprocess.run(cmd, cwd=cwd, timeout=limit, text=True, errors="replace",
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return r.returncode == 0, r.stdout
    except subprocess.TimeoutExpired:
        return False, f"killed after {limit}s (test_limit_s)"
    except OSError as e:
        return False, str(e)


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True).stdout


def tamper(cwd, job, adir, fid):
    """Acceptance files changed since the test writer's commit (sha in <job>/acceptance.sha), or uncommitted."""
    path = f"{adir}/{fid}"
    out = [l[3:] for l in git(cwd, "status", "--porcelain", "--", path).splitlines()]
    sha = os.path.join(job, "acceptance.sha")
    if os.path.exists(sha):
        with open(sha, encoding="utf-8") as f:
            out += git(cwd, "diff", "--name-only", f.read().strip(), "--", path).split()
    return sorted(set(out))


def main(argv):
    if len(argv) != 3:
        print("usage: gates.py <id> <round>", file=sys.stderr)
        return 1
    fid, rnd = argv[1], argv[2]
    root = os.getcwd()
    cfg = config(root)
    if cfg is None:
        print("no .claude/harness.json", file=sys.stderr)
        return 1
    wt = os.path.join(root, ".harness", "wt", fid)
    cwd = wt if os.path.isdir(wt) else root
    job = os.path.join(root, ".harness", "jobs", fid)
    limit = setting(cfg, "test_limit_s")
    lines, failed = [], False
    for kind in ("test", "gates"):
        for cmd in setting(cfg, kind):
            ok, out = run(cmd, cwd, limit)
            failed |= not ok
            lines += [f"## {kind}: {' '.join(cmd)}: {'PASS' if ok else 'FAIL'}"]
            lines += [] if ok else out.splitlines()[-40:]
    changed = tamper(cwd, job, setting(cfg, "acceptance_dir"), fid)
    failed |= bool(changed)
    lines.append(f"## acceptance tamper check: {'FAIL' if changed else 'PASS'}")
    lines += [f"changed: {c}" for c in changed]
    if len(lines) > CAP - 1:
        lines = lines[:CAP - 2] + [f"... {len(lines) - CAP + 2} more lines cut"]
    text = "\n".join([f"GATES: {'FAIL' if failed else 'PASS'}"] + lines) + "\n"
    os.makedirs(job, exist_ok=True)
    with open(os.path.join(job, f"gates-{rnd}.md"), "w", encoding="utf-8") as f:
        f.write(text)
    print(text, end="")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
