# Anthropic guidance and Claude Code primitives for a long-running autonomous coding harness (as of Oct 2026)

Scope: (a) Anthropic engineering posts on long-running agents, multi-agent systems, context engineering, agentic coding; (b) Claude Code primitives for a pipeline of spec-writer → builder → parallel specialist reviewers → approver → merge or human escalation. All quotes below were fetched on 2026-10-14. Note on dates: the engineering posts are from Dec 2024 to Nov 2025 and name models that are now superseded (Opus 4/4.5, Sonnet 3.7/4). The current models are Opus 5.5, Sonnet 5.5 and Haiku 5.5, and the Claude Code docs are current (they cite versions up to v2.1.295).

## Q1. What do Anthropic's engineering posts recommend for long-running agents?

### Takeaway
Anthropic's recipe has two parts. First, an initializer session writes a JSON feature list where every feature starts as failing, a progress file, an `init.sh` and a first git commit. Second, each later coding session reads those files, works on exactly one feature, tests it end to end the way a user would, then commits and updates the progress file. Multi-agent fan-out improves results on breadth-first work but costs about 15× the tokens of a chat. Anthropic says plainly that coding has fewer parallelizable tasks than research.

### Cited findings
**"Effective harnesses for long-running agents" (published Nov 26, 2025; written with Opus 4.5, so the model is superseded but the pattern still applies)**: [Source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Two-phase design. "The very first agent session uses a specialized prompt that asks the model to set up the initial environment." That setup includes an init.sh script, a progress log (`claude-progress.txt`) and an initial git commit. After that, "Every subsequent session asks the model to make incremental progress, then leave structured updates."
- The two "agents" are the same harness. "We refer to these as separate agents in this context only because they have different initial user prompts."
- Feature list. The initializer writes a large feature file (the example has over 200 features for a claude.ai clone) with every feature marked failing. "We prompt coding agents to edit this file only by changing the status of a passes field". The file is JSON because "the model is less likely to inappropriately change or overwrite JSON files". The prompt guards it with "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."
- One feature per session. "the next iteration of the coding agent was then asked to work on only one feature at a time." The authors call this incremental approach critical.
- init.sh. Write "an `init.sh` script that can run the development server", then run a basic end-to-end test before starting new work.
- Git. Commit "with descriptive commit messages" so a bad change can be reverted, and leave a "clean state", meaning code that could be merged to main.
- Verification. Agents are told to use browser automation and "do all testing as a human user would". Testing tools "dramatically improved performance". One stated limitation: "Claude can't see browser-native alert modals through the Puppeteer MCP."
- The post names four failure modes and the fix for each:
  - "Claude declares victory on the entire project too early." Fix: the feature list.
  - "Claude leaves the environment in a state with bugs or undocumented progress." Fix: git plus progress notes.
  - "Claude marks features as done prematurely." Fix: self-verify before marking a feature as passing.
  - "Claude has to spend time figuring out how to run the app." Fix: init.sh.
- Open question in the post: "it's still unclear whether a single, general-purpose coding agent performs best across contexts". It suggests specialized testing, QA or cleanup agents might help.

**"How we built our multi-agent research system" (June 13, 2025; uses Opus 4 and Sonnet 4, now superseded)**: [Source](https://www.anthropic.com/engineering/multi-agent-research-system)
- Pattern: "a multi-agent architecture with an orchestrator-worker pattern, where a lead agent coordinates the process".
- Token cost: "agents typically use about 4× more tokens than chat interactions" and "multi-agent systems use about 15× more tokens than chats". Token usage alone explained about 80% of the performance variance on BrowseComp (paraphrase).
- Gain: "outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval".
- Fit for coding: "most coding tasks involve fewer truly parallelizable tasks than research". Domains that need shared context or have many inter-agent dependencies are poor fits (paraphrase).
- Parallelism: "the lead agent spins up 3-5 subagents in parallel rather than serially", which "cut research time by up to 90% for complex queries".
- Effort scaling: "Simple fact-finding requires just 1 agent with 3-10 tool calls"; "complex research might use more than 10 subagents with clearly divided responsibilities".
- Failure handling: "we built systems that can resume from where the agent was when the errors occurred", plus "deterministic safeguards like retry logic and regular checkpoints".
- Evaluation: "LLM-as-judge evaluation scales when done well" using "a single LLM call with a single prompt outputting scores from 0.0-1.0 and a pass-fail grade".
- Models: "Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents". Also: "upgrading to Claude Sonnet 4 is a larger performance gain than doubling the token budget on Claude Sonnet 3.7".

**"Effective context engineering for AI agents" (Sep 29, 2025)**: [Source](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Context rot. As context grows, the "model's ability to accurately recall information from that context decreases". Context is an "attention budget" that every token draws down.
- Three techniques for long-horizon work: compaction, structured note-taking (for example "your custom agent maintaining a NOTES.md file"), and sub-agents that each return "only a condensed, distilled summary of its work (often 1,000-2,000 tokens)".
- Just-in-time retrieval: keep lightweight references ("file paths, stored queries, web links, etc.") and load the content at runtime. Avoid "bloated tool sets that cover too much functionality."

**"Building effective agents" (Dec 19, 2024; older but foundational)**: [Source](https://www.anthropic.com/engineering/building-effective-agents)
- Definition: "Workflows are systems where LLMs and tools are orchestrated through predefined code paths". Agents direct their own process.
- Advice: find "the simplest solution possible, and only increasing complexity when needed."
- Patterns that map onto the factory:
  - Orchestrator-workers: "A central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results."
  - Evaluator-optimizer: "One LLM call generates a response while another provides evaluation and feedback in a loop."
  - Parallelization by sectioning or voting.
- "Code solutions are verifiable through automated tests."

**Claude Code best practices (current docs)**: [Source](https://code.claude.com/docs/en/best-practices)
- "Claude's context window fills up fast, and performance degrades as it fills."
- Verification is the core rule: "Give Claude a check it can run... It's the difference between a session you watch and one you walk away from." The docs list four escalating ways to gate on that check: in the prompt, a `/goal` condition, a Stop hook ("a deterministic gate"), or a second-opinion verification subagent or workflow, "so the agent doing the work isn't the one grading it."
- Spec first: have Claude interview you and write SPEC.md, then "start a fresh session to execute it". "The most useful specs are self-contained: they name the files and interfaces involved, state what is out of scope, and end with an end-to-end verification step".
- Writer/Reviewer: "A fresh context improves code review since Claude won't be biased toward code it just wrote."
- Adversarial review warning: "A reviewer prompted to find gaps will usually report some, even when the work is sound... Chasing every finding leads to over-engineering... Tell the reviewer to flag only gaps that affect correctness or the stated requirements".
- Hooks versus CLAUDE.md: "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens." Keep CLAUDE.md short: "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"
- Corrections: "After two failed corrections, `/clear` and write a better initial prompt".

### Inferences
- The long-running-harness post maps directly onto the factory: the spec-writer plays the initializer (feature list, init script), and the builder plays the coding agent (one feature per session, JSON status, commit plus progress file).
- The 15× multi-agent multiplier, and the post's own caveat about coding, argue for parallelism only where tasks really are independent. Reviewers of the same diff from different angles fit that. Builders sharing files do not.
- Best practices point to an independent reviewer with a fresh context and a correctness-only brief. This guards against review-driven over-engineering.

### Gaps
- No Anthropic engineering post dated 2026 on long-running harnesses turned up. The newest is Nov 2025.
- The long-running-harness post gives no cost or token figures.

## Q2. Inventory of Claude Code primitives for the factory pipeline

### Takeaway
The building blocks are:
- Subagents: per-role model, tools, effort and worktree, resumable with SendMessage.
- Hooks: deterministic gates (Stop, SubagentStop, PreToolUse, SessionStart), with `agent_type` in the input.
- `/goal`: a judge loop on the small fast model.
- Headless `-p`: JSON or stream-json output, `--json-schema`, `--permission-prompts none`, `--max-budget-usd`.
- Auto mode: a classifier for unattended permissions.
- `/code-review`: local, in a background subagent.
- `claude plugin eval`: with/without-plugin ablation and CI exit codes.

Dynamic workflows and agent teams are higher-level orchestrators, covered in Q3.

### Cited findings

**Subagents**: [Source](https://code.claude.com/docs/en/sub-agents)
- Frontmatter fields:
  - `model`: "`sonnet`, `opus`, `haiku`, `fable`, a full model ID such as `claude-opus-5-5`, or `inherit`".
  - `tools` and `disallowedTools`.
  - `permissionMode`.
  - `maxTurns`: "When the subagent reaches the limit, Claude Code returns its output marked as partial, and Claude can resume it to continue". Requires v2.1.246+.
  - `skills`: "The full skill content is injected, not only the description". Up to 32 skill names.
  - `memory`: `user`, `project` or `local`. Stored in `.claude/agent-memory/<name>/`. The first "200 lines or 25KB of `MEMORY.md`" are loaded.
  - `background: true`.
  - `effort`: low, medium, high, xhigh, max.
  - `isolation: worktree`: "run the subagent in a temporary git worktree... branched by default from your default branch rather than the parent session's `HEAD`. The worktree is automatically cleaned up if the subagent makes no changes."
  - `omitClaudeMd` (v2.1.271+).
  - `experimental.cacheTtl` (`5m` or `1h`).
  - `hooks` and `mcpServers`.
- Resume: "Claude uses the `SendMessage` tool with the agent's ID or name as the `to` field to resume it. `SendMessage` doesn't require agent teams to be enabled." "Resumed subagents retain their full conversation history." The built-in Explore and Plan agents "are one-shot and return no agent ID".
- Limits:
  - Nesting is allowed "up to three layers below the main conversation". Configure with `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`.
  - "when 20 subagents are running in a session, spawning another with the Agent tool fails with `Concurrent subagent limit reached`". Configure with `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`.
  - "There's no limit on the total number of subagents Claude can spawn over a session."
- Context: "Each subagent starts with a fresh, isolated context window." Its startup context includes CLAUDE.md (except for Explore and Plan) and a git status snapshot.
- Cost: subagent requests "count toward the same usage limits as your main conversation". "Control costs by routing tasks to faster, lower-cost models like Haiku." A fork reuses the parent's context, so "a fork costs less than a fresh subagent for tasks that need the same context."
- Gotchas:
  - Plugin subagents ignore `hooks`, `mcpServers` and `permissionMode`.
  - Project frontmatter hooks need folder trust, and "a `-p` session doesn't count as trusted."
  - "Claude Code removes every other built-in tool from a background subagent" (it gets a reduced tool set).
  - Transcripts are deleted after `cleanupPeriodDays`, 30 days by default.

**Hooks**: [Source](https://code.claude.com/docs/en/hooks)
- Events relevant to the factory:
  - `SessionStart`: "When a session begins or resumes". Matchers are startup, resume, clear, compact, fork. `additionalContext` is "String added to Claude's context... before the first prompt". Only command and mcp_tool handler types are allowed; "keep these hooks fast".
  - `PreToolUse`: "Can block it". Uses `permissionDecision` allow, deny, ask or defer. "`updatedInput`... replaces a tool's arguments before it runs".
  - `Stop`: exit 2 "Prevents Claude from stopping, continues the conversation".
  - `SubagentStop`: exit 2 "Prevents the subagent from stopping". The input includes `last_assistant_message`.
  - `TeammateIdle` and `TaskCompleted`.
- Identity fields: `agent_type` is "Agent name (for example, `"Explore"` or `"security-reviewer"`). Present when the session uses `--agent` or the hook fires inside a subagent." `agent_id` is "Unique identifier for the subagent or in-process teammate".
- Handler types and default timeouts: command, http and mcp_tool (600 s), prompt (30 s, "single-turn evaluation"), and agent (60 s, "experimental").
- Timeout behavior: "A timed-out `command`, `http`, or `mcp_tool` hook doesn't block the tool call". Use `onFailure: "block"` (v2.1.295+) to make a timeout block.
- Windows notes:
  - The shell "Defaults to `"bash"`, or to `"powershell"` on Windows when Git Bash isn't installed."
  - "`.cmd` and `.bat` shims... can't be spawned without a shell". Call `node` with the script path instead.
  - The PowerShell example uses `-NoProfile` and `-ExecutionPolicy Bypass`.
- The best-practices page links to a cap on consecutive Stop-hook blocks ("Stop input covers the cap on consecutive blocks"). [Source](https://code.claude.com/docs/en/best-practices)

**`/goal`**: [Source](https://code.claude.com/docs/en/goal)
- "`/goal` is a wrapper around a session-scoped prompt-based Stop hook. Each time Claude finishes a turn, Claude Code sends the condition and the conversation so far to your configured small fast model." The judge returns one of three verdicts: Not yet met, Met, or Impossible.
- What the judge can see: "It doesn't run commands or read files independently, so write the condition as something Claude's own output can demonstrate." "The condition can be up to 4,000 characters."
- Turn bounds: "To bound how long a goal runs, include a turn or time clause in the condition, such as `or stop after 20 turns`... the evaluator judges it from the conversation." There is no hard turn flag; the bound is judged by the model.
- Stall guard: "If Claude keeps answering the evaluator without making progress (no tool use for several turns in a row), Claude Code stops the loop".
- The goal clears on auth failure, exhausted credit, an unclearable context overflow, or an unavailable model. Other errors trigger up to 3 automatic retries or a pause.
- Background work defers evaluation. Check-ins start at 30 minutes and back off.
- Headless use: "Setting a goal with `-p` runs the loop to completion in a single invocation". Add `--output-format stream-json --verbose` to watch progress.
- Cost: "Evaluation tokens are billed on the small fast model... typically negligible". Change the judge with `ANTHROPIC_DEFAULT_HAIKU_MODEL`. That variable also changes the `haiku` alias and the background tasks.
- Requires workspace trust. It is disabled by `disableAllHooks`.

**Headless `-p`**: [Source](https://code.claude.com/docs/en/headless)
- Output formats are `text`, `json` and `stream-json`. `--json-schema` returns `structured_output`. JSON output includes `total_cost_usd` and a per-model breakdown, described as "client-side estimates".
- Exit code: "exits with code 0 on success and a non-zero code when the run fails".
- `--bare`: skips hooks, skills, agents, plugins, MCP, memory and CLAUDE.md. "recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release". It requires `ANTHROPIC_API_KEY` and does not use the subscription login.
- Trust: without `--bare`, "a `-p` session runs the hooks in a project's `.claude/settings.json`... even in a folder you've never trusted".
- `--permission-prompts none` (v2.1.259+): "Anything that would prompt is denied unless a `PermissionRequest` hook allows it, Claude is told that nobody can approve the request and not to retry it, and the run continues." It also removes `AskUserQuestion`. In stream-json, denials appear as `permission_denied` messages and are listed in `permission_denials`.
- Background work: a `-p` run waits for background subagents and workflows. Other idle background work is stopped after 10 minutes (`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`). Hitting `--max-budget-usd` stops background work.
- Subagent transcripts in stream-json: identified by `parent_tool_use_id`. `--forward-subagent-text` adds their text and thinking.
- Retries emit `system/api_retry` events. SIGTERM exits with code 143.
- Resume with `--resume <session_id>`. "Piped stdin is capped at 10MB."

**Permission modes and auto mode**: [Source](https://code.claude.com/docs/en/permission-modes.md)
- "A separate classifier model reviews actions before they run, blocking anything that escalates beyond your request, targets unrecognized infrastructure, or appears driven by hostile content". Auto mode is the default starting mode for interactive sessions in v2.1.283+.
- Classifier model: "The classifier runs on Claude Sonnet 5 by default rather than on your `/model` selection." The server-side review (v2.1.281+ for `-p`) avoids separate classifier calls.
- Billing: on Enterprise and API accounts, "classifier calls count toward your token usage". "Reads and working-directory edits outside protected paths skip the classifier".
- Subagents: the classifier checks the task at spawn, each action while the subagent runs, and the final report. "Any `permissionMode` in the subagent's frontmatter is ignored."
- Fallback: "if the classifier blocks an action 3 times in a row or 20 times total, auto mode pauses". In `-p` with no prompt tool, "the action doesn't run and Claude keeps working. Claude Code doesn't stop the run." These thresholds are "not configurable".
- Default blocks to know about:
  - Recursive deletes of unresolved shell variables.
  - Pushing to the current repo's branches is allowed by default (v2.1.261+), "including the default branch". A harness that must not auto-merge needs deny rules or branch protection.
  - Boundaries the user states, such as "don't push", become blocks.
- Alternatives: `dontAsk` is "for CI pipelines... the session never waits for input". `--dangerously-skip-permissions` requires "a container, VM, or the sandbox runtime".

**`/code-review`**: [Source](https://code.claude.com/docs/en/code-review.md)
- Local: "reviews a diff in your terminal". It "runs as a background subagent with its own context window". Flags are `--fix`, `--comment` and `--max-findings`.
- Effort: "At `low`, the review reports the findings it's most confident in... From `medium` through `max`, the review broadens coverage."
- In `-p` it runs in the foreground and "Claude Code waits for the review and includes the findings in the response".
- It reads CLAUDE.md, not REVIEW.md. `--fix` edits made in the background are not undone by `/rewind`.
- Managed GitHub Code Review: Team and Enterprise only, research preview. It is a multi-agent fleet with a verification step. "Each review averages $15-25", "completing in 20 minutes on average". The check run "always completes with a neutral conclusion", so gating needs your own CI to parse the `bughunter-severity` JSON.
- `/code-review ultra` runs in the cloud and needs a claude.ai account.

**`claude plugin eval`**: [Source](https://code.claude.com/docs/en/plugin-evals.md)
- Each case is a prompt plus graders. Grader types: `regex`, `tool_used`, `tool_order` and `file_exists` are free; `llm` and `baseline` call a judge.
- "each case runs three times by default".
- Baseline: "a case's runs are repeated with no plugin loaded, and you get two scores, `WITH` and `W/OUT`. Their difference, `Δ`, is what the plugin contributed."
- Cost: "roughly cases × runs agent runs with the plugin and the same number again for the no-plugin baseline, plus three short judge calls per `llm` or `baseline` grader per run". `--ablation none` "halves the cost".
- CI: `--threshold`, `--max-cost-usd`, `--trust-plugin` and `--json`. Exit codes: 0 for pass, 1 for below threshold or error, 2 for a partial run. "The with-minus-without delta is reported but never changes the exit code". Pin `--model` "so a model rollout isn't mistaken for a plugin regression".
- Windows: "Native Windows has no backend, so run shell-granting suites under WSL2". Without a sandbox backend, runs that grant Bash or PowerShell are refused.

**Agent view and background sessions** (research preview): [Source](https://code.claude.com/docs/en/agent-view)
- Usage: `claude agents` and `claude --bg "<prompt>"`. `--bg` cannot be combined with `-p`.
- "Before editing files, Claude moves the session into an isolated git worktree under `.claude/worktrees/`".
- A supervisor process runs the sessions, and each session is its own Claude Code process. "when memory stays low, the supervisor stops idle sessions" (paraphrase of the page). Idle unattached sessions stop after about an hour.
- Usage: "running ten agents in parallel uses quota roughly ten times as fast". Sessions are local and stop if the machine shuts down.

**Cross-session messaging**: [Source](https://code.claude.com/docs/en/cross-session-messaging.md)
- Requires v2.1.234+ on native Windows, where it uses a named pipe. Uses the `ListAgents` and `SendMessage` tools.
- Delivery: a message to an idle session "starts a new turn" and counts toward usage like a typed prompt.
- Trust: incoming messages "can't approve anything", "can't change configuration", and "Commands don't run".
- A `claude -p` worker binds an inbox, but bare mode does not. To let a `-p` worker take messages unattended, set `crossSessionInbound: accept` through `--settings`.
- Limits: plain text only, about 1M characters, at most 50 queued messages, and loop throttling. WSL 2 and native Windows sessions "can't reach each other".

**Prompt caching in Claude Code**: [Source](https://code.claude.com/docs/en/prompt-caching)
- TTL buckets: main conversation versus "Everything else" (subagents, workflows, teammates, forks, compaction). On a subscription within plan usage, the main conversation gets one hour and everything else gets five minutes. On an API key, both get five minutes. Change them with `promptCacheTtl` and `subagentPromptCacheTtl`, or the env vars `CLAUDE_CODE_PROMPT_CACHE_TTL` and `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL`.
- Subagents: "Its first request doesn't read the parent's cache, because the two prefixes differ". "A fork... inherits the parent's system prompt, tools, and conversation history exactly, so its first request reads the parent's cache." "Resumed subagents" can read the cache from their original run.
- Cache invalidators: model switches ("Each model has its own cache"), `opusplan` toggles, MCP or tool changes, compaction, and upgrades. On Opus 5.5, Sonnet 5.5 and Haiku 5.5 with an API key or subscription, changing effort keeps the cache.
- Scope: "the cache is effectively scoped to one machine and directory". Sequential sessions share the prefix only when the git-status snapshot matches. Implication (inference): worktrees, which are different directories, do not share cache with the main checkout.
- Editing CLAUDE.md mid-session doesn't apply until `/clear`, `/compact` or a restart.

**Costs**: [Source](https://code.claude.com/docs/en/costs)
- Typical spend: "around $13 per developer per active day and $150-250 per developer per month".
- Model choice: "Sonnet handles most coding tasks well and costs less than Opus. Reserve Opus for complex architectural decisions or multi-step reasoning... For simple subagent tasks, specify `model: haiku`".
- Thinking: "You can't turn off thinking on Opus 5.5, Sonnet 5.5, Haiku 5.5... Thinking tokens are billed as output tokens".
- Hooks: "a hook can grep for `ERROR` and return only matching lines, reducing context from tens of thousands of tokens to hundreds". Keep CLAUDE.md under 200 lines.

**API pricing (per MTok)**: [Source](https://platform.claude.com/docs/en/about-claude/pricing)

| Model | Input | Output | Cache read | 5m cache write | 1h cache write |
| :- | :- | :- | :- | :- | :- |
| Opus 5.5 | $4 | $20 | $0.20 | $5 | $8 |
| Sonnet 5.5 | $2 | $10 | $0.10 | $2.50 | $4 |
| Haiku 5.5 (≤100K prompt) | $0.10 | $0.50 | $0.01 | not noted | not noted |
| Haiku 5.5 (>100K prompt) | $0.50 | $2.50 | not noted | not noted | not noted |
| Fable 5.1 | $10 | $50 | $0.25 | not noted | not noted |

- "On Claude Opus 5.5 and Claude Sonnet 5.5, a cache hit costs 5% of the standard input price."
- The Batch API gives 50% off.

### Inferences
- A main-session orchestrator spawning subagents is the best-documented and best-controlled base. It supports per-role model, effort, tools and worktree; it can resume with SendMessage; and SubagentStop hooks can gate on `agent_type`.
- Reviewers fanned out as subagents with the same model, agent type and tools may still each pay their own first-request cache write. Prompt-prefix sharing between siblings is documented explicitly only for workflow fan-outs (Q3).
- For an unattended Windows run, use `-p` (or the interactive mode) with `--permission-mode auto` and `--permission-prompts none`, plus deny rules for `git push` and merge to protect main. Auto mode allows pushes to the current repo by default.

### Gaps
- No page documents per-session RAM for Claude Code processes. With 8 GB of RAM, the number of concurrent background sessions or teammates is unknown. Each background session is a full Claude Code process, while subagents run inside the parent process.
- The exact Stop-hook consecutive-block cap number was not fetched. The hooks page was truncated at 100k characters.

## Q3. Dynamic workflows and agent teams: is either a better orchestration base than a main-session orchestrator spawning subagents?

### Takeaway
Dynamic workflows are a strong candidate for the deterministic parts of the pipeline. The script holds the plan and the intermediate results, runs up to 16 agents concurrently (fewer on low-CPU machines) with up to 1,000 per run, and resumes within a session. They also work in `-p`. Their limits: no mid-run user input (so a human escalation must end the run), JS-only with no imports, and no direct filesystem access from the script.

Agent teams are a poor fit for an unattended factory:
- Experimental.
- Interactive-only: no teammates under `-p`.
- No `/resume`.
- No worktree isolation.
- No nested teams.
- Split panes are not supported in Windows Terminal.
- About 7× the tokens.

### Cited findings
**Dynamic workflows**: [Source](https://code.claude.com/docs/en/workflows)
- What they are: "A dynamic workflow is a JavaScript script that orchestrates many subagents at once. Claude writes the script... and a runtime executes it in the background while your session stays responsive."
- Comparison table:
  - Who decides what runs next: "The script". With subagents it is "Claude, turn by turn".
  - Where intermediate results live: "Script variables".
  - Scale: "Dozens to hundreds of agents per run".
  - Interruption: "Resumable in the same session".
- "A workflow script holds the loop, the branching, and the intermediate results itself, so Claude's context holds only the final answer."
- "it can have independent agents adversarially review each other's findings before they're reported".
- Script API: `agent()`, `pipeline()`, `parallel()`, `phase()`, `log()`, an `args` global, and `schema` for JSON output. If output fails validation "after five attempts, the call fails" (configurable with `MAX_STRUCTURED_OUTPUT_RETRIES`).
- Determinism: `Date.now()`, `Math.random()` and `new Date()` throw, "so that a relaunched run repeats the same `agent()` calls."
- Limits:
  - "No mid-run user input: A run pauses on its own only for agent permission prompts and a usage-limit wait. For sign-off between stages, run each stage as its own workflow."
  - "No direct filesystem or shell access from the workflow itself."
  - "No module loading."
  - "Up to 16 concurrent agents by default, fewer when Claude Code has fewer CPUs available". Configure with `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS`, from 1 to 256 (v2.1.269+).
  - "Up to 4,096 items in a single `parallel()` or `pipeline()` call".
  - "1,000 agents total per run".
- Failure handling:
  - "An `agent()` call resolves to `null` if you stop it mid-run or it hits an unrecoverable API error".
  - On resume, a completed agent returns its saved result, while a failed agent "runs again, and so does every agent that started after it, even ones that completed".
  - Stalls: an agent restarts "at most five times". After that, "Inside `parallel()` or `pipeline()`: the run carries on with `null`"; if the agent was "Awaited directly: the run ends with the error". The stall window is set per agent with `stallMs` or globally with `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS`.
  - Usage limits: the run pauses only when interactive and on a subscription. "A run doesn't pause in non-interactive mode with `claude -p`... in a background session". In those cases the agent fails.
- Leaving the session: a run survives exit only if moved to the background. Otherwise "the run stops with the session". Saved results allow a relaunch after `claude --resume`.
- Prompt caching: agents with the same "model, effort level, agent type, tools, output schema, and working directory" share a prefix. Claude Code holds siblings for up to 5 s (`CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS`) so they read the first agent's cache. The workflow TTL is 5 min unless `subagentPromptCacheTtl=1h`.
- Cost: "a single run can use meaningfully more tokens than working through the same task in conversation". There is an advisory `Large workflow` warning above 25 agents or 1.5M projected tokens. Size guideline settings: small <5, medium <10 (the default), large <50. Agent model order follows the subagent order, and the script can name a model per stage.
- Headless: workflows work in `-p` and the Agent SDK, but "the keyword `ultracode`" does not trigger from `-p`. The `Workflow` tool must be allowed by an allow rule (`Workflow` or `Workflow(<name>)`), auto mode, bypass, a PreToolUse hook, or a permission-prompt tool.
- Saving: saved to `.claude/workflows/` and run as `/<name>`, and can ship in plugins.
- Ultracode: "each request uses more tokens and takes longer". It removes the concurrent subagent cap and the large-workflow warning.

**Agent teams**: [Source](https://code.claude.com/docs/en/agent-teams)
- Status: "Agent teams are experimental and disabled by default" (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).
- Headless: "In non-interactive mode with the `-p` flag, including Agent SDK sessions, Claude doesn't spawn teammates".
- Positioning: "Agent teams add coordination overhead and use significantly more tokens than a single session... For sequential tasks, same-file edits, or work with many dependencies, a single session or subagents are more effective."
- Mechanics: a shared task list with dependencies, where "Task claiming uses file locking", plus mailboxes as JSON files under `~/.claude/teams/`. Quality gates are the `TeammateIdle`, `TaskCreated` and `TaskCompleted` hooks (exit 2 blocks).
- Size: "Start with 3-5 teammates for most workflows."
- Limitations:
  - "No session resumption with in-process teammates."
  - "Task status can lag."
  - "One team per session."
  - "No nested teams."
  - "No background subagents from in-process teammates."
  - "Lead is fixed."
  - "Split-pane mode isn't supported in VS Code's integrated terminal, Windows Terminal, or Ghostty."
- Teammate definitions: `skills` in a subagent definition is not applied to teammates.
- Permissions: teammate permission prompts surface in the lead.
- Failures: "Teammates may stop after encountering errors instead of recovering". "The lead can stop early too".
- Isolation: "Agent teams don't isolate teammates in worktrees". [Source](https://code.claude.com/docs/en/agents)
- Cost: "Agent teams use approximately 7x more tokens than standard sessions when teammates run in plan mode". The docs recommend "Use Sonnet for teammates." [Source](https://code.claude.com/docs/en/costs)
- Side effect: enabling teams turns named subagents into teammates, so "teams can form even when you didn't ask for one".

**Overview page**: [Source](https://code.claude.com/docs/en/agents)
- "Running several sessions or subagents at once multiplies token usage."
- `/batch` "has Claude split one large change into 5 to 30 worktree-isolated subagents".

### Inferences
- A hybrid looks best, though no source states this directly:
  - A thin main-session orchestrator, or a `-p` driver script, runs each stage.
  - The fan-out stage (parallel specialist reviewers, then an approver that merges their findings) runs as a saved dynamic workflow. That gains cache-prefix sharing, structured JSON outputs, stall retries and resumability, and keeps reviewer transcripts out of the orchestrator's context.
  - Human escalation happens between workflow runs, because workflows cannot take mid-run input.
- Agent teams should be avoided for this pipeline: no headless mode, no resume, no worktree isolation, and the experimental flag also changes how normal subagents behave.
- 8 GB RAM and Windows: the workflow concurrency cap already scales down with CPU count, but nothing is documented about RAM. Setting `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` low (for example 3-4) and `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` low is a prudent untested default. Workflow agents are subagents inside the runtime, not separate OS processes, but this is not explicitly stated. Background sessions and agent view do spawn separate processes, and their supervisor stops idle sessions under memory pressure.

### Gaps
- None of the docs give RAM or CPU figures per agent or session.
- Whether workflow agents can use `isolation: worktree` per agent is implied ("working on each file in its own isolated copy") but the option name was not shown.
- No published benchmark compares workflows with orchestrator-plus-subagents on coding quality.

## Q4. What does Anthropic say about model choice per role and effort levels?

### Takeaway
Anthropic's guidance for Claude Code:
- Sonnet is the default worker. Opus is for architecture and hard reasoning. Haiku is for simple subagent tasks and judges.
- Sonnet for agent-team teammates.
- The 2025 research system used Opus as lead and Sonnet as workers.
- Opus 5.5, Sonnet 5.5 and Haiku 5.5 default to `medium` effort. `high` is for bug-fixing where verification matters; `max` is for unattended hard problems such as security, but "prone to overthinking".

### Cited findings
- Model aliases [Source](https://code.claude.com/docs/en/model-config):
  - `sonnet` "for daily coding tasks", `opus` "for complex reasoning tasks", `haiku` "for simple tasks", `fable` "for your hardest and longest-running tasks".
  - On the Anthropic API, `opus`, `sonnet` and `haiku` map to Opus 5.5, Sonnet 5.5 and Haiku 5.5. Subscriptions and the API default to Opus 5.5.
  - `opusplan` "uses `opus` during plan mode, then switches to `sonnet` for execution". Each toggle is a cache-breaking model switch.
- Effort defaults [Source](https://code.claude.com/docs/en/model-config): "`high` on every model that supports effort, except that Opus 5.5, Sonnet 5.5, and Haiku 5.5 default to `medium`".
  - `medium`: "day-to-day engineering work with a clear scope, such as implementing a new feature".
  - `high`: "Work where verification matters or edge cases are likely, such as fixing a bug in an existing codebase".
  - `xhigh`: "Deeper reasoning at higher token spend".
  - `max`: "Hard problems you want Claude to work through without you, such as finding security vulnerabilities. `max` may show diminishing returns and is prone to overthinking, so test before adopting it broadly".
- Context: Sonnet 5+, Haiku 5.5 and Opus 4.7+ run with 1M context by default and auto-compact at about 967K. "Haiku 5.5 costs more on prompts longer than 100K tokens." [Source](https://code.claude.com/docs/en/model-config)
- Costs guidance: "Sonnet handles most coding tasks well and costs less than Opus. Reserve Opus for complex architectural decisions or multi-step reasoning." [Source](https://code.claude.com/docs/en/costs)
- Teams: "Use Sonnet for teammates." [Source](https://code.claude.com/docs/en/costs)
- Best-practices example: the security-reviewer subagent uses `model: opus`. [Source](https://code.claude.com/docs/en/best-practices)
- Research system (2025, older models): "Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents". [Source](https://www.anthropic.com/engineering/multi-agent-research-system)
- Judges:
  - `/goal` uses the small fast model (Haiku-class) by default. [Source](https://code.claude.com/docs/en/goal)
  - Plugin-eval judges default to the background-task model. The docs warn: "A small judge model can mark a correct answer wrong because it's formatted differently... Re-run with `--judge-model sonnet`". [Source](https://code.claude.com/docs/en/plugin-evals.md)
  - The auto-mode classifier runs on Sonnet 5. [Source](https://code.claude.com/docs/en/permission-modes.md)
- Code review effort: `low` gives the highest-confidence findings and fewer false positives; `medium` to `max` broaden coverage. [Source](https://code.claude.com/docs/en/code-review.md)
- Price ratio: Opus 5.5 costs 2× Sonnet 5.5 ($4/$20 vs $2/$10 per MTok), and Haiku 5.5 is 20× cheaper than Sonnet 5.5 for prompts up to 100K. [Source](https://platform.claude.com/docs/en/about-claude/pricing)
- Effort and cache: on the 5.5 models with an API key or subscription, changing effort mid-session keeps the cache. [Source](https://code.claude.com/docs/en/prompt-caching)

### Inferences
Suggested role mapping, derived from the docs but not stated by Anthropic for this pipeline:

| Role | Model | Effort |
| :- | :- | :- |
| Spec-writer | Opus 5.5 | medium/high |
| Builder | Sonnet 5.5 | medium, high for bug fixes |
| Specialist reviewers | Sonnet 5.5; Opus only for security | medium-high |
| Approver / judge | Sonnet, not Haiku | — |
| Mechanical gates | Prefer deterministic hooks or scripts over any model | — |

- Approver: Sonnet rather than Haiku, given the plugin-eval warning about small judges.
- Keep each role on a fixed model and effort for its whole session to avoid cache rebuilds.

### Gaps
- The model announcement pages for Opus 5.5, Sonnet 5.5 and Haiku 5.5 (benchmarks, recommended agent uses) were not fetched. Per-model coding benchmark claims are therefore missing.
- No Anthropic source gives a quantitative quality comparison of effort levels for agentic coding.
