# Testing

This repo has two independent, stdlib-only checks and one eval harness.
All three are run with plain `python`; none require installing anything.

## 1. Structural validator

```
python scripts/validate-marketplace.py
```

Checks `marketplace.json` and every `plugin.json` for required fields,
unique plugin ids, resolvable source paths, and every skill's `SKILL.md`
for parseable frontmatter with `name`/`description`, plus no duplicate
skill names within a plugin. Exits non-zero with a clear message list on
any failure. Use `--only <plugin-name>` to restrict deep checks to one
plugin while others are still under construction.

This is this repo's own check, not a substitute for the real
`claude plugin validate` CLI command, which should also be run before
publishing (see `docs/publishing.md`) — it was not available in the
environment this repo was built in, so it has not been run here.

## 2. Unit tests

```
python -m unittest discover tests
```

Exercises the validator itself against good and bad fixtures (`tests/
test_validate_marketplace.py`), plus one test that runs it against this
actual repository.

## 3. Eval harness (`tests/evals/`)

```
python tests/evals/run_evals.py
```

Each skill has a fixture (`tests/evals/<plugin>/<skill>.json`) shaped as
`{skill, input, expected_behavior_description, pass_criteria}`. Each
`pass_criteria` entry is either:

- **Mechanically checkable** (`"check": "<name>"`): `run_evals.py`
  actually verifies it against the fixture's `input` using real parsers
  (e.g., confirms an "invalid JSON" fixture really fails to parse, or
  that formatting a JSON value and reparsing it yields an equal value).
- **`"requires_manual_review": true`**: a judgment call about a live
  skill run's output (e.g., "the explanation is clear", "the mapping
  convention was stated") that this harness does not and cannot check
  automatically — it is listed as requiring manual review, never silently
  marked as passing.

**Honest scope**: this harness does not invoke Claude or run any skill's
actual instructions — there is no offline mechanism here to do that. It
verifies the fixtures' own ground truth (so a fixture can't silently test
the wrong thing) and gives a human reviewer, or a future live-session eval
runner, a structured list of what to check by hand.

### How evals gate a release

Before bumping a plugin's version (see `docs/versioning.md`):

1. Run the structural validator and unit tests; both must pass.
2. Run `tests/evals/run_evals.py`; every mechanically-checkable criterion
   must pass (non-zero exit blocks the release).
3. Manually walk through every `requires_manual_review` criterion for any
   skill touched by the change, in a live Claude Code session, before
   publishing. This step is not automated and must not be skipped or
   claimed as done without actually doing it.

## What was actually run building this repo

`python -I scripts/validate-marketplace.py`,
`python -I -m unittest discover tests -v`, and
`python -I tests/evals/run_evals.py` were all actually executed against
this repository; see the final build report for their real output. The
`-I` flag isolates the interpreter from the current/script directory so a
planted same-named module can't shadow a stdlib import.
