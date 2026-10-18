---
name: code-review
description: Review a code change or diff for bugs, regressions, maintainability, and compatibility risk, with severity-ranked findings tied to file and line. Use when the user shares a diff, branch, or set of files and asks for a general review, not specifically a security or performance review.
---

# Code Review

Reviews a diff for correctness, regressions, maintainability, and
compatibility risk. See `reference.md` for a worked example. Shared
conventions (severity vocabulary, tool use, retries, no-hallucination):
`../../../../docs/shared-conventions.md`.

## Boundaries

- Does not edit source files unless explicitly asked; reports findings only.
- Does not replace security-review/performance-review for deep analysis in
  those areas — mention obvious issues briefly, suggest the dedicated skill.
- Does not approve, merge, or make a ship/no-ship call.
- Does not invent requirements when intent is unclear — say what's unclear.

## Workflow

1. Establish scope: review the diff, not the whole file, unless asked
   otherwise. Use Grep/Glob to locate call sites or related tests rather
   than reading whole files.
2. Read for intent (commit message, PR description, tests) before flagging
   deviations from it.
3. Check systematically: logic errors, regressions, error handling,
   maintainability, backward compatibility.
4. Classify each finding `blocking` / `should-fix` / `nit` (see shared
   conventions); lead with blocking.
5. Cite exact `path:line`; label each finding `confirmed:` or `possible:`.
6. Summarize: counts per severity + one-sentence overall risk.

## Input contract

A diff, PR reference, set of changed files, or a directory with stated
scope.

## Output contract

Findings grouped by severity, each with file:line, one-line description,
confirmed/possible label, optional one-line fix direction (not applied
unless asked); closed with a count summary and overall risk sentence.

## Exit criteria

Done once every changed file in scope has been checked against all five
categories in Workflow step 3, and the summary counts match the findings
actually listed.

## Retry policy

See shared conventions. If a called function or test referenced by the
diff isn't available, don't guess its behavior — say what's missing once.

## No hallucination rule

Only report file:line locations and behaviors actually read in the
provided diff/files. Never state a test exists, passes, or covers a case
without having read that test.

## Error handling

Say exactly what's missing when context (e.g., a called function) isn't
provided. For generated/vendored code, scope the review to non-generated
parts and say so.

## Security guidance

Flag any apparent committed credential/secret immediately regardless of
severity tier. Suggest a dedicated security-review pass for auth,
parsing, or deserialization changes.

## Dependencies and limitations

Static review only — no code execution, test running, or profiling.
Findings about runtime behavior are inferred, not observed; label them as
such. Confidence depends on how much surrounding context was available.
