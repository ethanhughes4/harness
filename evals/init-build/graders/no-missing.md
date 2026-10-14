---
type: llm
---

PASS if the reply is a JSON list of features where every feature has
id, stage, title, ui, depends_on, steps (non-empty, concrete) and
passes false, and together the features cover all five requirements:
add, list (including the empty case), delete (including the unknown
number), saving to notes.json, and no renumbering after delete. A
dependency, if any, points at an existing id.
FAIL if any requirement is missing, a step is vague, a passes is true,
or a field is missing.
