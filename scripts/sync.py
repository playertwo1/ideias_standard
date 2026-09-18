#!/usr/bin/env python3
"""Plan/apply a conservative Gold sync without overwriting existing files."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

EXCLUDED_DIRS = {".git", "__pycache__"}


def validate_directory(path: Path, label: str) -> Path:
    if not path.is_dir():
        raise ValueError(f"IS-SYNC-001: {label} path must be an existing directory: {path}")
    return path


def is_syncable(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return False
    if path.suffix == ".pyc" or path.name == ".env" or path.name.startswith(".env."):
        return False
    return True


def files(root: Path) -> set[str]:
    validate_directory(root, "project")
    return {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and is_syncable(p, root)}


def plan(source: Path, target: Path) -> dict:
    validate_directory(source, "source")
    validate_directory(target, "target")
    old, current = files(source), files(target)
    necessary = sorted(old - current)
    conflicts = sorted(path for path in old & current if hashlib.sha256((source / path).read_bytes()).digest() != hashlib.sha256((target / path).read_bytes()).digest())
    recommended = sorted(current - old)
    return {"source": str(source), "target": str(target), "necessary": necessary, "recommended": recommended, "conflicting": conflicts, "writes": False}


def apply_missing(source: Path, target: Path, report: dict, confirm_destructive: bool = False) -> dict:
    validate_directory(source, "source")
    validate_directory(target, "target")
    if report["conflicting"]:
        raise SystemExit("conflicting USER_OWNED files require explicit resolution")
    for path in report["necessary"]:
        destination = target / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / path, destination)
    report["writes"] = bool(report["necessary"])
    report["destructive_confirmation"] = confirm_destructive
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm-destructive", action="store_true")
    args = parser.parse_args()
    try:
        report = plan(args.source.resolve(), args.target.resolve())
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.apply:
        report = apply_missing(args.source.resolve(), args.target.resolve(), report, args.confirm_destructive)
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for section in ("necessary", "recommended", "conflicting"):
            print(section.upper())
            for item in report[section]:
                print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
