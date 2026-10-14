---
name: rule-agent-skills-preload
description: Agent `skills` field preloads full skill content; missing/disabled names skipped with a debug-log warning; docs do NOT say bare vs plugin:skill for plugin agents
metadata:
  type: reference
---

Rule: the agent `skills` field injects each listed skill's full content at startup (first 32 distinct names). A missing or disabled name is skipped with a warning in the debug log only. Plugin agents support `skills`. The docs do NOT say whether a plugin agent should write its own plugin's skill as `plugin:skill` or bare (checked 2026-10-14) — unresolved, confirm live.

Quotes (checked 2026-10-14):
- https://code.claude.com/docs/en/sub-agents#preload-skills-into-subagents : "The full content of each listed skill is injected into the subagent's context at startup, up to the first 32 distinct names in the list."
- same: "If a listed skill is missing or disabled, for example by your organization's policy, Claude Code skips it and logs a warning to the debug log."
- same: "You can't preload skills that set `disable-model-invocation: true`, since preloading draws from the same set of skills Claude can invoke."
- https://code.claude.com/docs/en/plugins/components (Frontmatter fields in plugin agents): "**Supported fields**: `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, ..."
- https://code.claude.com/docs/en/skills : "The bare `/fancy` also invokes the skill unless another command already uses that name." (about slash commands, not the agent field)

Docs example uses bare names only (project skills). Related: [[rule-plugin-skill-name]]
