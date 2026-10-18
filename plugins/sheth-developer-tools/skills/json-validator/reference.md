# JSON Validator — reference

## Example 1: trailing comma

Input:
```json
{
  "id": 7,
  "roles": ["admin", "editor",],
  "active": true
}
```

Output:
```
Invalid JSON: trailing comma after "editor" in the "roles" array, line 3.
JSON does not allow a comma before a closing bracket. Remove the comma
after "editor" to fix it.
```

## Example 2: unquoted keys

Input:
```json
{ name: "ops-team", id: 12 }
```

Output:
```
Invalid JSON: object keys must be double-quoted strings. "name" and "id" on
line 1 are unquoted identifiers, which is valid in JavaScript object
literals but not in JSON.
```
