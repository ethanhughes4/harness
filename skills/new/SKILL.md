---
description: The one start command. Asks one list of at most 15 questions, shows a mockup for UI apps, then sets up, writes the feature list and build.cmd, and commits, ready for build.cmd. Use to start a new project or add a feature or stage.
argument-hint: "\"<idea>\""
disable-model-invocation: true
---

Start from this idea: $ARGUMENTS

The plugin's absolute folder is: ${CLAUDE_PLUGIN_ROOT}

Call that value PLUGIN_ROOT. If it is empty or still starts with a
dollar sign, stop and tell the owner; do
not guess a path. Use forward slashes.

You are the owner's single entry (D73). Do the steps below in order by
reading each skill's instructions from
`PLUGIN_ROOT/skills/<name>/SKILL.md` and following them. Where a step
says "run from new", that skill's own approval stops are replaced as
described here. Do not write code.

If `feature_list.json` exists, this is an existing project: do the
same steps for ONE feature or stage only (the idea), skip the first
setup, and append to the list; never change an existing feature.

If `docs/spec.md` exists but `feature_list.json` does not, an earlier
intake stopped partway: resume it. Keep what docs/brief.md, docs/spec.md
and docs/decisions.md already settle and ask only what they leave open;
redo the design step if `docs/design/design-system.md` is missing; then
carry on with setup and the rest.

1. owner: follow `skills/owner/SKILL.md`. If
   `~/.claude/harness/owner.md` is missing, it interviews the owner;
   otherwise copy it silently to `docs/owner.md`.
2. questions: follow `skills/questions/SKILL.md` with the idea as the
   stage. One list, at most 15 questions that change what gets built,
   each with a recommended answer; "ok" accepts all. The brief's items
   (problem, user, must-nevers, out of scope) are in that list. The
   critic checks the TECHNICAL answers first. Decide the architecture
   yourself, without questions, and record it as D-numbered decisions
   (use `skills/architecture/SKILL.md`). Write docs/brief.md,
   docs/spec.md and docs/decisions.md. For a UI app also make the
   design exactly as the questions skill's UI step says: the agent derives
   the client's direction from the brief with the 10 per-client steps of
   `harness:design-guideline` (D96), then the owner picks a direction
   from the preview, confirms the brand sheet
   (docs/design/design-system.md) and approves the mockup. These are the only owner stops
   besides the questions themselves.
3. setup: follow `skills/setup/SKILL.md`, run from new: no separate
   review stop, only its one-screen summary (and the Playwright yes or
   no for a UI app).
4. init-build: follow `skills/init-build/SKILL.md`. Features get
   `status: "todo"`; build.cmd runs build.py. Skip its "is anything
   missing" stop; the spec was already agreed.
5. Commit (init-build's `git add -A` and commit). Do not push.
6. Tell the owner: run build.cmd.
