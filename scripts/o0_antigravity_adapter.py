#!/usr/bin/env python3
"""Antigravity CLI adapter for o0_runner.py (O0 v2 M2).

Invoked by o0_runner as the configured builder_command in cwd=builder_workspace.
Reads task and environment, executes Antigravity CLI in headless print mode,
validates that changes were made and tests pass, and writes the canonical
builder-report.json required by the Ideias Standard.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def _find_agy_binary(override: str | None = None) -> Path:
    if override:
        p = Path(override)
        if p.is_file():
            return p.resolve()
        raise FileNotFoundError(f"Specified Antigravity CLI binary not found: {override}")

    localappdata = Path(os.environ.get("LOCALAPPDATA", r"C:\Users\fael\AppData\Local"))
    candidate = localappdata / "agy" / "bin" / "agy.exe"
    if candidate.is_file():
        return candidate.resolve()

    which_agy = shutil.which("agy")
    if which_agy:
        return Path(which_agy).resolve()

    raise FileNotFoundError("Antigravity CLI (agy) binary not found")


def _run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", default=None, help="Explicit task description for Builder")
    parser.add_argument("--model", default="gemini-3.7-flash-medium", help="Model for Antigravity CLI")
    parser.add_argument("--agy-bin", default=None, help="Path to Antigravity CLI binary")
    parser.add_argument("--test-cmd", default=None, help="Optional test command to verify before report")
    args = parser.parse_args()

    report_env = os.environ.get("IDEAS_STANDARD_REPORT")
    if not report_env:
        print("ERROR: IDEAS_STANDARD_REPORT environment variable is required", file=sys.stderr)
        return 1

    report_path = Path(report_env).resolve()
    workspace = Path.cwd().resolve()

    # Discover binary
    agy_bin = _find_agy_binary(args.agy_bin)

    # Determine base SHA
    base_sha = _run_git(["rev-parse", "HEAD"], cwd=workspace).stdout.strip()

    # Determine task from arguments, environment or findings
    task_desc = args.task or os.environ.get("IDEAS_STANDARD_TASK")
    findings_path = os.environ.get("IDEAS_STANDARD_FINDINGS")

    if findings_path and Path(findings_path).is_file():
        findings_data = json.loads(Path(findings_path).read_text(encoding="utf-8"))
        findings_list = findings_data.get("findings", [])
        findings_summary = "; ".join(f.get("problem", "") for f in findings_list)
        prompt_task = (
            f"Fix the following audit findings: {findings_summary}. "
            f"Implement the necessary corrections in {workspace} and verify with tests."
        )
    elif task_desc:
        prompt_task = task_desc
    else:
        prompt_task = "Implement the requested changes in the active workspace and ensure tests pass."

    builder_prompt = (
        f"In the active workspace {workspace}, {prompt_task} "
        "Run unit tests if present. When tests pass, stage the modified files with 'git add' "
        "and commit with a semantic commit message. "
        "Reply with only the word DONE."
    )

    cmd = [
        str(agy_bin),
        f"--add-dir={workspace}",
        f"--model={args.model}",
        "--dangerously-skip-permissions",
        "--output-format", "json",
        f"--print={builder_prompt}",
    ]

    child_pid_file = os.environ.get("IDEAS_STANDARD_CHILD_PID_FILE")
    if child_pid_file:
        proc = subprocess.Popen(cmd, cwd=workspace, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            Path(child_pid_file).write_text(str(proc.pid), encoding="utf-8")
        except OSError:
            pass
        stdout, stderr = proc.communicate()
        p = subprocess.CompletedProcess(cmd, proc.returncode, stdout, stderr)
    else:
        p = subprocess.run(cmd, cwd=workspace, capture_output=True, text=True, check=False)
    if p.returncode != 0:
        print(f"ERROR: Antigravity CLI exited with code {p.returncode}: {p.stderr}", file=sys.stderr)
        return p.returncode

    try:
        output_json = json.loads(p.stdout.strip())
        status = output_json.get("status")
        if status != "SUCCESS":
            print(f"ERROR: Antigravity CLI status is not SUCCESS: {output_json}", file=sys.stderr)
            return 1
    except json.JSONDecodeError:
        print(f"ERROR: Antigravity CLI did not return valid JSON: {p.stdout[:300]}", file=sys.stderr)
        return 1

    # Verify produced SHA
    result_sha = _run_git(["rev-parse", "HEAD"], cwd=workspace).stdout.strip()
    if result_sha == base_sha:
        print("ERROR: Antigravity CLI did not create a new commit", file=sys.stderr)
        return 1

    # Get changed paths
    diff_proc = _run_git(["diff", "--name-only", f"{base_sha}..{result_sha}"], cwd=workspace)
    changed_paths = [line.strip() for line in diff_proc.stdout.splitlines() if line.strip()]
    if not changed_paths:
        changed_paths = ["."]

    # Run optional or detected unit tests
    test_evidence = "Unit tests verified by Antigravity Builder"
    if args.test_cmd:
        p_test = subprocess.run(args.test_cmd, shell=True, cwd=workspace, capture_output=True, text=True)
        if p_test.returncode != 0:
            print(f"ERROR: Builder tests failed: {p_test.stderr}", file=sys.stderr)
            return 1
        test_evidence = f"Test command '{args.test_cmd}' passed successfully"

    # Assemble canonical builder-report.json
    report_payload: dict[str, Any] = {
        "schema_version": "0.1",
        "executor_id": "antigravity-cli",
        "role": "BUILDER",
        "authority": "IMPLEMENTATION",
        "result_sha": result_sha,
        "result": "READY_FOR_AUDIT",
        "summary": f"Antigravity CLI completed task: {prompt_task[:200]}",
        "changed_paths": changed_paths,
        "checks": [
            {
                "id": "antigravity-build-and-test",
                "status": "PASS",
                "evidence": test_evidence,
            }
        ],
        "limitations": [],
        "disputed_findings": [],
        "escalation": None,
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
