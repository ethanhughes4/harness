---
name: rule-hook-exit2-blocking
description: Exit code 2 for PreToolUse blocks the tool (stderr = denial reason to Claude); for Stop keeps Claude going, for SubagentStop keeps the subagent running (stderr delivered to it)
metadata:
  type: reference
---

Rule: exit 2 blocks. stderr is the message.
- PreToolUse: tool call blocked; Claude sees stderr as the denial reason.
- Stop: Claude continues; stderr is the reason it should continue.
- SubagentStop: the subagent keeps running; stderr goes to the subagent (not the parent).

Quotes (code.claude.com/docs/en/hooks, checked 2026-10-14):
- Exit-code table: "`PreToolUse` | Yes | Blocks the tool call"; "`Stop` | Yes | Prevents Claude from stopping, continues the conversation"; "`SubagentStop` | Yes | Prevents the subagent from stopping"
- PreToolUse: "A hook that blocks by exiting 2 routes the same way as `\"deny\"`: Claude sees the stderr message as the denial reason."
- Stop: "A hook that blocks by exiting 2 routes the same way as `reason`: Claude receives the stderr message as the explanation for why it should continue."
- SubagentStop: "Returning `decision: \"block\"` with a `reason` keeps the subagent running and delivers `reason` to the subagent as its next instruction. A hook that blocks by exiting 2 delivers its stderr message the same way."

Link: https://code.claude.com/docs/en/hooks#exit-code-2-behavior-per-event
Related: [[rule-pretooluse-input]], [[rule-subagentstop-matcher]]
