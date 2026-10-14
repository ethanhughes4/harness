---
description: Interviews the owner about a new project and writes docs/brief.md with four headings (Problem, User, Must never, Out of scope). Use once, at the start of a project.
disable-model-invocation: true
---

Interview the owner about the project, then write docs/brief.md.

Your job is a short, firm brief that every later step can rely on. You
are not here to be agreeable. You are here to find every gap.

## Before asking anything

1. Read CLAUDE.md, docs/owner.md and every file in docs/, if they
   exist, and any code already in the project.
2. If docs/brief.md already exists, read it and ask only what is
   missing or out of date.

## How to ask

- Ask everything in ONE numbered list, in one message.
- Give each question your recommended answer and one sentence on why.
- Never ask something you can find out by reading the files. Look it up
  and state what you found.
- Use plain words. Explain each technical term the first time.
- Then wait for the owner's reply. They change only what they disagree
  with; an answer left alone accepts your recommendation.
- If an answer is vague, ask a short follow-up list for an example or a
  yes or no.
- If the owner says "I don't know", explain the options and their
  trade-offs, then ask again.

## What to cover

1. Problem: what is wrong or missing today, and for whom?
2. User: every kind of person who will use this, and what each one
   wants to do.
3. Must never: the things that must never happen, such as wrong
   numbers shown as right, lost data, leaked secrets, or a cost over a
   limit. One line each, concrete enough to check.
4. Out of scope: what is deliberately left out.

## Writing docs/brief.md

Write the file with exactly these four headings, in this order, and no
others:

```
## Problem
## User
## Must never
## Out of scope
```

Under "Must never" put one bullet per item. The
build re-reads that section after the context is compacted, so keep it
short and exact.

## Finishing

Read the whole brief back to the owner and ask: "Is anything missing or
wrong?" Keep going until they confirm, then write the file. Do not
write code.
