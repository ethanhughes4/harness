---
name: rule-code-review-skill-invocation
description: /code-review is a bundled skill Claude can start itself; docs only name project/user/plugin skills as invocable from subagents, so bundled-from-subagent is unstated
metadata:
  type: reference
---

- https://code.claude.com/docs/en/skills : "Claude Code includes a set of bundled skills, such as `/doctor`, `/code-review`, `/batch`, `/debug`, `/loop`, and `/claude-api`." The sentence "A few built-in commands are also available through the Skill tool, including `/init` and `/security-review`" is about built-in commands, not bundled skills. Permission table: "`Skill(review)` | The bundled `/code-review`, through its `/review` alias".
- https://code.claude.com/docs/en/code-review#let-claude-start-the-review : "Claude can start `/code-review` on its own." In -p it runs in the foreground: "You run it in non-interactive mode, with the `-p` flag or the Agent SDK; Claude Code waits for the review and includes the findings in the response". "`/code-review` runs the review as a forked subagent".
- https://code.claude.com/docs/en/sub-agents : "Subagents can still invoke unlisted project, user, and plugin skills through the Skill tool." Bundled skills are NOT named. Nesting: "By default, a subagent can spawn subagents of its own, up to three layers below the main conversation."
- Conclusion (2026-10-14): main session can call it (documented); a subagent calling it is not stated plainly.
