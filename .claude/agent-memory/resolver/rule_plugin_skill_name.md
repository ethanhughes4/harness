---
name: rule-plugin-skill-name
description: Skill name defaults to its folder; plugin skills run as /plugin-name:skill-name; frontmatter name replaces the folder part
metadata:
  type: reference
---

Rule: with no `name` frontmatter a skill is named after its directory. Plugin skills are namespaced `/plugin-name:skill-name` (plugin-name from .claude-plugin/plugin.json `name`).

Quotes (checked 2026-10-14, https://code.claude.com/docs/en/skills):
- `name` field: "Command name shown in the `/` menu. Defaults to the directory name."
- Where skills live, Plugin row: "Wherever the plugin is enabled, as `/plugin-name:skill-name`"
- "In a plugin skill, the frontmatter `name` replaces the directory name in the last segment of the command, so `my-plugin/skills/review/SKILL.md` with `name: fancy` becomes `/my-plugin:fancy`."

Related: [[rule-hook-exec-form]]
