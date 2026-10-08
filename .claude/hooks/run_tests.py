"""Hook: the tests must pass before Claude (or a builder) can finish.

Main session (Stop): runs pytest if a .py file has uncommitted changes.
Builders (the Stop hook in builder.md's frontmatter, run as SubagentStop, called
with --always): always runs pytest, because a builder commits its work, so git
shows nothing as changed.
If git cannot answer, pytest runs. Exit code 2 blocks.

A run past WARN_SHARE of the limit prints a warning, so the tests cannot quietly
outgrow it.
"""
import json
import os
import subprocess
import sys
import time

PASSING = (0, 5)  # pytest 5: no tests found
TAIL = 30  # lines of a failing run shown
LIMIT = 510  # seconds; must equal the hook "timeout" in settings.json and builder.md
WARN_SHARE = 0.8  # warn when a run takes more than this share of LIMIT


def needs_tests(changed, always):
    """changed: paths from git status, or None when git could not answer."""
    return always or changed is None or any(p.endswith(".py") for p in changed)


def changed_paths(folder):
    git = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"],
                         capture_output=True, text=True, cwd=folder)
    if git.returncode != 0:
        return None
    # "XY path" or "XY old -> new"; quoted paths lose their quotes
    return [line[3:].split(" -> ")[-1].strip('"') for line in git.stdout.splitlines()]


def warning(seconds):
    """A warning line when the tests took more than WARN_SHARE of LIMIT, else None."""
    if seconds <= WARN_SHARE * LIMIT:
        return None
    return (f"WARNING: the tests took {seconds:.0f} s, over {WARN_SHARE:.0%} of the hook's "
            f"{LIMIT} s limit. Speed them up or raise the limit before they time out.")


def main():
    always = "--always" in sys.argv
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    folder = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR", ".")
    if not needs_tests(None if always else changed_paths(folder), always):
        return
    start = time.monotonic()
    result = subprocess.run([sys.executable, "-m", "pytest", "-q"],
                            capture_output=True, text=True, cwd=folder)
    warn = warning(time.monotonic() - start)
    if result.returncode not in PASSING:
        lines = (result.stdout + result.stderr).splitlines()[-TAIL:]
        print("Tests are failing. Fix them before finishing.\npytest failed:\n"
              + "\n".join(lines) + (f"\n\n{warn}" if warn else ""), file=sys.stderr)
        sys.exit(2)
    if warn:
        print(json.dumps({"systemMessage": warn}))  # shown to the user; does not block


if __name__ == "__main__":
    main()
