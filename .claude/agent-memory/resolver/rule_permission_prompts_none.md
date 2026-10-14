---
name: rule-permission-prompts-none
description: claude -p --permission-prompts none denies anything that would prompt (after rules, hooks, mode/classifier decide); run continues, never waits
metadata:
  type: reference
---

Rule: with `--permission-prompts none` (v2.1.259+), rules, PermissionRequest hooks and the permission mode (auto = classifier) decide first; whatever would still prompt is denied, Claude is told not to retry, and the run continues. AskUserQuestion is removed. Denials show as `permission_denied` messages and in the result's `permission_denials`.

Quotes (checked 2026-10-14, https://code.claude.com/docs/en/headless#turn-off-permission-prompts-in-unattended-runs):
- "With the flag, your run doesn't consult the host or wait on it. Anything that would prompt is denied unless a `PermissionRequest` hook allows it, Claude is told that nobody can approve the request and not to retry it, and the run continues."
- "The classifier reviews each action as usual, and Claude Code denies anything that would have fallen back to a prompt"
CLI row (https://code.claude.com/docs/en/cli-reference): "Pass `none` when nobody can answer, and Claude Code denies them instead."

Related: [[rule-project-trust-allow-rules]]
