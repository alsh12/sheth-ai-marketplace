# Versioning and compatibility policy

Each of the three plugins is versioned independently under semver
(`MAJOR.MINOR.PATCH`), tracked in its own `.claude-plugin/plugin.json`
`version` field and its own `CHANGELOG.md`.

## What counts as which bump

- **Patch** (`1.0.0` -> `1.0.1`): wording/instruction clarifications
  within a skill's `SKILL.md` or `reference.md` that do not change what
  the skill is supposed to do or what it promises in its Input/Output
  contract — e.g., a clearer error-handling example, a typo fix, a
  tightened boundary statement that matches existing behavior.
- **Minor** (`1.0.0` -> `1.1.0`): a new capability that is additive and
  non-breaking — e.g., a new skill added to an existing plugin, a new
  optional input the skill now accepts, a new documented output field
  that doesn't remove or change the meaning of an existing one.
- **Major** (`1.0.0` -> `2.0.0`): a change that changes behavior a
  consumer could already be relying on — e.g., a skill's output contract
  changes shape, a default behavior changes, a skill or plugin is
  renamed or removed, an input that used to be optional becomes
  required.

## Changelog is required per bump

Every version bump, of any size, adds an entry to that plugin's
`CHANGELOG.md` describing what changed and why it's that size of bump.
A version bump without a changelog entry is treated as incomplete.

## Marketplace catalog pins consumers to a version

`marketplace.json`'s plugin entries set a `version` field that mirrors
each plugin's own `plugin.json` version. A user who has already installed
a plugin is not silently moved to a newer version when the catalog
changes — upgrading is an explicit, opt-in action
(`claude plugin update <name>` or the `/plugin` UI), the same as for any
other Claude Code plugin. This marketplace does not set
`forceRemoveDeletedPlugins` or otherwise attempt to push changes onto
existing installs.

## Release checklist

1. Make the change; classify it as patch/minor/major per the rules above.
2. Bump `plugins/<name>/.claude-plugin/plugin.json` `version`.
3. Add a `CHANGELOG.md` entry under that plugin.
4. Update the matching `version` in the root `marketplace.json` entry.
5. Run the gates in `docs/testing.md` (validator, unit tests, evals, and
   the manual-review checklist for any touched skill) — do not publish a
   bump whose eval fixtures fail.
