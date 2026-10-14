---
name: rule-stopfailure-input
description: StopFailure hook stdin fields (error, error_details, last_assistant_message + common cwd) and that its matcher filters on the error type
metadata:
  type: reference
---

Rule: StopFailure gets the common fields (incl. `cwd`) plus `error`, optional `error_details`, optional `last_assistant_message`. Matcher filters on `error`. Output and exit code ignored (logging only).

Quotes (checked 2026-10-14, https://code.claude.com/docs/en/hooks):
- "In addition to the common input fields, StopFailure hooks receive `error`, optional `error_details`, and optional `last_assistant_message`. The `error` field identifies the error type and is used for matcher filtering."
- Common input fields table: "`cwd` | Current working directory when the hook is invoked"
- Matcher table: "`StopFailure` | error type | `rate_limit`, `overloaded`, `authentication_failed`, ... `unknown`"
- "`FileChanged` and `StopFailure` use a narrower exact-match set of letters, digits, `_`, and `|` only."

Related: [[rule-hook-exec-form]]
