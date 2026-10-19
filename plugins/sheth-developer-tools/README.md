# Sheth Developer Tools

Structured-data utilities for JSON and XML. Five independent skills for
formatting, validating, and converting between the two formats — each one
explicit about what it will and will not silently change.

## Install

```
/plugin install sheth-developer-tools --marketplace alsh12/sheth-ai-marketplace
```

## Skills

| Skill | What it does |
| :- | :- |
| `json-formatter` | Pretty-print or minify JSON without changing data. |
| `json-validator` | Check JSON syntax validity and explain failures. |
| `xml-formatter` | Indent XML while preserving namespaces, comments, PIs. |
| `xml-validator` | Check XML well-formedness, optionally validate against a supplied DTD/XSD. |
| `json-xml-converter` | Convert JSON to XML and back, explaining lossy spots. |

## Design principles

- Never silently repair malformed input — report the problem instead.
- Never make network calls (no remote schema/DTD/entity fetching).
- State the convention or default used whenever one had to be chosen.
- Never claim a conversion is lossless without checking the specific input.

See each skill's `SKILL.md` for its input/output contract, and its
`reference.md` for worked examples. Shared conventions used across every
skill in this plugin live in `docs/shared-conventions.md`.


Check more details at https://shethhub.com