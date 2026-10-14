---
name: rule-project-trust-allow-rules
description: project .claude/settings.json allow rules need workspace trust (also under -p); env/hooks used under -p untrusted; defaultMode auto/bypassPermissions ignored in project settings
metadata:
  type: reference
---

Rules:
1. `permissions.allow` + `additionalDirectories` in project `.claude/settings.json` apply only after the folder is trusted. `claude -p` never shows the dialog and does NOT apply them in an untrusted folder (stderr warning "this workspace has not been trusted"). Trust = accept dialog interactively once, or set `projects["<repo root>"].hasTrustDialogAccepted: true` in ~/.claude.json. Worktrees use the main checkout root.
2. Under `-p`, untrusted: hooks, the `env` block, skill allowed-tools ARE used.
3. `permissions.defaultMode` `auto`/`bypassPermissions` don't take effect from project or local settings.

Quotes (checked 2026-10-14):
- https://code.claude.com/docs/en/permissions#project-allow-rules-and-workspace-trust: "`permissions.allow` rules and `permissions.additionalDirectories` entries in a project's `.claude/settings.json` grant capability, so Claude Code applies them only after you accept the workspace trust dialog for that folder."
- same page, "What runs before you trust a folder", `claude -p` column for allow rules: "Not used. Claude Code prints a `this workspace has not been trusted` warning to stderr"
- https://code.claude.com/docs/en/settings: "`permissions.defaultMode` values `auto` and `bypassPermissions` don't take effect from project or local settings; set them in user or managed settings instead, or pass `--permission-mode` for one session."

Related: [[rule-permission-prompts-none]]
