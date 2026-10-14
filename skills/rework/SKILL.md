---
description: Sends a needs-human job back for rework with a note from the owner. Use as /harness:rework <id> <note>. The next build session starts a fresh builder with the note.
disable-model-invocation: true
---

Send job `<id>` back for rework. The rest of the arguments is the owner's
note. Run from the project root.

Never name feature_list.json in a Bash command; the guard blocks it. The
only exception is the exact call `python <plugin_root>/scripts/status.py <id> <status>`.
Read `feature_list.json` with Read. Never push. Start no subagent.
Read `.claude/harness.json` for `plugin_root`.

1. Read `feature_list.json` with Read. The feature `<id>` must have
   status `needs-human`. If not, say its status and stop. If the note is
   empty, ask the owner for one and stop.
2. Write the note to `.harness/jobs/<id>/owner-note.md` (heredoc, exactly
   the owner's words).
3. `python <plugin_root>/scripts/status.py <id> rework`.
4. `git add -A` and `git commit -m "Rework <id>: owner note"`.

Keep the branch and worktree. Tell the owner: the next build session
(`build.py`) picks this job up again and starts a fresh builder with
`owner-note.md`.
