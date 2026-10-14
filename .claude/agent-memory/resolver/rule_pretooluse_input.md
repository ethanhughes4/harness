---
name: rule-pretooluse-input
description: PreToolUse tool_input fields - Bash uses tool_input.command, Write/Edit use tool_input.file_path (always absolute)
metadata:
  type: reference
---

Rule: PreToolUse stdin has `tool_name` and `tool_input`. Bash -> `tool_input.command`; Write and Edit -> `tool_input.file_path` (absolute).

Quotes (code.claude.com/docs/en/hooks, PreToolUse input, checked 2026-10-14):
- Bash: "| `command` | string | `\"npm test\"` | The shell command to execute |"
- Write: "| `file_path` | string | `\"/path/to/file.txt\"` | Absolute path to the file to write |"
- Edit: "| `file_path` | string | `\"/path/to/file.txt\"` | Absolute path to the file to edit |"
- "For the file tools `Write`, `Edit`, and `Read`, `tool_input.file_path` is always absolute."

Link: https://code.claude.com/docs/en/hooks#pretooluse-input
Related: [[rule-hook-exit2-blocking]]
