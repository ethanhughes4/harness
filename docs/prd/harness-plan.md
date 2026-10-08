# Harness: build plan for phases 1 and 2

Decisions: docs/prd/harness-decisions.md (D1 to D36).
Tests for this repo: `python -m pytest -q` at the repo root.

## Skeleton and the shared list

- The plugin lives at the repo root (D10): `.claude-plugin/plugin.json`,
  `skills/<name>/SKILL.md`, `agents/<name>.md`, `hooks/hooks.json`,
  `scripts/`, `tests/`, `evals/`.
- Skills and agents are found by folder, so a new one is a new file and
  needs no list.
- **The shared list is `hooks/hooks.json`.** Each hook step adds one
  entry for its event and nothing else. On a merge conflict there, keep
  every entry.
- `scripts/common.py` (step 1) holds the two things every hook needs:
  `config(cwd)` returns the parsed `.claude/harness.json` or `None`, and
  every hook script exits 0 at once when it is `None` (D14). Later steps
  import it and don't change it.
- `tests/test_layout.py` (step 1) checks every `skills/*/SKILL.md` and
  `agents/*.md` it finds, so each later skill or agent is checked
  without editing the test.

## Shared formats (every step uses these as written)

- `.claude/harness.json`: as in D15, keys `test`, `test_limit_s`,
  `max_builders`, `protected`, plus `plugin_root`: the plugin's
  absolute folder (D35).
- Script paths: agents and skills run plugin scripts as
  `python <plugin_root>/scripts/<name>.py`, reading `plugin_root` from
  `.claude/harness.json`. They never use `${CLAUDE_PLUGIN_ROOT}`;
  only `hooks/hooks.json` does (D35).
- `feature_list.json`: as in D25, a list of
  `{id, stage, title, ui, depends_on, steps, passes}`; an optional
  `"owner-writes": true` (D32).
- `docs/brief.md` headings: `## Problem`, `## User`, `## Must never`,
  `## Out of scope`.
- `progress.md`: entries appended at the end, each starting
  `## <YYYY-MM-DD HH:MM> <title>`, then plain lines.
- "Features in progress": `passes` false and every `depends_on` passing.

## Wave 1

### Step 1: The plugin loads and `/harness:questions` runs. Status: TODO
Depends on: none.

After it: `claude --plugin-dir .` loads the plugin; `/harness:questions
<stage>` asks every question in one list, each with a recommended
answer and a TECHNICAL or PREFERENCE tag, and writes `docs/spec.md` and
`docs/decisions.md` with a heading per stage; a run that dies on an API
error leaves an entry in `progress.md`; `python -m pytest -q` passes.

Creates:
- `.claude-plugin/plugin.json` (name `harness`) (D2, D10)
- `LICENSE` (MIT) (D12)
- `skills/questions/SKILL.md`: the repo's `.claude/skills/questions`
  made general: no FPL text, gender-neutral wording, one list, tags,
  recommended answers, D-numbered decisions and decision rules into
  `docs/decisions.md`, `disable-model-invocation: true` (D2, D25, D29,
  D32)
- `hooks/hooks.json` with one entry: `StopFailure` running
  `scripts/stop_failure.py` in exec form (D16, D19)
- `scripts/common.py`: `config(cwd)` and the D14 gate (D14, D15, D16)
- `scripts/stop_failure.py`: appends the error type and details to
  `progress.md` (D19)
- `tests/test_layout.py`: plugin.json parses with name `harness`;
  every SKILL.md and agent file has frontmatter with `name` or
  `description`; no agent file uses `hooks`, `permissionMode` or
  `mcpServers` (D1); every skill except `architecture` has
  `disable-model-invocation: true` (D4)
- `tests/test_stop_failure.py`: no `harness.json` means exit 0 and no
  file written; with it, an entry is appended; stdlib only (D14, D19)

Changes (the repo's own build tooling, D10, D11; `run_tests.py` was
already fixed before the build, D34):
- `.claude/settings.json`: FPL permissions and domains removed
- `.claude/agents/*.md`: FPL text removed (stack, web/, npm), wording
  gender-neutral
- `.claude/skills/questions/SKILL.md`: "himself" wording made neutral
- Deletes `.claude/skills/prd/` and `.claude/rules/web.md`
- Commits the staged rename of the design doc to `docs/design.md` (D9)

Not in this step: creating the private GitHub repo and pushing (D12).
The owner does that; agents never push.

## Wave 2

### Step 2: Tests block a finish. Status: TODO
Depends on: 1.

After it: in a project with `harness.json`, Claude and each
`harness:builder` can't finish while the project's test commands fail;
a slow run prints a warning.

Creates:
- `scripts/run_tests.py`: runs each command in `test`, kills a run past
  `test_limit_s`, warns past 80% of it, exit 2 with the failing tail on
  failure (D15, D16)
- `tests/test_run_tests.py`: passing command, failing command (exit
  2), timeout, 80% warning, no `harness.json` (exit 0) (D14, D15)

Changes: `hooks/hooks.json`: add `Stop` and `SubagentStop` (matcher
`^harness:builder$`), both with timeout 600 (D1, D15).

Note for the organiser prompt (step 14): Stop blocks cap at 8 in a row
(D6), so the loop runs the tests itself and never relies on the hook
looping.

### Step 3: The feature list can't be edited, only marked. Status: TODO
Depends on: 1.

After it: any Edit, Write or Bash command that touches
`feature_list.json` or a `protected` path is blocked with a reason;
`python scripts/mark_pass.py <id>` sets that feature's `passes` to true
and changes nothing else.

Creates:
- `scripts/guard.py`: PreToolUse check for Edit, Write and Bash; Bash is
  blocked when its command names `feature_list.json` or matches a
  `protected` glob, unless it is a call to `mark_pass.py` (D16, D17)
- `scripts/mark_pass.py`: flips one `passes`, refuses an unknown id,
  keeps every other byte of each feature (D17, D25)
- `tests/test_guard.py`: Edit/Write/Bash on the list blocked, on a
  protected path blocked, on another file allowed, mark_pass allowed,
  no `harness.json` allowed (D14, D17)
- `tests/test_mark_pass.py`: flips one, unknown id fails, others
  unchanged (D17, D25)

Changes: `hooks/hooks.json`: add `PreToolUse` with matcher
`Edit|Write|Bash`.

### Step 4: Key context comes back after compaction. Status: TODO
Depends on: 1.

After it: after `/compact` in a set-up project, Claude is told the
must-nevers, the features in progress, where `docs/owner.md` and
`docs/decisions.md` are, and the last 20 lines of `progress.md`.

Creates:
- `scripts/reinject.py`: builds that text, cut to under 2 KB, skips
  any file that is missing (D18)
- `tests/test_reinject.py`: content, the 2 KB cap, missing files, no
  `harness.json` (D14, D18)

Changes: `hooks/hooks.json`: add `SessionStart` with matcher `compact`.

### Step 5: The builder agent. Status: TODO
Depends on: 1.

After it: `harness:builder` builds one feature from `feature_list.json`
in its own worktree, tests first, and reports DONE,
DONE_WITH_CONCERNS, BLOCKED or NEEDS_CONTEXT.

Creates: `agents/builder.md`, from `.claude/agents/builder.md` made
general: no `hooks` field (the test hook is step 2's SubagentStop),
`isolation: worktree`, tools add `Agent` so it can ask the resolver;
its instructions say it may start only `harness:resolver`, since an
`Agent(...)` list is ignored inside a subagent; skips features marked
`owner-writes`; never edits `feature_list.json` (D1, D2, D22, D32,
D36).

Tests: covered by `tests/test_layout.py`.

### Step 6: The reviewer agent. Status: TODO
Depends on: 1.

After it: `harness:reviewer` checks a merged diff against
`docs/spec.md` and `docs/decisions.md` first, then quality, read-only,
and can run `/code-review` on the diff.

Creates: `agents/reviewer.md`, from `.claude/agents/reviewer.md`, made
general to features and the spec instead of plan steps (D2, D21 step
4, D33 `/code-review`).

Tests: covered by `tests/test_layout.py`.

### Step 7: The resolver agent. Status: TODO
Depends on: 1.

After it: `harness:resolver` answers a question from the spec,
`docs/owner.md`, the decision rules, then quoted sources; anything
still open comes back as the recommended answer marked PROVISIONAL.

Creates:
- `agents/resolver.md`, from `.claude/agents/resolver.md`, with
  `memory: project`, the order above, and PROVISIONAL instead of
  stopping (D2, D22, D30)
- `evals/resolver/`: one `claude plugin eval` case, no Bash granted:
  a preference question answered from a planted `owner.md` without
  escalating (D8, D27)

## Wave 3

### Step 8: `/harness:brief`. Status: TODO
Depends on: 1.

After it: `/harness:brief` interviews the owner and writes
`docs/brief.md` with the four headings above.

Creates: `skills/brief/SKILL.md` (D2, D32 wording).
Tests: covered by `tests/test_layout.py`.

### Step 9: `/harness:owner`. Status: TODO
Depends on: 1.

After it: `/harness:owner` creates or updates
`~/.claude/harness/owner.md` and copies it to `docs/owner.md`; a new
master holds the standing answer "Claude writes all code; I read and
edit".

Creates: `skills/owner/SKILL.md` (D2, D31, D32).
Tests: covered by `tests/test_layout.py`.

### Step 10: `/harness:setup`. Status: TODO
Depends on: 2, 3.

After it: `/harness:setup` writes, for the project's stack and with the
owner's review: `CLAUDE.md`, `.claude/settings.json` (permissions,
`env` with `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH: 2`,
`worktree.baseRef: head`), rule files, `.claude/harness.json` with
`plugin_root` set to the plugin's absolute folder, a skeleton and one
passing test. Afterwards the plugin's hooks are live in that project.

Creates: `skills/setup/SKILL.md` (D2, D3, D14, D15, D35).
Tests: covered by `tests/test_layout.py`; proved end to end by step 15.

### Step 11: The critic checks technical answers. Status: TODO
Depends on: 1.

After it: in `/harness:questions`, `harness:critic` checks every
TECHNICAL answer first (AGREE, or CHANGE with a quote and link); the
owner sees only the PREFERENCE questions and the critic's changes.

Creates:
- `agents/critic.md`: model opus; tools Read, Grep, Glob, WebSearch,
  WebFetch (D2, D29)
- `evals/questions/`: one eval case, no Bash granted: preference
  questions tagged correctly, and the critic catches a planted
  technical mistake (D8, D27)

Changes: `skills/questions/SKILL.md`: the critic pass (D29).

### Step 12: `/harness:init-build`. Status: TODO
Depends on: 1, 3.

After it: `/harness:init-build` turns `docs/spec.md` into
`feature_list.json` (all `passes` false, acceptance steps,
`depends_on`; a new stage appends), starts `progress.md`, writes
`build.cmd` and makes the first commit.

Creates:
- `skills/init-build/SKILL.md`. `build.cmd` holds exactly the D20
  command, appends to `build-log.jsonl`, and never uses `--continue`;
  any script it names is found through `plugin_root` (D2, D7, D20,
  D25, D26, D35)
- `evals/init-build/`: one eval case, no Bash granted: a short spec
  becomes features with acceptance steps and no missing requirement
  (D8, D27)

## Wave 4

### Step 13: The architecture skill. Status: TODO
Depends on: 6, 11.

After it: `/harness:questions` also writes `docs/architecture.md`
(requirements, non-functional needs, chosen pattern with trade-offs, a
diagram, risks), with its trade-offs as D-numbered decisions; the
reviewer flags code that breaks it.

Creates: `skills/architecture/SKILL.md`, our own text, model-invocable
(no `disable-model-invocation`), with the MIT notice if any
architecture-designer text is reused (D4, D13, D33).
Changes: `skills/questions/SKILL.md` (uses it), `agents/reviewer.md`
(`skills: [architecture]`, reads `docs/architecture.md`).
Tests: `tests/test_layout.py` already allows the one model-invocable
skill.

### Step 14: The organiser loop. Status: TODO
Depends on: 2, 3, 5, 6, 7, 12.

After it: `build.cmd` in a set-up project runs `harness:organiser` as
the main session; each /goal turn runs the six D21 steps and ends by
printing `feature_list: N/M passing, suites green|red`.

Creates: `agents/organiser.md`, from `.claude/agents/organiser.md`
rewritten for the loop:
- picks failing features whose `depends_on` all pass, at most
  `max_builders`, skipping `owner-writes` (D21, D32)
- runs the tests itself after each merge, not relying on Stop-hook
  loops (D6, D21)
- reviewer, then any eval in the acceptance steps with its decision
  rule, then `python <plugin_root>/scripts/mark_pass.py <id>` and a
  commit, then a `progress.md` entry (D17, D21, D35)
- the resolver on any question; open ones recorded PROVISIONAL in
  `docs/decisions.md`; never stops for one (D22)
- one retry for a BLOCKED builder with the resolver's answer, then
  skip and log; dependants wait (D24)
- the status line last, since the judge sees only the conversation
  (D5, D23)
- starts only `harness:builder`, `harness:reviewer`,
  `harness:resolver` (D2, D20)

Tests: covered by `tests/test_layout.py`; proved end to end by step 15.

## Wave 5

### Step 15: `/harness:smoke`. Status: TODO
Depends on: 7, 10, 12, 14.

After it: `/harness:smoke` clones the project to a temp folder, loads a
fixed two-feature mini-spec, runs the headless build, and reports
pass or fail for each check: the guard blocks a deleted feature,
`permission_denials` in the stream output is empty, a killed run
resumes on rerun, and `.claude/agent-memory/resolver/` was written.
The clone is deleted afterwards.

Creates:
- `skills/smoke/SKILL.md` and its mini-spec files beside it; it runs
  `check_log.py` through `plugin_root` (D7, D26, D28, D30, D35)
- `scripts/check_log.py`: reads a `build-log.jsonl` and prints every
  non-empty `permission_denials` (D7, D28)
- `tests/test_check_log.py`: a clean log, a log with a denial, a
  broken line

### Step 16: `/harness:report`. Status: TODO
Depends on: 12, 14.

After it: `/harness:report` summarises `feature_list.json` progress,
every PROVISIONAL decision with its options, eval results and
failures from `progress.md`.

Creates: `skills/report/SKILL.md` (D2, D22).
Tests: covered by `tests/test_layout.py`.

## Coverage

D1 s1,2,5 · D2 all agent and skill steps · D3 s10 · D4 s1,13 · D5 s14
· D6 s2,14 · D7 s12,15 · D8 s7,11,12 · D9 s1 · D10 s1 · D11 s1 · D12 s1
(push by owner) · D13 s13 · D14 s1–4,10 · D15 s1,2,10 · D16 s1–4 · D17
s3,14 · D18 s4 · D19 s1 · D20 s12,14 · D21 s6,14 · D22 s5,7,14,16 · D23
s14 · D24 s14 · D25 s1,3,12 · D26 s12,15 · D27 s1–4,7,11,12 · D28 s15 ·
D29 s1,11 · D30 s7,15 · D31 s9 · D32 s1,5,8,9,14 · D33 s6,13 (part)
· D34 done before the build (f747e5c) · D35 s10,12,14,15 · D36 s5

## UNCOVERED

- D33, the phase 4 parts: vetting and copying frontend-design and
  ui-ux-pro-max, and disabling the user-installed ui-ux-pro-max plugin.
  D13 puts them in phase 4.
- D27, the Ubuntu WSL2 install for Bash-granting evals: phase 4.

