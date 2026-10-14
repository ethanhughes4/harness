---
description: Creates or updates the owner's master preferences file at ~/.claude/harness/owner.md and copies it to docs/owner.md in this project. Use once per owner, and again when preferences change.
disable-model-invocation: true
---

Create or update the owner's preferences file.

The master is `~/.claude/harness/owner.md`. Each project holds a copy at
`docs/owner.md`. The resolver answers preference questions from that copy,
so it must be specific and easy to search.

Ask the owner only when `~/.claude/harness/owner.md` does not exist
(D74). If it exists, copy it to `docs/owner.md` silently (make `docs/`
if needed) and stop. Run the steps below only when there is no master,
or when the owner asks to change their preferences.

## Steps

1. Read `~/.claude/harness/owner.md` if it exists, and `docs/owner.md` if
   it exists. If the project copy differs from the master, show the
   differences and ask which one is newer.
2. If there is no master, create it (make the folder if needed) with the
   template below, then interview the owner (step 3) to fill it in.
3. Ask every question in ONE numbered list, in one message, each with a
   recommended answer and one sentence on why. Cover only what is empty
   or what the owner wants to change: how they like to work with Claude,
   how they read results, what they want to be asked about, and what they
   never want. Use plain words and wait for the reply. An answer left
   alone accepts the recommendation.
4. Write the master. Keep the headings exactly as in the template.
   Each entry is one plain line, "<topic>: <answer>". Use gender-neutral
   wording ("they", "the owner").
5. Create `docs/` if needed and copy the master to `docs/owner.md`.
   Overwrite the project copy only after the owner has confirmed the
   master.
6. Tell the owner both paths. Do not write code.

## Template for a new master

```
# Owner

## Standing answers
- Who writes code: Claude writes all code; I read and edit.

## How I work
- (when they want to be asked, how much detail, pace)

## How I read results
- (format, length, level of technical detail)

## Always
- (things they want done every time)

## Never
- (things they never want)
```

The standing answer under `## Standing answers` is always present in a
new master. Keep it unless the owner changes it. Features are tagged
`owner-writes` only when a project's brief asks for it.
