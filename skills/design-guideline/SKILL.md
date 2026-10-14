---
name: design-guideline
description: "The harness design guideline against the AI look. Load it when designing a client's look (turning a brief into a distinct direction and a brand sheet), when building UI (what to always do, what never to do), and when reviewing UI (scripted checks, tell score, screenshot judge). It wins over web-design-engineer and ui-ux-pro-max where they disagree."
---

# Design guideline

Source: `reports/Design guideline against AI look.md` (D95). Tells list: `references/tells.md`.

## Purpose

The "AI look" is a stack of unchosen defaults that show up together: Inter as the only
typeface, an indigo-to-purple gradient, a centred hero with a pill badge, three identical
icon-topped cards, one radius and one shadow on everything, glows and glass, all-caps
eyebrows, emoji icons, and an app that designs only the happy path. A scan of about 1,590
Show HN sites put 22% at four or more of these tells and another 32% at two or three
([Krebs](https://www.adriankrebs.ch/blog/design-slop/)).

Ban lists alone only move the model to the next default. Anthropic's own skill now lists the
"tasteful" escape routes (cream with serif and terracotta, near-black with an acid accent,
hairline broadsheets) as tells too
([SKILL.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)).
So every identity-bearing choice needs a written reason tied to the client's brief, and a
reviewer must check that the reason was built.

Labels used below: **[E]** evidence-backed (a standard or a measured study). **[C]**
consensus (several independent practitioner or vendor sources agree). **[R]** rule of
thumb (practice or inference, unvalidated).

## The overriding rule [C]

A Never item may be used, and an Always item may be broken, only when the brand sheet
records a reason that names the brief, the client's existing assets, or a competitor gap.
"It looks modern/clean/premium" is not a reason.

The reviewer checks that each recorded reason is visible in the build, because generative
tools leave 25-34% of stated rationales unimplemented
([arXiv 2607.22928](https://arxiv.org/abs/2607.22928)).

## Precedence over the vendored skills

This guideline sits above `web-design-engineer` and `ui-ux-pro-max`. Where they disagree,
this one wins. Elsewhere use them as normal.

| Topic | Vendored skill says | Guideline position |
|---|---|---|
| Cliché list | web-design-engineer's table covers first-generation tells (purple gradient, side-tab, emoji, Inter/Roboto/Fraunces display). failure-patterns adds eyebrows, centred hero and Instrument Serif | **Adds** the second-generation tells from Anthropic's current skill: cream + serif + terracotta, near-black + acid accent, broadsheet hairlines, middle-dot meta, "→" on links, 01/02/03 on non-sequences, one accented headline word, uniform fade-up. Makes the list a versioned file and scores co-occurrence |
| Example direction prompt | `design-directions.md` offers "single muted terracotta (#C04A1A) accent, GT Sectra serif headline … warm off-white (#F2EFE8)" as a sample | **Disagrees**: this is the cream/serif/terracotta cluster Anthropic now lists as a default. Allowed only with a brief-derived reason |
| "Aim to Stun" | Encourages `backdrop-filter`, entry animations, hover effects on cards | **Disagrees** for product UI: glass, fade-up on every section and hover on every card are listed tells. Allow one orchestrated motion moment and one signature effect, each with a stated reason |
| Where directions come from | Three directions from different schools, seeded from named recipes (Linear, Vercel, Raycast…) | **Agrees** on three directions from different schools. **Adds** that each direction is led by a different brief adjective and its "but not", breaks at least one category convention, and carries two or more ownable assets. A recipe is vocabulary, not identity, because the Linear look is itself a convergence point |
| Critique method | 0-10 score per dimension, run by the builder as a self-check | **Disagrees**: absolute scores cluster and self-grading skews positive. Use a separate reviewer, pairwise comparisons in both orders, yes/no checklists and few-shot calibration. Keep the best round, not the last |
| Browser acceptance | Run only when the user explicitly asks | **Overrides** for the pipeline: always run the scripted checks at three widths |
| Colour count | Critique says "typically ≤ 4" | Compatible. State it as one accent hue + tinted neutral ramp + semantic colours (a 4-6 named-hex base, per Anthropic) |
| Font pairings | ui-ux-pro-max `typography.csv` has 13 Inter-based pairings, including Inter + Inter "Minimal Swiss" for dashboards. `styles.csv` offers glassmorphism | **Adds a filter**: database output is a candidate. Inter, glass and similar defaults need a recorded reason that names the brief |
| Body line height | ui-ux-pro-max: 1.5-1.75 | **Partly disagrees**: Butterick gives 1.2-1.45. Use 1.3-1.6 as the script band (rule of thumb) and the upper end for long reading measures |
| Touch targets | ui-ux-pro-max: 44×44 everywhere | Compatible. Fail below 24 px (WCAG AA) and warn below 44 px on mobile viewports |

## Never: the AI tells

N1-N19 are in `references/tells.md`, each with why, detector, fix and label. Read it when
designing, building or reviewing.

Score tells per page. **Four or more unjustified tells fail the build; two or three trigger
review [R; Krebs's tiers measure prevalence, not human judgement].** A single tell with a
recorded reason passes. One tell is weak evidence. Co-occurrence is the signal.

## Always: what acclaimed design shares

| # | Rule | Numbers | Label |
|---|---|---|---|
| A1 | Build from tokens. Every colour, size, space, radius and shadow comes from a named token; no raw values in components | `stylelint-declaration-strict-value` passes on colour, spacing, radius and shadow properties | C (Geist, Linear, Carbon) |
| A2 | Type: one superfamily, or a display + body pair, plus an optional mono | ≤ 2 families excluding mono; ≤ 3 weights; ≤ 8 distinct sizes from one scale (ratio 1.2-1.25 for UI, fluid via `clamp()`) | Families C; counts R |
| A3 | Readable body text | 16-20 px body (Butterick's web range is 15-25); line height 1.3-1.6 (Butterick 1.2-1.45); measure 45-90 characters; all caps tracked +5-12% and < 1 line; h1 ≥ 2× body | E-ish (Butterick practice) / R |
| A4 | Neutral-first palette with one accent | 1 brand/accent hue + semantic success/warn/error/info + one tinted neutral ramp of ~8-11 steps; palette built in OKLCH/LCH so equal lightness looks equal; each step has a job (Geist's 100-300 backgrounds, 400-600 borders, 900-1000 text) | C (Linear, Vercel, Things, v0, Anthropic); step jobs R |
| A5 | Contrast | Text ≥ 4.5:1 (large text ≥ 3:1); component boundaries, states and focus rings ≥ 3:1; APCA Lc ≥ 75 for body as an advisory second check | E (WCAG); APCA R |
| A6 | Dark mode done properly | No pure #000 base; surfaces get lighter as they rise; accents desaturated against the light theme; text opacities around 87/60/38% | Platform (Material) / C |
| A7 | Spacing on a 4/8 base, grouping by proximity | ≥ 90% of margins, paddings and gaps are multiples of 4; ≤ 12 distinct values; gap inside a group ≤ 1/1.5 of the gap between groups | Base C (Carbon, Refactoring UI); thresholds R |
| A8 | Few alignment lines | Left edges of blocks cluster on few x-positions; no near-misses 2-6 px apart | R |
| A9 | Material presets | ≤ 3 radius values plus "full", scaled to element size; nested radius ≈ outer − padding; ≤ 4 shadow levels, layered (tight + soft) | R (Geist presets C) |
| A10 | One primary action per view | ≤ 1 filled accent button in the first viewport; the squint/blur test shows one dominant element, which is the H1 or primary CTA | R (NN/g squint test) |
| A11 | Complete states | Hover, focus-visible, active, disabled, loading, empty and error exist; `outline: none` without a replacement fails | E (WCAG focus) / C |
| A12 | Targets | ≥ 24×24 CSS px everywhere; ≥ 44 px on mobile viewports; ≥ 8 px apart | E (WCAG 2.5.8) / Platform |
| A13 | Motion with purpose | 100-300 ms for UI transitions, rarely > 500 ms; no linear easing on UI transitions; `prefers-reduced-motion` removes transforms | R (durations); E (honouring reduced motion) |
| A14 | Numbers align | `font-variant-numeric: tabular-nums` on table, price and stat cells | C |
| A15 | Conventional skeleton, owned signatures | Keep platform conventions for navigation, controls and forms (ui-ux-pro-max governs these). Spend distinctiveness on 2-3 deliberate assets: typeface, accent, one signature interaction or graphic device | C (Linear, Things, Raycast, Vercel); count R |
| A16 | Real content and imagery | Real product screenshots, client copy and real data, or labelled placeholders; never invented | C |
| A17 | Specific copy | H1 names what the product does for whom; sentence case; active-verb buttons ("Save changes", not "Submit"); errors say what went wrong and how to fix it | C |

## Per client: from brief to a distinct direction

`docs/design/design-system.md` IS the brand sheet (D96). Steps 1-10 end by writing it.

**Step 1. Extract facts [C].** From the brief, record: product and category, audience and
context of use, primary job of the site or app, existing assets (logo, product screenshots,
photography, mandated colours or fonts), and constraints. Missing logo or product imagery is
a blocking question for the owner, not something to draw.

**Step 2. Answer the discovery questions in writing [C].** The agent answers from the brief
and logs every inference as an assumption. Where the brief is silent, it picks a side and
records it rather than defaulting to the middle.
- Rank the three outcomes the design must achieve.
- If this brand were a vehicle (or a place, or a person), what would it be, and why?
- Where does it sit on each word pair: modern-traditional, illustrative-typographic,
  dense-spacious?
- What must the audience trust before they act?
- What must this never be mistaken for? Name a category cliché and an AI default.
- Who are three or more competitors or alternatives, and what do they all look like?

**Step 3. Write "this, not that" adjectives [C].** Write three to seven adjectives, each with
a "but not" overshoot, then rank them and keep the top two or three. At least one "but not"
names the category default ("trustworthy but not navy-and-gold bank") and one names an AI
default ("modern but not dark-glow SaaS"). Also write the NN/g verification list: the target
words, their opposites and distractors [E-method].

**Step 4. Place the sliders [C].** Use about six sliders (Serious-Playful,
Conventional-Rebel, Elite-Mass, Friend-Authority, Classic-Innovative, Quiet-Loud), placed
toward the ends with a one-line justification each. Rate the competitors on the same sliders.

**Step 5. Audit the competitor look [C].** Screenshot or describe three or more competitors.
List the category conventions (palette, type class, layout, imagery). Tag each as *keep* (a
trust cue the audience needs, such as clear pricing or regulated disclosures) or *break*.
Each direction must break at least one convention on purpose.

**Step 6. Map attributes to choices, each with a reason.** For every row, write "chosen X
because adjective/slider/gap Y".

| Lever | Mapping | Label |
|---|---|---|
| Type | Adjectives → Aaker dimension → type class: serif for traditional/sophisticated, sans for casual/approachable, mono for technical/plain; a display face carries the lead adjective | E (type class), R (via Aaker) |
| Colour | Lead adjective → hue family; saturation and value set intensity (higher amplifies excitement, lower reads sophisticated or competent); one accent; neutrals tinted toward the accent | E (direction, Labrecque & Milne) / R (specific values) |
| Layout and density | Elite-Mass and Quiet-Loud → whitespace and section padding (marketing 48-128 px; dashboards 4-12 px gaps); Conventional-Rebel → grid symmetry | R |
| Shape | Serious-Playful → radius and stroke weight | R |
| Imagery | Illustrative-typographic word pair; real product UI for digital products; client photography over stock | C / R |
| Motion | Quiet-Loud → zero or one orchestrated moment; Classic-Innovative → easing character | R |
| Ownable assets | Name two or more non-colour assets (type pairing, graphic device, shape language, signature interaction), since colour alone is the weakest distinctive asset | E (Romaniuk) / R |

**Step 7. Make three directions that differ [C].** Each direction is led by a different top
adjective and comes from a different school (web-design-engineer's school table works for
this). A style recipe may supply starting values, but at least the display type, accent and
one layout move must trace to this brief. Mark one direction as recommended, with written
reasoning [C, Parachute].

**Step 8. Test that they are different enough [E-method / R].**
- A non-designer would tell them apart at a glance. A hue swap on the same layout fails.
- Code check: directions differ in display family, in accent hue by more than 60°, and in at
  least one layout primitive (hero composition, grid, density).
- Screenshot judge check, in both orders: given the three adjective lists, can it match each
  preview to its list? Can it tell each from a no-direction baseline of the same content?

**Step 9. Show visual previews and let the owner choose [C].**
- Render each direction as a style tile or element collage. Use the client's real copy and
  real components: header, primary and secondary button, form field with an error, a card, a
  data row, and an imagery treatment.
- Screenshot each at desktop and mobile widths and show them in randomised order.
- Put the lead adjective, its "but not", and a three-line rationale under each.
- The owner picks one or asks for a mix. The agent resolves a mix into one coherent tile,
  does not stitch parts together, and re-previews.

**Step 10. Write the brand sheet [C].** The approved tile becomes the source for tokens. The
sheet (`docs/design/design-system.md`) holds:
- positioning line
- adjectives with their "but not"s
- slider positions for the client and its competitors
- category conventions tagged keep or break
- chosen direction with its reasoning
- type, palette, spacing, shape and motion tokens, each with its reason
- imagery rules
- ownable assets
- target word list

The builder may not introduce a value that is not on the sheet. The reviewer runs the
word-list test against the finished build.

## Checks

**Script checks on the running page.** Use Playwright and `getComputedStyle` over visible
elements at 360, 768 and 1440 px widths. Add a hover/focus pass, a `reducedMotion: 'reduce'`
pass, and fixtures for empty, slow and failing data. Scripts run first and are hard gates.

| Check | Threshold | Gate | Label |
|---|---|---|---|
| Text contrast (axe `color-contrast`) | ≥ 4.5:1; ≥ 3:1 for large text | Fail | E |
| Non-text contrast (custom: input, button and focus ring vs parent) | ≥ 3:1 | Fail | E |
| Target size (axe `target-size` + bounding boxes) | ≥ 24 px; warn < 44 px at 360 px width | Fail / warn | E / Platform |
| Visible focus on every interactive element | Computed style changes on `:focus-visible` | Fail | E |
| Horizontal overflow | None at any width | Fail | C |
| Reduced motion | Transforms or durations drop to ~0 | Fail | E |
| Font families | ≤ 2 excluding mono and fallbacks | Fail | C |
| Default or next-default fonts (N1, N2) | Present without a reason on the sheet → tell | Tell score | C |
| Distinct font sizes / weights | ≤ 8 / ≤ 3; > 10 sizes fails | Warn / fail | R |
| Body size, line height, measure | 16-20 px; 1.3-1.6; 45-90 characters per rendered line | Warn | R |
| Uppercase text | Tracking ≥ 0.05em, ≤ 1 line | Warn | R (Butterick) |
| Spacing | ≥ 90% multiples of 4; ≤ 12 distinct values | Warn | R |
| Radius / shadow | ≤ 3 radii + full; ≤ 4 shadows; no border + blur ≥ 16 px; no coloured blur ≥ 20 px | Warn / tell | R / C |
| Palette | Cluster colours in OKLCH (ΔE_OK < 0.02); chromatic hues (C > 0.04) ≤ accent + semantic; every colour maps to a token | Warn | R |
| Gradients | Hue 240-290° → tell; `background-clip: text` → tell; gradient on semantic colours → tell | Tell score | C |
| Side-tab, glass, emoji, eyebrow, nested card, identical card grid, pill-badge hero | Per the N-table detectors | Tell score | C |
| Primary buttons in first viewport | ≤ 1 | Warn | R |
| Motion | Durations 100-500 ms; no overshoot easing; same entrance animation on < 3 sections; ≤ 2 infinite animations per viewport | Warn / tell | R / C |
| Tabular numerals | On numeric table, price and stat cells | Warn | C |
| States | Empty, loading and error render for every list or table route | Fail | C |
| Copy | Buzzword regex; > 2 em-dashes per 100 words; forced-contrast pattern; H1 contains a brief noun or verb | Tell score | C |
| Token drift vs brand sheet | Every font, colour, radius and size is on the sheet | Fail | R |
| Tell total | ≥ 4 unjustified → fail; 2-3 → send to the judge | Fail / review | R |

Hard numbers behind these: WCAG contrast 4.5:1 body and 3:1 large text and UI boundaries
([W3C 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html);
[W3C 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)), and
targets of at least 24×24 CSS px
([W3C 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)).
Count thresholds such as "eight or fewer font sizes" come from practice and are not
validated against perceived professionalism. They are regression guards, not taste scores.

**Screenshot judge checks.** Use a separate model instance from the builder, with desktop and
mobile full-page screenshots.

| Question (narrow, answerable) | Format | Label |
|---|---|---|
| Name the most and second-most prominent element. Is the most prominent one the H1 or primary CTA? | Free answer, compared with intent | R |
| From this closed word list (targets, opposites, distractors), pick the five that best describe the page | Word pick; pass if ≥ 3 targets and 0 opposites | E-method (NN/g) |
| Is any imagery generic illustration, hand-drawn SVG people, stock, or a CSS silhouette? | Yes/no + location | C |
| Do icons come from one consistent family? List any misaligned or crowded text | Yes/no + list | R |
| Does the page feel like one coherent whole rather than a collection of parts? | Pairwise vs the previous round | C (Anthropic rubric) |
| Which of A/B shows more evidence of custom decisions rather than template layouts and library defaults? | Pairwise vs the no-direction baseline, both orders | R |
| Is each recorded reason on the brand sheet visible? (one question per reason) | Yes/no per reason | R |
| Directions differ: match each preview to its adjective list | Matching, both orders | R |

### How to run the judge

- **Prefer pairwise to scores [E].** Pairwise agreement with humans is about 60% overall,
  rising to about 93% on large gaps. Absolute Likert scores match exactly only about a third
  of the time and cluster tightly
  ([arXiv 2510.08783](https://arxiv.org/html/2510.08783v1)). Use pairwise for choosing
  between rounds, between directions, and against the no-direction baseline.
- **Swap positions [E].** Run every pairwise comparison in both orders and accept only
  verdicts that agree. A disagreement is a tie: no action, keep the incumbent. This handles
  position bias and close-pair noise.
- **Use checklists, not holistic grades [E].** Use per-task yes/no items, as ArtifactsBench
  does ([arXiv 2507.04952](https://arxiv.org/abs/2507.04952)). Do not ask the judge to rate
  "ease of use", where its accuracy is near chance. Use scripted checks and ui-ux-pro-max
  rules for that.
- **Calibrate with examples [E].** Include three to five few-shot examples in the judge
  prompt: a page with many tells, a good page from the same category, and a borderline one,
  each with a written critique (the UICrit approach, +55%,
  [arXiv 2407.08850](https://arxiv.org/abs/2407.08850)).
- **Separate the judge from the builder [C].** The judge never grades its own work. Prefer a
  different model or at least a fresh context.
- **Cap rounds and keep the best [C].** Fix the top three issues per round, for a maximum of
  three rounds. Keep the best round by pairwise comparison, not the last one. On a plateau,
  pivot to another direction instead of polishing.
- **Fix the order of checks [C].** Scripts run first and are hard gates. The judge sees only
  pages that pass the scripts, so its limited reliability goes to coherence, distinctiveness
  and adjective fit.
- **Keep the ban list live [C].** Version the N-list (`references/tells.md`). When the judge
  or owner sees a new recurring pattern across clients, such as two clients' directions
  converging, add it with a detector and date it. Periodically compare finished client sites
  against each other pairwise. If the judge cannot tell two clients apart, the pipeline has
  found its next default.

Open risk: no study has tested whether vision judges are biased toward the AI look itself.
So use the judge adversarially and comparatively: render the same content with no direction
as a "generic baseline", and require the judge, in both orders, to tell the client direction
from that baseline and from other clients' directions, and to match it to its own adjectives.
