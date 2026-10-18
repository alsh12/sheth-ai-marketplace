# Shared skill conventions

Common rules that apply to every skill in this marketplace. Individual
`SKILL.md` files reference this doc instead of repeating these points.

## Tool usage discipline

- Use **Grep** to search file contents for a pattern; never open whole
  files just to search them.
- Use **Glob** to find files by name/path pattern.
- Use **Read** for actual file contents, and only the relevant line range
  (offset/limit) when a file is large — don't read an entire large file
  when a section will do.
- Use **Write** only to create new files. Prefer targeted edits
  (Edit-equivalent) over rewriting an existing file wholesale.
- Never read or scan an entire repository when a targeted search answers
  the question.

## No hallucination rule (applies to every skill)

Never fabricate file contents, line numbers, command output, test results,
or validation outcomes that were not actually read, run, or produced in
this session. If something cannot be verified (a test wasn't run, a file
wasn't read, a result is uncertain), say so explicitly instead of
inventing a plausible-sounding answer.

## Retry policy (applies to every skill)

On a recoverable failure (parse error, ambiguous input, a tool call that
errors), retry at most 3 times, trying a genuinely different approach each
time (not the identical action). If all 3 attempts fail, stop and report
the failure clearly, including what was tried, rather than looping
indefinitely or guessing at a result.

## Severity / classification vocabulary

Review-type skills (code-review, security-review, performance-review,
pull-request-review) use a shared severity vocabulary so findings are
comparable across skills: `blocking` / `should-fix` / `nit` for general
review, `critical` / `high` / `medium` / `low` / `informational` for
security, and an explicit `confirmed:` vs. `possible:` label on every
finding whose certainty isn't total.

## Progressive disclosure

Each `SKILL.md` is kept short and scannable. Worked examples, longer
sample input/output, and edge-case notes live in that skill's own
`reference.md` (or `examples.md`) file in the same directory, and are
loaded only when needed — not inlined into the main skill file.
