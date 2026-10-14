"""python status.py <id> <status>: set that feature's `status` in ./feature_list.json (D68).

`done` also sets `passes` true. Edits the text in place, so every other byte is unchanged.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mark_pass import mark  # noqa: E402

STATUSES = ("todo", "building", "review", "rework", "needs-human", "done")
STATUS = re.compile(r'((?<!\\)"status"\s*:\s*)"[^"]*"')


def set_status(text, fid, status):
    dec, pos = json.JSONDecoder(), text.index("[") + 1
    while True:
        pos += len(text[pos:]) - len(text[pos:].lstrip(" \t\r\n,"))
        if text[pos] == "]":
            raise KeyError(fid)
        obj, end = dec.raw_decode(text, pos)
        if str(obj.get("id")) == fid:
            # ponytail: first `"status": "..."` in the object; a step quoting it unescaped is impossible in JSON
            m = STATUS.search(text, pos, end) if "status" in obj else None
            if m:
                text = text[:m.start()] + m.group(1) + json.dumps(status) + text[m.end():]
            else:  # new key goes first, copying the whitespace before the first key
                rest = text[pos + 1:end]
                ws = rest[:len(rest) - len(rest.lstrip(" \t\r\n"))]
                text = text[:pos + 1] + ws + f'"status": "{status}",' + text[pos + 1:]
            return mark(text, fid) if status == "done" else text
        pos = end


def main(argv):
    if len(argv) != 3 or argv[2] not in STATUSES:
        print(f"usage: status.py <id> {'|'.join(STATUSES)}", file=sys.stderr)
        return 1
    try:
        with open("feature_list.json", encoding="utf-8", newline="") as f:
            text = f.read()
        new = set_status(text, argv[1], argv[2])
    except (OSError, ValueError, KeyError, IndexError):
        print(f"cannot set status: unknown feature id or bad feature_list.json: {argv[1]}", file=sys.stderr)
        return 1
    with open("feature_list.json", "w", encoding="utf-8", newline="") as f:
        f.write(new)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
