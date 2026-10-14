---
description: Sets up a project for the harness. Writes CLAUDE.md, .claude/settings.json, rule files and .claude/harness.json, plus a skeleton and one passing test, after the owner reviews them. Use once per project, before building.
argument-hint: "[stack, e.g. python, node]"
disable-model-invocation: true
---

Set up this project for the harness. Stack, if given: $ARGUMENTS

The plugin's absolute folder is: ${CLAUDE_PLUGIN_ROOT}

Call that value PLUGIN_ROOT. Claude Code fills it in before you read
this text. If you still see a literal `${CLAUDE_PLUGIN_ROOT}` above or
an empty value, stop and tell the owner; do not guess a path. Write
PLUGIN_ROOT with forward slashes, even on Windows.

Until the owner approves, write nothing.

## Before writing

1. Read docs/brief.md, docs/owner.md, docs/spec.md and docs/decisions.md
   if they exist, and any code, package files or tests already here.
2. Work out the stack from those files, or from $ARGUMENTS. If it is
   still unclear, ask the owner in ONE numbered list, each question
   with your recommended answer and one sentence on why.
3. Decide the project's test commands. Each is an argument list, e.g.
   `["python","-m","pytest","-q"]`. They must run with no prompts and
   exit non-zero on failure.
4. Show the owner every file you plan to write, in full, and ask:
   "Is anything missing or wrong?" Change only what they dispute.
   Existing files: show the change, never overwrite silently.

## What to write

1. `.claude/harness.json`, exactly these keys:
   ```json
   {
     "test": [["python", "-m", "pytest", "-q"]],
     "test_limit_s": 300,
     "max_builders": 3,
     "protected": [],
     "plugin_root": "<PLUGIN_ROOT>"
   }
   ```
   Use the real test commands. `protected` lists globs for data that
   must never change (e.g. `data/raw/**`); ask the owner for them, and
   use `[]` if there are none.

2. `.claude/settings.json`. Merge into the file if it exists; keep
   its other keys.
   ```json
   {
     "permissions": {
       "allow": [
         "Bash(git status*)",
         "Bash(git diff*)",
         "Bash(git log*)",
         "Bash(git add *)",
         "Bash(git commit *)",
         "Bash(git merge *)",
         "Bash(git worktree *)",
         "Bash(git branch *)",
         "Bash(git checkout *)",
         "Bash(<test command, one rule per command, ending in *>)",
         "Bash(python <PLUGIN_ROOT>/scripts/mark_pass.py *)"
       ]
     },
     "env": { "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "2" },
     "worktree": { "baseRef": "head" }
   }
   ```
   - Add one `Bash(...)` rule for each test command, and for the
     project's formatter or build command if it has one.
   - Do not add `git push`, and do not add `defaultMode`.
   - The `python <PLUGIN_ROOT>/scripts/mark_pass.py *` rule must match
     the command the organiser runs, so write PLUGIN_ROOT exactly as in
     harness.json.
   - `worktree.baseRef: head` makes each builder's worktree branch from
     the current HEAD, not the default branch.
   - Permission rules from a project file apply only after the owner
     trusts the folder. Tell them to open Claude Code here once and
     accept the trust prompt before the first headless build.

3. `CLAUDE.md`: under 60 lines. The project's purpose from the brief,
   the stack, how to run the tests, the layout, and the must-nevers from
   docs/brief.md. Say that `feature_list.json` is changed only by
   `python <PLUGIN_ROOT>/scripts/mark_pass.py <id>`.

4. Rule files in `.claude/rules/`, one per topic the stack needs
   (e.g. testing, style). Short, concrete, no more than 30 lines each.
   Add `paths:` frontmatter when a rule applies only to some files.

5. A skeleton for the stack: the smallest folder layout and entry file
   that runs, and ONE passing test that exercises it. Do not build any
   feature.

## Finishing

1. Run each test command. If any fails, fix the skeleton or test, not
   the command, and run again.
2. Check .claude/harness.json parses and `plugin_root` is set.
3. Do not commit; `/harness:init-build` makes the first commit.
4. Tell the owner: the plugin's hooks are now live in this project,
   because `.claude/harness.json` exists (delete it to switch them
   off). Next step: `/harness:questions`, then `/harness:init-build`.
