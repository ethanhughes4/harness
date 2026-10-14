"""python mark_pass.py <id>: set that feature's `passes` to true in ./feature_list.json.

Edits the text in place, so every other byte of the file is unchanged.
"""
import json
import re
import sys

PASSES = re.compile(r'("passes"\s*:\s*)false')


def mark(text, fid):
    dec, pos = json.JSONDecoder(), text.index("[") + 1
    while True:
        pos += len(text[pos:]) - len(text[pos:].lstrip(" \t\r\n,"))
        if text[pos] == "]":
            raise KeyError(fid)
        obj, end = dec.raw_decode(text, pos)
        if str(obj.get("id")) == fid:
            if obj.get("passes") is True:
                return text
            # ponytail: last `"passes": false` in the object; step text containing it after the key would fool this
            ms = list(PASSES.finditer(text, pos, end))
            if not ms:
                raise KeyError(fid)
            m = ms[-1]
            return text[:m.start()] + m.group(1) + "true" + text[m.end():]
        pos = end


def main(argv):
    if len(argv) != 2:
        print("usage: mark_pass.py <id>", file=sys.stderr)
        return 1
    try:
        with open("feature_list.json", encoding="utf-8", newline="") as f:
            text = f.read()
        new = mark(text, argv[1])
    except (OSError, ValueError, KeyError, IndexError):
        print(f"cannot mark: unknown feature id or bad feature_list.json: {argv[1]}", file=sys.stderr)
        return 1
    with open("feature_list.json", "w", encoding="utf-8", newline="") as f:
        f.write(new)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
