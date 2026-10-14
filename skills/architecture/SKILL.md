---
name: architecture
description: Designs or checks a system architecture. Produces requirements, non-functional needs, a chosen pattern with trade-offs, a diagram and risks, in the shape of docs/architecture.md. Use when a stage changes structure, or when judging whether code fits the agreed design.
---

Use this to design a stage's architecture, or to check code against an
existing `docs/architecture.md`. Keep it as small as the stage allows:
choose the simplest structure that meets the needs.

## Designing

1. Requirements: what the system must do, taken from docs/brief.md and
   docs/spec.md. One line each.
2. Non-functional needs: only the ones that matter here, each with a
   number or a yes/no test (speed, size, cost, data safety, who can
   see what, how it fails).
3. Options: two or three structures that could meet 1 and 2. Include
   the plain one (for example a single module with functions).
4. Choice: pick one. For each rejected option, one line on why.
   Write each trade-off as a decision for docs/decisions.md:
   `D<number>: <chose X over Y> (reason: <the trade-off accepted>)`.
5. Diagram: a Mermaid block showing the parts and how data moves
   between them.
6. Risks: what could go wrong with the choice, and the sign that would
   tell us early.

## docs/architecture.md

Headings, in this order: Requirements, Non-functional needs, Chosen
pattern (with the trade-offs and their D-numbers), Diagram, Risks.
Add a `## <stage>` section per stage rather than rewriting earlier ones,
unless the owner changes an earlier choice; then say so and update it.

## Checking code against it

Read docs/architecture.md. Flag only code that breaks it: a part
reaching around the boundary the diagram shows, a dependency the pattern
rules out, a non-functional need that the code visibly fails. Quote the
line of the architecture that is broken. Do not flag style.
