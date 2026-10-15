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
- UI app only: the design (D88, D91, D96). The authority is the
  `harness:design-guideline` skill (use the Skill tool): its Never and
  Always rules and its 10 per-client steps win over the two vendored
  skills. `harness:web-design-engineer` supplies the schools, recipes and
  critique; `harness:ui-ux-pro-max` supplies the usability rules. The
  owner has exactly three stops: pick a direction from the visual
  preview, confirm the brand sheet, approve the mockup. Everything else
  you do yourself.
  1. Steps 1 to 6, from the brief, no owner stop: facts, discovery
     answers, "this, not that" adjectives (with the target word list),
     sliders, competitor audit (each convention tagged keep or break),
     and the attribute-to-choice mapping, each choice with its reason.
     The brief may be a client's, so infer from it, log every inference
     as an ASSUMPTION in docs/decisions.md, and write all of it into the
     brand sheet draft. Ask the owner only for a missing logo or product
     imagery (blocking: ask it in the question list, never draw one).
  1b. Reference step (D101), after step 1 and before the directions, no
     owner stop. Pick 3 to 5 genuinely premium products in the client's
     category (not the competitors being differentiated from, unless they
     are premium) plus one object or brand from outside software, each
     with a one-line reason. For app projects prefer pages that show the
     real product UI. Capture them:
     `python <plugin_root>/scripts/reference_capture.py docs/design/references <name> <url> [<url>...]`
     (plugin_root from .claude/harness.json; if it does not exist yet in
     this intake, use the plugin folder path the new skill already has).
     Output: `<out>/<name>/<n>/{390-<k>.png,1440-<k>.png,metrics.json}` and
     `<out>/ranges.json`. Read the PNGs. If a site fails to load, pick
     another. Write docs/design/reference-spec.md: per reference, what to
     borrow (systems: type treatment, spacing rhythm, borders and depth,
     number formatting, motion feel) and what not (assets, logos,
     signature look); the measured ranges from
     docs/design/references/ranges.json; and the exact target values this
     client's design will use.
  2. Steps 7 to 9, directions: three directions, each led by a different
     adjective and from a different school, each breaking at least one
     category convention. Each direction names which reference systems it
     borrows (D102); the premium spec
     (`harness:design-guideline` `references/premium-spec.md`) defaults
     apply unless the brand sheet overrides one with a reference or a
     brief fact (not a recipe name). Fonts follow `references/fonts.md`
     (D104). They must pass the difference test: display
     family differs, accent hue more than 60 degrees apart, at least one
     layout primitive differs (hero composition, grid, density). If
     not, rework. Then write docs/design/directions.html, one
     self-contained page of style tiles in randomised order (not the
     letters in a fixed order), each with the client's real copy and
     these components: header, primary and secondary button, a field
     with an error, a card, a data row, an imagery treatment; plus the
     app's main screen with realistic sample data from the spec. Under
     each tile: its lead adjective, "but not ...", and a 3-line
     rationale. Mark one recommended. Light/dark switch; stacks at phone
     width. It must meet the bar of the final design (D94):
     - Each direction uses its recipe file from web-design-engineer's
       `references/style-recipes/` with its real fonts, palette and
       signature moves, but display type, accent and one layout move
       must trace to this brief. They differ in layout and typography,
       not one wireframe in three colour schemes.
     - "Works offline" never means system fonts: fonts are chosen for the
       design, downloaded into the project at setup and served locally.
       Only a font the recipe itself names may be a system font.
     - Show only what the screen needs, with a clear hierarchy.
     - Before opening it: screenshot at 390 px and 1280 px, light and
       dark, and Read the screenshots. Fix text that wraps badly,
       overflows or collides. Run the 5-dimension critique on each
       direction and rework any dimension under 7.
     - Critique loop (D103): start `harness:design-critic` (fresh context)
       with the screenshots, docs/design/reference-spec.md and the
       reference screenshots; apply its top fixes and re-run, at most 3
       rounds, keeping the best round. Open the page only if the critic
       rated it PREMIUM; after 3 rounds open the best round and list the
       critic's remaining notes to the owner honestly. Only then open it.
     Open it in the owner's browser (Windows: `start "" docs\design\directions.html`;
     macOS: `open`; Linux: `xdg-open`). Stop 1: the owner picks a
     direction, or asks for a mix. Resolve a mix into one coherent tile
     (never stitch parts together) and preview it again; likewise for
     any change. Keep directions.html as the record.
  3. Step 10, brand sheet. Write docs/design/design-system.md as the
     brand sheet, with the contents the guideline lists: positioning
     line, adjectives with their "but not"s, slider positions (client
     and competitors), conventions tagged keep or break, the chosen
     direction with reasoning, the Design Read and dials, recipe name,
     type, palette, spacing, shape and motion tokens each with its
     reason, imagery rules, ownable assets, the signature moves, the
     recipe's "avoid" list, the target word list. Add a "References" section (names, urls, what
     is borrowed from each) and a "Fonts and licences" line: each font's
     licence and whether it may be bundled (D104). Add a "UX rules"
     section (D91): the ui-ux-pro-max rules this app must meet, by
     priority, one line each. Add a "Justified exceptions" section: each
     Never item (N1 to N19) the design uses, as `N<k>: <reason naming
     the brief>`; "none" if there are none. Show it. Stop 2: the owner
     confirms it (web-design-engineer's Checkpoint 1).
  4. v0 mockup: docs/design/mockup.html, one self-contained page with
     the main screens in that system, real states (empty, error,
     loading) where they matter, and none of the clichés in
     web-design-engineer's "Avoid AI-Style Clichés" table or
     `references/failure-patterns.md`, nor any Never item without an
     entry under Justified exceptions. Before building it, run ui-ux-pro-max's
     search for the app's UX concerns (`--domain ux` for the main
     interactions; `--domain chart` for any chart), read its
     `references/quick-reference.md` priorities 1 to 9, and take its
     palette or style picks only where they agree with the chosen
     recipe; never pass `--persist`. Check the mockup against its
     `references/pro-rules.md` pre-delivery checklist and against the
     guideline's checks, run the 5-dimension critique yourself and fix
     anything under 7. Then run the critique loop above on the mockup
     (`harness:design-critic` with screenshots, reference-spec.md and the
     reference screenshots; 3 rounds at most, best round kept) and run
     `python <plugin_root>/scripts/design_audit.py <url> --compare docs/design/references/ranges.json`
     on it. Show the owner only a mockup rated PREMIUM, or the best of 3
     rounds with the critic's remaining notes. Stop 3: the owner approves or asks for changes
     (its Checkpoint 2).
  Then write docs/design/tokens.md, the flat list (every colour, font,
  size, spacing, radius, shadow and motion value, one per line, as CSS
  custom property names and values). Builders and the visual reviewer
  work only from design-system.md, tokens.md and the mockup; a value not
  on the sheet may not be used. If the app must work offline, the design
  may not depend on a CDN or web font at run time: note in
  design-system.md that fonts and chart libraries are saved into the
  project.

## Finishing

Read the full decision list back to the owner and ask: "Is anything
missing or wrong?" Keep going until they confirm, then write the
files. Do not write code.
