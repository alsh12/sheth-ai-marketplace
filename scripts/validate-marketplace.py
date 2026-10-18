#!/usr/bin/env python3
"""Validate the Sheth AI Marketplace catalog.

Checks performed:
  - .claude-plugin/marketplace.json exists, parses, and has required
    top-level fields (name, owner, plugins).
  - Every plugin entry has a unique name and a resolvable "source" path.
  - Each referenced plugin directory has a .claude-plugin/plugin.json that
    parses and has required fields (name, version, description, author).
  - Each plugin's skills/ directory (if present) has one subdirectory per
    skill, each containing a SKILL.md with parseable YAML frontmatter
    containing required fields (name, description).
  - No duplicate skill names within a single plugin.

Usage:
    python scripts/validate-marketplace.py [--root PATH] [--only NAME ...]

Exits non-zero with a clear message list on any failure.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


class ValidationError(Exception):
    pass


def _parse_frontmatter(text: str) -> dict:
    """Parse a minimal YAML frontmatter block (flat string: string pairs).

    Supports the subset of YAML actually used by this repo's SKILL.md
    files: a leading '---' delimited block of "key: value" lines, with
    values optionally quoted. Does not attempt to be a general YAML
    parser; raises ValidationError on anything it cannot confidently parse.
    """
    if not text.startswith("---"):
        raise ValidationError("SKILL.md must start with a '---' frontmatter delimiter")
    lines = text.split("\n")
    if lines[0].strip() != "---":
        raise ValidationError("SKILL.md frontmatter must start on line 1")
    end_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break
    if end_index is None:
        raise ValidationError("SKILL.md frontmatter has no closing '---'")

    frontmatter: dict = {}
    current_key = None
    for raw_line in lines[1:end_index]:
        if not raw_line.strip():
            continue
        if raw_line.startswith((" ", "\t")) and current_key is not None:
            # Continuation of a multi-line scalar; append as text.
            frontmatter[current_key] = (
                frontmatter[current_key] + " " + raw_line.strip()
            )
            continue
        if ":" not in raw_line:
            raise ValidationError(f"Unparseable frontmatter line: {raw_line!r}")
        key, _, value = raw_line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
            value = value[1:-1]
        frontmatter[key] = value
        current_key = key
    return frontmatter


def _load_json(path: Path, label: str) -> dict:
    if not path.is_file():
        raise ValidationError(f"{label}: file not found at {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{label}: invalid JSON ({exc})") from exc


def validate_plugin_manifest(plugin_dir: Path, errors: list[str]) -> str | None:
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    try:
        manifest = _load_json(manifest_path, f"plugin manifest ({plugin_dir.name})")
    except ValidationError as exc:
        errors.append(str(exc))
        return None

    required = ["name", "version", "description", "author"]
    for field in required:
        if field not in manifest or not manifest[field]:
            errors.append(
                f"{manifest_path}: missing required field '{field}'"
            )

    author = manifest.get("author")
    if isinstance(author, dict):
        if not author.get("name"):
            errors.append(f"{manifest_path}: author.name is required")
    elif author is not None:
        errors.append(f"{manifest_path}: 'author' must be an object with a 'name' field")

    return manifest.get("name")


def validate_skills(plugin_dir: Path, plugin_name: str, errors: list[str]) -> None:
    skills_dir = plugin_dir / "skills"
    if not skills_dir.is_dir():
        errors.append(f"{plugin_dir}: no skills/ directory found")
        return

    skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir())
    if not skill_dirs:
        errors.append(f"{skills_dir}: contains no skill subdirectories")
        return

    seen_names: dict[str, Path] = {}
    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{skill_dir}: missing SKILL.md")
            continue

        text = skill_md.read_text(encoding="utf-8")
        try:
            frontmatter = _parse_frontmatter(text)
        except ValidationError as exc:
            errors.append(f"{skill_md}: {exc}")
            continue

        for field in ("name", "description"):
            if not frontmatter.get(field):
                errors.append(f"{skill_md}: frontmatter missing required field '{field}'")

        skill_name = frontmatter.get("name")
        if skill_name:
            if skill_name in seen_names:
                errors.append(
                    f"{skill_md}: duplicate skill name '{skill_name}' "
                    f"(also used by {seen_names[skill_name]}) within plugin '{plugin_name}'"
                )
            else:
                seen_names[skill_name] = skill_md


def validate_marketplace(root: Path, only: list[str] | None) -> list[str]:
    errors: list[str] = []

    marketplace_path = root / ".claude-plugin" / "marketplace.json"
    try:
        marketplace = _load_json(marketplace_path, "marketplace.json")
    except ValidationError as exc:
        return [str(exc)]

    for field in ("name", "owner", "plugins"):
        if field not in marketplace:
            errors.append(f"{marketplace_path}: missing required top-level field '{field}'")

    owner = marketplace.get("owner")
    if isinstance(owner, dict):
        if not owner.get("name"):
            errors.append(f"{marketplace_path}: owner.name is required")
    elif owner is not None:
        errors.append(f"{marketplace_path}: 'owner' must be an object with a 'name' field")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        errors.append(f"{marketplace_path}: 'plugins' must be a non-empty array")
        return errors

    seen_ids: dict[str, int] = {}
    for index, entry in enumerate(plugins):
        label = f"plugins[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label}: entry must be an object")
            continue

        name = entry.get("name")
        source = entry.get("source")
        if not name:
            errors.append(f"{label}: missing required field 'name'")
        if not source:
            errors.append(f"{label}: missing required field 'source'")

        if name:
            if name in seen_ids:
                errors.append(
                    f"{label}: duplicate plugin id '{name}' "
                    f"(also used by plugins[{seen_ids[name]}])"
                )
            else:
                seen_ids[name] = index

        if only and name not in only:
            continue

        if not isinstance(source, str) or not source.startswith("./"):
            errors.append(f"{label}: 'source' must be a relative path starting with './'")
            continue

        plugin_dir = (root / source).resolve()
        if not plugin_dir.is_dir():
            errors.append(f"{label}: source path not found: {source}")
            continue

        manifest_name = validate_plugin_manifest(plugin_dir, errors)
        validate_skills(plugin_dir, manifest_name or name or source, errors)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Marketplace root directory (default: repo root relative to this script)",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=None,
        help="Restrict deep validation (manifest + skills) to this plugin name. "
        "May be passed multiple times. Marketplace-level checks still run on all "
        "entries.",
    )
    args = parser.parse_args()

    errors = validate_marketplace(args.root, args.only)

    if errors:
        print("Marketplace validation FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        print(f"\n{len(errors)} error(s) found.", file=sys.stderr)
        return 1

    print("Marketplace validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
