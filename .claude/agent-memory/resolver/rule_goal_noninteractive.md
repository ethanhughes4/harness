---
name: rule-goal-noninteractive
description: /goal works under -p as the prompt; turn bound = clause in the condition judged by evaluator; combination with --agent not documented
metadata:
  type: reference
---

Rules (checked 2026-10-14):
1. `claude -p "/goal <condition>"` runs the goal loop to completion in one invocation.
2. Turn bound: put "or stop after N turns" in the condition; the evaluator (small fast model, no tools) judges it from the conversation. Not enforced by maxTurns/--max-turns.
3. /goal follows the workspace trust rule for settings hooks; unavailable if disableAllHooks or allowManagedHooksOnly.
4. No doc page states /goal together with `--agent`. Unverified; confirm by a smoke run.

Quotes:
- https://code.claude.com/docs/en/goal#run-non-interactively : "`/goal` works in non-interactive mode ... Setting a goal with `-p` runs the loop to completion in a single invocation"
- https://code.claude.com/docs/en/goal#write-an-effective-condition : "To bound how long a goal runs, include a turn or time clause in the condition, such as `or stop after 20 turns`. Claude reports progress against that clause each turn and the evaluator judges it from the conversation."
- https://code.claude.com/docs/en/goal#requirements : "Claude Code makes `/goal` available under the same workspace trust rule as hooks in settings files"

Related: [[rule-agent-main-session]], [[rule-project-trust-allow-rules]]
