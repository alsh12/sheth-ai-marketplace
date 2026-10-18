# Sheth AI Marketplace — Master Plan

Status: Phase 1-4 complete and verified. Phase 5 (publication) has manual steps outstanding.

## 1. Objective

One Claude Code plugin marketplace (`sheth-ai-marketplace`, brand: Sheth Hub, site:
https://shethhub.com) registering three independent, originally-authored plugins, each
owning its own skills, docs, and tests. Architecture must support adding more plugins
later without touching existing ones.

## 2. Scope — Release 1 (done)

| Plugin | Skills | Status |
|---|---|---|
| sheth-developer-tools | json-formatter, json-validator, xml-formatter, xml-validator, json-xml-converter | Done |
| sheth-code-review | code-review, security-review, performance-review, pull-request-review | Done |
| sheth-engineering | dotnet-development, python-development, api-development, test-development, debugging | Done |

Each skill: lean `SKILL.md` (Input contract, Output contract, Exit criteria, Retry
policy capped at 3, No-hallucination rule, Boundaries, Workflow, Error handling,
Security, Dependencies) + a separate `reference.md` for worked examples
(progressive disclosure, token-lean main file). Shared conventions centralized in
`docs/shared-conventions.md` instead of repeated per skill.

## 3. Architecture (4 layers)

1. **Catalog** — `.claude-plugin/marketplace.json` registers all 3 plugins by id,
   version, source path. Does not embed skill implementations.
2. **Plugins** — each has its own `.claude-plugin/plugin.json`, `skills/`, `README.md`,
   `CHANGELOG.md`. Independently installable; adding a plugin never edits another.
3. **Skills** — one responsibility per skill, `SKILL.md` + optional `reference.md`,
   scripts only where deterministic execution helps (see hooks below).
4. **Governance** — shared standards in `docs/`: architecture, installation,
   adding-a-plugin, adding-a-skill, testing, publishing, versioning, hooks, roadmap.

## 4. Quality gates

- **Structural validation**: `scripts/validate-marketplace.py` (stdlib-only) checks
  manifest fields, unique plugin/skill ids, valid frontmatter, referenced paths exist.
  Supports `--only <plugin>` for incremental builds.
- **Unit tests**: `tests/test_validate_marketplace.py` (unittest, 10 cases) — last run
  10/10 passed.
- **Evals**: `tests/evals/` — fixtures per skill (`{input, expected_behavior_description,
  pass_criteria}`), `run_evals.py` checks mechanically-verifiable criteria against real
  json/xml stdlib parsers (ground truth); anything needing human judgment is marked
  `requires_manual_review: true`, never auto-passed. Last run: 5/5 mechanical checks
  passed, 6 correctly flagged for manual review.
- **CI**: `.github/workflows/validate.yml` runs validator + unit tests + evals on
  push/PR.
- **Hooks**: `plugins/sheth-developer-tools/hooks/hooks.json` +
  `scripts/tool_checkpoint.py` — one real, working PreToolUse/PostToolUse example
  (confirmed Claude Code feature, not guidance-only). Other skills' pre/post-tool
  checkpoint conventions are documented authoring guidance in `docs/hooks.md`, honestly
  labeled as not independently enforced by the platform.

## 5. Versioning / change management (docs/versioning.md)

- Semver per plugin: patch = instruction clarification, minor = additive
  non-breaking capability, major = behavior-changing/breaking.
- Every bump requires a CHANGELOG.md entry.
- Marketplace catalog pins consumers to a plugin version; existing installs are not
  silently changed — upgrades are opt-in.
- A version bump should not ship if its eval fixtures fail.

## 6. Known gaps / unresolved (honest, not hidden)

- No live Claude Code session was available in this environment to actually install
  and exercise a plugin end-to-end.
- The real `claude plugin validate` CLI was unavailable here; only the project's own
  structural validator has been run.
- 6 eval criteria across sheth-developer-tools require a human or live-session
  walkthrough before a real release, per the gate in `docs/testing.md`.
- Only sheth-developer-tools has eval fixtures today; sheth-code-review and
  sheth-engineering have no eval coverage yet — tracked as follow-up, not silently
  assumed covered.

## 7. Roadmap (ideas only, not committed, see docs/roadmap.md)

Sheth PDF & Document Tools, Sheth Data Engineering, Sheth Data Science, Sheth AI
Media, Sheth Architecture, Sheth Project Management, Sheth Recruitment.

## 8. Next actions

1. Install the marketplace in a real Claude Code session and manually walk the 6
   manual-review eval criteria.
2. Run the real `claude plugin validate` CLI once available and fix any findings.
3. Add eval fixtures for sheth-code-review and sheth-engineering skills.
4. Review and commit the working tree (nothing has been committed yet — left for
   user review per repo-safety rules).
