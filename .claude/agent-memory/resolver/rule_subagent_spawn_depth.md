---
name: rule-subagent-spawn-depth
description: CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH = subagent layers below main (default 3); positive whole number only, else ignored; 1 = no nesting
metadata:
  type: reference
---

Rule: env var `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` sets how many subagent layers sit below the main conversation. Default 3 (since v2.1.219). Positive integer in plain digits; anything else ignored.

Quote (checked 2026-10-14, https://code.claude.com/docs/en/env-vars):
"Number of subagent layers allowed below the main conversation (default: 3). ... set `1` to turn nesting off. ... Accepts a positive whole number in plain digits; anything else is ignored, so the limit can be adjusted but not removed. Requires Claude Code v2.1.217 or later"

Can be set via settings `env` block (only telemetry export vars are ignored there, per https://code.claude.com/docs/en/settings). Related: [[rule-project-trust-allow-rules]]
