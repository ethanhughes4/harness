---
description: End-to-end check of the plugin (factory). Builds a fixed two-feature mini-spec with build.py in a throwaway git worktree and reports pass or fail for the guard, job folder, merge, resume, permission denials, a Playwright screenshot read by a subagent, builder resume and resolver memory. Run it when the plugin changes (D75).
disable-model-invocation: true
---

Run the plugin smoke test. Report PASS, FAIL or NOT EXERCISED per check.
Change nothing in the owner's working tree.

The plugin's absolute folder is: ${CLAUDE_PLUGIN_ROOT}

Call that value PLUGIN_ROOT, with forward slashes. If it is empty or
still starts with a dollar sign, stop and tell the owner. Scripts run as
`python <PLUGIN_ROOT>/scripts/<name>.py`; the mini-spec files are in
`<PLUGIN_ROOT>/skills/smoke/`.

## Setup

The smoke project is an empty-history worktree of the repo you are in,
so it shares this checkout's workspace trust (D48) and needs no setup of
its own project. Run everything below from the repo root unless it says
"in W".

1. W is `<system temp folder>/harness-smoke`, B is `smoke-<YYYYMMDDHHMM>`.
   If W exists from an earlier run, do the Cleanup first.
   `git worktree add --orphan -b B W`
2. In W, write:
   - `.claude/harness.json`:
     `{"test": [["python","-m","pytest","-q"]], "test_limit_s": 300, "max_builders": 2, "protected": [], "plugin_root": "<PLUGIN_ROOT>", "gates": [], "acceptance_dir": "tests/acceptance", "walkthrough_every": 5}`
   - `.claude/settings.json`: `permissions.allow` with `Bash(git status*)`,
     `Bash(git diff*)`, `Bash(git log*)`, `Bash(git add *)`,
     `Bash(git commit *)`, `Bash(git merge *)`, `Bash(git worktree *)`,
     `Bash(git branch *)`, `Bash(git checkout *)`, `Bash(git rev-parse *)`,
     `Bash(git reset *)`, `Bash(python -m pytest*)`,
     `Bash(python <PLUGIN_ROOT>/scripts/*)`; `permissions.deny` with
     `Bash(git push*)`; `env` with `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH: "2"`.
   - `CLAUDE.md`: three lines: what the project is, the test command,
     and that feature_list.json changes only through the harness scripts.
   - `tests/test_skeleton.py` with one passing test; `progress.md`
     with `# Progress`; `.gitignore` with `build-log.jsonl`,
     `.harness/wt/`, `__pycache__/`, `.pytest_cache/`.
   - Copy `spec.md` to `docs/spec.md` and `feature_list.json` to the root.
   Then in W: `python -m pytest -q` must pass; `git add -A`;
   `git commit -m "smoke: mini-spec project"`. Note the commit as START.
3. SMOKE_CMD, run in W. If `claude plugin list` does not show harness
   installed, add `--plugin-dir <PLUGIN_ROOT>` after the prompt. Keep the
   whole output out of W (write it to the system temp folder).
   `python <PLUGIN_ROOT>/scripts/build.py --session-cmd claude -p --agent harness:organiser "Run the next jobs" --permission-mode auto --permission-prompts none --output-format stream-json --verbose --max-turns 80`

## Run

1. Killed run: start SMOKE_CMD in the background. Wait until
   `git branch --list "factory/*"` shows a branch or 10 minutes pass, then
   kill the whole process tree (on Windows: `taskkill /PID <build.py pid> /T /F`).
   Record `git log --oneline --all` and the statuses in feature_list.json
   (read it with Read).
2. Resume: run SMOKE_CMD again (a fresh session, never `--continue`) and
   wait for it to end. Its last line is the D69 status line:
   `feature_list: N/M done, K needs-human`.

## Checks

1. Guard, feature list (D17): in W, pipe
   `{"tool_name":"Write","cwd":"<W>","tool_input":{"file_path":"<W>/feature_list.json","content":"[]"}}`
   into `python <PLUGIN_ROOT>/scripts/guard.py`. PASS if it exits 2 and the
   file is unchanged.
2. Guard, acceptance tests (D60): pipe
   `{"tool_name":"Write","agent_type":"harness:builder","agent_id":"x","cwd":"<W>","tool_input":{"file_path":"<W>/tests/acceptance/F1/x.py","content":"x"}}`
   into the guard. PASS if it exits 2 and nothing was written.
3. Job folders: PASS if each of `.harness/jobs/F1/` and `.harness/jobs/F2/`
   in W has `brief.md`, `acceptance.sha`, `gates-1.md`, `decision.md` and
   `round-1/review-code.md` whose first line starts `VERDICT:`.
4. Done and merged: PASS if the status line says `2/2 done`, and in W
   `git branch --merged` lists `factory/F1` and `factory/F2`, and
   `python -m pytest -q` passes.
5. Resume (D26): PASS if the resume run continued from the files: work
   committed before the kill (for example the acceptance tests) was not
   redone, and the run ended with the status line.
6. Denials (D49): in W, `python <PLUGIN_ROOT>/scripts/check_log.py build-log.jsonl`.
   PASS if it prints nothing. A guard block also shows here (an agent
   tried a Bash command its prompt tells it not to use), so for each
   line say which agent and command it was.
7. Playwright (D75): in W run
   `claude -p "Use the Agent tool (general-purpose subagent) to run: npx --no-install playwright screenshot --browser chromium \"data:text/html,<h1 style='color:red'>SMOKE 42</h1>\" smoke.png, then Read smoke.png and describe in one line the text and colour it shows. Report what the subagent said." --permission-mode auto --permission-prompts none --max-turns 10`
   PASS if the answer says red text "SMOKE 42". NOT EXERCISED if
   Playwright or its Chromium browser is not installed (say which).
8. Builder resume (D75): PASS if a job's `decision.md` shows a round 2
   from the resumed builder, with its commits on `factory/<id>`. NOT
   EXERCISED if no rework happened.
9. Resolver memory (D30): PASS if `.claude/agent-memory/resolver/` in W
   has a file; NOT EXERCISED if the resolver was never called.

Also report the cost: the sum of `total_cost_usd` over the `result`
lines of `build-log.jsonl`.

## Cleanup

Always, even after a failure, from the repo root:
1. Remove each job worktree first: for every
   `<W>/.harness/wt/<id>` in `git worktree list`,
   `git worktree remove --force <path>`.
2. `git worktree remove --force <W>`, then `git branch -D B` and every
   `factory/*` branch the run made. `git worktree prune`.
3. Confirm with `git worktree list` that only your own worktrees remain.

## Report

One line per check, numbered 1-9, then the cost. Overall PASS only if
checks 1-6 pass.
