---
name: xml-validator
description: Check whether XML is well-formed, and optionally validate it against a provided DTD or XML Schema. Use when the user asks to validate or lint XML, or check it against a schema or DTD they supply.
---

# XML Validator

Checks well-formedness always, and schema/DTD conformance only when the
user supplies the schema/DTD content. See `reference.md` for an example.
Shared conventions: `../../docs/shared-conventions.md`.

## Boundaries

- Never fetches a remote DTD, XSD, or external entity — external DTD/schema
  references are reported as present but never resolved or expanded
  (eliminates XXE by construction).
- Does not reformat (xml-formatter's job).
- Schema validation only runs against schema/DTD content the user actually
  provides — never assume or fabricate one.
- No Relax NG/Schematron support unless the user supplies separate tooling.

## Workflow

1. Check well-formedness first, always.
2. If not well-formed: report the specific problem and location, and stop
   — do not attempt schema validation on broken markup.
3. If well-formed, no schema supplied: report "well-formed" and explicitly
   note no schema/DTD was checked.
4. If well-formed and a schema/DTD was supplied: validate structure,
   types, and cardinality; report every violation (not just the first)
   with an element path and the specific rule violated.

## Input contract

An XML document (text or file path), and optionally a DTD or XSD (text or
file path).

## Output contract

`Well-formed.` / `Not well-formed: <reason> at line X.`, plus, if a schema
was supplied, `Valid against schema.` or a list of
`<element path>: <violation>` entries. Always states whether schema
validation was performed.

## Exit criteria

Done once well-formedness is determined and, when a schema was supplied,
every schema violation found has been reported — not just the first.

## Retry policy

See shared conventions. A malformed document is reported once, not
re-parsed repeatedly with different assumptions.

## No hallucination rule

Report only violations and line locations actually found by checking
against the exact supplied schema/document — never invent a rule or
assume a schema that wasn't given.

## Error handling

Name the specific well-formedness problem, or the specific schema rule
violated and the exact element/attribute path. If the supplied schema
itself is malformed, say so distinctly from a document violation.

## Security guidance

Never resolve external entities, external DTDs, or remote `schemaLocation`
URLs — a hard rule. Flag unusually large/recursive internal entity
definitions (e.g., "billion laughs" pattern) rather than expanding them.

## Dependencies and limitations

Requires a well-formedness parser with external entity resolution disabled,
and a DTD/XSD validator for the optional step. Namespace mismatches between
schema and document are reported as validation failures, not ignored.
