# JSON Formatter — reference

## Example

Input:
```json
{"user":{"id":42,"name":"Priya Natarajan","tags":["lead","ops"],"active":true,"note":"café visit — follow up"}}
```

Pretty-printed (2-space indent):
```json
{
  "user": {
    "id": 42,
    "name": "Priya Natarajan",
    "tags": [
      "lead",
      "ops"
    ],
    "active": true,
    "note": "café visit — follow up"
  }
}
```

Minified:
```json
{"user":{"id":42,"name":"Priya Natarajan","tags":["lead","ops"],"active":true,"note":"café visit — follow up"}}
```

## Large input / precision notes

- Extremely large inputs (hundreds of MB) may need chunked processing; say
  so rather than silently dropping data.
- Integers beyond IEEE-754 double range are preserved as text where
  possible, but downstream consumers may still lose precision — mention
  this when very large integers are present.
