# Design guideline: build plan

Decisions: docs/prd/factory-decisions.md D95-D99 (on top of D1-D94).
Source: reports/Design guideline against AI look.md, section "The guideline".
Tests: `python -m pytest -q` at the repo root (allow 400 s).

No shared list in this stage; steps touch different files.

## Wave 1

### Step 1: The guideline skill. Status: DONE
Depends on: none.
After it: agents can load `harness:design-guideline` and get the Never/Always
rules, per-client steps and checks, with precedence over the vendored skills.
Creates: `skills/design-guideline/SKILL.md` (model-invocable: who uses it,
the overriding reason rule, precedence table, Always A1-A17, per-client steps
1-10, checks, judge method), `skills/design-guideline/references/tells.md`
(N1-N19 with detector and fix, dated, "add new tells here" section),
`skills/design-guideline/SOURCE.md` (the report and research notes it comes
from). Changes: `tests/test_layout.py` (MODEL_INVOCABLE gains it). (D95)

### Step 2: The design audit script. Status: DONE
Depends on: none.
After it: `python <plugin_root>/scripts/design_audit.py <url> [--sheet docs/design/design-system.md]`
prints a JSON audit of a running page and exits non-zero on hard failures.
Creates: `scripts/design_audit.js`, `scripts/design_audit.py`,
`tests/test_design_audit.py` (fixture pages: one full of tells must score
>= 4 and fail; one clean page must pass; skip the browser tests if Python
Playwright is missing). (D97)

### Step 3: The intake follows the per-client steps. Status: DONE
Depends on: none.
After it: `/harness:new` derives a client's direction from the brief with
the 10 steps and writes design-system.md as the brand sheet.
Changes: `skills/questions/SKILL.md` (UI design step), `skills/new/SKILL.md`
(mention), `skills/setup/SKILL.md` (Python Playwright for Python UI
projects; allow rule for design_audit.py). (D96, D99)

## Wave 2

### Step 4: Builder and visual reviewer use the guideline. Status: DONE
Depends on: 1, 2.
After it: the builder builds only from the brand sheet and runs the audit
before DONE; the visual reviewer runs the audit as a hard gate, then judges
with the narrow pairwise questions.
Changes: `agents/builder.md`, `agents/visual.md`, `agents/user-tester.md`
(Python Playwright first), `docs/design.md` (one paragraph). (D95, D97, D98)

## Coverage
D95 s1,4 · D96 s3 · D97 s2,4 · D98 s4 · D99 s3,4
