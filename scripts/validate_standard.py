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
    "invariants": "invariants.schema.json",
    "builder-report": "builder-report.schema.json",
    "audit-report": "audit-report.schema.json",
    "orchestration-policy": "orchestration-policy.schema.json",
    "orchestrator-state": "orchestrator-state.schema.json",
}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


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


def catalog_items(path: Path, key: str) -> list[dict[str, Any]]:
    data = load_yaml(path)
    items = data.get(key, [])
    if not isinstance(items, list):
        raise ValueError(f"Catalog key {key!r} must be a list: {path}")
    return items


def catalog_ids(path: Path, key: str) -> set[str]:
    return {item["id"] for item in catalog_items(path, key)}


def adapter_statuses() -> dict[str, str]:
    return {item["id"]: item["status"] for item in catalog_items(ROOT / "adapters" / "catalog.yaml", "adapters")}


def current_version() -> str:
    return (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def detect_kind(data: dict[str, Any], path: Path) -> str:
    name = path.name
    if name == "project-manifest.json" or {"project", "standard", "governance", "context"} <= data.keys():
        return "project-manifest"
    if data.get("role") == "BUILDER":
        return "builder-report"
    if data.get("role") == "AUDITOR":
        return "audit-report"
    if {"builder_role_id", "auditor_role_id", "max_audit_rounds", "immutable_audit_target"} <= data.keys():
        return "orchestration-policy"
    if {"machine_state", "audit_round", "max_audit_rounds", "audit_target_sha"} <= data.keys():
        return "orchestrator-state"
    if "standard_version" in data and "template_fingerprint" in data:
        return "standard-lock"
    if "strategy" in data and "routes" in data:
        return "context-manifest"
    if "target" in data and "checks" in data and "result" in data:
        return "conformance-report"
    if "version" in data and "invariants" in data:
        return "invariants"
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
    checks.append({"code": code, "status": status, "severity": severity, "message": message, "path": path, "rationale": rationale})


def result_from_checks(checks: list[dict[str, Any]]) -> str:
    if any(check["status"] == "FAIL" for check in checks):
        return "FAIL"
    if any(check["status"] == "WARN" for check in checks):
        return "WARN"
    return "PASS"


def structural_checks(data: dict[str, Any], kind: str, schemas: dict[str, Any], registry: Registry) -> list[dict[str, Any]]:
    validator = Draft202012Validator(schemas[kind], registry=registry)
    errors = sorted(validator.iter_errors(data), key=lambda error: list(error.absolute_path))
    checks: list[dict[str, Any]] = []
    for error in errors:
        pointer = "/" + "/".join(str(part) for part in error.absolute_path) if error.absolute_path else "/"
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
        packs = set(data.get("packs", []))
        check_known_packs(checks, list(packs), "/packs", "IS-SEM-001")
        declared = data.get("standard", {}).get("version")
        if declared != current_version():
            add_check(checks, "IS-SEM-006", "FAIL", "HIGH", f"Manifest standard version {declared!r} != supported {current_version()!r}", "/standard/version")
        else:
            add_check(checks, "IS-SEM-006", "PASS", "INFO", "Manifest targets the supported Standard version")
        capabilities = data.get("capabilities", {})
        governance = data.get("governance", {})
        if "sensitive-data" in packs:
            if capabilities.get("human_gates") is not True:
                add_check(checks, "IS-SEM-009", "FAIL", "CRITICAL", "sensitive-data requires capabilities.human_gates=true", "/capabilities/human_gates")
            else:
                add_check(checks, "IS-SEM-009", "PASS", "INFO", "sensitive-data has human gates enabled")
        if "multi-agent" in packs:
            if capabilities.get("independent_audit") is not True:
                add_check(checks, "IS-SEM-010", "FAIL", "CRITICAL", "multi-agent requires capabilities.independent_audit=true", "/capabilities/independent_audit")
            else:
                add_check(checks, "IS-SEM-010", "PASS", "INFO", "multi-agent has independent audit enabled")
            if governance.get("builder") == governance.get("auditor"):
                add_check(checks, "IS-SEM-011", "FAIL", "CRITICAL", "multi-agent requires Builder and Auditor to be distinct", "/governance")
            else:
                add_check(checks, "IS-SEM-011", "PASS", "INFO", "Builder and Auditor are distinct")

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

    elif kind == "invariants":
        ids = [item.get("id") for item in data.get("invariants", [])]
        duplicates = sorted({invariant_id for invariant_id in ids if invariant_id is not None and ids.count(invariant_id) > 1})
        if duplicates:
            add_check(checks, "IS-INV-001", "FAIL", "CRITICAL", f"Duplicate invariant IDs: {', '.join(duplicates)}", "/invariants")
        else:
            add_check(checks, "IS-INV-001", "PASS", "INFO", "Invariant IDs are unique")

    elif kind == "orchestration-policy":
        if data.get("builder_role_id") == data.get("auditor_role_id"):
            add_check(checks, "IS-SEM-012", "FAIL", "CRITICAL", "Orchestration requires distinct Builder and Auditor role IDs", "/")
        else:
            add_check(checks, "IS-SEM-012", "PASS", "INFO", "Orchestration roles are distinct")

    elif kind == "audit-report":
        blocking = [finding for finding in data.get("findings", []) if finding.get("blocking") is True]
        if data.get("audit_result") == "PASS" and blocking:
            add_check(checks, "IS-SEM-014", "FAIL", "CRITICAL", "Audit PASS cannot contain blocking findings", "/findings")
        else:
            add_check(checks, "IS-SEM-014", "PASS", "INFO", "Audit result is consistent with blocking findings")

    elif kind == "orchestrator-state":
        machine = data.get("machine_state")
        target = data.get("audit_target_sha")
        audited = data.get("last_audited_sha")
        result = data.get("last_audit_result")
        approval = data.get("approval")
        if machine == "WAITING_PRODUCT_AUTHORITY" and not (result == "PASS" and target is not None and target == audited and approval is None):
            add_check(checks, "IS-SEM-013", "FAIL", "CRITICAL", "WAITING_PRODUCT_AUTHORITY requires PASS on the exact frozen SHA and no approval yet", "/")
        else:
            add_check(checks, "IS-SEM-013", "PASS", "INFO", "Waiting state is consistent")
        if machine == "GATE_APPROVED":
            valid = bool(approval) and result == "PASS" and target is not None and target == audited and approval.get("audited_sha") == audited and approval.get("gate") == data.get("gate")
            if not valid:
                add_check(checks, "IS-SEM-015", "FAIL", "CRITICAL", "GATE_APPROVED requires explicit approval matching gate and audited SHA", "/approval")
            else:
                add_check(checks, "IS-SEM-015", "PASS", "INFO", "Gate approval matches audited SHA")
        if data.get("audit_round", 0) > data.get("max_audit_rounds", 0):
            add_check(checks, "IS-SEM-016", "FAIL", "HIGH", "audit_round cannot exceed max_audit_rounds", "/audit_round")
        else:
            add_check(checks, "IS-SEM-016", "PASS", "INFO", "Audit round is within policy limit")

    return checks


def validate(path: Path, kind: str | None = None) -> dict[str, Any]:
    data = load_yaml(path) if path.suffix.lower() in {".yaml", ".yml"} else load_json(path)
    kind = kind or detect_kind(data, path)
    schemas, registry = schema_registry()
    checks = structural_checks(data, kind, schemas, registry)
    if not any(check["status"] == "FAIL" for check in checks):
        checks.extend(semantic_checks(data, kind))
    return {"schema_version": "0.1", "target": str(path), "standard_version": current_version(), "result": result_from_checks(checks), "checks": checks}


def duplicate_ids(items: list[dict[str, Any]]) -> list[str]:
    ids = [str(item.get("id")) for item in items]
    return sorted({item_id for item_id in ids if ids.count(item_id) > 1})


def self_check() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    schemas, _ = schema_registry()
    for kind, schema in schemas.items():
        try:
            Draft202012Validator.check_schema(schema)
            add_check(checks, "IS-SELF-001", "PASS", "INFO", f"Schema is valid: {kind}")
        except Exception as exc:
            add_check(checks, "IS-SELF-001", "FAIL", "CRITICAL", f"Invalid schema {kind}: {exc}")

    catalog_specs = [
        (ROOT / "packs" / "catalog.yaml", "packs"),
        (ROOT / "workflows" / "catalog.yaml", "workflows"),
        (ROOT / "bundles" / "catalog.yaml", "bundles"),
        (ROOT / "adapters" / "catalog.yaml", "adapters"),
    ]
    for path, key in catalog_specs:
        items = catalog_items(path, key)
        duplicates = duplicate_ids(items)
        if duplicates:
            add_check(checks, "IS-SELF-002", "FAIL", "CRITICAL", f"Duplicate IDs in {path.relative_to(ROOT)}: {', '.join(duplicates)}")
        else:
            add_check(checks, "IS-SELF-002", "PASS", "INFO", f"Catalog IDs are unique: {path.relative_to(ROOT)}")
        for item in items:
            rel = item.get("path")
            if rel is not None and not (ROOT / rel).exists():
                add_check(checks, "IS-SELF-003", "FAIL", "HIGH", f"Catalog path does not exist: {rel}")

    compatibility = load_yaml(ROOT / "COMPATIBILITY.yaml")
    if compatibility.get("standard_version") != current_version():
        add_check(checks, "IS-SELF-004", "FAIL", "HIGH", "COMPATIBILITY.yaml standard_version does not match VERSION")
    else:
        add_check(checks, "IS-SELF-004", "PASS", "INFO", "Compatibility matrix matches VERSION")

    invariant_report = validate(ROOT / "INVARIANTS.yaml", "invariants")
    add_check(checks, "IS-SELF-005", "PASS" if invariant_report["result"] != "FAIL" else "FAIL", "INFO" if invariant_report["result"] != "FAIL" else "CRITICAL", "Invariant registry is valid" if invariant_report["result"] != "FAIL" else "Invariant registry failed validation")

    for item in catalog_items(ROOT / "bundles" / "catalog.yaml", "bundles"):
        report = validate(ROOT / item["path"], "bundle")
        add_check(checks, "IS-SELF-006", "PASS" if report["result"] != "FAIL" else "FAIL", "INFO" if report["result"] != "FAIL" else "HIGH", f"Bundle {'is valid' if report['result'] != 'FAIL' else 'failed validation'}: {item['id']}")

    for item in catalog_items(ROOT / "workflows" / "catalog.yaml", "workflows"):
        report = validate(ROOT / item["path"], "workflow")
        add_check(checks, "IS-SELF-007", "PASS" if report["result"] != "FAIL" else "FAIL", "INFO" if report["result"] != "FAIL" else "HIGH", f"Workflow {'is valid' if report['result'] != 'FAIL' else 'failed validation'}: {item['id']}")

    policy_path = ROOT / "orchestration" / "builder-auditor-policy.json"
    if policy_path.exists():
        report = validate(policy_path, "orchestration-policy")
        add_check(checks, "IS-SELF-008", "PASS" if report["result"] != "FAIL" else "FAIL", "INFO" if report["result"] != "FAIL" else "CRITICAL", "Orchestration policy is valid" if report["result"] != "FAIL" else "Orchestration policy failed validation")

    return {"schema_version": "0.1", "target": "SELF", "standard_version": current_version(), "result": result_from_checks(checks), "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path)
    parser.add_argument("--kind", choices=sorted(SCHEMA_FILES))
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if not args.self_check and args.path is None:
        parser.error("path is required unless --self-check is used")
    try:
        report = self_check() if args.self_check else validate(args.path.resolve(), args.kind)
        exit_code = 1 if report["result"] == "FAIL" else 0
    except Exception as exc:
        report = {"schema_version": "0.1", "target": str(args.path) if args.path is not None else "SELF", "standard_version": current_version(), "result": "FAIL", "checks": [{"code": "IS-CLI-001", "status": "FAIL", "severity": "HIGH", "message": str(exc), "path": None, "rationale": "Operational error; see CLI_CONTRACT.md"}]}
        exit_code = 2
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"{report['result']}: {report['target']}")
        for check in report["checks"]:
            print(f"- {check['status']} {check['code']}: {check['message']}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
