# Project Harness: Design

Oct 8, 2026 · @Ethan Hughes

A Claude Code plugin that takes any new project from brief to working app: you answer questions for about an hour, then it builds headless until every feature passes.

## What it takes from the research

The harness combines four proven sources: Anthropic's long-running agent harness, Claude Code's own features, two popular open-source workflows, and what worked or failed in the FPL build.

| Idea | Where it comes from | What it does in our harness |
| --- | --- | --- |
| `feature_list.json`, all features start failing, agents may only flip `passes` | [Anthropic harness](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents) | The build can't finish by quietly dropping work |
| Progress log + git commits + one start script | Anthropic harness | Any session can resume where the last one stopped |
| `/goal` with a separate model judging "done" | [Claude Code docs](https://code.claude.com/docs/en/goal) | Runs headless until every feature passes |
| Project principles written once (a "constitution") | [GitHub Spec Kit](https://codemyspec.com/blog/github-spec-kit-guide) | `owner.md` answers preference questions mid-build |
| Clarify and consistency-check gates before building | Spec Kit | A critic agent checks every recommended answer |
| Tests first, then code | [Superpowers](https://pasqualepillitteri.it/en/news/215/superpowers-claude-code-complete-guide) | Builders write the failing test before the feature |
| Workers report DONE, DONE\_WITH\_CONCERNS, BLOCKED or NEEDS\_CONTEXT | Superpowers | The organiser knows exactly what to do with each result |
| Review in a fresh context: spec first, then quality | Superpowers; [Claude Code best practices](https://code.claude.com/docs/en/best-practices) | The reviewer never grades its own work |
| End-to-end checks as a real user would | Anthropic harness | Web apps get a browser check, not just unit tests |
| One organiser, 3 to 5 workers in parallel | [Anthropic multi-agent research](https://www.anthropic.com/engineering/multi-agent-research-system) | Capped at 3 builders on an 8 GB PC |
| File guards before any edit | [Community workflows](https://github.com/ithiria894/awesome-claude-code-workflows) | `PreToolUse` hooks protect the feature list and raw data |
| Re-inject key context after compaction | [Claude Code hooks guide](https://code.claude.com/docs/en/hooks-guide) | Long runs don't forget the rules |
| Plugin evals with a no-plugin baseline | [Claude Code plugin evals](https://code.claude.com/docs/en/plugin-evals) | Proves the harness beats plain Claude Code |
| Resolver with quoted sources, D-numbered decisions, provisional answers | FPL build | Questions get answered without stopping the run |
| Graders that print exactly what failed; hook timing warnings | FPL build | Silent failures get caught |

## Design principles

Six rules decide every part of the design:

1. **People decide, machines build.** Your time goes into the brief, the questions and your preferences. Everything after that runs without you.
2. **State lives in files.** The feature list, progress log, decisions and git history are the memory. Any session, or a rerun after a crash, picks up from them.
3. **Every check that can be a script is a script.** Tests, file guards and timing are hooks. Agents only do work that needs judgement.
4. **Nothing grades its own work.** Builders don't review themselves, the reviewer sees only the diff and the spec, and a separate model judges when the build is done.
5. **Decide in advance what results mean.** Decision rules ("if X scores under Y, switch to Z") let the build act on eval results without asking you.
6. **Never stop for a question; never hide one.** Unanswered questions get the recommended answer, marked provisional, and listed for you at the end.

## Lifecycle of a new project

About an hour of your time at the start, then a headless build, then you check and ship.

| # | Step | Command | Mode | Output |
| --- | --- | --- | --- | --- |
| 1 | New folder, `git init`, `claude` | — | You | Empty repo with the plugin enabled |
| 2 | Write the brief | `/harness:brief` | Interactive | `docs/brief.md`: problem, user, must-nevers, out of scope |
| 3 | Check your standing preferences | `/harness:owner` | Interactive | `docs/owner.md`, copied from your last project and updated |
| 4 | Questions for the whole app; the critic fixes technical answers; you answer only preference questions | `/harness:questions` | Interactive | `docs/spec.md`, `docs/decisions.md`, decision rules |
| 5 | Write the project's own setup; you review it | `/harness:setup` | Interactive | CLAUDE.md, permissions, test hook, rule files, skeleton, one passing test |
| 6 | Smoke test the setup | `/harness:smoke` | Headless | Proof hooks block, nothing waits on a prompt, a stopped run resumes |
| 7 | Turn the spec into features | `/harness:init-build` | Headless | `feature_list.json`, `progress.md`, first commit |
| 8 | Build until every feature passes; rerun if it stops | `build.cmd` | Headless | The app, one commit per feature |
| 9 | Read the report, confirm provisional decisions, use it, push | `/harness:report` | You | Shipped |

For an existing repo like FPL, skip steps 1 to 3 and start each new stage at step 4.

## Components

The plugin ships skills, agents and hooks. Permissions depend on each project's stack, so `/harness:setup` writes them into each project.

**Skills** (all `disable-model-invocation: true`, so only you start them)

| Skill | Does |
| --- | --- |
| `brief` | Interviews you for the problem, user, must-nevers and out of scope |
| `owner` | Creates or updates your standing preferences |
| `questions` | Asks everything for the spec with recommended answers, tags each TECHNICAL or PREFERENCE, sends technical ones to the critic, shows you only preference questions and critic changes |
| `setup` | Writes CLAUDE.md, permissions, test hook command, rule files and a skeleton for the chosen stack |
| `smoke` | Runs a two-feature build to prove the setup works |
| `init-build` | Turns the spec into `feature_list.json` with acceptance steps and dependencies |
| `report` | Summarises progress, provisional decisions, eval results and failures |

**Agents**

| Agent | Model | Tools | Job |
| --- | --- | --- | --- |
| organiser | opus | Agent, Read, Grep, Glob, Bash | Runs each turn of the loop; never edits code |
| builder | sonnet | Read, Edit, Write, Grep, Glob, Bash | One feature, test first, own worktree; reports DONE, DONE\_WITH\_CONCERNS, BLOCKED or NEEDS\_CONTEXT |
| reviewer | opus | Read, Grep, Glob, Bash (read-only) | Checks a merged wave against the spec, then quality; real gaps only |
| resolver | inherit | Read, Grep, Glob, WebSearch, WebFetch | Answers questions from spec, `owner.md`, decision rules, then quoted sources; has `memory: project` |
| critic | opus | Read, Grep, Glob, WebSearch, WebFetch | Checks every technical recommendation in `questions` against CLAUDE.md, rules, decisions and docs |

**Hooks** (in the plugin's `hooks/hooks.json`)

| Event | Does |
| --- | --- |
| `Stop`, `SubagentStop` | Runs the project's test command; blocks on failure; warns at 80% of the time limit |
| `PreToolUse` on Edit/Write | Blocks any change to `feature_list.json` except flipping `passes`; blocks edits to raw data |
| `SessionStart` (compact) | Re-injects the spec summary, rules and current feature after compaction |
| `StopFailure` | Appends the error to `progress.md` so a rerun knows why it stopped |

**Project files the harness creates**

| File | Holds |
| --- | --- |
| `docs/brief.md` | The problem, in your words |
| `docs/owner.md` | Your standing preferences |
| `docs/spec.md`, `docs/decisions.md` | What to build; D-numbered decisions; decision rules |
| `feature_list.json` | Every feature, acceptance steps, `depends_on`, `passes` |
| `progress.md` | One entry per turn: built, checked, decided, failed |
| `build.cmd` | The headless `/goal` command, rerunnable |

## Specialist skills

General agents produce generic work, so the harness preloads specialist skills into the agents that need them, using the subagent `skills` field. Each one runs at the phase where it changes the outcome.

| Area | Skill | Source | Used in | Produces |
| --- | --- | --- | --- | --- |
| Visual direction | `frontend-design` | [Anthropic](https://claudemarketplaces.com/skills/anthropics/claude-code/frontend-design) | Questions phase, ui-builder | A committed aesthetic: type, colour system, motion; no default fonts or purple gradients |
| UX and accessibility | `ui-ux-pro-max` | [Community](https://claudemarketplaces.com/skills/nextlevelbuilder/ui-ux-pro-max-skill/ui-ux-pro-max) | ui-builder, ui-reviewer | Palettes and font pairings; checks for contrast, focus states, touch targets, loading states |
| System design | `architecture` (our own, based on [architecture-designer](https://tessl.io/registry/skills/github/jeffallan/claude-skills/architecture-designer)) | Ours | Questions phase, reviewer | `docs/architecture.md`: requirements, non-functional needs, chosen pattern with trade-offs, a diagram, risks |
| Code review | `/code-review` | Bundled with Claude Code | Reviewer | Bug findings on each wave's diff |

**Where they change the flow**

1. **Questions phase gains two outputs.** The architecture skill writes `docs/architecture.md` with its trade-offs recorded as D-numbered decisions. For apps with a UI, the design skill produces a mockup you approve, saved in `docs/design/` with its colour and type tokens.
2. **Two new agents.** A `ui-builder` (builder with both design skills preloaded) takes features tagged UI. A `ui-reviewer` opens the running page in a browser, screenshots it, compares it with the approved mockup, and runs the UX checks.
3. **The architecture is a reviewer input.** The reviewer flags code that breaks a decision in `docs/architecture.md`.

**Rules for adding outside skills**

- Read every file of a third-party skill before adding it; skills can run scripts as you.
- Copy the version you reviewed into the plugin, and keep its licence, so updates elsewhere can't change your build.
- Only `disable-model-invocation` skills cost nothing per turn; others add their description to every turn, so keep the set small.
- Each specialist skill gets a plugin eval against the no-skill baseline. A UI case, for example: build the same page with and without the design skills, and have a judge score both screenshots against a rubric for generic AI look.

## The headless build loop

Each turn takes the next features from `feature_list.json` through build, test, review and evals, then records the result in files, so a crash or a usage limit costs one turn, not the build.

&#91;embedded content: headless build loop · 6 steps per turn\]

The reviewer is the step that catches what tests can't: a feature built to the wrong spec.

- **Questions during the loop** go to the resolver, which checks the spec, `owner.md`, the decision rules and the docs, in that order. Anything still open gets the recommended answer, recorded as PROVISIONAL.
- **A BLOCKED builder** gets one retry with the resolver's answer; after that the feature is skipped and logged, and features that depend on it wait.
- **The run command** (in `build.cmd`):

```
claude -p "/goal Every feature in feature_list.json has passes true and all test suites pass, or stop after 200 turns" --permission-mode auto --permission-prompts none --output-format stream-json --verbose >> build-log.jsonl
```

## Testing the harness itself

The harness is only "insanely good" if it measurably beats plain Claude Code, so it gets its own evals.

1. **Skill and agent evals** with `claude plugin eval`. Each case is a realistic prompt plus graders, run three times with the plugin and three times without. The difference is what the harness adds. Starter cases:
   - `questions` tags preference questions correctly and the critic catches a planted technical mistake
   - `init-build` turns a short spec into features with acceptance steps and no missing requirement
   - The feature-list hook blocks a deleted feature
   - The resolver answers a preference question from `owner.md` without escalating
2. **Two reference projects**, built end to end headless after every harness change:
   - A small Python CLI app (fast, tests the core loop)
   - A small React page with a data file (tests the browser check)
3. **Harness metrics** recorded per run, in `results/`:

| Measure | Target |
| --- | --- |
| Features passing at the end | 100% |
| Your minutes before the build | Under 60 |
| Questions you had to answer | Preference questions only |
| Provisional decisions you changed afterwards | Few, and falling |
| Reruns needed to finish | 0 or 1 |
| Reviewer gaps found after the build | 0 |

## Build plan

The harness gets built with the pipeline you already have, in its own repo, in five phases. Each phase ends with something you can run.

| Phase | Builds | Done when |
| --- | --- | --- |
| 1. Skeleton | Plugin repo, manifest, the FPL agents and skills made general (no FPL details) | `claude --plugin-dir .` loads it and `/harness:questions` runs |
| 2. New parts | `brief`, `owner`, critic, `setup`, `init-build`, `smoke`, `report`, organiser loop, hooks, `build.cmd` | Each has a passing test or eval case |
| 3. First reference project | Python CLI app built fully headless | Every feature passes with 0 or 1 reruns |
| 4. Prove it | `claude plugin eval` with the no-plugin baseline; React reference project | The harness beats the baseline on every starter case |
| 5. Use it | Install at user scope; run FPL stage 6 through it | Stage 6 ships with only preference questions asked |

**Getting started**

1. Create `C:\Users\User\source\repos\harness`, run `git init`, and push it to GitHub.
2. Export this doc as Markdown and save it in the new repo as `docs/design.md`.
3. Copy the FPL repo's `.claude` folder into the new repo, so `/questions`, `/plan-stage`, `/run-plan` and the agents are there to build with.
4. Open a terminal in the new repo, type `claude`, and paste:

```
This repo will become a Claude Code plugin called "harness". The
design is in docs/design.md; read it in full first. Also read the
current docs on plugins, subagents, hooks, skills, headless mode and
/goal at code.claude.com/docs, and check every file format and
frontmatter field against them.

Run /questions harness for phase 1 and phase 2 of the build plan.
Ask only what the design and docs don't settle. Give all questions
in one list with a recommended answer each, and mark each one
TECHNICAL or PREFERENCE. I'll change only the ones I disagree with.

The .claude folder here is copied from my FPL project. Treat it as
the starting point to generalise, not as finished: anything
FPL-specific must go.
```

Then `/plan-stage harness` and `/run-plan harness` as usual. From phase 3 on, the harness builds its own reference projects.

## Sources

- [Anthropic: Effective harnesses for long-running agents](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Anthropic: How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Claude Code: Plugins overview](https://code.claude.com/docs/en/plugins)
- [Claude Code: Test plugins with evals](https://code.claude.com/docs/en/plugin-evals)
- [Claude Code: /goal](https://code.claude.com/docs/en/goal)
- [Claude Code: Dynamic workflows](https://code.claude.com/docs/en/workflows)
- [Claude Code: Hooks guide](https://code.claude.com/docs/en/hooks-guide)
- [Claude Code: Subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code: Best practices](https://code.claude.com/docs/en/best-practices)
- [GitHub Spec Kit guide (CodeMySpec)](https://codemyspec.com/blog/github-spec-kit-guide)
- [Superpowers guide](https://pasqualepillitteri.it/en/news/215/superpowers-claude-code-complete-guide)
- [Awesome Claude Code workflows](https://github.com/ithiria894/awesome-claude-code-workflows)

The Spec Kit and Superpowers pages are third-party write-ups, and their performance figures are self-reported.
