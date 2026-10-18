---
name: python-development
description: Write and modify Python application code with type hints, clear exception handling, logging, and tests, avoiding unnecessary dependencies. Use when the user is working in a Python codebase and asks to write, change, or review application code.
---

# Python Development

Writes/modifies typed Python code with explicit error handling and
meaningful logging, avoiding unneeded dependencies. See `reference.md` for
a worked example. Shared conventions:
`../../../../docs/shared-conventions.md`.

## Boundaries

- Does not add a dependency the standard library already covers; if one
  genuinely earns its place, say why stdlib isn't sufficient.
- Does not silently use syntax/features beyond the project's declared
  Python version floor — check `pyproject.toml`/CI config first.
- Not for writing test code as the main output (see test-development),
  though code should be written testable (small, injectable, isolated I/O).
- Never suppresses exceptions with a bare `except:`/`except Exception: pass`.

## Workflow

1. Check conventions first: typing style, logging setup, supported Python
   version range. Use Grep to find existing patterns rather than reading
   the whole codebase.
2. Type all new signatures and non-trivial variables, matching the
   codebase's existing typing idiom.
3. Catch specific exception types at each call site, not bare `Exception`,
   unless documented (e.g., a top-level handler that must not crash).
4. Log via the project's existing logger (never `print()`), at a level
   matching the event, with enough context to debug without leaking
   sensitive data.
5. Write for testability: small functions, explicit parameters, I/O
   (network/disk/time/randomness) behind a replaceable seam.
6. Avoid unnecessary dependencies — check stdlib/existing deps first.

## Input contract

A description of the desired behavior, plus access to the relevant
modules, `pyproject.toml`/`requirements.txt`, and existing logging/typing
conventions.

## Output contract

Typed, testable Python code consistent with existing conventions, with a
brief note on any new dependency (or confirmation none was added) and the
exception-handling choices made.

## Exit criteria

Done once new/changed functions are typed, exceptions are handled at the
correct specificity, and no new dependency was added without an explicit
justification note.

## Retry policy

See shared conventions. If the supported Python version can't be
confirmed, state the assumption once rather than guessing differently on
each attempt.

## No hallucination rule

Never claim the code runs or tests pass without actually running them.
State explicitly when that wasn't done in this session.

## Error handling

Distinguish expected absence/failure (return `None`/a result
type/documented exception) from unexpected failure (propagate with full
context, logged once). Never catch-and-reraise a less specific exception
without `raise ... from err`.

## Security guidance

Never build shell commands or SQL via string-formatting untrusted input;
use `subprocess` with an argument list (not `shell=True`) and parameterized
queries. Don't log secrets/tokens/full payloads. Avoid
`eval`/`exec`/`pickle.loads` on untrusted input.

## Dependencies and limitations

Assumes access to the dependency manifest and CI config to confirm the
Python version floor and existing dependencies; state the assumption when
unavailable. Does not run the code/tests itself — recommend doing so
before any correctness claim.
