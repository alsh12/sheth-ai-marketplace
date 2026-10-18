# Security Review — reference

## Example

```
Critical
- api/users.py:61 — SQL injection: `cursor.execute(f"SELECT * FROM users
  WHERE name = '{name}'")` builds a query from the unvalidated `name` query
  parameter accepted at api/routes.py:18. Use a parameterized query instead
  of string interpolation.

High
- config/settings.py:9 — hardcoded database password
  (`DB_PASSWORD = "p@ssw0rd123"`) committed in source. Move to a secret
  manager or environment variable not checked into version control, and
  rotate this credential since it has already been exposed in history.

Scope note: this review covered the files in the diff for the categories
listed above. It is not an exhaustive security audit — dependency
vulnerability scanning and dynamic testing were out of scope and are
recommended as follow-ups.
```
