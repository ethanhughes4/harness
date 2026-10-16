# Harness

A Claude Code plugin that turns an idea into a built, tested project: an intake interview, a spec, a
feature list, and a guarded build loop (test writer, builder, gates, reviewers, merge). Design: `docs/design.md`.
Decisions: `docs/prd/factory-decisions.md`.

## Requirements

- Claude Code (recent enough for plugins, `--agent` and `--permission-prompts none`), Python 3.10+, git.
- UI projects: Playwright with Chromium (setup offers to install it).

## Install

Run Claude Code with the plugin folder: `claude --plugin-dir <this folder>`. To install it permanently, add this
folder as a plugin marketplace/plugin with your Claude Code version's `claude plugin` commands (see its docs).
`build.py` adds `--plugin-dir` itself when the plugin is not installed and `plugin_root` is set in
`.claude/harness.json`.

## Use it on a project

In the project folder (a git repo), open Claude Code, accept the folder trust prompt once, then:

| Step | Command | Result |
| --- | --- | --- |
| 1 | `/harness:new "<idea>"` | Questions, spec, `/harness:setup`, then `/harness:init-build` |
| 2 | `build.cmd` (runs `python <plugin_root>/scripts/build.py`) | Headless build sessions until done or stuck |
| 3 | `/harness:report`, `/harness:approve <id>`, `/harness:rework <id> <note>` | Settle `needs-human` jobs |

### Creating the feature list

`feature_list.json` can't be written directly (a hook blocks Write, Edit and Bash on it). `/harness:init-build`:

1. **Propose**: writes only the new features to `init-features-candidate.tmp` in the project root.
2. **Validate**: `python <plugin_root>/scripts/init_features.py --check init-features-candidate.tmp` (changes nothing).
3. **Approve**: shows you each id, title and dependency; you say what to change.
4. **Apply**: the same command with `--apply` (validates again, replaces the file atomically).
5. **Verify**: reads `feature_list.json` back.

This works only from the interactive session; subagents (builder, reviewers, organiser) are refused. Existing
features are never changed, ids must be unique, dependencies must exist, and new features start `todo` / `passes: false`.

## Configuration

- `.claude/harness.json` (written by `/harness:setup`): `test`, `plugin_root`, and optional `max_builders` (2), `gates`,
  `risky`, `acceptance_dir`, `walkthrough_every` (5), `run`, `test_limit_s` (300), `protected`.
- `factory.json` (in the plugin): the reviewers. Each has `name`, `agent`, `when` (`always`, `ui`, `high_risk`,
  `milestone`), `browser` and optional `batch`.
  - `code` runs on every feature, **batched**: one call reviews all the features built together, one verdict file each.
  - `security` runs only on **high-risk** features (files matching `risky`).
  - `user` and `visual` run at **milestones** (every `walkthrough_every` UI features, and once at the end), on the whole app.

High-risk features are never merged automatically: after the reviews pass they become `needs-human` with the
branch kept, and you merge with `/harness:approve <id>`.

## Tests

```
python -m pytest -q
```

The suite takes a few minutes (many tests start Python subprocesses). The design-audit tests use Playwright and Chromium; if they are missing, expect those tests to fail for
that reason (all 92 tests passed on the machine used for this change).
`/harness:smoke` runs the real line end to end on a mini project; it needs Claude Code and is billed.

## Release ZIP

`git archive --worktree-attributes --format=zip -o harness.zip HEAD` follows `.gitattributes`, which leaves out
agent memory, caches and compiled Python. `.git` is never included.

## Common errors

| Message | Cause and fix |
| --- | --- |
| `Blocked: feature_list.json and protected paths can't be changed directly` | Use `init_features.py`, `status.py` or `mark_pass.py`; never Write or Edit the list |
| `Feature validation failed: ...` | Fix `init-features-candidate.tmp` as the message says, run `--check` again |
| `Candidate must be the designated project-root file` | The candidate must be `init-features-candidate.tmp` in the folder you run it from |
| `session failed (N); see build-log.jsonl` | A build session exited with an error; read the end of `build-log.jsonl`, fix, rerun `build.cmd` (it resumes) |
| Jobs sit at `needs-human` | High risk, or still failing after two rework rounds: `/harness:report`, then approve or rework |
| Permission denials in `build-log.jsonl` | `python scripts/check_log.py build-log.jsonl`; add the missing `Bash(...)` rule in `.claude/settings.json` |

## Limits

- Review is not proof; tests, gates, the risk rule and the needs-human list are the safety net.
- Hooks apply only when `.claude/harness.json` exists. The init and merge rules rely on the hook input's
  `agent_type`, which Claude Code sets for subagents and `--agent` sessions (D56).
- Deployment and pushing are out of scope: `git push` is denied.
- The batch review, milestone walkthrough and high-risk parking are covered by script tests and prompt text; the
  full multi-agent line has not been run end to end in this repo's tests.
