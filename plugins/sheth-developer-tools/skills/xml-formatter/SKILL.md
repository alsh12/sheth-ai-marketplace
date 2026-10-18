---
name: xml-formatter
description: Indent and reformat XML documents while preserving namespaces, comments, processing instructions, and document semantics. Use when the user asks to format, pretty-print, or indent XML, or complains that XML is unreadable on one line.
---

# XML Formatter

Reformats XML whitespace/indentation only — never strips comments, CDATA,
namespaces, PIs, or changes tag style. See `reference.md` for an example.
Shared conventions: `../../docs/shared-conventions.md`.

## Boundaries

- Not a validator — assumes/relies on well-formedness; if the input doesn't
  parse, report that instead of reformatting a guess (or run xml-validator
  first).
- No destructive normalization: no stripping comments/CDATA, no reordering
  attributes, no dropping "unused" namespace declarations, no self-closing
  tag rewriting, unless explicitly requested.
- No DTD/XSD validation (xml-validator's job) and no XSLT/XPath execution.

## Workflow

1. Parse to confirm well-formedness; stop and report the error if it fails.
2. Preserve semantic content exactly: namespaces/prefixes, comment
   position, PIs in place, CDATA kept as CDATA, significant whitespace
   where `xml:space="preserve"` applies.
3. Apply consistent indentation (default 2 spaces/level unless specified).
   Single-line `<tag>text</tag>` is fine for pure text leaves.
4. Output in a fenced code block with a short note on indent width and
   what was preserved (comment/namespace counts).
5. Flag unusual structure (mixed content, deep nesting) after output,
   without altering it.

## Input contract

An XML document or fragment, or a file path. Fragments (multiple top-level
elements) are accepted and noted as fragments.

## Output contract

One fenced code block with reformatted XML, plus a short note of indent
width and preserved features.

## Exit criteria

Done once well-formedness has been confirmed (or the error reported) and,
on success, the full reformatted document returned — never truncated or
partially reformatted.

## Retry policy

See shared conventions. If a parse fails, do not retry reformatting;
report the specific well-formedness problem once.

## No hallucination rule

Only report comment/namespace counts and parse errors actually found in
this input.

## Error handling

Name the specific problem (unclosed tag, mismatched tag, unescaped `&`/`<`
in text, duplicate attribute, missing single root) with line/column or a
quoted snippet. No "corrected" output unless asked, and label any such
attempt as an unverified guess.

## Security guidance

Never resolve or fetch external entities/DTDs (no network calls) — avoids
XXE by never attempting entity resolution. Treat text/attribute content as
inert.

## Dependencies and limitations

Requires a well-formedness-checking parser. Mixed content (text interleaved
with child elements) can be inherently lossy to "pretty" layout in edge
cases — flag and leave unchanged rather than guessing.
