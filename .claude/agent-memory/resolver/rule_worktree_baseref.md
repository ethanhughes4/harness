---
name: rule-worktree-baseref
description: settings worktree.baseRef accepts only "fresh" (default, remote default branch) or "head" (local HEAD); subagent isolation:worktree follows it
metadata:
  type: reference
---

Rule: `worktree.baseRef` takes `"fresh"` (default) or `"head"`; no branch names. Subagent `isolation: worktree` uses the same base.

Quotes (checked 2026-10-14, https://code.claude.com/docs/en/worktrees#choose-the-base-branch):
- "The setting accepts two values:" ... "`\"head\"`: branch from your current local `HEAD`, so the worktree carries your unpushed commits and feature-branch state."
- "Subagent worktrees use the same base branch as `--worktree`, so they branch from your repository's default branch unless `worktree.baseRef` is set to `\"head\"`."

Related: [[rule-subagent-spawn-depth]]
