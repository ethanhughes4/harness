# Measurable, rule-based foundations of good UI visual design (checkable automatically), Oct 2026

Legend: **[STD]** = formal standard (WCAG etc.); **[PLATFORM]** = vendor design-system spec (Material, Apple); **[RoT]** = rule of thumb from expert practice; **[RESEARCH]** = empirical study. "(canonical, not re-fetched)" = a well-known primary URL cited from prior knowledge that I didn't re-open this session. Treat those as needing a quick check before quoting verbatim.

Verification column shorthand: **CSS** = computed-style audit (Playwright `getComputedStyle` over all visible elements); **LINT** = stylelint / token linter on source; **AXE** = axe-core / Lighthouse; **VLM** = vision-model rubric on a screenshot; **IMG** = pixel/image analysis of a screenshot.

## Typography: scales, sizes, weights, line height, measure, caps, numerals, pairing

### Takeaway
Typography has the most hard numbers: body text 15–25px on the web (16–18px in practice), line height 120–145%, line length 45–90 characters (45–75 is the tighter, commonly quoted band), all-caps tracked +5–12%, and sizes taken from a constrained scale (ratio 1.2–1.25 for UI, generated fluidly with `clamp()`). Almost all of it can be checked from computed styles. Counting distinct font sizes and weights is the strongest single "system vs ad hoc" signal.

### Cited Findings
- [RoT] Body text: 10–12pt in print, **15–25px on the web**. Line spacing **120–145%** of point size. Line length averages **45–90 characters including spaces**. Add **5–12% letter-spacing for all caps and small caps**. Use all caps only for **less than one line**. Paragraph separation is *either* a first-line indent of 1–4× point size *or* 4–10pt of space between paragraphs, never both. — [Butterick, Practical Typography: Summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- [RoT] Refactoring UI advises a hand-picked, constrained set of type sizes over computing a modular ratio. Its broader principle is that constrained scales for spacing, type, colour and shadow give consistently professional results. (Seen via a third-party summary only; I couldn't get the book's exact size list.) — [Refactoring UI summary (third-party)](https://cdn.jsdelivr.net/npm/claude-code-skills@0.5.0/data/skills/ux-ui-design-system/references/refactoring-ui.md)
- [RoT/tool] Utopia generates a fluid modular scale as `clamp()` custom properties from a min and max viewport (e.g. 320→1240px), a min and max base size (e.g. 18→20px) and a min and max ratio (e.g. **1.2 → 1.25**). The output is about 8 steps (`--step--2` … `--step-5`), e.g. `--step-0: clamp(1.125rem, 1.0815rem + 0.2174vi, 1.25rem)`. — [Utopia type calculator](https://utopia.fyi/type/calculator/); [Utopia clamp guide](https://utopia.fyi/blog/clamp/)
- [RoT] APCA's guidance ties contrast to size and weight, which in effect sets body-size floors. Body text at weight 400 needs Lc 90 at 16px, Lc 75 at 18px and Lc 100 at 14px, so 18px/400 is the smallest size where Lc 75 is enough for body text. — [ACHECKS APCA table](https://www.achecks.org/apca-accessible-colour-contrast-checker/); [sass-apca README](https://unpkg.com/sass-apca@1.2.0/README.md) (secondary sources)
- [PLATFORM] Material dark theme sets text emphasis by opacity: high emphasis **87%**, medium **60%**, disabled **38%**. — [Material 2 Dark theme](https://m2.material.io/design/color/dark-theme)

### Inferences
- Checks you can script with CSS, gathering every visible text node's computed `font-size`, `font-weight`, `line-height`, `font-family`, `letter-spacing`, `text-transform`:
  - Distinct font sizes: ≤ ~8 per page passes, > ~10 suggests no scale (RoT, derived from scale step counts above). Also check that each size sits within ±1px of a geometric series with ratio 1.125–1.333.
  - Distinct weights: 2–3 is typical in professional UI (RoT, unsourced; see Gaps).
  - Font families: ≤ 2 (RoT, unsourced).
  - Body `line-height / font-size` between 1.2 and 1.45 (Butterick). Headings tighter, about 1.0–1.25 (RoT).
  - Measure: `width of text box / (font-size × ~0.5)` ≈ characters per line. Flag paragraphs over ~90 or under ~45 characters. A better way is to count characters per rendered line with `Range.getClientRects()`.
  - `text-transform: uppercase` with `letter-spacing` < 0.05em is a fail. Uppercase text longer than one line is a fail.
  - Numbers in tables, prices or stats without `font-variant-numeric: tabular-nums` (check computed `font-variant-numeric`) is a craft flag.
  - Heading/body contrast: the h1 should be ≥ ~2× body size, or the ratio should step by a scale factor. Adjacent heading levels differing by < ~1.15× read as "muddy hierarchy" (RoT inference).
- Signs of AI-default type: one family (Inter or system) at 4+ weights, 12+ distinct sizes, all-caps eyebrow labels with no tracking, centred long paragraphs. A VLM can spot these on a screenshot, but the CSS checks are deterministic and should come first.

### Gaps
- I found no primary source fixing a "maximum number of font sizes or weights". Those thresholds are practitioner rules of thumb.
- I couldn't retrieve Refactoring UI's exact type-size list or its "max 2 fonts" wording, or Bringhurst's 45–75 (66 ideal) figure. 45–75 is widely quoted, but this session only verified Butterick's 45–90.
- Font-pairing "rules" (contrast in classification, matching x-height) have no quantitative source I could verify.

## Spacing and layout: 4/8-pt systems, distinct values, grid, rhythm, alignment, grouping, density

### Takeaway
Professional UIs take every margin, padding and gap from a small scale (4- or 8-px based, roughly 8–12 steps), and they group by proximity: space *inside* a group is clearly smaller than space *between* groups. Both checks work well on computed styles and on element bounding boxes.

### Cited Findings
- [RoT] Common scales: 4pt `4, 8, 12, 16, 20, 24, 28, 32` or `4, 8, 12, 16, 24, 32, 48, 64`. Start generous and tighten. One example of grouping: an 8px label-to-field gap with 24px between fields groups form fields without borders. A 2026 blog claims 4pt overtook 8pt as the default; that claim is unverified. — [Five spacing decisions (blog)](https://blakecrosley.com/es/blog/five-spacing-decisions); [4pt vs 8pt (blog)](https://www.pravinkumar.co/blog/4pt-vs-8pt-spacing-scale-webflow-design-2026)
- [RoT] Refactoring UI: use constrained scales for spacing. — [Refactoring UI summary (third-party)](https://cdn.jsdelivr.net/npm/claude-code-skills@0.5.0/data/skills/ux-ui-design-system/references/refactoring-ui.md)
- [Tool] Project Wallace's Design Tokens view extracts and groups every colour, font-size, shadow and spacing value in a stylesheet "to show where the design system is consistent and where it drifts". Its analyzer headlines unique colours and unique font sizes. Analysis is single-page or single-site. — [Project Wallace](https://projectwallace.com/); [OpenReplay walkthrough](https://blog.openreplay.com/audit-stylesheet-project-wallace/); [metric docs](https://www.projectwallace.com/docs/metrics/values-colors-totalunique)
- [RoT/Platform] Google Android: targets separated by **≥ 8dp**. — [Android accessibility: touch target size](https://support.google.com/accessibility/android/answer/7101858)

### Inferences
- Checks:
  - CSS: gather the computed `margin-*`, `padding-*`, `gap`, `row-gap`, `column-gap` (non-zero) for all elements. Report the share of values divisible by 4 (target ≥ 90%) and the number of distinct values (target ≤ ~10–12). Values like 13px, 15px or 17px are a drift signal.
  - Alignment: from bounding boxes, gather the left x-edges of block elements and cluster them within 1px. Few distinct alignment lines means a strong grid; many near-miss edges (2–6px apart) means misalignment. This is the most "pro vs amateur" layout metric that is also cheap to compute.
  - Proximity (Gestalt): for label→control and heading→body pairs, the gap inside the pair should be < the gap to the previous or next group. A ratio of about ≥ 1.5–2× is RoT, inferred from the 8/24 example.
  - Vertical rhythm: check whether vertical gaps are multiples of the base unit or of the body line height.
  - Density: dashboards use the lower end of the scale (4–12px gaps, 13–14px text). Marketing pages use 48–128px section padding. I found no source with numbers for this; treat as RoT.
- A VLM is weak at pixel-level alignment, so use geometry for alignment and the VLM only for overall "breathing room" or crowding.

### Gaps
- No verified primary source for a number of grid columns (12 columns is the convention: Bootstrap, Material's 4/8/12 responsive columns). I didn't fetch it.
- No empirical study found that links "distinct spacing values" to perceived quality. The threshold is a heuristic.

## Colour: palette size, neutrals, accent share, contrast (WCAG 2.2/APCA), OKLCH, dark mode, semantic colours

### Takeaway
The hard rules are WCAG contrast (4.5:1 for body text, 3:1 for large text and UI components) and, as a better-perceived but non-normative check, APCA Lc thresholds (90/75/60/45/30). Dark-mode rules from Material are specific: a #121212-type base rather than pure black, elevation shown by lightening the surface (0–16% white overlay), desaturated accents (200-tone), and 15.8:1 text contrast on the base. Palette discipline (few hues, a neutral ramp, one accent) is measured by counting unique colours.

### Cited Findings
- [STD] WCAG 2.x SC 1.4.3 contrast minimum (AA): **4.5:1** for normal text, **3:1** for large text (≥ 24px, or ≥ 18.66px bold). SC 1.4.6 (AAA) requires 7:1 / 4.5:1. SC 1.4.11 non-text contrast requires **3:1** for UI component boundaries and states, and for meaningful graphics. — [W3C Understanding 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html); [Understanding 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) (canonical, not re-fetched)
- [RoT, not yet a standard] APCA ladder: **Lc 90** preferred for body text; **Lc 75** minimum for body columns (≥ 18px/400); **Lc 60** for other content text (24px/400 or 16px/700); **Lc 45** for headlines (36px/400 or 24px/700) and detailed pictograms; **Lc 30** absolute minimum for placeholder or disabled text; **Lc 15** is about the point of invisibility. APCA "is not an official standard yet". — [sass-apca README](https://unpkg.com/sass-apca@1.2.0/README.md); [ACHECKS APCA checker table](https://www.achecks.org/apca-accessible-colour-contrast-checker/); [Frenzel on Washington Post design system & APCA](https://steve-frenzel.statichost.eu/posts/learning-about-perceptual-contrast)
- [PLATFORM] Material dark theme: contrast of **15.8:1** between text and the base surface, at least **4.5:1** on the highest-elevation surface. Use **desaturated colours (200 tones)**. Text opacities 87/60/38%. Avoid pure black. — [Material 2 Dark theme](https://m2.material.io/design/color/dark-theme). The base value **#121212** is widely attributed to this page, but my fetch didn't show the hex; see Gaps.
- [PLATFORM] Material 2 elevation in dark theme: surfaces get **lighter** as they rise, using a white (onSurface) overlay: 0dp 0%, 1dp 5%, 2dp 7%, 3dp 8%, 4dp 9%, 6dp 11%, 8dp 12%, 12dp 14%, 16dp 15%, 24dp 16%. Not applied to primary or secondary coloured surfaces. Shadows stay dark. Material 3 replaces the overlay with a surface tint and tonal surface roles. — [Material 2 Dark theme](https://m2.material.io/design/color/dark-theme); [Flutter applyElevationOverlayColor](https://api.flutter.dev/flutter/material/ThemeData/applyElevationOverlayColor.html)
- [Tool] Project Wallace's `values.colors.totalUnique` counts unique colours in CSS. The vendor says a clean palette often drifts to "140+ unique values" (a marketing figure, not a benchmark). — [Project Wallace docs](https://www.projectwallace.com/docs/metrics/values-colors-totalunique); [OpenReplay](https://blog.openreplay.com/audit-stylesheet-project-wallace/)
- [RESEARCH] Colourfulness and visual complexity are the most noticeable traits at first sight. Image-based models of both, plus demographics, explain about half the variance in appeal ratings after a 500ms view (450 sites, 548 raters). The preferred level varies by person and culture (2.4M ratings, ~40k participants). — [Reinecke et al., CHI 2013](https://kgajos.seas.harvard.edu/papers/reinecke13aesthetics.pdf); [Reinecke & Gajos, CHI 2014](https://wildlab.cs.washington.edu/Publications_files/ReineckeCHI2014.pdf)

### Inferences
- Checks:
  - AXE: the `color-contrast` rule covers WCAG 1.4.3 for text. Non-text contrast (1.4.11) is mostly *not* automated, so add a script that compares border or background versus the parent for inputs, buttons and focus rings.
  - APCA: compute Lc with `apca-w3` ([GitHub](https://github.com/paularmstrong/apca-w3)) for every text node, using computed size and weight, against the ACHECKS lookup.
  - Palette size: convert all computed `color`, `background-color`, `border-color`, `fill`, `stroke` to OKLCH and cluster within ΔE_OK < ~0.02. Count *chromatic hues* (C > ~0.04) separately from neutrals. RoT targets: 1 brand or accent hue, plus semantic success/warn/error/info, plus a neutral ramp of about 8–11 steps.
  - Neutrals tinted consistently: neutral hue angles should agree, and chroma should stay small and constant.
  - Accent share: from the screenshot (IMG), the fraction of pixels in the accent hue. Low single-digit % is RoT for app UI. I found no source for a number; the "60-30-10" rule is folklore.
  - Dark mode: flag any background with L ≈ 0 (`#000`). Check that surfaces get *lighter* with z-order or elevation. Check that accent chroma in dark mode is ≤ its light-mode chroma.
  - Semantic colours: check that red/green are not the only carrier of meaning (WCAG 1.4.1). This is partly VLM-checkable.
- Signs of AI-default colour: purple-to-blue gradients, many saturated hues, pure black or pure white extremes, grey text failing contrast on tinted backgrounds. Unique-hue count and gradient detection (`background-image: linear-gradient` count) catch most of this.

### Gaps
- My fetch of the M2 page didn't show the #121212 value or the "why not pure black" reasoning. The value is widely cited but I didn't verify it this session.
- No source found for OKLCH palette-construction thresholds (e.g. equal ΔL steps). Tools such as Radix Colors, Tailwind v4 (OKLCH defaults) and Evil Martians' Harmonizer exist, but I didn't fetch them.
- No source with a quantified "accent share".

## Components and craft: radius, border vs shadow, elevation, icons, states, touch targets, motion

### Takeaway
Craft is consistency. Use one radius scale (2–3 values, with nested radius = outer − padding), a small set of shadow or elevation levels, one icon family at one stroke width, every interactive state defined, targets ≥ 24px (WCAG AA) and ideally 44pt (iOS) or 48dp (Android), and motion at roughly 100–300ms with `prefers-reduced-motion` honoured. Most of this is countable from computed styles plus scripted interaction.

### Cited Findings
- [STD] WCAG 2.2 SC 2.5.8 Target Size (Minimum, AA): pointer targets **≥ 24×24 CSS px**. Smaller targets pass only if a 24px-diameter circle centred on each one doesn't overlap another target or another undersized target's circle. Exceptions: equivalent control, inline text, user-agent control, essential. SC 2.5.5 (AAA) is the stricter **44×44**. — [W3C Understanding 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)
- [PLATFORM] Android/Material: touch targets **≥ 48×48dp** (an icon may be 24dp inside 48dp of padding), separated by ≥ 8dp. — [Google Android Accessibility Help](https://support.google.com/accessibility/android/answer/7101858)
- [PLATFORM] Apple HIG: minimum tappable area **44×44pt**. Only secondary sources were seen this session. — [Deque attest-iOS touch-target rule](https://dequeuniversity.com/rules/attest-ios/1.0/touch-target-size); Apple primary: https://developer.apple.com/design/human-interface-guidelines/accessibility (canonical, not re-fetched)
- [PLATFORM] Material 3 motion tokens: duration `short1` = **50ms**, steps through short1–4, medium1–4, long1–4 and extra-long. Emphasized easing ≈ `cubic-bezier(0.2, 0, 0, 1)`. Seen only in secondary sources; the official tokens page didn't render for fetch. — [design.md issue #47](https://github.com/google-labs-code/design.md/issues/47); [Flutter M3 motion template](https://flutter.googlesource.com/mirrors/flutter/+/HEAD/dev/tools/gen_defaults/lib/motion_template.dart); official: [m3.material.io tokens](https://m3.material.io/styles/motion/easing-and-duration/tokens-specs)
- [RoT] UI animation: about **100ms** for simple feedback (toggle, checkbox), **200–300ms** for larger transitions, rarely over ~400–500ms. Attributed to NN/g via secondary sources. Microinteractions take 100–500ms. — [U-M Library design system: motion](https://design-system.lib.umich.edu/visual-elements/motion); [W3C CSSWG archive quoting NN/g](https://lists.w3.org/Archives/Public/public-css-archive/2025Apr/0702.html)
- [STD] WCAG 2.3.3 Animation from Interactions (AAA). Honour `prefers-reduced-motion`. — [W3C Understanding 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html) (canonical, not re-fetched)
- [STD] WCAG 2.2 added 2.4.11 Focus Not Obscured (AA) and 2.4.13 Focus Appearance (AAA: indicator area ≥ a 2 CSS px perimeter, 3:1 change contrast). — [W3C What's new in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/) (canonical, not re-fetched)

### Inferences
- Checks:
  - Radius: distinct non-zero computed `border-*-radius` values; RoT ≤ 3 plus "full" (9999px). For nested elements, check that inner radius ≈ outer radius − padding. Mismatched nested radii are a known amateur tell (RoT, unsourced).
  - Shadows: distinct `box-shadow` values; RoT ≤ 3–5 elevation levels. Flag elements with *both* a visible border and a large shadow, and coloured or glow shadows.
  - Icons: inline SVGs should share the same `stroke-width` (e.g. all 1.5 or all 2) and viewBox (24). Mixed icon sources (different stroke widths or fill styles) are detectable from the DOM.
  - States: in Playwright, `hover()`, `focus()` and press each interactive element and diff the computed styles. A missing visible focus style (`outline: none` with no replacement) is a fail. Check that `[disabled]` exists with reduced contrast (Lc ≈ 30 floor). Empty, error and loading states need fixture data or a VLM look at deliberately triggered states.
  - Targets: bounding boxes of `a, button, input, [role=button]` ≥ 24×24 (axe has a `target-size` rule). Use ≥ 44 for mobile viewports.
  - Motion: computed `transition-duration` and `animation-duration` within 100–500ms. Flag `linear` easing on UI transitions, and durations over 500ms. Re-run with `page.emulateMedia({reducedMotion:'reduce'})` and confirm durations drop to ~0 or transforms are removed.

### Gaps
- Couldn't load the official M3 duration and easing token tables or Apple HIG pages directly (JS-rendered). Values come from secondary sources.
- No authoritative numeric source found for "number of radius values" or "border vs shadow" usage. Those are practitioner heuristics.

## Hierarchy: one primary action, squint test, visual weight

### Takeaway
Hierarchy is the least formalised area. The accepted heuristic is that one element (the primary CTA or headline) wins the "squint test". The DOM can partly measure this (count of filled primary-style buttons per view), and so can images (blur the screenshot, compute a saliency or contrast map). Research shows first impressions form in about 50–500ms, driven by complexity and colourfulness.

### Cited Findings
- [RoT] NN/g's squint test assesses visual hierarchy: high-priority content should still stand out when the page is blurred. Hierarchy comes from colour and contrast, scale and grouping. — [NN/g Squint Test video](https://www.nngroup.com/videos/squint-test/)
- [RoT] Squint method: is the primary CTA still recognisable, do related elements still look grouped, and do only the things that should stand out actually stand out? "Most pages have one primary focus." — [Polypane: squint test](https://polypane.app/blog/debug-your-visual-hierarchy-with-the-squint-test/)
- [RESEARCH] Aesthetic-usability effect (Kurosu & Kashimura 1995): attractive designs are perceived as more usable. Lindgaard's work suggests aesthetic judgements form in about 50ms. — secondary: [XWiki design best practices](https://design.xwiki.org/xwiki/bin/view/Proposal/DesignBestPractices); [NN/g visual design study guide](https://www.nngroup.com/articles/visual-design-in-ux-study-guide/)
- [RESEARCH] Perceived visual complexity and colourfulness can be predicted from screenshots and drive 500ms appeal judgements. — [Reinecke et al. 2013](https://kgajos.seas.harvard.edu/papers/reinecke13aesthetics.pdf)

### Inferences
- Checks:
  - DOM: count buttons styled as primary (filled background in the accent hue) visible in the first viewport. More than 1 is a flag (RoT).
  - IMG: Gaussian-blur the screenshot (σ ≈ 8–12px) and threshold the luminance or contrast against the background. The largest high-contrast blob should overlap the primary CTA or H1. Several similarly sized blobs means competing emphasis.
  - IMG: estimate complexity with edge density, compressed (JPEG/PNG) file size per pixel, or the number of distinct regions. Estimate colourfulness with the Hasler–Süsstrunk metric. Both are proxies for Reinecke's measures (inference; their exact feature set isn't reproduced here).
  - VLM: ask the model to "name the single most prominent element and the second." This works better than an absolute 1–10 "hierarchy score" (see the reliability findings below).

### Gaps
- No standard numeric threshold for visual-weight balance. The NN/g aesthetic-usability article itself wasn't fetched.

## Automation: tools and approaches, and how reliable screenshot LLM judges are

### Takeaway
Use a layered pipeline: (1) source linting (stylelint with token-enforcement rules) blocks hardcoded values; (2) computed-style audits in Playwright count distinct sizes, colours, spacings, radii and shadows and check scale membership; (3) axe-core and Lighthouse cover contrast, target size and focus, but find only about 57% of issues by volume (vendor figure); (4) a VLM rubric on screenshots handles gestalt judgements. VLM judges match humans only moderately (pairwise ~60%, ±1-point Likert agreement ~72–77%) and do well only when quality differences are large. Use them for pairwise and comparative checks and specific yes/no questions, not as the final arbiter.

### Cited Findings
- [Tool] `stylelint-declaration-strict-value` (`scale-unlimited/declaration-strict-value`) forces variables, functions or keywords for chosen properties (e.g. `#FFF` warns, `var(--color-white)` passes). Mozilla ships a similar `use-design-tokens` stylelint rule. — [npm/yarn package](https://classic.yarnpkg.com/en/package/stylelint-declaration-strict-value); [Mozilla use-design-tokens](https://firefox-source-docs.mozilla.org/code-quality/lint/linters/stylelint-plugin-mozilla/rules/use-design-tokens.html)
- [Tool] `@projectwallace/css-analyzer` (npm) returns JSON metrics, including unique colours and font sizes, for a CSS string. — [Project Wallace analyzer README](https://unpkg.com/@projectwallace/css-analyzer@7.4.0/readme.md)
- [Vendor research] Deque (2021): over 2,000 audits, 13,000+ pages, ~300k issues. Automated axe testing fully covered **57% of issues by volume**, against the commonly cited 20–30% by success-criterion count. axe prioritises zero false positives. — [Deque blog](https://www.deque.com/blog/automated-testing-study-identifies-57-percent-of-digital-accessibility-issues)
- [RESEARCH] "MLLM as a UI Judge" (arXiv 2510.08783, 2025): GPT-4o, Claude 3.5 Sonnet and Llama-3.2-11B-Vision against human ratings on 9 factors (1–7 Likert). Exact-match accuracy **35–38%**, ±1 accuracy **72–77%**, Pearson with human rankings about **0.69–0.73**. Pairwise agreement about **60%** (GPT-4o, Claude) and 53% (Llama), near chance (~50%) on Ease of Use, ~78% on "Interesting". Agreement rises to about **90–93%** when the human score gap is large. Authors: "UI testing approximators, not replacements." Note: the paper's text and its Table 4 report inconsistent pairwise numbers. — [arXiv 2510.08783](https://arxiv.org/html/2510.08783v1)
- [RESEARCH] UICrit (UIST 2024): 3,059 critiques and ratings of 983 mobile UIs from 7 experienced designers. Few-shot and visual prompting with the dataset gave a **55% gain** in LLM UI-feedback quality, but LLMs still don't match human evaluators. — [arXiv 2407.08850](https://arxiv.org/abs/2407.08850)
- [RESEARCH] Generative Interfaces (arXiv 2508.19227, 2025): Claude 3.7 scoring UI code and screenshots reached **69.0% pairwise agreement** with human annotators. The authors flag length bias. — [arXiv 2508.19227](https://arxiv.org/pdf/2508.19227)
- [RESEARCH] Screenshot-based colourfulness and complexity models predict about half the variance in appeal (with demographics). — [Reinecke et al. 2013](https://kgajos.seas.harvard.edu/papers/reinecke13aesthetics.pdf)

### Inferences
- Reliability-driven design for an automated "anti-AI-look" checker:
  1. Use deterministic metrics (CSS counts, scale membership, contrast, target size, motion durations, focus styles) as hard gates. They are reproducible and cheap.
  2. Ask the VLM narrow, checkable questions ("Is there exactly one visually dominant button above the fold? Which element?"; "Are icons from one consistent family?"; "List any text that looks misaligned"). Avoid holistic 1–10 aesthetic scores, given the ±1 accuracy of only ~75% and weak fine-grained correlation.
  3. Prefer *pairwise* VLM comparisons (before/after, or candidate versus reference design) and act only on confident, large-gap verdicts, since agreement reaches ~90% there.
  4. Few-shot the VLM with designer-critiqued examples (the UICrit approach: +55%).
  5. Watch for VLM biases (length or verbosity bias, overrating "ease of use").
- A suggested starter threshold table (RoT, to tune per project): font sizes ≤ 8, families ≤ 2, weights ≤ 3, spacing values ≤ 12 with ≥ 90% on the 4px grid, chromatic hues ≤ 3 plus semantic colours, radius values ≤ 3, shadow levels ≤ 4, transition durations 100–500ms, targets ≥ 24px (≥ 44px on mobile), body line-height 1.2–1.45 (Butterick: 120–145%), measure 45–90 characters, text contrast ≥ 4.5:1 or APCA Lc ≥ 75 for body.

### Gaps
- No published study validates count thresholds (e.g. "≤ 8 font sizes") against perceived professionalism. These are inferred heuristics.
- No found benchmark of VLM reliability specifically on detecting "AI-default look" (generic gradients, emoji icons, uniform cards).
- Lighthouse's design-relevant audits weren't fetched this session. It runs a subset of axe rules, including colour contrast and tap targets (canonical: https://developer.chrome.com/docs/lighthouse/accessibility/).
