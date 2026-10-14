---
description: End-to-end check of the harness. Builds a fixed two-feature mini-spec in a temporary git worktree on a throwaway branch and reports pass or fail for the guard, permission_denials, resume and resolver memory. Use after /harness:setup to prove the build loop works.
disable-model-invocation: true
---

Run the harness smoke test. Report PASS or FAIL per check. Change nothing
in the owner's working tree.

## Setup

1. Read .claude/harness.json. If missing, stop: run `/harness:setup`.
   Note `plugin_root` (PLUGIN_ROOT). Scripts run as
   `python <PLUGIN_ROOT>/scripts/<name>.py`. The mini-spec files are in
   `<PLUGIN_ROOT>/skills/smoke/`.
2. Read `build.cmd` (written by /harness:init-build). If missing, stop:
   run `/harness:init-build` first.
3. Make the worktree, outside the project, on a throwaway branch (D54):
   `git worktree add -b smoke-<YYYYMMDDHHMM> <tmp>/harness-smoke HEAD`
   (`<tmp>` is the system temp folder). Trust is shared with this
   checkout (D48), so the project's real settings apply. Do all work
   below inside the worktree.
4. In the worktree, copy `spec.md` to `docs/spec.md` and
   `feature_list.json` to the root (replacing the project's own, which
   is fine: this is a throwaway branch), create `progress.md` if absent,
   then `git add -A` and `git commit -m "smoke: mini-spec"`.

## Checks

1. Guard (D17): in the worktree, pipe a PreToolUse payload that deletes
   F2 from feature_list.json into the guard, with CLAUDE_PROJECT_DIR set
   to the worktree:
   `echo '{"tool_name":"Write","tool_input":{"file_path":"feature_list.json","content":"[]"}}' | python <PLUGIN_ROOT>/scripts/guard.py`
   PASS if it exits 2 (blocked) and the file is unchanged.
2. Killed run: take the command from build.cmd but replace
   `stop after 200 turns` with `stop after 6 turns` (small bound for
   the smoke run). Keep the `>> build-log.jsonl` redirect. Start it in
   the background in the worktree, wait until `git log` or
   feature_list.json shows progress or 3 minutes pass, then kill it.
3. Resume (D26): run the same command again (fresh session, never
   `--continue`). PASS if it continues from the files: no feature that
   was `passes: true` before is redone (compare `git log` and
   feature_list.json before and after) and the run ends with a result
   message.
4. Denials (D49): `python <PLUGIN_ROOT>/scripts/check_log.py build-log.jsonl`
   in the worktree. PASS if it prints nothing and exits 0; otherwise
   FAIL and show what it printed.
5. Resolver memory (D30): PASS if `.claude/agent-memory/resolver/` in
   the worktree has a file. If the resolver was never called in the
   short run, report NOT EXERCISED, not PASS.

## Cleanup

Always, even after a failure: from the owner's checkout run
`git worktree remove --force <tmp>/harness-smoke` and
`git branch -D smoke-<YYYYMMDDHHMM>`. Confirm with `git worktree list`.

Finish with one line per check and an overall PASS only if checks 1-4
pass.
