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


RISKY = ["*auth*", "*payment*", "*crypto*", "*secret*", "*migration*", ".github/*", ".gitlab-ci.yml",
         "*package.json", "*package-lock.json", "*requirements*.txt", "*pyproject.toml", "*poetry.lock",
         "*cargo.toml", "*cargo.lock", "*go.mod", "*go.sum", ".claude/*"]
DEFAULTS = {"max_builders": 2, "gates": [], "risky": RISKY, "acceptance_dir": "tests/acceptance",
            "walkthrough_every": 5, "run": None, "test": [], "test_limit_s": 300}


def setting(cfg, key):
    """cfg[key], or the default for that key."""
    return (cfg or {}).get(key, DEFAULTS[key])
