# Sheth Engineering

Engineering workflows for .NET, Python, API design, test development, and
structured debugging, built around evidence-based, convention-respecting
practices.

## Skills

| Skill | What it does |
| :- | :- |
| `dotnet-development` | Writes/modifies C#/.NET code (ASP.NET Core, DI, async, EF Core) matching existing conventions. |
| `python-development` | Writes/modifies typed Python code with explicit error handling and logging. |
| `api-development` | Designs/implements REST endpoints with a complete contract (validation, auth, errors, pagination, versioning, idempotency, rate limits). |
| `test-development` | Writes deterministic, isolated tests and only reports pass/fail from an actual run. |
| `debugging` | Diagnoses bugs via reproduction and evidence before proposing a fix, then adds a regression test. |

## Design principles

- Match the project's existing conventions rather than imposing a generic
  style.
- Never claim code compiles, a test passed, or a fix is verified without
  actually having run it.
- State assumptions and compatibility caveats explicitly rather than
  guessing silently.

See each skill's `SKILL.md` for its input/output contract and
`reference.md` for a worked example. Shared conventions:
`../../docs/shared-conventions.md`.
