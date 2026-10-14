---
name: rule-agent-main-session
description: --agent main thread takes the agent's tools, model, system prompt; can spawn subagents via Agent / Agent(type) allowlist; maxTurns documented only for subagents
metadata:
  type: reference
---

Rules (checked 2026-10-14):
1. `--agent <name>`: main thread takes the agent's tool restrictions, model and system prompt (replaces the default prompt; CLAUDE.md still loads; omitClaudeMd ignored).
2. Main thread under `--agent` can spawn subagents with the Agent tool. `Agent(a, b)` in `tools` is an allowlist (only for main-thread agents); bare `Agent` = any type; omit = none.
3. `maxTurns` is defined only as a subagent cap ("before the subagent stops", output marked partial). No doc says it applies to an `--agent` main session. The documented main-session cap is `--max-turns` (print mode, exits with error). Neither is a /goal-turn count.
4. Plugin agents: supported fields include model, maxTurns, tools, color; ignored: permissionMode, hooks, mcpServers, initialPrompt. Name form `<plugin>:<name>`.

Quotes:
- https://code.claude.com/docs/en/sub-agents : "Pass `--agent <name>` to start a session where the main thread itself takes on that subagent's tool restrictions and model" / "Unless the agent's prompt is empty, a custom subagent's system prompt replaces the default Claude Code system prompt entirely, the same way `--system-prompt` does."
- same page: "When an agent runs as the main thread with `claude --agent`, it can spawn subagents using the Agent tool. To restrict which subagent types it can spawn, use `Agent(agent_type)` syntax in the `tools` field." / "To allow spawning any subagent without restrictions, use `Agent` without parentheses"
- same page, maxTurns row: "Maximum number of agentic turns before the subagent stops. When the subagent reaches the limit, Claude Code returns its output marked as partial"
- https://code.claude.com/docs/en/cli-reference : "`--max-turns` | Limit the number of agentic turns (print mode only). Exits with an error when the limit is reached. No limit by default."
- https://code.claude.com/docs/en/plugins/components#frontmatter-fields-in-plugin-agents : "**Supported fields**: `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, ..." and "The name form is `<plugin>:<name>`"

Related: [[rule-tool-names-skill-agent]], [[rule-goal-noninteractive]], [[rule-subagentstop-matcher]]
