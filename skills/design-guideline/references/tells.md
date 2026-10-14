# The tells list (N1-N19)

Version: 2026-10-14 v1. Source: `reports/Design guideline against AI look.md`.

Labels: **[E]** evidence-backed (a standard or a measured study). **[C]** consensus
(several independent practitioner or vendor sources agree). **[R]** rule of thumb
(practice or inference, unvalidated).

A tell is a default, not a crime. Any item may be used if the brand sheet
(`docs/design/design-system.md`) records a reason that names the brief, the client's
existing assets, or a competitor gap. "It looks modern/clean/premium" is not a reason.

## Scoring rule

Score tells per page. **Four or more unjustified tells fail the build. Two or three
trigger review. [R; Krebs's tiers measure prevalence, not human judgement.]** One tell
with a recorded reason passes. (Krebs scanned about 1,590 Show HN sites: 22% had four or
more tells, another 32% had two or three. Source: https://www.adriankrebs.ch/blog/design-slop/)

## The tells

| # | Tell | Why it reads as AI | Detect | Fix | Label |
|---|---|---|---|---|---|
| N1 | Inter, Geist, Roboto, Arial, Open Sans, Lato or system-ui as the only family, or as the display face | Default of every component library and builder | Code: computed `font-family` of h1 and body resolves to one of these and only one family is used | Pick display and body faces from the brief's type class (serif traditional, sans casual, mono plain), with a reason | C |
| N2 | Next-default fonts: Space Grotesk, Instrument Serif, Fraunces, or a serif italic accent word in a sans hero | What models switch to once Inter is banned | Code: font list match. Screenshot: one italic serif word in the H1 | Same as N1. The reason must not be "to avoid Inter" | C |
| N3 | Indigo/violet gradient (hue ~240-290°), Tailwind `indigo/purple/violet` 500-600 | Tailwind-lineage training median | Code: parse `linear-gradient` stops to OKLCH hue; class names `from-indigo-*`, `via-purple-*` | Colour by function with semantic tokens (`action-primary`). Purple is fine if the brand owns it | C |
| N4 | Gradient text | 2024-era flourish that also hurts legibility | Code: `background-clip: text` + transparent colour | Solid colour; emphasis by size or weight | C |
| N5 | Centred hero + pill badge above H1 + two CTAs + radial glow | Statistical default hero | Code: first section `text-align:center`, small rounded element before h1, `radial-gradient` behind | Lead with the real product (screenshot or loop) and one specific claim | C |
| N6 | Three or more identical icon-topped cards | Gives every point equal weight; template rhythm | Code: ≥3 siblings with the same DOM shape (icon → heading → text) and equal widths | Group, vary size, give one item dominance | C |
| N7 | Coloured left or top border on rounded cards | Turns cards into alerts; template leftover | Code: `border-left/top-width ≥ 2px`, non-neutral colour, `border-radius > 0` on the same element | Remove unless it signals status | C |
| N8 | One radius, padding and shadow on everything; 1px border plus wide shadow; cards nested in cards | SaaS-card kit; flat hierarchy | Code: identical radius on elements differing >3× in size; border + blur ≥ 16px on one element; card inside card | Radius scales with element size; choose edge or shadow; group with spacing | C |
| N9 | Glassmorphism, coloured glows, neon on dark, radial spotlight halos | Decoration with no layering job | Code: `backdrop-filter`; coloured `box-shadow` with blur ≥ 20px; hero `radial-gradient` | Use only to solve a real layering problem | C |
| N10 | Template chrome: tracked all-caps eyebrow above every heading, "A · B · C" meta strings, "→" appended to links, 01/02/03 on non-sequences, one accented headline word | Mechanical rhythm | Code: uppercase + `letter-spacing > 0.05em` on a small element directly before h2 in ≥ 2 sections; regex for `·` joins and trailing `→` | Remove, or fold the words into the heading | C |
| N11 | Emoji as icons | "Unprofessional, so add emoji" habit | Code: Extended_Pictographic code points inside nav, buttons or headings | One icon set at one stroke width, or no icon | C |
| N12 | Second-generation "tasteful" defaults: cream (#F4F1EA-like) + serif + terracotta; near-black + acid green or vermilion; hairline broadsheet; `#0B0B0B`/`#111` standing in for black | The anti-slop escape routes, now medians themselves | Code: palette match within ΔE_OK < 0.05 of the listed values plus a serif display face. Screenshot: hairline-rule editorial grid | Derive the palette from brief adjectives and the competitor gap | C |
| N13 | Same fade-and-slide-up on every section; hover lift on every card; pulsing dots; bounce or elastic easing | "Either nothing moves, or everything fades in with the same timing" | Code: same `animation-name` on ≥ 3 sections; `cubic-bezier` overshoot (y > 1); > 2 infinite animations per viewport | One orchestrated motion moment, chosen for the brief | C |
| N14 | Unmodified shadcn/ui + Lucide tokens | Library defaults left unchanged | Code: stock `--radius: 0.5rem` and stock `--primary` values | Keep the library, retheme its tokens | C |
| N15 | Placeholder or generic art: SVG-drawn people, abstract 3D blobs, glossy stock | Zero recognition value | Screenshot: "is any imagery generic illustration or a hand-drawn SVG scene?" | Real product screenshots or client photography; otherwise an honest labelled placeholder | C |
| N16 | Happy path only: no empty, loading or error states; everything shown at once | AI designs only the ideal state | Code/test: each list or table route rendered with fixture data that is empty, slow and failing | Design all three states; progressive disclosure | C |
| N17 | Equal three- or four-up KPI cards; decorative gradients on status colours; > 2 "live" indicators per view | Dashboard defaults | Code: equal-width identical KPI siblings; gradient on semantic colours; animated indicator count | One dominant metric, asymmetric layout, solid semantic colours | C/R |
| N18 | Generic copy: "the future of", unlock, unleash, supercharge, empower, world-class, game-changer; "Not X. A Y."; em-dash in most sentences | Averaged headlines that say nothing about the product | Code: word-list regex; em-dashes per 100 words > 2; forced-contrast regex; H1 lacks a product noun or verb from the brief | Would a competitor use this line unchanged? Rewrite with a concrete product fact | C |
| N19 | Fabricated stats, fake logos, dummy testimonials | Damages credibility | Code: numbers or logos not present in the brief or assets | "Real data needed" placeholder | C (integrity) |

N19 note: no independent source names fabricated stats as an AI tell. Treat it as an
integrity rule, not a detection signal.

## Adding a tell

The list is living. A fixed list goes stale within a model generation, and models route
around bans to the next default.

When the judge or the owner sees a new recurring pattern across clients (for example two
clients' directions converging), add a row:

1. Number it next (N20, N21 ...). Never renumber.
2. Fill all columns: tell, why it reads as AI, detect, fix, label.
3. Give a detector. Prefer a code check (computed style or DOM). If only a screenshot
   question works, write the yes/no question.
4. Date the change in the history below and bump the version at the top.
5. Add the detector to `scripts/design_audit.js` if it is a code check.

From time to time, compare finished client sites against each other, pairwise. If the
judge cannot tell two clients apart, the pipeline has found its next default.

## History

- 2026-10-14 v1: N1-N19 from the design guideline report.
