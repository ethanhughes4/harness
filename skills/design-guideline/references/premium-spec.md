# Premium spec: default craft values (D102)

Source: `reports/What makes sites look premium.md`, section "Changes to the pipeline" 2, and
the measured CSS in `research_notes/What makes sites look premium/product_teardowns.md`
(live stylesheets of each site, fetched 2026-10-15; public marketing sites, not logged-in
apps). Motion values: `motion_and_detail.md`.

Labels: **[M]** measured (live CSS of premium products, or a controlled study). **[C]**
consensus (several independent practitioners or vendors agree). **[P]** practitioner opinion
or inference. Values are not invented; where a source gives no exact value it says so.

These defaults sit under the brand. They change how type, colour and depth are *finished*,
not which hue or face is chosen.

## Override rule

The brand sheet may replace a default only by **naming the reference (from
`docs/design/reference-spec.md`) or the brief fact that shows the alternative working.** A
recipe name is not a reason ("the dieter-rams recipe says no shadows" fails). The reviewer
checks that the named reference or fact is real and that the override is built.

## Reference-range rule

Once `docs/design/reference-spec.md` exists, each property has a range across the
references (min to max of the measured values). **A client value outside that range needs a
recorded reason** (a reference that shows it working, or a brief fact). The defaults below
are the starting point when no reference value exists for a property. `design_audit.py
--compare reference-spec.json` reports client vs reference median and range.

## Values

### Colour

| Area | Default (CSS-ready) | Source | Label |
|---|---|---|---|
| Text, light theme | Off-black tinted toward the brand hue, OKLCH L about 0.18-0.26. Range `#191c1f` to `#282a30`. Never `#000`. Measured: Mercury `#272735`, Linear light `#282a30`, Stripe `#061b31`, Revolut `#191c1f`, Monzo `#091723`, Things `#212224` | live CSS of each | M |
| Ground, light | Off-white or lightly tinted, range `#f4f2f0` to `#f8fafd`. `#fff` only for raised surfaces. Measured: Ramp `#F4F2F0`, Notion `#f9f9f8`, Apple `#f5f5f7`, Stripe `#f8fafd`, Mercury beige `#f6f5f2` | live CSS | M |
| Text, dark theme | `#ECEAE4` to `#f7f8f8`, never `#fff`. Linear primary `#f7f8f8`, secondary `#d0d6e0`, tertiary `#8a8f98`, quaternary `#62666d` | linear.app | M |
| Dark surfaces | Stepped near-blacks, about +2-3% L per level, e.g. `#08090a`, `#0f1011`, `#141516`, `#191a1b` (Linear). Elevation by a lighter surface, not a shadow | linear.app | M |
| Accent and data colour | One accent over a small area; neutrals tinted toward it; palette built in OKLCH; semantic and data colours share a lightness at moderate chroma. Desaturate further only for an "established / heritage" brand, not an "innovative" one | Zhou et al. JCR 2025; Linear and Stripe colour blogs | M (perception) / C |
| Space and focus | Generous space around the one key figure or product per screen; one focal element per screen | Sevilla & Townsend; Tuch | M |

### Type

| Area | Default | Source | Label |
|---|---|---|---|
| Tracking by size | 12-14px: `0` to `-0.01em`. 16px: about `-0.011em`. 20-24px: `-0.015em` to `-0.02em`. 32px: `-0.02em` to `-0.03em`. 40px and up: `-0.022em` to `-0.04em` (to `-0.06em` for tight grotesks). All caps: `+0.05em` to `+0.12em`. Use the face's own table when it ships one (SF, Inter's curve). Light faces on dark may go slightly positive (Raycast +0.2px, Mercury +1-3%) | Linear, Vercel, Inter curve, Apple, Mercury, Raycast, Butterick | M / C |
| Inter's own curve (em) | 12px +0.0005, 16px -0.011, 24px -0.0195, 32px -0.0216, 48px and up -0.0223 (a = -0.0223, b = 0.185, c = -0.1745) | rsms.me dynamic metrics | M |
| Weights | 2-3 weights. Large display at 300-450, UI emphasis 500-600, 700+ only with a reason. With a variable face, use in-between steps (450/550, 510/590) | Stripe 300, Vercel 450/550, Linear 510/590, Mercury 360/420/480, Apple 400/600 | M |
| Line height | Body 1.45-1.6 (UI), 1.4-1.45 (long-form); headings 1.1-1.25; display 1.0-1.1 | Linear ladder (1.6 down to 1.0-1.1), Butterick 1.2-1.45 | M / C |
| Optical size | `font-optical-sizing: auto`, or the display cut above about 32px | Linear `opsz` auto, Inter 4 | M / C |
| Text wrap | `h1, h2, h3 { text-wrap: balance }` (works to about 6 lines in Chromium, 10 in Firefox); `p { text-wrap: pretty }` | Chrome, MDN | C |
| Figures | `font-variant-numeric: tabular-nums lining-nums` in tables, counters, timers and changing values; proportional with tight tracking for one hero figure; `slashed-zero` for IDs and account numbers; `Intl.NumberFormat`; 0 or 2 decimals, never mixed; right-align numeric columns. A proportional face with `tnum` reads better than a full mono; mono only for code, IDs, or one deliberate voice (the last clause is inference) | Every fintech site measured; Vercel guidelines | M / C |
| Punctuation | Curly quotes, `…` not `...`, `&nbsp;` between a number and its unit (`10&nbsp;MB`) and in shortcuts | Vercel, Butterick | C |
| Rendering | `-webkit-font-smoothing: antialiased`; `font-kerning: normal`; inputs 16px or larger (stops iOS zoom) | Rauno interfaces; typography notes | C |

### Borders, shadows, radii

| Area | Default | Source | Label |
|---|---|---|---|
| Borders | Rings, not lines: `box-shadow: 0 0 0 1px rgb(<ink> / .06)` to `.08`; dark `rgb(255 255 255 / .08)`; hover +.04. Opaque lines only for table dividers. Measured: Vercel `0 0 0 1px #00000014`, dark `#ffffff25`; Things `0 0 0 1px rgba(0,20,49,.18) inset`; Linear `#ffffff14` | Vercel, Things, Linear, Krehel | M |
| Shadows | At least 2 layers, alpha .04-.10 each, one light direction, tinted toward the ground hue; never one dark heavy shadow. Three levels: low `0 1px 2px rgb(<tint> / .06), 0 2px 4px rgb(<tint> / .04)`; mid `0 2px 4px / .06, 0 8px 16px / .06`; high `0 4px 8px / .06, 0 16px 32px / .08`. As elevation rises, offset and blur grow while opacity falls. Do not animate layered shadows | Things (`0 2px 4px`, `0 4px 16px`, `0 8px 32px`, each .1), Stripe, Ramp, Comeau, Krehel | M / C |
| Stripe's tinted shadow (reference) | `0 27px 40.5px -27px rgba(50,50,93,.25), 0 16.2px 32.4px -16.2px rgba(0,0,0,.1)`: tinted, negative spread, falls only below the card | stripe.com | M |
| Dark highlight | `inset 0 1px rgb(255 255 255 / .06)` to `.10` on raised dark surfaces | Linear (`#ffffff0a`), Raycast (`#ffffff1a`) | M |
| Radii | A scale that grows with element size, e.g. 4/6/8/12/16 and full (Linear 4,6,8,12,16,24,32; Stripe 2,4,6,16,32; Vercel 6,12). **Nested rule:** `inner = max(outer - padding, 0)`, e.g. `calc(var(--radius-outer) - var(--pad))`; child radius is never larger than its parent's | Linear, Stripe, Monzo; Krehel concentric radius; Vercel | M / C |
| Images | `outline: 1px solid rgb(0 0 0 / .1); outline-offset: -1px` (dark: white .1); explicit width and height | Krehel, Vercel | C |

### Motion

| Area | Default | Source | Label |
|---|---|---|---|
| One curve | `--ease-out: cubic-bezier(.23, 1, .32, 1)` for entrances, exits and hover. Optional `--ease-in-out: cubic-bezier(.77, 0, .175, 1)` for on-screen movement and `--ease-drawer: cubic-bezier(.32, .72, 0, 1)` for drawers. No `ease-in`, no bare `linear` on UI (linear only for marquee or progress), no overshoot unless gesture-driven. Measured: Linear and Raycast `(.23,1,.32,1)`, Stripe `(.25,1,.5,1)`, Ramp `(.16,1,.3,1)`, Monzo `(.33,1,.68,1)`, Apple `(.4,0,.6,1)` x122 | Kowalski; live CSS of each | M / C |
| Durations (2-3 total) | Press 100-160ms; tooltip 125-200ms; dropdown 150-250ms; modal or drawer 200-300ms (drawers to 500ms); UI motion under 300ms. Exits 20-30% shorter than entries. Hover in 0ms, out 150ms (Linear: highlight in 0s, out .15s). Measured: Linear .1/.16/.25s, Vercel .15/.2s, Apple 320ms (240, 160), Stripe .3s | Kowalski, Rauno (under 200ms for interactions), live CSS | M / C |
| What animates | Only `transform` and `opacity`; list properties, never `transition: all`; no animation on actions used 100+ times a day (command menu, keyboard shortcuts) or tens of times a day (hover, list navigation: remove or cut hard); animation must be interruptible (CSS transitions retarget, keyframes restart). Autoplay over 5s needs pause. Reduced motion keeps fades and drops movement ("fewer and gentler, not zero") | Kowalski frequency table, Rauno, Vercel | C |
| Press | `:active { transform: scale(.97); transition: transform 160ms var(--ease-out) }` plus a slight background darken. Range 0.95-0.98. Hover effects only under `@media (hover: hover) and (pointer: fine)` | Kowalski, Rauno | C |
| Enter | Popovers from `scale(.95)` + `opacity: 0` at the trigger's `transform-origin` (modals excepted); never from `scale(0)`; stagger 30-80ms between items, never blocking input | Kowalski, Vercel | C |
| Exit | Faster and subtler than the entry (e.g. opacity plus a small shift, not a full slide) | Kowalski, Krehel | C |
| Loading | Show delay 150-300ms, then visible for at least 300-500ms, so fast responses never flash; skeletons mirror the final layout; buttons keep their label plus a spinner ("Saving…"); optimistic update with rollback; mutations under 500ms | Vercel guidelines | C |
| Focus | `:focus-visible` ring on every focusable element, 2px, offset from the element: `box-shadow: 0 0 0 2px var(--bg), 0 0 0 4px var(--ring)`. Never `outline: none` without a replacement. The exact offsets are practitioner convention; no source gives a spec | Vercel, Rauno | C / P |

### Platform polish

`color-scheme` on `<html>` and a matching `theme-color` meta; SVG favicon with a dark
variant; `::selection` and `caret-color` in the brand tint (P, no source values); preload
critical fonts, `size-adjust` plus ascent/descent overrides on the fallback `@font-face`,
at most 2 webfont families plus an optional mono (Stripe ships 2) [C: web.dev, Vercel].

### Target words

Add **"refined"** or **"crafted"** to every brand sheet's target word list and **"basic"** or
**"unfinished"** to its opposites, so a judge cannot pass a build only for being plain [P].

## Measured from: which product shipped which value

| Value | Shipped by (live CSS, 2026-10-15) |
|---|---|
| Heading weight 300 at md and up | Stripe |
| Weights 450 / 550; large headings at 450 | Vercel |
| Weights 510 / 590 / 680 | Linear |
| Weights 360 / 420 / 480 | Mercury |
| Only 400 and 600 | Apple |
| Tracking -0.02em at 14-20px, -0.04em at 24-32px, -0.06em at 40px | Vercel |
| Tracking -0.011em body, -0.013em small, -0.022em display | Linear |
| Tracking positive at 19-28px (+0.007 to +0.012em) | Apple (SF tracking table) |
| Tracking +1-3% on light custom type | Mercury |
| Tracking +0.2px on dark | Raycast |
| Off-black text `#272735` | Mercury |
| Off-black text `#282a30` (light), `#f7f8f8` (dark) | Linear |
| Off-black text `#061b31` | Stripe |
| Off-black text `#191c1f` | Revolut |
| Off-black text `#091723` | Monzo |
| Off-black text `#212224` | Things |
| Ground `#F4F2F0` | Ramp |
| Ground `#f9f9f8` | Notion |
| Ground `#f5f5f7` | Apple |
| Ground `#f8fafd` | Stripe |
| Ground `#f6f5f2` | Mercury |
| Dark steps `#08090a`, `#0f1011`, `#141516`, `#191a1b` | Linear |
| Ring border `0 0 0 1px #00000014` (dark `#ffffff25`) | Vercel |
| Inset ring `rgba(0,20,49,.18)`; 3-layer shadow at .1 | Things |
| Tinted shadow `rgba(50,50,93,.25)` with negative spread | Stripe |
| 4+ layer shadow, alphas .006-.09 | Ramp |
| Inner top highlight `inset 0 1px #ffffff0a` to `1a` | Linear, Raycast |
| Single box-shadow (depth from tonal blocks) | Apple |
| Easing `(.23,1,.32,1)` | Linear, Raycast |
| Easing `(.25,1,.5,1)` at .3s | Stripe |
| Easing `(.16,1,.3,1)` | Ramp |
| Easing `(.33,1,.68,1)` at .3s | Monzo |
| Easing `(.4,0,.6,1)` at 320ms | Apple |
| Durations .1 / .16 / .25s | Linear |
| Durations .15 / .2s | Vercel |
| `tabular-nums` / `tnum` | Mercury, Monzo, Stripe, Copilot, Linear (plus `slashed-zero`), Things |
| Radius scale 4-32 plus full | Linear |
| Radii 6 and 12 | Vercel |

Caveats from the source notes: counts show what a site uses most, not where. App-internal
values for Mercury, Ramp, Revolut, Monzo, Copilot, Things and Wallet were not measurable.
No study measures "premium" directly; tracking, shadow and easing values are measured
practice, not measured perception. Emil Kowalski's numbers come from his repo and secondary
packages; Rauno and Vercel numbers are from their published guidelines.
