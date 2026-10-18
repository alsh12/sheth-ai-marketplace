# Security Policy

## Scope

This repository is a Claude Code plugin marketplace: static instruction
files (`SKILL.md`), JSON/Markdown manifests, a stdlib-only Python
validator and eval runner, and one minimal, original hook script. There
is no server, no database, and no code that runs with elevated privileges
beyond what Claude Code itself grants a plugin.

## Out of scope / explicitly not done

- **No network calls**: no skill in this marketplace fetches a remote
  schema, DTD, external entity, or URL as part of its own instructions.
  The validator and eval runner are offline, stdlib-only scripts.
- **No telemetry**: nothing in this repository collects, transmits, or
  stores usage data about anyone who installs these plugins.
- **No remote schema/DTD fetching**: the `xml-validator` and
  `json-xml-converter` skills explicitly document that external
  entities/schemas are never resolved, to avoid XXE-style risks by
  construction.
- **No secrets are stored in this repository.**

## Supported versions

Only the latest published version of each plugin (`sheth-developer-tools`,
`sheth-code-review`, `sheth-engineering`) is supported. See each plugin's
`CHANGELOG.md` for its current version and `docs/versioning.md` for the
upgrade policy — upgrades are opt-in, so an older installed version keeps
working until a user explicitly updates.

## Reporting a vulnerability

Email **security@shethhub.com** with a description of the issue and, if
possible, steps to reproduce it. Please do not open a public issue for a
security report until it has been triaged.

We aim to acknowledge reports within a reasonable timeframe and will
credit reporters who want credit once a fix is published.
