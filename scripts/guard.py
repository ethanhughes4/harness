"""PreToolUse hook (Edit|Write|Bash): block changes to feature_list.json and `protected` paths.

Blocks with exit 2 and the reason on stderr. Only scripts/mark_pass.py and scripts/status.py may change
the list (D17, D68). A reviewer agent listed in factory.json may write only its own review file (D64).
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
STATUS = re.compile(r'\s*python3?(\.exe)?\s+("[^"$`]*"|[^\s;&|<>`$"]+)status\.py\s+[\w.-]+\s+[a-z-]+\s*')
REVIEW = re.compile(r"\.harness/jobs/[\w.-]+/round-\d+/review-([\w.-]+)\.md")


def reviewer_names(agent):
    """Names of the factory.json reviewers run by this agent type, or None if it is not a reviewer."""
    plugin_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        with open(os.path.join(plugin_root, "factory.json"), encoding="utf-8") as f:
            names = {r["name"] for r in json.load(f)["reviewers"] if r["agent"] == agent}
    except (OSError, ValueError, KeyError, TypeError):
        return None
    return names or None


def relative(path, cwd):
    path = path.replace("\\", "/")
    if os.path.isabs(path):
        path = os.path.relpath(path, cwd)  # ValueError on another Windows drive
    return os.path.normpath(path).replace("\\", "/")


def own_review(path, cwd, names):
    try:
        m = REVIEW.fullmatch(relative(path, cwd))
    except ValueError:
        return False
    return bool(m) and m.group(1) in names


def blocked_path(path, cwd, protected):
    try:
        path = relative(path, cwd)
    except ValueError:  # other drive on Windows
        return False
    return path == LIST or any(fnmatch.fnmatch(path, g) for g in protected)


def blocked_command(cmd, protected):
    cmd = cmd.replace("\\", "/")
    if MARK_PASS.fullmatch(cmd) or STATUS.fullmatch(cmd):
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
    names = reviewer_names(data.get("agent_type"))
    if tool in ("Edit", "Write") and names is not None:
        if own_review(inp.get("file_path", ""), cwd, names):
            return 0
        print("Blocked: a reviewer may write only .harness/jobs/<id>/round-<n>/review-<name>.md "
              f"with its own name ({', '.join(sorted(names))}).", file=sys.stderr)
        return 2
    if tool in ("Edit", "Write"):
        hit = blocked_path(inp.get("file_path", ""), cwd, protected)
    elif tool == "Bash":
        hit = blocked_command(inp.get("command", ""), protected)
    else:
        return 0
    if hit:
        print(f"Blocked: {LIST} and protected paths can't be changed directly. "
              f"Use: python <plugin_root>/scripts/mark_pass.py <id> or status.py <id> <status>", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
