# Efficiency and cost of an autonomous Claude Code build pipeline (as of 14 Oct 2026)

Pipeline under study: spec-writer, then builder, then parallel specialist reviewers, then approver, for each feature. It runs headless on Claude Code, operated by one person on a Windows PC with 8 GB of RAM.

All pages were fetched on 2026-10-14 unless a note says otherwise. Anything marked **[ESTIMATE]** is my own arithmetic from the cited prices, not a published figure.

## Q1. Current prices, caching, plan limits, rate limits, and typical token use

### Takeaway
At list price, Opus 5.5 is $4 in / $20 out per million tokens (MTok) and Sonnet 5.5 is $2 / $10, so Opus costs 2x Sonnet. On both, a cache read costs only 5% of the base input price. Haiku 5.5 costs $0.10 / $0.50 for prompts up to 100k tokens, which is 20x cheaper than Sonnet. The Fable models cost $10 / $50.

In Claude Code, subagents get a 5-minute cache by default, even on a subscription. Each subagent builds its own cache and does not read the parent's, while a fork does read the parent's cache. On a subscription, every subagent draws from the same 5-hour and weekly pool as the main session.

### Cited Findings

**Per-token list prices, per MTok** ([platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing), fetched 2026-10-14)

| Model | Input | 5m cache write | 1h cache write | Cache hit | Output |
|---|---|---|---|---|---|
| Fable 5.1 | $10 | $12.50 | $20 | $0.25 (0.025x) | $50 |
| Fable 5 | $10 | $12.50 | $20 | $1 | $50 |
| Opus 5.5 | $4 | $5 | $8 | $0.20 (0.05x) | $20 |
| Opus 5 | $5 | $6.25 | $10 | $0.50 | $25 |
| Sonnet 5.5 | $2 | $2.50 | $4 | $0.10 (0.05x) | $10 |
| Sonnet 5 | $2 | $2.50 | $4 | $0.20 | $10 |
| Haiku 5.5, prompt ≤100k tokens | $0.10 | $0.125 | $0.20 | $0.01 | $0.50 |
| Haiku 5.5, prompt >100k tokens | $0.50 | $0.625 | $1 | $0.05 | $2.50 |

Mythos 5.1 and Mythos 5 cost the same as Fable but have limited availability.

Other pricing rules from the same page ([pricing](https://platform.claude.com/docs/en/about-claude/pricing)):
- **Sonnet 5 price:** the $2/$10 price was introductory, but it is now the standard price. The increase to $3/$15 that had been planned for 1 Sep 2026 "will not occur."
- **Cache multipliers:**
  - A 5-minute cache write costs 1.25x base input and a 1-hour write costs 2x.
  - A cache hit costs 0.1x by default, 0.05x on Opus 5.5 and Sonnet 5.5, and 0.025x on Fable 5.1 and Mythos 5.1.
  - A 5-minute write "pays off after one cache read," and a 1-hour write after two.
  - The cache multipliers stack with the Batch discount and with data residency.
- **Batch API:** 50% off both input and output. For example, Opus 5.5 drops to $2/$10, Sonnet 5.5 to $1/$5, and Haiku 5.5 (prompts ≤100k) to $0.05/$0.25. Fast mode cannot be combined with Batch.
- **Long context:** "Claude 4.6 and later models (except Claude Haiku 5.5)" get the full 1M-token context at standard price. Haiku 5.5 switches to the higher price tier for any request whose prompt is over 100,000 tokens, and that count includes cached tokens.
- **Fast mode** (research preview): Opus 5.5 costs $8/$40 per MTok, which is 2x standard.
- **US-only inference** (`inference_geo: "us"`) costs 1.1x.
- **Minimum cacheable prompt:** 286 tokens for Opus 5.5, Sonnet 5.5 and Haiku 5.5.
- **Worked example on the pricing page:** 50k input plus 15k output on Opus 5.5 costs $0.50 in tokens. When 40k of that input is read from cache, the token cost falls to $0.348. (The page's totals of $0.58 and $0.428 add $0.08 of Managed Agents session runtime.)

**How Claude Code uses caching** ([code.claude.com/docs/en/prompt-caching](https://code.claude.com/docs/en/prompt-caching))
- **Request layout:** each request is ordered system prompt and tools, then project context (CLAUDE.md, memory, rules), then the conversation.
- **Prefix matching:** the cache matches the request prefix exactly, so "a change anywhere in the prefix recomputes everything after it. There is no per-file or per-segment caching."
- **Default TTLs:**
  - On a subscription within plan usage, the main conversation (including `-p` runs) gets a 1-hour cache.
  - Subagents, workflows, teammates, forks and compaction get 5 minutes.
  - When you are drawing on usage credits, or using an API key or a cloud provider, everything defaults to 5 minutes.
- **TTL overrides:**
  - `promptCacheTtl` or `CLAUDE_CODE_PROMPT_CACHE_TTL` sets the main conversation's TTL.
  - `subagentPromptCacheTtl` or `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL` sets it for everything else.
  - A subagent's frontmatter can set `experimental.cacheTtl`.
  - These require v2.1.242 or later (v2.1.248 for the frontmatter field).
- **What breaks the cache:**
  - switching models (each model has its own cache), including `opusplan` toggles and a skill whose frontmatter names a different model
  - changing effort on older models (on Opus 5.5, Sonnet 5.5, Haiku 5.5 and Fable 5.1 the cache stays intact)
  - turning on fast mode
  - adding or removing MCP tools when tool definitions are loaded upfront
  - compaction
  - upgrading Claude Code
- **What keeps the cache:** editing repo files, editing CLAUDE.md mid-session (the edit is not applied until `/clear`, `/compact` or a restart), skills, permission-mode changes, and `/rewind`.
- **Subagents and the cache:**
  - A subagent's "first request doesn't read the parent's cache," and it builds its own.
  - A fork inherits the parent's prefix and does read its cache.
  - In a workflow fan-out of agents that share a prefix, Claude Code holds back all but the first for up to 5 seconds so the rest can read the first one's cache.
- **Cache scope:** the cache is effectively scoped to one machine and directory. "Sessions you run in parallel in the same directory build matching prefixes and read each other's cache." Sequential sessions share a prefix only when the startup git-status snapshot matches. Separate worktree directories therefore do **not** share each other's cache.
- **Checking the cache:** `/usage` shows a `Prompt cache (main)` line (v2.1.251+). Running `claude -p "hello" --output-format json` shows `ephemeral_1h_input_tokens` and `ephemeral_5m_input_tokens`.

**Claude Code cost figures and levers** ([code.claude.com/docs/en/costs](https://code.claude.com/docs/en/costs))
- **Average spend:** "around $13 per developer per active day and $150-250 per developer per month, with costs remaining below $30 per active day for 90% of users" (enterprise deployments).
- **Agent teams:** they use "approximately 7x more tokens than standard sessions when teammates run in plan mode." Token use is "roughly proportional to team size." The page recommends Sonnet for teammates.
- **Thinking:** thinking tokens are billed as output. Thinking cannot be turned off on Opus 5.5, Sonnet 5.5, Haiku 5.5 or Fable, so the cost lever is the effort level.
- **Hooks as preprocessors:** a hook can cut context "from tens of thousands of tokens to hundreds." The page gives an example PreToolUse hook that filters test output down to failures.
- **CLAUDE.md:** keep it under 200 lines and move workflow-specific instructions into skills.
- **Tools:** prefer CLI tools over MCP servers. MCP tool definitions are deferred by default.
- **Background usage:** typically under $0.04 per session.
- **Rate-limit guidance for teams of 1-5 users:** 200k-300k TPM and 5-7 RPM per user.
- **Subagent cost:** every subagent "sends its own requests on top of the main conversation's." `/usage` attributes plan usage to subagents, skills and MCP servers.

**Subagent cost controls** ([code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents))
- **Frontmatter fields:**
  - `model`: `haiku`, `sonnet`, `opus`, `fable`, `inherit`, or a full model ID
  - `effort`: `low` to `max`
  - `maxTurns`: output is returned marked as partial when the limit is hit
  - `tools` and `disallowedTools`
  - `background`
  - `isolation: worktree`
  - `omitClaudeMd: true` (v2.1.271+)
  - `experimental.cacheTtl`
- **Defaults:** up to 20 subagents can run at once by default (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`), and nesting goes up to 3 levels (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`).
- **Forcing one model:** `CLAUDE_CODE_SUBAGENT_MODEL` together with `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` makes every subagent use one model.
- **Shared limits:** "Subagent requests count toward the same usage limits as your main conversation."
- **Thinking:** extended thinking is inherited from the main session, and there is no per-subagent thinking setting.
- **Descriptions:** if the combined subagent descriptions exceed 15,000 tokens, Claude Code shows a warning at startup.
- **Built-in agents:** Explore and Plan skip CLAUDE.md and the git status snapshot "to keep them fast and inexpensive."

**Subscription plans** ([claude.com/pricing](https://claude.com/pricing); [support article 11145838](https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan))
- **Prices:**
  - Pro: $20 a month billed monthly, or $17 a month billed annually.
  - Max 5x: from $100 a month, with 5x Pro's usage per 5-hour session.
  - Max 20x: 20x Pro's usage per session. The page I fetched did not state a separate price for it. Third parties commonly cite $200 ([leanware](https://leanware.co/insights/claude-max-plan)).
  - Team: Standard seats $20/$25 and Premium seats $100/$125 (annual/monthly).
- **Limits:** every plan has a rolling 5-hour window, and paid plans "add weekly limits on top." Max has a separate weekly limit for Fable, and Fable usage on Max counts at "50% of weekly limits" per the pricing table.
- **Shared pool:** the limits "are shared across Claude and Claude Code."
- **No published numbers:** Anthropic publishes **no** token or message counts for these limits.
- **Third-party estimates (not authoritative):** Max 5x is about 225 messages per 5 hours, and Max 20x about 900. Third parties also report that on 6 May 2026 Anthropic doubled Claude Code's 5-hour limits ([ai-toolbox](https://www.ai-toolbox.co/claude-management-and-productivity/claude-usage-limits-2026); [verdent](https://www.verdent.ai/guides/claude-code-limits-doubled-may-2026)). These sources disagree about a temporary weekly increase.

**API rate limits** ([platform.claude.com/docs/en/api/rate-limits](https://platform.claude.com/docs/en/api/rate-limits))
- **Start tier** (spend cap $500 a month): Opus 5.5, Sonnet 5.5 and Haiku 5.5 each get 1,000 RPM, 2,000,000 input tokens per minute (ITPM) and 400,000 output tokens per minute (OTPM). Fable 5.x gets 1,000 RPM, 500k ITPM and 100k OTPM.
- **Build tier** (cap $1,000 a month): 5,000 RPM, 5M ITPM and 1M OTPM.
- **Scale tier** (cap $200,000 a month): 10,000 RPM, 10M ITPM and 2M OTPM.
- **Cached input:** "only uncached input tokens count toward your ITPM rate limits" for most models.
- **Spend cap:** reaching it pauses the API until the first day of the next month (UTC).

**Multi-agent token multipliers** ([Anthropic engineering, 13 Jun 2025](https://www.anthropic.com/engineering/multi-agent-research-system))
- "agents typically use about 4× more tokens than chat interactions… multi-agent systems use about 15× more tokens than chats."
- "token usage by itself explains 80% of the variance" in BrowseComp performance.
- Multi-agent setups fit poorly in domains "where all agents must share the same context or involve many dependencies."

### Inferences
- **[ESTIMATE] Cost of one reviewer pass:** Sonnet 5.5 reading 30k tokens of fresh input (spec plus diff) and writing 3k tokens costs about $0.06 + $0.03 = **$0.09**. The same pass on Haiku 5.5 costs about **$0.0045**, and on Opus 5.5 about **$0.18**. A reviewer that instead reads the whole repo, say 300k tokens, costs about $0.60 on Sonnet and $1.20 on Opus for the first read alone. On Haiku 5.5 it would also jump to the >100k price tier.
- **[ESTIMATE] Cost of a builder run:** Opus 5.5 with 40 turns and an average cached context of 80k tokens comes to about 3.2M cache-read tokens × $0.20 = $0.64. Add about 200k tokens of cache writes at $5 = $1.00 and about 40k output tokens at $20 = $0.80. That is roughly **$2.50 per feature build**. Sonnet 5.5 would cost about half. Output and cache writes dominate the bill, not cache reads.
- **Cache TTL on Windows/headless runs:** each `claude -p` call is a "main conversation," so on a subscription it gets the 1-hour TTL. A reviewer spawned as a subagent gets 5 minutes. Running each pipeline stage as its own `claude -p` process from a script, in the same directory, keeps 1-hour caching and lets same-directory runs share a prefix.
- **Worktrees and caching:** per-feature worktrees in different directories lose cross-session cache sharing. That is a small loss, because each stage's content differs anyway.
- **Keep the prefix stable:** use the same model and the same tool set for each role, avoid mid-run model switches, pin the Claude Code version during a batch, and keep CLAUDE.md short or use `omitClaudeMd` for reviewers.

### Gaps
- Anthropic publishes no numeric 5-hour or weekly limits, so it is unknown how many feature builds fit in a Max window.
- I found no official Anthropic figure for the token use of a typical single subagent run or feature build. The 7x agent-team figure and the 15x multi-agent figure are the only published multipliers.
- I did not confirm Max 20x's price on the official page; $200 comes from third parties.

## Q2. Where the cost goes in multi-agent pipelines, and how to cut it

### Takeaway
Cost grows with the size of each agent's context times its number of turns. The biggest wins are:
- give each agent the smallest possible context (the diff plus the spec, not the repo)
- run cheap deterministic checks first and spawn LLM reviewers only when needed
- use smaller models and lower effort for triage
- keep prefixes stable so the cache is hit

### Cited Findings
- **Context is re-read on every turn:** Claude Code "sends your full conversation with every request," so a long session "draws usage for the whole conversation." Tool results add another request each time. Compaction is itself a large request ([costs](https://code.claude.com/docs/en/costs)).
- **Isolation has a cost:** a non-fork subagent starts with its own system prompt, CLAUDE.md, git status and preloaded skills, and does not see the parent's history. That isolates noise but means it re-reads what it needs ([sub-agents](https://code.claude.com/docs/en/sub-agents)).
- **Specific prompts are cheaper:** "Vague requests like 'improve this codebase' trigger broad scanning" ([costs](https://code.claude.com/docs/en/costs)).
- **Code-intelligence (LSP) plugins** replace "a grep followed by reading multiple candidate files" with a single go-to-definition call ([costs](https://code.claude.com/docs/en/costs)).
- **Filtering hooks:** a hook that greps a 10,000-line log for errors cuts context "from tens of thousands of tokens to hundreds" ([costs](https://code.claude.com/docs/en/costs)).
- **Model, effort and turn caps:** route simple subagents to `model: haiku`, and set `effort: low` and `maxTurns` ([costs](https://code.claude.com/docs/en/costs); [sub-agents](https://code.claude.com/docs/en/sub-agents)).
- **Batch API** gives 50% off for work that is not time-sensitive ([pricing](https://platform.claude.com/docs/en/about-claude/pricing)). It is not usable from Claude Code itself; it applies only to direct API calls.
- **Meta's RADAR pipeline** runs, in order: eligibility gates, static heuristics, an ML Diff Risk Score, LLM-based automated code review, and deterministic validation before landing. In other words, the cheap stages come before the LLM stage ([arXiv 2605.30208](https://arxiv.org/abs/2605.30208)).

### Inferences
- **Recommended order for each feature** [ESTIMATE / design]:
  1. Run deterministic checks (format, lint, type check, tests, secret scan, SAST, dependency audit) as hook or script steps with no model involved. If any fail, send only the compact failure output back to the builder.
  2. Run a Haiku 5.5 triage call (about $0.005 per call at ≤100k tokens) on the diff stat and the list of changed paths. It decides which specialist reviewers to run.
  3. Run only the triggered Sonnet 5.5 reviewers. Each gets the spec, the `git diff` output, and at most the changed files, never a repo-wide exploration. Set `tools` to Read and Grep only, `maxTurns` to 5-10, `effort` to low or medium, and `omitClaudeMd: true`.
  4. Keep Opus 5.5 for the builder, and for the approver only when the risk is high.
- **Expected effect** [ESTIMATE]: deterministic gating plus conditional reviewers can plausibly avoid most reviewer spawns on low-risk diffs. Each avoided Sonnet reviewer saves about $0.10-0.60 depending on its context.
- **Parallelism does not save tokens.** Parallel reviewers cost about the same tokens as running them one after another; parallelism buys wall-clock time only.

### Gaps
- I found no published A/B numbers on how much diff-only review saves compared with whole-repo review, or on how often deterministic gates catch issues before the LLM stage.

## Q3. Risk-based gating: what can auto-merge and what needs a human

### Takeaway
Industry practice is to classify changes by consequence, not by size. Path rules (auth, payments, migrations, infra, secrets) force human review, and a classifier, either an ML model or an LLM, routes the rest. Meta and Vercel both report that auto-approving low-risk changes did not increase reverts.

### Cited Findings
- **Meta RADAR** ("Risk Aware Diff Auto Review"):
  - It "has reviewed 535K+ diffs and landed 331K+."
  - Relaxing the threshold from the 25th to the 50th percentile raised the approval rate to 60.31%.
  - The revert rate is 1/3 that of non-RADAR diffs, and the production incident rate is 1/50.
  - Median time to close fell by "over 330%" (ambiguous wording; a co-author describes it as 3.3x faster), and median review wall time fell by 35%.
  - Context: lines of code per diff grew 105.9% year over year, with agentic AI accounting for more than 80% of that growth ([arXiv 2605.30208](https://arxiv.org/abs/2605.30208), May 2026).
- **Vercel:**
  - An LLM classifier reads the diff, title and description and outputs HIGH or LOW.
  - HIGH covers auth, payments, data integrity, security and infra. LOW covers UI, styling, tests, docs, refactors, and feature flags that are off.
  - The agent's approval satisfies branch protection for LOW changes.
  - 671 low-risk PRs skipped review and none were reverted; the upper bound of the 95% Wilson interval is 0.6%. A human-reviewed control group had 2 reverts in 513 (0.39%).
  - Deployment rollbacks fell from 2.8 to 1.9 a week. The post is titled "58% of PRs in our largest monorepo merge without human review" ([Vercel blog](https://vercel.com/blog/58-percent-of-prs-in-our-largest-monorepo-merge-without-human-review), per search summary; my direct fetch returned 404 and the .md variant was not fetched).
- **Classification methods** described in practitioner guides:
  - file-path heuristics (auth/, migrations/, infrastructure/ are high; docs/ and styles/ are low)
  - diff analysis (schema changes, permission changes, new environment variables)
  - the agent classifying its own change, which risks underestimating
  - guides also recommend that CODEOWNERS always require human review for critical files, and that diff size be used only to prompt splitting a change. For example, a 12-line migration can take down production.
  - Sources: [agentpatterns.ai risk-based shipping](https://agentpatterns.ai/verification/risk-based-shipping/), [dev.to risk-based review](https://dev.to/pyor/risk-based-code-review-tier-rigor-by-blast-radius-352j), [rewind.com](https://rewind.com/blog/ai-approve-pull-requests-safely/), [cortex.io](https://www.cortex.io/post/risk-based-code-review). These are secondary practitioner sources.

### Inferences
- **Suggested policy for a one-person pipeline** [design]:
  - **Always human:** auth, crypto, secrets, payments, DB migrations, CI/hook config, dependency manifest changes, and any change to the harness's own gate scripts.
  - **Auto-approve:** docs, tests and styling where all deterministic checks pass and no sensitive path is touched.
  - **Everything else:** the LLM approver decides.
  - **Feedback loop:** log every auto-merge and review any revert, then tune the rules.
- **Self-classification:** the builder agent should never classify its own change's risk. A separate deterministic path check, or a Haiku classifier, should do it.

### Gaps
- I did not fetch primary sources on Google's code-review practice (small CLs, the readability/OWNERS model) or on GitHub/GitLab auto-merge policy docs.
- I found no data on risk gating for a solo developer as opposed to a large organization.

## Q4. Practical limits on an 8 GB Windows machine

### Takeaway
There is no official figure for Claude Code's memory use. User reports show about 1.5 GB per Claude Code process on Windows, more with MCP or Node subprocesses, and occasional runaway growth to many GB from leaks or large retained bash output. On 8 GB, plan for **2 concurrent Claude Code processes, and 3 at most**, with heavy test suites run one at a time.

### Cited Findings
- **Windows report (16 GB machine):** Claude processes at about 1.5 GB, plus about 1.2 GB across 17 Node MCP subprocesses ([claudeissues #51476](https://claudeissues.com/issue/51476-high-ram-consumption-from-node-mcp-subprocesses-on-windows-many-plugins-1m-conte)). User report.
- **Leak reports elsewhere:**
  - about 12 GB of growth on macOS ([GitHub #23252](https://github.com/anthropics/claude-code/issues/23252))
  - over 20 GB on Ubuntu, with `NODE_OPTIONS=--max-old-space-size=5120` used as a cap ([GitHub #20777](https://github.com/anthropics/claude-code/issues/20777))
  - about 3 GB at startup ([claudeissues #17650](https://claudeissues.com/issue/17650-bug-memory-leak-claude-code-consumes-3gb-ram-within-seconds-of-startup))
  - Bash output retained for the whole session, and lingering watch-mode child processes, are cited as causes ([Medium, low authority](https://medium.com/@joe.njenga/claude-code-high-memory-usage-hits-crazy-129gb-ram-my-investigation-fixes-38bd44dfcfce)).
- **Subagent concurrency:** the default ceiling is 20 subagents ([sub-agents](https://code.claude.com/docs/en/sub-agents)). That is a software limit, not a sizing recommendation.
- **Worktree isolation:** `isolation: worktree` creates a temporary git worktree, which is removed automatically if the subagent made no changes ([sub-agents](https://code.claude.com/docs/en/sub-agents)).

### Inferences
- **Memory budget on 8 GB** [ESTIMATE]: Windows itself plus an editor or browser takes about 3-4 GB, which leaves about 4 GB. At about 1-1.5 GB per Claude Code process with no MCP servers, that allows 2, maybe 3, concurrent processes.
- **Subagents inside one process** probably share that process's Node heap, so they are cheaper in RAM than separate `claude -p` processes. I could not confirm this from docs.
- **Memory mitigations:**
  - disable MCP servers and plugins in headless runs
  - cap the heap with `NODE_OPTIONS=--max-old-space-size=2048` (value is an estimate)
  - pipe test output through a filter
  - restart processes between features rather than reusing one long session
- **Test suites:** run one at a time, since test runners (pytest, node) can use more RAM than Claude Code itself. Parallel reviewers that only read the diff are light.

### Gaps
- There is no official Anthropic figure for memory per process or subagent, and I found no Windows-specific benchmark.
- It is unconfirmed whether in-process subagents add meaningful heap.

## Q5. Free tools that can run as Windows hook scripts

### Takeaway
Gitleaks (a single Go binary) and Semgrep CE (native on Windows since fall 2025, installed via pip) are confirmed options. The Python-ecosystem tools ruff, bandit and pip-audit are standard pip installs, but I did not verify their details in this session.

### Cited Findings
- **Gitleaks:**
  - Install via Homebrew, Docker or Go, or download prebuilt binaries from the releases page for "many popular platforms" ([github.com/gitleaks/gitleaks](https://github.com/gitleaks/gitleaks)). Third-party mirrors show Windows ZIP archives up to v8.30.1 ([onworks](https://www.onworks.net/software/windows/app-gitleaks)).
  - `detect` and `protect` were deprecated in v8.19.0 in favour of `git` (which takes `--log-opts` for commit ranges) and `dir`.
  - Exit codes: 0 means no leaks, 1 means leaks or an error, and `--exit-code` overrides the code returned for leaks ([github](https://github.com/gitleaks/gitleaks)).
- **Semgrep CE:** "native Windows support (no WSL required!)" arrived in the fall 2025 release. It was in beta in July 2025 and became generally available in autumn 2025. Install with `pip install semgrep` ([Semgrep blog](https://semgrep.dev/blog/2025/semgrep-community-edition-fall-release-2025); [release notes Jul 2025](https://docs.semgrep.dev/release-notes/july-2025)).
- **Claude Code hooks:** they can rewrite tool input, for example to filter test output, and can return compact results ([costs](https://code.claude.com/docs/en/costs)).

### Inferences
- **Candidate hook stack:**
  - gitleaks with `dir` on changed files, or `git --log-opts` for a range
  - semgrep with `--config auto` or a pinned ruleset, on changed files only
  - ruff for lint and format
  - bandit for Python SAST
  - pip-audit or `npm audit` for dependencies
  - the project's type checker and tests
  - Each step should exit non-zero on failure and print at most about 100 lines, so the output that reaches the LLM stays small.
- Python-stdlib-only checks, such as a path-based risk classifier that reads `git diff --name-only`, need no install at all.

### Gaps
- I did not verify the current versions, Windows install details or flags for ruff, bandit, pip-audit or npm audit (their docs were not fetched): [ruff](https://docs.astral.sh/ruff/), [bandit](https://bandit.readthedocs.io/), [pip-audit](https://github.com/pypa/pip-audit), [npm audit](https://docs.npmjs.com/cli/commands/npm-audit).
- I found no gitleaks or Semgrep release info dated 2026.
- Gitleaks' `--staged` flag is not mentioned in the README I fetched.
