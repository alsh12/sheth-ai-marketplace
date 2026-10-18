---
name: api-development
description: Design or implement REST APIs covering request validation, authentication, error responses, pagination, versioning, documentation, idempotency, and rate limiting. Use when the user asks to design, add, or change an HTTP API endpoint or its contract.
---

# API Development

Designs/implements REST endpoints with a complete contract: validation,
auth, errors, pagination, versioning, idempotency, rate-limit awareness.
See `reference.md` for a worked example. Shared conventions:
`../../../../docs/shared-conventions.md`.

## Boundaries

- Matches the project's existing versioning/auth scheme rather than
  picking a new one unilaterally; flag introducing a new one explicitly.
- Does not build rate-limiting infrastructure as a side effect of one
  endpoint — note where it applies, defer enforcement to existing
  middleware/gateway.
- Not for GraphQL/gRPC contracts — say so and confirm REST is wanted.
- Never silently breaks an existing endpoint's response shape — call out
  the break and a migration path.

## Workflow

1. Define the resource and HTTP method/path (REST nouns + verbs, or match
   the project's existing convention).
2. Specify request validation (required/optional, types, formats) and
   confirm invalid input yields a structured 4xx, not a 500.
3. State the auth/authz model, matching the existing project convention.
4. Design error responses with a consistent shape and correct status
   codes (400/401/403/404/409/429/5xx).
5. Add pagination for any collection endpoint (cursor or offset, matching
   existing convention; explicit page-size default/limit).
6. State the versioning approach for this change and why.
7. Note idempotency for retryable unsafe methods (idempotency key vs.
   naturally idempotent).
8. Note rate-limiting considerations; defer enforcement to infrastructure.
9. Document the contract in the project's existing format (OpenAPI,
   Markdown, doc comments).

## Input contract

A description of the resource/operation needed, plus access to the
existing API's conventions (routing, auth middleware, error shape,
existing OpenAPI spec if any).

## Output contract

The endpoint implementation (or design) plus a contract summary covering
validation, auth, errors, pagination, versioning, idempotency, and
rate-limiting — explicitly noting any section that's not applicable
rather than silently omitting it.

## Exit criteria

Done once every contract dimension above (validation through
documentation) has been addressed or explicitly marked not applicable.

## Retry policy

See shared conventions. If a validation rule is ambiguous, state the
ambiguity and the choice made once rather than re-guessing silently.

## No hallucination rule

Never claim an endpoint was tested, deployed, or matches an existing
contract that wasn't actually read. State assumptions explicitly.

## Error handling

Never return a raw stack trace/internal exception message in an API
response; map to a generic 5xx and log detail server-side.

## Security guidance

Validate authorization on every resource access (not just authentication).
Never accept a client-supplied field that should be server-determined
(e.g., price) without flagging the risk. Consider 404-over-403 when
resource existence itself is sensitive.

## Dependencies and limitations

Assumes access to existing routing/auth/error conventions; state the
assumption when unavailable. Does not provision actual rate-limiting
infrastructure — flags where needed, defers implementation.
