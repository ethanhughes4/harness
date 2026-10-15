# Calibration example: competent but generic

Used by `agents/design-critic.md` as the "competent but generic" anchor.

## What it is

Pocket's "Instrument" mockup, made 2026-10-15. Pocket is a small offline
money app; the mockup shows the PIN, lockout, first-run and Home screens.

- `pocket-instrument-desktop.png`: the screens at desktop width.
- `pocket-instrument-phone.png`: the screens at phone width.

It passed every audit check (no Inter, no gradients, no glows, no emoji, no
centred hero, real error states). The owner still judged it AI-made.

## Verdict: COMPETENT

Not GENERIC (no tells) and not PREMIUM. The guideline measured what was
absent, not what was present. A design at this level is the floor for
COMPETENT; a design below it is GENERIC.

## The critique, with the fix values

Source: `reports/What makes sites look premium.md`, "Why the Pocket mockup
reads as competent, not premium".

| Area | What the mockup does | Why it reads generic | Fix (exact values) |
|---|---|---|---|
| Tracking | 0 everywhere except the readout at -0.02em; 20px "Enter your PIN" and the "Pocket" wordmark at 500, untracked | Default spacing at heading sizes looks unset: nobody typeset this | 16px -0.005em, 20px -0.01em, 28px -0.015em |
| Weights and hierarchy | Wordmark and "Enter your PIN" near-identical in size and weight; only 400/500 | Two adjacent headings compete; no typographic voice | Give the wordmark its own treatment; big type lighter (300-400), clear jumps between levels |
| Figures | Every figure, date and the "of £1,150.00 budgeted, 84%" line in Plex Mono; hero `£961.39` in mono with a wide gap around the "." | A calm money app looks like a terminal; the sentence in mono reads as a mistake | Readout in proportional Plex Sans (or a lighter display cut), 48-56px, weight 300-400, tracking about -0.03em, `tabular-nums` only where digits change; mono only for the dates column, or drop it |
| Font choice | IBM Plex Sans + Plex Mono | On a published "de-slop" list; becoming the next default (inference) | A licensed grotesk, or a less-used free face set with care |
| Borders | Opaque 1px `#C4C1BA` lines around every panel and input; 2px solid red error borders | Opaque grey outlines on a grey ground look like a wireframe | `0 0 0 1px rgb(26 26 25 / .08)` (dark: `rgb(255 255 255 / .08)`); error as ring plus tint |
| Depth | "No shadows"; ground `#E5E3DE` vs surface `#F5F4F0` is the only elevation | Panels float flat: a default admin template | Two-layer warm-tinted shadow `0 1px 2px rgb(60 50 40 / .06), 0 2px 6px rgb(60 50 40 / .04)` |
| Colour | Full-width saturated orange `#E0612A` slab on every screen; salmon disabled button; category colours at near-Tailwind saturation (Bills `#7B5CD6` indigo-violet); Eating-out `#E07A1F` collides with the accent | The loudest thing on a "Quiet" brand is the button | Lower chroma of every category colour in OKLCH to a shared lightness; move Bills off violet; dark ink primary button with orange only on the active dot and the "Add" key, so over-budget red is the loudest thing |
| Focal point | Home stacks three heavy blocks: black readout, orange button, saturated meters | The eye has nowhere to land | One focal element per screen |
| Readout and PIN field | Flat `#1E1E1C` slab; the empty locked PIN field is a black bar that looks redacted | The "display window" is drawn as a rectangle, not an object | Inner top highlight `inset 0 1px rgb(255 255 255 / .06-.10)` plus a ring; 6-8px radius; stepped near-blacks |
| Meters | Ten 12px saturated blocks with 4px gaps | A stock progress-bar widget, not instrument precision | Thin and precise; colour only where it carries meaning |
| Space | 16px readout padding, 12px between groups, 4px radius on everything from 6px dots to 360px panels | Crowded; the brand promised "spacious totals" | Double the padding around the total; radius scaled to size, 4px buttons nested concentrically in 8px panels |
| Interaction | 100ms colour change only; no press transform | A Braun object is defined by how its keys feel | `:active` 1px `translateY` plus inset shadow at 100ms (calculator key), or `scale(.97)` 100-160ms ease-out |

## Process cause

No reference image of a Braun ET66, T3 or a premium money app (Things,
Copilot, Mercury, Monzo) was screenshotted or measured. The target word
list rewarded "plain", so a judge could pass the build honestly. Brand
sheet "exceptions" (4px radius, no shadows) cited a recipe, not the brief.

## How the critic uses this

State whether the design under review is at, above or below this example.
A design that has the same gaps (untuned tracking, opaque borders, flat
depth, loud accent, mono figures) is at this level: COMPETENT at best.
