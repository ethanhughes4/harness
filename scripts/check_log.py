"""Print every non-empty permission_denials in a build-log.jsonl; exit 1 if any (D7, D28)."""
import json
import sys


def main(path):
    found = 0
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            try:
                msg = json.loads(line)
            except ValueError:
                continue  # non-JSON lines are skipped
            if isinstance(msg, dict) and msg.get("permission_denials"):
                found += 1
                print(f"line {n}: {json.dumps(msg['permission_denials'])}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
