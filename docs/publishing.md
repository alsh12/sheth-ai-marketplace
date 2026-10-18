# Publishing

1. Follow `docs/versioning.md` for the version bump and changelog entry.
2. Run the full gate from `docs/testing.md`: structural validator, unit
   tests, eval harness, and the manual-review checklist for any touched
   skill.
3. Run the real `claude plugin validate .` (the authoritative Claude Code
   CLI validator) from your shell before publishing — this repository's
   own `scripts/validate-marketplace.py` is a structural check, not a
   replacement for it, and `claude plugin validate` was not available to
   run in the environment this repo was built in.
4. Commit the change (this repo does not commit on your behalf — review
   `git status`/`git diff` yourself first).
5. Push to wherever this marketplace is hosted (a `github`, `git`, or
   `url` marketplace source, per `docs/architecture.md`'s layers) and
   confirm `claude plugin marketplace update` or a fresh
   `claude plugin marketplace add` picks up the change in a real Claude
   Code session — this is a manual step that has not been performed as
   part of building this repository.
6. If removing or renaming a plugin, use `marketplace.json`'s `renames`
   field rather than silently deleting its entry, so existing installs
   aren't orphaned (see `docs/versioning.md` on opt-in upgrades).

See `docs/roadmap.md` for plugin ideas that are explicitly not yet
candidates for publishing.
