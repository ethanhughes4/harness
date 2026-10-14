# Project Harness: Design

Updated Oct 14, 2026 · @Ethan Hughes

A Claude Code plugin that works as a software factory. You answer one list of questions, which takes about 10 to 15 minutes. Then `build.cmd` runs headless: every feature goes down a production line until it is merged or handed back to you.

The decisions behind this are D58 to D81 in `docs/prd/factory-decisions.md`, on top of D1 to D57 in `docs/prd/harness-decisions.md`. The research is in `reports/Efficient Claude Code build harness.md` (the "research report" below).

## What it takes from the research

The research report compared Anthropic's harness, commercial agents (Factory, Replit, Copilot), open-source workflows (Superpowers, Spec Kit) and papers on review, repair and reward hacking. The factory keeps what the evidence supports and drops the rest.

| Finding in the research report | What it does in our factory |
| --- | --- |
| One writer, a JSON feature list that starts failing, a progress file, git per feature ([Anthropic harness](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents)) | `feature_list.json` with `status`, `progress.md`, one merge per feature. A build can't finish by quietly dropping work |
| Tests in the prompt and structured test feedback beat everything else per token | A test writer makes executable acceptance tests before the builder starts |
| Reward hacking is measured and rising; it rose under "keep going" prompts (METR, Cursor) | Acceptance tests are locked against the builder; the organiser has no "keep going" pressure |
| Passing tests is not mergeable: none of 15 METR PRs were (lint, types, gaps) | `gates.py` runs tests, lint, types, secret scan and audit before any AI reviewer |
| LLM reviewers over-flag correct code; judges are unstable; no evidence that a panel beats one strong reviewer | One strong code reviewer on every feature. Other reviewers run only when the feature needs them. A blocking finding must cite a failing test, a screenshot or a concrete fix. No AI approver |
| Route by consequence, not size; the author must not classify its own risk (Meta RADAR, Vercel) | `risk.py` matches changed files against `risky` globs. High risk waits for you |
| Gains from repair end by round 2 to 3; never retry unchanged | At most 2 rework rounds: a resumed builder, then a fresh opus builder |
| Sonnet where tokens are many, opus where they are few and errors are costly | Sonnet builds; opus writes tests, reviews and organises |
| Checks that use the running app as a person would catch most (Anthropic, Replit, Factory) | A user tester and a visual reviewer drive a real browser |
| Fresh sessions beat one long one; a script, not a judge, decides "done" | `build.py` starts a fresh organiser session per batch and counts statuses |
| About 1.5 GB per Claude Code process on Windows | 2 builders by default, one suite and one browser at a time |
| Audit a sample of transcripts | The report lists three builder transcripts to skim |
| Plugin evals with a no-plugin baseline ([plugin evals](https://code.claude.com/docs/en/plugin-evals)) | Proves the factory beats plain Claude Code |
| Resolver with quoted sources, D-numbered decisions, provisional answers; graders that print what failed (FPL build) | Questions get answered without stopping the run |

## Design principles

Six rules decide every part of the design:

1. **People decide, machines build.** Your time goes into the intake list, the mockup and the needs-human jobs. Everything else runs without you.
2. **State lives in files.** The feature list, job folders, progress log, decisions and git history are the memory. Any session, or a rerun after a crash, picks up from them.
3. **Every check that can be a script is a script.** Tests, lint, types, secret scan, the tamper check, risk class, file guards and timing are scripts (`gates.py`, `risk.py`, hooks). Agents only do work that needs judgement.
4. **Nothing grades its own work.** A different agent writes the tests than writes the code. The reviewers see the diff and the spec, not the builder's reasoning. The builder never decides its own risk. A script, not a model, decides when the build is done.
5. **Decide in advance what results mean.** Decision rules ("if X scores under Y, switch to Z") let the build act on results without asking you.
6. **Never stop for a question; never hide one.** Unanswered questions get the recommended answer, marked provisional, and listed for you at the end.

## Your part

| Step | Command | Time | Output |
| --- | --- | --- | --- |
| Start | `/harness:new "<idea>"` | about 10 to 15 minutes | One list of at most 15 questions with a recommended answer each ("ok" accepts all). For a UI app, one mockup and tokens to approve. Then setup, the feature list, `build.cmd` and a commit |
| Build | `build.cmd` | headless | The app, one merge per feature |
| Act | `/harness:report`, then `/harness:approve` or `/harness:rework` | as needed | Needs-human jobs settled; provisional decisions confirmed |

The critic checks every TECHNICAL answer first, so you see only preference questions and the critic's changes. Architecture is decided without questions and recorded as decisions. Your standing preferences (`owner.md`) are asked for only the first time, then copied from `~/.claude/harness/owner.md`. In an existing project, `/harness:new` runs the same intake for one feature or stage and appends to the list.

## The line

Each feature is one job. It goes through the line below, in its own branch `factory/<id>` and worktree `.harness/wt/<id>`.

```
test writer -> builder -> gates -> risk -> reviewers -> merge
                   ^                          |
                   +---- rework (at most 2) --+      or: needs-human
```

| Stage | Who | What happens |
| --- | --- | --- |
| Test writer | `harness:test-writer`, opus | Turns the feature's `steps` into acceptance tests in `<acceptance_dir>/<id>/` (default `tests/acceptance`), with Playwright flows for UI features. Checks they fail on the current code, commits them, and writes the commit to `.harness/jobs/<id>/acceptance.sha` |
| Builder | `harness:builder`, sonnet | Builds the feature in its worktree. Can't touch the acceptance folder. Reports DONE, DONE\_WITH\_CONCERNS, BLOCKED, NEEDS\_CONTEXT or TEST\_WRONG |
| Gates | `scripts/gates.py <id> <round>` | No AI. Runs every `test` command, every `gates` command and the tamper check. Output is capped at 100 lines and written to `gates-<round>.md`. Any failure goes straight back to the builder |
| Risk | `scripts/risk.py <id>` | Prints `{"risk": "low"\|"high", "files": [...]}` from the files changed against main |
| Reviewers | listed in `factory.json` | Run when their `when` says so. Each writes `round-<n>/review-<name>.md` starting `VERDICT: PASS` or `VERDICT: CHANGES` |
| Merge | organiser | Low risk and every review PASS: `git merge --no-ff`, run every `test` command. Green: status `done`. Red: reset to before the merge and rework. High risk: status `needs-human`, branch kept |

**Waiting.** A round is done only when every review file it needs exists. Browser reviewers of one job run one after the other. The others run in parallel with them.

**Rework.** Round 1 resumes the same builder (`SendMessage`) with the findings and "think harder". Round 2 starts a fresh opus builder, `builder-<id>-2`, on the same branch. If the job is still red after round 2's rework, it becomes `needs-human`. The same findings are never sent a third time.

**Tests the builder thinks are wrong.** The builder reports TEST\_WRONG. The organiser asks the resolver. If the resolver agrees, the test writer fixes the test and the builder carries on. This is not a rework round.

**Questions.** Any question goes to the resolver, which checks the spec, `owner.md`, the decision rules and the docs, in that order. Anything still open gets the recommended answer, recorded as PROVISIONAL.

## The reviewers

| Reviewer | Agent | Model | Runs when | Looks at | Blocks on |
| --- | --- | --- | --- | --- | --- |
| `code` | `harness:reviewer` | opus | Always | The diff against the spec, decisions and `docs/architecture.md`, then correctness | A finding that cites a failing test or a concrete fix |
| `security` | `harness:security` | opus | High risk | The changed files only | A concrete exploit path or fix |
| `user` | `harness:user-tester` | sonnet | UI features | Starts the app and uses it in a browser: the feature's steps, obvious wrong inputs, console errors, with screenshots | A step that fails or a broken flow, shown by a screenshot or an error |
| `visual` | `harness:visual` | sonnet | UI features | Screenshots at 1280 px and 390 px wide, light and dark, against `docs/design/` and its tokens, plus an axe accessibility scan | Broken layout, overflow, wrong tokens, failed contrast, missing focus or loading states, a clear mockup mismatch. Taste is a note |

`user` and `visual` have `browser: true` in `factory.json`. A reviewer may write only its own review file; the guard enforces this by agent type.

**Milestone walkthrough.** Every `walkthrough_every` merged UI features (default 5), and once when nothing is left to build, the organiser runs each browser reviewer on the whole app on the main branch. Findings go to `progress.md` and the report as needs-human items. Features can pass alone and still fail together.

## Components

The plugin ships skills, agents, scripts and hooks. Permissions depend on each project's stack, so setup writes them into each project.

**Skills** (all `disable-model-invocation: true`, so only you start them)

| Skill | Does |
| --- | --- |
| `/harness:new` | The one start command. Runs the intake, then follows the three parts below |
| `questions` | The intake list; tags each question TECHNICAL or PREFERENCE; sends technical ones to the critic |
| `setup` | Writes CLAUDE.md, permissions, `harness.json`, rule files and a skeleton for the chosen stack |
| `init-build` | Turns the spec into `feature_list.json` with steps and dependencies, and writes `build.cmd` |
| `owner` | Creates your standing preferences, only when no master copy exists |
| `architecture` | Records the architecture as decisions and `docs/architecture.md`; also preloaded into the code reviewer |
| `/harness:approve <id>` | Merges a needs-human job (tests must pass), sets it done, commits |
| `/harness:rework <id> <note>` | Saves your note in the job folder and sets the job to rework; the next session starts a fresh builder with it |
| `/harness:report` | Progress by status, needs-human jobs with the command to act, walkthrough findings, cost per session, three builder transcripts, provisional decisions, failures |
| `/harness:smoke` | Tests the plugin itself (see below) |

**Agents**

| Agent | Model | Job |
| --- | --- | --- |
| organiser | opus | Runs one build session: preflight, picks jobs, runs the line, merges, writes `progress.md`. Never edits code |
| test-writer | opus | Acceptance tests before the build |
| builder | sonnet (opus in round 2) | One feature in its worktree |
| reviewer, security, user-tester, visual | see the reviewers table | Review files only |
| resolver | inherit | Answers questions from spec, `owner.md`, decision rules, then quoted sources; has `memory: project` |
| critic | opus | Checks every technical recommendation in the intake |

**Scripts**

| Script | Does |
| --- | --- |
| `build.py` | The build loop |
| `gates.py`, `risk.py` | The checks of the line |
| `status.py <id> <status>` | The only way to change `status`; `done` also sets `passes` true |
| `mark_pass.py` | Flips `passes` (still allowed by the guard) |
| `guard.py` | The PreToolUse hook |
| `run_tests.py`, `reinject.py`, `stop_failure.py` | Hook scripts |

**Hooks** (in `hooks/hooks.json`)

| Event | Does |
| --- | --- |
| `Stop` | Runs the project's test command; blocks on failure; warns at 80% of the time limit |
| `SubagentStop` (builder) | Same, so a builder can't finish with red tests |
| `PreToolUse` on Edit, Write, Bash | Blocks any change to `feature_list.json` except `status.py` and `mark_pass.py`; blocks protected paths; blocks the builder from the acceptance folder; limits each reviewer to its own review file |
| `SessionStart` (compact) | Re-injects the spec summary, rules and current feature after compaction |
| `StopFailure` | Appends the error to `progress.md` so a rerun knows why it stopped |

## State files

| File | Holds |
| --- | --- |
| `docs/owner.md` | Your standing preferences |
| `docs/spec.md`, `docs/decisions.md`, `docs/architecture.md` | What to build; D-numbered decisions; decision rules |
| `docs/design/` | `mockup.html` and `tokens.md` for UI apps |
| `feature_list.json` | Every feature, `steps`, `depends_on`, `ui`, `status` (todo, building, review, rework, needs-human, done), `passes` |
| `.harness/jobs/<id>/` | The job's trail: `brief.md`, `acceptance.sha`, `gates-<round>.md`, `round-<n>/review-*.md`, `decision.md`, an optional owner note |
| `.harness/wt/<id>/` | The job's worktree (git-ignored) |
| `progress.md` | One entry per session: jobs, tests, needs human, provisional decisions |
| `build-log.jsonl` | The raw output of every session; the source of cost figures |
| `.claude/harness.json` | `test`, `plugin_root`, and optional `max_builders` (2), `gates`, `risky`, `acceptance_dir`, `walkthrough_every` (5), `run`, `test_limit_s` (300) |
| `build.cmd` | Runs `build.py`; rerunnable |

## Running it

`build.cmd` runs `python <plugin_root>/scripts/build.py`. The script loops:

1. Start a fresh `claude -p --agent harness:organiser "Run the next jobs"` session, with auto permission mode and no prompts. Append its output to `build-log.jsonl`.
2. The session does a **preflight**: tests pass on the main branch and the app's `run` command starts. If not, it records why and ends.
3. It takes up to `max_builders` ready jobs through the line to done or needs-human, runs a walkthrough if one is due, writes `progress.md`, and ends.
4. `build.py` stops when no feature is ready, or when two sessions in a row change nothing. It prints `feature_list: N/M done, K needs-human`.

A feature is ready when it is todo or rework, its dependencies are done, and it is not `owner-writes`. Features left `building` or `review` by a crashed session count as ready too, so the next session picks them up.

`/goal` is no longer used. Each session is fresh and works from the files, so a crash or a usage limit costs one session, not the build. Setup also denies `git push`, because auto mode would push.

## Cost estimate

These are estimates from list prices, not measured. The research report estimates about $2.90 a feature for this pipeline, against $5 to $9 for the four-reviewer panel with an approver. The UI figure is our own addition, covering the two browser reviewers. The first real proof run will replace both.

| Feature | Estimate | Main parts |
| --- | --- | --- |
| Non-UI | about $2.90 | Test writer $0.40, builder $1.20, code review $0.45, security lens $0.20 (expected), rework $0.45, organiser $0.20 |
| UI | about $3.40 | The above plus the user tester and the visual reviewer, about $0.50 together |

A 40-feature project is then roughly $115 to $135 at API prices. `/harness:report` shows the real cost per session from `build-log.jsonl`.

## Limits

- **Accounts and keys.** The factory can't create accounts or hold your keys. A feature that needs them is marked `owner-writes` and waits for you.
- **Deployment is not covered.** It ends at a merged, tested app on your machine. You push and deploy.
- **Memory.** On 8 GB the default is 2 jobs at a time. Test suites run one at a time.
- **One browser at a time.** Browser reviewers of a job run in turn, and the walkthrough runs them one by one.
- **Review is not proof.** A reviewer can miss things. The tests, the gates, the risk rule and your needs-human list are the safety net.

## Testing the harness itself

The factory is only worth having if it beats plain Claude Code, so it gets its own checks.

1. **Python tests** (`python -m pytest -q`) cover the scripts, the guard, `factory.json` and the agent files.
2. **Skill and agent evals** with `claude plugin eval`: each case is a prompt plus graders, run with and without the plugin. Cases today: `questions`, `init-build`, `resolver`.
3. **`/harness:smoke`** tests the plugin, not each project, and runs when the plugin changes. It runs the line on a two-feature mini-spec, checks that a headless subagent can take and read a Playwright screenshot, and checks that a resumed builder still works in its `.harness/wt/<id>` folder. Projects get the preflight instead.
4. **A proof run**: a 15 to 20 feature app built end to end. It is billed and long, so it follows the build rather than being part of it.

Measures to record per run:

| Measure | Target |
| --- | --- |
| Features done at the end | 100% (needs-human jobs count against this) |
| Your minutes before the build | 10 to 15 |
| Needs-human jobs | Few |
| Provisional decisions you changed afterwards | Few, and falling |
| Reruns needed to finish | 0 or 1 |
| Cost per feature | Near the estimate above |

## Dropped or deferred

A per-feature spec-writer (the intake and the test writer cover it); a fixed four-reviewer panel on every feature; an AI approver; `/code-review` in the loop (the code reviewer does it); `board.json` and an HTML dashboard (the report and job folders cover them); an MCP browser server or Claude in Chrome (Playwright through Bash instead); the `brief` skill (the intake list covers it).

## Differences from the decisions

Where the code differs from D58 to D81, this doc follows the code.

1. **The guard's `status.py` pattern** accepts any lowercase status word. `status.py` itself rejects a value that is not one of the six statuses.
2. **Round 1 rework** sends "think harder" as text in the message. The research report suggests a higher effort setting; no effort setting is passed.
3. **The tamper check** (D80) also fails on uncommitted changes in the acceptance folder, even when `acceptance.sha` exists.
4. **The acceptance lock** is a substring match on the folder name in Bash commands, so it can block more than it needs to. The same is true of `risk.py`: `*auth*` matches any path containing "auth" (for example `author.md`), so it can flag more files as high risk than intended. Both are marked `ponytail:` in the code.
5. **`test_limit_s`** (default 300) is a setting the decisions do not list; gates and the Stop hook kill a command that runs longer.
6. **The UI cost of about $3.40** is not in the research report. It is the report's $2.90 plus about $0.50 for the two browser reviewers, our own figure.
7. **Design skills:** `web-design-engineer` (D88) decides the look and `ui-ux-pro-max` (D91) supplies usability rules. Both are used by the intake's design step, the builder on UI features and the visual reviewer; the user tester uses ui-ux-pro-max.
