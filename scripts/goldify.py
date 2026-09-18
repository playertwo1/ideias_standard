#!/usr/bin/env python3
"""Read-only discovery and minimal Golden Diff for an existing project."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def discover(root: Path) -> dict:
    if not root.is_dir():
        raise ValueError(f"IS-GOLD-001: project path must be an existing directory: {root}")
    names = {p.name for p in root.iterdir()}
    has_tests = any((root / name).is_dir() for name in ("tests", "test")) or any(
        path.is_file() for path in (root / "scripts").glob("test_*.py")
    )
    has_ci = (root / ".github" / "workflows").is_dir()
    has_check = any((root / name).is_file() for name in ("check.py", "check.sh", "Makefile")) or (root / "scripts" / "check.py").is_file()
    necessary = []
    recommended = []
    if "README.md" not in names:
        necessary.append("README.md: explicar propósito e verificação")
    if "AGENTS.md" not in names:
        necessary.append("AGENTS.md: instruções mínimas para agentes")
    if not has_tests:
        necessary.append("tests/: adicionar apenas testes aplicáveis")
    if not has_ci:
        recommended.append(".github/workflows/ci.yml: repetir verificações essenciais")
    if not has_check:
        recommended.append("check reproduzível: documentar ou criar comando existente")
    return {
        "project": str(root),
        "inventory": {"readme": "README.md" in names, "agents": "AGENTS.md" in names, "tests": has_tests, "ci": has_ci, "check": has_check},
        "necessary": necessary,
        "recommended": recommended,
        "user_owned": sorted(names),
        "writes": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        report = discover(args.path.resolve())
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("NECESSÁRIO")
        for item in report["necessary"]:
            print(f"- {item}")
        print("RECOMENDADO")
        for item in report["recommended"]:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
