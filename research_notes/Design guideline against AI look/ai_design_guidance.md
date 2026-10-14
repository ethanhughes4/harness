# Steering AI tools toward distinctive UI, and judging UI quality automatically (as of Oct 2026)

Method note: about 20 searches and fetches on 2026-10-14. Where a page could not be quoted word for word, the text is marked as a paraphrase. Star counts and leaderboard figures change often. They are given as the pages showed them on that date.

## 1. What vendors publish about avoiding generic AI aesthetics (Anthropic, v0, Lovable, Bolt, Stitch, Figma Make)

### Takeaway
The vendors agree on the cause and on the fixes. Models drift to a "safe" average look, so every vendor tells you to fix a direction before building, give the model persistent design rules (skill, DESIGN.md, Guidelines.md, project knowledge), name specific defaults to avoid, and put hard limits on palette and fonts. None of them publishes measured evidence. All of their evidence is screenshots.

### Cited Findings
**Anthropic (frontend-design skill and blog)**
- Cause stated: "Safe design choices–those that work universally and offend no one–dominate web training data." Unguided output "creates what users call the 'AI slop' aesthetic." — [Claude blog: Improving frontend design through skills](https://www.claude.com/blog/improving-frontend-design-through-skills)
- The original ~400-token `<frontend_aesthetics>` prompt covers typography, colour/theme, motion and backgrounds. Quotes: "Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics"; "Dominant colors with sharp accents outperform timid, evenly-distributed palettes." It also explicitly warns against converging on the next default, naming Space Grotesk. — [same](https://www.claude.com/blog/improving-frontend-design-through-skills)
- Observation (not measured): the typography instruction alone "seems to encourage the model to improve other aspects of the design as well." All evidence is side-by-side screenshots of a SaaS landing page, a blog and a dashboard. No metrics are reported. — [same](https://www.claude.com/blog/improving-frontend-design-through-skills)
- The current SKILL.md on main has been revised and now targets the *newer* clichés. The following is a paraphrase from a fetch summary, so check the raw file before quoting it. It tells the model to make choices specific to the brief and taken from the subject's industry and vernacular. It says "Spend your boldness in one place." It asks for one font family, or two clearly distinct ones, a deliberate type scale and lines under ~80 characters. It asks for a base palette of 4–6 named hex values. Borders, dividers and labels must carry information. Motion is limited to about one orchestrated moment. The listed tells are: cream-and-terracotta palettes, near-black with one neon or acid-green accent, hairline broadsheet layouts, uniform rounded SaaS cards, all-caps eyebrows, middle-dot meta strings, arrows on links, an accent colour on one headline word, and fade-and-slide on every section. — [anthropics/skills frontend-design SKILL.md](https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md)

**Vercel v0.** The source is a *leaked* system prompt, not official docs. No official v0 design rules were found.
- "ALWAYS use exactly 3-5 colors total." / "NEVER exceed 5 total colors without explicit user permission" / "NEVER use purple or violet prominently, unless explicitly asked for" — [leaked v0 prompt (x1xhlol repo)](https://raw.githubusercontent.com/x1xhlol/system-prompts-and-models-of-ai-tools/main/v0%20Prompts%20and%20Tools/Prompt.txt)
- "Avoid gradients entirely unless explicitly asked for. Use solid colors." / "ALWAYS limit to maximum 2 font families total." / "NEVER use decorative fonts for body text or fonts smaller than 14px" — [same](https://raw.githubusercontent.com/x1xhlol/system-prompts-and-models-of-ai-tools/main/v0%20Prompts%20and%20Tools/Prompt.txt)
- "NEVER generate abstract shapes like gradient circles, blurry squares, or decorative blobs as filler elements" / "NEVER use emojis as icons" / "Ship something interesting rather than boring, but never ugly." / "Utilize the GenerateDesignInspiration tool before any design work." — [same](https://raw.githubusercontent.com/x1xhlol/system-prompts-and-models-of-ai-tools/main/v0%20Prompts%20and%20Tools/Prompt.txt)
- A third-party essay (opinion) says the v0 team relies on design systems and registries (shadcn tokens) as the fix. It also reports that models given explicit style rules "still get more purple." — [UX Collective: Purple](https://uxdesign.cc/purple-6a6d1786f6c1)

**Lovable**
- Visual language is "a foundation, not a polish layer." Style buzzwords "aren't fluff: they meaningfully influence typography, spacing, shadow, border radius, and color palette." Use style terms early and in every section "for cohesive designs that avoid the default-UI look." Keep style keywords in project knowledge. "Pointing beats re-prompting" for visual edits. — [Lovable docs: Prompting](https://docs.lovable.dev/prompting/prompting-one)

**Bolt** (paraphrased from docs and blog)
- Design-system sources that contain real component code work best: a GitHub repo, an npm package or llms.txt. Generate a base section first, then ask new sections to reuse its style. Style in small, focused passes. — [Bolt design-system best practices](https://support.bolt.new/building/design-system/best-practices); [Bolt prompting tips](https://bolt.new/blog/prompting-tips-for-bolt)

**Figma Make**
- Guidelines.md is the entry point that "Figma Make always looks at first," with subfiles for tokens and components. Short, direct rules work better: "Do not use small text for anything except captions" beats "Use small text sparingly." — [Figma dev docs: write design system guidelines](https://developers.figma.com/docs/code/write-design-system-guidelines/); [Figma help: Before you start](https://help.figma.com/hc/en-us/articles/33665861260823)

**Google Stitch** (secondary sources only)
- "Vibe design" launched March 2026. DESIGN.md is an agent-readable markdown file of design rules (colours, typography, spacing, components). Google published an open draft spec on 21 April 2026. Third-party guides say to put the palette and spacing constraints in the prompt and to treat exports as drafts. — [Nervegna: Inside Google Stitch's March 2026 update](https://nervegna.substack.com/p/vibe-design-is-real-inside-google); [itechguides](https://www.itechguides.com/google-adds-vibe-design-to-stitch-what-the-ai-ui-tool-can-do/)

### Inferences
- The recurring vendor rules are: a palette of 3–6 colours, at most 2 font families, no default purple, no decorative gradients or blobs, no emoji icons, a design-inspiration or direction step before building, and persistent rule files.
- Ban lists go stale. Anthropic's own skill moved from banning Inter and purple to banning cream-and-terracotta, neon-on-black and editorial-hairline layouts, which are the clichés that the first round of anti-slop prompts produced. A checker therefore needs a ban list that can be updated, not a fixed one.

### Gaps
- No official v0 design rules were found, only a leaked prompt of uncertain date. Google's own DESIGN.md spec and Stitch guidance were not fetched directly. No vendor publishes quantitative evidence.

## 2. Community anti-slop and taste skills: recurring rules and evidence

### Takeaway
The popular skills (Impeccable, Taste Skill, ui-ux-pro-max and others) repeat the vendor bans and add commands for review steps and self-critique in a browser. They are very popular, but none publishes a controlled with-vs-without evaluation.

### Cited Findings
- Impeccable (pbakaus) rules: "Don't use overused fonts (Arial, Inter, system defaults)"; "Don't use gray text on colored backgrounds"; "Don't use pure black/gray (always tint)"; "Don't wrap everything in cards or nest cards inside cards"; "Don't use bounce/elastic easing (feels dated)." — [github.com/pbakaus/impeccable](https://github.com/pbakaus/impeccable)
- Impeccable has 24 commands, including `critique` (UX review), `audit` (accessibility, performance, responsiveness), `polish`, `bolder`/`quieter`/`distill`, and `init`, which writes PRODUCT.md and DESIGN.md. It has "59 deterministic detector rules plus LLM-only critique checks". The CLI runs the rules "with no LLM and no API key" and detects side-tab borders, purple gradients, bounce easing, dark glows, cramped padding and small touch targets. It warns that a clean run "is evidence, not proof." The repo showed ~81k stars. The only evidence offered is a single before/after case study. — [same](https://github.com/pbakaus/impeccable)
- Impeccable extends Anthropic's skill with 7 reference files: typography, colour/contrast (OKLCH), spatial design, motion, interaction, responsive design and UX writing (secondary). — [emelia.io guide](https://emelia.io/hub/impeccable-ai-design-skill)
- Taste Skill (Leonxlnx) v2 picks a direction by dealing 3 of 20 researched directions, drawn from a study of 247 curated sites. It uses real, credited CC photos. It checks the page "in a real browser at three widths and fails it on slop." The agent "looks at its own screenshots and fixes the top three problems, up to three rounds." Earlier versions used 1–10 dials (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY). A build costs about 30–45 minutes and a few hundred thousand tokens. The repo showed ~96k stars. No controlled comparison is published. — [github.com/Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)
- The closest thing to a comparison is HappyCapy Skill Arena. It ran 6 frontend skills on 3 tasks with the same model, and two judges blind-scored screenshots on 5 axes. Anthropic's frontend-design came first (8.0 overall, tied with two others). Judge identity is unverified, and there is no no-skill baseline. — [HappyCapy Skill Arena](https://happycapy.ai/skill-arena/frontend-design)
- The rest is anecdote. One blogger reported 35 minutes without the skill versus 12 minutes with it for one component, which measures speed, not quality. ClickUp recommends running the identical prompt with and without the skill. — [ClickUp: Claude design skills](https://clickup.com/blog/claude-skills-design/)
- The "AI look" stereotype (opinion): Inter, purple-to-blue gradients, nested cards, a centred hero with a glowing number. — [emelia.io](https://emelia.io/hub/impeccable-ai-design-skill)

### Inferences
- The rules that recur across skills are: tinted neutrals, no pure black or grey, no grey text on colour, no card nesting, no bounce easing, no default fonts, a palette in OKLCH, real photos and content, a fixed direction drawn from a curated set, and browser screenshot checks at several widths with a capped number of fix rounds.
- Impeccable's split between deterministic rules and LLM critique is the most directly reusable checker design.

### Gaps
- No blind with-vs-without study of any design skill was found. Effectiveness is unproven beyond screenshots and star counts.

## 3. Process techniques that improve AI design quality

### Takeaway
The best-supported technique is a separate evaluator that screenshots the live page with a browser, scores it against a weighted rubric and feeds a critique back over several iterations. Anthropic describes this, and ReLook and the UICrit work back it up. Committing to a named direction, tokens or rule files first, and using real content are recommended everywhere, but the support is qualitative.

### Cited Findings
- Anthropic's harness rubric:
  - Design quality: "Does the design feel like a coherent whole rather than a collection of parts?"
  - Originality: "Is there evidence of custom decisions, or is this template layouts, library defaults, and AI-generated patterns?"
  - Craft: "typography hierarchy, spacing consistency, color harmony, contrast ratios"
  - Functionality: "Usability independent of aesthetics."

  Design quality and originality were weighted more heavily, because the model already handles craft well. — [Anthropic Engineering: Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- In the same harness, the evaluator used Playwright MCP to browse and screenshot the page, and ran 5–15 iterations, up to 4 hours. After each round the generator chose whether to refine or pivot to a new aesthetic. Few-shot calibration examples with score breakdowns reduced score drift. Agents "reliably skew positive when grading their own work," so the generator and evaluator were kept separate. Scores plateaued, and the author sometimes preferred a middle iteration. Even after tuning, the evaluator missed small layout problems. — [same](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- ReLook (RL for web coding): an MLLM critic scores screenshots in a generate–diagnose–refine loop. It uses a "strict zero-reward rule for invalid renders" against reward hacking and accepts only improving revisions. The authors claim it "consistently outperforms strong baselines". Figures are not in the abstract. — [arXiv 2510.11498](https://arxiv.org/abs/2510.11498)
- UICrit: 3,059 designer critiques of 983 mobile UIs. Few-shot and visual prompting gave a "55% performance gain in LLM-generated UI feedback." — [arXiv 2407.08850](https://arxiv.org/abs/2407.08850). A follow-up uses iterative refinement of the critique and its bounding boxes, and closes 50% of the gap to humans on one metric. — [arXiv 2412.16829](https://arxiv.org/abs/2412.16829)
- Lovable on naming the style: style words "meaningfully influence typography, spacing, shadow, border radius, and color palette". Specific wording beats vague wording. — [Lovable docs](https://docs.lovable.dev/prompting/prompting-one)
- Rules first: Figma (Guidelines.md), Google (DESIGN.md) and Bolt (real component code) all put persistent design-system context ahead of prompts. — [Figma](https://developers.figma.com/docs/code/write-design-system-guidelines/); [Bolt](https://support.bolt.new/building/design-system/best-practices); [Nervegna](https://nervegna.substack.com/p/vibe-design-is-real-inside-google)
- Picking from several options: Taste Skill deals 3 directions and picks one. v0 uses a GenerateDesignInspiration tool before design work. — [taste-skill](https://github.com/Leonxlnx/taste-skill); [leaked v0 prompt](https://raw.githubusercontent.com/x1xhlol/system-prompts-and-models-of-ai-tools/main/v0%20Prompts%20and%20Tools/Prompt.txt)

### Inferences
- For our pipeline: a direction step that picks one of N named directions, then a tokens or DESIGN.md step, then the build, then a *separate* reviewer agent. The reviewer screenshots several widths, applies deterministic rules plus a weighted rubric with few-shot calibration, and runs a capped number of rounds. Keep the best round, not the last.

### Gaps
- No controlled study was found that isolates the effect of moodboards or reference images, tokens-first, or real versus placeholder content on rated quality.

## 4. Automatic evaluation of UI aesthetics: what correlates with humans

### Takeaway
VLM judges are reliable at *ranking models* and at *large* quality gaps: ArtifactsBench reports 94.4% ranking consistency with WebDev Arena. They are close to chance on close pairs, and on usability or comfort. Pairwise comparison and checklist rubrics are more reliable than absolute scores. Computed metrics explain only about 35–50% of the variance in aesthetic ratings, so they suit regression guards better than taste scores.

### Cited Findings
- MLLM-as-UI-judge (30 UIs, crowdsourced ratings): "MLLMs approximate human preferences on some dimensions but diverge on others." — [arXiv 2510.08783](https://arxiv.org/abs/2510.08783)
- Pairwise accuracy in that study was Claude 59.98%, GPT-4o 59.60%, Llama 52.96%. "Interesting" was easiest (Claude 78.49%, Pearson 0.85). Accuracy reached about 93% at the largest human score gaps and stayed near 50% for close pairs. "Ease of Use" was overestimated, with pairwise accuracy about 47–52%. Scores cluster more tightly than human scores. The authors recommend "UI testing approximators, not replacements." — [arXiv 2510.08783 HTML](https://arxiv.org/html/2510.08783)
- ArtifactsBench: an app runs in a sandbox, 3 screenshots of the interaction are taken, and an MLLM scores it against a 10-dimension checklist for each task (Gemini-2.5-Pro and Qwen2.5-VL-72B as referees). It reports "94.4% ranking consistency with WebDev Arena" and "up to 90.95% pairwise agreement with human experts." These are the authors' own figures and have not been independently replicated. — [arXiv 2507.04952](https://arxiv.org/abs/2507.04952)
- WebDev Arena: two models build an app, a user interacts with both and votes, and Bradley-Terry ranks the models. It had 80k+ votes after launch in December 2024. — [LMArena blog: WebDev Arena](https://news.lmarena.ai/webdev-arena). See the critique of arena practices in [The Leaderboard Illusion, arXiv 2504.20879](https://arxiv.org/pdf/2504.20879)
- Position bias: WiserUI-Bench (A/B-tested variants) reports that MLLMs remain sensitive to position bias and do poorly at predicting behaviour-aligned preferences. This is secondhand, via PerceptUI. — [arXiv 2606.05697](https://arxiv.org/html/2606.05697v1)
- Pairwise beats pointwise: GenArena (general visual generation) reports an immediate accuracy boost from switching to pairwise judging. — [arXiv 2602.06013](https://arxiv.org/pdf/2602.06013)
- Design2Code (reference-based):
  - Metrics: Block-Match, Text (Dice), Position, Color (CIEDE2000), CLIP.
  - A logistic regression on these metrics predicted human pairwise preference with 79.9% accuracy. Layout, colour and CLIP mattered, and text detail did not.
  - Humans judged GPT-4V pages better designed than the original in 64% of cases.

  — [arXiv 2403.03163](https://arxiv.org/html/2403.03163v3)
- Computed aesthetics (Miniukovich, Oulasvirta et al.): metrics for colour depth, dominant colours, clutter, symmetry, figure-ground contrast and edge congestion explained 36% of the variance in aesthetics ratings for mobile UIs, and up to 49–51% for webpages in other studies. Visual complexity was a strong predictor. These metrics are packaged as Aalto Interface Metrics (AIM). — [Oulasvirta et al. 2018 AIM PDF](https://acris.aalto.fi/ws/portalfiles/portal/30261274/ELEC_oulasvirta_et_al_2018_002_.pdf); [Miniukovich papers](https://unitn.academia.edu/AliakseiMiniukovich)
- UI2Code^N's VLM judge, checked against 2 experts on 80 samples, gave Pearson 0.93 for net-win margins. The sample is small. — [arXiv 2511.08195](https://arxiv.org/pdf/2511.08195)

### Inferences
- In the pipeline, use the VLM judge pairwise, with position swapped and a per-task checklist, to pick between candidates or iterations, and to catch big failures. Do not trust it to tell apart close variants, or to score usability or comfort.
- Use deterministic checks as hard gates:
  - contrast and WCAG
  - number of colours and fonts
  - spacing-scale adherence
  - touch-target size
  - banned patterns (Impeccable-style rules)
  - overflow at several widths
- Treat complexity and colourfulness metrics (AIM) as soft signals at best.

### Gaps
- No independent replication of ArtifactsBench agreement was found. No dedicated learned UI aesthetic model with published human correlation for 2025–26 was found, beyond UICrit's proposed reward model. No study was found on whether VLM judges are themselves biased *toward* the "AI look" (Anthropic notes generosity toward LLM output, but this is not quantified). There are no computed metrics for alignment-grid adherence with human validation.
