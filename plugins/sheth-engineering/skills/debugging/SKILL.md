---
name: debugging
description: Diagnose a bug through reproduction, isolation, and evidence before proposing a fix, then add a regression test. Use when the user reports an error, unexpected behavior, a stack trace, or asks "why is this happening" or "help me debug this".
---

# Debugging

Diagnoses bugs via reproduction and evidence before fixing, then adds a
regression test. See `reference.md` for a worked example. Shared
conventions: `../../../../docs/shared-conventions.md`.

## Boundaries

- Never proposes a fix before a root cause is backed by evidence — a
  guess is a labeled hypothesis, not a diagnosis.
- Never applies a broad speculative refactor when a narrow fix addresses
  the confirmed cause.
- Never claims a fix works without verifying it against the reproduction
  case when that's possible.
- Never hides remaining uncertainty — say explicitly what's still
  unexplained.

## Workflow

1. Understand the problem: expected vs. actual, concrete input/output/
   conditions. Ask for missing specifics rather than assuming.
2. Reproduce or isolate it directly when the environment allows; otherwise
   narrow scope (component/input range/code path).
3. Inspect actual evidence: full stack trace, real log output, exact
   error — quote it, don't paraphrase from memory. Use Grep to locate the
   failing code path rather than reading unrelated files.
4. Form a hypothesis tied to specific evidence (exact file:line + the
   broken condition).
5. Confirm the hypothesis before fixing (targeted log, minimal failing
   test) when possible.
6. Apply the minimal verifiable fix addressing the confirmed cause.
7. Verify against the original reproduction case.
8. Add a regression test (see test-development).
9. Flag any remaining unresolved uncertainty explicitly.

## Input contract

A bug report, error message, stack trace, or description of unexpected
behavior, plus access to the relevant code and logs.

## Output contract

A diagnosis stating the root cause with supporting evidence, the fix
applied (or proposed), confirmation of verification (or an explicit
statement it wasn't possible here), the regression test added, and any
open questions.

## Exit criteria

Done once the root cause is evidence-backed, the fix has been verified
against the reproduction case (or verification is explicitly marked as
not possible here), and a regression test has been added.

## Retry policy

See shared conventions: at most 3 reproduction/isolation attempts with a
genuinely different approach each time (direct run, narrowed input,
added logging); after 3, report what's known and what remains unconfirmed
rather than continuing to guess.

## No hallucination rule

Never invent a stack trace, log line, or root cause that wasn't actually
read. Quote real evidence; state explicitly when evidence is incomplete.

## Error handling

If reproduction fails entirely, say so and ask for more specifics rather
than fabricating a plausible but unconfirmed cause. Present multiple
remaining plausible causes explicitly as alternatives, not as one
certainty.

## Security guidance

Flag security-sensitive paths (auth, input handling) explicitly and
suggest a security-review pass in addition to the fix. Redact real
sensitive data from logs in the write-up.

## Dependencies and limitations

Full confirmation depends on being able to run the reproduction case and
fix here; when not possible, mark the diagnosis as a supported hypothesis.
Intermittent/environment-specific bugs are inherently harder to fully
confirm statically — state the confidence level honestly.
