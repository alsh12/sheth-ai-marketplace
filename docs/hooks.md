# Hooks: pre-tool and post-tool checkpoints

This document covers two things that are easy to conflate, so they are
kept deliberately separate:

1. **A real Claude Code feature**: plugins can declare `hooks` (a
   `hooks/hooks.json` file or an inline `hooks` field in `plugin.json`)
   that run actual shell commands at lifecycle events such as
   `PreToolUse` and `PostToolUse`. This is documented in Anthropic's own
   plugin manifest reference and is implemented by Claude Code itself —
   it is not something this marketplace invents.
2. **An original authoring convention layered on top of that feature**:
   this marketplace's own "pre-tool checkpoint" / "post-tool checkpoint"
   pattern, described below, for how a skill author in this marketplace
   should use that real mechanism (or, where no tool call is involved,
   should describe the equivalent discipline in prose inside SKILL.md).

## Honesty check: what's real vs. what's guidance

- **Real and implemented**: `PreToolUse` and `PostToolUse` hook events
  exist in Claude Code's plugin system (`hooks/hooks.json`, or a `hooks`
  key in `plugin.json`), and run an actual command with JSON on stdin
  before/after a tool call. One plugin in this marketplace,
  `sheth-developer-tools`, ships a minimal **working** example of this
  (see below) — it is original to this repository, not copied from any
  other project.
- **Guidance only, not a runtime feature**: the specific checklist
  content below ("validate input contract before invoking a tool",
  "detect a hallucinated result after a tool call returns") is this
  marketplace's own authoring convention for what a hook *should check*
  for a given skill. Claude Code does not enforce these specific checks
  automatically — a skill author has to write the actual hook script (or
  follow the discipline in prose) for their own skill. Most of the 14
  skills in this marketplace rely on the prose form (the "Input
  contract" / "Output contract" / "No hallucination rule" sections in
  each `SKILL.md`) rather than a wired-up hook script, because most of
  their work (formatting, review, analysis) doesn't invoke an external
  tool call that a hook could intercept.

## The convention: pre-tool and post-tool checkpoints

For a skill whose workflow does invoke a tool (a script, an external
command, a file write), skill authors in this marketplace are encouraged
to think in two checkpoints:

- **Pre-tool checkpoint**: before the tool runs, confirm the input
  actually matches the skill's documented "Input contract" section
  (right shape, required fields present). Reject or ask for
  clarification rather than passing through something that doesn't match.
- **Post-tool checkpoint**: after the tool returns, confirm the result
  actually matches the skill's "Output contract" section, and that
  nothing is being reported (a line number, a pass/fail result, a parsed
  value) that the tool didn't actually produce — this is the mechanical
  side of each skill's "No hallucination rule" section.

Where a real `PreToolUse`/`PostToolUse` hook is wired up (as in the
example below), it enforces this mechanically. Where it isn't, the
`SKILL.md` prose is the enforcement mechanism, and that is an honest,
intentional choice for skills whose checks (e.g., "does this review cite
a real file:line") aren't easily expressed as a standalone shell script.

## Working example: sheth-developer-tools

`plugins/sheth-developer-tools/hooks/hooks.json` declares a minimal
`PreToolUse` hook that runs before any `Write` tool call while this
plugin is enabled, and a `PostToolUse` hook that runs after. Both call a
small, original stdlib-only Python script
(`plugins/sheth-developer-tools/scripts/tool_checkpoint.py`) that reads
the hook's JSON payload from stdin and exits non-zero (blocking the
action, for `PreToolUse`) only on a structurally obvious problem — it
does not attempt to replicate full skill logic. See that plugin's
`hooks/hooks.json` and `scripts/tool_checkpoint.py` for the actual,
runnable implementation.

This is intentionally a minimal, illustrative example — it demonstrates
the mechanism is real and wired up correctly, not a full implementation
of input/output-contract checking for every skill in the marketplace.
