#!/usr/bin/env python3
"""OpenAI Codex CLI adapter for o0_runner.py (O0 v2 M2).

Invoked by o0_runner as the configured auditor_command in cwd=audit_workspace.
Reads target SHA and environment, executes Codex CLI with --sandbox read-only,
validates that the checkout was unmodified, and writes the canonical
audit-report.json required by the Ideias Standard.
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


def _find_codex_binary(override: str | None = None) -> Path:
    if override:
        p = Path(override)
        if p.is_file():
            return p.resolve()
        raise FileNotFoundError(f"Specified Codex CLI binary not found: {override}")

    appdata = Path(os.environ.get("APPDATA", r"C:\Users\fael\AppData\Roaming"))
    candidate = appdata / "npm" / "codex.CMD"
    if candidate.is_file():
        return candidate.resolve()

    which_codex = shutil.which("codex")
    if which_codex:
        return Path(which_codex).resolve()

    raise FileNotFoundError("OpenAI Codex CLI binary not found")


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
    parser.add_argument("--task", default=None, help="Explicit task description for Auditor")
    parser.add_argument("--codex-bin", default=None, help="Path to Codex CLI binary")
    args = parser.parse_args()

    report_env = os.environ.get("IDEAS_STANDARD_REPORT")
    if not report_env:
        print("ERROR: IDEAS_STANDARD_REPORT environment variable is required", file=sys.stderr)
        return 1

    target_sha = os.environ.get("IDEAS_STANDARD_AUDIT_TARGET_SHA")
    if not target_sha:
        print("ERROR: IDEAS_STANDARD_AUDIT_TARGET_SHA environment variable is required", file=sys.stderr)
        return 1

    report_path = Path(report_env).resolve()
    audit_workspace = Path.cwd().resolve()

    # Discover binary
    codex_bin = _find_codex_binary(args.codex_bin)

    # Verify workspace is on the target SHA
    current_head = _run_git(["rev-parse", "HEAD"], cwd=audit_workspace).stdout.strip()
    if current_head != target_sha:
        print(f"ERROR: Audit workspace HEAD ({current_head}) does not match target SHA ({target_sha})", file=sys.stderr)
        return 1

    # Temporary schema and output paths placed safely outside the audit checkout
    temp_dir = report_path.parent / f".codex_tmp_{target_sha[:8]}"
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_schema_file = temp_dir / "auditor-schema.json"
    temp_report_file = temp_dir / "codex-raw-report.json"

    codex_output_schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["audited_sha", "audit_result", "summary", "findings", "checks"],
        "properties": {
            "audited_sha": {"type": "string"},
            "audit_result": {"enum": ["PASS", "FAIL"]},
            "summary": {"type": "string"},
            "findings": {"type": "array", "items": {"type": "string"}},
            "checks": {"type": "array", "items": {"type": "string"}},
        },
    }
    temp_schema_file.write_text(json.dumps(codex_output_schema, indent=2), encoding="utf-8")

    task_criteria = args.task or os.environ.get("IDEAS_STANDARD_AUDIT_CRITERIA")
    if not task_criteria and os.environ.get("IDEAS_STANDARD_TASK_GOAL"):
        goal = os.environ["IDEAS_STANDARD_TASK_GOAL"]
        criteria_str = os.environ.get("IDEAS_STANDARD_TASK_CRITERIA")
        parts = [f"Goal: {goal}"]
        if criteria_str:
            try:
                criteria_list = json.loads(criteria_str)
                parts.append("Acceptance criteria to verify:\n- " + "\n- ".join(criteria_list))
            except Exception:
                pass
        task_criteria = "\n".join(parts)
    elif not task_criteria:
        task_criteria = (
            "Inspect the repository files, implementation and tests. "
            "Verify correctness, completeness and that tests pass."
        )

    diff_summary = ""
    try:
        git_show = _run_git(["show", "--stat", "--oneline", target_sha], cwd=audit_workspace).stdout.strip()
        diff_summary = f"\n\nCommit under audit:\n{git_show}\n"
    except Exception:
        pass

    reaudit_handoff_env = os.environ.get("IDEAS_STANDARD_REAUDIT_HANDOFF")
    if reaudit_handoff_env and Path(reaudit_handoff_env).is_file():
        try:
            reaudit_data = json.loads(Path(reaudit_handoff_env).read_text(encoding="utf-8"))
            changed_paths = reaudit_data.get("changed_paths", [])
            changed_desc = f" Changed files: {', '.join(changed_paths)}." if changed_paths else ""
        except Exception:
            changed_desc = ""
        auditor_prompt = (
            f"You are an independent auditor performing a REAUDIT of the repository in the current directory at commit {target_sha}. "
            f"The previous round had findings that Builder was tasked to fix.{changed_desc} "
            f"{task_criteria}{diff_summary}"
            "Verify whether the findings from the previous round have been corrected and all tests pass in this commit. "
            "Return the JSON report required by the output schema. Use audit_result PASS only if the implementation and tests are correct. "
            "Use arrays of strings for findings and checks; findings must be empty for PASS."
        )
    else:
        auditor_prompt = (
            f"You are an independent auditor. Audit the repository in the current directory at commit {target_sha}. "
            f"{task_criteria}{diff_summary}"
            "Return the JSON report required by the output schema. Use audit_result PASS only if the implementation and tests are correct. "
            "Use arrays of strings for findings and checks; findings must be empty for PASS."
        )


    codex_cmd = [
        str(codex_bin),
        "exec",
        "--ephemeral",
        "--skip-git-repo-check",
        "-C", str(audit_workspace),
        "--sandbox", "read-only",
        "--json",
        "--output-schema", str(temp_schema_file),
        "-o", str(temp_report_file),
        auditor_prompt,
    ]

    child_pid_file = os.environ.get("IDEAS_STANDARD_CHILD_PID_FILE")
    if child_pid_file:
        proc = subprocess.Popen(codex_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            Path(child_pid_file).write_text(str(proc.pid), encoding="utf-8")
        except OSError:
            pass
        stdout, stderr = proc.communicate(input="")
        p = subprocess.CompletedProcess(codex_cmd, proc.returncode, stdout, stderr)
    else:
        p = subprocess.run(
            codex_cmd,
            input="",
            text=True,
            capture_output=True,
            check=False,
        )

    if p.returncode != 0:
        print(f"ERROR: Codex CLI exited with code {p.returncode}: {p.stderr}", file=sys.stderr)
        shutil.rmtree(temp_dir, ignore_errors=True)
        return p.returncode

    if not temp_report_file.is_file():
        print(f"ERROR: Codex CLI did not produce output report at {temp_report_file}", file=sys.stderr)
        shutil.rmtree(temp_dir, ignore_errors=True)
        return 1

    try:
        raw_report = json.loads(temp_report_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: Failed to parse Codex output JSON: {exc}", file=sys.stderr)
        shutil.rmtree(temp_dir, ignore_errors=True)
        return 1

    # Verify audit checkout remained completely clean
    p_status = _run_git(["status", "--porcelain"], cwd=audit_workspace)
    if p_status.stdout.strip():
        print(f"ERROR: Audit checkout was modified during audit: {p_status.stdout}", file=sys.stderr)
        shutil.rmtree(temp_dir, ignore_errors=True)
        return 1

    audit_result = raw_report.get("audit_result", "FAIL")
    raw_findings = raw_report.get("findings", [])
    raw_checks = raw_report.get("checks", [])
    if not raw_checks:
        raw_checks = ["Auditor verification performed in frozen checkout"]

    converted_findings = []
    if audit_result == "FAIL":
        for i, item in enumerate(raw_findings):
            converted_findings.append({
                "id": f"CODEX-FINDING-{i+1:03d}",
                "severity": "HIGH",
                "blocking": True,
                "files": ["."],
                "evidence": f"Codex reported finding: {item}",
                "problem": item,
                "violated_criterion": "Implementation or test correctness",
                "resolution_condition": "Builder must fix the reported finding and produce a new SHA.",
            })

    canonical_report: dict[str, Any] = {
        "schema_version": "0.1",
        "executor_id": "codex-cli",
        "role": "AUDITOR",
        "authority": "INDEPENDENT_AUDIT",
        "audit_result": audit_result,
        "audited_sha": target_sha,
        "summary": raw_report.get("summary", f"Independent audit {audit_result} by Codex CLI."),
        "findings": converted_findings,
        "checks": [
            {
                "id": f"codex-check-{i+1}",
                "status": audit_result,
                "evidence": check_desc,
            }
            for i, check_desc in enumerate(raw_checks)
        ],
        "residual_risks": [],
        "gate_registration": "NOT_AUTHORIZED",
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(canonical_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Cleanup temporary files
    shutil.rmtree(temp_dir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
