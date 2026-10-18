# Sheth Code Review

Severity-ranked code review workflows: general correctness, security,
performance, and pull-request-level review against stated requirements.

## Skills

| Skill | What it does |
| :- | :- |
| `code-review` | General correctness/regression/maintainability review of a diff. |
| `security-review` | Reviews for auth, injection, secrets, deserialization, and dependency risk. |
| `performance-review` | Reviews for algorithmic, allocation, and I/O inefficiency. |
| `pull-request-review` | Reviews a PR against its stated requirements with a blocking/non-blocking summary. |

## Design principles

- Every finding is tied to a file:line and labeled confirmed or possible.
- No skill in this plugin approves, merges, or claims exhaustive security
  coverage — all four produce recommendations, not actions or guarantees.
- Severity vocabulary is shared across skills (see
  `../../docs/shared-conventions.md`) so findings are comparable.

See each skill's `SKILL.md` for its input/output contract and
`reference.md` for a worked example.
