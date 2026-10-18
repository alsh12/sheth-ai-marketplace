---
name: dotnet-development
description: Write and modify C#/.NET code, including ASP.NET Core, dependency injection, async code, and EF Core, following the project's existing conventions. Use when the user is working in a .NET/C# codebase and asks to write, change, or review application code (not specifically tests, which belongs to test-development).
---

# .NET Development

Writes/modifies C#/.NET code respecting existing project conventions. See
`reference.md` for a worked example. Shared conventions:
`../../../../docs/shared-conventions.md`.

## Boundaries

- Not for writing tests (see test-development), though a minimal smoke test
  alongside a change is fine if asked.
- Does not add a new major dependency/pattern (NuGet package, CQRS/MediatR,
  a second ORM) without flagging the addition and reason.
- Does not assume a .NET version's features are available — check
  `<TargetFramework>` in the `.csproj` first.
- Does not silently change public API surface without calling out the
  compatibility impact.

## Workflow

1. Read before writing: target framework, existing DI style, naming,
   nullable-reference-types setting, async patterns. Use Grep/Glob to find
   `Program.cs`/`Startup.cs` and parallel examples rather than reading the
   whole project.
2. Verify compatibility: don't use a language feature newer than the
   target framework/installed package versions.
3. Follow existing DI conventions (constructor injection; match existing
   lifetime choices and explain the choice).
4. Write async correctly: propagate async/await, honor `CancellationToken`
   where already used, avoid `async void` except event handlers.
5. EF Core: match existing query style, use `AsNoTracking()` for read-only
   queries when that's the convention, be explicit about transaction
   boundaries.
6. ASP.NET Core endpoints: match existing style (minimal API vs.
   controllers), validate input models, use consistent status codes.
7. State what changed and why, especially for any deviation from an
   existing pattern.

## Input contract

A description of the desired change, plus access to the relevant `.cs`
files, `.csproj`, and DI registration code.

## Output contract

Modified or new C# files consistent with surrounding conventions, with a
short explanation of key decisions (lifetime, async boundaries, query
shape) and any compatibility caveats.

## Exit criteria

Done once the change compiles conceptually against the stated target
framework and every deviation from an existing pattern has been called
out — not merely once code "looks right."

## Retry policy

See shared conventions. If target framework/package versions can't be
confirmed from `.csproj`, state the assumption once rather than guessing
silently on each attempt.

## No hallucination rule

Never claim code compiles or that `dotnet build`/`dotnet test` passed
without having actually run them. State explicitly when that wasn't done.

## Error handling

Let programmer-error exceptions (null ref, bad arguments) surface with
actionable messages. For expected failures, use the project's existing
pattern (result types, specific exceptions, nullable returns). Flag any
discarded exception that isn't logged or rethrown.

## Security guidance

Never build SQL manually from untrusted input when EF Core/parameterized
`FromSqlInterpolated` is available. Validate request models explicitly;
don't trust client-supplied IDs without a server-side authorization check.
Don't log request bodies or connection strings that may hold credentials.

## Dependencies and limitations

Assumes access to `.csproj`/`Directory.Build.props` to confirm target
framework; state the assumption when unavailable. Does not run
`dotnet build`/`dotnet test` itself — recommend doing so before any claim
of correctness.
