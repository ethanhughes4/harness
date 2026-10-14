---
max_turns: 15
allowed_tools: [Agent, Read, Glob, Grep]
tags: [questions, critic]
expected_outcome: The critic changes the technical answer that contradicts the decisions, agrees with the sound one, and does not review the PREFERENCE question.
---

The /harness:questions skill has drafted the list below. Ask the
harness:critic agent to check it, giving it the full list and the text of
docs/decisions.md below (this project has no other files), and reply with
exactly what the critic answers.

docs/decisions.md:

```
## tool
D1: The tool must run on Python 3.9, the oldest version the owner's machine has. (reason: owner)
D2: Standard library only, no new dependencies. (reason: owner)
```

Questions:

1. [TECHNICAL] Which Python syntax can we use for branching on a command name?
   Recommended: a `match` statement. It is the clearest way to branch.
2. [TECHNICAL] How should the config file be read?
   Recommended: `json.load` from the standard library. No dependency needed.
3. [PREFERENCE] What should the tool print when it finishes?
   Recommended: one line, "done". Short output is easiest to scan.
