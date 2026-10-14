# Source

Third-party skill, copied with one change (D33, D91).

- Repo: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill, folder `.claude/skills/ui-ux-pro-max`
- Commit: 7246805992a42b7bba37d4cac83b01416f0c6c44 (2026-10-12)
- Licence: MIT (Copyright (c) 2024 Next Level Builder), see `LICENSE` here
- Copied: SKILL.md, data/, references/, and scripts/search.py, core.py,
  design_system.py, reasoning_contract.py. Left out: scripts/tests/ and
  scripts/validate_data.py (the project's own test and data tooling).
- Changed: in SKILL.md, every `${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py`
  became `${CLAUDE_SKILL_DIR}/scripts/search.py`, because in this plugin the
  skill lives at `skills/ui-ux-pro-max/`. Nothing else changed.
- Reviewed 2026-10-14: SKILL.md read in full; the four scripts read in full.
  They use the Python standard library only: no network, no subprocess, no
  eval. They read only the skill's own data/ folder. The only write is
  `--persist`, into `<output-dir or cwd>/design-system/<slug>/`; the harness
  never passes `--persist` (it writes docs/design/ itself).
- To update: copy a newer commit, review it the same way, redo the path
  change, and update the commit above.
