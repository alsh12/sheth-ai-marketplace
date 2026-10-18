# Adding a plugin

1. Create `plugins/<new-plugin-name>/.claude-plugin/plugin.json` with at
   least `name`, `version`, `description`, and `author` (matching the
   format used by the three existing plugins).
2. Add `plugins/<new-plugin-name>/skills/<skill-name>/SKILL.md` for each
   skill (see `docs/adding-a-skill.md`).
3. Add `plugins/<new-plugin-name>/README.md` (skills table + design
   principles, following the existing plugins' format) and
   `CHANGELOG.md` (starting with `## 1.0.0 - Initial release`).
4. Register the plugin in the root `.claude-plugin/marketplace.json`
   `plugins` array: a unique `name`, a `source` of
   `"./plugins/<new-plugin-name>"`, a `description`, and a `version`
   matching the plugin manifest.
5. Run the validator (see `docs/testing.md`) and fix anything it flags.
6. Follow `docs/versioning.md` for the initial version number and the
   required changelog entry.

Keep each plugin independently installable: do not have one plugin's
skills assume another plugin is also enabled.
