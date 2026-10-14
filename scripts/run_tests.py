"""Stop / SubagentStop hook: run the project's test commands; exit 2 blocks the finish."""
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import config  # noqa: E402

TAIL = 3000  # chars of failing output sent back to Claude


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        data = {}
    cwd = data.get("cwd") or os.getcwd()
    cfg = config(cwd)
    if cfg is None:
        return 0
    limit = cfg.get("test_limit_s", 300)
    for cmd in cfg.get("test", []):
        start = time.monotonic()
        try:
            r = subprocess.run(cmd, cwd=cwd, timeout=limit, text=True, errors="replace",
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            ok, out = r.returncode == 0, r.stdout
        except subprocess.TimeoutExpired as e:
            partial = e.stdout.decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
            ok, out = False, f"killed after {limit}s (test_limit_s)\n{partial}"
        except OSError as e:
            ok, out = False, str(e)
        took = time.monotonic() - start
        if ok and took > 0.8 * limit:
            print(f"warning: {' '.join(cmd)} took {took:.0f}s of the {limit}s limit", file=sys.stderr)
        if not ok:
            print(f"Tests failed: {' '.join(cmd)}\n{out[-TAIL:]}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
