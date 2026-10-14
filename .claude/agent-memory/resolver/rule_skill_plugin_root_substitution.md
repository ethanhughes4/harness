---
name: rule-skill-plugin-root-substitution
description: ${CLAUDE_PLUGIN_ROOT} and ${CLAUDE_PLUGIN_DATA} ARE substituted in a plugin skill's markdown body and allowed-tools Bash rules
metadata:
  type: reference
---

Rule: in a plugin skill, `${CLAUDE_PLUGIN_ROOT}` (plugin install dir, not the skill subdir) is substituted in the SKILL.md content and in `allowed-tools` Bash rules. `${CLAUDE_SKILL_DIR}` is the skill's own subfolder.

Quotes (checked 2026-10-14, https://code.claude.com/docs/en/skills, "Available string substitutions"):
- Table row: "`${CLAUDE_PLUGIN_ROOT}` | The plugin's installation directory. Substituted only in plugin skills."
- "In a plugin skill, Claude Code substitutes `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_PLUGIN_DATA}` in the same two places." (the two places: "the skill's markdown content, and Bash rules in the `allowed-tools` frontmatter")

Settles the "unconfirmed" reason in decision D35 for skills (agents not checked). Related: [[rule-hook-exec-form]], [[rule-plugin-skill-name]]
