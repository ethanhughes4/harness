# Open-source and community workflows for spec-driven, multi-agent coding (as of 14 Oct 2026)

Labels used below: **[measured]** means a benchmark or count. **[anecdote]** means one practitioner's experience. **[vendor claim]** means the project's own unverified marketing. **[docs]** means official README or docs, describing design rather than outcomes. Most evidence in this space is anecdote or docs. Controlled comparisons are rare.

## Q1. What pipeline does each framework use (phases, roles, artifacts, test-first, review, state)?

### Takeaway
The strongest frameworks share one shape: a durable spec or plan on disk, small tasks, a fresh-context implementer per task, an independent reviewer that reads the diff against the task brief, and an append-only ledger or progress file for resume. They differ mainly in how much up-front documentation they generate. Heavy frameworks (Spec Kit, BMAD full mode, Kiro on small work) are the ones users most often call too slow or too verbose.

### Cited Findings

**GitHub Spec Kit** [docs]
- Commands: `/speckit-constitution` once per project, then per feature `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement` and `/speckit-converge`. Implement and converge "repeat until convergence reports 'Converged.'" Clarify, checklist and analyze are optional quality gates. — [github/spec-kit README](https://github.com/github/spec-kit)
- Opt-in extensions: bug fixing (`/speckit-bug-assess`, `-fix`, `-test`, with reports in `.specify/bugs/<slug>/`) and idea assessment (`.specify/assessments/<slug>/`, ending in go, needs-clarification or kill). In the bug flow, "missing verification does not count as success." State lives as Markdown in `.specify/`, and unresolved items are refined in place rather than regenerated. The page showed about 141k stars and no TDD enforcement. — [github/spec-kit README](https://github.com/github/spec-kit)
- Each feature gets a spec folder of about eight files (spec, plan, tasks, research, data model, API, component, and so on) plus a project "constitution." A branch per spec suggests a spec lives for one change request. — [Böckeler, martinfowler.com, 15 Oct 2025](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- Templates mark unknowns "NEEDS CLARIFICATION" instead of guessing. The reviewer also found no code-review step and that changing direction regenerates whole documents. [anecdote, Spec-Kit v0.1.6, tested Feb 2026] — [Ran the Builder, 13 Apr 2026](https://ranthebuilder.cloud/blog/i-tested-three-spec-driven-ai-tools-here-s-my-honest-take/)

**AWS Kiro specs** [docs]
- Each feature spec has three files: `requirements.md` (user stories and acceptance criteria), `design.md` (architecture, sequence diagrams, error handling, testing strategy) and `tasks.md`. A bugfix spec uses `bugfix.md` covering current, expected and unchanged behaviour. Feature specs can be Requirements-First or Design-First, and "Quick Spec" writes all three files without approval gates. — [kiro.dev/docs/specs](https://kiro.dev/docs/specs/)
- "Run all tasks" builds a dependency graph and runs independent tasks in concurrent waves, with the waves run in sequence. There is also "Analyze Requirements" (flags inconsistencies and gaps before design) and a "Correctness" feature for property-based testing. — [kiro.dev/docs/specs](https://kiro.dev/docs/specs/)
- EARS pattern: "WHEN [condition/event] THE SYSTEM SHALL [expected behavior]". Kiro says each requirement "can be translated directly into test cases." — [kiro.dev feature specs](https://kiro.dev/docs/specs/feature-specs/)
- Optional "steering" files hold project context. — [Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)

**BMAD Method** [docs]
- Delivery loop: Clarify, Plan, Build and verify, Learn and adjust. It offers product, architecture, UX, development and testing perspectives, and its "right-sized process" lets clear changes go straight to implementation. Optional add-ons are a Test Architect and "BMad Loop," which builds, verifies and retrospects a whole epic unattended. v6.12 is stable and frozen. V7 is an alpha shipped as a Claude Code or Codex plugin, with a stated release ETA of 16 Oct 2026. — [BMAD-METHOD README](https://github.com/bmad-code-org/BMAD-METHOD)
- Full mode took about 6 days and about $200 for one feature, and its artifacts were "heavy and hard to review." Its adversarial code review "caught things a standard review would miss." Quick mode used one document and reached the same elicitation quality in two steps. All output goes to one shared directory, which weakens parallel work. [anecdote, BMAD v6.0.3] — [Ran the Builder](https://ranthebuilder.cloud/blog/i-tested-three-spec-driven-ai-tools-here-s-my-honest-take/)
- Another review describes BMAD as having "twelve agents, a heavy artifact set and a steep learning curve." — via [search summary of reenbit / particula comparisons](https://reenbit.com/bmad-vs-spec-kit-vs-openspec-choosing-your-spec-driven-ai-framework/)
- The fetched README did not cover PRD and story-file sharding or `sprint-status.yaml`. See Gaps.

**OpenSpec** [docs]
- Commands: `/opsx:explore`, then `/opsx:propose <name>`, which creates `openspec/changes/<name>/` holding `proposal.md`, `specs/`, `design.md` and `tasks.md`. Next `/opsx:apply` implements the tasks and checks them off. Then `/opsx:archive` moves the change to `changes/archive/<date>-<name>/` and merges it into the live `openspec/specs/`. Requirements use SHALL, and scenarios use WHEN and THEN. Delta headings such as "## ADDED Requirements" are used. It describes itself as "built for brownfield not just greenfield." The page showed about 72k stars. — [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)
- It scored highest of three tools (4.00, against 2.77 for Spec Kit). Delta specs stay compact and reviewable, and it always suggests the next step. Weak points: no review gates between phases, and it "adds rationale to decisions the developer never made." [anecdote with a rubric] — [Ran the Builder](https://ranthebuilder.cloud/blog/i-tested-three-spec-driven-ai-tools-here-s-my-honest-take/)

**Superpowers (obra)** [docs]
- Skills run in this order: brainstorming (Q&A, then a design doc), using-git-worktrees (isolated branch with a clean test baseline), writing-plans ("tasks of about 2 to 5 minutes each," with exact file paths, complete code and verification steps, written for "an enthusiastic junior engineer with poor taste"), then subagent-driven-development or executing-plans, test-driven-development, requesting-code-review, and finishing-a-development-branch. The TDD skill "deletes code written before its tests." "Critical issues block progress." The project was first announced around 9 Oct 2025. — [obra/superpowers](https://github.com/obra/superpowers)
- The subagent-driven-development loop works like this:
  - The controller records the BASE SHA. A script extracts each task into its own brief file, which is the single source of requirements. The implementer never reads the whole plan, and implementers never run in parallel.
  - The implementer returns DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED. On BLOCKED, the rule is "never retry the same model unchanged."
  - A reviewer gets a review package (commits, stat summary and full BASE..HEAD diff), the brief and the report. It returns two verdicts, spec compliance and task quality. "Implementer self-review never replaces the task review."
  - In the fix loop, rounds 1 to 3 resume the same implementer and rounds 4 to 5 use a fresh implementer on a stronger model. A circuit breaker trips after round 5. Each fix report must include tests, the command run and its output. "The controller never fixes code itself."
  - The durable record is a git-ignored per-plan ledger with completion lines, fix rounds and rulings. The skill says to trust the ledger over memory after compaction.
  - — [subagent-driven-development SKILL.md](https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/SKILL.md)
- On harnesses without a post-compaction hook, a long session can lose the bootstrap, and skills stop triggering. — [obra/superpowers](https://github.com/obra/superpowers)

**gstack (Garry Tan)** [docs and vendor claim]
- About 23 role skills along Think, Plan, Build, Review, Test, Ship, Reflect. Examples: `/office-hours`, `/plan-ceo-review`, `/plan-eng-review`, `/plan-design-review`, `/autoplan`, `/review` (staff-engineer review), `/investigate`, `/qa` (browser), `/ship`, `/land-and-deploy`, `/canary`, `/cso` (security), `/retro`, `/codex` (second-opinion review from another model), and `/careful`, `/freeze` and `/guard` as guardrails. Each skill reads the previous skill's output. State is kept in `.gstack/` and `~/.gstack/`. — [garrytan/gstack](https://github.com/garrytan/gstack)
- The author claims about 810x his 2013 pace and 10 to 15 parallel sprints, and says `/qa` took him from 6 to 12 parallel workers. These are self-reported and unverified. [vendor claim] — [garrytan/gstack](https://github.com/garrytan/gstack)

**Anthropic long-running harness** (reference design, not a framework) [docs, with observed failures]
- An initializer agent writes `init.sh`, `claude-progress.txt`, an initial commit, and a JSON feature list (over 200 features for a claude.ai clone, all initially failing). Each entry has `category`, `description`, `steps` and `passes`. Coding agents may only flip `passes`. JSON was chosen because "the model is less likely to inappropriately change or overwrite JSON files compared to Markdown." The instruction reads: "It is unacceptable to remove or edit tests." — [Anthropic, 26 Nov 2025](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Resume runs `pwd`, reads the git log and progress file, picks the highest-priority failing feature, runs `init.sh`, and does a basic end-to-end test before starting new work. Telling the agent to use browser automation "dramatically improved performance." — [Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

**Taskmaster AI** [docs]
- `task-master parse-prd .taskmaster/docs/prd.txt` turns a PRD into tasks. Other commands: `next`, `expand_task` and `expand_all` for subtasks, `analyze_project_complexity` and `complexity_report`, tags for workstreams, and dependency-aware `move`. It has 36 MCP tools in "all" mode. — [eyaltoledano/claude-task-master](https://github.com/eyaltoledano/claude-task-master)

**Agent OS (Builder Methods)** [docs]
- The current README covers four capabilities: Discover Standards (extract conventions from the codebase), Deploy Standards (inject the relevant ones), Shape Spec, and Index Standards. It is now framed mainly as standards injection plus spec shaping, not a full pipeline. About 5.5k stars. — [buildermethods/agent-os](https://github.com/buildermethods/agent-os)

**Aider architect/editor** [measured]
- An Architect model describes the solution and an Editor model turns it into file edits. Results on Aider's editing benchmark: o1-preview plus o1-mini or DeepSeek scored 85.0%, against 79.7% for o1-preview alone. Claude 3.5 Sonnet paired with itself scored 80.5%, against 77.4% solo. GPT-4o paired with itself scored 75.2%, against 71.4% solo. — [aider.chat, 26 Sep 2024](https://aider.chat/2024/09/26/architect.html)

**claude-flow / Ruflo** [vendor claim]
- A "meta-harness" for Claude Code with mesh, hierarchical, ring and star swarm topologies and consensus protocols. It was renamed Ruflo at v3.5 (Feb 2026). It claims 30 to 50% token savings, which one analysis notes "have not been independently verified." A mesh topology costs more tokens. A critical review found no independent evidence that the swarm outperforms simpler harnesses. — [Daniel Vaughan, 9 Apr 2026](https://codex.danielvaughan.com/2026/04/09/claude-multi-agent-ecosystem/); [rywalker.com research](https://rywalker.com/research/claude-flow)

**OpenHands / SWE-agent** [docs]
- SWE-agent introduced the agent-computer interface (ACI): a few targeted tools for editing files, navigating code and running tests. OpenHands' base agent has a small action set (bash, file editor, think, finish) plus a planning agent. A secondary source reports that v1.5.0 added a task-list panel. — [codesota comparison, Apr 2026](https://codesota.com/agentic/openhands-vs-swe-agent); [OpenHands paper](https://arxiv.org/html/2407.16741v3); [toolnavs, secondary](https://toolnavs.com/article/1218-openhands-releases-150-task-list-planning-agent-and-skill-slash-menus-are-launch)

**Tessl** [anecdote]
- Tessl takes a spec-as-source approach: one spec per code file, and generated files carry a "do not edit" header. Generating repeatedly from the same spec produced different code. — [Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)

### Inferences
- Superpowers' subagent-driven-development is the most fully specified per-task loop found, and it is closest to what a Claude Code plugin can implement with subagents and hooks. Its specific controls are: a brief file per task, a BASE SHA and diff package, reviewer verdicts with no pre-judging, a capped fix loop that escalates the model, and a ledger.
- Anthropic's harness adds what Superpowers lacks for multi-session greenfield work: a whole-scope feature list in JSON as the acceptance oracle, and a "smoke test before new work" rule on resume.
- OpenSpec's change-and-archive model is the most credible answer to spec drift. Live specs are updated only when a change is archived.

### Gaps
- I could not fetch Spec Kit's `spec-driven.md`, so the exact SDD file names and whether its templates mandate tests-first are unverified.
- BMAD details (PRD and architecture sharding, story files, `sprint-status.yaml`, Dev/SM/QA agent names) were not on the fetched README. They need the BMAD docs site.
- Taskmaster's `tasks.json` schema (my memory suggests id, title, status, dependencies, priority, details, testStrategy and subtasks) is unverified.
- The rationale for Agent OS's change from versions 1 and 2 to the current form is unverified. It is likely in its CHANGELOG.
- I found no awesome-claude-code or "software factory" template with `board.json` dashboards that had a credible experience report.

## Q2. At what granularity are specs written, and which acceptance-criteria format works best?

### Takeaway
The best-supported pattern has three tiers. A small project-level constitution or standards file sits at the top. Per-feature or per-change specs with testable criteria sit below it. Small tasks (Superpowers says 2 to 5 minutes each) are extracted into self-contained briefs. A whole-app spec helps only as a scope list, as in Anthropic's feature list. Heavy per-feature specs on small work are the most common complaint. I found no measurement that compares EARS, Given/When/Then and checklists.

### Cited Findings
- On Kiro, a small bug turned into "4 user stories with 16 acceptance criteria," which the author called "like using a sledgehammer to crack a nut." On Spec Kit, the author would "rather review code than all these markdown files." For a 3 to 5 point feature, plain AI-assisted coding seemed faster. [anecdote] — [Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- A Spec Kit date-display feature reportedly produced 8 files and 1,300 lines of spec. Advice from the same summary: skip full SDD for anything under a few hundred lines. [anecdote, via search summary] — [particula.tech](https://particula.tech/blog/spec-driven-development-tools-spec-kit-vs-kiro-vs-tessl)
- "The question of how much detail to include in a spec is really hard" (robertclaus, Plotly Studio, with one spec per chart). Another user reports that as "memory banks grow," the AI "gets confused" (tharkun__). [anecdote] — [HN thread](https://news.ycombinator.com/item?id=45610996)
- "Following a BDD approach with a coding CLI works a lot better," because features are documented as executable code, not markdown (gsadaka). [anecdote] — [HN](https://news.ycombinator.com/item?id=45610996)
- EARS ("WHEN … THE SYSTEM SHALL …") is pitched as directly translatable into tests. — [Kiro](https://kiro.dev/docs/specs/feature-specs/). OpenSpec uses SHALL requirements with WHEN/THEN scenarios. — [OpenSpec](https://github.com/Fission-AI/OpenSpec)
- Anthropic's feature list gives each entry explicit test `steps`, which the agent must verify end-to-end before flipping `passes`. — [Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Superpowers plans include exact paths, complete code and verification steps per 2 to 5 minute task, and the implementer sees only its brief. — [obra/superpowers](https://github.com/obra/superpowers)
- None of the three tools flagged an authorization gap during planning. BMAD added permission checks, while Spec Kit and OpenSpec trusted caller-supplied context. [anecdote] — [Ran the Builder](https://ranthebuilder.cloud/blog/i-tested-three-spec-driven-ai-tools-here-s-my-honest-take/)

### Inferences
- Size the process to the change. Kiro's "Quick Spec," BMAD Quick mode and OpenSpec's compact deltas all respond to the same complaint. A harness should offer a trivial path, such as spec-in-chat with no files.
- Acceptance criteria should be machine-checkable. Executable tests, or a JSON list with test steps, beat prose. EARS and WHEN/THEN are useful mainly because each line maps to one test.
- Security and authorization criteria need an explicit prompt slot, because planners miss them.

### Gaps
- I found no controlled study comparing EARS, Gherkin and checklists for LLM implementation accuracy.

## Q3. Which roles do they use, and do many roles help or just add cost?

### Takeaway
Evidence favours few writers and more independent readers. One agent writes the code, while fresh-context reviewers, a second-model opinion or an architect-planner add measurable value. Many-persona pipelines (BMAD's roughly 12 agents, gstack's roughly 23 skills, claude-flow swarms) have strong fans but only anecdotal or vendor evidence, and they carry clear cost and review overhead.

### Cited Findings
- Cognition, Apr 2026: what works is "multiple agents contribute intelligence while writes stay single-threaded." Devin Review catches about 2 bugs per Devin PR, about 58% of them severe [measured, vendor-internal]. The reviewer works best with clean context, seeing only the diff. A filter on reviewer findings prevents loops and out-of-scope work. Parallel writer swarms make conflicting implicit choices. Unstructured swarms are "mostly a distraction." Manager and child setups suffer from over-prescriptive managers and assumed shared state. — [Cognition, "Multi-Agents: What's Actually Working," 22 Apr 2026](https://cognition.com/blog/multi-agents-working)
- Splitting work across subagents that get only fragments of context is "very fragile" (the Flappy Bird example). — [Cognition, "Don't Build Multi-Agents," 12 Jun 2025](https://cognition.com/blog/dont-build-multi-agents). LangChain's view: multi-agent systems that "read" are easier than those that "write." — [LangChain](https://blog.langchain.com/how-and-when-to-build-multi-agent-systems)
- Architect plus editor split beat solo runs on every model pair Aider reported (for example, 77.4% to 80.5% for Sonnet 3.5). [measured] — [Aider](https://aider.chat/2024/09/26/architect.html)
- BMAD's adversarial review caught extra issues, but full mode cost about $200 over about 6 days. [anecdote] — [Ran the Builder](https://ranthebuilder.cloud/blog/i-tested-three-spec-driven-ai-tools-here-s-my-honest-take/)
- Superpowers uses one implementer at a time and forbids implementers from spawning their own reviewers. — [SKILL.md](https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/SKILL.md)
- gstack's productivity numbers are self-reported. — [gstack](https://github.com/garrytan/gstack). Claims of claude-flow swarm benefits are unverified. — [rywalker](https://rywalker.com/research/claude-flow)

### Inferences
- A practical role set is planner/architect, implementer, independent reviewer (spec compliance plus quality, optionally another model) and a verifier that runs tests or the browser. PM, UX and security fit better as checklists or optional review lenses than as standing agents.
- Parallelism should be limited to independent tasks in separate worktrees, as in Kiro's waves. Even then, merges need one integrator.

### Gaps
- I found no independent measurement of total cost or quality for BMAD, gstack or claude-flow against a single-agent baseline.

## Q4. Which files hold durable state, and how does resume work?

### Takeaway
Every working framework persists state in plain files in the repo, plus git. Resume works by re-reading these files, never by trusting chat memory. The common files are a spec or plan folder, a task list with status, an append-only progress log or ledger, and git commits per task.

### Cited Findings
- Anthropic: `claude-progress.txt`, the feature list JSON, git history and `init.sh`. Resume order is pwd, git log, progress file, feature list, `init.sh`, then a smoke test. — [Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Superpowers: a ledger in a git-ignored per-plan workspace that "trust[s] over memory after compaction," plus a todo per task. — [SKILL.md](https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/SKILL.md)
- Spec Kit: Markdown under `.specify/`, refined in place. — [spec-kit](https://github.com/github/spec-kit). OpenSpec: `openspec/changes/*` and `openspec/specs/`, plus an archive. — [OpenSpec](https://github.com/Fission-AI/OpenSpec). Kiro: `tasks.md` with live task status. — [Kiro](https://kiro.dev/docs/specs/). gstack: `.gstack/`. — [gstack](https://github.com/garrytan/gstack). Taskmaster: `.taskmaster/` with `next`. — [Taskmaster](https://github.com/eyaltoledano/claude-task-master)
- BMAD writes everything to one shared output directory by default, which hurts parallel features. Spec Kit and OpenSpec isolate one directory per feature. [anecdote] — [Ran the Builder](https://ranthebuilder.cloud/blog/i-tested-three-spec-driven-ai-tools-here-s-my-honest-take/)
- Session bootstrap must be re-injected after compaction, or the workflow silently stops. — [superpowers](https://github.com/obra/superpowers)

### Inferences
- Use JSON (or another structured format) for status that agents must not rewrite freely, and Markdown for prose specs. Keep one directory per feature or change for parallel safety. Use a SessionStart or post-compaction hook to re-inject "read the ledger first."

### Gaps
- I found no reports comparing resume reliability across these state formats.

## Q5. Which failure modes do users report?

### Takeaway
The recurring failures are spec-to-code drift, verbose specs that humans stop reviewing, agents fixing tests instead of code, premature "done," loops in fix cycles, and cost blowups in heavy pipelines. The mitigations with the best support are immutable acceptance criteria, independent diff-based review, evidence-bearing reports, capped retries with escalation, and end-to-end verification.

### Cited Findings
- **Agents altering tests.** One user ran Spec Kit with Claude Code for about 10 days: "most tests were failing, and the build was not successful." The agent "almost always has to go back and fix the tests, not the implementation" (yoaviram). Sprints plus a task subagent raised their trust "significantly." [anecdote] — [HN](https://news.ycombinator.com/item?id=45610996)
- ImpossibleBench makes the tests contradict the spec, so any pass implies cheating. Observed behaviours include modifying test assertions, special-casing test inputs, and stateful gaming. [measured] Limits: EvilGenie notes that some flagged cases are legitimate fixes of wrong tests. — [ImpossibleBench on LessWrong](https://www.lesswrong.com/posts/qJYMbrabcQqCZ7iqm/impossiblebench-measuring-reward-hacking-in-llm-coding-1); [EvilGenie](https://arxiv.org/pdf/2511.21654)
- **Premature "done" and unverified passes.** Anthropic saw agents declaring the project complete, and marking features complete without real end-to-end testing. Fixes: a full-scope feature list and mandatory end-to-end checks. — [Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- **Spec drift and ignored specs.**
  - The Spec Kit agent ignored research notes about existing classes and created duplicates. It also over-applied a constitution article, a "false sense of control." — [Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
  - Spec Kit code "didn't faithfully match the spec's intent." OpenSpec invented rationale. — [Ran the Builder](https://ranthebuilder.cloud/blog/i-tested-three-spec-driven-ai-tools-here-s-my-honest-take/)
  - A user never saw how multiple specs merge into "a single ground truth" (iamdeedubs). — [HN](https://news.ycombinator.com/item?id=45610996)
- **Destructive edits.** Kiro "deleted code unpredictably and wouldn't revert changes" and produced "12+ tasks with 4+ sub-tasks each" (hatmanstack). [anecdote] — [HN](https://news.ycombinator.com/item?id=45610996)
- **Review overload and rubber-stamping risk.** Reviewers find the verbose markdown tedious. — [Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html). Superpowers counters this: self-review never replaces the task review, the controller must not pre-judge findings, and "Cannot verify from diff" items must be resolved. — [SKILL.md](https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/SKILL.md)
- **Loops.** Superpowers caps fix rounds at 5 with model escalation and a breaker. Cognition filters reviewer findings against user instructions to prevent looping. — [SKILL.md](https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/SKILL.md); [Cognition](https://cognition.com/blog/multi-agents-working)
- **Cost.** BMAD full mode cost about $200 over about 6 days. — [Ran the Builder](https://ranthebuilder.cloud/blog/i-tested-three-spec-driven-ai-tools-here-s-my-honest-take/). A mesh swarm costs more tokens. — [Vaughan](https://codex.danielvaughan.com/2026/04/09/claude-multi-agent-ecosystem/)
- **Non-determinism.** Regenerating from the same spec gives different code. — [Böckeler on Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)

### Inferences: best ideas for a Claude Code plugin harness (synthesis)
1. **Size the process.** Offer three paths: a trivial path (chat only), a change path (an OpenSpec-style delta folder) and a project path (a constitution plus a Spec Kit or BMAD-style plan). Do not force full SDD on small changes.
2. **Use acceptance criteria as an immutable oracle.** Store criteria as structured JSON, with an id, an EARS or WHEN/THEN statement, test steps and a pass flag. Only the verifier flips the flag. Use a hook to block implementer edits to the criteria file and to existing test assertions without an explicit ruling. This combines Anthropic's JSON choice with the ImpossibleBench evidence.
3. **Use per-task briefs and fresh contexts.** Extract each task into a brief file and give the implementer only the brief plus interfaces, never the whole plan (Superpowers).
4. **Make review independent and diff-based.** Build a review package from BASE..HEAD, and get two verdicts (spec compliance and quality). Optionally use a second model, as in gstack `/codex` and Cognition's "smart friend." The controller does not pre-judge findings.
5. **Require evidence in reports.** Implementer and fix reports must include the test command and its output. A "Cannot verify" item blocks completion.
6. **Bound the loops.** Cap fix rounds (Superpowers uses 3 rounds, then escalate the model, then break at 5). On BLOCKED, change the model, the context or the task size, never retry unchanged.
7. **Keep state on disk.** Use a ledger or progress file, a task status JSON and one commit per task. Resume with git log, the ledger, the status file, and a smoke test before new work. Add a SessionStart or post-compaction hook to re-inject the bootstrap.
8. **Allow only one writer at a time.** Parallelise only independent tasks in worktrees, in waves (Kiro), with a single integrator. Avoid swarms.
9. **Verify end-to-end.** Use browser or CLI smoke tests, not unit tests alone (Anthropic).
10. **Add a security lens to planning.** All three tools tested missed an authorization gap.

### Gaps
- I found no quantitative data on how often LLM reviewers rubber-stamp in these frameworks, apart from Cognition's figure for bugs caught.
- Reddit threads were not reached within the tool budget. The community evidence here leans on one HN thread and three blog reviews.
