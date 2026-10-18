#!/usr/bin/env python3
"""Minimal, original pre/post-tool checkpoint hook for sheth-developer-tools.

This is a deliberately small illustration of this plugin's own
"pre-tool checkpoint" / "post-tool checkpoint" authoring convention
(see ../docs/hooks.md), wired up as a REAL Claude Code hook
(PreToolUse / PostToolUse, declared in ../hooks/hooks.json). It is not a
general-purpose contract checker for every skill in this plugin — it only
demonstrates the mechanism with one mechanically-checkable rule per stage,
for the Write tool.

Claude Code invokes this script with the hook's JSON payload on stdin and
a single CLI argument identifying which stage is running: "pre" or
"post". Exiting non-zero from a PreToolUse hook blocks the tool call;
exiting non-zero from a PostToolUse hook surfaces a warning but does not
undo the completed action. This script is intentionally conservative: it
only blocks on a structurally unambiguous problem, never on a judgment
call, and it never raises on malformed/unexpected input - it fails open
(exit 0) so a hook bug can never silently brick the plugin's own tool use.
"""
from __future__ import annotations

import json
import sys


def _read_payload() -> dict:
    try:
        raw = sys.stdin.read()
    except Exception:
        return {}
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def check_pre(payload: dict) -> int:
    """Pre-tool checkpoint: the Write tool's input must at least have a
    non-empty target path and some content — this is the mechanical floor
    of each skill's "Input contract" section, not a full validation of it.
    """
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        # Unexpected payload shape: fail open rather than guess.
        return 0

    file_path = tool_input.get("file_path")
    content = tool_input.get("content")

    if file_path is not None and not str(file_path).strip():
        print(
            "sheth-developer-tools pre-tool checkpoint: blocked a Write "
            "with an empty file_path.",
            file=sys.stderr,
        )
        return 2

    if content is not None and content == "":
        print(
            "sheth-developer-tools pre-tool checkpoint: blocked a Write "
            "with empty content — likely an incomplete formatting/"
            "conversion result rather than an intentional empty file.",
            file=sys.stderr,
        )
        return 2

    return 0


def check_post(payload: dict) -> int:
    """Post-tool checkpoint: a completed Write's reported result should be
    internally consistent (no error reported alongside a success marker).
    This is the mechanical floor of each skill's "No hallucination rule" —
    it does not verify the written content is semantically correct, only
    that the hook payload itself isn't self-contradictory.
    """
    tool_response = payload.get("tool_response")
    if not isinstance(tool_response, dict):
        return 0

    if tool_response.get("error") and tool_response.get("success"):
        print(
            "sheth-developer-tools post-tool checkpoint: tool_response "
            "reports both an error and success=true; flagging rather than "
            "letting the skill report an unverified success.",
            file=sys.stderr,
        )
        return 2

    return 0


def main() -> int:
    stage = sys.argv[1] if len(sys.argv) > 1 else ""
    payload = _read_payload()

    if stage == "pre":
        return check_pre(payload)
    if stage == "post":
        return check_post(payload)

    # Unknown stage: fail open, do not block anything.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
