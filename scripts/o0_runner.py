#!/usr/bin/env python3
"""Provider-neutral operational runner for one Builder/Auditor handoff."""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

from scripts.orchestrate_handoffs import (
    HandoffError,
    audit_handoff,
    builder_handoff,
    load_json,
    next_actor,
    status,
    validate_with_schema,
    write_json,
)

REQUIRED_CONFIG = {
    "repository",
    "state_path",
    "reports_dir",
    "builder_workspace",
    "audit_workspaces",
    "builder_command",
    "auditor_command",
}

_LANDLOCK_CREATE_RULESET = 444
_LANDLOCK_ADD_RULE = 445
_LANDLOCK_RESTRICT_SELF = 446
_LANDLOCK_RULE_PATH_BENEATH = 1
_LANDLOCK_CREATE_RULESET_VERSION = 1
_PR_SET_NO_NEW_PRIVS = 38

_WRITE_FILE = 1 << 1
_REMOVE_DIR = 1 << 4
_REMOVE_FILE = 1 << 5
_MAKE_CHAR = 1 << 6
_MAKE_DIR = 1 << 7
_MAKE_REG = 1 << 8
_MAKE_SOCK = 1 << 9
_MAKE_FIFO = 1 << 10
_MAKE_BLOCK = 1 << 11
_MAKE_SYM = 1 << 12
_REFER = 1 << 13
_TRUNCATE = 1 << 14
_EVIDENCE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class _RulesetAttr(ctypes.Structure):
    _fields_ = [("handled_access_fs", ctypes.c_uint64)]


class _PathBeneathAttr(ctypes.Structure):
    _fields_ = [
        ("allowed_access", ctypes.c_uint64),
        ("parent_fd", ctypes.c_int32),
        ("reserved", ctypes.c_uint32),
    ]


def load_config(path: Path) -> dict[str, Any]:
    data = load_json(path)
    missing = sorted(REQUIRED_CONFIG - data.keys())
    if missing:
        raise HandoffError(f"Runner config missing: {', '.join(missing)}")
    for key in ("builder_command", "auditor_command"):
        if not isinstance(data[key], list) or not data[key] or not all(
            isinstance(item, str) and item for item in data[key]
        ):
            raise HandoffError(f"{key} must be a non-empty string array")
    return data


def canonical_json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def store_evidence(
    root: Path,
    *,
    evidence_id: str,
    content: str,
    current: dict[str, Any],
) -> dict[str, str]:
    if not _EVIDENCE_ID.fullmatch(evidence_id):
        raise HandoffError("Unsafe evidence_id")
    envelope = {
        "schema_version": "0.1",
        "evidence_id": evidence_id,
        "run_id": current["run_id"],
        "audit_round": current["audit_round"],
        "audit_target_sha": current["audit_target_sha"],
        "content": content,
    }
    validate_with_schema(envelope, "evidence")
    canonical = canonical_json_bytes(envelope)
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{evidence_id}.json"
    digest = hashlib.sha256(canonical).hexdigest()
    try:
        with path.open("xb") as stream:
            stream.write(canonical)
    except FileExistsError as exc:
        if path.read_bytes() != canonical:
            raise HandoffError(f"Evidence ID already exists: {evidence_id}") from exc
    return {"evidence_id": evidence_id, "sha256": digest}


def evidence_id(kind: str, source_id: str, current: dict[str, Any], content: str = "") -> str:
    identity = f"{current['run_id']}:{current['audit_round']}:{current['audit_target_sha']}:{kind}:{source_id}:{content}"
    return f"r{current['audit_round']}-{kind}-{hashlib.sha256(identity.encode('utf-8')).hexdigest()[:16]}"


def resolve_evidence(
    root: Path,
    reference: dict[str, str],
    current: dict[str, Any],
) -> dict[str, Any]:
    evidence_id = reference.get("evidence_id")
    digest = reference.get("sha256")
    if not isinstance(evidence_id, str) or not _EVIDENCE_ID.fullmatch(evidence_id):
        raise HandoffError("Invalid evidence reference ID")
    if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
        raise HandoffError("Invalid evidence reference digest")
    path = root / f"{evidence_id}.json"
    if not path.is_file():
        raise HandoffError(f"Evidence does not exist: {evidence_id}")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise HandoffError(f"Evidence digest mismatch: {evidence_id}")
    envelope = load_json(path)
    validate_with_schema(envelope, "evidence")
    if raw != canonical_json_bytes(envelope):
        raise HandoffError(f"Evidence is not canonically encoded: {evidence_id}")
    if (
        envelope["evidence_id"] != evidence_id
        or envelope["run_id"] != current.get("run_id")
        or envelope["audit_round"] != current.get("audit_round")
        or envelope["audit_target_sha"] != current.get("audit_target_sha")
    ):
        raise HandoffError(f"Evidence is linked to another audit: {evidence_id}")
    return envelope


def canonicalize_report_evidence(
    report_path: Path,
    report_kind: str,
    current: dict[str, Any],
    evidence_root: Path,
) -> dict[str, Any]:
    payload = load_json(report_path)
    collections = [payload.get("checks", [])]
    kinds = [f"{report_kind}-check"]
    if report_kind == "audit":
        collections.append(payload.get("findings", []))
        kinds.append("audit-finding")
    for items, kind in zip(collections, kinds):
        for item in items:
            raw = item.get("evidence")
            if isinstance(raw, str):
                item["evidence"] = store_evidence(
                    evidence_root,
                    evidence_id=evidence_id(kind, item.get("id", "missing"), current, raw),
                    content=raw,
                    current=current,
                )
            elif isinstance(raw, dict):
                resolve_evidence(evidence_root, raw, current)
            else:
                raise HandoffError("Report evidence must be text input or a valid reference")
    validate_with_schema(payload, report_kind)
    write_json(report_path, payload)
    return payload


def resolve_path(config_path: Path, value: str) -> Path:
    path = Path(value)
    return path.resolve() if path.is_absolute() else (config_path.parent / path).resolve()


def _overlap(left: Path, right: Path) -> bool:
    return left == right or left in right.parents or right in left.parents


def validate_workspaces(builder: Path, audits: Path) -> None:
    if _overlap(builder, audits):
        raise HandoffError("Builder and Auditor workspace roots must be separate")


def validate_auditor_boundaries(state: Path, audits: Path, reports: Path) -> None:
    if _overlap(reports, state) or _overlap(reports, audits):
        raise HandoffError("Auditor report path must not expose state or audit workspace to writes")


def verify_commit(repository: Path, sha: str) -> None:
    result = subprocess.run(
        ["git", "-C", str(repository), "cat-file", "-e", f"{sha}^{{commit}}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise HandoffError(f"Unknown result SHA: {sha}")


def git_head(workspace: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(workspace), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise HandoffError("Cannot resolve workspace HEAD")
    return result.stdout.strip()


def make_read_only(root: Path) -> None:
    for path in [root, *root.rglob("*")]:
        mode = path.stat().st_mode
        path.chmod(mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))


def prepare_audit_workspace(repository: Path, audit_root: Path, sha: str) -> Path:
    verify_commit(repository, sha)
    audit_root.mkdir(parents=True, exist_ok=True)
    workspace = audit_root / sha
    if workspace.exists():
        if git_head(workspace) != sha:
            raise HandoffError("Existing audit workspace does not match audit_target_sha")
    else:
        result = subprocess.run(
            ["git", "-C", str(repository), "worktree", "add", "--detach", str(workspace), sha],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise HandoffError(f"Cannot create audit workspace: {result.stderr.strip()}")
    make_read_only(workspace)
    return workspace


def _landlock_write_access(abi: int) -> int:
    access = (
        _WRITE_FILE
        | _REMOVE_DIR
        | _REMOVE_FILE
        | _MAKE_CHAR
        | _MAKE_DIR
        | _MAKE_REG
        | _MAKE_SOCK
        | _MAKE_FIFO
        | _MAKE_BLOCK
        | _MAKE_SYM
    )
    if abi >= 2:
        access |= _REFER
    if abi >= 3:
        access |= _TRUNCATE
    return access


def _auditor_write_sandbox(allowed_directory: Path):
    """Return a child-only Landlock setup; fail closed when unavailable."""
    allowed_directory = allowed_directory.resolve()

    def restrict() -> None:
        libc = ctypes.CDLL(None, use_errno=True)
        syscall = libc.syscall
        abi = syscall(
            _LANDLOCK_CREATE_RULESET,
            ctypes.c_void_p(),
            ctypes.c_size_t(0),
            ctypes.c_uint(_LANDLOCK_CREATE_RULESET_VERSION),
        )
        if abi < 1:
            os._exit(126)
        access = _landlock_write_access(abi)
        ruleset_attr = _RulesetAttr(access)
        ruleset_fd = syscall(
            _LANDLOCK_CREATE_RULESET,
            ctypes.byref(ruleset_attr),
            ctypes.sizeof(ruleset_attr),
            ctypes.c_uint(0),
        )
        if ruleset_fd < 0:
            os._exit(126)
        parent_fd = os.open(allowed_directory, os.O_PATH | os.O_CLOEXEC)
        try:
            path_attr = _PathBeneathAttr(access, parent_fd, 0)
            if syscall(
                _LANDLOCK_ADD_RULE,
                ruleset_fd,
                _LANDLOCK_RULE_PATH_BENEATH,
                ctypes.byref(path_attr),
                ctypes.c_uint(0),
            ) != 0:
                os._exit(126)
            if libc.prctl(_PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0:
                os._exit(126)
            if syscall(_LANDLOCK_RESTRICT_SELF, ruleset_fd, ctypes.c_uint(0)) != 0:
                os._exit(126)
        finally:
            os.close(parent_fd)
            os.close(ruleset_fd)

    return restrict


def run_actor(
    command: list[str],
    workspace: Path,
    report: Path,
    env: dict[str, str],
    *,
    write_sandbox: bool = False,
) -> None:
    report.parent.mkdir(parents=True, exist_ok=True)
    process = subprocess.run(
        command,
        cwd=workspace,
        env={**os.environ, **env, "IDEAS_STANDARD_REPORT": str(report)},
        check=False,
        preexec_fn=_auditor_write_sandbox(report.parent) if write_sandbox else None,
    )
    if process.returncode == 126 and write_sandbox:
        raise HandoffError("Auditor write sandbox is unavailable; refusing unsafe execution")
    if process.returncode != 0:
        raise HandoffError(f"Actor command failed with exit code {process.returncode}")
    if not report.is_file():
        raise HandoffError(f"Actor did not produce report: {report}")


def write_state_snapshot(state_path: Path, audit_root: Path, target: str) -> Path:
    snapshot_root = audit_root / "state-snapshots"
    snapshot_root.mkdir(parents=True, exist_ok=True)
    snapshot = snapshot_root / f"{target}.json"
    snapshot.write_bytes(state_path.read_bytes())
    snapshot.chmod(snapshot.stat().st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
    return snapshot


def verify_audit_after(
    workspace: Path,
    state_path: Path,
    target: str,
    state_before: bytes,
) -> None:
    if state_path.read_bytes() != state_before:
        raise HandoffError("Canonical state changed during Auditor execution")
    if status(state_path).get("audit_target_sha") != target:
        raise HandoffError("audit_target_sha changed during Auditor execution")
    if git_head(workspace) != target:
        raise HandoffError("Auditor workspace HEAD changed from audit_target_sha")
    dirty = subprocess.run(
        ["git", "-C", str(workspace), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,
    )
    if dirty.returncode != 0 or dirty.stdout:
        raise HandoffError("Auditor modified or invalidated the frozen audit workspace")


def prepare_builder_findings(
    current: dict[str, Any],
    reports_dir: Path,
) -> Path | None:
    if current["machine_state"] != "FIX_REQUIRED":
        return None
    if current.get("last_audit_result") != "FAIL" or current.get("audit_round", 0) < 1:
        raise HandoffError("FIX_REQUIRED requires a recorded FAIL audit round")
    report_ref = current.get("last_audit_report")
    if not report_ref:
        raise HandoffError("FIX_REQUIRED requires last_audit_report")
    report = canonicalize_report_evidence(
        Path(report_ref), "audit", current, Path(report_ref).parent / "evidence"
    )
    target = current.get("audit_target_sha")
    if (
        report["audit_result"] != "FAIL"
        or report["audited_sha"] != target
        or current.get("last_audited_sha") != target
    ):
        raise HandoffError("Audit findings do not match the current failed audit target")
    findings = []
    for finding in report["findings"]:
        forwarded = dict(finding)
        resolve_evidence(Path(report_ref).parent / "evidence", finding["evidence"], current)
        findings.append(forwarded)
    handoff = reports_dir / "builder-findings.json"
    write_json(
        handoff,
        {
            "audit_target_sha": target,
            "audit_round": current["audit_round"],
            "findings": findings,
        },
    )
    validate_builder_findings_handoff(current, handoff)
    return handoff


def validate_builder_findings_handoff(current: dict[str, Any], handoff: Path) -> None:
    payload = load_json(handoff)
    validate_with_schema(payload, "builder-findings")
    if (
        payload["audit_target_sha"] != current.get("audit_target_sha")
        or payload["audit_round"] != current.get("audit_round")
    ):
        raise HandoffError("Builder findings are not linked to the current audit round")
    for finding in payload["findings"]:
        resolve_evidence(handoff.parent / "evidence", finding["evidence"], current)


def prepare_reaudit_handoff(
    current: dict[str, Any],
    builder_report: dict[str, Any],
    repository: Path,
    findings_handoff: Path,
    reports_dir: Path,
) -> Path:
    previous_sha = current["last_audited_sha"]
    new_sha = builder_report["result_sha"]
    findings_payload = load_json(findings_handoff)
    audit_payload = load_json(Path(current["last_audit_report"]))
    validate_with_schema(audit_payload, "audit")
    validate_builder_findings_handoff(current, findings_handoff)
    forwarded_findings = findings_payload["findings"]
    if len(forwarded_findings) != len(audit_payload["findings"]):
        raise HandoffError("Reaudit findings are not linked to the corrected audit")
    evidence_root = reports_dir / "evidence"
    reaudit_findings = []
    for forwarded, source in zip(forwarded_findings, audit_payload["findings"]):
        forwarded_without_evidence = {key: value for key, value in forwarded.items() if key != "evidence"}
        source_without_evidence = {key: value for key, value in source.items() if key != "evidence"}
        resolved = resolve_evidence(findings_handoff.parent / "evidence", forwarded["evidence"], current)
        source_resolved = resolve_evidence(Path(current["last_audit_report"]).parent / "evidence", source["evidence"], current)
        if forwarded_without_evidence != source_without_evidence or resolved["content"] != source_resolved["content"]:
            raise HandoffError("Reaudit findings are not linked to the corrected audit")
        reaudit_finding = dict(forwarded)
        reaudit_finding["evidence"] = store_evidence(
            evidence_root,
            evidence_id=forwarded["evidence"]["evidence_id"],
            content=resolved["content"],
            current=current,
        )
        reaudit_findings.append(reaudit_finding)
    if (
        findings_payload.get("audit_target_sha") != previous_sha
        or findings_payload.get("audit_round") != current["audit_round"]
    ):
        raise HandoffError("Reaudit findings are not linked to the corrected audit")

    changed_paths = reaudit_changed_paths(repository, previous_sha, new_sha)
    declared_paths = sorted(builder_report["changed_paths"])
    findings = audit_payload["findings"]
    checks = audit_payload["checks"]
    source_evidence_root = Path(current["last_audit_report"]).parent / "evidence"
    context_findings = [
        {**finding, "evidence": resolve_evidence(source_evidence_root, finding["evidence"], current)["content"]}
        for finding in findings
    ]
    context_checks = [
        {**check, "evidence": resolve_evidence(source_evidence_root, check["evidence"], current)["content"]}
        for check in checks
    ]
    reasons = reaudit_context_reasons(
        context_findings,
        context_checks,
        changed_paths,
        declared_paths,
        audit_payload["residual_risks"],
    )

    payload = {
        "schema_version": "0.1",
        "previous_audited_sha": previous_sha,
        "new_audit_target_sha": new_sha,
        "audit_round": current["audit_round"],
        "context_mode": "FULL" if reasons else "DELTA",
        "full_context_reasons": reasons,
        "findings": reaudit_findings,
        "changed_paths": changed_paths,
        "declared_changed_paths": declared_paths,
        "reusable_evidence": [
            {
                "check_id": check["id"],
                "status": check["status"],
                "evidence": store_evidence(
                    evidence_root,
                    evidence_id=evidence_id(
                        "check",
                        check["id"],
                        current,
                        resolve_evidence(source_evidence_root, check["evidence"], current)["content"],
                    ),
                    content=resolve_evidence(source_evidence_root, check["evidence"], current)["content"],
                    current=current,
                ),
            }
            for check in checks
        ],
    }
    validate_with_schema(payload, "reaudit")
    handoff = reports_dir / "reaudit-handoff.json"
    write_json(handoff, payload)
    return handoff


def reaudit_changed_paths(repository: Path, previous_sha: str, new_sha: str) -> list[str]:
    diff = subprocess.run(
        ["git", "-C", str(repository), "diff", "--name-only", f"{previous_sha}..{new_sha}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if diff.returncode != 0:
        raise HandoffError("Cannot resolve reaudit delta")
    return sorted(path for path in diff.stdout.splitlines() if path)


def reaudit_context_reasons(
    findings: list[dict[str, Any]],
    checks: list[dict[str, Any]],
    changed_paths: list[str],
    declared_paths: list[str],
    residual_risks: list[Any],
) -> list[str]:
    reasons = []
    if changed_paths != declared_paths:
        reasons.append("OUT_OF_SCOPE_CHANGE")
    if (
        not findings
        or any(not finding.get("evidence") for finding in findings)
        or not checks
        or any(not check.get("evidence") for check in checks)
    ):
        reasons.append("MISSING_EVIDENCE")
    if any(finding["severity"] in {"HIGH", "CRITICAL"} for finding in findings) or residual_risks:
        reasons.append("MATERIAL_RISK")
    return reasons


def validate_reaudit_handoff(current: dict[str, Any], handoff: Path, repository: Path) -> None:
    payload = load_json(handoff)
    validate_with_schema(payload, "reaudit")
    audit_payload = load_json(Path(current["last_audit_report"]))
    validate_with_schema(audit_payload, "audit")
    builder_report_ref = current.get("last_builder_report")
    if not builder_report_ref:
        raise HandoffError("Reaudit requires the canonical Builder report")
    builder_payload = load_json(Path(builder_report_ref))
    validate_with_schema(builder_payload, "builder")
    canonical_declared_paths = sorted(builder_payload["changed_paths"])
    if (
        builder_payload["result_sha"] != current["audit_target_sha"]
        or payload["declared_changed_paths"] != canonical_declared_paths
    ):
        raise HandoffError("Reaudit handoff differs from the canonical Builder report")
    evidence_context = {**current, "audit_target_sha": payload["previous_audited_sha"]}
    if len(payload["findings"]) != len(audit_payload["findings"]):
        raise HandoffError("Reaudit handoff is inconsistent with canonical evidence")
    for forwarded, source in zip(payload["findings"], audit_payload["findings"]):
        forwarded_without_evidence = {key: value for key, value in forwarded.items() if key != "evidence"}
        source_without_evidence = {key: value for key, value in source.items() if key != "evidence"}
        resolved = resolve_evidence(handoff.parent / "evidence", forwarded["evidence"], evidence_context)
        source_resolved = resolve_evidence(Path(current["last_audit_report"]).parent / "evidence", source["evidence"], evidence_context)
        if forwarded_without_evidence != source_without_evidence or resolved["content"] != source_resolved["content"]:
            raise HandoffError("Reaudit handoff is inconsistent with canonical evidence")
    reusable_evidence = payload["reusable_evidence"]
    if len(reusable_evidence) != len(audit_payload["checks"]):
        raise HandoffError("Reaudit handoff is inconsistent with canonical evidence")
    for forwarded, source in zip(reusable_evidence, audit_payload["checks"]):
        resolved = resolve_evidence(handoff.parent / "evidence", forwarded["evidence"], evidence_context)
        source_resolved = resolve_evidence(Path(current["last_audit_report"]).parent / "evidence", source["evidence"], evidence_context)
        if (
            forwarded["check_id"] != source["id"]
            or forwarded["status"] != source["status"]
            or resolved["content"] != source_resolved["content"]
        ):
            raise HandoffError("Reaudit handoff is inconsistent with canonical evidence")
    changed_paths = reaudit_changed_paths(
        repository, payload["previous_audited_sha"], payload["new_audit_target_sha"]
    )
    context_findings = [
        {**finding, "evidence": resolve_evidence(Path(current["last_audit_report"]).parent / "evidence", finding["evidence"], evidence_context)["content"]}
        for finding in audit_payload["findings"]
    ]
    context_checks = [
        {**check, "evidence": resolve_evidence(Path(current["last_audit_report"]).parent / "evidence", check["evidence"], evidence_context)["content"]}
        for check in audit_payload["checks"]
    ]
    reasons = reaudit_context_reasons(
        context_findings,
        context_checks,
        changed_paths,
        canonical_declared_paths,
        audit_payload["residual_risks"],
    )
    if (
        payload["new_audit_target_sha"] != current["audit_target_sha"]
        or payload["previous_audited_sha"] != audit_payload["audited_sha"]
        or payload["audit_round"] != current["audit_round"]
        or payload["changed_paths"] != changed_paths
    ):
        raise HandoffError("Reaudit handoff is inconsistent with canonical evidence")
    if payload["full_context_reasons"] != reasons or payload["context_mode"] != ("FULL" if reasons else "DELTA"):
        raise HandoffError("Reaudit context decision is inconsistent")



def validate_builder_result(
    current: dict[str, Any],
    payload: dict[str, Any],
    repository: Path,
    findings_handoff: Path | None,
    findings_before: bytes | None,
    builder_workspace: Path | None = None,
) -> None:
    validation_payload = json.loads(json.dumps(payload))
    for check in validation_payload.get("checks", []):
        if isinstance(check.get("evidence"), str):
            check["evidence"] = {"evidence_id": "transient", "sha256": "0" * 64}
    validate_with_schema(validation_payload, "builder")
    result_sha = payload["result_sha"]
    verify_commit(repository, result_sha)
    previous_target = current.get("audit_target_sha")
    if current["machine_state"] == "FIX_REQUIRED" and (
        not previous_target or result_sha == previous_target
    ):
        raise HandoffError("Builder correction must produce a new SHA")
    if git_head(builder_workspace or repository) != result_sha:
        raise HandoffError("Builder report result_sha does not match Builder workspace HEAD")
    if current["machine_state"] != "FIX_REQUIRED":
        return
    if findings_handoff is None or findings_before is None:
        raise HandoffError("Builder correction requires findings from the failed audit")
    if not findings_handoff.is_file() or findings_handoff.read_bytes() != findings_before:
        raise HandoffError("Builder findings changed during correction")
    findings = load_json(findings_handoff)
    if (
        findings.get("audit_target_sha") != previous_target
        or findings.get("audit_round") != current.get("audit_round")
    ):
        raise HandoffError("Builder findings are not linked to the corrected audit round")


def run_once(config_path: Path) -> dict[str, Any]:
    config_path = config_path.resolve()
    config = load_config(config_path)
    repository = resolve_path(config_path, config["repository"])
    state_path = resolve_path(config_path, config["state_path"])
    reports_dir = resolve_path(config_path, config["reports_dir"])
    builder_workspace = resolve_path(config_path, config["builder_workspace"])
    audit_root = resolve_path(config_path, config["audit_workspaces"])
    validate_workspaces(builder_workspace, audit_root)
    validate_auditor_boundaries(state_path, audit_root, reports_dir)

    current = status(state_path)
    actor = next_actor(current)
    common_env = {
        "IDEAS_STANDARD_PROJECT_ID": current["project_id"],
        "IDEAS_STANDARD_PHASE": current["phase"],
        "IDEAS_STANDARD_GATE": current["gate"],
    }

    if actor == "BUILDER":
        if not builder_workspace.is_dir() or not os.access(builder_workspace, os.W_OK):
            raise HandoffError("Builder workspace must exist and be writable")
        report = reports_dir / "builder-report.json"
        builder_env = {**common_env, "IDEAS_STANDARD_STATE": str(state_path)}
        findings_handoff = prepare_builder_findings(current, reports_dir)
        findings_before = None
        if findings_handoff is not None:
            builder_env["IDEAS_STANDARD_FINDINGS"] = str(findings_handoff)
            findings_before = findings_handoff.read_bytes()
        run_actor(
            config["builder_command"],
            builder_workspace,
            report,
            builder_env,
        )
        payload = load_json(report)
        report_context = {**current, "audit_target_sha": payload.get("result_sha")}
        payload = canonicalize_report_evidence(report, "builder", report_context, reports_dir / "evidence")
        validate_builder_result(
            current,
            payload,
            repository,
            findings_handoff,
            findings_before,
            builder_workspace,
        )
        if current["machine_state"] == "FIX_REQUIRED":
            prepare_reaudit_handoff(
                current,
                payload,
                repository,
                findings_handoff,
                reports_dir,
            )
        return builder_handoff(state_path, report)

    if actor == "AUDITOR":
        target = current.get("audit_target_sha")
        if not target:
            raise HandoffError("Auditor requires audit_target_sha")
        auditor_env = {
            **common_env,
            "IDEAS_STANDARD_AUDIT_TARGET_SHA": target,
        }
        if current["audit_round"] > 0:
            reaudit_handoff = reports_dir / "reaudit-handoff.json"
            if not reaudit_handoff.is_file():
                raise HandoffError("Reaudit requires reaudit-handoff.json")
            validate_reaudit_handoff(current, reaudit_handoff, repository)
            auditor_env["IDEAS_STANDARD_REAUDIT_HANDOFF"] = str(reaudit_handoff)
        workspace = prepare_audit_workspace(repository, audit_root, target)
        snapshot = write_state_snapshot(state_path, audit_root, target)
        state_before = state_path.read_bytes()
        report = reports_dir / "audit-report.json"
        auditor_env["IDEAS_STANDARD_STATE_SNAPSHOT"] = str(snapshot)
        run_actor(
            config["auditor_command"],
            workspace,
            report,
            auditor_env,
            write_sandbox=True,
        )
        verify_audit_after(workspace, state_path, target, state_before)
        audit_context = {**current, "audit_round": current["audit_round"] + 1}
        canonicalize_report_evidence(report, "audit", audit_context, reports_dir / "evidence")
        return audit_handoff(state_path, report)

    return current


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = run_once(args.config)
        print(json.dumps({**result, "next_actor": next_actor(result)}, ensure_ascii=False, indent=2))
        return 0
    except (HandoffError, OSError, json.JSONDecodeError) as exc:
        print(f"RUNNER ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
