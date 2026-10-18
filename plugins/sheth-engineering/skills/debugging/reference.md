# Debugging — reference

## Example

```
Reported: intermittent 500 errors on POST /orders under load.

Evidence: stack trace shows
  System.InvalidOperationException: Nullable object must have a value.
    at OrderService.CalculateTotal() in OrderService.cs:line 52
Reading OrderService.cs:45-55 shows `discount.Value` is accessed without
checking `discount.HasValue`, where `discount` is a `decimal?` populated
from a cache lookup at line 40 that returns null on a cache miss.

Hypothesis: under load, the cache has a higher miss rate (cache eviction
under memory pressure), so the null path is hit more often than in normal
testing, explaining the "intermittent under load" pattern specifically.

Confirmation: added a temporary log at line 40 showing cache misses
correlate with the reported error timestamps in the provided log excerpt.

Fix: added the missing `discount.HasValue` check at OrderService.cs:52,
defaulting to zero discount on a cache miss rather than throwing.

Verification: re-ran the reproduction script with the cache artificially
forced to miss on every call; previously threw on every request, now
returns 200 with discount = 0 as expected.

Regression test added: test_calculate_total_handles_cache_miss
(tests/orders/test_order_service.py), simulating a cache miss directly.

Open question: I haven't confirmed why the cache's eviction rate increases
specifically under this load pattern — that's a separate capacity/tuning
question beyond this bug fix.
```
