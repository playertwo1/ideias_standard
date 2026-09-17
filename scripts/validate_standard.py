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
    if (
        name in {"project-manifest.json", "project-manifest.yaml", "project-manifest.yml"}
        or name.endswith(".project.json")
        or name.endswith(".project.yaml")
        or name.endswith(".project.yml")
        or {"project", "standard", "governance", "context"} <= data.keys()
    ):
        return "project-manifest"
    if (
        name in {
            "standard.lock",
            "standard-lock.json",
            "standard.lock.json",
            "standard.lock.yaml",
            "standard.lock.yml",
            "standard-lock.yaml",
            "standard-lock.yml",
        }
        or name.endswith(".standard-lock.json")
        or name.endswith(".standard-lock.yaml")
        or name.endswith(".standard-lock.yml")
        or name.endswith(".lock.json")
        or name.endswith(".lock.yaml")
        or name.endswith(".lock.yml")
        or ("standard_version" in data and "template_fingerprint" in data)
    ):
        return "standard-lock"
    if (
        name in {
            "context-manifest.json",
            "context-manifest.yaml",
            "context-manifest.yml",
            "context.json",
            "context.yaml",
            "context.yml",
        }
        or name.endswith(".context-manifest.json")
        or name.endswith(".context-manifest.yaml")
        or name.endswith(".context-manifest.yml")
        or ("strategy" in data and "routes" in data)
    ):
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
    if (
        name in {"artifact-policy.json", "artifact-policy.yaml", "artifact-policy.yml"}
        or name.endswith(".artifact-policy.json")
        or name.endswith(".artifact-policy.yaml")
        or name.endswith(".artifact-policy.yml")
        or ("ownership" in data and "source" in data and "fingerprint" in data)
    ):
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


def check_project_composition(checks: list[dict[str, Any]], project_dir: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """Validate project-level S1 composition without duplicating document rules."""
    required = {
        "project-manifest": any((project_dir / n).exists() for n in ("project-manifest.json", "project-manifest.yaml", "project-manifest.yml")),
        "standard-lock": any((project_dir / n).exists() for n in ("standard.lock", "standard-lock.json", "standard.lock.yaml", "standard.lock.yml", "standard-lock.yaml", "standard-lock.yml")),
        "context-manifest": any((project_dir / n).exists() for n in ("context-manifest.json", "context-manifest.yaml", "context-manifest.yml", "context.json", "context.yaml", "context.yml")),
    }
    missing = [name for name, present in required.items() if not present]
    if missing:
        add_check(checks, "IS-SEM-028", "FAIL", "HIGH", f"Missing required project contracts: {', '.join(missing)}", "/")
    else:
        add_check(checks, "IS-SEM-028", "PASS", "INFO", "All required project contracts are present", "/")

    compatibility = load_yaml(ROOT / "COMPATIBILITY.yaml")
    compatible = manifest.get("standard", {}).get("version") == compatibility.get("standard_version") == current_version()
    add_check(checks, "IS-SEM-030", "PASS" if compatible else "FAIL", "INFO" if compatible else "HIGH",
              "Project version is compatible with the active matrix" if compatible else "Project version is incompatible with COMPATIBILITY.yaml",
              "/standard/version")

    packs = manifest.get("packs", [])
    pack_catalog = {item["id"]: item for item in catalog_items(ROOT / "packs" / "catalog.yaml", "packs")}
    project_type = manifest.get("project", {}).get("type")
    invalid_packs = [pack for pack in packs if pack not in pack_catalog or not (ROOT / pack_catalog[pack]["path"]).exists()]
    for pack in packs:
        if pack in pack_catalog:
            pack_data = load_yaml(ROOT / pack_catalog[pack]["path"])
            predicates = pack_data.get("applies_when", [])
            typed = [str(predicate).split("==", 1)[1].strip() for predicate in predicates if "project.type ==" in str(predicate)]
            if typed and project_type not in typed:
                invalid_packs.append(pack)
    add_check(checks, "IS-SEM-031", "PASS" if not invalid_packs else "FAIL", "INFO" if not invalid_packs else "HIGH",
              "All declared packs are applicable and available" if not invalid_packs else f"Unavailable applicable packs: {', '.join(sorted(invalid_packs))}", "/packs")

    lock_path = next((project_dir / n for n in ("standard.lock", "standard-lock.json", "standard.lock.yaml", "standard.lock.yml", "standard-lock.yaml", "standard-lock.yml") if (project_dir / n).exists()), None)
    missing_artifacts: list[str] = []
    if lock_path is not None:
        lock_data = load_yaml(lock_path) if lock_path.suffix in {".yaml", ".yml"} else load_json(lock_path)
        for artifact in lock_data.get("artifacts", []):
            if artifact.get("ownership") == "MANAGED" and isinstance(artifact.get("path"), str) and not (project_dir / artifact["path"]).is_file():
                missing_artifacts.append(artifact["path"])
    add_check(checks, "IS-SEM-029", "FAIL" if missing_artifacts else "PASS", "HIGH" if missing_artifacts else "INFO",
              f"Missing MANAGED artifacts: {', '.join(sorted(missing_artifacts))}" if missing_artifacts else "All declared MANAGED artifacts exist", "/artifacts")

    # Workflow applicability is validated against the catalog and its materialized path.
    workflow = manifest.get("workflow")
    if workflow is None:
        for name in ("standard.lock", "standard-lock.json", "standard.lock.yaml", "standard.lock.yml"):
            lock_path = project_dir / name
            if lock_path.exists():
                lock_data = load_yaml(lock_path) if lock_path.suffix in {".yaml", ".yml"} else load_json(lock_path)
                workflow = lock_data.get("workflow")
                break
    workflows = {item["id"]: item for item in catalog_items(ROOT / "workflows" / "catalog.yaml", "workflows")}
    invalid_workflow = workflow is not None and (workflow not in workflows or not (ROOT / workflows[workflow]["path"]).exists())
    add_check(checks, "IS-SEM-032", "PASS" if not invalid_workflow else "FAIL", "INFO" if not invalid_workflow else "HIGH",
              "Declared workflow is applicable and available" if not invalid_workflow else f"Unavailable applicable workflow: {workflow}", "/workflow")
    return checks


def check_artifact_entry(
    checks: list[dict[str, Any]],
    artifact: dict[str, Any],
    pointer_prefix: str,
    known_packs: set[str],
    lock_packs: list[str] | None = None,
) -> tuple[bool, bool, bool, bool]:
    """Validate a single artifact policy entry. Returns (traversal_err, pack_err, profile_err, inv002_err)."""
    traversal_err = False
    pack_err = False
    profile_err = False
    inv002_err = False

    path_ptr = f"{pointer_prefix}/path" if pointer_prefix else "/path"
    pack_ptr = f"{pointer_prefix}/pack" if pointer_prefix else "/pack"
    prof_ptr = f"{pointer_prefix}/profile" if pointer_prefix else "/profile"
    over_ptr = f"{pointer_prefix}/local_override" if pointer_prefix else "/local_override"
    warn_ptr = pointer_prefix if pointer_prefix else "/local_override"

    # 1. Path check IS-SEM-024
    p = artifact.get("path")
    if isinstance(p, str):
        p_norm = p.replace("\\", "/")
        parts = p_norm.split("/")
        if p_norm.startswith("/") or (len(p_norm) > 1 and p_norm[1] == ":") or ".." in parts:
            traversal_err = True
    else:
        traversal_err = True

    if traversal_err:
        add_check(
            checks,
            "IS-SEM-024",
            "FAIL",
            "HIGH",
            f"Artifact path contains absolute path or path traversal (..): {p}",
            path_ptr,
        )

    # 2. Pack check IS-SEM-025
    pack = artifact.get("pack")
    if pack is not None:
        if pack not in known_packs:
            pack_err = True
            add_check(
                checks,
                "IS-SEM-025",
                "FAIL",
                "HIGH",
                f"Artifact references unknown pack: {pack}",
                pack_ptr,
            )
        elif lock_packs is not None and pack not in lock_packs:
            pack_err = True
            add_check(
                checks,
                "IS-SEM-025",
                "FAIL",
                "HIGH",
                f"Artifact pack {pack!r} is not declared in lock packs",
                pack_ptr,
            )

    # 3. Profile check IS-SEM-026
    profile = artifact.get("profile")
    if profile is not None and profile not in {"LIGHT", "STANDARD", "DEEP"}:
        profile_err = True
        add_check(
            checks,
            "IS-SEM-026",
            "FAIL",
            "HIGH",
            f"Invalid artifact profile: {profile}",
            prof_ptr,
        )

    # 4. Invariant INV-002 check IS-SEM-027
    if artifact.get("ownership") == "USER_OWNED" and artifact.get("local_override") is True:
        inv002_err = True
        add_check(
            checks,
            "IS-SEM-027",
            "FAIL",
            "CRITICAL",
            "USER_OWNED artifact cannot have local_override=true (INV-002)",
            over_ptr,
        )

    # 5. Managed override warning IS-WARN-001
    if artifact.get("ownership") == "MANAGED" and artifact.get("local_override") is True:
        add_check(
            checks,
            "IS-WARN-001",
            "WARN",
            "MEDIUM",
            "MANAGED artifact has a local override; review before upgrade",
            warn_ptr,
        )

    return traversal_err, pack_err, profile_err, inv002_err


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
        declared = data.get("standard_version")
        if declared is not None and declared != current_version():
            add_check(checks, "IS-SEM-006", "FAIL", "HIGH", f"Lock standard version {declared!r} != supported {current_version()!r}", "/standard_version")
        elif declared is not None:
            add_check(checks, "IS-SEM-006", "PASS", "INFO", "Lock targets the supported Standard version")
        artifact_paths = [artifact.get("path") for artifact in data.get("artifacts", [])]
        duplicates = sorted({p for p in artifact_paths if p is not None and artifact_paths.count(p) > 1})
        if duplicates:
            add_check(checks, "IS-SEM-002", "FAIL", "HIGH", f"Duplicate artifact paths: {', '.join(duplicates)}", "/artifacts")
        else:
            add_check(checks, "IS-SEM-002", "PASS", "INFO", "Artifact paths are unique")

        known_packs = catalog_ids(ROOT / "packs" / "catalog.yaml", "packs")
        artifacts = data.get("artifacts", [])
        has_t_err = False
        has_pk_err = False
        has_pr_err = False
        has_inv_err = False
        for index, artifact in enumerate(artifacts):
            t_err, pk_err, pr_err, inv_err = check_artifact_entry(
                checks, artifact, f"/artifacts/{index}", known_packs, lock_packs=data.get("packs", [])
            )
            if t_err:
                has_t_err = True
            if pk_err:
                has_pk_err = True
            if pr_err:
                has_pr_err = True
            if inv_err:
                has_inv_err = True

        if not has_t_err:
            add_check(checks, "IS-SEM-024", "PASS", "INFO", "All artifact paths are valid relative paths", "/artifacts")
        if not has_pk_err:
            add_check(checks, "IS-SEM-025", "PASS", "INFO", "All artifact pack references are valid", "/artifacts")
        if not has_pr_err:
            add_check(checks, "IS-SEM-026", "PASS", "INFO", "All artifact profiles are valid", "/artifacts")
        if not has_inv_err:
            add_check(checks, "IS-SEM-027", "PASS", "INFO", "All artifact ownership definitions comply with INV-002", "/artifacts")

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

    elif kind == "context-manifest":
        routes = data.get("routes", {})
        has_traversal_or_absolute = False
        duplicate_across_categories = []

        for route_name, route_spec in routes.items():
            if not isinstance(route_spec, dict):
                continue
            req_set = set(route_spec.get("required", []))
            cond_set = set(route_spec.get("conditional", []))
            disc_set = set(route_spec.get("discovery", []))

            # Check disjointness across categories in the same route
            overlap_req_cond = req_set & cond_set
            overlap_req_disc = req_set & disc_set
            overlap_cond_disc = cond_set & disc_set
            all_overlaps = overlap_req_cond | overlap_req_disc | overlap_cond_disc
            if all_overlaps:
                duplicate_across_categories.append(f"route '{route_name}': {', '.join(sorted(all_overlaps))}")

            # Check path traversal or absolute paths
            all_paths = list(route_spec.get("required", [])) + list(route_spec.get("conditional", [])) + list(route_spec.get("discovery", []))
            for p in all_paths:
                if not isinstance(p, str):
                    continue
                p_norm = p.replace("\\", "/")
                file_part = p_norm.split("#")[0]
                if file_part.startswith("/") or (len(file_part) > 1 and file_part[1] == ":") or ".." in file_part.split("/"):
                    has_traversal_or_absolute = True

        if has_traversal_or_absolute:
            add_check(checks, "IS-SEM-021", "FAIL", "HIGH", "Context routes contain absolute paths or path traversal (..)", "/routes")
        else:
            add_check(checks, "IS-SEM-021", "PASS", "INFO", "Context route paths are valid relative paths")

        if duplicate_across_categories:
            add_check(checks, "IS-SEM-022", "FAIL", "HIGH", f"Overlapping paths across route categories: {'; '.join(duplicate_across_categories)}", "/routes")
        else:
            add_check(checks, "IS-SEM-022", "PASS", "INFO", "Route categories are mutually disjoint")

        budgets = data.get("budgets")
        if isinstance(budgets, dict):
            bootstrap = budgets.get("bootstrap_target_max_bytes")
            task_budget = budgets.get("task_target_max_bytes")
            if bootstrap is not None and task_budget is not None and bootstrap > task_budget:
                add_check(checks, "IS-SEM-023", "FAIL", "MEDIUM", f"bootstrap_target_max_bytes ({bootstrap}) exceeds task_target_max_bytes ({task_budget})", "/budgets/bootstrap_target_max_bytes")
            else:
                add_check(checks, "IS-SEM-023", "PASS", "INFO", "Context budgets are logically consistent")

    elif kind == "artifact-policy":
        known_packs = catalog_ids(ROOT / "packs" / "catalog.yaml", "packs")
        t_err, pk_err, pr_err, inv_err = check_artifact_entry(
            checks, data, "", known_packs, lock_packs=None
        )
        if not t_err:
            add_check(checks, "IS-SEM-024", "PASS", "INFO", "Artifact path is a valid relative path", "/path")
        if not pk_err:
            add_check(checks, "IS-SEM-025", "PASS", "INFO", "Artifact pack is valid or not specified", "/pack" if data.get("pack") is not None else "/")
        if not pr_err:
            add_check(checks, "IS-SEM-026", "PASS", "INFO", "Artifact profile is valid or not specified", "/profile" if data.get("profile") is not None else "/")
        if not inv_err:
            add_check(checks, "IS-SEM-027", "PASS", "INFO", "Artifact ownership complies with INV-002", "/")

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
