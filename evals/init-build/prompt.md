---
max_turns: 15
allowed_tools: [Read, Glob, Grep]
tags: [init-build]
expected_outcome: A short spec becomes features with acceptance steps, every passes false, no requirement left out.
---

/harness:init-build notes

You cannot write files here, so reply with the feature_list.json you
would write and nothing else. Assume .claude/harness.json exists and
feature_list.json does not. docs/spec.md, docs/decisions.md,
docs/brief.md and docs/owner.md are not on disk; docs/spec.md is below
and the others are empty.

docs/spec.md:

```
## notes

A command-line notes tool, used by one person.

1. `notes add "<text>"` saves a note and prints its number. Example:
   `notes add "buy milk"` prints `1`.
2. `notes list` prints every note as `<number>: <text>`, oldest first.
   With no notes it prints `No notes.`
3. `notes delete <number>` removes that note. An unknown number prints
   `No such note.` and changes nothing.
4. Notes are kept in notes.json in the current folder and survive
   restarts.
5. Deleting a note never renumbers the others (D1).
```
