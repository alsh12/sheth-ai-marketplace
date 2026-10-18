# API Development — reference

## Example

```
POST /v1/orders

Request body:
  { "customer_id": "string (required)",
    "items": "array of { sku: string, qty: integer > 0 } (required, min 1 item)",
    "idempotency_key": "string (required)" }

Auth: bearer token identifying the authenticated customer; customer_id in
  the body must match the authenticated principal, or the request is
  rejected with 403.

Responses:
  201 Created -> { "order_id": "...", "status": "pending" }
  400 Bad Request -> validation error (missing/invalid field), structured
    as { "error": { "code": "invalid_request", "message": "..." } }
  403 Forbidden -> customer_id mismatch
  409 Conflict -> idempotency_key already used with a different body

Idempotency: required via `idempotency_key`; a retried request with the
  same key and body returns the original 201 response rather than creating
  a duplicate order.

Versioning: new endpoint under the existing /v1 prefix; purely additive,
  no breaking change to any existing contract.

Rate limiting: flagged as a write endpoint that creates billable orders;
  recommend the gateway's existing per-customer write-rate limit apply
  here rather than building a bespoke limiter for this endpoint.
```
