# copilot-catalog

`copilot-catalog` is the merged home for:

- installable GitHub Copilot CLI plugins
- standalone reusable skills

This repository keeps both artifact types in one curated place while preserving clear top-level categories.

## Repository layout

- `plugins/<plugin-name>/` - installable plugin packages
- `skills/<skill-name>/SKILL.md` - standalone reusable skills
- `docs/` - migration and maintenance guidance
- `scripts/` - repository helpers and validation scripts

## Available plugins

### copilot-cmux

Send Copilot CLI notifications to cmux with a macOS fallback.

Path: `plugins/copilot-cmux`

### fun-colleague

Add a playful but still rigorous pairing style for interactive Copilot CLI sessions.

Path: `plugins/fun-colleague`

## Available skills

### agentic-progressive-disclosure-architecture

Design code for agentic coding with progressive disclosure.

Path: `skills/agentic-progressive-disclosure-architecture`

### codespaces-secret-sync

Sync user Codespaces secret repository access across multiple secrets.

Path: `skills/codespaces-secret-sync`

### github-mermaid-diagrams

Create Mermaid diagrams optimized for GitHub rendering in light and dark mode.

Path: `skills/github-mermaid-diagrams`

### migrate-agents-to-copilot-instructions

Migrate `AGENTS.md` guidance into GitHub Copilot instruction files.

Path: `skills/migrate-agents-to-copilot-instructions`

## Migration from the old repositories

Preferred cutover:

1. rename `ekroon/copilot-plugins` to `ekroon/copilot-catalog`
2. merge in `ekroon/agent-skills`
3. keep `plugins/` and `skills/` stable at the top level
4. archive `ekroon/agent-skills` with a forwarding README

See [`docs/migration.md`](docs/migration.md) for the old-path to new-path mapping and the local migration helper.

## Quick start

```bash
git clone https://github.com/ekroon/copilot-catalog.git
cd copilot-catalog
```

Local plugin development example:

```bash
copilot plugin install /absolute/path/to/copilot-catalog/plugins/fun-colleague
```

Run the catalog validator:

```bash
python3 scripts/validate_catalog.py
```
