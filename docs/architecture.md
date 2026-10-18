# Architecture

Sheth AI Marketplace is organized in four layers:

1. **Catalog** — `.claude-plugin/marketplace.json` at the repo root. Lists
   every plugin, its source path, and marketplace-level metadata (owner,
   description). This is the single entry point a user adds with
   `claude plugin marketplace add`.
2. **Plugins** — `plugins/<name>/`, each with its own
   `.claude-plugin/plugin.json` manifest, `README.md`, and `CHANGELOG.md`.
   Plugins install and version independently of one another; installing
   one does not require installing the others.
3. **Skills** — `plugins/<name>/skills/<skill>/SKILL.md`, each with its
   own `reference.md` for worked examples (progressive disclosure — the
   main file stays lean and is loaded into context on every turn by name
   and description; the full body loads only when the skill is used).
4. **Governance** — the shared conventions, docs, CI, and contribution
   process that keep all plugins and skills consistent: this `docs/`
   directory, `CONTRIBUTING.md`, `SECURITY.md`, the validator in
   `scripts/`, the eval harness in `tests/evals/`, and
   `.github/workflows/validate.yml`.

## Shared conventions

Rules every skill in this marketplace follows (tool-use discipline,
retry policy, no-hallucination rule, severity vocabulary) are centralized
in `docs/shared-conventions.md` and referenced from each `SKILL.md` rather
than repeated inline, to keep per-skill files short.

## Hooks

Optional pre-tool/post-tool checkpoint guidance (and one real, working
example) lives in `docs/hooks.md`. Read that document for the honest
distinction between the real Claude Code hooks mechanism and this
marketplace's own authoring convention layered on top of it.

## Versioning

Each plugin is versioned independently under semver; the policy is in
`docs/versioning.md`.

## Unresolved compatibility questions

These were not fully resolved by the public documentation consulted while
building this marketplace (docs.claude.com / code.claude.com, as of
October 2026) and are noted honestly rather than guessed at:

- The exact minimum Claude Code version required for `skills` arrays using
  the bare `"."` plugin-root form, and for several newer manifest fields
  (e.g., `userConfig.options`, `metadata`), is version-gated per the docs,
  but this repo does not pin or test against a specific Claude Code
  version. Installers on an older Claude Code release may see warnings for
  fields introduced in a later version than they run.
- Whether `claude plugin validate` (the authoritative CLI validator) would
  raise additional warnings beyond what `scripts/validate-marketplace.py`
  checks could not be confirmed in this environment, because the `claude`
  CLI itself was not available to run here. `scripts/validate-marketplace.py`
  is this repo's own structural check (required fields, paths, duplicate
  names, frontmatter) and is not a substitute for running the real
  `claude plugin validate` before publishing.
- The precise behavior of `PreToolUse`/`PostToolUse` hook matchers against
  tool names as used by this marketplace's skills (which invoke tools like
  Read/Write/Grep themselves rather than being invoked as tools) was not
  verified end-to-end in a live Claude Code session; the hook in
  `plugins/sheth-developer-tools/hooks/hooks.json` was verified only by
  running its underlying script directly with sample JSON payloads (see
  `docs/testing.md`), not inside an actual Claude Code tool-use loop.
