"""Shared by every hook script. Standard library only."""
import json
import os


def config(cwd):
    """The parsed <cwd>/.claude/harness.json, or None (hooks then exit 0, D14)."""
    try:
        with open(os.path.join(cwd, ".claude", "harness.json"), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None
