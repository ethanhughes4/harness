"""PreToolUse hook (Edit|Write|Bash): block changes to feature_list.json and `protected` paths.

Blocks with exit 2 and the reason on stderr. Only scripts/mark_pass.py may change the list (D17).
"""
import fnmatch
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import config  # noqa: E402

LIST = "feature_list.json"
# a lone `python <path>mark_pass.py <id>`: no shell operators outside quotes
MARK_PASS = re.compile(r'\s*python3?(\.exe)?\s+("[^"$`]*"|[^\s;&|<>`$"]+)mark_pass\.py\s+[\w.-]+\s*')


def blocked_path(path, cwd, protected):
    path = path.replace("\\", "/")
    if os.path.isabs(path):
        try:
            path = os.path.relpath(path, cwd)
        except ValueError:  # other drive on Windows
            return False
    path = os.path.normpath(path).replace("\\", "/")
    return path == LIST or any(fnmatch.fnmatch(path, g) for g in protected)


def blocked_command(cmd, protected):
    cmd = cmd.replace("\\", "/")
    if MARK_PASS.fullmatch(cmd):
        return False
    # ponytail: substring match on each glob's literal prefix; over-blocks, and misses
    # globs that start with a wildcard
    prefixes = [re.split(r"[*?\[]", g)[0] for g in protected]
    return LIST in cmd or any(p and p in cmd for p in prefixes)


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return 0
    cwd = data.get("cwd") or os.getcwd()
    cfg = config(cwd)
    if cfg is None:
        return 0
    protected = [g.replace("\\", "/") for g in cfg.get("protected", [])]
    tool, inp = data.get("tool_name"), data.get("tool_input") or {}
    if tool in ("Edit", "Write"):
        hit = blocked_path(inp.get("file_path", ""), cwd, protected)
    elif tool == "Bash":
        hit = blocked_command(inp.get("command", ""), protected)
    else:
        return 0
    if hit:
        print(f"Blocked: {LIST} and protected paths can't be changed directly. "
              f"Mark a feature done with: python <plugin_root>/scripts/mark_pass.py <id>", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
