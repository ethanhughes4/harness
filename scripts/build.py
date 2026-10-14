"""python build.py [--session-cmd CMD ARGS...]: the build loop (D69). Run from the project root.

Starts a fresh organiser session while a feature is ready; stops when none is, or after two
sessions in a row leave feature_list.json unchanged. --session-cmd replaces the whole `claude`
command (tests stub it); it must be the last argument.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import config, setting  # noqa: E402

CLAUDE = ["claude", "-p", "--agent", "harness:organiser", "Run the next jobs", "--permission-mode", "auto",
          "--permission-prompts", "none", "--output-format", "stream-json", "--verbose"]


def load():
    with open("feature_list.json", encoding="utf-8") as f:
        return json.load(f)


def state(f):
    return f.get("status") or ("done" if f.get("passes") else "todo")


def ready(features, limit):
    """Ids a session would take: todo or rework (or left building/review by a crash), deps done."""
    done = {str(f["id"]) for f in features if state(f) == "done"}
    return [str(f["id"]) for f in features
            if state(f) in ("todo", "rework", "building", "review") and not f.get("owner-writes")
            and all(str(d) in done for d in f.get("depends_on", []))][:limit]


def status_line(features):
    n = sum(state(f) == "done" for f in features)
    k = sum(state(f) == "needs-human" for f in features)
    return f"feature_list: {n}/{len(features)} done, {k} needs-human"


def main(argv):
    cmd = CLAUDE
    if "--session-cmd" in argv:
        cmd = argv[argv.index("--session-cmd") + 1:]
        if not cmd:
            print("usage: build.py [--session-cmd CMD ARGS...]", file=sys.stderr)
            return 1
    limit = setting(config(os.getcwd()), "max_builders")
    idle = 0
    while True:
        features = load()
        if not ready(features, limit) or idle >= 2:
            break
        before = json.dumps(features, sort_keys=True)
        r = subprocess.run(cmd, stdout=subprocess.PIPE)
        with open("build-log.jsonl", "ab") as log:
            log.write(r.stdout)
        features = load()
        idle = idle + 1 if json.dumps(features, sort_keys=True) == before else 0
        print(status_line(features), flush=True)
    print(status_line(load()), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
