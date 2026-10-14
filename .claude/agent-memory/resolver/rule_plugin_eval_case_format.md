---
name: rule-plugin-eval-case-format
description: claude plugin eval case layout, prompt.md fields, grader types/options, --allow-tools set, Agent dispatch by namespaced name, which graders are unscored in two-arm runs
metadata:
  type: reference
---

Source: https://code.claude.com/docs/en/plugin-evals (checked 2026-10-14)

- Layout: "A directory counts as a case when it holds a `prompt.md` or a `case.yaml`, and a case without at least one grader fails to load". Grader name = filename without .md.
- prompt.md: "`prompt.md` frontmatter accepts these fields. An unknown key is an error" — schema_version, name, description, tags, plugins, runs, expected_outcome ("For humans. Not used at run time"), model, max_turns (default 10, up to 200), timeout_seconds, allowed_tools, append_system_prompt, env (keys must match EVAL_*).
- Tools: "A run allows only the read-only tools the case lists in `allowed_tools`, from `Read`, `Glob`, `Grep`, `NotebookRead`, `Skill`, `AskUserQuestion`, `Agent`, `TodoWrite`, and the task tools ... plus whatever you grant with `--allow-tools`. ... To let cases use `Bash`, `Write`, `Edit`, `WebFetch`, or `WebSearch`, grant them yourself"
- regex: "The JavaScript regex `pattern` is found in the target. Set `match: not_contains` to require absence ... Put case-insensitivity in `flags: i`". Default target last_message.
- tool_used: "The number of calls to `tool` whose JSON-encoded input matches the optional `input_match` regex is between `min`, default 1, and `max`".
- Agents: "a case that lists `Agent` in `allowed_tools` can dispatch one of your plugin's agents by its namespaced name, such as `my-plugin:code-reviewer`". Baseline arm fails with "Agent type '<plugin>:<agent-name>' not found".
- Unscored in two-arm runs only: "Every `tool_used` grader whose `tool` is `Skill`", mock_calls graders, "Any grader you mark `arm: with-only`". So a tool_used: Agent grader on a plugin agent needs `arm: with-only` or it inflates Δ.

Related: [[rule-plugin-skill-name]]
