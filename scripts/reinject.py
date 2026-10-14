"""SessionStart (compact) hook: re-inject key context, under 2 KB (D18)."""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import config  # noqa: E402

CAP = 2000


def read(cwd, rel):
    try:
        with open(os.path.join(cwd, rel), encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def build(cwd):
    parts = []
    brief = read(cwd, "docs/brief.md")
    m = brief and re.search(r"^## Must never[ \t]*\n(.*?)(?=^## |\Z)", brief, re.M | re.S)
    if m and m.group(1).strip():
        parts.append("Must never:\n" + m.group(1).strip())
    try:
        feats = json.loads(read(cwd, "feature_list.json") or "")
        done = {f.get("id") for f in feats if f.get("passes")}
        todo = [f"{f['id']}: {f.get('title', '')}" for f in feats
                if not f.get("passes") and all(d in done for d in f.get("depends_on", []))]
        if todo:
            parts.append("Features in progress:\n" + "\n".join(todo))
    except (ValueError, TypeError, AttributeError, KeyError):
        pass
    paths = [p for p in ("docs/owner.md", "docs/decisions.md") if os.path.exists(os.path.join(cwd, p))]
    if paths:
        parts.append("Read when needed: " + ", ".join(paths))
    prog = read(cwd, "progress.md")
    if prog and prog.strip():
        parts.append("Last progress.md lines:\n" + "\n".join(prog.rstrip().splitlines()[-20:]))
    text = "\n\n".join(parts)
    # ponytail: byte cut can drop the tail of progress; fine, it is the lowest priority
    return text.encode("utf-8")[:CAP].decode("utf-8", "ignore")


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    cwd = data.get("cwd") or os.getcwd()
    if config(cwd) is None:
        return
    text = build(cwd)
    if text:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                                 "additionalContext": text}}))


if __name__ == "__main__":
    main()
