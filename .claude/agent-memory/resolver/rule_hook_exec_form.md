---
name: rule-hook-exec-form
description: Plugin hooks/hooks.json wrapper shape, and command-hook exec form (command + args) with ${CLAUDE_PLUGIN_ROOT} substituted inside args
metadata:
  type: reference
---

Rule: plugin hooks live in `hooks/hooks.json` as `{"description"?, "hooks": {"<Event>": [{"matcher"?, "hooks": [{"type":"command", ...}]}]}}`. A command hook with `args` runs in exec form (no shell); `${CLAUDE_PLUGIN_ROOT}` is substituted into `command` and each `args` element.

Quotes (checked 2026-10-14, https://code.claude.com/docs/en/hooks):
- "Define plugin hooks in `hooks/hooks.json` with an optional top-level `description` field." (example shows `"hooks": {"PostToolUse": [{"matcher": ..., "hooks": [{"type": "command", ...}]}]}`)
- "A command hook runs as exec form when `args` is set, and shell form when `args` is omitted."
- "Exec form runs when `args` is present. Claude Code resolves `command` as an executable on `PATH` and spawns it directly with `args` as the argument vector. There is no shell, so each `args` element is one argument exactly as written, and path placeholders like `${CLAUDE_PLUGIN_ROOT}` are substituted into `command` and into each `args` element as plain strings."
- Example: `{"type": "command", "command": "node", "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/format.js", "--fix"]}`

Related: [[rule-stopfailure-input]], [[rule-plugin-skill-name]]
