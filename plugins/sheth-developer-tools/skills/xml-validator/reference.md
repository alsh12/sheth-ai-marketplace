# XML Validator — reference

## Example

Input XML:
```xml
<order id="A1"><item qty="3">Widget</item><item qty="-1">Gadget</item></order>
```

Input XSD (user-supplied, simplified):
```xml
<xs:element name="item">
  <xs:complexType>
    <xs:attribute name="qty" type="xs:positiveInteger"/>
  </xs:complexType>
</xs:element>
```

Output:
```
Well-formed: yes.
Validated against the supplied schema: yes.
Violations:
- /order/item[2]: attribute "qty" = "-1" is not a valid xs:positiveInteger
  (must be >= 1).
```
