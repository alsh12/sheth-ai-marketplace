# Python Development — reference

## Example

```python
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class OrderSummary:
    order_id: int
    total_cents: int
    status: str


def load_order_summary(order_id: int, repo: "OrderRepository") -> OrderSummary | None:
    """Return the order summary, or None if the order does not exist."""
    try:
        row = repo.fetch_order(order_id)
    except OrderRepository.ConnectionError:
        logger.error("could not reach order store for order_id=%s", order_id)
        raise

    if row is None:
        logger.info("order_id=%s not found", order_id)
        return None

    return OrderSummary(order_id=row.id, total_cents=row.total_cents, status=row.status)
```

Note: `repo` is passed in rather than constructed inside the function, so a
test can supply a fake `OrderRepository`; the specific
`OrderRepository.ConnectionError` is caught and logged (not swallowed) and
re-raised, rather than a bare `except Exception`; a missing order is a
normal, expected case (`None`) rather than an exception.
