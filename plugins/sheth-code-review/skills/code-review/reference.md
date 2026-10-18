# Code Review — reference

## Example

```
Blocking
- auth/session.py:142 — confirmed: `expires_at` is compared with `<` instead
  of `<=`, so a session is treated as valid exactly at its expiry instant,
  reintroducing the off-by-one this function was refactored to fix (see
  test at auth/test_session.py:88, which doesn't cover the exact-expiry
  case).

Should-fix
- orders/service.rb:57 — possible: `Order.find(id)` will raise
  `RecordNotFound` on a missing id; the caller at
  controllers/orders_controller.rb:23 doesn't rescue it, so a bad id
  returns a 500 instead of a 404. Worth checking how this path is reached.

Nits
- utils/format.go:14 — `formatAmount` and `formatPrice` are near-duplicates;
  consider consolidating.

Summary: 1 blocking, 1 should-fix, 1 nit. Overall risk: medium — the
session-expiry bug should be fixed before merge.
```
