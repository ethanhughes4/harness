# What makes a website or app UI look AI-generated (as of Oct 2026)

Source-type key: **[M]** = measurement or systematic study; **[O]** = practitioner opinion or observation; **[V]** = vendor or tool author (has a stake). Note: several fetched pages were summarised by a fetch model, so "verbatim" quotes are as returned by that tool. Re-check any quote before publishing it.

## 1. Which tells do designers name most often, and are there numbers?

### Takeaway
There is strong agreement on one core set of tells: Inter/Geist or system-ui as the only typeface; purple/indigo-to-blue gradients, including gradient text; a centred hero with a pill badge above the H1; three (or more) identical icon-topped feature cards; one radius, padding and shadow applied to everything; colored left or top borders on cards; glassmorphism and glows; all-caps eyebrow labels; emoji used as icons; and missing states. The only large-scale measurement found is Adrian Krebs's DOM scan of about 1,590 Show HN sites. It found 22% with 4+ tells and 32% with 2–3. No source gives per-pattern prevalence.

### Cited Findings

**Measurements**
- [M] Krebs scored Show HN landing pages with Playwright, using "deterministic CSS or DOM check[s]" rather than screenshots or LLM judgment, and estimated ~5–10% false positives. Results: High (4+ patterns) 22% (347 sites); Medium (2–3) 32% (508); Low (0–1) 46% (735) of 1,590. The intro says ~1,400 sites; the article doesn't reconcile the two numbers. Dated April 20, 2026. — [Adrian Krebs, "Scoring Show HN submissions for AI design patterns"](https://www.adriankrebs.ch/blog/design-slop/)
- [M] Krebs's pattern list. This is the best ready-made checkable rule set:
  - **Fonts:** Inter everywhere, especially centred hero headlines; LLM font pairings (Space Grotesk, Instrument Serif, Geist); a serif italic accent word inside an Inter hero.
  - **Colors:** "VibeCode Purple"; permanent dark mode with grey body text and all-caps section labels; low-contrast body text in dark themes; gradients everywhere; large colored glows or colored box-shadows.
  - **Layout:** centred hero in a generic sans; badge above the hero H1; colored top or left borders on cards; identical icon-topped feature cards; numbered 1-2-3 steps; stat banner rows; sidebar or nav with emoji icons; all-caps headings.
  - **CSS:** shadcn/ui; glassmorphism.

  — [Krebs](https://www.adriankrebs.ch/blog/design-slop/); also reported by [Gigazine, Apr 23, 2026](https://www.gigazine.net/gsc_news/en/20260423-design-slop)
- [M] An academic benchmark (24 tasks, 120 interfaces from 5 generative UI tools) found "convergence in visual appearance and layout organization" across tools, while color choices varied more. Over 25% of the tools' stated design rationales were not implemented (34% for functional requirements). — [Imteyaz et al., "Design Theater", arXiv 2607.22928, Jul 2026](https://arxiv.org/abs/2607.22928)
- [M/O] NN/g tested Figma Make, Relume, First Draft, UX Pilot, Bolt, Lovable, Replit, v0, Claude and Stitch on a real redesign. Screens "appear flat and interchangeable". Problems included "a lack of visual hierarchy or grouping among related elements", "overused colors creating visual tension", "poor color contrast" and "inconsistent margin spacing". Verdict: "good from afar, but far from good." — [NN/g, Wang & Brown, Oct 24, 2025](https://www.nngroup.com/articles/ai-prototyping/)

**The most-agreed tells (pattern → why it reads as AI → detect → fix)**

1. **Inter / Geist / system-ui as the only typeface.** This is the most widely cited tell; it appears in nearly every source.
   - **Why:** It is the default "in nearly every AI design tool, component library, and website builder" ([925 Studios](https://www.925studios.co/blog/ai-slop-web-design-guide) [V]). Anthropic's prompt says "Never use: Inter, Roboto, Open Sans, Lato, default system fonts", and notes that models also converge on Space Grotesk ([Anthropic, Nov 12, 2025](https://www.claude.com/blog/improving-frontend-design-through-skills) [V]). Impeccable's "Overused font" rule: "Familiar defaults such as Inter and Geist can make unrelated products look alike" ([impeccable.style](https://impeccable.style/anti-patterns) [V]). Mania Design: "Inter paired with a system fallback and nothing else" ([Kosta Canatselis, Jul 23, 2026](https://www.mania.design/blog/spot-the-slop-a-ui-designers-guide-to-fixing-ai-defaults/) [O]). Also named by [Krebs](https://www.adriankrebs.ch/blog/design-slop/) [M] and [prg.sh](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website) [O].
   - **Detect:** the computed `font-family` of h1 and body resolves to Inter, Geist, Roboto, Arial or system-ui, and only one family is used.
   - **Fix:** choose a display face and a body face for the product's character. Mania calls this the first and highest-leverage move.
   - **Caveat:** Anthropic's own frontend-design skill now also lists the "tasteful" counter-defaults as tells: cream #F4F1EA with a serif and terracotta #D97757, near-black with an acid-green accent, and broadsheet hairline layouts ([anthropics/skills frontend-design SKILL.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)). Simply swapping Inter for Instrument Serif is itself a recognised tell ([Krebs](https://www.adriankrebs.ch/blog/design-slop/)).

2. **Purple/indigo → blue gradient ("VibeCode Purple").** This is the second most cited tell.
   - **Why:** Anthropic's prompt lists "purple gradients on white backgrounds" as a cliché ([Anthropic](https://www.claude.com/blog/improving-frontend-design-through-skills)). Other sources: [Krebs](https://www.adriankrebs.ch/blog/design-slop/), [Mania](https://www.mania.design/blog/spot-the-slop-a-ui-designers-guide-to-fixing-ai-defaults/), [prg.sh](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website), and the [avoid-ai-design](https://github.com/funboy322/avoid-ai-design) rule C1, "The canonical unchosen gradient (the Tailwind indigo-500 lineage)". Impeccable's "AI color palette" rule: "Purple gradients and bright cyan on dark backgrounds are familiar AI defaults" ([impeccable](https://impeccable.style/anti-patterns)). Ole Lehmann on X: "purple gradient, inter font, same hero layout every single time" ([X](https://x.com/itsolelehmann/status/2037215657649983917)) [O].
   - **Detect:** `linear-gradient` stops in the hue range ~240–290°; Tailwind classes such as `from-indigo-*`, `via-purple-*`, `to-blue-*` and `bg-indigo-500`/`600`.
   - **Fix:** assign color by function, with semantic token names such as `action-primary` rather than `gradient-start` ([925 Studios](https://www.925studios.co/blog/ai-slop-web-design-guide); [Mania](https://www.mania.design/blog/spot-the-slop-a-ui-designers-guide-to-fixing-ai-defaults/)). Mania notes a brand whose logo really is purple "gets a pass": the problem is the lack of intent.

3. **Gradient text** (`bg-clip-text`).
   - **Why:** avoid-ai-design rule C6 (P0): "bg-clip-text gradients are a 2024-era default flourish that also hurts legibility" ([GitHub](https://github.com/funboy322/avoid-ai-design)). Impeccable: "A gradient makes color change across a heading or number, often just for decoration" ([impeccable](https://impeccable.style/anti-patterns)).
   - **Detect:** `background-clip: text` combined with `color: transparent`.
   - **Fix:** use one solid color, and size or weight for emphasis.

4. **Centred hero + pill badge above the H1 + two CTAs + glow.**
   - **Why:** avoid-ai-design L1, "Pill badge + centered hero" (P0) ([GitHub](https://github.com/funboy322/avoid-ai-design)). Impeccable: "A small pill above the headline can look clickable and compete with the message" ([impeccable](https://impeccable.style/anti-patterns)). Also [Krebs](https://www.adriankrebs.ch/blog/design-slop/) and [prg.sh](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website). Anthropic's skill: "a big number with a small label, supporting stats, and a gradient accent is the default treatment" for heroes ([SKILL.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)).
   - **Detect:** the first section has `text-align: center`, a small rounded element before the h1, and a radial-gradient halo behind it.
   - **Fix:** lead with the actual product (a screenshot or a loop) and one specific claim.

5. **Identical icon-topped feature cards (often exactly 3).**
   - **Why:** Impeccable's "Icon tile stacked above heading" rule: "An icon in a rounded square above a heading is a familiar AI feature-card pattern". Its "Identical card grids" rule: "Repeated icon, heading, and text cards give every point the same weight" ([impeccable](https://impeccable.style/anti-patterns)). Also [Krebs](https://www.adriankrebs.ch/blog/design-slop/) and [prg.sh](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website) ("Three icon boxes below the hero").
   - **Detect:** a grid of N≥3 siblings with the same DOM shape (icon container → heading → paragraph) and equal widths.
   - **Fix:** group related ideas, vary size and layout, and give one item dominance.

6. **Colored left or top border on rounded cards ("side-tab").**
   - **Why:** Impeccable calls it the most recognisable tell: "A thick colored stripe turns an ordinary card into something that looks like an alert" ([impeccable](https://impeccable.style/anti-patterns)). Mania names the "left-edge coloured line + curve on a panel" ([Mania](https://www.mania.design/blog/spot-the-slop-a-ui-designers-guide-to-fixing-ai-defaults/)). Also [Krebs](https://www.adriankrebs.ch/blog/design-slop/).
   - **Detect:** `border-left-width` (or top) ≥2px, a non-neutral color, and `border-radius > 0` on the same element; Tailwind `border-l-4 border-*-500`.
   - **Fix:** remove it unless it signals status.

7. **Uniform radius, padding and shadow ("SaaS-card kit").**
   - **Why:** "When everything gets the same 16px radius and 24px padding, the page goes flat" ([Mania](https://www.mania.design/blog/spot-the-slop-a-ui-designers-guide-to-fixing-ai-defaults/)). Anthropic's skill: "one border-radius on everything regardless of hierarchy, the same soft grey shadow (rgba(0,0,0,.1)) under each" ([SKILL.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)). Impeccable has "Monotonous spacing", "Nested cards", "Hairline border with wide shadow" and "Extreme border-radius on cards" (it suggests ~12–16px max on cards, per the search summary of its docs) ([impeccable](https://impeccable.style/anti-patterns)).
   - **Detect:** count distinct `border-radius` and `box-shadow` values (1–2 distinct values across all cards = flag); cards nested inside cards; a 1px border plus a large-blur shadow on the same element.
   - **Fix:** scale radius to element size, choose either edge or shadow, and use spacing to show grouping.

8. **Glassmorphism, glows and neon on dark backgrounds.**
   - **Why:** Impeccable has "Glassmorphism everywhere", "Radial-gradient background halo", "Dark mode with glowing accents" and "Soft spotlight behind content" ([impeccable](https://impeccable.style/anti-patterns)). Also [Krebs](https://www.adriankrebs.ch/blog/design-slop/) (glassmorphism; colored glows; permanent dark mode with grey text).
   - **Detect:** `backdrop-filter: blur`; colored `box-shadow` with blur ≥20px; `radial-gradient` behind the hero.
   - **Fix:** use these only to solve a real layering problem.

9. **All-caps eyebrow label above every heading, and other "template chrome".**
   - **Why:** Anthropic's skill: "a tracked-out ALL-CAPS eyebrow label above every heading; meta strings joined with middle dots ('A · B · C'); … '→' appended to link and button text"; also "numbered markers (01 / 02 / 03)" when the content isn't a sequence; and "Accenting just a single word … in a headline" ([SKILL.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)). Impeccable has "Label above a heading" and "Tiny numbered section labels" ([impeccable](https://impeccable.style/anti-patterns)). [Krebs](https://www.adriankrebs.ch/blog/design-slop/) has all-caps labels, numbered steps and the serif italic accent word.
   - **Detect:** `text-transform: uppercase` plus `letter-spacing > 0.05em` on a small element placed immediately before an h2, repeated in ≥2 sections.
   - **Fix:** remove it, or fold its words into the heading.

10. **Emoji as icons.**
    - **Why:** [Krebs](https://www.adriankrebs.ch/blog/design-slop/) (sidebar or nav with emoji icons). Search summaries also mention emoji standing in for icons in nav and feature lists (21st.dev / codemyspec; not fetched).
    - **Detect:** emoji codepoints (Extended_Pictographic) inside nav items, buttons or card headers.
    - **Fix:** use one consistent icon set, or no icon.

11. **Stock or generic illustration and placeholder art.**
    - **Why:** Impeccable has "Placeholder-style illustrations" and "Rough SVG illustrations" ([impeccable](https://impeccable.style/anti-patterns)). 925 Studios points to glossy symmetrical illustrations and abstract 3D shapes ([925 Studios](https://www.925studios.co/blog/ai-slop-web-design-guide)).
    - **Fix:** use real product screenshots.

12. **Motion: the same fade-and-slide-up on every section, hover effects on every card, pulsing dots, bounce easing.**
    - **Why:** Anthropic's skill: "fade-and-slide-up entrances on each section and hover transitions on every card are the generic default and read as AI-generated" ([SKILL.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)). Mania: "Either nothing moves, or everything fades in with the same timing" ([Mania](https://www.mania.design/blog/spot-the-slop-a-ui-designers-guide-to-fixing-ai-defaults/)). Impeccable has "Pulsing status dot", "Bounce or elastic easing", "Images that move on hover" and "Auto-scrolling marquee" ([impeccable](https://impeccable.style/anti-patterns)).

13. **Default shadcn/ui + Lucide look.**
    - **Why:** [Krebs](https://www.adriankrebs.ch/blog/design-slop/) counts shadcn/ui as a pattern. The giveaways list "default shadcn components, the Lucide icons, the Inter font, the glowing gradient borders" comes from the search summary of [codemyspec](https://codemyspec.com/blog/vibe-coded-websites-look-the-same) (not fetched directly) [O].
    - **Detect:** shadcn CSS variable names (`--radius: 0.5rem`, `--primary` with stock values) left unchanged; `lucide-react` imports.
    - **Fix:** keep the library but retheme its tokens. Sources say the tools aren't the problem; unmodified defaults are.

### Inferences
- The tells that are both widely cited and machine-checkable from code or a DOM are fonts, purple gradients, gradient text, side-tab borders, uppercase eyebrows, emoji icons, glassmorphism and glow, and the count of distinct radius and shadow values. Card-grid sameness, hierarchy and imagery need a screenshot or a human or model review. Impeccable splits its rules the same way: 49 source-checkable, 12 browser-checkable, 6 design review.
- Krebs's result implies a single tell is weak evidence; co-occurrence (4+) is the signal. A rule set should score totals rather than ban single items outright. This matches Anthropic's line: "All traits are legitimate for some briefs, but they are defaults rather than choices."

### Gaps
- No per-pattern prevalence numbers were found anywhere. Krebs publishes only tiers.
- Default blue `#3B82F6` (Tailwind blue-500), sparkle ✨ icons, and fake testimonials or stats were in the brief, but I found no source that specifically names them as tells. Not verified.
- The Krebs sample size is inconsistent (1,400 vs 1,590).

## 2. Why do AI tools converge on these patterns?

### Takeaway
Two causes recur: (a) "distributional convergence", where models reproduce the statistical median of their training data; and (b) framework defaults that dominate that data and the tools' scaffolds, especially Tailwind's indigo-500 and shadcn/Inter. When the prompt leaves a decision open, the model fills it with the default.

### Cited Findings
- [V] Anthropic names the cause "distributional convergence": safe, common design choices dominate training data, so unguided models default to them. — [Anthropic, "Improving frontend design through Skills", Nov 12, 2025](https://www.claude.com/blog/improving-frontend-design-through-skills)
- [O] Adam Wathan (Tailwind) apologised on X in Aug 2025 for making every Tailwind UI button `bg-indigo-500` five years earlier, "which caused every AI-generated interface on Earth to turn purple" (tongue-in-cheek). — [X post](https://x.com/adamwathan/status/1953510802159219096), as reported by [prg.sh, Oct 26, 2025](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website) and [AIbase](https://news.aibase.com/zh/news/20365). The causal link is commentary, not something Wathan or a lab documented.
- [O] "Not because purple is objectively good. Because purple is statistically common in the training corpus." — [prg.sh](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website)
- [M/O] NN/g: the tools' "pattern-matching tendency drives them toward the most common solutions, not the most contextually meaningful ones"; output is "biased toward mainstream design conventions". — [NN/g](https://www.nngroup.com/articles/ai-prototyping/)
- [M] Convergence in "visual appearance and layout organization" across 5 tools. — [arXiv 2607.22928](https://arxiv.org/abs/2607.22928)
- [O] "These headlines say nothing about the actual product because AI generates them by averaging every headline it has seen." — [925 Studios](https://www.925studios.co/blog/ai-slop-web-design-guide)
- [O] On Inter specifically: it is the default in component libraries and builders. — [925 Studios](https://www.925studios.co/blog/ai-slop-web-design-guide)
- [V] Anthropic's skill warns that the escape route converges too: cream/serif/terracotta, acid-green on black, and broadsheet looks are "defaults rather than choices". — [SKILL.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)

### Inferences
- A "never use Inter" rule simply moves the model to the next default (Space Grotesk, Instrument Serif, cream + terracotta). Rules should require a stated reason for each choice tied to the brief, not just a ban list. Anthropic's skill does this through a written design plan before any code.

### Gaps
- There is no published lab study isolating training-data versus scaffold-template effects. v0/Lovable/Bolt template contents were not examined directly.

## 3. Copy and content tells

### Takeaway
The tells are vague, aspirational, interchangeable headlines ("Build the future of work"), buzzword verbs (unlock, supercharge, empower, world-class), em-dash overuse, "Not X. A Y." forced contrasts, and copy that names no concrete product fact. The usual test is whether a competitor could use the line unchanged.

### Cited Findings
- [O] Example headlines "Build the future of work" and "Scale without limits". Test: could a competitor use the line unchanged? Good examples given: Stripe's "Financial infrastructure for the internet" and Linear's "Plan and build products". — [925 Studios](https://www.925studios.co/blog/ai-slop-web-design-guide)
- [O] Mania: a headline that says "Build the future of work" and means nothing. Fix: write in a real person's voice, and check whether the founder would say it aloud. — [Mania](https://www.mania.design/blog/spot-the-slop-a-ui-designers-guide-to-fixing-ai-defaults/)
- [O] Words to avoid: "Unlock, Unleash, Exceed, Empower, Game-changer, Supercharge … they've been used so much that they start to feel like empty buzzwords." — [Microcopy Examples, "Avoid landing page words"](https://microcopyexamples.substack.com/p/avoid-landing-page-words)
- [V] Impeccable copy rules:
  - "Generic marketing claims": "Words like 'supercharge' and 'world-class' promise a lot without explaining the product."
  - "Forced contrast": "Repeated lines like 'Not a feature. A platform.'"
  - "Em-dash overuse": "A dash in every sentence is a familiar AI writing habit."
  - "Same text repeated inside one container."
  - "Calling things 'theater'."

  — [impeccable](https://impeccable.style/anti-patterns)
- [V] Anthropic's skill copy guidance: write from the user's perspective, use active verbs ("Save changes", not "Submit"), keep button labels consistent with the toasts they trigger, use sentence case, and write errors that say what went wrong and how to fix it. — [SKILL.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)
- [O] Stock section order (hero, logos, features, stats, pricing, CTA) appears as an audit item. — per the search summary of [funboy322/avoid-ai-design](https://github.com/funboy322/avoid-ai-design) (not confirmed on the fetched page)

### Inferences
- Detection: a regex word list (unlock, unleash, supercharge, empower, seamless, elevate, world-class, game-changer, "the future of"); a count of em-dashes per 100 words; a "Not X. Y." pattern; and a check that the hero H1 contains a product noun or verb from the brief.

### Gaps
- "Seamless" and "Elevate" were not confirmed as cited tells by any fetched source.
- No sourced data on fake testimonials, invented stats ("10k+ users") or lorem ipsum as a tell. Rocket mentions lorem ipsum filler from vague prompts (search summary only).

## 4. Tells in app UI (dashboards, settings, lists, empty states)

### Takeaway
In apps the tells shift from decoration to structure: every metric in its own card; an equal 3- or 4-up KPI grid; everything visible at once with flat hierarchy; only the happy path designed (no empty, loading or error states); proportional numerals in tables; gradients on status colors; and pulsing "live" dots everywhere.

### Cited Findings
- [V] Six default failures of AI dashboard output:
  1. "Card overuse": "cards group, never decorate".
  2. "The equal-3 KPI grid": use an asymmetric layout with one dominant metric instead.
  3. "Sans-serif numbers in tables": use tabular numerals.
  4. "Decorative gradients in status colors": use solid semantic colors.
  5. "No empty / loading / error states".
  6. "Live indicators on everything": the guide's suggested cap is ≤2 per viewport.

  The same guide says choosing the wrong dashboard archetype is the most common reason a dashboard feels off. — [Laith0003/ux-skill wiki](https://github.com/Laith0003/ux-skill/wiki/How-to-design-a-dashboard-with-Claude-Code)
- [O] "AI nails the happy path every time." Also "AI generally creates layouts & pages that shows everything, all at once." Fix: progressive disclosure. — [Mania](https://www.mania.design/blog/spot-the-slop-a-ui-designers-guide-to-fixing-ai-defaults/)
- [M/O] NN/g: lack of hierarchy and grouping; inconsistent margins; secondary information in focus "at the expense of the primary one"; a large gap separating a password from its link. — [NN/g](https://www.nngroup.com/articles/ai-prototyping/)
- [M] Four of five generative UI tools implemented ≤6% of functional UX principles. Functional rationales went unimplemented 34% of the time. — [arXiv 2607.22928](https://arxiv.org/abs/2607.22928)
- [O] Missing functional details: validation, required-field indicators, error states, accessibility. — [prg.sh](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website)
- [V] Impeccable includes "Pulsing status dot", "Nested cards", "Flat type hierarchy" and "Monotonous spacing". — [impeccable](https://impeccable.style/anti-patterns)
- [O] Vague prompts produce "placeholder cards, and a generic layout that could belong to any app type" (search summary). — [Rocket](https://www.rocket.new/blog/best-ai-prompts-to-build-a-saas-dashboard). Its "42% of AI-generated interfaces look nearly identical" figure is unsourced; do not use it.

### Inferences
- Checkable app rules:
  - Every list or table view has empty, loading and error variants.
  - Numeric table cells use `font-variant-numeric: tabular-nums`.
  - A KPI row is not N equal-width cards of identical structure.
  - At most 2 animated status indicators per view.
  - Status colors are solid.
  - No card nested inside a card.

### Gaps
- Settings pages, list views and forms in AI-built apps have little dedicated critique. NN/g covers a profile page only.

## 5. Published lists, skills and tools that detect or prevent the look

### Takeaway
There are now several reusable rule sets. Anthropic's frontend-design skill and its Nov 2025 blog prompt are the canonical prevention text. Impeccable (Paul Bakaus) has a 67-entry anti-pattern catalog with a CLI detector. avoid-ai-design is a zero-dependency scanner with a 67-tell catalog. Krebs's 16–18 DOM checks are the only published scoring with prevalence data.

### Cited Findings
- [V] **Anthropic frontend-design skill.** It lists 5 trait clusters:
  1. Cream background + serif + terracotta #D97757.
  2. Near-black + acid-green or vermilion accent.
  3. Broadsheet hairline layout.
  4. The SaaS-card kit.
  5. Template chrome: eyebrows, middle dots, em-dash labels, #0B0B0B/#111 standing in for black, mono data labels, "→" in links.

  Process: write a design plan (4–6 named hex colors, type roles, ASCII wireframes) and review it for defaults before coding; put boldness in one element; "remove one accessory" before finishing. — [anthropics/skills SKILL.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)
- [V] **Anthropic `<frontend_aesthetics>` prompt** (~400 tokens). It covers typography, color, motion and backgrounds, and bans Inter, Roboto, Open Sans, Lato and system fonts, plus "purple gradients on white backgrounds". — [Anthropic blog, Nov 12, 2025](https://www.claude.com/blog/improving-frontend-design-through-skills)
- [V] **Impeccable.** 67 entries: 61 detector rules and 6 design-review patterns. By check method: 49 source, 12 browser, 6 review. Run with `npx impeccable detect` on files, HTML or URLs, and in CI. It also checks against a project DESIGN.md (font, color, radius or size outside the system). — [impeccable.style/anti-patterns](https://impeccable.style/anti-patterns). Different versions quote 24–38 rules; counts vary by snapshot (search summary).
- [V] **avoid-ai-design.** A 67-tell catalog with P0/P1/P2 ranking. The Node scanner exits 2 on any P0 or P1. It covers "purple-gradient slop and the 'tasteful' defaults (cream + terracotta, mono chrome)". It notes that palette weight, rhythm and hierarchy need a render. — [GitHub](https://github.com/funboy322/avoid-ai-design)
- [M] **Krebs's Playwright DOM scorer.** Described under section 1. — [adriankrebs.ch](https://www.adriankrebs.ch/blog/design-slop/)
- [O] **Other guides:**
  - [Mania Design, "Spot the Slop" (7 tells)](https://www.mania.design/blog/spot-the-slop-a-ui-designers-guide-to-fixing-ai-defaults/)
  - [925 Studios guide (6 tells)](https://www.925studios.co/blog/ai-slop-web-design-guide). Its stats (e.g. "40–62% of AI code has flaws") have no stated method; don't use them.
  - [Laith dashboard wiki](https://github.com/Laith0003/ux-skill/wiki/How-to-design-a-dashboard-with-Claude-Code)
  - Hallmark ([dev.to](https://dev.to/rams901/hallmark-stop-ai-generated-ui-slop-in-one-command-in-2026-3p9n)); not fetched.

### Inferences
- The repo already vendors ui-ux-pro-max and web-design-engineer. Impeccable's catalog and Krebs's DOM checks are the best sources for turning these notes into deterministic checks. Anthropic's "defaults rather than choices" framing argues for scoring co-occurrence plus a brief-justification step, rather than hard bans.

### Gaps
- I didn't check whether the avoid-ai-design and Impeccable "67" counts are coincidence or shared lineage.
- The v0, Lovable and Bolt docs were not checked for their own anti-generic guidance.
- No YouTube transcripts or Bluesky threads were reviewed.
