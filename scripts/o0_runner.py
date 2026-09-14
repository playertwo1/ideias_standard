#!/usr/bin/env python3
"""Provider-neutral operational runner for one Builder/Auditor handoff."""
from __future__ import annotations

import argparse
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


def validate_workspaces(builder: Path, audits: Path) -> None:
    if builder == audits or builder in audits.parents or audits in builder.parents:
        raise HandoffError("Builder and Auditor workspace roots must be separate")


def verify_commit(repository: Path, sha: str) -> None:
    result = subprocess.run(
        ["git", "-C", str(repository), "cat-file", "-e", f"{sha}^{{commit}}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise HandoffError(f"Unknown result SHA: {sha}")


def make_read_only(root: Path) -> None:
    for path in [root, *root.rglob("*")]:
        mode = path.stat().st_mode
        path.chmod(mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))


def prepare_audit_workspace(repository: Path, audit_root: Path, sha: str) -> Path:
    verify_commit(repository, sha)
    audit_root.mkdir(parents=True, exist_ok=True)
    workspace = audit_root / sha
    if workspace.exists():
        head = subprocess.run(
            ["git", "-C", str(workspace), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
        if head.returncode != 0 or head.stdout.strip() != sha:
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


def run_actor(command: list[str], workspace: Path, report: Path, env: dict[str, str]) -> None:
    report.parent.mkdir(parents=True, exist_ok=True)
    process = subprocess.run(
        command,
        cwd=workspace,
        env={**os.environ, **env, "IDEAS_STANDARD_REPORT": str(report)},
        check=False,
    )
    if process.returncode != 0:
        raise HandoffError(f"Actor command failed with exit code {process.returncode}")
    if not report.is_file():
        raise HandoffError(f"Actor did not produce report: {report}")


def run_once(config_path: Path) -> dict[str, Any]:
    config_path = config_path.resolve()
    config = load_config(config_path)
    repository = resolve_path(config_path, config["repository"])
    state_path = resolve_path(config_path, config["state_path"])
    reports_dir = resolve_path(config_path, config["reports_dir"])
    builder_workspace = resolve_path(config_path, config["builder_workspace"])
    audit_root = resolve_path(config_path, config["audit_workspaces"])
    validate_workspaces(builder_workspace, audit_root)

    current = status(state_path)
    actor = next_actor(current)
    common_env = {
        "IDEAS_STANDARD_STATE": str(state_path),
        "IDEAS_STANDARD_PROJECT_ID": current["project_id"],
        "IDEAS_STANDARD_PHASE": current["phase"],
        "IDEAS_STANDARD_GATE": current["gate"],
    }

    if actor == "BUILDER":
        if not builder_workspace.is_dir() or not os.access(builder_workspace, os.W_OK):
            raise HandoffError("Builder workspace must exist and be writable")
        report = reports_dir / "builder-report.json"
        run_actor(config["builder_command"], builder_workspace, report, common_env)
        payload = load_json(report)
        verify_commit(repository, payload.get("result_sha", ""))
        return builder_handoff(state_path, report)

    if actor == "AUDITOR":
        target = current.get("audit_target_sha")
        if not target:
            raise HandoffError("Auditor requires audit_target_sha")
        workspace = prepare_audit_workspace(repository, audit_root, target)
        report = reports_dir / "audit-report.json"
        run_actor(
            config["auditor_command"],
            workspace,
            report,
            {**common_env, "IDEAS_STANDARD_AUDIT_TARGET_SHA": target},
        )
        dirty = subprocess.run(
            ["git", "-C", str(workspace), "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=False,
        )
        if dirty.returncode != 0 or dirty.stdout:
            raise HandoffError("Auditor modified or invalidated the frozen audit workspace")
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
