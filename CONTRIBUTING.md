# Contributing

Thanks for contributing to `copilot-catalog`.

## Add a new skill

1. Create a new folder under `skills/<skill-name>/`.
2. Add `SKILL.md` with YAML frontmatter including:
   - `name`
   - `description`
3. Add optional `scripts/` and `references/` folders as needed.
4. Keep examples generic and reusable across users.

## Add a new plugin

1. Create a new folder under `plugins/<plugin-name>/`.
2. Add a `README.md` describing purpose, install flow, and update guidance.
3. Add `plugin.json` and any plugin-local assets such as `agents/`, `skills/`, `hooks.json`, or helper scripts.
4. If the plugin is published through the marketplace wrapper, add or update its entry in `.github/plugin/marketplace.json`.

## Validation checklist

- Skills have valid frontmatter and clear trigger-oriented descriptions.
- Plugin manifests and README files stay in sync.
- Script examples run from repository root when documented that way.
- No personal credentials or account-specific defaults are committed.
- `python3 scripts/validate_catalog.py` passes before publishing structural changes.
