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
`high_risk` or `milestone`), `browser` (true or false) and optional
`batch` (true or false, default false; never with `browser: true`; D109).
Each writes only
`.harness/jobs/<id>/round-<n>/review-<name>.md`, whose first line is
`VERDICT: PASS` or `VERDICT: CHANGES`; the guard enforces the file
ownership by agent type (D56). A blocking finding must cite a failing
test, a screenshot or a concrete fix; anything else is a note, not
CHANGES. (reason: precision-first review; research)

D65: The reviewers: `code` (`harness:reviewer`, opus, always: diff
against spec, decisions and architecture, then correctness); `security`
(`harness:security`, opus, high_risk); `user` (`harness:user-tester`,
sonnet, milestone, browser (D111): starts the app and uses it in a browser like a
person, following the feature's steps plus obvious wrong inputs and
console errors, with screenshots); `visual` (`harness:visual`, sonnet,
milestone, browser (D111): screenshots at 1280 px and 390 px wide, light and dark,
against `docs/design/` and the tokens, plus an axe accessibility scan;
blocks only on broken layout, overflow, wrong tokens, failed contrast,
missing focus or loading states, or a clear mockup mismatch; taste is a
note). (reason: owner; Anthropic, Replit and Factory test like a user)

D66: WAIT FOR ALL: a round is done only when every review file the
round needs exists. Browser reviewers of a job run one after the other
(one browser at a time on 8 GB); the others run in parallel with them.
Reviewers marked `batch` run once for the jobs that are ready together
(D109). Any CHANGES → rework. Still CHANGES or red gates after round 2's
rework → `needs-human`. (reason: owner; research: gains end by round 2–3)

D67: Merge: low risk and every review PASS → the organiser merges
`factory/<id>` into the main branch with `--no-ff`, runs every `test`
command; green → status done, commit, remove the worktree; red → reset
to before the merge and treat it as a rework round. High risk → status
`needs-human`, branch kept, never merged by the organiser: a successful
review, security included, does not change that. This is enforced in
`scripts/merge.py`, the only way the organiser may merge (D108). No AI
approver. (reason: LLM judges are
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
when nothing is left to build (the final walkthrough), the organiser runs
each `milestone` reviewer in whole-app mode on the main branch. Findings go to
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

## Smoke test, 2026-10-14

D82: ${CLAUDE_PLUGIN_ROOT} is substituted in plugin agent text too, not
only skill text, so "never use ${CLAUDE_PLUGIN_ROOT}" read as "never use
<the plugin folder>" and the organiser refused every job. Prompts name
the variable only on the one line that hands setup, new and smoke the
path; a test enforces it. (smoke run 1; answers the open part of D35)

D83: build.py streams each session's output straight into
build-log.jsonl, so a killed session keeps its log. (smoke run 1)

D84: risk.py diffs against the branch the project root has checked out,
not a guessed `main`. (smoke run 2: a project on another branch name was
parked as needs-human)

D85: Agents read feature_list.json and the acceptance tests with the Read
tool; the guard blocks any Bash command naming them, reads included, and
each block shows up as a permission denial. (smoke runs 2 and 3)

D86: Smoke result after the fixes: guard checks, job folders, both
features done and merged, and resume all PASS. Two features cost $1.02
in total, about $0.51 each. One denial remained: the builder used `cat`
on its acceptance tests, now covered in its prompt (D85). Playwright's
Chromium browser is not downloaded on this PC, so the browser check is
NOT EXERCISED; builder resume and resolver memory were NOT EXERCISED (no
rework, no questions).

D87: build.py adds `--plugin-dir <plugin_root>` to each session when
`claude plugin list` doesn't list harness, so a project can build while the
plugin is run from its repo rather than installed. Playwright's Chromium was
downloaded on 2026-10-14; smoke check 7 then passed (a headless subagent
screenshotted red "SMOKE 42" and read it, $0.38).

## Design layer (2026-10-14)

D88: The design layer is the third-party `web-design-engineer` skill
(ConardLi/garden-skills, MIT, commit 7a6d5a7, v1.3.0), copied unchanged
into `skills/web-design-engineer/` with its licence and a SOURCE.md
(D33). It is model-invocable so agents can load it (D4). The intake's UI
step follows it: 3 directions from different schools, the owner picks;
a Design Read with five dials and a recipe's concrete values, the owner
confirms; a v0 mockup self-critiqued, the owner approves. It writes
docs/design/design-system.md and tokens.md. The builder invokes it for
`ui: true` features and builds only from those files, with none of the
skill's interactive parts and nothing loaded from a CDN at run time. The
visual reviewer invokes it, uses its critique and failure patterns, and
also blocks on a listed AI cliché the design system doesn't choose.
(owner chose this skill; live check: a subagent invoked it via the Skill
tool and quoted it, $0.42) This replaces the deferral in D13 for design.

D89: `/harness:new` resumes a half-finished intake: when docs/spec.md
exists but feature_list.json doesn't, it keeps what the docs settle, asks
only what's open, and redoes the design step if design-system.md is
missing. (Pocket's first intake stopped before setup.)

D90: ui-ux-pro-max is not used; the owner chose web-design-engineer.

D91: Both design skills are used (owner, replaces D90). ui-ux-pro-max
(nextlevelbuilder/ui-ux-pro-max-skill, MIT, commit 7246805) is copied into
`skills/ui-ux-pro-max/` with its data, references and four runtime scripts;
its SKILL.md paths were changed to `${CLAUDE_SKILL_DIR}/scripts/search.py`
(see its SOURCE.md). Division of work: web-design-engineer decides the look
(direction, recipe, colours, type); ui-ux-pro-max supplies usability rules
(quick-reference priorities, pro-rules checklist, `--domain ux` and
`--domain chart` searches). Its palette and style picks count only where
they agree with the recipe: for Pocket its default was glassmorphism with
#3B82F6, the cliché web-design-engineer warns against. Intake records the
rules as a "UX rules" section in design-system.md; the builder, visual
reviewer and user tester invoke it; the visual reviewer blocks on broken
CRITICAL rules (accessibility, touch targets under 44 px) and the user
tester on broken CRITICAL or HIGH usability rules. `--persist` is never
used. Setup allows its search script. Reviewed: SKILL.md and all four
scripts read in full (stdlib only, no network, no subprocess, reads only
its data/, writes only with --persist); data greps clean. Live check: a
subagent invoked it and ran the search, $0.39, no denials.

D92: The owner's user-scope ui-ux-pro-max plugin also loads in every
session, so the skill appears twice (`ui-ux-pro-max:ui-ux-pro-max` and
`harness:ui-ux-pro-max`). Harness agents name `harness:ui-ux-pro-max`.
Disabling the user plugin (`claude plugin disable ui-ux-pro-max`) avoids
the double description cost (D33); left to the owner.

D93: The intake never asks the owner to pick a design direction from words
alone. It writes docs/design/directions.html (the main screen in all three
directions side by side, with sample data, light/dark, phone width) and
opens it in the browser before asking. (owner, 2026-10-14, during Pocket's
intake)

D94: A design preview meets the same bar as the final design: each
direction from its real recipe (fonts, palette, signature moves), the
three different in layout and type, not recolours; only what the screen
needs, with clear hierarchy; screenshotted at 390 and 1280 px in light and
dark and fixed before it is shown; each direction critiqued with the
skill's 5 dimensions and reworked below 7. "Works offline" means fonts and
libraries are bundled into the project, never "use system fonts".
(owner, 2026-10-14: Pocket's first preview used system fonts because its
D41 read offline as "fonts already on the device", and showed one
wireframe in three colour schemes with a wrapping bug in B.)

## Design guideline (2026-10-14)

D95: The harness has its own design guideline, from the research in
`reports/Design guideline against AI look.md`: the "Never" tells N1-N19,
the "Always" rules A1-A17, the 10 per-client steps and the checks. It lives
in our skill `skills/design-guideline/` (model-invocable) with the tells
list in a versioned file. It sits above both vendored skills and wins where
they disagree (the report's disagreement table: the terracotta sample
direction, "Aim to Stun" glass and fade-ins, self-scored critique, browser
acceptance only on request, Inter pairings and glass from ui-ux-pro-max,
line height). Overriding rule: a Never item may be used and an Always rule
broken only with a reason on the brand sheet that names the brief, the
client's assets or a competitor gap.

D96: The intake's design step follows the guideline's 10 per-client steps:
facts, discovery answers, "this not that" adjectives, sliders, competitor
audit with keep/break, attribute-to-choice mapping with reasons, three
directions led by different adjectives and schools, a difference test, a
visual preview (directions.html, randomised order, rationale under each,
screenshotted and checked before opening, D93-D94), and a brand sheet.
docs/design/design-system.md IS the brand sheet. The builder may use only
values on it.

D97: `scripts/design_audit.js` (browser-side, no dependencies) measures a
page from computed styles and runs the coded tell detectors;
`scripts/design_audit.py` runs it with Python Playwright at 360, 768 and
1440 px plus a focus and a reduced-motion pass, checks values against the
brand sheet tokens, and prints JSON with failures, warnings and the tell
score (>= 4 unjustified fails, 2-3 sends to the judge). Python Playwright is
the one non-stdlib dependency; the script says so plainly if missing.

D98: The visual reviewer runs design_audit.py first (hard gates), then acts
as the separate screenshot judge with the guideline's narrow questions:
dominant element, closed word-list pick, generic imagery, icon family,
reasons visible, and pairwise against the previous round in both orders
(a disagreement is a tie). It never gives absolute taste scores. Rounds keep
the best, not the last.

D99: Python Playwright 1.64 was installed on this PC (2026-10-14); Node
Playwright existed only in the npx cache, so agents' `require('playwright')`
would have failed and sent every UI job to needs-human. Setup installs
Python Playwright for Python UI projects after the owner says yes (D78).

## Premium layer (2026-10-15)

D100: Avoiding AI tells only reaches "competent"; premium is a separate
layer. Source: reports/What makes sites look premium.md ("Changes to the
pipeline"). The owner judged Pocket's Instrument mockup, which passed every
check, still AI-made. This layer applies to every client.

D101: Reference step. Before directions, the intake picks 3-5 premium
products in the client's category plus one object or brand from outside
software, captures the same screen types the app needs with
`scripts/reference_capture.py` (screenshots at 390 and 1440 px plus the
audit's measured values), and writes docs/design/reference-spec.md with
exact, checkable values and what to borrow (systems) vs not (assets,
signature look). Directions derive from the references. A fresh-model test
checks the result is not a copy (it must not name the reference).

D102: Premium spec. skills/design-guideline/references/premium-spec.md
holds sourced defaults (size-dependent tracking, in-between weights with
large type lighter, off-black text and off-white or tinted backgrounds,
1px alpha ring borders, layered low-opacity shadows, nested radii, one
ease-out curve and 2-3 durations, press/enter/exit states, loading timing,
tabular figures, text-wrap, focus). They apply unless the brand sheet
overrides one by naming a reference or brief fact that shows the
alternative working. Recipe names are not reasons.

D103: Critique loop. A separate `harness:design-critic` agent (fresh
context) judges previews, mockups and built UI against the matching
reference screens pairwise in both orders, points at regions with cropped
screenshots, scores several named dimensions, and runs at most 3 rounds,
keeping the best. It is calibrated with Pocket's Instrument mockup as the
"competent but generic" example (stored in the guideline skill). The
visual reviewer uses it for the judgement part.

D104: Fonts for client work: references/fonts.md in the guideline skill
lists free commercial-licence faces that read premium and are not
overused, the overused ones to avoid (Clash Display, Satoshi, and the
next-defaults list), never Pangram Pangram freebies on client sites, and
when to recommend a paid licence (with a shortlist). Bundling terms must
be checked per font for offline apps; the brand sheet records the licence.

D105: The design audit gains the report's premium checks (tracking by size,
pure black/white text, opaque vs alpha borders, shadow layering, easing and
duration count, text-wrap, figures, punctuation, nested radii, press state,
colourfulness), and a compare mode that reports a page's values against a
reference-spec range.

D106: reference_capture.py takes one screenshot per screenful while
scrolling (up to 8 per width, named <width>-<n>.png) instead of one tall
image. Premium sites such as Mercury pin sections and animate them in on
scroll, so a full-page screenshot showed only the hero and a background
image; per-screen captures show the real product UI. (live check
2026-10-15 on mercury.com and linear.app)

## Review cost and safety, 2026-10-16

D107: Adding features goes through `scripts/init_features.py --check|--apply
init-features-candidate.tmp`. Cause of the first-run blocker: init-build told
Claude to write `feature_list.json` while the guard (D17, D68) blocks every
Write, Edit and Bash on it, and status.py / mark_pass.py only edit existing
records. The script validates a candidate list of NEW features (valid JSON,
required fields of the existing schema, unique ids, known dependencies, no
self-dependency or cycle, status `todo`, passes false), never changes an
existing feature, and `--apply` replaces the file atomically; `--check`
changes nothing. The candidate must be named `init-features-candidate.tmp` in
the project root. The guard allows the exact command only when the hook input
has no `agent_type`: PreToolUse input carries it for subagents and `--agent`
sessions (D56), so the interactive init-build session can run it and the
builder, reviewers, organiser and every other subagent cannot. Direct Write
and Edit stay blocked for everyone. (reason: a narrow door instead of
loosening the lock; acceptance criteria must not be rewritable by builders)

D108: `scripts/merge.py <id> <round>` is the one place a job merges. It
requires `gates-<round>.md` PASS and every review the job needs (from
`factory.json`: `always`, `high_risk` when risk.py says high, `ui` for a UI
feature) to be `VERDICT: PASS`, and no CHANGES file in the round. A high-risk
job is then NOT merged: status `needs-human`, the reason and risky files in
`decision.md`, branch and worktree kept; it waits for `/harness:approve`
(D76). A low-risk job is merged `--no-ff`, tests run, red undoes the merge with
`reset --keep` (uncommitted job files survive), green sets `done`. The guard
blocks `git merge` from the organiser. This fixes the organiser prompt that said
a high-risk job was merged automatically, against D67.

D109: Batch review. The organiser builds up to `max_builders` jobs (concurrency
unchanged), runs the gates and risk for each, and only when every picked job is
past its gates runs a `batch: true` reviewer (the `code` reviewer) once for all
of them, in one call. That reviewer reads the shared project files once, then
judges each job alone and writes one `round-<n>/review-code.md` per job, each
with its own VERDICT line. There is never a shared verdict. Jobs with PASS merge
through merge.py at once; only the jobs with CHANGES are reworked, get new gates
and risk, and are reviewed again (together if they are ready together). Reviewers
without `batch` run per job as before. (reason: the opus reviewer reread the same
spec, decisions and rules for every feature)

D110: build.py reads `--session-cmd` before it runs `claude plugin list`, so a
stubbed session never needs Claude Code installed. A session that exits nonzero
or cannot start stops the build with exit 1, a message on stderr and the status
line; its output stays in build-log.jsonl. It is not counted as an idle session.
Completed builds and two idle sessions in a row end as before, exit 0.

D111: Milestone UI review. `user` and `visual` have `when: "milestone"`: they
no longer run for each UI feature. Feature-level acceptance tests (with
Playwright flows), gates and the code review still run on every feature. The
whole-app walkthrough (D70) runs them every `walkthrough_every` merged UI
features (default 5) and once at the end. The organiser may run a milestone
reviewer on one feature earlier when a gate, test or code-review finding is
about what the user sees, or a UI feature is high risk, and records why in
`decision.md`. (reason: the same screens were reviewed twice by two sonnet
browser agents)
