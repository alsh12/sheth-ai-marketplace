# XML Formatter — reference

## Example

Input:
```xml
<root xmlns:ops="https://example.invalid/ops"><!-- generated --><ops:job id="42"><name>nightly-sync</name><ops:tags><tag>batch</tag><tag>sync</tag></ops:tags></ops:job></root>
```

Output:
```xml
<root xmlns:ops="https://example.invalid/ops">
  <!-- generated -->
  <ops:job id="42">
    <name>nightly-sync</name>
    <ops:tags>
      <tag>batch</tag>
      <tag>sync</tag>
    </ops:tags>
  </ops:job>
</root>
```

Note: the `ops` namespace prefix, the comment, and the attribute `id="42"`
are preserved exactly; only whitespace and line breaks changed.
