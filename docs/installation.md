# Installation

## Add the marketplace

From a Claude Code terminal session:

```
/plugin marketplace add <path-or-url-to-this-repo>
```

Or, from your shell:

```
claude plugin marketplace add <path-or-url-to-this-repo>
```

## Install a plugin

Each plugin installs independently. From `/plugin` in a terminal session,
open the **Discover** tab and install one of:

- `sheth-developer-tools@sheth-ai-marketplace`
- `sheth-code-review@sheth-ai-marketplace`
- `sheth-engineering@sheth-ai-marketplace`

Or from your shell:

```
claude plugin install sheth-developer-tools@sheth-ai-marketplace
```

Repeat for any of the other two — installing one does not require or
imply installing the others.

## Choose a scope

Pick user scope (every project on this machine), project scope (shared
with collaborators via committed settings), or local scope (just this
repo, just you). See each plugin's own `README.md` for which skills it
adds and docs/versioning.md for how version pins work once installed.

## Verify it loaded

Run `/plugin` and check the **Installed** tab, or `claude plugin list`
from your shell. A skill from an enabled plugin becomes available as
`/plugin-name:skill-name` and can also be invoked automatically by Claude
when its `description` matches your request.

## Develop or test locally without installing

Load a plugin directly from its folder, without adding the marketplace:

```
claude --plugin-dir plugins/sheth-developer-tools
```
