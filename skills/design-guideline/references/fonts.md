# Fonts for client work (D104)

Source: `reports/What makes sites look premium.md`, "Changes to the pipeline" 4 (T1-T7) and
the "Typography" section; `research_notes/What makes sites look premium/typography.md`.
Labels: **[M]** measured or foundry terms, **[C]** consensus, **[P]** practitioner opinion or
inference.

## Default pattern [C: Typewolf]

A neutral grotesk for UI and text, plus an optional characterful display or serif face for
one brand voice, plus an optional mono for IDs or code. Not two sans faces. Premium sites
mostly use commercial neo-grotesques and editorial serifs; the free pool below is the
zero-cost route to the same pattern.

## Licence rule (D104)

**Bundling terms are checked per font, not per foundry or per site.** Offline apps store the
font files in the repo, which is redistribution; web embedding and app embedding can need
different terms. The research did not verify the ITF Free Font License's redistribution terms
for bundling [P]. Before shipping any face:

1. Read the licence of that specific font (the file in its download, or its page).
2. Confirm it allows commercial use, self-hosting and, for an app, bundling in the repo.
3. Record the face, licence name, URL and date checked **on the brand sheet**
   (`docs/design/design-system.md`). A face with no licence recorded fails review.

If the terms are unclear, treat the face as not cleared and pick another or recommend a paid
licence.

## Free commercial-licence faces that can read premium

In order of preference [C: Made Good Designs; P for the picks]:

| Pool | Licence | Faces and notes | Source |
|---|---|---|---|
| Fontshare (Indian Type Foundry), less-common faces | ITF Free Font License, free for personal and commercial use (100+ families). Check bundling per font | **General Sans, Switzer, Supreme** as a neutral grotesk. Check the current catalogue for fit | madegooddesigns.com/fontshare; typography notes |
| Velvetyne, Collletttivo | Open source: use, modify, redistribute freely (Velvetyne); some Collletttivo faces open source. Check each | Display voice, characterful | Dribbble resources; Creative Lives in Progress |
| Google Fonts and other SIL OFL faces | OFL, chosen for fit not popularity | A less-used grotesk or an open-licence serif for editorial accents. No sourced list of high-quality under-used Google Fonts exists; choose per brief | typography notes (gap) |
| Inter, set deliberately | SIL OFL 1.1 | Acceptable when chosen: display optical size (`opsz`, Inter 4), tracking to Inter's own curve, `cv11` (single-storey a), `ss01` (open digits), `tnum`, `case`, display weights below 600. Linear does this. Needs a recorded reason on the sheet [C: rsms.me, Linear] | rsms.me/inter |
| Mono (optional) | Open licences | JetBrains Mono, IBM Plex Mono, Space Mono, Geist Mono are free but common; use mono for code, IDs or one deliberate voice, not for prose or a whole money readout | typography notes |

The pairing pattern (characterful serif + neutral grotesk + optional mono) matters more than
any single name [P, inferred from Typewolf Site of the Day pairings].

## Overused or next-default: avoid as the main voice

Needs a recorded reason on the brand sheet that names the brief if used:

- **Inter set at defaults**, Roboto, Arial, system UI fonts [M: Krebs audit of 1,590 sites flags Inter everywhere].
- **Space Grotesk, Instrument Serif (especially as a one-word italic accent), Geist** [M: Krebs; Anthropic found banning Inter only moved Claude to Space Grotesk].
- **Clash Display and Satoshi**: the most common Fontshare picks, now so common that being popular works against them [C: Made Good Designs; P].
- **IBM Plex Sans + Plex Mono**: first on a vendor's published de-slop pairing list, so a rising default [P, inference; Mowgli]. The Pocket mockup used it.
- Poppins and Montserrat: probably overused, a common view the research could not source [P].
- Any pairing a vendor publishes as de-slop advice. Any fixed safe list becomes the next default, so **choose per client from the broad pool and keep a per-client log of chosen faces; never give two consecutive clients in one category the same pairing** [C: Anthropic; P].

## Never on client sites

**Pangram Pangram free downloads** (Neue Montreal, Editorial New and the others) are personal
use only. Web and app embedding needs a paid licence (a third-party summary puts desktop
licences from $30 per family) [M: foundry terms, pangrampangram.com/pages/about; LicenseOrg].
Never ship them, or any other "free for personal use" face, without a bought web licence.

## When to recommend a paid licence

Recommend it when type is the brand's main carrier [M: Stanford, finance look came up in
54.6% of credibility comments; P]:

- a consumer-facing brand or marketing site
- money, luxury or editorial categories where design drives credibility
- a client planning to grow the brand

Shortlist faces seen on premium products and give the client the foundry link. The research
did not verify webfont prices, so quote from the foundry at the time:

| Role | Face (foundry) | Seen at |
|---|---|---|
| Grotesk | Söhne (Klim) | Stripe |
| Grotesk | GT America (Grilli Type) | Typewolf most-used |
| Grotesk | Graphik (Commercial Type) | Typewolf most-used |
| Grotesk | Lausanne (Weltkern) | Ramp |
| Grotesk | Aeonik (CoType) | Revolut |
| Grotesk | Suisse Int'l (Swiss Typefaces) | Aesop |
| Serif | Tiempos (Klim) | Mercury |
| Serif | Lyon Text (Commercial Type) | Notion |

Do not borrow a reference's licensed font from its CSS; borrow the setting (tracking,
weight, line height), not the file.

## Setting rules that apply to any face

See `premium-spec.md` for tracking by size, weights, line height, optical size, figures and
text wrap. Fallback metrics: `size-adjust` plus ascent/descent overrides on the fallback
`@font-face`; at most 2 webfont families plus an optional mono [C: web.dev, Vercel].
