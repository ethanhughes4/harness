# Motion, interaction and micro-detail craft that makes interfaces feel premium (as of Oct 2026)

## Motion: durations, easing, springs, what to animate, enter/exit, interruption, reduced motion

### Takeaway
Polished UIs use short (mostly 100–300ms), strong ease-out curves, springs for anything gesture-driven or interruptible, scale-from-~0.95 (never from 0), origin-aware popovers, faster exits than entries, and *no* animation on high-frequency/keyboard actions. Generic UIs over-animate, use default `ease`/`ease-in`, `transition: all`, scale from 0, and animate layout properties.

### Cited Findings
**Durations**
- Emil Kowalski duration table: button press feedback 100–160ms; tooltips/small popovers 125–200ms; dropdowns/selects 150–250ms; modals/drawers 200–500ms; marketing/explanatory can be longer. Rule: UI animations "under 300ms"; common review fix "Reduce to 150–250ms" — [emilkowalski/skills, emil-design-eng SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md)
- A 180ms select feels more responsive than a 400ms one; tooltip transition 0.125s ease-out on transform+opacity — [Emil Kowalski, 7 practical animation tips](https://emilkowal.ski/ui/7-practical-animation-tips)
- "Animation duration should not be more than 200ms for interactions" — [Rauno Freiberg, Web Interface Guidelines (GitHub)](https://github.com/raunofreiberg/interfaces)
- A 500ms enter animation on a frequently repeated action is cited as too slow — [Emil Kowalski, Great animations](https://emilkowal.ski/ui/great-animations)

**Easing curves**
- Emil's tokens: strong ease-out `cubic-bezier(0.23, 1, 0.32, 1)` for UI interactions; strong ease-in-out `cubic-bezier(0.77, 0, 0.175, 1)` for on-screen movement; iOS-like drawer `cubic-bezier(0.32, 0.72, 0, 1)` (from Ionic) — [emil-design-eng SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md)
- Easing decision order: entering/exiting → ease-out; moving/morphing on screen → ease-in-out; hover/colour change → ease; constant motion (marquee, progress) → linear; default → ease-out. "Never use ease-in" for UI. Built-in CSS easings are usually "not strong enough"; use easings.co / easing.dev — [emil-design-eng SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md); [7 practical animation tips](https://emilkowal.ski/ui/7-practical-animation-tips)
- Sonner toasts deliberately use `ease` (not ease-out), slightly slower (400ms transform), to feel "elegant" — [Great animations](https://emilkowal.ski/ui/great-animations); [SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md)
- Jakub Krehel's hero enter: `translateY(8px)` + `blur(8px)` + `opacity:0` → rest, `800ms cubic-bezier(0.25, 0.46, 0.45, 0.94)` (marketing context, longer than UI) — [Jakub Krehel, Details that make interfaces feel better](https://jakub.kr/writing/details-that-make-interfaces-feel-better)
- Vercel: "Choose easing based on what changes: size, distance, or trigger"; never `transition: all`, list properties explicitly — [Vercel Web Interface Guidelines](https://vercel.com/design/guidelines)

**Springs**
- Apple model (WWDC23 "Animate with springs"): springs parameterised by just duration + bounce; bounce range −1.0 to 1.0 (0 = smooth, no overshoot, long tail; >0 overshoots). Presets `.smooth`, `.snappy`, `.bouncy`, tunable e.g. `.snappy(duration: 0.4)`, `.snappy(extraBounce: 0.1)`. SwiftUI now defaults to springs; session examples use `.spring(duration: 0.5)` — [WWDC Notes, Animate with springs](https://wwdcnotes.com/notes/wwdc23/10158); [Apple WWDC23 10158](https://developer.apple.com/videos/play/wwdc2023/10158/)
- Emil's recommended web spring: `{ type: "spring", duration: 0.5, bounce: 0.2 }`; traditional physics `{ mass: 1, stiffness: 100, damping: 10 }`; keep bounce 0.1–0.3 and avoid in most UI (reserve for drag-to-dismiss/playful) — [SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md)
- Jakub Krehel exit spring: `duration: 0.45, bounce: 0` — [jakub.kr](https://jakub.kr/writing/details-that-make-interfaces-feel-better)
- Lighter objects should bounce less (a card is "conceptually lighter" than an app); gestures keep the momentum/angle they were thrown with — [Rauno Freiberg, Invisible Details of Interaction Design](https://rauno.me/craft/interaction-design)

**Scale / transform values**
- Button press: `scale(0.97)` on `:active` (subtle range 0.95–0.98), `transition: transform 160ms ease-out` — [SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md); [7 tips](https://emilkowal.ski/ui/7-practical-animation-tips). Rauno: press ~0.96 or 0.9, "not 0.8" — [interfaces](https://github.com/raunofreiberg/interfaces)
- Never animate from `scale(0)`; start ≥0.9 (Emil demo 0.93/0.95 + opacity 0). Rauno: dialogs fade+scale from ~0.8, not 0→1 — [7 tips](https://emilkowal.ski/ui/7-practical-animation-tips); [interfaces](https://github.com/raunofreiberg/interfaces)
- Popovers scale from their trigger: `transform-origin: var(--radix-dropdown-menu-content-transform-origin)` / `var(--transform-origin)`; default `center` is "wrong for almost every popover"; modals are the exception — [SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md); Vercel: "Set transform origin to where the motion physically starts" — [Vercel](https://vercel.com/design/guidelines)
- Blur as crossfade mask: `filter: blur(2px)` with `filter 200ms ease, opacity 200ms ease`; keep blur < 20px (expensive, esp. Safari) — [SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md)
- Stagger: 30–80ms between items (e.g. 0/50/100/150ms), item `translateY(8px)`→0 + fade, 300ms ease-out; stagger must never block interaction — [SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md). Krehel: 100ms between title/description/buttons, 80ms between word spans — [jakub.kr](https://jakub.kr/writing/details-that-make-interfaces-feel-better)
- Hover scale `1.05` gated by `@media (hover: hover) and (pointer: fine)` — [SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md)

**What to animate / not**
- Frequency table: 100+/day (keyboard shortcuts, command palette) → no animation; tens/day (hover, list nav) → remove or drastically reduce; occasional (modals, drawers, toasts) → standard; rare/first-time (onboarding, celebrations) → can add delight. Raycast's lack of open/close animation is the model — [SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md)
- Right-click menus and the macOS app switcher appear without motion because used constantly; removing motion from command menus made Rauno "feel faster" — [Rauno, interaction design](https://rauno.me/craft/interaction-design)
- Animate only `transform`/`opacity`; padding/margin/width/height/top/left trigger layout. Prefer CSS → WAAPI → JS libraries. Framer Motion `x/y/scale` shorthands aren't hardware-accelerated; use a `transform` string — [Great animations](https://emilkowal.ski/ui/great-animations); [Vercel](https://vercel.com/design/guidelines); [SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md)
- Don't animate layered box-shadows (cost) — [Josh Comeau, Designing beautiful shadows](https://www.joshwcomeau.com/css/designing-shadows/). Krehel does transition `box-shadow` for hover on shadow-borders — [jakub.kr](https://jakub.kr/writing/details-that-make-interfaces-feel-better) (minor tension: single-layer/low-cost cases are fine)
- Looping animations pause off-screen; autoplay > 5s needs pause/stop controls — [Rauno](https://github.com/raunofreiberg/interfaces); [Vercel](https://vercel.com/design/guidelines)

**Enter/exit asymmetry**
- Exit faster than enter; "slow where the user is deciding, fast where the system is responding" (hold-to-delete 2s linear press, 200ms ease-out release) — [SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md)
- Exits should be subtler than entries: subtle exit `x: -70%`, `opacity: 0`, `blur(4px)` instead of full `calc(-100% - 4px)` slide — [jakub.kr](https://jakub.kr/writing/details-that-make-interfaces-feel-better)

**Interruption**
- Use CSS transitions (retarget mid-flight) not keyframes (restart from zero) for toasts/toggles; springs preserve velocity when interrupted — [SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md); "Animations must be interruptible by user input" — [Vercel](https://vercel.com/design/guidelines)
- Gestures: respond immediately (apply delta during pinch, then animate past a threshold); trigger lightweight actions mid-gesture, destructive ones on release; peeks reversible — [Rauno](https://rauno.me/craft/interaction-design)
- Velocity-based dismiss: velocity = |swipe|/time, dismiss if > ~0.11 regardless of distance; rubber-band damping past bounds; pointer capture; ignore extra touches — [SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md)

**Reduced motion**
- "Fewer and gentler animations, not zero": keep opacity/colour, remove movement; e.g. `animation: fade 0.2s ease` under `prefers-reduced-motion: reduce`; `useReducedMotion()` → closed x `0` instead of `-100%` — [SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md); [Great animations](https://emilkowal.ski/ui/great-animations); Vercel requires a reduced-motion variant — [Vercel](https://vercel.com/design/guidelines)

**Fluidity as product value (Family)**
- Family (Benji Taylor): pillars Simplicity → Fluidity → Delight; context-aware "trays" that vary in height to signal change; "Continue" morphs into "Confirm" via shared letters; tab switches slide in the tapped direction; commas shift as amounts are typed; "Mastering delight is mastering selective emphasis" (more delight in rarely used features) — [Benji Taylor, Family Values](https://benji.org/family-values)

### Inferences
- A safe default token set for a premium web build: `--ease-out: cubic-bezier(0.23,1,0.32,1)`, `--ease-in-out: cubic-bezier(0.77,0,0.175,1)`, durations 150/200/250ms, press `scale(.97)` 160ms, popover enter from `scale(.95)`+opacity 0 at trigger origin, exits ~20–30% shorter than entries, springs `duration .5 bounce 0–.2` for drags/drawers.
- The strongest "generic" tell is over-animation of frequent actions plus default easing; the strongest "premium" tell is motion that responds instantly and can be interrupted.

### Gaps
- Apple HIG Motion page itself was not fetched; Apple guidance here comes via the WWDC23 spring session (secondary notes). No confirmed default spring value for SwiftUI beyond examples.
- Material 3 easing/duration token values (e.g. emphasized curve) could not be retrieved (page rendered empty); not included to avoid relying on memory.
- No published concrete values from Linear/Vercel/Arc product motion specs found.

## Feedback and states: press, optimistic UI, skeletons vs spinners, toasts, numbers, focus rings

### Takeaway
Premium feedback is immediate (press scale, optimistic updates) but not flickery: loaders get a show-delay and a minimum visible time, skeletons mirror real content, toasts are interruptible/stackable, numbers use tabular figures, and focus rings are styled with box-shadow/`:focus-visible`.

### Cited Findings
- Loading timing: spinners/skeletons use a show-delay ~150–300ms and a minimum visible time ~300–500ms (prevents flash) — [Vercel guidelines](https://vercel.com/design/guidelines)
- Loading buttons show an indicator but keep the original label; use `…` in loading text ("Saving…"); keep submit enabled until submission starts, then disable + spinner + idempotency key — [Vercel](https://vercel.com/design/guidelines); disable after submit to avoid duplicate requests — [Rauno](https://github.com/raunofreiberg/interfaces)
- Optimistic updates: update UI first when success is likely; on failure roll back and show error; POST/PATCH/DELETE should complete < 500ms — [Vercel](https://vercel.com/design/guidelines)
- Skeletons should mirror final content exactly — [Vercel](https://vercel.com/design/guidelines)
- Toasts (Sonner): timers pause when tab is hidden; pseudo-elements fill gaps between stacked toasts to keep hover; transitions not keyframes so rapid toasts retarget smoothly; entry via `@starting-style` `translateY(100%)` — [SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md)
- Tooltips: delay the first, subsequent ones in the group open instantly (`[data-instant]{transition-duration:0ms}`) — [7 tips](https://emilkowal.ski/ui/7-practical-animation-tips); [Vercel](https://vercel.com/design/guidelines)
- Undo within a safe window as alternative to confirmation for destructive actions — [Vercel](https://vercel.com/design/guidelines)
- Numbers: `font-variant-numeric: tabular-nums` for tables/timers/comparisons — [Rauno](https://github.com/raunofreiberg/interfaces); [Vercel](https://vercel.com/design/guidelines); [jakub.kr](https://jakub.kr/writing/details-that-make-interfaces-feel-better). Family animates comma shifts as amounts are typed — [Family Values](https://benji.org/family-values)
- Focus rings: visible on every focusable element via `:focus-visible` (not `:focus`), `:focus-within` for groups, not covered by sticky UI — [Vercel](https://vercel.com/design/guidelines); "Box shadow should be used for focus rings, not outline" (Safari 16.4+ supports outline radius, so outline is now viable) — [Rauno](https://github.com/raunofreiberg/interfaces)
- Hover/active/focus states should have more contrast than rest — [Vercel](https://vercel.com/design/guidelines)
- Dropdowns open on `mousedown` not `click` (feels faster); nested menus use a "prediction cone" — [Rauno](https://github.com/raunofreiberg/interfaces)
- Icons appearing contextually animate `opacity` + `scale` + `blur` together — [jakub.kr](https://jakub.kr/writing/details-that-make-interfaces-feel-better)
- Showing feedback where input is obscured (enlarged key, magnifier) "gives you confidence that the interface understood" — [Rauno](https://rauno.me/craft/interaction-design)

### Inferences
- Concrete press state: `:active { transform: scale(.97) }` + 100–160ms ease-out, plus a slight background darken; focus: `box-shadow: 0 0 0 2px var(--bg), 0 0 0 4px var(--accent)` style double ring (common pattern; no specific source value found).

### Gaps
- No primary source found for specific number-transition libraries/values (e.g. NumberFlow timings) or a quantified skeleton-vs-spinner perception study within 2022–2026.
- No sourced px/alpha spec for "designed" focus ring offsets.

## Depth and materials: layered shadows, hairlines, gradients/grain, dark-mode elevation, glass

### Takeaway
Premium depth = 2+ soft shadow layers sharing one light direction, tinted toward the background hue, combined with a translucent 1px ring/hairline; in dark mode shadows give way to lighter surfaces and white-alpha hairlines; glass works only with saturation boost, extended backdrop and an edge highlight.

### Cited Findings
- Layered shadow recipes (Josh Comeau), consistent light (y offset = 2× x), as elevation rises offset/blur grow and opacity falls:
  - Small: `0.5px 1px 1px hsl(220deg 60% 50% / 0.7)`
  - Medium: `1px 2px 2px / 2px 4px 4px / 3px 6px 6px` each at `hsl(220deg 60% 50% / 0.333)`
  - Large: 5 layers `1/2/4/8/16px` offsets (x), `2/4/8/16/32px` (y), blur = y, alpha 0.2
  - Neutral: `0 1px 1px, 0 2px 2px, 0 4px 4px, 0 8px 8px, 0 16px 16px` at `hsl(0 0% 0% / 0.075)`
  - Tint shadows with the background hue, not pure black (black looks washed out on colour); use `filter: drop-shadow()` for non-rectangular shapes — [Josh Comeau, Designing beautiful shadows](https://www.joshwcomeau.com/css/designing-shadows/)
- Vercel: at least two shadow layers (ambient + direct); combine borders and shadows; semi-transparent borders improve edge clarity; tint borders/shadows/text toward background hue — [Vercel](https://vercel.com/design/guidelines)
- "Shadows instead of borders" (Krehel): light `0 0 0 1px rgba(0,0,0,.06), 0 1px 2px -1px rgba(0,0,0,.06), 0 2px 4px 0 rgba(0,0,0,.04)`; hover alphas .08/.08/.06; dark `0 0 0 1px rgba(255,255,255,.08)`, hover `.12` — [jakub.kr](https://jakub.kr/writing/details-that-make-interfaces-feel-better)
- Image treatment: `outline: 1px solid rgba(0,0,0,.1); outline-offset: -1px` (dark: `rgba(255,255,255,.1)`) — [jakub.kr](https://jakub.kr/writing/details-that-make-interfaces-feel-better)
- Dark mode: Linear builds elevation (background, panels, dialogs, modals) via LCH-generated surfaces; early explorations used only "opacities of black and white" for elevation; theme reduced from 98 variables to 3 inputs (base, accent, contrast) — [Linear, How we redesigned the Linear UI](https://linear.app/now/how-we-redesigned-the-linear-ui)
- Material dark theme: base `#121212`; elevation = semi-transparent on-surface (white) overlay increasing with elevation, e.g. 4dp app bar = 9% white; M3 replaced this with `surfaceTintColor` — [Prototypr dark theme tutorial](https://blog.prototypr.io/how-to-design-a-dark-theme-for-your-android-app-3daeb264637); [Flutter applyElevationOverlayColor](https://api.flutter.dev/flutter/material/ThemeData/applyElevationOverlayColor.html). (Full table 1dp 5% … 24dp 16% and text 87/60/38% is commonly cited but I could not fetch the primary page to verify.)
- Set `color-scheme: dark` on `<html>` and `<meta name="theme-color">` matching background — [Vercel](https://vercel.com/design/guidelines)
- Gradients: use radial gradients instead of blurred/scaled rectangles to avoid banding — [Rauno](https://github.com/raunofreiberg/interfaces); avoid CSS-mask banding by using background images — [Vercel](https://vercel.com/design/guidelines)
- Glass done well (Josh Comeau): base `backdrop-filter: blur(16px)`; extend the backdrop child to `height: 200%` with `mask-image: linear-gradient(to bottom, black 0% 50%, transparent 50% 100%)` so nearby content bleeds in (default backdrop-filter "only considers the pixels directly behind"); semi-opaque fill like `hsl(0 0% 100% / .5)`; edge highlight element 4px thick, `hsl(0 0% 100% / .1)`, `blur(12px) brightness(.96)`; saturation boost (e.g. `blur(8px) brightness(90%) saturate(140%)`) reduces muddiness; `@supports` fallback `hsl(0 0% 100% / .95)` — [Josh Comeau, Next-level frosted glass](https://www.joshwcomeau.com/css/backdrop-filter/)
- Common glass recipe (lower-authority vendor blogs): white fill 10–15% alpha, `blur(16px) saturate(160%)`, 1px light border; without saturate it "can look like dirty plastic"; faint noise overlay dithers banding; does nothing over flat backgrounds; Liquid Glass (Apple, June 2025) revived the style — [DEV: Liquid glass on the web](https://dev.to/devyatov/liquid-glass-on-the-web-6-ways-to-build-it-with-css-and-svg-3m07); [theplusaddons](https://theplusaddons.com/blog/glassmorphism/)

### Inferences
- Bad glass = blur alone over a flat or busy background with no saturation, no edge, no fallback; good glass = saturate + extended backdrop + edge + tint, used sparingly on chrome (headers, overlays).
- In dark mode, swap visible drop shadows for (a) lighter surface per elevation step and (b) 1px white ring at 6–12% alpha.

### Gaps
- No high-quality primary source with concrete grain/noise opacity values (only vendor blog mentions "low opacity").
- Primary Material dark-theme elevation table could not be fetched.

## Micro-details: optical alignment, icons, concentric radii, hit areas, scrollbars, selection, caret, favicon, fonts, images

### Takeaway
The small details reviewers notice: concentric radii, ±1px optical corrections, text-wrap balance/pretty, tabular nums, antialiased smoothing, 24px/44px hit areas, no dead zones in lists, themed SVG favicon, metric-matched font fallbacks, and image hairlines.

### Cited Findings
- Concentric radii: outer radius = inner radius + padding (include border width); derive with `calc(var(--radius) - var(--pad))`; clamp to 0 if negative — [jakub.kr](https://jakub.kr/writing/details-that-make-interfaces-feel-better); [Jakub Krehel, Concentric border radius](https://jakub.kr/work/concentric-border-radius); [DEV: concentric border radius rule](https://dev.to/sgbp/the-concentric-border-radius-rule-why-nested-rounded-corners-look-slightly-wrong-3hog); child radius ≤ parent and concentric — [Vercel](https://vercel.com/design/guidelines)
- Optical alignment: adjust ±1px where perception differs from geometry — [Vercel](https://vercel.com/design/guidelines); slightly less padding on the icon side of a button; fix icon offsets inside the SVG not via margin — [jakub.kr](https://jakub.kr/writing/details-that-make-interfaces-feel-better); Linear's redesign explicitly aligned labels, icons and buttons vertically and horizontally in sidebar/tabs — [Linear](https://linear.app/now/how-we-redesigned-the-linear-ui)
- Hit areas: expand targets < 24px to ≥ 24px; mobile ≥ 44px — [Vercel](https://vercel.com/design/guidelines); lists should have no dead areas between items (use padding, not margin) — [Rauno](https://github.com/raunofreiberg/interfaces); screen edges/corners are effectively infinite targets (Fitts) — [Rauno](https://rauno.me/craft/interaction-design)
- Typography details: `-webkit-font-smoothing: antialiased`, `text-rendering: optimizeLegibility`; avoid weights < 400; medium headings 500–600; inputs ≥ 16px (prevents iOS zoom) — [Rauno](https://github.com/raunofreiberg/interfaces); `text-wrap: balance` for titles, `pretty` for paragraphs — [jakub.kr](https://jakub.kr/writing/details-that-make-interfaces-feel-better); curly quotes, `…`, non-breaking spaces between number and unit (`10&nbsp;MB`), avoid widows — [Vercel](https://vercel.com/design/guidelines); Linear uses Inter Display for headings, Inter for body — [Linear](https://linear.app/now/how-we-redesigned-the-linear-ui)
- Scrollbars: avoid unnecessary scrollbars; on macOS set scrollbars to "Always" to see what Windows users see; `overscroll-behavior: contain` in modals/drawers, `none` on `<html>` for fine pointers — [Vercel](https://vercel.com/design/guidelines)
- Tap highlight: `-webkit-tap-highlight-color: rgba(0,0,0,0)` with a designed replacement; hover styles under `@media (hover: hover)`; `touch-action: manipulation` — [Rauno](https://github.com/raunofreiberg/interfaces); [Vercel](https://vercel.com/design/guidelines)
- Favicon: SVG with a `<style>` using `prefers-color-scheme` — [Rauno](https://github.com/raunofreiberg/interfaces)
- `<select>`: set explicit background and colour for Windows dark mode — [Vercel](https://vercel.com/design/guidelines)
- Font loading without flash/shift: `@font-face` `size-adjust` (Chrome/Edge/Firefox 92, Safari 17) plus `ascent-override`/`descent-override`/`line-gap-override` to metric-match the fallback — [web.dev, CSS size-adjust](https://web.dev/articles/css-size-adjust); preload critical fonts, subset via `unicode-range`, limit variable axes — [Vercel](https://vercel.com/design/guidelines); glyph widths can still change wrapping — [Shopify docs](https://shopify.dev/docs/storefronts/themes/best-practices/performance/reduce-cls-font-swapping.md)
- Images: explicit dimensions (no layout shift), preload only above-fold, 1px 10% alpha inset outline — [Vercel](https://vercel.com/design/guidelines); [jakub.kr](https://jakub.kr/writing/details-that-make-interfaces-feel-better). Video: `muted playsinline`, prefer `<video autoplay muted loop playsinline>` over GIFs — [Rauno](https://github.com/raunofreiberg/interfaces); [Vercel](https://vercel.com/design/guidelines)
- Anchors: `scroll-behavior: smooth` with offset / `scroll-margin-top` — [Rauno](https://github.com/raunofreiberg/interfaces); [Vercel](https://vercel.com/design/guidelines)

### Inferences
- Selection colour (`::selection` in brand tint), caret colour (`caret-color: var(--accent)`) and cursor choices are widely practised but I found no 2022–2026 craft source giving values; treat as cheap brand touches.

### Gaps
- No sourced guidance on icon stroke-width consistency values (e.g. 1.5px at 24px) from the target authors.
- No sourced scrollbar styling values (`scrollbar-width: thin`, `scrollbar-color`) from these authors.
- `::selection`, `caret-color`, custom cursor: no primary craft source found.

## Which details have the biggest perceived impact

### Takeaway
Writers on craft converge on: (1) responsiveness — remove/shorten animation on frequent actions and make everything interruptible; (2) correct easing and origin; (3) consistent, subtle depth (layered shadows + alpha hairlines); (4) "unseen details compound" — the cumulative effect of many tiny corrections rather than any single flourish.

### Cited Findings
- Emil: frequency of use decides whether to animate at all; keyboard-initiated actions never animated; "unseen details compound"; review animations the next day and at 2–5× slow-motion — [SKILL.md](https://raw.githubusercontent.com/emilkowalski/skills/main/skills/emil-design-eng/SKILL.md); [Great animations](https://emilkowal.ski/ui/great-animations)
- Rauno: removing motion from core high-frequency interactions made the experience feel faster; "Truly fluid gestures are immediately responsive"; interruptibility is central — [Rauno, interaction design](https://rauno.me/craft/interaction-design)
- Benji Taylor: polish everywhere, including rarely used features, "because unpolished corners undermine the whole product"; smooth motion signals "the app is in tune with my intentions"; delight concentrated in rare moments — [Family Values](https://benji.org/family-values)
- Jakub Krehel frames premium feel as a stack of small details: text wrapping, concentric radii, interruptible animations, optical alignment, shadows instead of borders, image outlines, tabular numbers — [jakub.kr](https://jakub.kr/writing/details-that-make-interfaces-feel-better)
- Linear's redesign focused on reducing visual noise, alignment, neutral colour (less blue chrome) and contrast, i.e. restraint over decoration — [Linear](https://linear.app/now/how-we-redesigned-the-linear-ui)
- Josh Comeau: consistent light source across all shadows makes a page feel cohesive — [Designing shadows](https://www.joshwcomeau.com/css/designing-shadows/)

### Inferences
- Ranked by impact-per-effort for a builder: (1) easing tokens + ≤250ms durations + no animation on frequent actions; (2) press `scale(.97)`; (3) layered tinted shadows + 1px alpha ring (shadows-as-borders), dark-mode white-alpha hairlines; (4) concentric radii and optical alignment; (5) text-wrap balance/pretty, tabular-nums, antialiasing; (6) metric-matched font fallback; (7) image hairlines; glass only where there is a real backdrop.

### Gaps
- No empirical/user-study evidence ranking these details; ranking is based on author emphasis, not measured perception.
