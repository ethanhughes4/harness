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


# Skills agents preload or invoke must be model-invocable (D4); every other skill is user-only.
MODEL_INVOCABLE = {"architecture", "web-design-engineer"}


def test_skills_not_model_invocable_except_preloaded():
    for p in SKILLS:
        if p.parent.name not in MODEL_INVOCABLE:
            assert frontmatter(p).get("disable-model-invocation", "").strip() == "true", p


def test_plugin_root_variable_only_where_it_is_read():
    # Claude Code substitutes ${CLAUDE_PLUGIN_ROOT} in plugin agent and skill text, so a
    # sentence like "never use ${CLAUDE_PLUGIN_ROOT}" becomes "never use <the plugin path>".
    # Only setup, new and smoke may name it, on the line that hands them the path.
    var = "${CLAUDE_PLUGIN_ROOT}"
    for f in list(ROOT.glob("agents/*.md")) + list(ROOT.glob("skills/*/SKILL.md")):
        lines = [l for l in f.read_text(encoding="utf-8").splitlines() if var in l]
        if f.parent.name in ("setup", "new", "smoke"):
            assert lines == [f"The plugin's absolute folder is: {var}"], f
        else:
            assert not lines, f
