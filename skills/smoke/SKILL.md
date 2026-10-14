---
description: End-to-end check of the plugin (factory). Builds a fixed two-feature mini-spec with build.py in a temporary git worktree on a throwaway branch and reports pass or fail for the guard, job folder, merge, resume, permission_denials, a Playwright screenshot read by a subagent, builder resume and resolver memory. Run it when the plugin changes (D75).
disable-model-invocation: true
---

Run the plugin smoke test. Report PASS, FAIL or NOT EXERCISED per check.
Change nothing in the owner's working tree.

## Setup

1. Read .claude/harness.json. If missing, stop: run `/harness:setup`.
   Note `plugin_root` (PLUGIN_ROOT) and `acceptance_dir` (default
   `tests/acceptance`). Scripts run as
   `python <PLUGIN_ROOT>/scripts/<name>.py`. The mini-spec files are in
   `<PLUGIN_ROOT>/skills/smoke/`.
2. Make the worktree, outside the project, on a throwaway branch (D54):
   `git worktree add -b smoke-<YYYYMMDDHHMM> <tmp>/harness-smoke HEAD`
   (`<tmp>` is the system temp folder). Trust is shared with this
   checkout (D48), so the project's real settings apply. Do all work
   below inside the worktree.
3. In the worktree, copy `spec.md` to `docs/spec.md` and
   `feature_list.json` to the root (replacing the project's own, which
   is fine: this is a throwaway branch), create `progress.md` if absent,
   add `build-log.jsonl` and `.harness/wt/` to .gitignore, then
   `git add -A` and `git commit -m "smoke: mini-spec"`.
4. The run command (SMOKE_CMD). It is small so it is cheap; the session
   limit is `--max-turns 80` (D69). Do not use /goal.
   `python <PLUGIN_ROOT>/scripts/build.py --session-cmd claude -p --agent harness:organiser "Run the next jobs" --permission-mode auto --permission-prompts none --output-format stream-json --verbose --max-turns 80`

## Run

1. Start SMOKE_CMD in the background in the worktree. Wait until
   `git log` or feature_list.json shows progress, or 5 minutes pass,
   then kill it (the whole process tree). This is the killed run.
2. Record feature_list.json and `git log`. Run SMOKE_CMD again (fresh
   session, never `--continue`) and wait for it to end. Its last line is
   the D69 status line: `feature_list: N/M done, K needs-human`.

## Checks

1. Guard, feature list (D17): in the worktree, pipe a PreToolUse payload
   that deletes F2 from feature_list.json into the guard, with
   CLAUDE_PROJECT_DIR set to the worktree:
   `echo '{"tool_name":"Write","tool_input":{"file_path":"feature_list.json","content":"[]"}}' | python <PLUGIN_ROOT>/scripts/guard.py`
   PASS if it exits 2 (blocked) and the file is unchanged.
2. Guard, acceptance tests (D60): pipe
   `{"tool_name":"Write","agent_type":"harness:builder","cwd":"<worktree>","tool_input":{"file_path":"<acceptance_dir>/F1/x.py","content":"x"}}`
   into the guard. PASS if it exits 2 and nothing was written.
3. Job folder: PASS if `.harness/jobs/F1/` has `brief.md`,
   `acceptance.sha`, `gates-1.md` and `round-1/review-code.md`, and that
   review's first line starts `VERDICT:`.
4. Done and merged: PASS if the status line says `2/2 done` (both
   features `done` in feature_list.json) and `git branch --merged`
   lists `factory/F1`.
5. Killed run resumes (D26): PASS if the second run continued from the
   files: no feature that was `done` before is redone (compare
   `git log` and feature_list.json) and it ended with the status line.
6. Denials (D49): `python <PLUGIN_ROOT>/scripts/check_log.py build-log.jsonl`
   in the worktree. PASS if it prints nothing and exits 0; otherwise
   FAIL and show what it printed.
7. Playwright (D75): if `npx playwright --version` fails in the
   worktree, report NOT EXERCISED: "Playwright not installed". Otherwise
   run, in the worktree:
   `claude -p "Use the Agent tool (general-purpose subagent) to run: npx playwright screenshot --browser chromium about:blank smoke.png, then Read smoke.png and describe it in one line. Report what the subagent said." --permission-mode auto --permission-prompts none --max-turns 10`
   PASS if smoke.png exists and the answer describes the image (for
   example a blank page); FAIL if the subagent could not read it.
8. Builder resume (D75): read the job folders' `progress` and
   `decision.md` files. PASS if a builder was resumed with SendMessage
   (a round 2 or a decision) and its new commits are on `factory/<id>`,
   made from `.harness/wt/<id>`. If no rework happened, report NOT
   EXERCISED: "no rework".
9. Resolver memory (D30): PASS if `.claude/agent-memory/resolver/` in
   the worktree has a file. If the resolver was never called, report
   NOT EXERCISED.

## Cleanup

Always, even after a failure: from the owner's checkout run
`git worktree remove --force <tmp>/harness-smoke` and
`git branch -D smoke-<YYYYMMDDHHMM>`. The `.harness/wt/<id>` worktrees
are inside the smoke worktree and go with it; delete any `factory/F1`
and `factory/F2` branches too. Confirm with `git worktree list`.

## Report

One line per check, numbered 1-9 as above. Overall PASS only if checks
1-6 pass.
