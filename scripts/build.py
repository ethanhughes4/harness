"""python build.py [--session-cmd CMD ARGS...]: the build loop (D69). Run from the project root.

Starts a fresh organiser session while a feature is ready; stops when none is, or after two
sessions in a row leave feature_list.json unchanged. --session-cmd replaces the whole `claude`
command (tests stub it; `claude` is then never run); it must be the last argument. A session that
exits nonzero or cannot start stops the build with exit 1; its output stays in build-log.jsonl.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import config, setting  # noqa: E402

CLAUDE = ["claude", "-p", "--agent", "harness:organiser", "Run the next jobs", "--permission-mode", "auto",
          "--permission-prompts", "none", "--output-format", "stream-json", "--verbose"]


def with_plugin_dir(cmd, plugin_list, plugin_root):
    """Add --plugin-dir when the harness plugin isn't installed (e.g. while developing it)."""
    if plugin_root and "harness@" not in plugin_list:
        return cmd + ["--plugin-dir", plugin_root]
    return cmd


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
    cfg = config(os.getcwd())
    if "--session-cmd" in argv:
        cmd = argv[argv.index("--session-cmd") + 1:]
        if not cmd:
            print("usage: build.py [--session-cmd CMD ARGS...]", file=sys.stderr)
            return 1
    else:
        listed = subprocess.run(["claude", "plugin", "list"], capture_output=True, text=True, errors="replace")
        cmd = with_plugin_dir(CLAUDE, listed.stdout or "", (cfg or {}).get("plugin_root"))
    limit = setting(cfg, "max_builders")
    idle = 0
    while True:
        features = load()
        if not ready(features, limit) or idle >= 2:
            break
        before = json.dumps(features, sort_keys=True)
        with open("build-log.jsonl", "ab") as log:  # streamed, so a killed session keeps its log
            try:
                code = subprocess.run(cmd, stdout=log).returncode
            except OSError as e:
                code = f"could not start: {e}"
        if code != 0:
            print(f"session failed ({code}); see build-log.jsonl. {status_line(load())}", file=sys.stderr, flush=True)
            return 1
        features = load()
        idle = idle + 1 if json.dumps(features, sort_keys=True) == before else 0
        print(status_line(features), flush=True)
    print(status_line(load()), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
