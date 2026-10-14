---
description: Summarises the factory build for the owner, in one report. Shows progress by status, needs-human jobs with the command to act, milestone findings, cost, builder transcripts to skim, provisional decisions and failures. Read-only. Use after or during a headless build.
disable-model-invocation: true
---

Report on the state of the build.

You only read. Never edit feature_list.json, docs/decisions.md,
progress.md or anything in `.harness/`, and do not start any subagent.
The guard hook blocks Bash commands that name feature_list.json, so
read it with Read, never in Bash.

## Read

1. `feature_list.json`: each feature has `id`, `stage`, `passes`,
   `depends_on`, possibly `owner-writes`, and `status` (todo, building,
   review, rework, needs-human, done). A missing `status` is todo, or
   done when `passes` is true.
2. `docs/decisions.md`: every line starting `D<n> (PROVISIONAL):`.
3. `progress.md`: every entry. Each starts with a heading
   `## <YYYY-MM-DD HH:MM> <title>` and has the lines `Jobs:`, `Tests:`,
   `Needs human:`, `Provisional:`. Milestone walkthrough findings are
   needs-human items in entries about a walkthrough. An API error that
   stopped the run is an entry titled `API error stopped the run`,
   with an `error:` line and sometimes a `details:` line.
4. For each feature with status needs-human: `.harness/jobs/<id>/decision.md`
   and the files `.harness/jobs/<id>/round-<n>/review-*.md` of the
   highest `<n>` (use Glob, then Read; the first line of each is
   `VERDICT: PASS` or `VERDICT: CHANGES`).
5. `build-log.jsonl` in the project root, for cost (below).

If a file is missing, say so in its section and go on.

## Write the report

Use plain words, in this order, and address the owner as "you".

1. Progress: `N/M done` overall, then a count per status (todo,
   building, review, rework, needs-human, done), then per stage N/M
   done. List every feature that is not done with its status; for todo
   say if it waits on `depends_on` ids (name them) or `owner-writes`
   (waiting for you).
2. Needs you: each needs-human job, with
   - its job folder `.harness/jobs/<id>/`;
   - the reason, from `decision.md`;
   - the latest round's VERDICT lines, one per reviewer
     (`<name>: PASS|CHANGES`), and the gates result if
     `gates-<round>.md` is the latest finding;
   - what to do: `/harness:approve <id>` to merge it as it is, or
     `/harness:rework <id> <note>` to send it back with your note.
   If none, say "nothing needs you".
3. Milestone walkthrough: the findings from the walkthrough entries in
   `progress.md`, each with its entry heading. If none, say "no
   walkthrough yet".
4. Cost: from `build-log.jsonl`. Each line is JSON; skip a line that
   does not parse. A line with `"type": "result"` has `session_id` and
   `total_cost_usd`. A session may emit more than one result line, and
   the figure is cumulative, so use only the last result per
   `session_id`. Give the cost per session, the total, and the total
   divided by the number of done features. Say the per-feature figure
   is an average, because a session works on several features. If the
   file is missing or has no result lines, say "cost not recorded".
5. Transcripts to skim: pick three builder runs. Builder transcripts are
   at `~/.claude/projects/<project>/<session>/subagents/agent-*.jsonl`;
   `<project>` is the project folder path with every character that is
   not a letter or digit replaced by `-`, and `<session>` is a
   `session_id` from `build-log.jsonl`. Glob that pattern for each
   session, Read the first lines of each `agent-*.jsonl`, and keep
   those whose first prompt or name is `builder-<id>` or
   `builder-<id>-2`. Give three full paths, with the feature id of
   each. If you cannot find them, say so and give the pattern you
   tried.
6. Decisions for you to confirm: every `D<n> (PROVISIONAL)`. For each,
   show the number, the option that was taken, the other options, and
   the evidence, copied from the line. Say what to do: to accept it,
   do nothing; to change it, tell the questions skill or write the new
   decision in docs/decisions.md and list which features may need
   rework.
7. Failures: each red suite, each reviewer finding left unfixed, each
   `API error stopped the run` entry (give its `error:`), each blocked
   builder, each entry whose `Tests:` shows a failure. Give the entry
   heading and a one-line reason.
8. Next: one sentence on what the build will do next or what is
   needed from you.

Keep it short. Quote numbers and ids exactly; do not guess a status
the files do not show, write "not recorded" instead.
