# Harness: decisions for phases 1 and 2

Stage: harness, phases 1 (Skeleton) and 2 (New parts) of the build plan
in docs/design.md. Questions answered 2026-10-08. Docs checked against
code.claude.com/docs on the same day, Claude Code v2.1.294.

## Facts from the docs (these override the design where they differ)

D1: Plugin agents ignore the frontmatter fields `hooks`, `permissionMode`
and `mcpServers`. The builder's Stop hook moves to the plugin's
hooks/hooks.json as a SubagentStop hook with matcher `^harness:builder$`.
(reason: sub-agents docs, "Plugin subagents ignore these frontmatter fields")

D2: Plugin components are namespaced: agents are `harness:builder`,
`harness:organiser`, `harness:reviewer`, `harness:resolver`,
`harness:critic`; skills run as `/harness:<skill>`. Agent prompts name
the namespaced types. (reason: plugins reference, `name`)

D3: A plugin can't ship permissions, `env`, `worktree.baseRef` or rule
files; its settings.json only takes `agent` and `subagentStatusLine`, and
a plugin-root CLAUDE.md isn't loaded. /harness:setup writes all of these
into the project, including `worktree.baseRef: head` (otherwise
`isolation: worktree` branches from the default branch, not HEAD).
(reason: plugins reference, `settings` and standard layout; sub-agents docs)

D4: Skills with `disable-model-invocation: true` can't be preloaded with
the agent `skills` field. Specialist skills that agents preload are
model-invocable, so they cost their description every turn.
(reason: sub-agents docs, "How the skills field works")

D5: The /goal judge is the small fast model and can't read files or run
commands; it judges only what the conversation shows. The turn limit in
the condition is judged from the conversation too, so it is approximate.
(reason: /goal docs, "How evaluation works")

D6: Stop hooks are capped at 8 consecutive continuations; the count resets
when a tool is called. (reason: hooks reference, Stop "Block cap")

D7: `claude -p` supports `/goal`, `--permission-mode auto` and
`--permission-prompts none` (needs v2.1.259+); `--output-format
stream-json --verbose` streams each message. (reason: headless and /goal docs)

D8: Plugin evals that grant Bash need an OS sandbox; native Windows has
none. This PC's WSL2 has only the docker-desktop distro.
(reason: plugin evals docs, "Grant tools"; `wsl --status`)

## Repo and layout

D9: The design doc lives at docs/design.md (renamed with git mv).
(reason: the getting-started steps and the build prompt use that path)

D10: The plugin lives at the repo root: .claude-plugin/plugin.json,
skills/, agents/, hooks/hooks.json, scripts/. The repo's .claude/ stays
as tooling to build the harness itself, with every FPL detail removed.
(reason: plugin standard layout; namespacing keeps the two sets apart)

D11: The plugin does not ship prd, plan-stage or run-plan; feature_list.json
replaces the plan. plan-stage and run-plan stay in .claude/ to build the
harness. prd is deleted. (reason: not in the design's skill list;
plan-stage covers prd)

D12: The repo is MIT licensed and private on GitHub.
(reason: a licence is needed before vendoring MIT/Apache skills)

## Scope

D13: Phase 2 adds only the `architecture` skill (ours, based on
architecture-designer), used by `questions` and preloaded into the
reviewer. frontend-design, ui-ux-pro-max, ui-builder and ui-reviewer wait
for phase 4, where the React reference project tests them.
(reason: the phase 2 list doesn't name them; the UI parts need a UI project to prove)

## Hooks

D14: Every plugin hook exits 0 at once unless the project has
.claude/harness.json, which /harness:setup writes.
(reason: at user scope the plugin's hooks fire in every project)

D15: .claude/harness.json holds the project's test commands, time limit,
builder cap and protected paths, e.g.
`{"test": [["python","-m","pytest","-q"]], "test_limit_s": 300,
"max_builders": 3, "protected": ["data/raw/**"]}`. hooks.json gives the
test hook a fixed 600 s timeout; the script enforces `test_limit_s` and
warns past 80% of it. (reason: hooks.json is static per plugin; limits and
the 3-builder cap are per project and per machine)

D16: Hook scripts are Python, standard library only, run in exec form
(`"command": "python", "args": [...]`). (reason: matches FPL; npm .cmd
shims can't run in exec form on Windows)

D17: Only scripts/mark_pass.py <id> flips `passes` in feature_list.json,
and only the organiser calls it. A PreToolUse hook on Edit|Write|Bash
blocks every other change to feature_list.json and to the `protected`
paths. (reason: the organiser edits files through Bash, so an Edit/Write
guard alone leaks)

D18: SessionStart (matcher `compact`) re-injects, in under 2 KB: the
brief's must-nevers, the features in progress, the paths of owner.md and
decisions.md, and the last 20 lines of progress.md.
(reason: CLAUDE.md already reloads after compaction)

D19: StopFailure appends the error type and details to progress.md.
(reason: design; StopFailure has no decision control, logging only)

## Build loop

D20: The organiser is the main session of the headless build. build.cmd
runs `claude -p --agent harness:organiser "/goal Every feature in
feature_list.json has passes true and all test suites pass, or stop after
200 turns" --permission-mode auto --permission-prompts none
--output-format stream-json --verbose >> build-log.jsonl`. Builders,
reviewer and resolver are its subagents. Each /goal turn is one loop turn.
(reason: no extra nesting level; D7)

D21: Each loop turn runs these six steps:
1. Pick next features: failing, depends_on all passing, at most
   `max_builders` (3).
2. Builders, one feature each, tests first.
3. Merge and test: the test hook blocks any failure.
4. Reviewer: spec first, then quality.
5. Evals and decision rules: run any eval in the feature's acceptance
   steps; beat its baseline or apply the matching decision rule.
6. Mark passes (mark_pass.py) and commit; append to progress.md.
(reason: the original diagram, from the owner)

D22: The resolver is not a loop step. Builders and the organiser call it
whenever a question comes up. An open question gets the recommended
answer, recorded as PROVISIONAL; the build never stops for it.
(reason: owner; design principle 6)

D23: Each turn ends by printing
`feature_list: N/M passing, suites green|red` for the /goal judge.
(reason: owner; D5)

D24: A BLOCKED builder gets one retry with the resolver's answer; then the
feature is skipped and logged, and features that depend on it wait.
(reason: design, headless build loop)

D25: feature_list.json is one file for all stages:
`[{id, stage, title, ui, depends_on, steps, passes}]`. New stages append
features. docs/spec.md and docs/decisions.md are likewise one file each,
with a heading per stage. (reason: existing repos like FPL add stages)

D26: A rerun of build.cmd starts a fresh session (no --continue) and
resumes from the files. (reason: design principle 2)

## Testing the harness

D27: Phase 2's "passing test or eval case": hook scripts and mark_pass.py
get pytest tests run on Windows; questions, init-build and the resolver
each get one `claude plugin eval` case that grants no Bash. An Ubuntu
WSL2 distro is installed in phase 4 for Bash-granting cases and the
baseline comparison. (reason: D8)

D28: /harness:smoke runs in a temporary clone of the project with a fixed
two-feature mini-spec and proves: the guard blocks a deleted feature,
`permission_denials` in the stream output is empty, a killed run resumes
on rerun, and the resolver's memory directory is written. The clone is
deleted afterwards. (reason: design step 6; D30)

## Skills and agents

D29: /harness:questions asks everything in one list, each question with a
recommended answer and tagged TECHNICAL or PREFERENCE. The critic checks
every TECHNICAL answer first (AGREE, or CHANGE with a quote and link). The
owner sees the PREFERENCE questions and the critic's changes, and changes
only what they disagree with. It writes docs/spec.md, docs/decisions.md
and the decision rules. (reason: design; replaces FPL's one-at-a-time rule)

D30: The resolver keeps `memory: project` (.claude/agent-memory/ in each
project); it works only while auto memory is on. (reason: sub-agents docs)

D31: The master owner.md lives at ~/.claude/harness/owner.md; each project
gets a copy at docs/owner.md. (reason: ${CLAUDE_PLUGIN_DATA} is deleted on uninstall)

D32: The owner-writes option stays: features tagged `owner-writes` are
skipped by builders. The owner's standing answer in owner.md is "Claude
writes all code; I read and edit", so no feature is tagged owner-writes
unless a project's brief asks for it. Wording is gender-neutral.
(reason: owner)

## Third-party skills (phase 4, not installed)

D33: Before adding a third-party skill: read every file, copy the
reviewed version into the plugin with its licence, pin the commit, and
confirm it has no `disable-model-invocation` (D4).
- frontend-design (anthropics/skills): read LICENSE.txt and SKILL.md.
- ui-ux-pro-max (nextlevelbuilder, MIT): read scripts/search.py and the
  other scripts; confirm no network calls or writes outside the project;
  disable the user-installed ui-ux-pro-max plugin to avoid a double load.
- architecture-designer (jeffallan, MIT): basis only; ours is rewritten,
  keep the MIT notice if any text is reused.
- /code-review: bundled; confirm the reviewer can call it.
(reason: design, "Rules for adding outside skills")

## Added at plan approval (2026-10-08)

D34: The repo's own build hook (.claude/hooks/run_tests.py) runs pytest
only; the npm/web part is removed before /run-plan, in the main session,
not by a builder. Done and committed in f747e5c; run with and without
--always and no web/ folder, both exit 0.
(reason: owner; step 1's builder would otherwise run under the FPL hook)

D35: Agent and skill text does not rely on ${CLAUDE_PLUGIN_ROOT}
expanding. /harness:setup writes the plugin's absolute folder into
.claude/harness.json as "plugin_root"; agents and skills read script
paths from there. Hooks in hooks/hooks.json may still use
${CLAUDE_PLUGIN_ROOT}. (reason: owner; expansion in agent and skill
text is unconfirmed)

D36: The builder's instructions say it may start only harness:resolver,
because an Agent(...) allow-list in a subagent's tools is ignored.
(reason: owner)
