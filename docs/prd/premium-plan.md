# Premium layer: build plan

Decisions: docs/prd/factory-decisions.md D100-D105 (on top of D1-D99).
Source: reports/What makes sites look premium.md, section "Changes to the
pipeline" and the sections it cites; research notes in
research_notes/What makes sites look premium/.
Tests: `python -m pytest -q` at the repo root (allow 400 s).
No shared list; steps touch different files.

## Wave 1

### Step 1: Premium spec and fonts in the guideline skill. Status: DONE
Depends on: none.
After it: `harness:design-guideline` carries the premium layer: the
reference step, premium defaults, the critique loop and font guidance.
Creates: `skills/design-guideline/references/premium-spec.md`,
`skills/design-guideline/references/fonts.md`.
Changes: `skills/design-guideline/SKILL.md` (a "Premium layer" section:
what it is, D100-D104, the override rule, pointers), `skills/design-guideline/SOURCE.md`.
(D100, D101, D102, D104)

### Step 2: Audit premium checks and reference capture. Status: DONE
Depends on: none.
After it: the audit reports premium checks; `reference_capture.py <name>
<url>...` saves screenshots and measured values of reference pages;
`design_audit.py --compare reference-spec.json` reports a page against a
reference range.
Creates: `scripts/reference_capture.py`, fixtures and tests.
Changes: `scripts/design_audit.js`, `scripts/design_audit.py`,
`tests/test_design_audit.py`. (D101, D105)

### Step 3: The design critic. Status: DONE
Depends on: none.
After it: `harness:design-critic` judges a design against references and
the calibration example.
Creates: `agents/design-critic.md`,
`skills/design-guideline/references/calibration/` (Pocket Instrument
screenshots + the report's critique of them as the "competent but generic"
example). (D103)

## Wave 2

### Step 4: The intake uses references, premium defaults and the critic. Status: TODO
Depends on: 1, 2, 3.
Changes: `skills/questions/SKILL.md` (design step), `skills/new/SKILL.md`,
`skills/setup/SKILL.md` (allow rule for reference_capture.py).
(D101-D104)

### Step 5: Builder and visual reviewer use the premium layer. Status: TODO
Depends on: 1, 2, 3.
Changes: `agents/builder.md`, `agents/visual.md`, `docs/design.md`.
(D102, D103, D105)

## Coverage
D100 s1 · D101 s1,2,4 · D102 s1,4,5 · D103 s3,4,5 · D104 s1,4 · D105 s2,5
