# Product teardowns: craft details behind premium product UIs and sites (as of Oct 2026)

Method note: most values below are **primary data**. I fetched each site's homepage and its linked stylesheets with curl on 2026-10-15 and counted declarations (font-face families, custom-property tokens, letter-spacing, radii, easing curves, durations, shadows, hex colours). These are tagged **[live CSS]** with the site URL as the source.

- **Counts:** frequency counts show what a site uses most, not where it uses it. Mapping a value to a component (for example "this is the hero") is marked **(inferred)**.
- **Marketing sites only:** these are the public sites, not logged-in product apps. App-internal values for Mercury, Ramp, Revolut, Monzo, Copilot, Things and Apple Wallet were not measurable.
- **Failed fetches:** Aesop's site returned a 5 KB bot-blocked shell, and Teenage Engineering rendered mostly through JS. Both are thin.
- **Third-party guides:** several "DESIGN.md" or design-guide pages (blakecrosley.com, webdesignhot, shadcn.io/design, kombai) are third-party, partly AI-generated reconstructions. They are cited only where they agree with live CSS, or are flagged.

---

## 1. What concrete details does each product use? (per-product teardown)

### Takeaway
On a typeface level the premium set splits into two camps. Licensed or custom grotesques with tuned tracking: Stripe/Söhne, Revolut/Aeonik, Ramp/Lausanne, Mercury/Arcadia, Monzo/MonzoSans, Apple/SF Pro, Vercel/Geist. Tuned Inter: Linear, Raycast, Notion. Almost all of them use non-default variable weights (Linear 510/590/680, Vercel 450/550, Mercury 360/420/480), size-dependent letter-spacing, tabular figures, borders drawn as 1px low-alpha rings or shadows, layered low-opacity shadows, and a single strong ease-out curve at 150–320 ms.

### Cited Findings

**Linear (tool)**
- **Type families:** `--font-regular: "Inter Variable", "SF Pro Display", -apple-system…`, `--font-monospace: "Berkeley Mono", ui-monospace, "SF Mono"…`, and `--font-serif-display: "Tiempos Headline"`. @font-face loads Inter Variable and Berkeley Mono (Berkeley Mono is a paid licence). — [live CSS, linear.app](https://linear.app/)
- **OpenType and optical sizing:** `--font-settings: "cv01","ss03"` and `--font-variations: "opsz" auto`. Inter's optical-size axis is switched on automatically. — [live CSS, linear.app](https://linear.app/)
- **Weights:** non-standard variable weights `--font-weight-normal:400`, `medium:510`, `semibold:590`, `bold:680`, `light:300`. — [live CSS, linear.app](https://linear.app/)
- **Text scale (size / line-height / tracking):**

  | Token | Size | Line-height | Tracking |
  |---|---|---|---|
  | tiny | 0.625rem | 1.5 | -0.015em |
  | micro | 0.75rem | 1.4 | 0 |
  | mini | 0.8125rem | 1.5 | -0.01em |
  | small | 0.875rem | 21/14 | -0.013em |
  | regular | 0.9375rem (15px) | 1.6 | -0.011em |
  | large | 1.0625rem | 1.6 | 0 |

  Tracking is negative at UI sizes and back to 0 at large and micro. — [live CSS, linear.app](https://linear.app/)
- **Title scale:** title-1 1.0625rem, title-2 1.25rem, title-3 1.5rem (all -0.012em), title-4 2rem, title-5 2.5rem, title-6 3rem, title-7 3.5rem, title-8 4rem, title-9 4.5rem (title-4 to title-9 at -0.022em). Line-heights tighten from 1.4 down to 1.0–1.1 as size grows. — [live CSS, linear.app](https://linear.app/)
- **Numbers:** `font-variant-numeric: lining-nums tabular-nums slashed-zero` and `font-feature-settings: var(--font-settings), "zero"`. — [live CSS, linear.app](https://linear.app/)
- **Dark surfaces as stepped levels:** bg-level-0 `#08090a`, level-1 `#0f1011`, level-2 `#141516`, level-3 `#191a1b`, marketing bg `#010102`. The light theme runs `#fff`, `#f8f8f8`, `#f4f4f4`, `#f0f0f0`. — [live CSS, linear.app](https://linear.app/)
- **Text colours (dark):** primary `#f7f8f8`, secondary `#d0d6e0`/`#b4bcd0`, tertiary `#8a8f98`, quaternary `#62666d`. Light-theme primary is `#282a30`, not black. — [live CSS, linear.app](https://linear.app/)
- **Borders and brand:** border-primary `#23252a` or `#ffffff14` (white at 8%). Brand `#5e6ad2`, accent `#7170ff`. — [live CSS, linear.app](https://linear.app/)
- **Radius:** scale of 4, 6, 8, 12, 16, 24, 32px plus 9999px. — [live CSS, linear.app](https://linear.app/)
- **Shadows (light theme):** low `0 1px 4px -1px #00000017`, medium `0 3px 12px #00000017`, high `0 7px 24px #0000000f`.
- **Button shadow (dark):** a 4-layer stack, `inset 0 0 0 1px #ffffff08, inset 0 1px #ffffff0a, 0 0 0 1px #0009, 0 4px 4px #0000001a`. It combines an inner top highlight, an inner hairline, a dark outer ring and a soft drop. — [live CSS, linear.app](https://linear.app/)
- **Motion:** `--speed-quickTransition: .1s`, `--speed-regularTransition: .25s`, highlight fade-in 0s and fade-out .15s (hover appears instantly and leaves slowly). 160ms is the most common transition. The full Penner easing set is defined as tokens, for example ease-out-quint `cubic-bezier(.23,1,.32,1)`. — [live CSS, linear.app](https://linear.app/)
- **Redesign blog (stated):**
  - Inter Display for headings and Inter for other text.
  - The theme generator moved from HSL to LCH, cutting 98 variables per theme to 3 ("base color, accent color, and contrast"). The contrast input auto-generates high-contrast themes.
  - The team limited how much chrome blue goes into the neutrals, for "a more neutral and timeless appearance".
  - Goals were to "reduce visual noise, maintain visual alignment, and increase the hierarchy and density of navigation elements", with sidebar labels, icons and buttons aligned on both axes.
  - Apple standards guided spacing so the desktop app feels native. The redesign took about 6 weeks.

  — [Linear, How we redesigned the Linear UI part II](https://linear.app/now/how-we-redesigned-the-linear-ui)
- **Signature:** dark-first, near-black stepped greys with no pure black and no pure white text, plus dense 13–15px Inter with negative tracking and keyboard-first speed. (Signature is my synthesis of the above.)

**Vercel (brand site and the Geist design system)**
- **Type families:** Geist Sans and Geist Mono (Vercel's own open-source family, with Basement Studio). The live site also loads display faces "GeistPixelSquare/Grid/Line/Circle/Triangle". — [live CSS, vercel.com](https://vercel.com/); [Geist intro](https://vercel.com/geist/introduction)
- **Weights:** 550 is the most common weight (99 uses), then 450 (42). Both sit between the standard steps. text-heading-32 and text-heading-40 are overridden to 450, so large headings are set lighter. — [live CSS, vercel.com](https://vercel.com/)
- **Heading scale (size / line-height / tracking), weight semibold:**

  | Class | Size / line-height | Tracking | In em |
  |---|---|---|---|
  | text-heading-14 | 14/20 | -0.28px | -0.02em |
  | text-heading-16 | 16/24 | -0.32px | -0.02em |
  | text-heading-20 | 20/26 | -0.4px | -0.02em |
  | text-heading-24 | 24/32 | -0.96px | -0.04em |
  | text-heading-32 | 32/40 | -1.28px | -0.04em |
  | text-heading-40 | 40/48 | -2.4px | -0.06em |

  Other common values are -3.84px, -2.88px, -3.36px and -4.32px, which match about -0.06em at 56–72px (inferred). — [live CSS, vercel.com](https://vercel.com/)
- **Copy and button scale:** copy-13 13/18, copy-14 14/20, copy-16 16/24. Button text 12/16, 14/20 and 16/20 at medium weight. — [live CSS, vercel.com](https://vercel.com/)
- **Borders as shadows:** `--ds-shadow-border-base: 0 0 0 1px #00000014` (8% black). Dark mode uses `#ffffff25`. The base is combined with elevation (`--ds-shadow-border-medium: border-base, shadow-medium, background-border`), and inset variants use `#00000014` / `#ffffff1a`. — [live CSS, vercel.com](https://vercel.com/)
- **Colours:** greys `#fafafa`, `#eaeaea`, `#1f1f1f`, `#383838`. Blue `#0070f3`/`#2688fe`, plus `#7928ca` purple and `#de2670` pink as gradient accents. Greys are tokenised as `hsla(var(--ds-gray-100-value),1)` steps 100–1000. — [live CSS, vercel.com](https://vercel.com/)
- **Radius and motion:** radius is mostly 6px and 12px, with pills at 2147483647px. Durations are .15s (29) and .2s (28). Easing includes `cubic-bezier(.4,0,.2,1)` and the iOS-sheet-like `cubic-bezier(.32,.72,0,1)`. — [live CSS, vercel.com](https://vercel.com/)
- **Geist foundations (stated):** a "high contrast, accessible color system". Materials are "presets for radii, fills, strokes, and shadows", and the grid is "a core part of the Vercel aesthetic". The visible structural grid lines are the signature. — [Geist intro](https://vercel.com/geist/introduction)

**Stripe (brand site)**
- **Type families:** only two webfonts, `sohne-var` (Söhne variable, Klim, licensed) and `SourceCodePro`. — [live CSS, stripe.com](https://stripe.com/)
- **Light headings:** every heading token at md and above is **weight 300**: `--hds-font-heading-{sm,md,lg,xl,xxl,hero-sm,hero-md,hero-lg}-weight:300`. Only xs and xxs (1rem, 0.875rem) are 400. — [live CSS, stripe.com](https://stripe.com/)
- **Heading sizes (several breakpoint values):** hero-lg 2.5rem, hero-sm 2rem, xxl 2.125, 3 or 3.5rem, xl 1.75, 2.125 or 3rem, lg 1.75 or 2rem, md 1.25–1.625rem. — [live CSS, stripe.com](https://stripe.com/)
- **Features and tracking:** `font-feature-settings:"ss01" on` (5 uses), `"tnum"` and `tabular-nums` for figures. The most common tracking is -0.01em (52 uses); others are .1px, .01em and -.0308em. — [live CSS, stripe.com](https://stripe.com/)
- **Radius tokens:** xs 2px, sm 4px, md 6px (218 uses), lg 16px, xl 32px, round 99999px. — [live CSS, stripe.com](https://stripe.com/)
- **Signature shadow:** `0 27px 40.5px -27px rgba(50,50,93,.25), 0 16.2px 32.4px -16.2px rgba(0,0,0,.1)`. The first layer is blue-tinted (50,50,93 is slate-indigo) and has a large negative spread, so it falls only below the card. Small shadow: `0 2px 5px 0 rgba(0,0,0,.1)`. — [live CSS, stripe.com](https://stripe.com/)
- **Motion:** the dominant easing is `cubic-bezier(.25,1,.5,1)` (60 uses, an ease-out-quart-like curve), mostly at .3s. — [live CSS, stripe.com](https://stripe.com/)
- **Colours:** primary action `#533afd` (with legacy blurple `#635bff`), navy `#061b31` for headings, page tint `#f8fafd`/`#fcfdfe`. Gradient accents are `#ff6118`, `#ffd601`, `#ee30fb`, `#fb76fa` and `#7232f1` (the "wave" mesh gradient). — [live CSS, stripe.com](https://stripe.com/); navy, purple and 4px-button details also agree with the third-party [kombai Stripe breakdown](https://kombai.com/gallery/inspirations/stripe/)
- **Colour system (stated):** Stripe rebuilt its product colour system in CIELAB because HSL lightness "doesn't match perception". The rules: text and icons pass 4.5:1 on white and on the lightest tint of any hue; "any two colors five or more levels apart" pass small-text contrast, and four or more levels pass large text and icons; badge text and background each shift one level for guaranteed contrast. The old palette was "dark and muddy". — [Stripe blog, Designing accessible color systems](https://stripe.com/blog/accessible-color-systems)
- **Product UI typeface:** the dashboard and docs are reported to use system font stacks, not Söhne. — [kombai](https://kombai.com/gallery/inspirations/stripe/) (third-party, unverified)

**Apple (brand site)**
- **Type family:** `SF Pro Text, SF Pro Icons, Helvetica Neue…`. The icons are a font too ("Apple Icons 100–900", one face per weight). — [live CSS, apple.com](https://www.apple.com/)
- **Tracking changes with size (SF optical tracking):**

  | Size | Line-height | Weight | Tracking |
  |---|---|---|---|
  | 17px body | 1.235 | 400 | -0.022em |
  | 19px | 1.21 | 400 | +0.012em |
  | 21px | 1.19 | 400 | +0.011em |
  | 28px | 1.143 | 600 | +0.007em |
  | 48px | 1.083 | 600 | -0.002em |
  | 56px | 1.071 | 600 | -0.005em |

  — [live CSS, apple.com](https://www.apple.com/)
- **Weights and figures:** only 400 and 600 in practice (78 and 56 uses). Uses `"numr"` and `"case"` features. — [live CSS, apple.com](https://www.apple.com/)
- **Motion:** one easing everywhere, `cubic-bezier(.4,0,.6,1)` (122 uses), at **320ms** (63 uses). Secondary timings are 240ms and 160ms. — [live CSS, apple.com](https://www.apple.com/)
- **Colours:** link and action blue `#0071e3`/`#0076df`/`#006edb`, greys `#f5f5f7` (section bg), `#6e6e73` and `#86868b` (secondary text), `#1d1d1f`-range darks (`#18181a`, `#272729`). Pill buttons use radius 980px or 999px. There is almost no box-shadow: one instance, `3px 5px 30px rgba(0,0,0,.22)`. — [live CSS, apple.com](https://www.apple.com/)

**Mercury (fintech)**
- **Type families:** @font-face loads `arcadia`, `arcadiaDisplay` (custom), `tiemposHeadline` and Tiempos Fine (`--font-tiempos-fine`, Klim, licensed) and `IBM Plex Mono`. — [live CSS, mercury.com](https://mercury.com/)
- **Weight tokens:** `--font-weight-300, 360, 400, 420, 480, 500`. Body is at 420 and display at 480. Third-party guides also cite 480 headlines and 420 body. — [live CSS, mercury.com](https://mercury.com/); [blakecrosley Mercury guide](https://blakecrosley.com/guides/design/mercury) (third-party)
- **Positive tracking:** tokens `--tracking-0.5%:.005em`, `1%:.01em`, `1.5%:.015em`, `2%:.02em`, `3%:.03em`. Usage counts are normal 56, 1% 30, 2% 25, 1.5% 25. This is unusual among the sites here. — [live CSS, mercury.com](https://mercury.com/)
- **Text scale:**

  | Token | Size (rem) |
  |---|---|
  | xxs | .625 |
  | xs | .75 |
  | sm | .875 |
  | base | 1 |
  | md | 1.125 |
  | lg | 1.313 |
  | xl | 1.5 |
  | 2xl | 1.75 |
  | 3xl | 2 |
  | 4xl | 2.25 |
  | 5xl | 2.625 |
  | 6xl | 3 |
  | 7xl | 3.438 |

  — [live CSS, mercury.com](https://mercury.com/)
- **Text colour:** `#272735` (427 uses), a blue-violet near-black rather than black. Darkest neutral `#10101a`, neutral-100 `#f4f5f9`, warm beige-100 `#f6f5f2`, beige-200 `#e0ded7`. Semantic roles (`--text-primary: purple-magic-600`, `--text-subdued`, `--text-emphasized`) exist per hue family. — [live CSS, mercury.com](https://mercury.com/)
- **Numbers:** `tabular-nums` / `"tnum"`, plus `"ss01"`. — [live CSS, mercury.com](https://mercury.com/)
- **Radius:** xl .75rem, 2xl 1rem, 4xl 2rem, 5xl 2.5rem. — [live CSS, mercury.com](https://mercury.com/)
- **Motion:** custom curves `cubic-bezier(.16,0,.13,1)` and `cubic-bezier(.2,1,.4,1)` at .3–.5s. Very long ambient loops of 17.4s (50 uses) and 24s, read as slow background or hero animation (inferred). — [live CSS, mercury.com](https://mercury.com/)
- **Conflicting reports:** one third-party design summary names a Tiempos-style serif with GT America. Live CSS confirms Tiempos but not GT America; the sans is Arcadia. — [webdesignhot Mercury](https://www.webdesignhot.com/design.md/mercury/)

**Ramp (fintech)**
- **Type families:** @font-face loads `Lausanne` (Weltkern, licensed), `IBM Plex Sans`, `IBM Plex Mono` and IBM Plex Sans JP. Material Icons appear in the CSS. — [live CSS, ramp.com](https://ramp.com/)
- **Tracking:** -.01em, -.04em, -.03em, -.025em, plus .12em on uppercase labels (inferred). — [live CSS, ramp.com](https://ramp.com/)
- **Colours:** warm off-white `#F4F2F0`/`#f4f2ef` instead of white, `#2A0A3C` deep aubergine, `#0066FF`, success `#18A957`, `#d2cecb` warm grey border. — [live CSS, ramp.com](https://ramp.com/)
- **Motion:** `cubic-bezier(.16,1,.3,1)` (ease-out-expo-like, 29 uses) at .15–.3s. — [live CSS, ramp.com](https://ramp.com/)
- **Shadow:** an 8-layer-style physical shadow, `0px 232px 65px rgba(0,0,0,.006), 0px 35px 59px rgba(0,0,0,.03), 0px 20px 50px rgba(0,0,0,.09), 0px 37px 37px…`. — [live CSS, ramp.com](https://ramp.com/)
- **Caveat:** the weight-600 count (131) is inflated by @font-face descriptors.

**Revolut (fintech)**
- **Type families:** `Aeonik Pro` (CoType, licensed), a separate `Aeonik Pro Capitalised` cut, and `Inter`. — [live CSS, revolut.com](https://www.revolut.com/)
- **Tracking:** always slightly negative, -0.01rem to -0.025rem. — [live CSS, revolut.com](https://www.revolut.com/)
- **Radius and motion:** `--rui-radius-r12: .75rem`, `r16: 1rem`. Transitions at 200ms. — [live CSS, revolut.com](https://www.revolut.com/)
- **Colours:** text `#191c1f`, bg `#f4f4f4`/`#f7f7f7`, blue `#0666eb`, indigo `#4f55f1`, green `#00b88b`/`#13d1a3`, red `#e23b4a`. — [live CSS, revolut.com](https://www.revolut.com/)
- **Brand reading:** a branding analysis attributes Revolut's premium feel to "sleek, minimalist design" and metal card tiers. — [phable](https://phable.io/blog/innovative-financial-services-branding-lessons-from-monzo-and-revolut) (opinion)

**Monzo (fintech)**
- **Type families:** custom `MonzoSansDisplay` and `MonzoSansText` (separate optical cuts), with `Maison Neue Web` and Maison Neue Mono. — [live CSS, monzo.com](https://monzo.com/)
- **Weights:** 600 dominant (250 uses), then 700. — [live CSS, monzo.com](https://monzo.com/)
- **Tracking:** -.02em is most common. — [live CSS, monzo.com](https://monzo.com/)
- **Figures:** `"tnum"` (12 uses). — [live CSS, monzo.com](https://monzo.com/)
- **Radius tokens (large):** x-small 8px, small 12px, medium 16px, large 24/32px, x-large 32/48/64px. — [live CSS, monzo.com](https://monzo.com/)
- **Elevation:** level1 `0px 2px 8px rgba(0,0,0,.16)`, level3 `0px 8px 32px rgba(0,0,0,.16)`. — [live CSS, monzo.com](https://monzo.com/)
- **Colours:** navy `#091723` (355 uses), mint-white `#f2f8f3`, blue `#218fb7`, hot coral `#ff4f40`, lime `#d9ff6f`. — [live CSS, monzo.com](https://monzo.com/)
- **Motion:** easing `cubic-bezier(.33,1,.68,1)` (ease-out-cubic) and `(0,0,.12,1)`, mostly .3s. — [live CSS, monzo.com](https://monzo.com/)
- **Trust and voice:** commentary cites real-time notifications, instant balance updates and plain-English, human copy as trust builders. — [Kota](https://kota.co.uk/blog/how-fintech-brands-like-revolut-and-monzo-use-ux-to-build-trust) (agency opinion)

**Copilot Money (fintech)**
- **Site type families:** the site is built in Framer and loads `Jokker` (Regular/Medium/Semibold/Bold/Heavy), `Matter Variable Thin`, `Inter` and `Fragment Mono`. — [live CSS, copilot.money](https://www.copilot.money/)
- **Weights and tracking:** 100 and 670 appear often (thin display numerals and heavy labels, inferred). Tracking +0.04em is common, likely on caps labels (inferred). — [live CSS, copilot.money](https://www.copilot.money/)
- **Colours:** deep navy canvas `#010d1e`/`#000814`/`#020c1b`, slate blues `#5979a6`/`#7f8ba4`, green `#00cc4b`, yellow `#fece4c`. — [live CSS, copilot.money](https://www.copilot.money/)
- **Glass shadows:** `inset 0px 24px 64px -12px rgba(255,255,255,.16), inset 0px -24px 40px -12px rgba(0,0,0,.16)…`. — [live CSS, copilot.money](https://www.copilot.money/)
- **Recognition and build (stated):** Apple featured Copilot for its Swift Charts work. The team "mold[s]" UIKit components and "tweak[s] it a lot". Data is stored locally "so the app is really responsive". The team calls itself "very picky when it comes to the design". The Cash Flow feature (2024) has "a lot of interactive charts". — [Apple Developer, Copilot Money](https://developer.apple.com/articles/copilot-money)
- **Awards:** ADA finalist 2024 and App Store Editor's Choice; the same guide describes the "deep navy canvases and vibrant Swift Charts". — [blakecrosley Copilot guide](https://blakecrosley.com/guides/design/copilot-money) (third-party)

**Raycast (tool)**
- **Type families:** `Inter`, `GeistMono`, `jetBrainsMono`, `Instrument Serif` (editorial accent) and `VT323` (pixel font for playful moments). — [live CSS, raycast.com](https://raycast.com/)
- **Weights:** 500 is the default (144 uses). — [live CSS, raycast.com](https://raycast.com/)
- **Positive tracking on dark:** `.2px` (79 uses), `.3px`, `.1px`. Inter features `"ss08" on, "ss02" on, "liga" off` and `"ss09"`. — [live CSS, raycast.com](https://raycast.com/)
- **Radius:** `--rounding-md:12px`, `--rounding-lg:16px`, plus 4/6/8/10/18px. — [live CSS, raycast.com](https://raycast.com/)
- **Signature shadows:** an inner top highlight, `inset 0 1px #ffffff1a` (17 uses). Glow: `0 1px 40px #9aaaff0d, 0 0 16px -7px #9aaaff0d, 0 2px 40px 10px #9aaaff0d, inset 0 1px 1px #ffffff1a`. — [live CSS, raycast.com](https://raycast.com/)
- **Colours:** red `#ff6363` brand, near-black backgrounds `#07080a`/`#0c0d0f`/`#111214`, text grey `#D8D8D8`. — [live CSS, raycast.com](https://raycast.com/)
- **Motion:** `cubic-bezier(.23,1,.32,1)` (ease-out-quint) and `(.16,1,.3,1)`, at .3s and .2s. — [live CSS, raycast.com](https://raycast.com/)

**Things 3 (tool, Cultured Code)**
- **Site type:** culturedcode.com loads no webfonts. It uses `ui-sans-serif, -apple-system, BlinkMacSystemFont…` (SF on Apple devices), weights 700/600/500 and a custom 440, with `"tnum"`. — [live CSS, culturedcode.com](https://culturedcode.com/)
- **Shadow stack:** `0 2px 4px rgba(0,0,0,.1), 0 4px 16px rgba(0,0,0,.1), 0 8px 32px rgba(0,0,0,.1)` (each layer doubles). Hairline borders are inset rings: `0 0 0 1px rgba(0,20,49,.18) inset` (blue-tinted), and `rgba(191,218,255,.08)` in dark. Focus ring `0 0 0 2px rgba(37,118,235,.75)`. — [live CSS, culturedcode.com](https://culturedcode.com/)
- **Radius and motion:** radii in em (.25em, .4em, .5em, 1em) or 6px. Transitions .1–.2s. — [live CSS, culturedcode.com](https://culturedcode.com/)
- **Colours:** blue `#2576eb`, greys `#f2f5f7`/`#eceef0`, text `#212224`/`#303336`, pale-yellow highlight `#fcf9cf`. — [live CSS, culturedcode.com](https://culturedcode.com/)
- **Awards:** two Apple Design Awards. — [App Store listing](https://apps.apple.com/de/app/things-3/id904244226)
- **Third-party reading:** one analysis says the completion animation plus sound "make finishing tasks feel good", and that about 95% of the UI is neutral, with yellow, red and indigo used only where they carry information. — [blakecrosley design study: Things](https://blakecrosley.com/blog/design-study-things) (third-party)

**Notion (tool)**
- **Type families:** `NotionInter` (custom Inter build), `Lyon Text` (Commercial Type serif, licensed), `iA Writer Mono` and `Permanent Marker` (hand-drawn accent). — [live CSS, notion.com](https://www.notion.com/)
- **Figures and tracking:** sans feature settings `"lnum" 1, "locl" 0`. Heading tracking -.125rem, -.09375rem and -.0078125rem. — [live CSS, notion.com](https://www.notion.com/)
- **Radius tokens:** 300 = .3125rem (5px), 500 = .5rem, 700 = .75rem. — [live CSS, notion.com](https://www.notion.com/)
- **Warm greys:** `#f9f9f8`, `#f6f5f4`, `#dfdcd9`, `#a39e98`, `#78736f`, `#615d59`, `#494744`, all with a slight yellow-brown cast. Accents are `#f64932` red, `#ffb110` yellow, `#097fe8` blue and `#1aae39` green. — [live CSS, notion.com](https://www.notion.com/)

**Arc (The Browser Company, brand site)**
- **Type families:** `Marlin Soft SQ` (rounded grotesque, most used), `ABC Favorit Mono`, `ABC Oracle`, `Exposure VAR`, `Söhne Breit`, `EB Garamond`, `Inter`, `Space Mono`. — [live CSS, arc.net](https://arc.net/)
- **Tracking:** tight display, -0.05em and -0.04em. — [live CSS, arc.net](https://arc.net/)
- **Colours:** electric blue `#3139FB`, cream `#FFFCEA`/`#FFFADD` instead of white, deep indigo `#2702c2`/`#000354`, coral `#FB3A4D`. — [live CSS, arc.net](https://arc.net/)
- **Radius:** 16px, 22px, pills. — [live CSS, arc.net](https://arc.net/)

**Teenage Engineering (brand site)**
- **Type:** the only family declared in fetched CSS is `UniversNextPro-Thin` at weight 200. — [live CSS, teenage.engineering](https://teenage.engineering/)
- **Fluid geometry:** radii and shadows are proportional to viewport width, for example `border-radius: calc(.0153061 * var(--client-width))` and `box-shadow: #00000080 0 calc(.00408163*var(--client-width)) calc(.0163265*var(--client-width))`. The whole layout scales like an image (inferred). — [live CSS, teenage.engineering](https://teenage.engineering/)
- **Colours:** `#E5E5E5`, `#f1f2f2`, black, signal red `#ed2024`. — [live CSS, teenage.engineering](https://teenage.engineering/)

**Aesop (brand site)**
- **Type:** Fonts In Use lists the website as Suisse Int'l plus Zapf Humanist 601 (Optima-like), with a c. 2018 identity, website and packaging by Work & Co. — [Fonts In Use, Aesop tag](https://fontsinuse.com/tags/11303/aesop)
- **Usage split:** Font Alternatives says Suisse Int'l carries nav, headlines and copy, while the humanist serif appears mainly in the wordmark. — [fontalternatives](https://fontalternatives.com/inspiration/aesop-suisse/)
- **Conflict:** aesop-planning.eu claims Cooper Hewitt and Open Sans, which looks unreliable or about a different entity. — [aesop-planning.eu](https://aesop-planning.eu/branding)

**Apple Card / Wallet (fintech)**
- **Physical card:** titanium with no number, expiry, CVV or signature. Only the name and Apple logo are laser-etched, under a multi-layer white coating. Card details live in Wallet. — [Dezeen](https://www.dezeen.com/2019/08/23/apple-card-care-design-news/); [One Mile at a Time](https://onemileatatime.com/titanium-apple-card/)

### Inferences
- **Size-aware tracking:** "Negative tracking on headings" is too crude a rule. Linear, Vercel and Apple all vary tracking by size. Body sizes sit near 0 to -0.022em; headings sit at -0.02em (Linear) to -0.06em (Vercel 40px+). Apple turns positive (+0.007 to +0.012em) at 19–28px because SF Pro Display has its own tracking table.
- **Lighter display text:** Stripe sets every heading at 300 and Vercel overrides large headings to 450. Big type that is lighter, not bolder, reads as expensive.
- **Positive tracking:** Mercury (+1–3%) and Raycast (+.2px on dark) are the counter-example. Positive tracking reads as airy and calm on light-weight custom type, and helps legibility of light text on dark.

### Gaps
- No app-internal (logged-in) values for Mercury, Ramp, Revolut, Monzo, Copilot, Things, Wallet or Notion. Grid and spacing scales (for example a 4px vs 8px base) could not be reliably extracted from minified utility CSS.
- Aesop's live CSS was blocked, and Teenage Engineering loads fonts through JS, so their tokens are incomplete.
- Mercury's Arcadia origin (custom foundry or designer) is not confirmed by Mercury.
- I found no official teardown for Revolut's or Monzo's app type scale.

---

## 2. What do designers point to when explaining "premium"? What recurs and what is specific?

### Takeaway
The details named most often in team blogs and critiques are perceptually uniform colour systems (LCH or Lab), restraint (neutral surfaces with colour used only for meaning), alignment and density work, and responsive, interruptible motion. In the measured CSS, the high-impact recurring details are:
1. A licensed or custom typeface, or a tuned Inter.
2. Tuned tracking and non-default weights.
3. Off-black text and off-white or tinted backgrounds.
4. Borders as 1px low-alpha rings.
5. Multi-layer low-opacity shadows.
6. A single ease-out curve at roughly 150–320ms.

### Cited Findings
- **Linear:** moved from HSL to LCH so surfaces at the same lightness look equally light, and reduced the chrome hue for a "neutral and timeless" look. Alignment and density were explicit goals. — [Linear blog](https://linear.app/now/how-we-redesigned-the-linear-ui)
- **Stripe:** moved to CIELAB for "predictable accessibility, clear and vibrant hues, and consistent visual weight across hues". — [Stripe blog](https://stripe.com/blog/accessible-color-systems)
- **Rauno Freiberg on interaction details:**
  - Interruptibility: animations you must wait out are the anti-pattern.
  - Momentum is preserved through gestures.
  - Lightweight actions trigger during a gesture; destructive ones trigger on gesture end.
  - Spatial consistency: things animate from where they live.
  - Frequency vs novelty: frequent actions such as command menus may need no animation, because a menu seen "for the hundredth time" becomes cognitive burden.

  — [Rauno, Invisible Details of Interaction Design](https://rauno.me/craft/interaction-design)
- **Emil Kowalski's guidance as packaged by others:**
  - UI motion should stay under 300ms; drawers can go to about 500ms.
  - Ease-out for entrances; never ease-in for UI.
  - Button press feedback at 100–160ms, dropdowns at 150–250ms.
  - Animate only transform and opacity; press scale(0.97).

  — [skills.sh emilkowal-animations](https://skills.sh/mrmps/smry/emilkowal-animations) (secondary; verify against animations.dev)
- **Measured motion matches that guidance:**

  | Site | Main easing | Duration |
  |---|---|---|
  | Apple | `(.4,0,.6,1)` | 320ms |
  | Stripe | `(.25,1,.5,1)` | .3s |
  | Linear | — | .1s / .16s / .25s |
  | Vercel | — | .15s / .2s |
  | Monzo | `(.33,1,.68,1)` | .3s |
  | Ramp | `(.16,1,.3,1)` | — |
  | Raycast | `(.23,1,.32,1)` | — |

  The ease-out curves are strong (expo, quart or quint shaped). — [live CSS of each site, linked in section 1]
- **Borders drawn as low-alpha rings or shadows:**
  - Vercel: `0 0 0 1px #00000014`.
  - Linear: `#ffffff14` borders and a `0 0 0 1px #0009` outer ring.
  - Things: `0 0 0 1px rgba(0,20,49,.18) inset`.
  - Raycast and Linear: an `inset 0 1px #ffffff0a–1a` top highlight on dark surfaces.

  — [live CSS, vercel.com](https://vercel.com/), [linear.app](https://linear.app/), [culturedcode.com](https://culturedcode.com/), [raycast.com](https://raycast.com/)
- **Layered shadows at low opacity:**
  - Things: 3 layers at .1 with doubling offsets.
  - Ramp: 4+ layers from .006 to .09.
  - Stripe: a tinted rgba(50,50,93,.25) with negative spread.
  - Monzo: two elevations, both at .16.

  — [live CSS, culturedcode.com](https://culturedcode.com/), [ramp.com](https://ramp.com/), [stripe.com](https://stripe.com/), [monzo.com](https://monzo.com/)
- **Off-black text:**

  | Site | Text colour |
  |---|---|
  | Mercury | `#272735` |
  | Linear (light) | `#282a30` |
  | Stripe | navy `#061b31` |
  | Revolut | `#191c1f` |
  | Monzo | `#091723` |
  | Things | `#212224` |

- **Off-white or tinted backgrounds:**

  | Site | Background colour |
  |---|---|
  | Ramp | `#F4F2F0` |
  | Notion | `#f9f9f8` |
  | Arc | `#FFFCEA` |
  | Apple | `#f5f5f7` |
  | Stripe | `#f8fafd` |
  | Mercury | `#f6f5f2` beige |

  — [live CSS for each site]
- **Licensed or custom type, with OpenType stylistic sets:**

  | Site | Typeface | Feature settings |
  |---|---|---|
  | Stripe | Söhne | ss01 |
  | Linear | Inter | cv01, ss03 |
  | Raycast | Inter | ss02, ss08 |
  | Mercury | Arcadia | ss01 |
  | Ramp | Lausanne | ss01 |

  — [live CSS]
- **Specific to one product:**
  - Stripe's 300-weight headings and mesh gradient.
  - Vercel's visible grid and pixel display fonts.
  - Mercury's positive tracking and serif-plus-grotesque pairing.
  - Linear's stepped near-black levels.
  - Teenage Engineering's viewport-proportional geometry.
  - Apple's single easing at 320ms, with icons served as a font.
  - Monzo's very large radii (up to 64px) and coral or lime accents.
  - Things' completion animation and sound.

  — [sources above]

### Inferences
- **Biggest contributors** (visible on first glance, my ranking):
  1. Typeface quality plus tuned tracking and weight.
  2. Restrained palette: neutral surfaces, off-black and off-white, one accent.
  3. Generous or deliberately dense spacing applied consistently.
  4. Hairline borders instead of heavy outlines.
- **Small polish** (felt, not seen):
  - tabular and slashed-zero figures
  - inner top highlights
  - tinted shadows
  - instant hover-in with a slow hover-out (Linear's 0s / .15s)
  - stylistic sets
  - optical sizing
- **One curve, few durations:** every site measured converges on one dominant easing curve and two or three durations. Consistency of motion is itself a signal.

### Gaps
- I did not fetch Anthony Hobday's or Jordan Singer's critiques, or Built for Mars chapters, because of the tool-call budget. Their specific named criteria are not captured here.
- Emil Kowalski's numbers come from secondary skill packages, not his own site.

---

## 3. How do premium money apps build trust and calm (numbers, tables, charts, empty states)?

### Takeaway
On the evidence available, money apps build calm with:
- Tabular, lining figures in a quiet weight (every fintech site measured enables `tnum`).
- A desaturated or tinted neutral base with semantic colour held back for meaning.
- Serif or light-weight display type for an editorial, non-alarmist tone (Mercury, Copilot).
- Slow ambient motion on marketing pages paired with quick UI transitions.
- Plain-language copy and instant feedback such as real-time balances and notifications.
- In Apple Card's case, removing numbers entirely from the physical object.

### Cited Findings
- **Tabular figures on every fintech site measured:**

  | Site | Setting |
  |---|---|
  | Mercury | `tabular-nums`, `"tnum"` |
  | Monzo | `"tnum"` ×12 |
  | Stripe | `"tnum"`, `tabular-nums` |
  | Copilot | `tabular-nums` |
  | Ramp | Tailwind numeric utilities |

  Linear adds `slashed-zero` and Notion `"lnum"`. — [live CSS, mercury.com](https://mercury.com/), [monzo.com](https://monzo.com/), [stripe.com](https://stripe.com/), [linear.app](https://linear.app/), [notion.com](https://www.notion.com/)
- **Apple figure features:** Apple uses `"numr"`, which suggests typographic fractions or superscripts in prices (inferred). — [live CSS, apple.com](https://www.apple.com/)
- **Mercury's editorial pairing:** Tiempos serif display, light 300–360 weights, positive tracking, a blue-violet near-black and warm beige neutrals. It also uses a mono (IBM Plex Mono), probably for figures or account details (inferred). — [live CSS, mercury.com](https://mercury.com/)
- **Mercury's slow motion:** 17.4s and 24s ambient loops and custom slow-in curves. — [live CSS, mercury.com](https://mercury.com/)
- **Copilot:** native Swift Charts, local data for responsiveness, and a deep navy canvas. — [Apple Developer](https://developer.apple.com/articles/copilot-money); [live CSS, copilot.money](https://www.copilot.money/)
- **Calmer palettes (general claim):** a roundup argues that harsh reds and alarms make people avoid their finances and that calmer palettes help. — [getfinny blog](https://getfinny.app/blog/aesthetic-budget-apps-2026) (general, low authority)
- **Monzo's transparency signals:** real-time spending notifications, instant balance updates and plain-English copy. — [Kota](https://kota.co.uk/blog/how-fintech-brands-like-revolut-and-monzo-use-ux-to-build-trust)
- **Monzo's regulatory signal:** the FSCS-protected banking licence is a major trust signal but sits low on Monzo's page. — [Landing Doctor teardown](https://landingdoctors.com/teardowns/monzo-com)
- **Built for Mars banking study:** the author opened 12 real bank accounts to test whether challenger banks are better. Incumbents "didn't realize what made Monzo better, just that it felt better." — [banq interview with Peter Ramsey](https://blog.banq.ai/challengers-built-for-mars-interview-peter-ramsey)
- **Stripe's colour contrast rule:** a "five levels apart" contrast guarantee means status badges and text are always legible, so no colour pairs fail on data-dense screens. — [Stripe blog](https://stripe.com/blog/accessible-color-systems)
- **Apple Card:** the physical card has no number, expiry or CVV, so sensitive details live behind device authentication in Wallet. — [Dezeen](https://www.dezeen.com/2019/08/23/apple-card-care-design-news/)
- **Things colour restraint:** about 95% neutral UI, with colour only where it carries meaning (third-party). — [blakecrosley Things study](https://blakecrosley.com/blog/design-study-things)

### Inferences
- **Copyable recipe for money UIs:**
  - `font-variant-numeric: tabular-nums lining-nums` (plus `slashed-zero` for IDs and account numbers).
  - Mono or tnum for amounts in tables.
  - Amounts at a regular or medium weight, not bold.
  - Text in a tinted near-black (`#272735`, `#191c1f`) on an off-white.
  - Red and green reserved for state, desaturated rather than pure.
  - Positive or neutral tracking at small sizes.
- **Calm is partly motion:** quick (≤200ms), ease-out UI responses signal competence, while slow ambient background loops (Mercury) signal stability.

### Gaps
- No primary sources found on empty states, chart styling (gridline weights, colours) or negative-number formatting in Mercury, Ramp, Revolut or Monzo apps. Only Copilot's use of Swift Charts is documented.
- Built for Mars chapter specifics were not retrieved.

---

## 4. What do they deliberately NOT do?

### Takeaway
Across the measured sites, these products avoid:
- pure black text and pure white dark-mode text
- thick or high-contrast borders
- single heavy drop shadows
- many easing curves
- bold display headings (Stripe, Vercel, Mercury)
- saturated colour on neutral chrome
- slow UI animations
- animating frequent actions

### Cited Findings
- **Linear:** deliberately reduced chrome blue in neutrals and cut theme variables from 98 to 3. Navigation changes were deferred to avoid disrupting users. — [Linear blog](https://linear.app/now/how-we-redesigned-the-linear-ui)
- **Animation on frequent actions:** avoid it ("hundredth time" burden), and avoid non-interruptible animations. — [Rauno](https://rauno.me/craft/interaction-design)
- **Ease-in and slow UI motion:** avoid ease-in and motion over 300ms (secondary). — [skills.sh emilkowal-animations](https://skills.sh/mrmps/smry/emilkowal-animations)
- **Shadows:** Apple's homepage CSS has a single box-shadow declaration. Depth comes from imagery and colour blocks (`#f5f5f7` sections), not shadows. — [live CSS, apple.com](https://www.apple.com/)
- **Webfonts:** Stripe loads only two (Söhne and Source Code Pro), and Things' site loads none (system UI). — [live CSS, stripe.com](https://stripe.com/), [culturedcode.com](https://culturedcode.com/)
- **Muddy colours:** Stripe's old palette passed contrast but looked "dark and muddy", so they rejected HSL-derived palettes. — [Stripe blog](https://stripe.com/blog/accessible-color-systems)
- **Apple Card:** removes all printed numbers. — [Dezeen](https://www.dezeen.com/2019/08/23/apple-card-care-design-news/)

### Inferences
- **Few font weights:** none of the measured sites uses more than about 4–6 weights, and Apple effectively uses 2 (400 and 600).
- **No decorative gradients on UI chrome:** gradients appear as brand moments (Stripe mesh, Vercel accents), not on buttons or cards.

### Gaps
- No primary statement from Mercury, Ramp, Revolut or Monzo on what they avoid.
- Icon style specifics are not covered. Only Apple serving icons as a font and Ramp's Material Icons in CSS were observed; I found no stroke-weight data for Linear's or Raycast's icons.
