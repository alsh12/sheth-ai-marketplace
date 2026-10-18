---
name: test-development
description: Write unit, integration, and regression tests that are deterministic and isolated, and only report a test as passing after actually running it. Use when the user asks to write tests, add test coverage, write a regression test for a bug, or asks whether tests pass.
---

# Test Development

Writes deterministic, isolated tests and reports pass/fail only from an
actual run. See `reference.md` for a worked example. Shared conventions:
`../../../../docs/shared-conventions.md`.

## Boundaries

- **Never claims a test passed without running it.** If the suite can't be
  executed here, say so plainly and give the command to run instead.
- **Never changes production behavior just to make a test pass**, and
  never weakens an assertion to get a green run unless the assertion
  itself was wrong.
- Never writes intentionally flaky tests (real time/network/unseeded
  randomness/order dependence) — treat as bugs in the test.
- Does not duplicate existing coverage without reason — check first
  (Grep for the behavior/function name in the test directory).

## Workflow

1. Understand the specific behavior under test. For a regression test,
   confirm the original bug (input -> wrong output) first.
2. Design for determinism/isolation: fake time/randomness/network/disk;
   no shared mutable state or execution-order dependence; no real sleeps.
3. Write the test using the project's existing framework/conventions.
4. Cover the primary behavior, meaningful edge cases, and — for a
   regression test — the exact previously-failing scenario.
5. Actually run the test suite (or the new/changed tests) with the
   project's real test command.
6. If a test fails, diagnose whether the bug is in the code or the test,
   and say which, with reasoning.
7. Report precisely: command used, and the actual pass/fail/error output
   — never a generic "tests pass."

## Input contract

The behavior or bug to cover, plus access to the codebase and its test
runner/configuration.

## Output contract

New/modified test code, plus a report of having run it (command + actual
result) — or, if running wasn't possible, an explicit statement that it's
unverified plus the command the user should run.

## Exit criteria

Done once the written test(s) have actually been executed and the real
outcome (pass/fail/error, with output) has been reported — never when a
test merely "looks correct."

## Retry policy

See shared conventions. If a test fails on first run, don't rewrite it
blindly 3 times — diagnose (test bug vs. code bug) before the next
attempt, and stop after 3 attempts to report the unresolved failure.

## No hallucination rule

Never report a pass/fail result, test count, or command output that
wasn't actually produced by running the suite in this session.

## Error handling

On a new test failing, re-check the test's own setup/assertion before
re-checking the code under test; state which was wrong. Report a newly
broken existing test as a potential regression, not something to silently
adjust.

## Security guidance

Don't commit real credentials/production data into fixtures — use fake
values. Don't make real calls to external/production services from tests.

## Dependencies and limitations

Requires the project's test runner to actually be invocable here for a
real result; say so when it isn't available. Unit-test coverage alone
doesn't guarantee integration-level correctness — say when an
integration/end-to-end test is actually needed.
