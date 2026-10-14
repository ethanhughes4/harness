"""python risk.py <id>: print {"risk": "low"|"high", "files": [...]} for branch factory/<id> against the checked-out branch (D63)."""
import fnmatch
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import config, setting  # noqa: E402


def git(*args):
    return subprocess.run(["git", *args], text=True, capture_output=True)


def classify(files, globs):
    # ponytail: fnmatch on the lowercased path, where * also crosses /; over-flags (author.md matches *auth*)
    hit = [f for f in files if any(fnmatch.fnmatch(f.lower(), g.lower()) for g in globs)]
    return {"risk": "high" if hit else "low", "files": hit}


def main(argv):
    if len(argv) != 2:
        print("usage: risk.py <id>", file=sys.stderr)
        return 1
    # the branch the project has checked out is the one jobs merge into; never guess "main"
    base = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip() or "HEAD"
    r = git("diff", "--name-only", f"{base}...factory/{argv[1]}")
    if r.returncode:
        print(f"cannot diff {base}...factory/{argv[1]}: {r.stderr.strip()}", file=sys.stderr)
        return 1
    files = [f.replace("\\", "/") for f in r.stdout.split("\n") if f]
    print(json.dumps(classify(files, setting(config(os.getcwd()), "risky"))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
