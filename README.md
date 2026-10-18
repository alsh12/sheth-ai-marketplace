# Sheth AI Marketplace

A Claude Code plugin marketplace from Sheth Hub: three independently
installable plugins covering structured-data developer tools, code
review, and software engineering workflows.

## Design principles

- **Independently installable.** Each plugin stands alone; installing one
  never requires or assumes another is also enabled.
- **No silent repair or silent guessing.** Formatting/validation skills
  report problems instead of quietly "fixing" malformed input; engineering
  skills state assumptions and compatibility caveats explicitly.
- **No fabricated results.** No skill in this marketplace claims a test
  passed, a build succeeded, or a security review was exhaustive unless
  that was actually verified. See each skill's "No hallucination rule."
- **Lean, structured skills.** Every `SKILL.md` states its Input contract,
  Output contract, Exit criteria, Retry policy, and No-hallucination rule
  explicitly, with worked examples kept in a separate `reference.md` so
  the main instructions stay short and scannable.
- **No network calls from skill instructions.** Nothing here fetches a
  remote schema, DTD, or URL as part of doing its job.

## Plugin catalog

| Plugin | Description |
| :- | :- |
| `sheth-developer-tools` | JSON/XML formatting, validation, and bidirectional conversion. |
| `sheth-code-review` | Severity-ranked code, security, performance, and pull-request review. |
| `sheth-engineering` | .NET, Python, API design, test development, and debugging workflows. |

## Skills by plugin

**sheth-developer-tools**: `json-formatter`, `json-validator`,
`xml-formatter`, `xml-validator`, `json-xml-converter`.

**sheth-code-review**: `code-review`, `security-review`,
`performance-review`, `pull-request-review`.

**sheth-engineering**: `dotnet-development`, `python-development`,
`api-development`, `test-development`, `debugging`.

## Installation and usage

Add this marketplace, then install any plugin by name — each installs and
updates independently:

```
claude plugin marketplace add <path-or-url-to-this-repo>
claude plugin install sheth-developer-tools@sheth-ai-marketplace
```

A plugin's skills become available as `/plugin-name:skill-name`, and
Claude can also invoke them automatically when a request matches a
skill's description. See `docs/installation.md` for scopes and local
development without installing.

## Contributing

See `CONTRIBUTING.md` for how to add a skill, add a plugin, update the
catalog, validate manifests, and run tests locally.

## Security and privacy

See `SECURITY.md`. In short: no network calls, no telemetry, no remote
schema/entity fetching, and a disclosure process for anything found.

## Versioning and releases

Each plugin is versioned independently under semver, with a required
changelog entry per bump and opt-in upgrades for existing installs. See
`docs/versioning.md` and `docs/publishing.md`.

## Roadmap

Future plugin ideas — not commitments — are listed in `docs/roadmap.md`.

## Architecture and hooks

The catalog/plugins/skills/governance layering is documented in
`docs/architecture.md`. Optional pre-tool/post-tool checkpoint guidance,
and one minimal real working example, is documented in `docs/hooks.md`.

---

https://shethhub.com
