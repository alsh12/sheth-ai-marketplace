# Adding a skill

1. Create `plugins/<plugin>/skills/<skill-name>/SKILL.md` with YAML
   frontmatter: `name` and `description` are required (the description
   should state when to activate the skill, not just what it does).
2. Keep `SKILL.md` lean (roughly 60-150 lines): Purpose, Boundaries,
   Workflow, **Input contract**, **Output contract**, **Exit criteria**,
   **Retry policy**, **No hallucination rule**, Error handling, Security
   guidance, Dependencies and limitations. These structured sections are
   required for every skill in this marketplace.
3. Move worked examples and longer sample input/output into a
   `reference.md` file in the same directory — do not inline a full
   example into `SKILL.md`. Link to shared conventions
   (`docs/shared-conventions.md`) instead of repeating tool-use, retry, or
   no-hallucination boilerplate per skill.
4. If the skill's workflow invokes a tool whose input/output is worth
   mechanically checking, consider the pre-tool/post-tool checkpoint
   convention in `docs/hooks.md` — most skills in this marketplace instead
   rely on the prose contracts in step 2, which is a valid and honest
   choice when the check isn't easily scriptable.
5. Add a fixture to `tests/evals/<plugin>/<skill-name>.json` (see
   `docs/testing.md`) with `input`, `expected_behavior_description`, and
   `pass_criteria` — mark `requires_manual_review: true` for any criterion
   that isn't mechanically checkable.
6. Update the plugin's `README.md` skills table and `CHANGELOG.md`.
7. Run the validator and the eval runner before considering the skill
   done.
