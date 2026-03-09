# Copilot Instructions

## Repository layout

This repository is a catalog with two top-level artifact types:

- `plugins/` — installable Copilot CLI plugin packages
- `skills/` — standalone reusable skills with `SKILL.md`

Keep the taxonomy obvious:

- standalone reusable assets belong in `skills/<name>/`
- plugin-specific assets belong inside `plugins/<plugin-name>/`
- plugin-local `agents/` and `skills/` stay nested inside the plugin package when they are part of that plugin

## Editing rules

- Keep root documentation oriented around the full catalog, not a single plugin.
- Update `.github/plugin/marketplace.json` when publishing plugin version changes through the marketplace wrapper.
- Preserve stable paths under both `plugins/` and `skills/` so local users can migrate with minimal churn.
- Prefer shared documentation and references over copying the same standalone skill content into multiple places.

## Validation

- Run `python3 scripts/validate_catalog.py` after structural changes.
- Run existing plugin tests when changing plugin behavior.
- Keep plugin manifests, install docs, and marketplace metadata aligned.
