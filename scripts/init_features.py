"""python init_features.py --check|--apply init-features-candidate.tmp: add new features to ./feature_list.json.

The only way to create or extend the list (the guard blocks Write and Edit on it). --check validates and
changes nothing; --apply validates again, then replaces feature_list.json atomically. Existing features are
never changed. The candidate is a JSON list of new features at the project root. Run from the project root.
"""
import argparse
import json
import os
import sys
from pathlib import Path

CANDIDATE_NAME = "init-features-candidate.tmp"

REQUIRED = [
    "id", "stage", "title", "ui",
    "depends_on", "steps", "status", "passes"
]


def read_json(path):
    try:
        with path.open(encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(
            f"Could not read valid JSON from {path.name}: {error}"
        ) from error


def validate(existing, additions):
    if not isinstance(existing, list):
        raise ValueError("The existing feature list must be a JSON list.")

    if not isinstance(additions, list) or not additions:
        raise ValueError("The candidate must contain at least one feature.")

    existing_ids = []

    for feature in existing:
        if not isinstance(feature, dict):
            raise ValueError("An existing feature is not an object.")

        feature_id = feature.get("id")

        if not isinstance(feature_id, str) or not feature_id.strip():
            raise ValueError("An existing feature has an invalid ID.")

        if feature_id in existing_ids:
            raise ValueError(
                f"Duplicate existing feature ID: {feature_id}"
            )

        existing_ids.append(feature_id)

    new_ids = []

    for feature in additions:
        if not isinstance(feature, dict):
            raise ValueError("Every candidate feature must be an object.")

        for key in REQUIRED:
            if key not in feature:
                raise ValueError(
                    f"Feature is missing required field: {key}"
                )

        feature_id = feature["id"]

        if not isinstance(feature_id, str) or not feature_id.strip():
            raise ValueError("Every feature needs a non-empty string ID.")

        if feature_id in existing_ids or feature_id in new_ids:
            raise ValueError(f"Duplicate feature ID: {feature_id}")

        if not isinstance(feature["stage"], str) or not feature["stage"].strip():
            raise ValueError(f"{feature_id}: stage is required.")

        if not isinstance(feature["title"], str) or not feature["title"].strip():
            raise ValueError(f"{feature_id}: title is required.")

        if type(feature["ui"]) is not bool:
            raise ValueError(f"{feature_id}: ui must be true or false.")

        dependencies = feature["depends_on"]

        if not isinstance(dependencies, list):
            raise ValueError(f"{feature_id}: depends_on must be a list.")

        if not all(isinstance(dep, str) and dep for dep in dependencies):
            raise ValueError(f"{feature_id}: dependency IDs must be strings.")

        if len(dependencies) != len(set(dependencies)):
            raise ValueError(f"{feature_id}: duplicate dependencies found.")

        steps = feature["steps"]

        if not isinstance(steps, list) or not steps:
            raise ValueError(f"{feature_id}: at least one step is required.")

        if not all(isinstance(step, str) and step.strip() for step in steps):
            raise ValueError(f"{feature_id}: steps must be non-empty strings.")

        if feature["status"] != "todo":
            raise ValueError(f"{feature_id}: new features must start as todo.")

        if feature["passes"] is not False:
            raise ValueError(f"{feature_id}: passes must start as false.")

        if (
            "owner-writes" in feature
            and feature["owner-writes"] is not True
        ):
            raise ValueError(
                f"{feature_id}: omit owner-writes unless it is true."
            )

        new_ids.append(feature_id)

    all_ids = set(existing_ids + new_ids)

    for feature in additions:
        feature_id = feature["id"]

        for dependency in feature["depends_on"]:
            if dependency not in all_ids:
                raise ValueError(
                    f"{feature_id}: unknown dependency {dependency}."
                )

            if dependency == feature_id:
                raise ValueError(
                    f"{feature_id}: a feature cannot depend on itself."
                )

    # a cycle can only run through new features: an existing one cannot depend on a new one
    deps = {f["id"]: f["depends_on"] for f in additions}
    state = {}

    def visit(fid):
        if state.get(fid) == "open":
            raise ValueError(f"dependency cycle through {fid}.")
        if fid in deps and fid not in state:
            state[fid] = "open"
            for dep in deps[fid]:
                visit(dep)
            state[fid] = "done"

    for fid in deps:
        visit(fid)

    return True


def main():
    parser = argparse.ArgumentParser()
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--check", action="store_true")
    actions.add_argument("--apply", action="store_true")
    parser.add_argument("candidate")

    args = parser.parse_args()

    ROOT = Path.cwd().resolve()
    TARGET = ROOT / "feature_list.json"
    candidate = Path(args.candidate).resolve()

    if candidate.parent != ROOT or candidate.name != CANDIDATE_NAME:
        print("Candidate must be the designated project-root file.",
              file=sys.stderr)
        return 1

    if not candidate.is_file():
        print("Feature candidate file does not exist.", file=sys.stderr)
        return 1

    try:
        existing = read_json(TARGET) if TARGET.exists() else []
        additions = read_json(candidate)
        validate(existing, additions)
    except ValueError as error:
        print(f"Feature validation failed: {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(additions)} new feature(s):")

    for feature in additions:
        print(
            f"{feature['id']}: {feature['title']} "
            f"(depends on: {', '.join(feature['depends_on']) or 'none'})"
        )

    if args.check:
        print("Check complete. No changes were made.")
        return 0

    updated = existing + additions
    temporary = TARGET.with_name("feature_list.json.tmp")

    try:
        temporary.write_text(
            json.dumps(updated, indent=2) + "\n",
            encoding="utf-8"
        )
        os.replace(temporary, TARGET)
    except OSError as error:
        temporary.unlink(missing_ok=True)
        print(f"Could not write feature list: {error}", file=sys.stderr)
        return 1

    print(f"Applied {len(additions)} feature(s) successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())