---
description: Sets up a project for the harness. Writes CLAUDE.md, .claude/settings.json, rule files and .claude/harness.json, plus a skeleton and one passing test, after the owner reviews them. Use once per project, before building.
argument-hint: "[stack, e.g. python, node]"
disable-model-invocation: true
---

Set up this project for the harness. Stack, if given: $ARGUMENTS

The plugin's absolute folder is: ${CLAUDE_PLUGIN_ROOT}

Call that value PLUGIN_ROOT. Claude Code fills it in before you read
this text. If the value above is empty or still starts with a dollar
sign, stop and tell the owner; do not guess a path. Write
PLUGIN_ROOT with forward slashes, even on Windows.

Run on its own, write nothing until the owner approves. Run from
`/harness:new`, there is no separate approval stop: write the files,
then show the one-screen summary (see Finishing).

## Before writing

1. Read docs/brief.md, docs/owner.md, docs/spec.md and docs/decisions.md
   if they exist, and any code, package files or tests already here.
2. Work out the stack from those files, or from $ARGUMENTS. If it is
   still unclear, ask the owner in ONE numbered list, each question
   with your recommended answer and one sentence on why.
3. Decide the project's test commands. Each is an argument list, e.g.
   `["python","-m","pytest","-q"]`. They must run with no prompts and
   exit non-zero on failure.
4. Find which of these tools are actually installed (run `<tool>
   --version`): ruff, eslint, tsc, gitleaks, semgrep, pip-audit,
   `npm audit`. Only those go into `gates`; note the missing ones.
5. Run on its own: show every file you plan to write and ask "Is
   anything missing or wrong?". Existing files: show the change, never
   overwrite silently.

## What to write

1. `.claude/harness.json`, exactly these keys:
   ```json
   {
     "test": [["python", "-m", "pytest", "-q"]],
     "test_limit_s": 300,
     "run": {"cmd": ["<start command>"], "url": "<local url>"},
     "gates": [["ruff", "check", "."]],
     "risky": ["*auth*", "*payment*", "*crypto*", "*secret*", "*migration*",
               ".github/*", ".gitlab-ci.yml", "*package.json",
               "*package-lock.json", "*requirements*.txt", "*pyproject.toml",
               "*poetry.lock", "*cargo.toml", "*cargo.lock", "*go.mod",
               "*go.sum", ".claude/*"],
     "acceptance_dir": "tests/acceptance",
     "walkthrough_every": 5,
     "max_builders": 2,
     "protected": [],
     "plugin_root": "<PLUGIN_ROOT>"
   }
   ```
   - `run`: for an app, the command that starts it and the URL it
     serves; leave the key out for a library or script.
   - `gates`: argument lists, only for tools found installed in step 4
     (lint, types, secret scan, dependency audit); `[]` if none.
   - `risky`: the defaults above (D63); add project-specific globs.
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
         "Bash(python <PLUGIN_ROOT>/scripts/mark_pass.py *)",
         "Bash(python <PLUGIN_ROOT>/scripts/status.py *)",
         "Bash(python <PLUGIN_ROOT>/skills/ui-ux-pro-max/scripts/search.py *)",
         "Bash(python <PLUGIN_ROOT>/scripts/gates.py *)",
         "Bash(python <PLUGIN_ROOT>/scripts/risk.py *)",
         "Bash(python <PLUGIN_ROOT>/scripts/design_audit.py *)",
         "Bash(python <PLUGIN_ROOT>/scripts/reference_capture.py *)",
         "Bash(python <PLUGIN_ROOT>/scripts/build.py*)",
         "Bash(python <PLUGIN_ROOT>/scripts/merge.py *)",
         "Bash(python <PLUGIN_ROOT>/scripts/init_features.py *)"
       ],
       "deny": ["Bash(git push*)"]
     },
     "env": {
       "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "2",
       "CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL": "1h"
     },
     "worktree": { "baseRef": "head" }
   }
   ```
   - Add one `Bash(...)` rule for each test command, and for the
     project's formatter or build command if it has one.
   - `deny` for `Bash(git push*)` is required (D78): auto mode would
     push. Never add a push allow rule, and do not add `defaultMode`.
   - `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL` "1h" keeps the subagent
     prompt cache for an hour (documented at
     https://code.claude.com/docs/en/env-vars; needs Claude Code
     v2.1.242 or later; 1-hour cache writes cost more).
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
   `python <PLUGIN_ROOT>/scripts/mark_pass.py <id>`, `status.py`, and
   (new features, interactive session only) `init_features.py`.

4. Rule files in `.claude/rules/`, one per topic the stack needs
   (e.g. testing, style). Short, concrete, no more than 30 lines each.
   Add `paths:` frontmatter when a rule applies only to some files.

5. A skeleton for the stack: the smallest folder layout and entry file
   that runs, and ONE passing test that exercises it. Do not build any
   feature.

6. UI projects only: Playwright (e.g. `npm i -D @playwright/test` and
   `npx playwright install chromium`). For a Python UI project offer
   `python -m pip install playwright` then
   `python -m playwright install chromium`; the design audit
   (`scripts/design_audit.py`, D97) needs them (D99). Install only
   after the owner says yes in the summary (D78); until then list it as
   "not installed".

## Finishing

1. Run each test command. If any fails, fix the skeleton or test, not
   the command, and run again.
2. Check .claude/harness.json parses and `plugin_root` is set.
3. Show a one-screen summary (about 20 lines): stack, test commands,
   gates found and missing, `run`, the push deny, and for a UI project
   "Install Playwright now? (yes/no)". Wait only for that answer. Run
   from `new`, this is the only stop and no other approval is asked.
4. Do not commit; `/harness:init-build` makes the first commit.
5. Tell the owner: the plugin's hooks are now live in this project,
   because `.claude/harness.json` exists (delete it to switch them
   off). Next step: `/harness:questions`, then `/harness:init-build`.
