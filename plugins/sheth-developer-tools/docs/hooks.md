# Hooks: pre-tool and post-tool checkpoints

This document covers two things that are easy to conflate, so they are
kept deliberately separate:

1. **A real Claude Code feature**: plugins can declare `hooks` (a
   `hooks/hooks.json` file or an inline `hooks` field in `plugin.json`)
   that run actual shell commands at lifecycle events such as
   `PreToolUse` and `PostToolUse`. This is documented in Anthropic's own
   plugin manifest reference and is implemented by Claude Code itself —
   it is not something this plugin invents.
2. **An original authoring convention layered on top of that feature**:
   this plugin's own "pre-tool checkpoint" / "post-tool checkpoint"
   pattern, described below, for how a hook should behave for a skill
   whose workflow invokes a tool call.

## Honesty check: what's real vs. what's guidance

- **Real and implemented**: `PreToolUse` and `PostToolUse` hook events
  exist in Claude Code's plugin system (`hooks/hooks.json`, or a `hooks`
  key in `plugin.json`), and run an actual command with JSON on stdin
  before/after a tool call. This plugin ships a minimal **working**
  example of this (see below) — it is original to this repository, not
  copied from any other project.
- **Guidance only, not a runtime feature**: the specific checklist
  content below ("validate input contract before invoking a tool",
  "detect a hallucinated result after a tool call returns") is this
  plugin's own authoring convention for what a hook *should check*. Claude
  Code does not enforce these specific checks automatically — the hook
  script implements the actual logic; the convention just explains why it
  checks what it checks.

## The convention: pre-tool and post-tool checkpoints

For a skill whose workflow does invoke a tool (a script, an external
command, a file write), this plugin's hooks think in two checkpoints:

- **Pre-tool checkpoint**: before the tool runs, confirm the input
  actually matches the skill's documented "Input contract" section
  (right shape, required fields present). Reject or ask for
  clarification rather than passing through something that doesn't match.
- **Post-tool checkpoint**: after the tool returns, confirm the result
  actually matches the skill's "Output contract" section, and that
  nothing is being reported (a line number, a pass/fail result, a parsed
  value) that the tool didn't actually produce — this is the mechanical
  side of each skill's "No hallucination rule" section.

## Working example: this plugin's Write hook

`hooks/hooks.json` declares a minimal `PreToolUse` hook that runs before
any `Write` tool call while this plugin is enabled, and a `PostToolUse`
hook that runs after. Each hook command is a plain shell script
(`scripts/tool_checkpoint_pre.sh`, `scripts/tool_checkpoint_post.sh`)
that only calls another file in the plugin — the actual check logic
lives in a small, original stdlib-only Python script
(`scripts/tool_checkpoint.py`) that reads the hook's JSON payload from
stdin and exits non-zero (blocking the action, for `PreToolUse`) only on
a structurally obvious problem — it does not attempt to replicate full
skill logic. See `hooks/hooks.json`, the two shell wrappers, and
`scripts/tool_checkpoint.py` for the actual, runnable implementation.

This is intentionally a minimal, illustrative example — it demonstrates
the mechanism is real and wired up correctly, not a full implementation
of input/output-contract checking for every skill in this plugin.
