# Pull Request Review — reference

## Example

```
Summary: 1 blocking, 2 non-blocking. The PR implements the stated
requirement (reject orders over the configured credit limit) but is
missing a test for the exact-limit boundary case.

Blocking
- tests/orders/test_credit_limit.py — no test covers the boundary case
  (order amount exactly equal to the credit limit). The acceptance
  criteria ("reject orders exceeding the limit") implies amounts equal to
  the limit should be allowed; this isn't verified anywhere.

Non-blocking
- orders/service.py:77 — the new `credit_limit` parameter has no docstring;
  worth adding for discoverability.
- CHANGELOG.md — not updated for this user-facing behavior change; consider
  adding an entry.

Recommendation: add the boundary-case test before merging; the docstring
and changelog items can be follow-ups if the team prefers to merge first.
```
