import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = sorted(ROOT.glob("skills/*/SKILL.md"))
AGENTS = sorted(ROOT.glob("agents/*.md"))


def frontmatter(path):
    m = re.match(r"---\r?\n(.*?)\r?\n---", path.read_text(encoding="utf-8"), re.S)
    assert m, f"{path} has no frontmatter"
    return dict(line.split(":", 1) for line in m.group(1).splitlines() if re.match(r"^\w[\w-]*:", line))


def test_plugin_json():
    data = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    assert data["name"] == "harness"


def test_files_have_frontmatter():
    for p in SKILLS + AGENTS:
        fm = frontmatter(p)
        assert "name" in fm or "description" in fm, p


def test_agents_use_no_ignored_fields():
    for p in AGENTS:
        for key in ("hooks", "permissionMode", "mcpServers"):
            assert key not in frontmatter(p), (p, key)


def test_skills_not_model_invocable_except_architecture():
    for p in SKILLS:
        if p.parent.name != "architecture":
            assert frontmatter(p).get("disable-model-invocation", "").strip() == "true", p
