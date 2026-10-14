---
description: Summarises the build for the owner, in one report. Shows feature progress, every provisional decision to confirm, eval results and failures. Read-only. Use after or during a headless build.
disable-model-invocation: true
---

Report on the state of the build.

You only read. Never edit feature_list.json, docs/decisions.md or
progress.md, and do not start any subagent. The guard hook blocks
Bash commands that name feature_list.json, so read it with Read.

## Read

1. `feature_list.json`: each feature has `id`, `stage`, `passes`,
   `depends_on` and possibly `owner-writes`.
2. `docs/decisions.md`: every line starting `D<n> (PROVISIONAL):`.
3. `progress.md`: every entry. Each starts with a heading
   `## <YYYY-MM-DD HH:MM> <title>` and has the lines `Features built:`,
   `Reviewed:`, `Tests:`, `Skipped:`, `Provisional:`. Skip decisions
   are separate lines `SKIPPED <id>: <reason>`. Also look for any
   entry or line that mentions StopFailure.

If a file is missing, say so in its section and go on.

## Write the report

Use plain words, in this order, and address the owner as "you".

1. Progress: `N/M passing` overall, then N/M per stage. List the
   features that are not passing, each with its state: ready, waiting
   on `depends_on` ids (name them), `owner-writes` (waiting for you),
   or skipped.
2. Skipped features: each `SKIPPED <id>: <reason>`, plus the ids that
   cannot start because they depend on it.
3. Decisions for you to confirm: every `D<n> (PROVISIONAL)`. For each,
   show the number, the option that was taken, the other options, and
   the evidence, copied from the line. Say what to do: to accept it,
   do nothing; to change it, tell the questions skill or write the new
   decision in docs/decisions.md and list which features may need
   rework.
4. Eval results: from the `Tests:` and `Reviewed:` lines and any eval
   named in the progress entries, say each eval, its result against
   baseline, and the date. If none ran, say "no evals recorded".
5. Failures: each red suite, each reviewer finding left unfixed, each
   StopFailure entry, each blocked builder, each entry whose `Tests:`
   shows a failure. Give the entry heading and a one-line reason.
6. Next: one sentence on what the build will do next or what is
   needed from you.

Keep it short. Quote numbers and ids exactly; do not guess a status
the files do not show, write "not recorded" instead.
