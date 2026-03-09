---
name: migrate-agents-to-copilot-instructions
description: |
  Migrate or mirror AGENTS.md guidance into GitHub Copilot custom instruction files.
  Use this skill whenever the user wants to replace, convert, or align AGENTS.md, CLAUDE.md,
  or GEMINI.md content with `.github/copilot-instructions.md` and `.github/instructions/*.instructions.md`,
  especially when preserving root-wide guidance versus subtree-specific guidance for GitHub Copilot.
---

# Migrate AGENTS.md to GitHub Copilot Instructions

Use this skill to convert repository guidance from `AGENTS.md` files into GitHub Copilot custom instruction files without losing scope or intent.

For exact file names, supported locations, and official syntax, read `references/github-copilot-instructions.md` before writing the target files.

## What to migrate where

Map guidance by scope instead of copying file-for-file blindly:

- Put repository-wide guidance into `.github/copilot-instructions.md`.
- Put subtree-specific guidance into `.github/instructions/NAME.instructions.md`.
- Keep `AGENTS.md` files unless the user explicitly asks you to remove them.

Why: GitHub Copilot combines repository-wide instructions with matching path-specific instructions, but `AGENTS.md` files still matter in some Copilot surfaces and other agent ecosystems.

## Migration workflow

1. Inventory the current instruction sources:
   - root and nested `AGENTS.md`
   - root `CLAUDE.md` or `GEMINI.md` if present
   - any existing `.github/copilot-instructions.md`
   - any existing `.github/instructions/**/*.instructions.md`
2. Read each source and classify every instruction as one of:
   - repository-wide
   - path-specific
   - agent-only workflow advice
3. Draft a migration map before editing:
   - source file
   - intended Copilot target file
   - target scope or `applyTo` glob
   - anything that should stay in `AGENTS.md`
4. Write or update `.github/copilot-instructions.md` with the broad guidance that should apply across the repository.
5. Write or update `.github/instructions/*.instructions.md` for scoped guidance.
6. Validate that each new `applyTo` pattern matches the intended files and does not accidentally overreach.

## Scope mapping rules

### Repository-wide content

Usually migrate these to `.github/copilot-instructions.md`:

- repository purpose and architecture overview
- global coding conventions
- build, test, and validation commands
- cross-cutting safety or review expectations
- repository-wide layout notes

### Path-specific content

Usually migrate these to `.github/instructions/*.instructions.md`:

- rules that only apply inside one subtree
- framework conventions tied to one directory
- exceptions for tests, generated code, docs, infra, or UI folders
- local architecture notes for a package, service, or module tree

When a nested `AGENTS.md` lives under `path/to/subtree/`, default to an `applyTo` glob like:

```md
---
applyTo: "path/to/subtree/**"
---
```

If the content clearly targets a narrower subset, use a tighter glob instead, such as:

- `"packages/api/**/*.ts"`
- `"docs/**/*.md"`
- `"services/payments/**/*"`
- `"src/**/*.test.ts,src/**/*.spec.ts"`

## How to translate AGENTS.md content

Do not copy agent-specific behavior literally when it does not make sense as a Copilot repository instruction.

Prefer these transformations:

- Convert "search these files first" into concise repository layout guidance.
- Convert "run these commands before finishing" into validation instructions.
- Convert local coding norms into short, self-contained rules.
- Convert subtree context into path-scoped instructions with `applyTo`.

Be cautious with instructions that are only meaningful for a specific agent runtime, such as:

- rules about which tools the agent must use first
- session-management behavior
- UI-specific interaction instructions for a different assistant

For those cases, either:

- keep the original `AGENTS.md`, or
- rewrite the guidance into repository facts that still help Copilot.

## Writing the target files

### `.github/copilot-instructions.md`

- Use plain Markdown.
- Keep it broadly applicable.
- Favor short, self-contained statements over long prose.
- Avoid duplicating subtree-specific rules that belong in scoped files.

### `.github/instructions/NAME.instructions.md`

- Use the exact `.instructions.md` suffix.
- Put a frontmatter block at the top with `applyTo`.
- Use official-doc syntax with a quoted glob string; for multiple patterns, use a comma-separated string.
- Add `excludeAgent` only when the instructions should be ignored by either `code-review` or `coding-agent`.
- Keep each file focused on one area of the repository.

Template:

```md
---
applyTo: "path/to/subtree/**"
---

# Subtree guidance

- Keep these instructions concise and local to the matching files.
- Mention local conventions, validation rules, or architectural constraints.
```

Optional exclusion:

```md
---
applyTo: "docs/**"
excludeAgent: "code-review"
---
```

## Conflict control

- Avoid contradictory guidance across repository-wide and path-specific files.
- If several nested `AGENTS.md` files overlap, preserve the intent with multiple scoped instruction files and narrower globs.
- Prefer one focused instruction file per concern or subtree instead of one oversized file.
- Keep critical guidance near the top because some Copilot surfaces read only part of long files.

## Safe defaults

- Do not delete or rename original instruction files unless the user asks.
- If a migration decision is ambiguous, preserve behavior by keeping the original file and adding the Copilot instruction file.
- If an `AGENTS.md` contains both global and subtree-local guidance, split it rather than forcing everything into one target file.

## Expected output

When you complete a migration, provide:

1. the created or updated `.github/copilot-instructions.md`
2. any created or updated `.github/instructions/*.instructions.md` files
3. a short migration summary covering:
   - which source files were mapped
   - which scoped globs were chosen
   - what content, if any, was intentionally left in `AGENTS.md`
