# Typography as the main driver of a premium look (web/app UI, Oct 2026)

## Which typefaces do premium products and award-winning sites use, which free fonts read premium, and which are overused or AI defaults?

### Takeaway
Premium and award-winning sites mostly use commercial neo-grotesques and editorial serifs: Apercu, GT America, Neue Haas Grotesk, Graphik, Söhne, Suisse Int'l, Diatype, Canela, Tiempos and Ogg. Sites built with AI give themselves away through Inter, plus Space Grotesk, Instrument Serif and Geist, especially a serif italic used for one accent word. The free fonts that can still read as premium are the less common Fontshare and open-source faces, and Inter used on purpose. Pangram Pangram's well-known free downloads are personal-use trials, not free for websites.

### Cited Findings
- Typewolf's "Most Popular Fonts on Typewolf" list, in order: Apercu, GT America, Futura, Founders Grotesk, Neue Haas Grotesk, Canela, Graphik, Proxima Nova, GT Walsheim, Avenir, Maison Neue, Circular, Brandon Grotesque, Ogg, Helvetica Neue. Every one is a commercial font. — [Typewolf](https://www.typewolf.com/)
- Recent Typewolf Site of the Day pairings (the latest shown are dated Dec 2025, so the page may be cached or not updated recently): Grenette + Styrene; Swear + DM Mono; DaVinci + Suisse Int'l; Kabel + Neue Haas Grotesk; Editorial Old + Neue Montreal; Tobias + Diatype + Diatype Mono; Signifier + Switzer; Arizona Flare + Dia; Agipo + Topol + Maison Neue. The pattern is a characterful serif or display face paired with a neutral grotesk, often with a mono. — [Typewolf](https://www.typewolf.com/)
- BGR reports that Apercu (Colophon) tops Typewolf's ranking. Typewolf aggregates "over 3,000 websites and type foundries". — [BGR](https://bgr.com/2238361/most-popular-web-font-2026/)
- Claim: neo-grotesques "have overtaken geometric sans-serifs as the dominant choice in professional design". Geometric sans say "we are friendly and accessible", while neo-grotesques say "we are confident and competent". "When every SaaS homepage and fintech app uses a geometric sans-serif, the category loses its ability to differentiate." — [Made Good Designs, Trending Fonts 2026](https://madegooddesigns.com/trending-fonts/) (a blog, so treat it as opinion)
- Same source: Söhne is "adopted by Stripe, Linear, and a growing number of premium tech companies". Its other premium examples are Tiempos, Canela, Ogg, Aktiv Grotesk, Suisse Int'l and ABC Diatype Mono. Serifs are "experiencing their strongest period in digital design in over a decade". Inter is "the most-used free sans-serif for UI and web design". — [Made Good Designs](https://madegooddesigns.com/trending-fonts/)
- Free options the same source names: Fontshare's Clash Display ("one of the most popular free display fonts of the year"), Satoshi and General Sans ("increasingly appearing as a free replacement for Circular"), plus Instrument Serif, Roboto Flex, IBM Plex Mono, JetBrains Mono and Space Mono. — [Made Good Designs](https://madegooddesigns.com/trending-fonts/). Note that being popular cuts against reading as premium: Clash Display and Satoshi are now very common.
- Licences:
  - Inter is "free and open source", under the SIL Open Font License 1.1. — [rsms.me/inter](https://rsms.me/inter/)
  - Fontshare (Indian Type Foundry) fonts are free for personal and commercial use under the ITF Free Font License. It has 100+ families. — [Made Good Designs, Fontshare](https://madegooddesigns.com/fontshare/)
  - Velvetyne fonts are open source and can be used, modified and redistributed freely. Collletttivo releases some open-source typefaces. — [Dribbble resources](https://dribbble.com/resources/tips/best-free-font-websites); [Creative Lives in Progress](https://creativelivesinprogress.com/articles/free-fonts-typefaces-dazed-studio-jethro-nepomuceno)
- Pangram Pangram (Neue Montreal, Editorial New and others): the foundry offers "free access to quality fonts to everyone for personal use", and "licenses are available to purchase for commercial projects". A third-party summary says web and app embedding need separate licences, with desktop licences from $30 per family. A client website therefore cannot use them free. — [Pangram Pangram About](https://pangrampangram.com/pages/about); [LicenseOrg summary](https://licenseorg.com/guide/fonts/pangram-pangram)
- AI-slop audit (primary source): Adrian Krebs scored 1,590 Show HN sites with deterministic CSS/DOM checks run in Playwright, with an estimated 5–10% false-positive rate. Three of the 16 patterns are about type:
  - "Inter used for everything, but especially the centered hero headlines"
  - "LLM tend to use certain font combos like Space Grotesk, Instrument Serif and Geist"
  - "Serif italic for one accent word in an otherwise-Inter hero"

  Results: 22% of sites triggered 4+ patterns, 32% triggered 2–3, and 46% triggered 0–1. The post's intro says "~1400" pages, which conflicts with the 1,590 in the results. — [adriankrebs.ch](https://www.adriankrebs.ch/blog/design-slop/)
- Developers Digest calls Inter "the Helvetica of the LLM era" and advises "start by not using Inter". It suggests Haas Grotesk, Untitled Sans, Söhne, Inktrap, Migra, and even Geist, which contradicts listing Geist as a slop font. It also says "Pair it with a body font that is not also Inter", and recommends writing the type system into DESIGN.md or CLAUDE.md so the agent keeps it between sessions. — [Developers Digest](https://www.developersdigest.tech/blog/ai-design-slop-and-how-to-spot-it)
- Anthropic's frontend-design skill, seen only through third-party mirrors, tells the model to avoid Inter, Roboto, Arial and system fonts and not to converge on Space Grotesk. It asks for "a distinctive display font with a refined body font". — [skills.sh mirror](https://skills.sh/anthropics/claude-code/frontend-design)
- Other blogs add that when an AI avoids Inter it falls back to Roboto, and that Inter is a problem only when nobody chose it. — [925studios](https://www.925studios.co/blog/ai-slop-design-tells); [vibecodekit](https://vibecodekit.dev/ai-slop-design) (low-authority sources)

### Inferences
- Overused or AI-default fonts to avoid as the main voice: Inter (when used unaltered as the default), Roboto, Arial and system UI fonts, Space Grotesk, Instrument Serif as a hero accent, Geist, and probably Poppins and Montserrat (a common view I could not source in this pass). Clash Display and Satoshi are heavily used Fontshare picks.
- A recipe that reads as premium at zero licence cost: a less common Fontshare grotesk (for example General Sans, Switzer or Supreme) or an open-licence grotesk, with an open-licence serif for editorial accents. Set it carefully, as described in the next section. Typewolf winners suggest the pairing pattern (characterful serif + neutral grotesk + optional mono) matters more than any single name.
- If Inter is used, it reads as intentional when you turn on the display optical size for headings, tight tracking, and cv/ss features such as cv11 (single-storey a) and ss01 (open digits). That moves it away from its default look.

### Gaps
- I did not get Fonts In Use or Awwwards statistics, so there are no quantified usage figures beyond Typewolf's ranking.
- Graphik, GT America and Söhne were not checked against each foundry's own licence or price page. They are commercial; Söhne is from Klim, GT America from Grilli Type, Graphik from Commercial Type.
- I found no sourced list of specific Google Fonts judged both high quality and under-used.
- The Typewolf homepage data may be stale (latest entries dated Dec 2025).

## Typesetting craft: optical sizes, tracking, line-height, OpenType features, wrapping, rag, scales

### Takeaway
What makes type look professionally set: tighten tracking as size grows, add tracking to all caps, keep line length to 45–90 characters, use 120–145% line spacing for body text, use real punctuation, and use `text-wrap: balance` on headings and `pretty` on paragraphs. Inter's own tracking curve gives concrete values to copy.

### Cited Findings
- Butterick's rules:
  - Body text of 15–25px on the web.
  - "Line spacing should be 120–145% of the point size."
  - "The average line length should be 45–90 characters."
  - "Use 5–12% extra letterspacing with all caps and small caps."
  - "Kerning should always be turned on."
  - "Use bold or italic as little as possible, and not together."
  - "All caps are fine for less than one line of text."
  - Use curly quotes and a real ellipsis character.
  - Butterick also says to "avoid… most free fonts, and system fonts". — [Practical Typography, summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- Inter's dynamic-metrics tracking formula is tracking = a + b·e^(c·z), where z is the font size and a = -0.0223, b = 0.185, c = -0.1745. Computed values (em): 12px ≈ +0.0005; 16px ≈ -0.011; 24px ≈ -0.0195; 32px ≈ -0.0216; 48px and up ≈ -0.0223. The page also says line height should depend on size but gives no formula. — [Inter v3 dynamic metrics (archived)](https://d.rsms.me/inter-website/v3/dynmetrics/)
- Inter 4 has an optical-size axis running from "text" to "display". Text sizes get a tall x-height and ink traps; display sizes get "clean lines, smooth curves and delicate details". Features include tnum (the same width across all weights), ss01 (open digits), ss02 (disambiguation), cv01–cv13 (for example cv11 single-storey a) and `case` (punctuation aligned to capitals). — [rsms.me/inter](https://rsms.me/inter/)
- `text-wrap`: "I personally use `balance` for headlines and `pretty` for paragraphs". `pretty` is available from Chrome 117. — [Chrome for Developers](https://developer.chrome.com/blog/css-text-wrap-pretty)
- `balance` works only on blocks of "six or less [lines] for Chromium and ten or less for Firefox". `pretty` "has a negative effect on performance" and is meant for body copy. `text-wrap-style` became Baseline in October 2024. — [MDN text-wrap-style](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-wrap-style)
- `hanging-punctuation` (first / last / allow-end) hangs quotes and brackets outside the line box. It has "Limited availability" and is not Baseline; it is generally known to work only in Safari, which I did not verify in the compat table. — [MDN hanging-punctuation](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/hanging-punctuation)
- Vercel's interface guidelines:
  - Use curly quotes, and a real ellipsis for "Rename…" and "Saving…".
  - Avoid widows and orphans by "tidying the rag and line breaks".
  - Use non-breaking spaces between a number and its unit (`10&nbsp;MB`) and in shortcuts (`⌘&nbsp;+&nbsp;K`).
  - Title Case for headings and buttons in product UI, sentence case on marketing pages.
  - Animate a wrapper rather than the text itself so anti-aliasing doesn't shift.
  - Preload critical fonts, subset with `unicode-range`, and limit variable axes to the ones used.
  - Mobile inputs at 16px or larger to prevent iOS zoom. — [Vercel Web Interface Guidelines](https://vercel.com/design/guidelines)
- MDN recommends `font-variant-*` longhands over raw `font-feature-settings` where possible. — [MDN via search summary](https://developer.mozilla.org/en/CSS/-moz-font-feature-settings)

### Inferences
- Concrete defaults, derived from the sources above:
  - Body text 16–18px, line-height 1.5–1.6 for UI and 1.4–1.45 for long-form (Butterick allows 1.2–1.45). Headings 1.05–1.2. Display text 0.95–1.05.
  - Tracking: 0 at 16px, -0.01 to -0.02em at 24–32px, about -0.02 to -0.03em at 48px and up. All-caps labels +0.05 to +0.12em.
  - `font-kerning: normal`.
  - `text-wrap: balance` on h1–h3 and `pretty` on `p`.
  - Line length 60–75ch.
- Use the display optical size or display cut for anything above about 32px. A text cut blown up to hero size looks loose and clumsy, which is one of the clearest template tells.
- Weight contrast: a small number of weights with clear jumps (for example 400 and 600, or a light 300 display against 500 UI text) reads as designed. Many close weights, or bold on everything, reads as default.

### Gaps
- I found no authoritative source for modular-scale ratios. A common practice I could not source in this pass: about 1.125–1.2 for dense UI and 1.25–1.333 or more for editorial and marketing.
- I could not find Rauno Freiberg's or Emil Kowalski's writing on type through search. Anthony Hobday's material was not retrieved.
- Oldstyle numerals (`onum`) in running text were not sourced in this pass.

## Numbers in finance and data UIs

### Takeaway
Use tabular lining figures (`font-variant-numeric: tabular-nums`) or a mono anywhere numbers are compared or change, format by locale, keep currency decimals consistent, and right-align numbers so the decimals line up.

### Cited Findings
- "Use tabular numbers for comparisons with `font-variant-numeric: tabular-nums` or a monospace font such as Geist Mono." "Display currency with either 0 or 2 decimal places, never both in the same context." "Format dates, times, numbers, delimiters, and currencies for the user's locale." — [Vercel Web Interface Guidelines](https://vercel.com/design/guidelines)
- Inter's tnum gives "fixed-width numbers… useful for tabular data", with the same width across all weights. — [rsms.me/inter](https://rsms.me/inter/)
- A Blender UI pull request adopted Inter with tnum to remove "jiggling" when numeric inputs change. — [Blender PR #112795](https://projects.blender.org/blender/blender/pulls/112795)
- Proportional lining numerals are a good default for UI and body text; switch to tabular in columns. — [search summary, low-authority typography guide](https://www.cssportal.com/css-properties/font-feature-settings.php)

### Inferences
- A good rule:
  - Proportional figures in prose and headlines; a big hero number usually looks better proportional and tightly tracked.
  - `tabular-nums` in tables, tickers, counters and timers.
  - Right-align numeric columns, keep the same number of decimals, and use `Intl.NumberFormat` for currency.
- A proportional font with tnum generally reads as more premium than a full monospace. Keep mono for code, IDs and hashes, or as a deliberate stylistic voice (the Diatype Mono and DM Mono pairings on Typewolf).
- Use `case` and lining figures next to all-caps labels.

### Gaps
- I found no authoritative source on decimal-point alignment in CSS. `text-align: "."` is not supported, so the usual approaches are right alignment plus a fixed number of decimals, or `tabular-nums`.

## How designers critique "AI typography"

### Takeaway
The criticism is mainly about default choices nobody made, not about bad fonts. Inter everywhere, the same three fallback faces, a serif italic accent word, centred heroes, all-caps section labels, and low-contrast dark-mode body text.

### Cited Findings
- Typography patterns from the Krebs audit: Inter everywhere, Space Grotesk / Instrument Serif / Geist combinations, and a serif-italic accent word. Developers Digest adds a "Centered hero set in a generic sans", "All-caps headings and section labels", and dark themes whose body text fails WCAG AA. — [adriankrebs.ch](https://www.adriankrebs.ch/blog/design-slop/); [Developers Digest](https://www.developersdigest.tech/blog/ai-design-slop-and-how-to-spot-it)
- The mechanism: models predict the most probable output, so they converge on the most common choices in their training data. — [vibecodekit](https://vibecodekit.dev/ai-slop-design); [925studios](https://www.925studios.co/blog/ai-slop-web-design-guide) (blogs)
- Fixes suggested across sources: pick fonts on purpose, pair a distinctive display face with a refined body face, use a real type scale, and write the decisions into a design file the agent reads. — [Developers Digest](https://www.developersdigest.tech/blog/ai-design-slop-and-how-to-spot-it); [skills.sh mirror of Anthropic frontend-design](https://skills.sh/anthropics/claude-code/frontend-design)
- Popular pairings "become cliches fastest", and fonts become "category signifiers rather than brand differentiators". — [Made Good Designs](https://madegooddesigns.com/trending-fonts/)

### Inferences
- For a builder agent, two kinds of check catch most of this:
  - Font-family checks: reject the AI-default fonts listed in the first section, and the serif-italic accent pattern.
  - Typesetting checks: tracking on large headings, `text-wrap` set, line length, tabular figures in data, curly quotes, and a real ellipsis.
- Because the AI fallback fonts rotate (Inter, then Space Grotesk/Geist, then Instrument Serif), any fixed "safe" list will itself become a default over time. Choose per client from a broader pool.

### Gaps
- I found no quantitative study of AI site builders' default fonts beyond the Krebs audit. The 925studios and Sailop pieces are vendor blogs.
