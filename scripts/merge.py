"""python merge.py <id> <round>: merge factory/<id> into the checked-out branch, only if it is allowed (D108).

The one place a job merges. Checks, in order: gates-<round>.md is PASS; every review the job needs exists
in round-<round>/ and every review file there is PASS (needed = `always` reviewers in factory.json, plus
`high_risk` ones when risk.py says high, plus `ui` ones for a `"ui": true` feature). Then a high-risk job
is NOT merged: status needs-human, the reason in decision.md, branch and worktree kept (D67). Low risk:
`git merge --no-ff`, run every `test` command, status done. Red tests: the merge is undone (reset --keep,
so uncommitted job files survive). Run from the project root.

Exit: 0 merged, 1 usage or error, 2 not ready (reason printed), 3 high risk, parked for the owner,
4 merge conflict (aborted), 5 tests red (merge undone).
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import status  # noqa: E402
from common import config, setting  # noqa: E402
from risk import assess, git  # noqa: E402

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def first_line(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.readline().strip()
    except OSError:
        return None


def needed(fid, high):
    with open(os.path.join(PLUGIN, "factory.json"), encoding="utf-8") as f:
        reviewers = json.load(f)["reviewers"]
    with open("feature_list.json", encoding="utf-8") as f:
        ui = any(str(x.get("id")) == fid and x.get("ui") is True for x in json.load(f))
    return [r["name"] for r in reviewers
            if r["when"] == "always" or (r["when"] == "high_risk" and high) or (r["when"] == "ui" and ui)]


def not_ready(fid, rnd, high):
    """Why the job may not merge yet, or None."""
    job = os.path.join(".harness", "jobs", fid)
    if first_line(os.path.join(job, f"gates-{rnd}.md")) != "GATES: PASS":
        return f"gates-{rnd}.md is missing or not GATES: PASS"
    folder = os.path.join(job, f"round-{rnd}")
    names = needed(fid, high)
    for n in names:
        if first_line(os.path.join(folder, f"review-{n}.md")) != "VERDICT: PASS":
            return f"review-{n}.md is missing or not VERDICT: PASS"
    for f in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
        if f.startswith("review-") and f.endswith(".md") and first_line(os.path.join(folder, f)) != "VERDICT: PASS":
            return f"{f} is not VERDICT: PASS"
    return None


def park(fid, rnd, files):
    status.main(["status.py", fid, "needs-human"])
    job = os.path.join(".harness", "jobs", fid)
    with open(os.path.join(job, "decision.md"), "a", encoding="utf-8") as f:
        f.write(f"\nHigh risk, round {rnd}: all required reviews passed but the job is NOT merged. It waits for "
                f"the owner (/harness:approve {fid}). Branch factory/{fid} and worktree .harness/wt/{fid} kept. "
                f"Risky files: {', '.join(files)}. Reviews: {job}/round-{rnd}/review-*.md\n")


def main(argv):
    if len(argv) != 3:
        print("usage: merge.py <id> <round>", file=sys.stderr)
        return 1
    fid, rnd = argv[1], argv[2]
    cfg = config(os.getcwd())
    if cfg is None:
        print("no .claude/harness.json", file=sys.stderr)
        return 1
    try:
        risk = assess(fid)
        high = risk["risk"] == "high"
        why = not_ready(fid, rnd, high)
    except (RuntimeError, OSError, ValueError, KeyError) as e:
        print(f"cannot merge {fid}: {e}", file=sys.stderr)
        return 1
    if why:
        print(f"not ready: {why}")
        return 2
    if high:
        park(fid, rnd, risk["files"])
        print(f"high risk, not merged: status needs-human, branch kept. Risky files: {', '.join(risk['files'])}")
        return 3
    before = git("rev-parse", "HEAD").stdout.strip()
    if git("merge", "--no-ff", "-m", f"Merge factory/{fid}", f"factory/{fid}").returncode:
        git("merge", "--abort")
        print("merge conflict, aborted: send the builder the conflict (merge the main branch into the job branch)")
        return 4
    for cmd in setting(cfg, "test"):
        try:
            r = subprocess.run(cmd, timeout=setting(cfg, "test_limit_s"), text=True, errors="replace",
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            ok, out = r.returncode == 0, r.stdout
        except (subprocess.TimeoutExpired, OSError) as e:
            ok, out = False, str(e)
        if not ok:
            git("reset", "--keep", before)
            print(f"tests red after merge, merge undone: {' '.join(cmd)}\n" + "\n".join(out.splitlines()[-40:]))
            return 5
    status.main(["status.py", fid, "done"])
    print(f"merged {fid}, tests green, status done")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
