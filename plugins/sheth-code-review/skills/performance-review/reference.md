# Performance Review — reference

## Example

```
Likely significant
- reports/builder.py:34 — N+1 query: `for order in orders: order.customer`
  triggers one query per order inside the loop (confirmed by reading the
  ORM's lazy-load behavior for this relation). For the reported typical
  batch size of ~2,000 orders, this is ~2,000 extra queries per report run.
  Prefetching the `customer` relation in the initial query would collapse
  this to one additional query total.

Possibly significant
- search/index.go:88 — linear scan over `allDocuments` inside
  `FindByTag`, O(n) per call. Whether this matters depends on how large
  `allDocuments` grows in practice; no volume data was given here. Worth
  profiling if this path is called per request rather than at startup.

Recommendation: before changing search/index.go:88, get a count of typical
`allDocuments` size and call frequency; the N+1 fix in reports/builder.py
is worth making regardless of exact numbers, since it scales linearly with
a quantity (order count) that is already known to be large.
```
