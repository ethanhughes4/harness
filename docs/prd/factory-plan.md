# Factory: build plan

Decisions: docs/prd/factory-decisions.md (D58–D79), on top of
docs/prd/harness-decisions.md (D1–D57).
Tests for this repo: `python -m pytest -q` at the repo root.

## Skeleton and the shared list

- **The shared list is `factory.json` at the plugin root**: the
  reviewers of a round (D64). Each reviewer step adds one entry and its
  own agent file. On a merge conflict there, keep every entry.
- The organiser reads `factory.json` and runs the line; it never needs
  editing to add a reviewer.
- `tests/test_factory.py` (step 1) checks every `factory.json` entry
  has a matching `agents/<agent>.md`, a valid `when` and a boolean
  `browser`, so later reviewer steps are checked without editing it.
- `tests/test_layout.py` already checks every agent and skill file.

## Shared formats

- `factory.json`:
  `{"reviewers": [{"name": "code", "agent": "harness:reviewer", "when": "always", "browser": false}]}`
- `.claude/harness.json` new keys, all optional, with these defaults in
  `scripts/common.py`: `max_builders` 2, `gates` `[]`,
  `risky` (the D63 default globs), `acceptance_dir` `"tests/acceptance"`,
  `walkthrough_every` 5, `run` none.
- `feature_list.json`: each feature may have `status` (D68); missing
  means `todo`, or `done` when `passes` is true.
- Job folder `.harness/jobs/<id>/`: `brief.md`, `gates-<round>.md`,
  `round-<n>/review-<name>.md`, `decision.md`. Rounds count from 1.
- Branch `factory/<id>`, worktree `.harness/wt/<id>`. `.harness/wt/`
  is git-ignored; `.harness/jobs/` is committed.
- Review file first line: `VERDICT: PASS` or `VERDICT: CHANGES`.

## Wave 1

### Step 1: One feature goes through the line. Status: TODO
Depends on: none.

After it: in a set-up project, `build.cmd` runs `build.py`. Each fresh
organiser session takes up to 2 ready features through builder, gates,
risk, the code reviewer, up to 2 rework rounds, then merge or
needs-human. You can watch `.harness/jobs/<id>/` fill up, and
`feature_list.json` statuses change.

Creates:
- `factory.json` with the `code` entry (D64, D65)
- `scripts/status.py`: sets `status`, and `passes` true on `done`, in
  place like mark_pass.py (D68)
- `scripts/gates.py`: `test` commands, `gates` commands, and the
  acceptance tamper check (empty folder is fine) (D60, D62)
- `scripts/risk.py` (D63)
- `scripts/build.py`: the session loop, stop rules and status line; the
  `claude` command it runs can be replaced by an argument so tests can
  stub it (D69, D72)
- `tests/test_status.py`, `tests/test_gates.py`, `tests/test_risk.py`,
  `tests/test_build.py` (stubbed sessions: stops when done, stops after
  two sessions without change), `tests/test_factory.py`

Changes:
- `agents/organiser.md`: rewritten for the job line: pick, worktree,
  named builder, gates, risk, reviewers from `factory.json` with WAIT
  FOR ALL and browser reviewers one at a time, rework by resume then
  fresh opus builder, merge or needs-human, job files, preflight,
  milestone walkthrough for `browser` reviewers, no keep-going
  pressure (D58, D61–D67, D69–D72)
- `agents/builder.md`: works in the folder it is given, no
  `isolation`, answers rework messages, reports TEST_WRONG (D60, D61)
- `agents/reviewer.md`: per feature: diff `main...factory/<id>`, writes
  its review file with the VERDICT line; blockers cite a test or fix
  (D64, D65)
- `scripts/common.py`: the defaults above
- `scripts/guard.py`: allows the exact `status.py` call; a reviewer
  agent may write only its own `review-<name>.md` under `.harness/jobs/`
  (D56, D64, D68)
- `tests/test_guard.py`: the new rules
- `skills/init-build/SKILL.md`: build.cmd runs build.py; features get
  `status: "todo"`; `.harness/wt/` to .gitignore (D68, D69)

## Wave 2

### Step 2: Tests are written first and locked. Status: TODO
Depends on: 1.

After it: each job starts with `harness:test-writer` committing failing
acceptance tests; the builder can't change them, and gates fail if
anything did.

Creates: `agents/test-writer.md` (D59).
Changes: `scripts/guard.py` (block `harness:builder` on
`<acceptance_dir>/**`), `tests/test_guard.py`, `agents/organiser.md`
(test-writer first; TEST_WRONG path through the resolver) (D59, D60).

### Step 3: Security review on risky changes. Status: TODO
Depends on: 1.

After it: a job that touches a `risky` path gets a security review and
always ends needs-human.

Creates: `agents/security.md` (D65).
Changes: `factory.json`: add `security` (`high_risk`, browser false).

### Step 4: The user tester uses the app. Status: TODO
Depends on: 1.

After it: every UI feature is used in a real browser like a person
would, with screenshots in its round folder; it also does the milestone
walkthrough.

Creates: `agents/user-tester.md` (Playwright through Bash; starts the
app from `run`, stops it after) (D65, D70, D79).
Changes: `factory.json`: add `user` (`ui`, browser true).

### Step 5: The visual reviewer checks the look. Status: TODO
Depends on: 1.

After it: every UI feature is screenshotted at phone and desktop width,
light and dark, checked against `docs/design/` and the tokens, with an
axe scan.

Creates: `agents/visual.md` (D65).
Changes: `factory.json`: add `visual` (`ui`, browser true).

### Step 6: Approve and rework. Status: TODO
Depends on: 1.

After it: `/harness:approve <id>` merges a needs-human job;
`/harness:rework <id> <note>` sends it back.

Creates: `skills/approve/SKILL.md`, `skills/rework/SKILL.md` (D76).

### Step 7: The report shows the factory. Status: TODO
Depends on: 1.

After it: `/harness:report` lists needs-human jobs with their folders,
cost per session and three transcripts to skim.

Changes: `skills/report/SKILL.md` (D77).

## Wave 3

### Step 8: One command to start. Status: TODO
Depends on: 1, 2, 4, 5.

After it: `/harness:new "<idea>"` asks one list of at most 15 questions,
shows a mockup for UI apps, then sets up, writes the feature list and
build.cmd and commits, ready for `build.cmd`.

Creates: `skills/new/SKILL.md` (D73, D74, D78).
Changes: `skills/questions/SKILL.md` (question cap, brief items, mockup
and tokens), `skills/setup/SKILL.md` (new harness.json keys, push deny,
Playwright, one-screen summary, no separate review stop when run from
`new`), `skills/owner/SKILL.md` (only when no master exists).
Deletes: `skills/brief/` (D73).

### Step 9: Smoke tests the plugin. Status: TODO
Depends on: 1, 4.

After it: `/harness:smoke` proves the line on a mini-spec, plus a
Playwright screenshot read by a headless subagent and a resumed builder
still in its worktree.

Changes: `skills/smoke/SKILL.md`, `skills/smoke/feature_list.json`,
`skills/smoke/spec.md` (D75).

### Step 10: The design doc matches the factory. Status: TODO
Depends on: 1.

After it: `docs/design.md` describes the factory as built.

Changes: `docs/design.md` (D58–D79).

## Coverage

D58 s1 · D59 s2 · D60 s1,2 · D61 s1 · D62 s1 · D63 s1 · D64 s1,3,4,5 ·
D65 s1,3,4,5 · D66 s1 · D67 s1 · D68 s1 · D69 s1 · D70 s1,4 · D71 s1 ·
D72 s1 · D73 s8 · D74 s8 · D75 s9 · D76 s6 · D77 s7 · D78 s8 · D79 s4,10

## UNCOVERED

None. The proof run (a 15–20 feature app built end to end) is billed
and long, so it follows this plan rather than being a step in it.
