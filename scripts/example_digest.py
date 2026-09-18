#!/usr/bin/env python3
"""Print stable SHA-256 digests for a compact project example."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python scripts/example_digest.py <example-dir>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1])
    if not root.is_dir():
        print(f"missing example directory: {root}", file=sys.stderr)
        return 2
    files = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name != "evidence.json":
            files.append({
                "path": path.relative_to(root).as_posix(),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
    print(json.dumps({"example": root.as_posix(), "files": files}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
