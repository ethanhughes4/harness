# Commercial autonomous coding agent pipelines (as of Oct 2026)

Scope note: about 20 tool calls. Primary sources were fetched for Devin, GitHub Copilot coding agent, Cursor Bugbot, OpenAI Codex code review and cloud, Factory Missions, Replit Agent 3 and Jules. Amp is covered only through its own news page plus secondary coverage. Sources are vendor material unless marked otherwise. Treat every number as **self-reported** unless it says "independent".

## Q1: How does a task go from request to merged change, product by product?

### Takeaway
Every product follows the same basic steps: take the task, optionally make a plan the human approves, build in an isolated cloud sandbox or VM on a branch, self-verify with tests (and for app builders, a browser), then open a PR for a human to merge. None of these products advertises auto-merge. They differ mainly in how heavy the planning step is (Factory Missions has the heaviest), whether a reviewer pass runs before the PR opens (Copilot self-review), and whether verification drives a real UI (Replit, Factory user-testing validators).

### Cited Findings

**Factory (Droids / "software factory" / Missions)**
- Droid workflow as described by an aggregator: it "explores the repository, creates a plan, edits files, runs commands and tests, inspects failures, revises its work, and submits a diff or pull request for human approval". The same runtime is exposed through desktop/web, CLI and a TS/Python SDK, plus connectors to Slack, Linear, GitHub, Sentry and others. — [rywalker.com research (secondary)](https://rywalker.com/research/factory-ai)
- Factory's own framing: the "software factory" makes delivery "repeatable and measurable". — [Factory articles index](https://factory.com/articles) (article: [what-is-a-software-factory](https://factory.ai/articles/what-is-a-software-factory))
- Missions (long, multi-feature work) has three roles. "Orchestrators handle planning, workers handle implementation, and validators handle verification." The orchestrator splits the project into milestones. At each milestone, validation reviews the accumulated work, runs tests and checks for regressions. If validation finds issues, the orchestrator "creates follow-up work to fix them before moving on". — [Factory Missions docs (search summary)](https://docs.factory.ai/missions/overview); [Factory news: Missions](https://factory.ai/news/missions)
- There are two kinds of validator. "Scrutiny" validators cover tests, lint and code review; "user testing" validators interact with the live application. The validation contract is defined before coding starts, to prevent drift. — [Factory docs / ZenML LLMOps summary](https://zenml.io/llmops-database/multi-agent-software-development-system-with-extended-autonomous-execution)
- Planning is "a conversation, not a one-shot prompt". The plan has to be approved before execution. Each milestone "represents a meaningful checkpoint". During execution the mission "runs user-facing QA testing against your application to validate each feature and self-correct as it goes". "Without [a scriptable way to exercise the app], the mission cannot reliably verify its own work." — [Factory Missions overview](https://docs.factory.com/missions/overview)
- Human involvement in Missions: "Missions are not fire-and-forget." The user can pause the orchestrator, "describe what you are seeing in plain language, and ask it to recover". The docs have a troubleshooting entry for a "feature retry limit warning", but the limit itself is not documented. — [Factory Missions overview](https://docs.factory.com/missions/overview)
- Parallelism is treated as an open question. The docs ask "Is parallelization necessary?", and Factory says it is testing whether parallel agents beat sequential ones. On cost: "More planning and validation means higher cost but potentially better output." The suggested scope is about 1 to 500 features per Mission. Repos should be at "Agent Readiness Level 4 (Optimized) or above" (tooling: `/readiness-report`, `/readiness-fix`). — [Factory Missions overview](https://docs.factory.com/missions/overview)
- Missions can run on persistent remote machines in the background. Mission Control lets the user pick separate models for the orchestrator, worker and validator. — [Factory docs: running in app](https://docs.factory.ai/missions/running-app.md)
- The longest recorded mission ran 16 days, and Factory believes 30-day missions are achievable. This comes from a third-party transcript of a talk by Luke Alvoeiro (Factory). — [SozAI transcript](https://sozai.app/transcript/multi-agent-architecture-luke-alvoeiro-factory/index.md)

**Devin (Cognition)** — the 2025 performance review, dated Nov 14, 2025
- The target task size is work that would take a junior engineer 4 to 8 hours. Devin "does best with clear requirements" and "usually performs worse when you keep telling it more after it starts the task", so scope has to be set up front. — [Cognition blog](https://cognition.com/blog/devin-annual-performance-review-2025)
- Fleet pattern: humans write a playbook (for example, a unit-testing playbook covering a few hundred repos). A fleet of Devins executes it; Cognition calls Devin "infinitely parallelizable". Code owners then check the logic. Devin also does first-pass code review, but "Human review is still necessary, because code quality is not straightforwardly verifiable." — [Cognition blog](https://cognition.com/blog/devin-annual-performance-review-2025)
- The post does not describe isolation. — [Cognition blog](https://cognition.com/blog/devin-annual-performance-review-2025)

**GitHub Copilot coding agent ("cloud agent")**
- Intake: assign an issue or create a task in the Agents panel, with a model picker. Before opening the PR, the agent "runs Copilot code review on its own changes, applies the feedback, and iterates". Code scanning, secret scanning and dependency-vulnerability checks run inside the agent's workflow, so findings surface before the PR opens. Code scanning is included at no extra cost. "Copilot requests your review only after it has iterated." Custom agents live in `.github/agents/` (example: a performance agent that benchmarks, changes, then re-measures). CLI handoff lets a user pull the cloud session down locally, and `&` pushes it back. — [GitHub Blog, Feb 26 2026](https://github.blog/ai-and-ml/github-copilot/whats-new-with-github-copilot-coding-agent/)
- Limits: it runs in an "ephemeral cloud development environment", "can only work on one branch at a time and can open one pull request per task", and changes only the repository specified. Sessions are capped at 59 minutes, which "cannot be extended or bypassed". Repository rulesets can block it. Session logs "do not replace your own review and testing." — [GitHub Docs: about coding agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- A separate `/security-review` command shipped in public preview on Jul 14, 2026. It scans in-progress changes for injection, XSS and path traversal. — [GitHub changelog](https://github.blog/changelog/2026-07-14-security-reviews-now-available-in-the-github-copilot-app/)

**Cursor (background/cloud agents + Bugbot)**
- Bugbot Autofix (beta) "spins up a Cloud Agent to patch issues". This closes the loop from review to fix. Planned additions: running code to verify its own reports, and an always-on scanning mode. — [Cursor forum: Building a better Bugbot, Jan 16 2026](https://forum.cursor.com/t/building-a-better-bugbot/149040)

**OpenAI Codex (cloud)**
- Each task runs in its own isolated workspace, inside a configured environment. Codex installs dependencies through a saved install script that is reused across tasks. Internet access is toggled per environment, with package-manager presets and allowed-domain lists; OpenAI advises "limit the environment's network destinations". Tasks keep running "while your computer is asleep". The user reviews the diff and test results, then "commit[s] or open[s] a pull request when you're ready". — [Codex cloud docs](https://learn.chatgpt.com/docs/cloud)
- Codex code review runs in GitHub through `@codex review`, automatic reviews, Review guidelines in AGENTS.md, P0/P1 prioritization, and `@codex fix`. — [eastondev guide, Jul 2026 (secondary)](https://eastondev.com/blog/en/posts/ai/20260709-codex-ai-code-review-pr/)

**Google Jules**
- Jules clones the repo into an isolated cloud VM, applies changes, runs tests and captures the diff. The user then clicks "Publish PR". — [MachineLearningMastery (secondary)](https://machinelearningmastery.com/practical-agentic-coding-with-google-jules/)
- Jules produces a plan with step-by-step breakdowns and assumptions, and the user can give feedback before approving it. If the user navigates away, the plan auto-approves on a timer. In the API, plans auto-approve unless `requirePlanApproval` is true. — [Jules docs: review plan](https://jules.google/docs/review-plan/)

**Replit Agent 3** (Sep 2025)
- App Testing drives a real browser to "test its own work... find problems, and fix them in a loop". It runs only when the agent judges enough has changed, not after every message. At launch it supported Full Stack JS and Streamlit only. — [Replit docs: app testing](https://docs.replit.com/replitai/app-testing)
- The agent can run autonomously for up to 200 minutes. — [Replit changelog Sep 12 2025](https://docs.replit.com/updates/2025/09/12/changelog)
- Replit says "without robust verification, mistakes compound". Its REPL-based verification combines code execution with browser automation to catch "Potemkin interfaces" (features that look functional but are not), and Replit credits this with enabling 200+ minute runs. — [Replit blog: automated self-testing](https://replit.com/blog/automated-self-testing)

**Amp (spun out of Sourcegraph)**
- The "oracle" is a read-only subagent on a stronger, slower reasoning model (o3 at launch). It is used for review and debugging alongside the main agent, and it is invoked by explicit prompting (for example, "review the last commit") rather than pushed hard in the system prompt. — [ampcode.com/news/oracle](https://ampcode.com/news/oracle)
- Amp replaced its one-shot review request with a dedicated review agent and toolset, "to perform deeper analysis... and filter out low-signal feedback". — [HackerNoon (secondary)](https://hackernoon.com/amps-code-review-agent-tries-to-cut-the-low-signal-noise); [Tessl blog](https://tessl.io/blog/amp-adds-agentic-code-review-to-its-coding-agent-toolkit)

### Inferences
- **Recurring patterns:**
  - Isolated ephemeral cloud sandbox or VM per task, with network egress controls.
  - One branch and one PR per task.
  - Optional plan approval. The default leans toward auto-approval (Jules); approval is explicit in Factory Missions.
  - Self-verification with the repo's own tests.
  - Repo instruction files steer behaviour (AGENTS.md, `.github/agents/`, Bugbot rules, Devin playbooks).
  - A human merges.
- **Distinctive:**
  - Factory Missions: orchestrator/worker/validator roles, a validation contract fixed before coding, milestone checkpoints, multi-day runs, and a "readiness level" gate on the repo.
  - Copilot: the reviewer and security scan run *before* the PR opens.
  - Replit: browser-level "Potemkin" detection.
  - Cursor: review flows into autofix by a cloud agent.
  - Devin: fleet execution of human-written playbooks across hundreds of repos.
  - Amp: an on-demand stronger "oracle" model as a second opinion, rather than a fixed pipeline stage.
- Copilot's hard 59-minute cap contrasts with Replit's 200+ minutes and Factory's multi-day missions. Products differ widely on the long-task bet.

### Gaps
- Exact retry or rework round limits are unpublished for every product. Factory has a "feature retry limit" but does not give its value.
- I fetched no primary source for Copilot's Actions runtime, `copilot/` branch naming, the CI-workflow approval requirement, or the rule that the agent cannot approve its own PR. These are commonly reported but unverified here.
- Did not cover Cursor background-agent internals (VM type, parallel agents/best-of-N), Codex best-of-N attempts, Devin's VM/isolation, or Jules's newer features (e.g., any critic step). No search hits on "Jules critic".
- Did not cover other notable agents (Claude Code on the web / GitHub Actions, AWS Kiro spec-driven flow, Augment, Windsurf/Cognition merger).

## Q2: Which use separate reviewer agents or panels, and does it help? Data on precision and noise?

### Takeaway
Separate reviewer agents are now standard: Copilot code review (used as a self-review gate), Cursor Bugbot, Codex code review, Amp's review agent and oracle, Devin first-pass review, and Factory scrutiny validators. Vendors publish "resolution" or "address" rates of roughly 50 to 80%. None publish precision, recall or false-positive rates. OpenAI says plainly that it trades recall for precision.

### Cited Findings
- Bugbot: "multiple bug-finding passes" run on shuffled orderings of the diff, and an issue is kept only if it appears across several passes ("majority voting"). Bugbot moved from a fixed pipeline to "a fully agentic loop" with tool calls. It reviews "over two million PRs every month". Its metric is resolution rate: an AI judge checks at merge time "which Bugbot-reported issues actually got fixed in the final diff". About 40 experiments raised resolution from about 52% to over 70%, and resolved bugs per PR more than doubled. — [Cursor forum, Jan 16 2026](https://forum.cursor.com/t/building-a-better-bugbot/149040)
- In a May 2026 changelog (as summarized), 80% of Bugbot-identified bugs were resolved by merge at default effort, and high effort found 35% more bugs. Cursor publishes no precision, recall or false-positive rate. — [Augment Code analysis (secondary)](https://www.augmentcode.com/guides/cursor-bugbot-code-review-capabilities-limits)
- Bugbot reached a 78% resolution rate after "Bugbot Learning", which turns developer feedback into rules, up from 52% at its July 2025 launch. — [Creative AI News (secondary)](https://www.creativeainews.com/blog/cursor-bugbot-78-resolution-rate-learned-rules/)
- A June 2026 claim on X says Bugbot became 3x faster, 22% cheaper and finds 10% more bugs. This comes only via search snippet (unverified). — [Augment Code (secondary)](https://www.augmentcode.com/guides/cursor-bugbot-code-review-capabilities-limits)
- User complaints about Bugbot: misses on the first pass, multiple review cycles needed, and 9 to 12 minute latency on small PRs. — [Cursor forum](https://forum.cursor.com/t/building-a-better-bugbot/149040)
- OpenAI Codex reviewer (Dec 1, 2025) on review volume and uptake:
  - Handles more than 100k external PRs per day (as of Oct 2025).
  - Comments on 36% of PRs that Codex cloud generated entirely.
  - 46% of its comments on Codex-generated PRs lead to a code change, versus 53% on human PRs; the overall address rate is 52.7%.
  - Over 80% of reactions are positive.

  — [OpenAI Alignment blog](https://alignment.openai.com/scaling-code-verification/)
- OpenAI Codex reviewer design and caveats:
  - "Repo access and execution" improved both recall and precision compared with diff-only review.
  - "We optimize for signal-to-noise first, and only then push recall."
  - The reviewer is trained separately from the generation reward model.
  - "Even at a small fraction of the generator's token spend", the verifier catches a large share of high-severity issues (no exact numbers given).
  - Caveat from OpenAI: teams might treat "a clean review as a guarantee of safety rather than as one layer of defense."

  — [OpenAI Alignment blog](https://alignment.openai.com/scaling-code-verification/)
- Copilot coding agent runs Copilot code review on itself before opening the PR. GitHub gives no effectiveness numbers. — [GitHub Blog, Feb 2026](https://github.blog/ai-and-ml/github-copilot/whats-new-with-github-copilot-coding-agent/)
- Amp: a dedicated review agent replaced its one-shot review in order to "filter out low-signal feedback". — [HackerNoon](https://hackernoon.com/amps-code-review-agent-tries-to-cut-the-low-signal-noise)
- Specialist security reviewers: Copilot runs code, secret and dependency scanning inside the agent loop ([GitHub Blog](https://github.blog/ai-and-ml/github-copilot/whats-new-with-github-copilot-coding-agent/)), and `/security-review` is a separate command ([GitHub changelog Jul 2026](https://github.blog/changelog/2026-07-14-security-reviews-now-available-in-the-github-copilot-app/)). Devin is used for security fixes: 1.5 minutes per vulnerability versus 30 for humans, self-reported ([Cognition](https://cognition.com/blog/devin-annual-performance-review-2025)).

### Inferences
- The measured lever is noise control. Ways vendors cut noise:
  - repeated passes plus voting (Cursor)
  - giving the reviewer tools and execution (OpenAI)
  - learned rules from developer feedback (Cursor)
  - a precision-first tuning target (OpenAI)
- "Panels" in the sense of multiple independent passes plus voting exist (Bugbot). Panels of distinct specialist personas are not documented by any vendor, except that security scanning is a separate deterministic tool layer.
- The roughly 50% address rate for both AI and human PRs (OpenAI) suggests that about half of reviewer comments are acted on. This is an upper bound on how many reviewer outputs prompt a change, and it is not a precision measure.

### Gaps
- No vendor publishes false-positive rates. No independent head-to-head evaluation of review precision was found.

## Q3: When do they escalate to a human versus auto-merge? Is there risk classification?

### Takeaway
None of the products surveyed auto-merges by default. The human gates are plan approval (optional) and PR merge, with mid-run intervention possible. Risk classification shows up only as severity tagging of review findings (Codex P0/P1) and as Devin's "which work goes to human vs AI" routing advice. No vendor publishes a documented auto-merge risk policy.

### Cited Findings
- Copilot requests human review only after self-iteration; it opens one PR per task; rulesets can block it. — [GitHub Blog](https://github.blog/ai-and-ml/github-copilot/whats-new-with-github-copilot-coding-agent/); [GitHub Docs](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- Jules auto-approves its plan on a timer unless `requirePlanApproval` is set; the user then publishes the PR manually. — [Jules docs](https://jules.google/docs/review-plan/)
- Factory: plan approval is required, and the user can pause the orchestrator and intervene. — [Factory Missions overview](https://docs.factory.com/missions/overview)
- Codex: findings are tagged P0/P1. A third-party guide advises checking the diff, CI and tests before invoking `@codex fix`. — [eastondev (secondary)](https://eastondev.com/blog/en/posts/ai/20260709-codex-ai-code-review-pr/). A community skill (not product spec) escalates to a human after 3 review-fix-review cycles if P0/P1 issues persist. — [skills.sh codex-code-review](https://skills.sh/nickcrew/claude-cortex/codex-code-review)
- Devin can "map dependencies, flag breaking changes, and recommend which work should go to humans or AI". — [Cognition](https://cognition.com/blog/devin-annual-performance-review-2025)

### Inferences
- In practice, escalation is triggered by (a) ambiguity, which is handled by front-loaded planning; (b) the merge gate, which is always human; and (c) repeated failure or retry limits (Factory's retry-limit warning). An explicit "N rounds then escalate" limit appears only in community conventions (3 cycles).

### Gaps
- No primary source found for an auto-merge risk-tier policy from any vendor.

## Q4: How do they handle long tasks (decomposition, progress files, checkpoints, resume)?

### Takeaway
Factory Missions is the most explicit design: a plan with features and milestones, validation at each milestone, follow-up fix work, Mission Control tracking, and pause/recover. Replit relies on continuous self-testing so that errors don't compound. Devin and Copilot avoid long tasks by sizing work small (4 to 8 human-hours; 59-minute cap) and fanning out in parallel.

### Cited Findings
- Factory: the plan is organised into features and milestones; the validation contract is set before coding; follow-up work is created when validation fails; work runs on persistent remote machines; the user can pause and ask the orchestrator to recover. Factory warns against converting a long normal session into a Mission. — [Factory Missions overview](https://docs.factory.com/missions/overview); [ZenML summary](https://zenml.io/llmops-database/multi-agent-software-development-system-with-extended-autonomous-execution)
- Replit: verification is what made 200+ minute runs viable. — [Replit blog](https://replit.com/blog/automated-self-testing)
- Devin: sizing is 4 to 8 junior-hours, scope is set up front, and parallel fleets are used for breadth. — [Cognition](https://cognition.com/blog/devin-annual-performance-review-2025)
- Copilot: hard 59-minute session cap; CLI handoff moves a session between cloud and local while keeping its branch, logs and context. — [GitHub Docs](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent); [GitHub Blog](https://github.blog/ai-and-ml/github-copilot/whats-new-with-github-copilot-coding-agent/)

### Inferences
- Two strategies for long work:
  - Make the task short (small scope plus parallelism): Devin, Copilot, Codex.
  - Make the run durable (milestones, a validation contract, a remote persistent machine): Factory.
- Both strategies depend on an automated way to verify the app.

### Gaps
- Factory's progress-file format and resume-after-crash mechanics were not described in the fetched pages.

## Q5: Published cost per task, time per task, success rates

### Takeaway
Hard per-task cost numbers are almost absent. Success figures are vendor-reported merge or resolution rates. Independent tests are scarce and older, and they are much less favorable.

### Cited Findings
- Devin (self-reported, Nov 2025):
  - PR merge rate 67%, up from 34% a year earlier.
  - 4x faster and 2x more resource-efficient.
  - Migrations 10x to 14x faster.
  - Test coverage from 50–60% to 80–90%.
  - Pushed about one third of the commits to Cognition's web app.

  — [Cognition](https://cognition.com/blog/devin-annual-performance-review-2025)
- Independent: Answer.AI's late-2024 month-long test of Devin got 3 successes out of 20 tasks (14 failures, 3 inconclusive). Dated, and it predates the 67% claim. — summarized at [blog.imseankim.com (secondary)](https://blog.imseankim.com/devin-2-ai-software-engineer-review-cognition-pricing-benchmark/); an analysis notes that the merge-rate metric cannot be replicated by third parties — [agentmarketcap.ai](https://agentmarketcap.ai/blog/2026/08/26/cognition-devin-67-percent-pr-merge-rate-vendor-production-metric)
- Bugbot resolution rate went from 52% to over 70% (Jan 2026), then 78% to 80% (2026). Self-reported, measured by an AI judge. — [Cursor forum](https://forum.cursor.com/t/building-a-better-bugbot/149040); [Augment Code](https://www.augmentcode.com/guides/cursor-bugbot-code-review-capabilities-limits)
- Codex review: 52.7% of comments are addressed and more than 100k PRs are reviewed per day (self-reported). — [OpenAI](https://alignment.openai.com/scaling-code-verification/)
- Factory pricing: Pro $20/mo, Plus $100/mo, Max $200/mo (aggregator, unverified). No per-task cost published; Factory says only that more planning and validation means higher cost. — [AI Agent Index](https://theaiagentindex.com/agents/factory-ai); [Factory docs](https://docs.factory.com/missions/overview)

### Inferences
- Vendors have converged on production-outcome metrics (merge rate, resolution rate, address rate) rather than benchmarks. These metrics are easy to inflate through task selection, and no third party can audit them.

### Gaps
- No published per-task dollar cost or wall-clock time for any product. No independent 2026 success-rate study was found.
