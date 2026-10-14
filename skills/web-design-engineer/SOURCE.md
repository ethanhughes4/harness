# Source

Third-party skill, copied unchanged (D33, D88).

- Repo: https://github.com/ConardLi/garden-skills, folder `skills/web-design-engineer`
- Commit: 7a6d5a72e4f44bb4cc0c23c01b3d97205c723b68 (2026-10-11), skill version 1.3.0
- Licence: MIT, see `LICENSE` in this folder
- Copied: SKILL.md and references/. Left out: README.md, README.zh-CN.md,
  manifest.json, agents/openai.yaml (human docs and Codex metadata).
- Reviewed 2026-10-14: SKILL.md read in full; references read in full or
  searched for commands, URLs, secrets and hidden instructions. No install,
  shell or exfiltration instructions. Remote resources appear only in
  example code (Chart.js and Google Fonts links in advanced-patterns.md).
- How the harness uses it: see the harness notes in skills/questions,
  agents/builder.md and agents/visual.md. To update, copy a newer commit,
  review it the same way, and change the commit above.
