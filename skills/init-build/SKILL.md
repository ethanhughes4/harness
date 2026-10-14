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

Write the list with 2-space indentation.

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
3. Add `build-log.jsonl` and `.harness/wt/` to .gitignore.

## Finishing

1. Check feature_list.json parses, ids are unique, every `depends_on`
   id exists, every `passes` is false and every `status` is `todo`.
2. Show the owner the features (id, title, depends_on) and ask: "Is
   anything missing or wrong?" Change only what they dispute.
3. Then run `git add -A` and `git commit -m "Init build: <stage>"`.
   Do not push.
4. Tell the owner: run build.cmd to start the build.

If you cannot write files, print the feature_list.json you would write
instead.
