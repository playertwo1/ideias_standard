#!/usr/bin/env python3
"""Provider-neutral operational runner for one Builder/Auditor handoff."""
from __future__ import annotations

import argparse
import ctypes
import json
import os
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
        raise HandoffError("Cannot resolve Auditor workspace HEAD")
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
        run_actor(
            config["builder_command"],
            builder_workspace,
            report,
            {**common_env, "IDEAS_STANDARD_STATE": str(state_path)},
        )
        payload = load_json(report)
        verify_commit(repository, payload.get("result_sha", ""))
        return builder_handoff(state_path, report)

    if actor == "AUDITOR":
        target = current.get("audit_target_sha")
        if not target:
            raise HandoffError("Auditor requires audit_target_sha")
        workspace = prepare_audit_workspace(repository, audit_root, target)
        snapshot = write_state_snapshot(state_path, audit_root, target)
        state_before = state_path.read_bytes()
        report = reports_dir / "audit-report.json"
        run_actor(
            config["auditor_command"],
            workspace,
            report,
            {
                **common_env,
                "IDEAS_STANDARD_STATE_SNAPSHOT": str(snapshot),
                "IDEAS_STANDARD_AUDIT_TARGET_SHA": target,
            },
            write_sandbox=True,
        )
        verify_audit_after(workspace, state_path, target, state_before)
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
