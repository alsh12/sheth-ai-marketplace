---
name: pull-request-review
description: Review a pull request against its stated requirements or acceptance criteria, checking test coverage and backward-compatibility risk, and produce a concise blocking/non-blocking summary. Use when the user shares a pull request with a description, linked ticket, or acceptance criteria and asks for a review before merge.
---

# Pull Request Review

Reviews a PR against its stated goal, test coverage, and compatibility
risk, ending in a blocking/non-blocking summary. See `reference.md` for a
worked example. Shared conventions: `../../../../docs/shared-conventions.md`.

## Boundaries

- **Never auto-approves or merges** — produces a recommendation only; the
  decision and action stay with a human/the team's process.
- Not a full line-by-line review (that's code-review) — focus is PR-level:
  does it meet the stated goal, is it tested, is it compatible.
- Never assumes unstated acceptance criteria — say so and scope narrower.

## Workflow

1. Extract stated requirements from the PR description, linked ticket, or
   commit messages. If none exist, say so and narrow the review's scope
   explicitly.
2. Check the diff against each requirement individually.
3. Check test coverage: new/updated tests for new behavior, missing edge
   cases/error paths.
4. Check backward-compatibility risk: changed public APIs, default
   behavior, data formats, removed functionality.
5. Write a concise summary first (blocking count, non-blocking count, one
   sentence on whether the stated goal is met), then the details.
6. Label every finding `Blocking` or `Non-blocking` explicitly.
7. Close with a recommendation phrased as a recommendation, not an
   approval action.

## Input contract

A PR diff plus its description/ticket/acceptance criteria (as much as is
available).

## Output contract

A summary line, then a `Blocking` list and a `Non-blocking` list (each
with file:line where applicable), closed with a recommendation sentence
that stops short of approving or merging.

## Exit criteria

Done once every stated requirement has been checked against the diff and
every finding is labeled Blocking or Non-blocking — not left unclassified.

## Retry policy

See shared conventions. If CI/test results are referenced but not
actually visible, state that once rather than assuming a pass and moving
on.

## No hallucination rule

Never state that CI passed, a test exists, or a requirement is met without
having actually read the diff/tests that confirm it.

## Error handling

If the PR's stated goal and its diff diverge (e.g., unrelated refactor
bundled in), call this out explicitly as scope creep rather than silently
reviewing the unrelated part as in-scope.

## Security guidance

Flag that a dedicated security-review pass is recommended when the PR
touches auth, secrets, or data validation.

## Dependencies and limitations

Review quality depends on how complete the stated requirements are.
Does not execute the test suite or CI itself — confirms coverage by
reading tests, not running them; say that running them is required for a
pass/fail claim (see test-development).
