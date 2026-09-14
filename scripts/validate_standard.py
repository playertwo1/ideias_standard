#!/usr/bin/env python3
"""Deterministic structural + semantic validator for Ideias Standard v0.1."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"

SCHEMA_FILES = {
    "project-manifest": "project-manifest.schema.json",
    "standard-lock": "standard-lock.schema.json",
    "context-manifest": "context-manifest.schema.json",
    "artifact-policy": "artifact-policy.schema.json",
    "bundle": "bundle.schema.json",
    "workflow": "workflow.schema.json",
    "change": "change.schema.json",
    "conformance-report": "conformance-report.schema.json",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be an object: {path}")
    return data


def schema_store() -> tuple[dict[str, Any], dict[str, Any]]:
    schemas: dict[str, Any] = {}
    store: dict[str, Any] = {}
    for kind, filename in SCHEMA_FILES.items():
        schema = load_json(SCHEMA_DIR / filename)
        schemas[kind] = schema
        if "$id" in schema:
            store[schema["$id"]] = schema
    return schemas, store


def catalog_ids(path: Path, key: str) -> set[str]:
    data = load_yaml(path)
    return {item["id"] for item in data.get(key, [])}


def adapter_statuses() -> dict[str, str]:
    data = load_yaml(ROOT / "adapters" / "catalog.yaml")
    return {item["id"]: item["status"] for item in data.get("adapters", [])}


def current_version() -> str:
    return (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def detect_kind(data: dict[str, Any], path: Path) -> str:
    name = path.name
    if name == "project-manifest.json" or {"project", "standard", "governance", "context"} <= data.keys():
        return "project-manifest"
    if "standard_version" in data and "template_fingerprint" in data:
        return "standard-lock"
    if "tasks" in data and "budget" in data:
        return "context-manifest"
    if "target" in data and "checks" in data and "result" in data:
        return "conformance-report"
    if "kind" in data and "affected" in data and str(data.get("id", "")).startswith("CHG-"):
        return "change"
    if "steps" in data:
        return "workflow"
    if "profile" in data and "packs" in data and "id" in data:
        return "bundle"
    if "ownership" in data and "source" in data and "fingerprint" in data:
        return "artifact-policy"
    raise ValueError(f"Unable to detect document kind: {path}")


def add_check(checks: list[dict[str, Any]], code: str, status: str, severity: str, message: str, path: str | None = None, rationale: str | None = None) -> None:
    checks.append({
        "code": code,
        "status": status,
        "severity": severity,
        "message": message,
        "path": path,
        "rationale": rationale,
    })


def structural_checks(data: dict[str, Any], kind: str, schemas: dict[str, Any], store: dict[str, Any]) -> list[dict[str, Any]]:
    schema = schemas[kind]
    resolver = RefResolver.from_schema(schema, store=store)
    validator = Draft202012Validator(schema, resolver=resolver)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
    checks: list[dict[str, Any]] = []
    for error in errors:
        pointer = "/" + "/".join(str(p) for p in error.absolute_path) if error.absolute_path else "/"
        add_check(checks, "IS-SCHEMA-001", "FAIL", "HIGH", error.message, pointer)
    if not errors:
        add_check(checks, "IS-SCHEMA-001", "PASS", "INFO", f"{kind} satisfies its JSON Schema")
    return checks


def semantic_checks(data: dict[str, Any], kind: str) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    packs = catalog_ids(ROOT / "packs" / "catalog.yaml", "packs")
    workflows = catalog_ids(ROOT / "workflows" / "catalog.yaml", "workflows")
    adapters = adapter_statuses()

    if kind == "project-manifest":
        unknown = sorted(set(data.get("packs", [])) - packs)
        if unknown:
            add_check(checks, "IS-SEM-001", "FAIL", "HIGH", f"Unknown packs: {', '.join(unknown)}", "/packs")
        else:
            add_check(checks, "IS-SEM-001", "PASS", "INFO", "All manifest packs exist")
        declared = data.get("standard", {}).get("version")
        if declared != current_version():
            add_check(checks, "IS-SEM-006", "FAIL", "HIGH", f"Manifest standard version {declared!r} != supported {current_version()!r}", "/standard/version")
        else:
            add_check(checks, "IS-SEM-006", "PASS", "INFO", "Manifest targets the supported Standard version")

    elif kind == "standard-lock":
        artifact_paths = [a.get("path") for a in data.get("artifacts", [])]
        duplicates = sorted({p for p in artifact_paths if p is not None and artifact_paths.count(p) > 1})
        if duplicates:
            add_check(checks, "IS-SEM-002", "FAIL", "HIGH", f"Duplicate artifact paths: {', '.join(duplicates)}", "/artifacts")
        else:
            add_check(checks, "IS-SEM-002", "PASS", "INFO", "Artifact paths are unique")
        for index, artifact in enumerate(data.get("artifacts", [])):
            if artifact.get("ownership") == "MANAGED" and artifact.get("local_override") is True:
                add_check(checks, "IS-WARN-001", "WARN", "MEDIUM", "MANAGED artifact has a local override; review before upgrade", f"/artifacts/{index}")

    elif kind == "bundle":
        unknown_packs = sorted(set(data.get("packs", [])) - packs)
        if unknown_packs:
            add_check(checks, "IS-SEM-003", "FAIL", "HIGH", f"Bundle references unknown packs: {', '.join(unknown_packs)}", "/packs")
        else:
            add_check(checks, "IS-SEM-003", "PASS", "INFO", "All bundle packs exist")
        workflow = data.get("workflow")
        if workflow is not None and workflow not in workflows:
            add_check(checks, "IS-SEM-004", "FAIL", "HIGH", f"Unknown workflow: {workflow}", "/workflow")
        else:
            add_check(checks, "IS-SEM-004", "PASS", "INFO", "Bundle workflow is available")
        bad_adapters = [a for a in data.get("adapters", []) if adapters.get(a) != "ACTIVE"]
        if bad_adapters:
            add_check(checks, "IS-SEM-005", "FAIL", "HIGH", f"Adapters are missing or not ACTIVE: {', '.join(sorted(bad_adapters))}", "/adapters")
        else:
            add_check(checks, "IS-SEM-005", "PASS", "INFO", "All bundle adapters are ACTIVE")

    elif kind == "workflow":
        ids = [step.get("id") for step in data.get("steps", [])]
        duplicates = sorted({i for i in ids if i is not None and ids.count(i) > 1})
        if duplicates:
            add_check(checks, "IS-SEM-007", "FAIL", "HIGH", f"Duplicate workflow step IDs: {', '.join(duplicates)}", "/steps")
        else:
            add_check(checks, "IS-SEM-007", "PASS", "INFO", "Workflow step IDs are unique")

    return checks


def validate(path: Path, kind: str | None = None) -> dict[str, Any]:
    if path.suffix.lower() in {".yaml", ".yml"}:
        data = load_yaml(path)
    else:
        data = load_json(path)
    kind = kind or detect_kind(data, path)
    schemas, store = schema_store()
    checks = structural_checks(data, kind, schemas, store)
    if not any(c["status"] == "FAIL" for c in checks):
        checks.extend(semantic_checks(data, kind))
    result = "FAIL" if any(c["status"] == "FAIL" for c in checks) else ("WARN" if any(c["status"] == "WARN" for c in checks) else "PASS")
    return {
        "schema_version": "0.1",
        "target": str(path),
        "standard_version": current_version(),
        "result": result,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--kind", choices=sorted(SCHEMA_FILES))
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    try:
        report = validate(args.path.resolve(), args.kind)
    except Exception as exc:
        report = {
            "schema_version": "0.1",
            "target": str(args.path),
            "standard_version": current_version(),
            "result": "FAIL",
            "checks": [{
                "code": "IS-SCHEMA-001",
                "status": "FAIL",
                "severity": "HIGH",
                "message": str(exc),
                "path": None,
                "rationale": None,
            }],
        }
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"{report['result']}: {report['target']}")
        for check in report["checks"]:
            print(f"- {check['status']} {check['code']}: {check['message']}")
    return 1 if report["result"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
