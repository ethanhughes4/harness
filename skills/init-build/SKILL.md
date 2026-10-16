---
description: Turns docs/spec.md into feature_list.json (every feature failing, with acceptance steps and dependencies), starts progress.md, writes build.cmd and makes the first commit. Use after /harness:questions, before the headless build.
argument-hint: "[stage-name]"
disable-model-invocation: true
---

Prepare the build for: $ARGUMENTS

You turn the agreed spec into a feature list the build loop can run. You
write no code.

## Before writing

1. Read .claude/harness.json. If it is missing, stop and tell the owner
   to run `/harness:setup` first. Note `plugin_root` from it; any plugin
   script you name is run as `python <plugin_root>/scripts/<name>.py`.
   In any file you write, give plugin paths exactly as `plugin_root`
   gives them.
2. Read docs/spec.md, docs/decisions.md, docs/brief.md and docs/owner.md.
   Use the `## <stage>` heading in docs/spec.md for $ARGUMENTS; if no
   stage is given and there is only one, use it. If the stage is
   missing or unclear, stop and ask.
3. Read feature_list.json if it exists. A new stage appends to it; never
   change or remove an existing feature.

## Features

Each feature is one object in a JSON list:

```json
{
  "id": "F1",
  "stage": "<stage>",
  "title": "<one line, what the user can do>",
  "ui": false,
  "depends_on": [],
  "steps": ["<acceptance step>", "..."],
  "status": "todo",
  "passes": false
}
```

- `id`: unique across the whole file. Continue from the highest number.
- `ui`: true if the owner would see it on a screen.
- `depends_on`: ids that must pass first. Only real dependencies; no
  cycles; no unknown ids.
- `steps`: concrete, checkable acceptance steps a builder can write a
  test for, using the examples in the spec. Where the spec has a
  decision rule or an eval, name it and its D-number in the step.
- `status`: always `"todo"` (D68). Only `status.py` changes it later.
- `passes`: always false.
- Add `"owner-writes": true` only if the brief or spec asks for the
  owner to write that part (D32). Otherwise leave the key out.
- Size: a builder finishes one in one sitting. Split larger ones.
- Cover every requirement, example, error behaviour and boundary in the
  spec. When done, list each spec requirement against the feature that
  holds it; if one has none, add a feature.

## Writing the list: propose, validate, approve, apply, verify

A hook blocks Write, Edit and any Bash command on `feature_list.json`,
so you never touch it directly. You add features through
`init_features.py`, which works only from this interactive session (a
subagent, including the builder and the organiser, is refused by the
hook). It handles a new list and an append to an existing one the same
way, and it never changes an existing feature.

1. Propose. Write ONLY the new features, as a JSON list in the exact
   shape above, to `init-features-candidate.tmp` at the project root
   (with Write; that name and place are the only ones accepted). Do not
   copy the existing features into it. Every new feature has
   `"status": "todo"` and `"passes": false`; ids must not exist yet.
   A feature may depend on an existing feature or on another one in the
   same file.
2. Validate. Run
   `python "<plugin_root>/scripts/init_features.py" --check init-features-candidate.tmp`
   It changes nothing. On "Feature validation failed: ..." fix the
   candidate file (not the list) and run it again until it prints
   "Check complete. No changes were made." It rejects bad JSON, a
   missing field, a duplicate or already used id, an unknown or self
   dependency, a dependency cycle, and any status other than `todo` or
   `passes` other than false.
3. Approve. Show the owner each id, title and `depends_on` from the
   check output, and ask: "Is anything missing or wrong?" Change only
   what they dispute, in the candidate file, and run step 2 again. Run
   from `new` there is no separate stop: show the summary and go on.
   Do not apply before the owner has approved.
4. Apply. Run the same command with `--apply` in place of `--check`.
   It validates again and replaces `feature_list.json` in one step, so
   a failure leaves the old list intact.
5. Verify. Read `feature_list.json` with Read: every proposed id is
   there, in order, after the old ones, with status `todo`. Then delete
   `init-features-candidate.tmp` (it is git-ignored).

## Other files

1. `progress.md`: create it if missing. Append, at the end, an entry:
   `## <YYYY-MM-DD HH:MM> init-build: <stage>`, then plain lines: the
   number of features added and any that are owner-writes.
2. `build.cmd`: a single line, exactly this, with `<plugin_root>`
   replaced by the real value from harness.json (D69):
   ```
   python "<plugin_root>/scripts/build.py"
   ```
   build.py starts a fresh organiser session per round, appends to
   build-log.jsonl, and stops by itself; a rerun resumes from the files.
   If build.cmd exists and differs, show the owner the difference and
   keep it unless they say to replace it.
3. Add `build-log.jsonl`, `.harness/wt/` and `init-features-candidate.tmp`
   to .gitignore.

## Finishing

1. Check the list as step 5 says: every `depends_on` id exists, every
   `passes` is false and every `status` is `todo` (init_features.py
   already enforced this; the read is your check that it was applied).
2. Make sure the owner approved the features (step 3).
3. Then run `git add -A` and `git commit -m "Init build: <stage>"`. Do
   not push.
4. Tell the owner: run build.cmd to start the build.

If you cannot run `init_features.py`, stop and tell the owner why; do
not write the list by another route.
