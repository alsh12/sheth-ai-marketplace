---
name: performance-review
description: Review code for algorithmic inefficiency, excess allocation, and unnecessary database or network calls, distinguishing measured from theoretical impact. Use when the user asks for a performance review, flags something as slow, or wants to know if a change could cause a regression under load.
---

# Performance Review

Reviews code for algorithmic, allocation, and I/O inefficiency, labeling
every claim measured or theoretical. See `reference.md` for a worked
example. Shared conventions: `../../../../docs/shared-conventions.md`.

## Boundaries

- Never claims a specific speed improvement without a benchmark; label any
  number as measured (with the measurement) or estimated (with the
  complexity-class reasoning).
- Does not recommend optimizing a path confirmed to be cold (rare,
  non-latency-sensitive) — deprioritize and say why.
- Does not apply changes unless explicitly asked.
- Does not replace load testing/profiling — recommends it when static
  analysis can't settle the question.

## Workflow

1. Identify hot paths (frequently called / latency-sensitive) vs. cold
   ones; focus there.
2. Check systematically: algorithmic complexity, allocations, database
   calls (N+1), network calls (serial-in-loop, missing caching/batching).
3. Label each finding measured (cite the benchmark/metric given) or
   theoretical (cite the complexity-class reasoning) — never blend the two
   without saying which is which.
4. Classify impact plausibility: `likely significant` / `possibly
   significant` / `probably negligible`.
5. Recommend profiling explicitly when evidence is insufficient to settle
   impact, rather than guessing.

## Input contract

Code, a diff, or a described hot path, ideally with expected scale
(request volume, data size) and any existing measurements.

## Output contract

Findings grouped by impact plausibility, each with location, the specific
inefficiency, measured/theoretical label, and a suggested direction;
closed with a note on what further measurement would raise confidence.

## Exit criteria

Done once every identified hot-path candidate has an impact-plausibility
label backed by either a cited measurement or a stated complexity-class
rationale.

## Retry policy

See shared conventions. If scale/volume data needed to judge impact is
missing, state exactly what number is needed — don't guess a worst/best
case and don't ask the same way twice.

## No hallucination rule

Never invent a benchmark number, profiler reading, or production metric
that wasn't actually supplied. Clearly separate what was measured from
what is estimated.

## Error handling

If a suspected inefficiency turns out, on closer reading, to already be
mitigated (e.g., an existing cache), retract the finding rather than
leaving it in the output.

## Security guidance

Flag when a proposed performance fix (e.g., caching) could introduce a
security issue (e.g., cross-user cache key collision) as a cross-cutting
concern.

## Dependencies and limitations

Static review identifies complexity-class issues and obvious N+1/I/O
patterns but cannot measure actual latency/throughput/memory without
running the code — say so and recommend profiling/load testing for any
impact claim.
