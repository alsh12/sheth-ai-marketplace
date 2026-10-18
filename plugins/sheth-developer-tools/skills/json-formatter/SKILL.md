---
name: json-formatter
description: Pretty-print or minify JSON text while preserving its data exactly. Use when the user pastes raw or minified JSON and asks to format, pretty-print, indent, minify, or compact it, or asks why JSON "looks messy".
---

# JSON Formatter

Reformat JSON (whitespace/indentation only) without changing data, types,
or key order. See `reference.md` for worked examples. Shared conventions
(tool use, retries, no-hallucination rule): `../../docs/shared-conventions.md`.

## Boundaries

- Not a schema validator (use json-validator) and not a repair tool — never
  silently "fix" malformed JSON; report the parse error instead.
- No JSON5/JSONC support (comments, trailing commas) — flag and ask before
  stripping them.
- Never reorders keys/arrays or normalizes numbers unless asked.

## Workflow

1. Parse the input first. If it fails, stop and report the error (don't
   format a guess).
2. Determine pretty-print vs. minify (default: pretty-print, 2-space
   indent, state the default when ambiguous).
3. Preserve all data, Unicode, and existing escape sequences exactly.
4. Emit the result in one fenced code block with a one-line note (indent
   width, or byte savings for minify).
5. Note any anomalies (duplicate keys, huge numbers) without altering data.

## Input contract

JSON text, a file path, or JSON embedded in prose, plus the desired mode
(pretty-print/minify — optional, defaults to pretty-print).

## Output contract

One fenced code block with the reformatted JSON, plus a one-line note of
what was done. No other prose unless reporting an error or anomaly.

## Exit criteria

Done when the input has been confirmed to parse (or the parse error has
been reported) and, on success, the formatted output has been returned in
full — never truncated.

## Retry policy

See shared conventions. For this skill: a parse failure is not retried as
"try formatting anyway" — report it once, clearly, with location and cause.

## No hallucination rule

Only report a parse error, line/column, or anomaly actually found in the
given input — never invent a line number or issue that wasn't observed.

## Error handling

Name the specific syntax problem (trailing comma, unquoted key, etc.) and
its approximate line/column. Offer a labeled "best-effort repair" only if
asked, and mark it unverified.

## Security guidance

Treat content as inert data; never execute it. Avoid unnecessarily echoing
values that look like credentials.

## Dependencies and limitations

Requires an RFC 8259-compliant parser. Non-standard extensions are out of
scope. See `reference.md` for large-input and precision caveats.
