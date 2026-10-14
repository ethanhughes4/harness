# Factory: decisions

Stage: factory. The harness becomes a software factory: a short intake,
then a per-feature production line, then the owner. Agreed with the owner
2026-10-14 after the research in `reports/Efficient Claude Code build harness.md`
and the follow-ups in conversation (user tester, visual reviewer, shorter
start). docs/prd/harness-decisions.md (D1–D57) still holds unless a
decision here replaces it.

## The line

D58: Each feature is one job and goes through: test writer → builder →
gates → risk → reviewers → rework (at most 2 rounds) → merge, or
needs-human. This replaces the per-wave loop of D21. (reason: owner; research)

D59: The test writer (`harness:test-writer`, opus) turns the feature's
`steps` into executable acceptance tests in `<acceptance_dir>/<id>/`
(default `tests/acceptance`). For a `ui: true` feature these include
Playwright user flows. It runs them, confirms they FAIL on the current
code, and commits them on the job branch before the builder starts.
(reason: an oracle fixed before the code, by a different agent, is the
best-evidenced check; research "evidence" and "open_source_workflows")

D60: Acceptance tests are locked. The guard blocks any Edit, Write or
Bash from `harness:builder` that touches `<acceptance_dir>/**` (D56).
The gates also fail if those files differ from the test writer's commit.
A builder that thinks a test is wrong reports TEST_WRONG with its
reason; the organiser asks the resolver, and if the resolver agrees it
resumes the test writer to fix the test. (reason: reward hacking is
measured and rising; mitigations are environmental)

D61: The builder is sonnet. The organiser names it `builder-<id>` and
makes its worktree itself: `git worktree add .harness/wt/<id> -b
factory/<id>`; the builder works only in that folder. Rework round 1
resumes the same builder with SendMessage (D55) with the findings and
"think harder". Round 2 starts a fresh builder with `model: opus` on
the same branch. No `isolation: worktree` (D57 is unsettled).
(reason: research; D55; never retry unchanged)

D62: `scripts/gates.py <id> <round>` runs, with no AI: every `test`
command, every command in harness.json `gates` (lint, types, secret
scan, dependency audit; whatever setup found), and the acceptance
tamper check. Output is capped at 100 lines and written to
`.harness/jobs/<id>/gates-<round>.md`. Any failure goes straight back
to the builder as that round's findings, before any AI reviewer runs.
(reason: deterministic checks first; METR "passes but unmergeable")

D63: `scripts/risk.py <id>` lists the files the job branch changed
against main and matches them against harness.json `risky` globs
(defaults: auth, payment, crypto, secret, migration, CI, dependency
manifests, `.claude/**`). It prints `{"risk": "low"|"high", "files": [...]}`.
The builder never classifies its own work. (reason: Meta RADAR, Vercel;
consequence not size)

D64: Reviewers are listed in the plugin's `factory.json` (the shared
list): each entry has `name`, `agent`, `when` (`always`, `ui` or
`high_risk`) and `browser` (true or false). Each writes only
`.harness/jobs/<id>/round-<n>/review-<name>.md`, whose first line is
`VERDICT: PASS` or `VERDICT: CHANGES`; the guard enforces the file
ownership by agent type (D56). A blocking finding must cite a failing
test, a screenshot or a concrete fix; anything else is a note, not
CHANGES. (reason: precision-first review; research)

D65: The reviewers: `code` (`harness:reviewer`, opus, always: diff
against spec, decisions and architecture, then correctness); `security`
(`harness:security`, opus, high_risk); `user` (`harness:user-tester`,
sonnet, ui, browser: starts the app and uses it in a browser like a
person, following the feature's steps plus obvious wrong inputs and
console errors, with screenshots); `visual` (`harness:visual`, sonnet,
ui, browser: screenshots at 1280 px and 390 px wide, light and dark,
against `docs/design/` and the tokens, plus an axe accessibility scan;
blocks only on broken layout, overflow, wrong tokens, failed contrast,
missing focus or loading states, or a clear mockup mismatch; taste is a
note). (reason: owner; Anthropic, Replit and Factory test like a user)

D66: WAIT FOR ALL: a round is done only when every review file the
round needs exists. Browser reviewers of a job run one after the other
(one browser at a time on 8 GB); the others run in parallel with them.
Any CHANGES → rework. Still CHANGES or red gates after round 2's
rework → `needs-human`. (reason: owner; research: gains end by round 2–3)

D67: Merge: low risk and every review PASS → the organiser merges
`factory/<id>` into the main branch with `--no-ff`, runs every `test`
command; green → status done, commit, remove the worktree; red → reset
to before the merge and treat it as a rework round. High risk → status
`needs-human`, branch kept. No AI approver. (reason: LLM judges are
unstable; owner keeps the risky merges)

D68: `feature_list.json` gains a `status` field: `todo`, `building`,
`review`, `rework`, `needs-human`, `done`. Only `scripts/status.py <id>
<status>` changes it; `done` also sets `passes` true. The guard allows
that exact call, as for mark_pass.py (D17). Each job keeps its trail in
`.harness/jobs/<id>/`: `brief.md` (the feature, with the spec parts it
needs), `gates-<round>.md`, `round-<n>/review-*.md`, `decision.md`.
(reason: the factory's board and job folders without a second state file)

## Running it

D69: `build.cmd` runs `python <plugin_root>/scripts/build.py`. It loops:
start a fresh `claude -p --agent harness:organiser "Run the next jobs"
--permission-mode auto --permission-prompts none --output-format
stream-json --verbose` session (appending to build-log.jsonl); each
session takes up to `max_builders` ready jobs through the line to
done or needs-human, then ends. The script stops when no feature is
todo/rework-and-ready, or after two sessions in a row change nothing,
and prints `feature_list: N/M done, K needs-human`. /goal is no longer
used for the build. Each session starts with a preflight: tests pass
on the main branch and the app's `run` command starts. (reason:
research: fresh sessions beat one long one; a script, not a judge,
decides "done"; replaces D20, D23, D26's single /goal session)

D70: Every `walkthrough_every` merged UI features (default 5), and once
when nothing is left to build, the organiser runs each `browser`
reviewer in whole-app mode on the main branch. Findings go to
`progress.md` and to the report as needs-human items. (reason: Factory
validates per milestone; features can pass alone and fail together)

D71: The organiser's prompt has no "keep going whatever happens"
pressure for work; it keeps "never stop for a question" (D22).
(reason: Cursor measured more test hacking under keep-going prompts)

D72: `max_builders` defaults to 2 on this PC; test suites run one at a
time. (reason: ~1.5 GB per Claude Code process on Windows)

## The owner's part

D73: `/harness:new "<idea>"` is the one start command. It asks one list
of at most 15 questions that change what gets built, each with a
recommended answer ("ok" accepts all); the brief's items are in that
list; the critic checks TECHNICAL answers first (D29). Architecture is
decided without questions and recorded as decisions. For a UI app it
writes `docs/design/mockup.html` and `docs/design/tokens.md` for the
owner to approve once. Then, with no more stops, it does setup (one
screen of summary), writes the feature list and build.cmd, commits, and
tells the owner to run build.cmd. In an existing project it runs the
same intake for one feature or stage and appends to the list. The
`brief` skill is removed; `questions`, `setup` and `init-build` stay as
the parts `new` follows. (reason: owner: too many stages before building)

D74: `owner.md` is asked for only when `~/.claude/harness/owner.md` does
not exist; otherwise it is copied silently (replaces the per-project
step of D31). (reason: owner)

D75: Smoke tests the plugin, not each project: it runs when the plugin
changes. Projects get the preflight of D69 instead. Smoke adds two
checks: a headless subagent can take a Playwright screenshot and read
it, and a SendMessage-resumed builder still works in its
`.harness/wt/<id>` folder. (reason: owner; D57)

D76: `/harness:approve <id>` merges a needs-human job (tests must pass),
sets it done and commits. `/harness:rework <id> <note>` writes the note
to the job folder and sets it to rework; the next build session starts a
fresh builder with the note. (reason: factory commands)

D77: `/harness:report` adds: the needs-human list with each job folder,
cost per session from build-log.jsonl (`total_cost_usd`), and the
transcript paths of three builder runs for the owner to skim.
(reason: research: audit a sample of transcripts)

D78: Setup adds: a `deny` rule for `Bash(git push*)` (auto mode would
push), `run` (`{"cmd": [...], "url": "..."}`) for apps, `gates`,
`risky`, `acceptance_dir` and `walkthrough_every` in harness.json, and
Playwright (installed only after the owner says yes in the summary) for
UI projects. (reason: research: auto mode pushes to any branch)

D79: Dropped or deferred: a per-feature spec-writer (intake and the
test writer cover it); a fixed four-reviewer panel on every feature; an
AI approver; `/code-review` in the loop (D45 replaced: the code reviewer
does it); `board.json` and the HTML dashboard (deferred; the report and
job folders cover them). Browsing is by Playwright through Bash, not an
MCP server or Claude in Chrome. (reason: research; cost; headless)

## Added during the build

D80: The tamper check compares `<acceptance_dir>/<id>` against the commit
named in `.harness/jobs/<id>/acceptance.sha`, which the test writer's step
writes after committing its tests; without that file, it fails only on
uncommitted changes there. (builder, step 1; small detail)

D81: build.py treats `building` and `review` features as ready too, so a
job left half-done by a crashed session is picked up again by the next
session. (builder, step 1; fits D69 and principle 2)
