# Contributing

## Add a skill to an existing plugin

See `docs/adding-a-skill.md`.

## Add a new plugin

See `docs/adding-a-plugin.md`.

## Update the marketplace catalog

Edit the `plugins` array in `.claude-plugin/marketplace.json`: each entry
needs a unique `name`, a `source` path, a `description`, and a `version`
matching that plugin's own `plugin.json`. Run the validator afterward.

## Validate manifests

```
python scripts/validate-marketplace.py
```

Add `--only <plugin-name>` while a plugin is still under construction.

## Run tests locally

```
python -m unittest discover tests
python tests/evals/run_evals.py
```

See `docs/testing.md` for what each one actually checks and its honest
scope (the eval harness checks fixture ground truth and mechanical
invariants, not live model output).

## Update changelogs and versions

See `docs/versioning.md` for the semver rules (patch/minor/major) and the
requirement that every version bump has a changelog entry.

## Prepare a release

See `docs/publishing.md`.

## Diagnose install/discovery failures

- Run `python scripts/validate-marketplace.py` first — most structural
  problems (missing fields, bad paths, duplicate names) surface there.
- Confirm the plugin's `source` path in `marketplace.json` starts with
  `./` and actually resolves to a directory containing
  `.claude-plugin/plugin.json`.
- Confirm every skill directory under `skills/` has a `SKILL.md` whose
  frontmatter starts on line 1 with `---` and includes `name` and
  `description`.
- If a skill isn't being picked up automatically, check that its
  `description` states when to use it, not just what it does — that's
  what Claude matches against.
- For anything the validator doesn't catch, run the real
  `claude plugin validate <path>` from your shell, which is the
  authoritative check (see `docs/publishing.md`).

## Style

- Keep `SKILL.md` files lean (roughly 60-150 lines); move worked examples
  to that skill's `reference.md`.
- Don't repeat tool-use/retry/no-hallucination boilerplate per skill —
  reference `docs/shared-conventions.md` instead.
- Never claim a test, validation, or eval result that wasn't actually
  produced by running it.
