---
name: codespaces-secret-sync
description: Sync user Codespaces secret repository access so multiple secrets match a base secret (defaults to first listed secret).
---

# Codespaces Secret Sync

Use this skill when you want multiple **user Codespaces secrets** to share the same selected-repository access as one base secret.

## What it does

- Reads the selected repositories from a base secret (`--base-secret`, or first listed secret by default).
- Syncs other secrets to that same repo set.
- Supports dry-run (default) and apply mode.

## Prerequisites

- `gh` CLI authenticated for the target account (`gh auth status`)
- `python3`

## Script

`scripts/sync_codespaces_secret_repos.py`

## Usage

Dry-run all user Codespaces secrets except the base secret:

```bash
python3 scripts/sync_codespaces_secret_repos.py
```

Apply for all secrets:

```bash
python3 scripts/sync_codespaces_secret_repos.py --apply
```

Apply only for specific secrets:

```bash
python3 scripts/sync_codespaces_secret_repos.py --apply --secrets SECRET_A SECRET_B SECRET_C
```

Use a different base secret:

```bash
python3 scripts/sync_codespaces_secret_repos.py --apply --base-secret MY_BASE_SECRET
```

Add missing repos only (do not remove extras):

```bash
python3 scripts/sync_codespaces_secret_repos.py --apply --add-only
```
