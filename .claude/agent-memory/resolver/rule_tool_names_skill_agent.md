---
name: rule-tool-names-skill-agent
description: Skill and Agent are exact tool names valid in subagent tools lists; Skill in tools lets the agent invoke skills (skills field is only for preloading)
metadata:
  type: reference
---

Rule (checked 2026-10-14): `Skill` and `Agent` are built-in tool names usable in a `tools` list. Listing `Skill` lets the agent invoke skills; the `skills` field only preloads content. Omitting `Skill` blocks skill invocation.

Quotes:
- https://code.claude.com/docs/en/tools-reference : "The tool names are the exact strings you use in permission rules, subagent tool lists, and hook matchers." Table: "`Skill` | Executes a skill within the main conversation | Yes" (permission required = Yes).
- https://code.claude.com/docs/en/sub-agents : "To prevent a subagent from invoking skills entirely, omit `Skill` from the `tools` list or add it to `disallowedTools`." and tools row: "To preload Skills into context, use the `skills` field rather than listing `Skill` here".

Related: [[rule-agent-main-session]], [[rule-code-review-skill-invocation]]
