"""StopFailure hook: log the API error to progress.md. Logging only."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import config  # noqa: E402


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    cwd = data.get("cwd") or os.getcwd()
    if config(cwd) is None:
        return
    lines = [f"## {time.strftime('%Y-%m-%d %H:%M')} API error stopped the run",
             f"error: {data.get('error', 'unknown')}"]
    if data.get("error_details"):
        lines.append(f"details: {data['error_details']}")
    with open(os.path.join(cwd, "progress.md"), "a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
