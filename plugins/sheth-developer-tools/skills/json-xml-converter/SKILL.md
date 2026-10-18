---
name: json-xml-converter
description: Convert data bidirectionally between JSON and XML, explaining model differences and lossy-conversion risks. Use when the user asks to convert JSON to XML, XML to JSON, or asks why a round trip didn't come back the same.
---

# JSON <-> XML Converter

Converts between JSON and XML using a stated, consistent mapping
convention, and always calls out lossy/ambiguous spots. See `reference.md`
for a worked example. Shared conventions:
`../../docs/shared-conventions.md`.

## Boundaries

- Never claims losslessness for arbitrary input — JSON and XML have
  different data models; state this up front.
- Never invents a mapping convention silently when the project already has
  an XML/JSON convention — look for one or ask before picking
  attribute-vs-element/array-wrapping rules.
- Does not validate against a schema as part of conversion (mention
  xml-validator/json-validator as a follow-up instead).
- Never fetches or resolves external DTD/schema references.

## Workflow

1. Confirm the source is valid in its own format first; stop and report if
   not.
2. State the mapping convention being used (attribute vs. element for
   `@`-prefixed keys, array <-> repeated-sibling-element naming, null
   handling, namespace handling) before or alongside output.
3. Apply the convention consistently across the whole document.
4. Call out lossy/ambiguous spots found in *this* input: dropped
   comments/PIs, mixed content, numeric-looking text that could become a
   number, null representation choice, attribute/element ordering.
5. State the round-trip caveat: converting back is not guaranteed to
   reproduce the original, and say why when relevant.

## Input contract

JSON or XML text or a file path, with a stated or inferred target format.

## Output contract

The converted document in a fenced code block, preceded or followed by (a)
the mapping convention used and (b) a short list of lossy/ambiguous
elements actually encountered in this input.

## Exit criteria

Done once the full document has been converted under one consistently
applied convention and every lossy/ambiguous spot actually present has
been called out.

## Retry policy

See shared conventions. If the input mixes conventions inconsistently,
don't silently guess on the first try — ask which convention applies
before (re-)converting.

## No hallucination rule

Only report lossy/ambiguous elements and conventions actually present in
the given input — never claim a conversion is lossless without having
checked for mixed content, nulls, and namespace collisions in this input.

## Error handling

If the source fails to parse, report that instead of a partial conversion.
If conventions are inconsistent in the input, flag it and ask rather than
picking one interpretation silently.

## Security guidance

Never resolve external entities or remote schema references from either
side. Treat all data as inert; never execute embedded content.

## Dependencies and limitations

Requires parsers for both formats. No universal lossless JSON<->XML
mapping exists. Namespace-heavy XML (reused prefixes, multiple prefixes
per URI) is a known hard case — flag rather than silently collapsing.
