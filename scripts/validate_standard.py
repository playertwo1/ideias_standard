#!/usr/bin/env python3
"""Deterministic structural + semantic validator for Ideias Standard v0.1."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

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


def schema_registry() -> tuple[dict[str, Any], Registry]:
    schemas: dict[str, Any] = {}
    resources: list[tuple[str, Resource[Any]]] = []
    for kind, filename in SCHEMA_FILES.items():
        schema = load_json(SCHEMA_DIR / filename)
        schemas[kind] = schema
        schema_id = schema.get("$id")
        if schema_id:
            resources.append((schema_id, Resource.from_contents(schema)))
    return schemas, Registry().with_resources(resources)


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
    if "strategy" in data and "routes" in data:
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


def structural_checks(data: dict[str, Any], kind: str, schemas: dict[str, Any], registry: Registry) -> list[dict[str, Any]]:
    schema = schemas[kind]
    validator = Draft202012Validator(schema, registry=registry)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
    checks: list[dict[str, Any]] = []
    for error in errors:
        pointer = "/" + "/".join(str(p) for p in error.absolute_path) if error.absolute_path else "/"
        add_check(checks, "IS-SCHEMA-001", "FAIL", "HIGH", error.message, pointer)
    if not errors:
        add_check(checks, "IS-SCHEMA-001", "PASS", "INFO", f"{kind} satisfies its JSON Schema")
    return checks


def check_known_packs(checks: list[dict[str, Any]], values: list[str], path: str, code: str) -> None:
    known = catalog_ids(ROOT / "packs" / "catalog.yaml", "packs")
    unknown = sorted(set(values) - known)
    if unknown:
        add_check(checks, code, "FAIL", "HIGH", f"Unknown packs: {', '.join(unknown)}", path)
    else:
        add_check(checks, code, "PASS", "INFO", "All referenced packs exist", path)


def check_workflow(checks: list[dict[str, Any]], workflow: str | None, path: str) -> None:
    workflows = catalog_ids(ROOT / "workflows" / "catalog.yaml", "workflows")
    if workflow is not None and workflow not in workflows:
        add_check(checks, "IS-SEM-004", "FAIL", "HIGH", f"Unknown workflow: {workflow}", path)
    else:
        add_check(checks, "IS-SEM-004", "PASS", "INFO", "Referenced workflow is available", path)


def check_adapters(checks: list[dict[str, Any]], values: list[str], path: str) -> None:
    adapters = adapter_statuses()
    bad = [adapter for adapter in values if adapters.get(adapter) != "ACTIVE"]
    if bad:
        add_check(checks, "IS-SEM-005", "FAIL", "HIGH", f"Adapters are missing or not ACTIVE: {', '.join(sorted(bad))}", path)
    else:
        add_check(checks, "IS-SEM-005", "PASS", "INFO", "All referenced adapters are ACTIVE", path)


def semantic_checks(data: dict[str, Any], kind: str) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    if kind == "project-manifest":
        check_known_packs(checks, data.get("packs", []), "/packs", "IS-SEM-001")
        declared = data.get("standard", {}).get("version")
        if declared != current_version():
            add_check(checks, "IS-SEM-006", "FAIL", "HIGH", f"Manifest standard version {declared!r} != supported {current_version()!r}", "/standard/version")
        else:
            add_check(checks, "IS-SEM-006", "PASS", "INFO", "Manifest targets the supported Standard version")

    elif kind == "standard-lock":
        check_known_packs(checks, data.get("packs", []), "/packs", "IS-SEM-001")
        check_workflow(checks, data.get("workflow"), "/workflow")
        check_adapters(checks, data.get("adapters", []), "/adapters")
        artifact_paths = [artifact.get("path") for artifact in data.get("artifacts", [])]
        duplicates = sorted({p for p in artifact_paths if p is not None and artifact_paths.count(p) > 1})
        if duplicates:
            add_check(checks, "IS-SEM-002", "FAIL", "HIGH", f"Duplicate artifact paths: {', '.join(duplicates)}", "/artifacts")
        else:
            add_check(checks, "IS-SEM-002", "PASS", "INFO", "Artifact paths are unique")
        for index, artifact in enumerate(data.get("artifacts", [])):
            if artifact.get("ownership") == "MANAGED" and artifact.get("local_override") is True:
                add_check(checks, "IS-WARN-001", "WARN", "MEDIUM", "MANAGED artifact has a local override; review before upgrade", f"/artifacts/{index}")

    elif kind == "bundle":
        check_known_packs(checks, data.get("packs", []), "/packs", "IS-SEM-003")
        check_workflow(checks, data.get("workflow"), "/workflow")
        check_adapters(checks, data.get("adapters", []), "/adapters")

    elif kind == "workflow":
        ids = [step.get("id") for step in data.get("steps", [])]
        duplicates = sorted({step_id for step_id in ids if step_id is not None and ids.count(step_id) > 1})
        if duplicates:
            add_check(checks, "IS-SEM-007", "FAIL", "HIGH", f"Duplicate workflow step IDs: {', '.join(duplicates)}", "/steps")
        else:
            add_check(checks, "IS-SEM-007", "PASS", "INFO", "Workflow step IDs are unique")

    return checks


def validate(path: Path, kind: str | None = None) -> dict[str, Any]:
    data = load_yaml(path) if path.suffix.lower() in {".yaml", ".yml"} else load_json(path)
    kind = kind or detect_kind(data, path)
    schemas, registry = schema_registry()
    checks = structural_checks(data, kind, schemas, registry)
    if not any(check["status"] == "FAIL" for check in checks):
        checks.extend(semantic_checks(data, kind))
    result = "FAIL" if any(check["status"] == "FAIL" for check in checks) else ("WARN" if any(check["status"] == "WARN" for check in checks) else "PASS")
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
