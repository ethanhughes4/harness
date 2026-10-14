---
name: rule-eval-slash-and-workspace
description: plugin eval runs are claude -p in an empty workspace; plugin files not readable; /plugin:skill in the prompt is expanded in -p (user-only skills too); unknown /name in baseline goes to Claude as plain text
metadata:
  type: reference
---

Checked 2026-10-14.

- Empty workspace: "Each run starts in an empty working directory, so put whatever the task needs in the prompt itself, or set up the workspace first." https://code.claude.com/docs/en/plugin-evals
- Run = -p child: "the agent under test runs there as a `claude -p` child process with only your plugin loaded." Same page, #how-runs-are-isolated. add_dirs are "Directories inside the case directory", read-only. "A run can't read the eval directory". Nothing says the plugin directory is readable.
- Body not rewritten: "Claude receives the body exactly as you wrote it. `@path` mentions in it aren't expanded" (plugin-evals). The page says nothing about slash commands.
- -p expands user-invoked skills: "User-invoked skills and custom commands work. Include `/skill-name` in the prompt string and Claude Code expands it before running." https://code.claude.com/docs/en/headless
- disable-model-invocation: you can invoke = Yes, Claude can = "Not on its own", "Description not in context". https://code.claude.com/docs/en/skills
- Baseline (no plugin), unknown /name: "doesn't fail the query. Claude Code sends the prompt to Claude as an ordinary message, with a note that the command didn't run" (v2.1.274+). https://code.claude.com/docs/en/agent-sdk/slash-commands

Gap: plugin-evals never states slash expansion for case prompts. That conclusion is an inference from "-p child" plus the headless note. Confirm it with one run.

Related: [[rule-plugin-eval-case-format]] [[rule-plugin-skill-name]]
