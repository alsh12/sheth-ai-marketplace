# JSON <-> XML Converter — reference

## Example

Input (JSON):
```json
{
  "job": {
    "@id": "42",
    "name": "nightly-sync",
    "tags": ["batch", "sync"]
  }
}
```

Convention: keys prefixed with `@` become XML attributes; arrays become
repeated sibling elements named after the singular of the array key
(`tags` -> `tag`).

Output (XML):
```xml
<job id="42">
  <name>nightly-sync</name>
  <tags>
    <tag>batch</tag>
    <tag>sync</tag>
  </tags>
</job>
```

Note: no mixed content or nulls were present, so this specific conversion
is round-trip-safe under the stated convention — that is not true in
general.
