"""Unit tests for scripts/validate-marketplace.py.

Run with: python -m unittest discover tests
"""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "validate-marketplace.py"

spec = importlib.util.spec_from_file_location("validate_marketplace", SCRIPT_PATH)
validate_marketplace_module = importlib.util.module_from_spec(spec)
sys.modules["validate_marketplace"] = validate_marketplace_module
spec.loader.exec_module(validate_marketplace_module)  # type: ignore[union-attr]


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


GOOD_SKILL_MD = """---
name: demo-skill
description: A demo skill used for testing. Use when testing the validator.
---

# Demo Skill

Body content here.
"""

BAD_SKILL_MD_NO_FRONTMATTER = """# Demo Skill

No frontmatter at all.
"""

BAD_SKILL_MD_MISSING_FIELD = """---
name: demo-skill
---

# Demo Skill

Missing description field.
"""


class RealRepoTests(unittest.TestCase):
    """Validate the actual repository this script lives in."""

    def test_real_marketplace_validates_for_developer_tools(self):
        errors = validate_marketplace_module.validate_marketplace(
            REPO_ROOT, only=["sheth-developer-tools"]
        )
        self.assertEqual(errors, [], msg="\n".join(errors))


class FixtureTests(unittest.TestCase):
    """Validate against good/bad fixtures built in a temp directory."""

    def _build_good_marketplace(self, root: Path, plugin_name: str = "demo-plugin") -> None:
        write_json(
            root / ".claude-plugin" / "marketplace.json",
            {
                "name": "demo-marketplace",
                "owner": {"name": "Demo Owner"},
                "plugins": [
                    {
                        "name": plugin_name,
                        "source": f"./plugins/{plugin_name}",
                        "description": "A demo plugin",
                        "version": "1.0.0",
                    }
                ],
            },
        )
        write_json(
            root / "plugins" / plugin_name / ".claude-plugin" / "plugin.json",
            {
                "name": plugin_name,
                "version": "1.0.0",
                "description": "A demo plugin",
                "author": {"name": "Demo Owner"},
            },
        )
        write_text(
            root / "plugins" / plugin_name / "skills" / "demo-skill" / "SKILL.md",
            GOOD_SKILL_MD,
        )

    def test_good_fixture_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._build_good_marketplace(root)
            errors = validate_marketplace_module.validate_marketplace(root, only=None)
            self.assertEqual(errors, [], msg="\n".join(errors))

    def test_missing_marketplace_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            errors = validate_marketplace_module.validate_marketplace(root, only=None)
            self.assertTrue(errors)
            self.assertIn("file not found", errors[0])

    def test_duplicate_plugin_names_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._build_good_marketplace(root, plugin_name="dup-plugin")
            data = json.loads((root / ".claude-plugin" / "marketplace.json").read_text())
            data["plugins"].append(dict(data["plugins"][0]))
            write_json(root / ".claude-plugin" / "marketplace.json", data)
            errors = validate_marketplace_module.validate_marketplace(root, only=None)
            self.assertTrue(any("duplicate plugin id" in e for e in errors), errors)

    def test_missing_plugin_manifest_field_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._build_good_marketplace(root)
            manifest_path = root / "plugins" / "demo-plugin" / ".claude-plugin" / "plugin.json"
            data = json.loads(manifest_path.read_text())
            del data["description"]
            write_json(manifest_path, data)
            errors = validate_marketplace_module.validate_marketplace(root, only=None)
            self.assertTrue(
                any("missing required field 'description'" in e for e in errors), errors
            )

    def test_missing_skill_md_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._build_good_marketplace(root)
            skill_md = root / "plugins" / "demo-plugin" / "skills" / "demo-skill" / "SKILL.md"
            skill_md.unlink()
            errors = validate_marketplace_module.validate_marketplace(root, only=None)
            self.assertTrue(any("missing SKILL.md" in e for e in errors), errors)

    def test_skill_md_without_frontmatter_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._build_good_marketplace(root)
            skill_md = root / "plugins" / "demo-plugin" / "skills" / "demo-skill" / "SKILL.md"
            write_text(skill_md, BAD_SKILL_MD_NO_FRONTMATTER)
            errors = validate_marketplace_module.validate_marketplace(root, only=None)
            self.assertTrue(any("frontmatter delimiter" in e for e in errors), errors)

    def test_skill_md_missing_required_field_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._build_good_marketplace(root)
            skill_md = root / "plugins" / "demo-plugin" / "skills" / "demo-skill" / "SKILL.md"
            write_text(skill_md, BAD_SKILL_MD_MISSING_FIELD)
            errors = validate_marketplace_module.validate_marketplace(root, only=None)
            self.assertTrue(
                any("missing required field 'description'" in e for e in errors), errors
            )

    def test_duplicate_skill_names_within_plugin_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._build_good_marketplace(root)
            second_skill_dir = (
                root / "plugins" / "demo-plugin" / "skills" / "demo-skill-2"
            )
            write_text(second_skill_dir / "SKILL.md", GOOD_SKILL_MD)  # same name: demo-skill
            errors = validate_marketplace_module.validate_marketplace(root, only=None)
            self.assertTrue(any("duplicate skill name" in e for e in errors), errors)

    def test_source_path_not_found_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_json(
                root / ".claude-plugin" / "marketplace.json",
                {
                    "name": "demo-marketplace",
                    "owner": {"name": "Demo Owner"},
                    "plugins": [
                        {
                            "name": "ghost-plugin",
                            "source": "./plugins/ghost-plugin",
                            "description": "Does not exist on disk",
                            "version": "1.0.0",
                        }
                    ],
                },
            )
            errors = validate_marketplace_module.validate_marketplace(root, only=None)
            self.assertTrue(any("source path not found" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
