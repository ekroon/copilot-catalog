#!/usr/bin/env python3
"""Sync user Codespaces secret selected repositories to match a base secret."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Dict, Iterable, List


class GhApiError(RuntimeError):
    pass


def gh_api(path: str, method: str = "GET", expect_json: bool = True):
    cmd = ["gh", "api", "-X", method, path]
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        message = (result.stderr or result.stdout).strip()
        raise GhApiError(f"gh api failed for {path}: {message}")
    if not expect_json:
        return None
    output = result.stdout.strip()
    return json.loads(output) if output else {}


def list_secret_names() -> List[str]:
    data = gh_api("/user/codespaces/secrets?per_page=100")
    return [item["name"] for item in data.get("secrets", [])]


def get_secret_visibility(secret_name: str) -> str:
    data = gh_api(f"/user/codespaces/secrets/{secret_name}")
    return data.get("visibility", "")


def get_secret_repo_map(secret_name: str) -> Dict[str, int]:
    data = gh_api(f"/user/codespaces/secrets/{secret_name}/repositories?per_page=100")
    return {repo["full_name"]: int(repo["id"]) for repo in data.get("repositories", [])}


def ensure_selected_visibility(secret_name: str) -> None:
    visibility = get_secret_visibility(secret_name)
    if visibility != "selected":
        raise GhApiError(
            f"Secret {secret_name} has visibility '{visibility}'. "
            "This script requires 'selected' visibility."
        )


def unique_ordered(names: Iterable[str]) -> List[str]:
    seen = set()
    ordered: List[str] = []
    for name in names:
        if name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync user Codespaces secret repositories to match a base secret."
    )
    parser.add_argument(
        "--base-secret",
        help=(
            "Base secret whose selected repositories are treated as source of truth. "
            "If omitted, the first user Codespaces secret is used."
        ),
    )
    parser.add_argument(
        "--secrets",
        nargs="+",
        help="Target secret names. If omitted, all user Codespaces secrets except base are used.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes. Without this flag, runs in dry-run mode.",
    )
    parser.add_argument(
        "--add-only",
        action="store_true",
        help="Only add missing repositories; do not remove extra repositories.",
    )
    args = parser.parse_args()

    try:
        all_secret_names = list_secret_names()
        if not all_secret_names:
            raise GhApiError("No user Codespaces secrets found.")

        base_secret = args.base_secret or all_secret_names[0]
        if base_secret not in all_secret_names:
            raise GhApiError(
                f"Base secret {base_secret} was not found in user Codespaces secrets."
            )

        ensure_selected_visibility(base_secret)
        base_repo_map = get_secret_repo_map(base_secret)
        base_repos = set(base_repo_map.keys())

        if args.secrets:
            targets = unique_ordered(name for name in args.secrets if name != base_secret)
        else:
            targets = [name for name in all_secret_names if name != base_secret]

        if not targets:
            print("No target secrets found.")
            return 0

        mode = "APPLY" if args.apply else "DRY_RUN"
        print(f"MODE|{mode}")
        print(f"BASE_SECRET|{base_secret}")
        print(f"TARGET_COUNT|{len(targets)}")

        change_count = 0

        for secret_name in targets:
            ensure_selected_visibility(secret_name)
            current_repo_map = get_secret_repo_map(secret_name)
            current_repos = set(current_repo_map.keys())

            to_add = sorted(base_repos - current_repos)
            to_remove = sorted(current_repos - base_repos) if not args.add_only else []

            print(
                f"PLAN|{secret_name}|add={len(to_add)}|remove={len(to_remove)}"
            )

            for repo_name in to_add:
                repo_id = base_repo_map[repo_name]
                print(f"ADD|{secret_name}|{repo_name}")
                if args.apply:
                    gh_api(
                        f"/user/codespaces/secrets/{secret_name}/repositories/{repo_id}",
                        method="PUT",
                        expect_json=False,
                    )
                change_count += 1

            for repo_name in to_remove:
                repo_id = current_repo_map[repo_name]
                print(f"REMOVE|{secret_name}|{repo_name}")
                if args.apply:
                    gh_api(
                        f"/user/codespaces/secrets/{secret_name}/repositories/{repo_id}",
                        method="DELETE",
                        expect_json=False,
                    )
                change_count += 1

        print(f"PLANNED_OR_APPLIED_CHANGES|{change_count}")

        if args.apply:
            mismatch_count = 0
            for secret_name in targets:
                final_repos = set(get_secret_repo_map(secret_name).keys())
                missing = sorted(base_repos - final_repos)
                extra = sorted(final_repos - base_repos) if not args.add_only else []
                if missing or extra:
                    mismatch_count += 1
                    print(
                        f"MISMATCH|{secret_name}|missing={','.join(missing) or '-'}|"
                        f"extra={','.join(extra) or '-'}"
                    )
            if mismatch_count:
                print(f"VERIFY|FAILED|count={mismatch_count}")
                return 1
            print("VERIFY|OK")

        return 0
    except GhApiError as exc:
        print(f"ERROR|{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
