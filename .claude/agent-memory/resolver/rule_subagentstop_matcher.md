---
name: rule-subagentstop-matcher
description: SubagentStop/SubagentStart matcher filters agent type; plugin agents report plugin:agent; a colon makes the matcher an unanchored JS regex, so anchor ^...$
metadata:
  type: reference
---

Rule: SubagentStop matcher filters on agent type (same values as SubagentStart). Plugin agents report `plugin:agent` (e.g. `harness:builder`). Matchers with only letters/digits/_/-/space/,/| are exact strings; any other character (e.g. `:`, `^`) makes it an unanchored JavaScript regex, so use `^harness:builder$`.

Quotes (code.claude.com/docs/en/hooks, checked 2026-10-14):
- Matcher table: "`SubagentStop` | agent type | same values as `SubagentStart`"
- SubagentStart: "For subagents shipped by a plugin, the agent type is the plugin-scoped identifier such as `my-plugin:reviewer`, not the bare frontmatter name. The colon places a plugin-scoped name on the regular-expression path, so anchor the matcher with `^` and `$` for an exact match: `^my-plugin:reviewer$`."
- Matcher rules: "| Contains any other character | JavaScript regular expression, unanchored |"

Link: https://code.claude.com/docs/en/hooks#subagentstart
Related: [[rule-hook-exit2-blocking]], [[rule-plugin-skill-name]]
