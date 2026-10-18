#!/usr/bin/env python3
"""Run mechanically-checkable eval fixtures for Sheth AI Marketplace skills.

Honest scope: this harness does NOT invoke Claude or any skill's actual
instructions — there is no offline way to run a SKILL.md's prose through
a model from this script. What it DOES do, for each fixture, is verify
the mechanically-checkable `pass_criteria` entries against the fixture's
own `input` using real stdlib parsers (e.g., "this input that the fixture
claims is invalid JSON is actually invalid JSON", "formatting this input
and reparsing it yields the same value"). This catches fixture authoring
mistakes and encodes the ground truth a human (or a future live-session
eval) checks a real skill run against.

Any `pass_criteria` entry with `"requires_manual_review": true` is never
claimed to pass here — it is listed as skipped/manual, exactly as
docs/testing.md describes. This script never fabricates a pass for a
criterion it did not actually check.

Usage:
    python tests/evals/run_evals.py [--dir PATH]

Exit code is non-zero if any mechanically-checkable criterion fails.
"""
from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

DEFAULT_DIR = Path(__file__).resolve().parent


def check_json_round_trip(input_text: str) -> tuple[bool, str]:
    try:
        value = json.loads(input_text)
    except json.JSONDecodeError as exc:
        return False, f"input did not parse as JSON: {exc}"
    # Round-trip through dump/load and confirm equality.
    dumped = json.dumps(value, indent=2)
    reparsed = json.loads(dumped)
    if reparsed != value:
        return False, "round-tripped value did not equal original"
    return True, "input parses and round-trips to an equal value"


def check_json_is_invalid(input_text: str) -> tuple[bool, str]:
    try:
        json.loads(input_text)
    except json.JSONDecodeError as exc:
        return True, f"input correctly fails to parse ({exc})"
    return False, "input unexpectedly parsed as valid JSON"


def check_xml_is_well_formed(input_text: str) -> tuple[bool, str]:
    try:
        ET.fromstring(input_text)
    except ET.ParseError as exc:
        return False, f"input unexpectedly failed to parse ({exc})"
    return True, "input parses as well-formed XML"


def check_xml_is_malformed(input_text: str) -> tuple[bool, str]:
    try:
        ET.fromstring(input_text)
    except ET.ParseError as exc:
        return True, f"input correctly fails to parse ({exc})"
    return False, "input unexpectedly parsed as well-formed XML"


CHECKS = {
    "json_round_trip": check_json_round_trip,
    "json_is_invalid": check_json_is_invalid,
    "xml_is_well_formed": check_xml_is_well_formed,
    "xml_is_malformed": check_xml_is_malformed,
}


def run_fixture(path: Path) -> tuple[int, int, int, list[str]]:
    """Returns (passed, failed, manual, messages) for one fixture file."""
    data = json.loads(path.read_text(encoding="utf-8"))
    skill = data.get("skill", path.stem)
    input_text = data.get("input", "")
    criteria = data.get("pass_criteria", [])

    passed = failed = manual = 0
    messages: list[str] = []

    for criterion in criteria:
        crit_id = criterion.get("id", "<unnamed>")
        if criterion.get("requires_manual_review"):
            manual += 1
            messages.append(
                f"[{skill}] {crit_id}: MANUAL REVIEW REQUIRED (not automated) - "
                f"{criterion.get('description', '')}"
            )
            continue

        check_name = criterion.get("check")
        check_fn = CHECKS.get(check_name)
        if check_fn is None:
            failed += 1
            messages.append(
                f"[{skill}] {crit_id}: FAIL - no mechanical check named "
                f"'{check_name}' is implemented"
            )
            continue

        ok, detail = check_fn(input_text)
        if ok:
            passed += 1
            messages.append(f"[{skill}] {crit_id}: PASS - {detail}")
        else:
            failed += 1
            messages.append(f"[{skill}] {crit_id}: FAIL - {detail}")

    return passed, failed, manual, messages


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", type=Path, default=DEFAULT_DIR)
    args = parser.parse_args()

    fixture_paths = sorted(args.dir.rglob("*.json"))
    if not fixture_paths:
        print(f"No fixture files found under {args.dir}", file=sys.stderr)
        return 1

    total_passed = total_failed = total_manual = 0
    for path in fixture_paths:
        passed, failed, manual, messages = run_fixture(path)
        total_passed += passed
        total_failed += failed
        total_manual += manual
        for message in messages:
            print(message)

    print(
        f"\n{total_passed} mechanical check(s) passed, "
        f"{total_failed} failed, {total_manual} require manual review."
    )

    return 1 if total_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
