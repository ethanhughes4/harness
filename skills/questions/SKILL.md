---
description: Asks the owner every question about a planned stage in one list (at most 15, each with a recommended answer), then writes docs/brief.md, docs/spec.md and docs/decisions.md, plus a mockup and tokens for UI apps. Use before building a stage.
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
  question at a time. At most 15 questions, and only ones whose answer
  changes what gets built; fold the rest into your recommended answers.
  The owner may reply "ok" to accept every recommendation.
- The brief's items are questions in the same list (skip any that
  docs/brief.md or docs/owner.md already answers): the problem, the
  user, the must-nevers, and what is out of scope.
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

Settled answers go into these files, each with one heading per stage
(`## <stage>`), appended if the file exists:

- docs/decisions.md, one line per decision, numbered across the whole
  file (continue from the highest D-number):
  `D<number>: <the decision> (reason: <why>)`
  Decision rules are written as decisions:
  `D<number>: Rule: if <X>, then <Y> (reason: <why>)`
  Mark anything the owner was unsure about as ASSUMPTION.
- docs/spec.md, what will be built, in plain prose and examples, with
  the decision numbers it rests on.
- docs/architecture.md, only if the stage adds or changes structure
  (new parts, new data flow, new dependencies). Use the
  `harness:architecture` skill to write it, with one `## <stage>`
  heading. Its trade-offs go into docs/decisions.md as D-numbered
  decisions like the rest.

- docs/brief.md (new project, or if missing), with exactly these
  headings in this order and no others: `## Problem`, `## User`,
  `## Must never` (one short concrete bullet per item), `## Out of
  scope`. scripts/reinject.py re-reads "Must never" after compaction.
- UI app only: the design, made with the `harness:web-design-engineer`
  skill (use the Skill tool; D88). Follow its workflow with these stops:
  1. Directions: unless the owner named a style, run its Design
     Direction Advisor: 3 directions from 3 different schools, each
     with its named anchor, why it fits, and signature cues. Recommend
     one. The owner picks (or names their own).
  2. System: read the one matching file in its
     `references/style-recipes/`, write the Design Read with the five
     dials (its `references/design-calibration.md`) and the Design
     Decisions block with the recipe's concrete values. Show it; the
     owner confirms (its Checkpoint 1).
  3. v0: docs/design/mockup.html, one self-contained page with the main
     screens in that system, real states (empty, error, loading) where
     they matter, and none of the clichés in its "Avoid AI-Style
     Clichés" table or `references/failure-patterns.md`. Before showing
     it, run its 5-dimension critique on it yourself and fix anything
     under 7. The owner approves or asks for changes (its Checkpoint 2).
  Use both design skills (D91): web-design-engineer decides the look
  (direction, recipe, colours, type); `harness:ui-ux-pro-max` supplies
  the usability rules. Before step 3, run its search for the app's UX
  concerns (`--domain ux` for the main interactions such as forms,
  navigation and feedback; `--domain chart` for any chart) and read its
  `references/quick-reference.md` priorities 1 to 9. Take its palette or
  style picks only where they agree with the chosen recipe; never pass
  `--persist`. Check the mockup against its
  `references/pro-rules.md` pre-delivery checklist as well as the
  critique.
  Then write docs/design/design-system.md (Design Read, dials, recipe
  name, the Design Decisions block, the signature moves, the recipe's
  "avoid" list, and a "UX rules" section: the ui-ux-pro-max rules this
  app must meet, by priority, each one line) and docs/design/tokens.md (every colour, font,
  size, spacing, radius, shadow and motion value, one per line, as CSS
  custom property names and values). Builders and the visual reviewer
  work only from these two files and the mockup. If the app must work
  offline, the design may not depend on a CDN or web font at run time:
  note in design-system.md that fonts and chart libraries are saved
  into the project.

## Finishing

Read the full decision list back to the owner and ask: "Is anything
missing or wrong?" Keep going until they confirm, then write the
files. Do not write code.
