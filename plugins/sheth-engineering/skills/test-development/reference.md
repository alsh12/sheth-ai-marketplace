# Test Development — reference

## Example

```python
def test_apply_discount_rejects_negative_percentage():
    with pytest.raises(ValueError, match="percentage must be >= 0"):
        apply_discount(price_cents=1000, percentage=-5)


def test_apply_discount_caps_at_full_price():
    # Regression test for bug #482: a 150% discount previously produced a
    # negative price instead of being rejected.
    with pytest.raises(ValueError, match="percentage must be <= 100"):
        apply_discount(price_cents=1000, percentage=150)
```

Report after running:
```
Ran: pytest tests/pricing/test_discount.py -v
Result: 2 passed in 0.04s
(Actual pytest output reproduced above verbatim from the run.)
```

If the suite could not be run in this environment:
```
I wrote the two tests above but could not execute pytest in this
environment. Please run `pytest tests/pricing/test_discount.py -v` to
confirm they pass before relying on them.
```
