#!/usr/bin/env python3
"""Run the minimal, provider-neutral Gold Audit decision on a fixture."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def audit(change: dict) -> dict:
    findings = []
    if not str(change.get("request", "")).strip():
        findings.append({"code": "IS-AUDIT-001", "message": "request is missing"})
    if not change.get("acceptance"):
        findings.append({"code": "IS-AUDIT-001", "message": "acceptance criteria are missing"})
    if not change.get("diff"):
        findings.append({"code": "IS-AUDIT-002", "message": "diff evidence is missing"})
    if change.get("check") != "PASS":
        findings.append({"code": "IS-AUDIT-003", "message": "check did not pass"})
    return {"result": "FAIL" if findings else "PASS", "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        change = json.loads(args.fixture.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR IS-AUDIT-000: cannot read fixture: {exc}")
        return 2
    report = audit(change)
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(report["result"])
        for finding in report["findings"]:
            print(f"- {finding['code']}: {finding['message']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
