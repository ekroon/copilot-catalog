#!/usr/bin/env python3
"""Rewrite local Copilot config paths from old repo names to copilot-catalog."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable


DEFAULT_EXTENSIONS = {
    ".json",
    ".jsonc",
    ".yaml",
    ".yml",
    ".md",
    ".txt",
}


def iter_candidate_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in DEFAULT_EXTENSIONS:
            yield path


def rewrite_text(text: str, old_repo_name: str, new_repo_name: str) -> tuple[str, int]:
    replacements = [
        (f"{old_repo_name}/plugins/", f"{new_repo_name}/plugins/"),
        ("agent-skills/skills/", f"{new_repo_name}/skills/"),
    ]

    updated = text
    count = 0
    for old, new in replacements:
        matches = updated.count(old)
        if matches:
            updated = updated.replace(old, new)
            count += matches
    return updated, count


def process_file(path: Path, old_repo_name: str, new_repo_name: str, apply_changes: bool) -> int:
    original = path.read_text(encoding="utf-8")
    updated, count = rewrite_text(original, old_repo_name, new_repo_name)
    if count and apply_changes:
        path.write_text(updated, encoding="utf-8")
    return count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Directory to scan")
    parser.add_argument("--old-repo-name", default="copilot-plugins")
    parser.add_argument("--new-repo-name", default="copilot-catalog")
    parser.add_argument("--apply", action="store_true", help="Write changes in place")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Root directory does not exist or is not a directory: {root}")

    changed_files = 0
    replacement_count = 0
    for path in iter_candidate_files(root):
        try:
            count = process_file(path, args.old_repo_name, args.new_repo_name, args.apply)
        except UnicodeDecodeError:
            continue
        if count:
            changed_files += 1
            replacement_count += count
            verb = "updated" if args.apply else "would update"
            print(f"{verb}: {path} ({count} replacements)")

    if changed_files == 0:
        print("No matching paths found.")
        return 0

    verb = "Updated" if args.apply else "Would update"
    print(f"{verb} {changed_files} files with {replacement_count} replacements.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
