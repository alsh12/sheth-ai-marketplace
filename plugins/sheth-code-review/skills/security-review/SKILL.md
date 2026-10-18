---
name: security-review
description: Review code changes for security weaknesses such as auth gaps, injection, unsafe deserialization, secret exposure, and risky dependencies. Use when the user asks for a security review, threat check, or vulnerability scan of code, or mentions auth, secrets, or injection concerns.
---

# Security Review

Reviews code for concrete security weaknesses by category, never claiming
exhaustive coverage. See `reference.md` for a worked example. Shared
conventions: `../../../../docs/shared-conventions.md`.

## Boundaries

- **Never claims a complete security guarantee** — state the review covers
  what was reviewable, not an exhaustive audit; recommend dependency
  scanning/dynamic testing/pen testing for anything out of reach.
- No live exploits, fuzzers, or scanners — manual code read only.
- Never fabricates a CVE status for a dependency — say a vulnerability
  database check is needed instead.
- Does not modify code unless explicitly asked.

## Workflow

1. Establish scope and trust boundaries (what's user-controlled vs.
   trusted).
2. Check systematically: auth/authz, injection, input validation, secrets,
   deserialization, sensitive data exposure, dependency risk. Mark "not
   applicable" rather than skipping silently. Use Grep to find sinks
   (query builders, shell calls, deserializers) rather than reading every
   file in full.
3. Classify severity: `critical` / `high` / `medium` / `low` /
   `informational`.
4. Cite exact location; trace data flow from untrusted source to sink when
   possible.
5. Suggest a concrete mitigation direction, not applied unless asked.
6. Close with an explicit scope statement (what was/wasn't reviewed).

## Input contract

A diff, PR, or set of files, ideally noting what's user-facing/externally
reachable.

## Output contract

Findings grouped by severity, each with location, category, a data-flow
trace when relevant, and a mitigation direction; closed with an explicit
"not an exhaustive audit" scope note.

## Exit criteria

Done once every applicable category in Workflow step 2 has been checked
(or explicitly marked not applicable) and the closing scope statement
accurately reflects what was reviewed.

## Retry policy

See shared conventions. If a data flow can't be traced because a function
is out of view, say so once rather than guessing the sink is safe.

## No hallucination rule

Never assert a CVE, a specific vulnerability database result, or an
exploit outcome that wasn't actually checked. Report only what was read in
the given files.

## Error handling

State explicitly when a finding is unconfirmed ("might be reachable from
an unauthenticated route, but routing config isn't in view") and what
would confirm it.

## Security guidance

Never reproduce a full secret value in a finding — reference its location
and redact/truncate it. Never attempt to exploit an identified weakness
against a live system.

## Dependencies and limitations

Manual/static review only — cannot detect runtime-only issues (timing
attacks, infra misconfiguration) without seeing that code/config.
Confidence in "no issues found" is bounded by what was actually in view.
