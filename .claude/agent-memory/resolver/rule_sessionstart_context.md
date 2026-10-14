---
name: rule-sessionstart-context
description: SessionStart matcher "compact" fires on auto/manual compaction; context added via hookSpecificOutput.additionalContext JSON or plain stdout
metadata:
  type: reference
---

Rule: SessionStart matcher `compact` = "Auto or manual compaction". A SessionStart hook adds context with
`{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "..."}}` on stdout; plain-text stdout also works.

Quotes (code.claude.com/docs/en/hooks, checked 2026-10-14):
- Matcher table row: "| `compact` | Auto or manual compaction |"
- Decision control: "`additionalContext` | String added to Claude's context at the start of the conversation, before the first prompt."
- "A hook that only adds context can print it without building JSON, because Claude Code adds a SessionStart hook's plain-text stdout to Claude's context."
- Doc example: `{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "Current branch: ..."}}`

Link: https://code.claude.com/docs/en/hooks#sessionstart
Related: [[rule-hook-exec-form]]
