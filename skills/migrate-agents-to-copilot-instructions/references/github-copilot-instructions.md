# GitHub Copilot instruction file reference

This reference captures the GitHub Copilot instruction file details that matter for AGENTS-to-Copilot migrations.

## Verified repository file names

Official GitHub docs confirm these repository-level instruction file locations:

- `.github/copilot-instructions.md` for repository-wide instructions
- `.github/instructions/NAME.instructions.md` for path-specific instructions
- `AGENTS.md` files can still exist anywhere in the repository for agent instructions

Relevant docs:

- https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions
- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions
- https://docs.github.com/en/copilot/reference/custom-instructions-support

## Repository-wide syntax

Repository-wide instructions live in `.github/copilot-instructions.md`.

They use plain Markdown with natural-language instructions. No frontmatter is required.

Example:

```md
# Repository guidance

- Use TypeScript rather than JavaScript.
- Run `pnpm test` before finishing a change.
- Keep API handlers thin and move business logic into services.
```

## Path-specific syntax

Path-specific instructions live under `.github/instructions/` and the file name must end with `.instructions.md`.

Use a frontmatter block at the top with `applyTo`.

Official-doc style:

```md
---
applyTo: "app/models/**/*.rb"
---
```

For multiple patterns, use a comma-separated string:

```md
---
applyTo: "**/*.ts,**/*.tsx"
---
```

Then add normal Markdown instructions below the frontmatter:

```md
---
applyTo: "packages/frontend/**"
---

# Frontend guidance

- Prefer accessible components.
- Use the shared design tokens.
```

## Optional `excludeAgent`

Official CLI docs also support `excludeAgent` in path-specific instruction frontmatter.

Supported values:

- `"code-review"`
- `"coding-agent"`

Example:

```md
---
applyTo: "docs/**"
excludeAgent: "code-review"
---
```

If `excludeAgent` is omitted, both Copilot code review and Copilot coding agent can use the file where supported.

## How Copilot combines instructions

Official docs state:

- repository-wide instructions and matching path-specific instructions are both used together
- path-specific instructions have higher repository-level precedence than repository-wide instructions
- conflicting instructions can produce non-deterministic results, so avoid overlaps that disagree

This means a migration should:

- move broad rules into `.github/copilot-instructions.md`
- keep local rules in `.github/instructions/*.instructions.md`
- avoid copying the same rule into both places unless the duplication is harmless

## AGENTS.md compatibility

Official docs still describe `AGENTS.md` as a supported instruction source for several Copilot surfaces, including Copilot coding agent and Copilot CLI.

Do not assume the right migration is to delete `AGENTS.md`.

Safer default:

- add Copilot instruction files
- keep existing `AGENTS.md` files unless the user explicitly wants a cleanup step

## Support summary

From GitHub's support matrix:

- GitHub.com Copilot Chat: repository-wide instructions
- GitHub.com Copilot coding agent: repository-wide, path-specific, and agent instructions
- GitHub.com Copilot code review: repository-wide and path-specific instructions
- VS Code Copilot Chat: repository-wide, path-specific, and `AGENTS.md`
- Copilot CLI: repository-wide, path-specific, and `AGENTS.md`

This is why AGENTS-to-Copilot migration is usually about adding better-supported repository and path-specific instruction files, not necessarily removing `AGENTS.md`.

## Migration heuristics

Use these defaults when converting nested `AGENTS.md` files:

- `AGENTS.md` at repository root -> `.github/copilot-instructions.md`
- `services/payments/AGENTS.md` -> `.github/instructions/services-payments.instructions.md` with `applyTo: "services/payments/**"`
- `docs/AGENTS.md` -> `.github/instructions/docs.instructions.md` with `applyTo: "docs/**"`

If one `AGENTS.md` mixes global and local guidance:

1. move global guidance into `.github/copilot-instructions.md`
2. move local guidance into a scoped `.instructions.md`
3. keep only truly agent-specific leftovers in `AGENTS.md`

## Authoring reminders

- Keep instructions concise and self-contained.
- Prefer repository facts, conventions, commands, and architectural notes over assistant-personality rules.
- Keep important rules early in the file because Copilot code review only reads the first 4,000 characters of any custom instruction file.
