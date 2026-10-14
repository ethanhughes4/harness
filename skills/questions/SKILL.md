---
description: Asks the owner every question about a planned stage in one list, each with a recommended answer, then writes docs/spec.md and docs/decisions.md. Use before building a stage.
argument-hint: "[stage-name]"
disable-model-invocation: true
---

Question the owner in depth about: $ARGUMENTS

Your job is to reach full agreement on what will be built. You
are not here to be agreeable. You are here to find every gap.

## Before asking anything

1. Read CLAUDE.md, docs/brief.md, docs/owner.md, every other file in
   docs/ (including docs/spec.md and docs/decisions.md if they exist),
   and the code this stage will build on.
2. If docs/decisions.md already has a heading for this stage, read it
   and ask only what is still open.

## How to ask

- Ask everything in ONE numbered list, in one message. Do not ask one
  question at a time.
- Each question has:
  - a tag: TECHNICAL (a fact or engineering choice that has a right
    answer) or PREFERENCE (something the owner would see or notice, or
    a trade-off only they can weigh);
  - your recommended answer, and one sentence on why.
- Never ask something you can find out by reading the code or docs.
  Look it up and state what you found.
- Use plain words. Explain each technical term the first time.
- If docs/owner.md already answers a question, use that answer and
  say so instead of asking.
- Before showing the list, start `harness:critic` with every TECHNICAL
  question and its recommended answer. It returns AGREE or CHANGE
  (with a quote and link) for each. Apply every CHANGE to the list.
  Show the owner the PREFERENCE questions, and the technical ones the
  critic changed, each with the critic's quote and link. List the
  AGREEd technical answers in one line each so the owner can object.
- Then wait for the owner's reply. They change only what they
  disagree with; an answer left alone accepts your recommendation.
- If an answer is vague, ask a short follow-up list for a number, an
  example, or a yes or no. If it conflicts with an earlier decision,
  say so and ask which one stands.
- If the owner says "I don't know", explain the options and their
  trade-offs, then ask again.

## What to cover

1. Purpose: who uses this, and what can they do afterwards? List every
   kind of user and every thing each one wants to do.
2. Examples: at least three real inputs with the exact output expected
   for each.
3. Boundaries: what is deliberately left out?
4. Behaviour when things go wrong: missing data, a failed lookup, a
   question it cannot answer.
5. Where every number in an answer comes from.
6. Technical choices: libraries, models, cost limits.
7. How we will prove it works: which tests, which checks, and for each
   judgement call a decision rule: "if X, then Y", so the build never
   has to stop and ask.
8. Which parts the owner wants to write themselves. Record the answer
   as `owner-writes` on those features only; docs/owner.md holds the
   standing answer.

## Recording

Settled answers go into two files, each with one heading per stage
(`## <stage>`), appended if the file exists:

- docs/decisions.md, one line per decision, numbered across the whole
  file (continue from the highest D-number):
  `D<number>: <the decision> (reason: <why>)`
  Decision rules are written as decisions:
  `D<number>: Rule: if <X>, then <Y> (reason: <why>)`
  Mark anything the owner was unsure about as ASSUMPTION.
- docs/spec.md, what will be built, in plain prose and examples, with
  the decision numbers it rests on.

## Finishing

Read the full decision list back to the owner and ask: "Is anything
missing or wrong?" Keep going until they confirm, then write the two
files. Do not write code.
