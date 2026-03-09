#!/usr/bin/env python3
"""Validate the proposed copilot-catalog repository layout."""

from __future__ import annotations

import sys
from pathlib import Path


def names_in(directory: Path) -> set[str]:
    if not directory.exists():
        return set()
    return {path.name for path in directory.iterdir() if path.is_dir()}


def check_required_files(base: Path, category: str, required_name: str) -> list[str]:
    issues: list[str] = []
    root = base / category
    if not root.exists():
        issues.append(f"Missing top-level directory: {root}")
        return issues

    for item in sorted(root.iterdir()):
        if item.is_dir() and not (item / required_name).exists():
            issues.append(f"Missing {required_name}: {item / required_name}")
    return issues


def main() -> int:
    base = Path.cwd()
    issues: list[str] = []

    duplicates = sorted(names_in(base / "skills") & names_in(base / "plugins"))
    for name in duplicates:
        issues.append(f"Duplicate artifact name across skills/ and plugins/: {name}")

    issues.extend(check_required_files(base, "skills", "SKILL.md"))
    issues.extend(check_required_files(base, "plugins", "README.md"))

    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        return 1

    print("Catalog layout looks valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
