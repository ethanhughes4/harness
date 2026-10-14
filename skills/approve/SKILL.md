---
description: Approves a needs-human job. Shows the owner the decision and latest reviews, merges factory/<id> into the main branch, runs the tests, and marks the feature done. Use as /harness:approve <id>. Never pushes.
disable-model-invocation: true
---

Approve job `<id>` (the argument). Run from the project root.

Never name feature_list.json in a Bash command; the guard blocks it. The
only exception is the exact call `python <plugin_root>/scripts/status.py <id> <status>`.
Read `feature_list.json` with Read. Never push. Start no subagent.

Paths: branch `factory/<id>`, worktree `.harness/wt/<id>`, job folder
`.harness/jobs/<id>/`. Read `.claude/harness.json` for `test` (a list of
commands, each a list of arguments) and `plugin_root`.

## Check

1. Read `feature_list.json` with Read. The feature `<id>` must have
   status `needs-human`. If not, say its status and stop.
2. `git status` must be clean and you must be on the main branch. If
   not, tell the owner and stop.

## Show

Read `.harness/jobs/<id>/decision.md` and the latest
`.harness/jobs/<id>/round-<n>/review-*.md` files (highest `<n>`) and the
latest `gates-<n>.md`. Give the owner one short summary: why it is
needs-human, risk and files, each reviewer's verdict and main points.

## Merge

1. Note the current commit: `git rev-parse HEAD`.
2. `git merge --no-ff factory/<id>`. On a conflict:
   `git merge --abort`, tell the owner, stop. Status stays.
3. Run every `test` command, one at a time.
   - Red: `git reset --hard <the noted commit>`. Tell the owner which
     command failed and why. Status stays needs-human. Stop.
   - Green: continue.
4. `python <plugin_root>/scripts/status.py <id> done`.
5. Append `APPROVED by owner <YYYY-MM-DD>` to
   `.harness/jobs/<id>/decision.md` (printf or a heredoc with >>).
6. `git add -A` and `git commit -m "Approve <id>"`.
7. `git worktree remove .harness/wt/<id>`. Keep the branch.

Tell the owner it is merged and done, and that nothing was pushed.
