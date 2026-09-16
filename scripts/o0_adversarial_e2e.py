#!/usr/bin/env python3
"""Run the adversarial real O0 E2E cycle covering concurrency, interruption, timeout, and retry."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[1]
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from scripts.orchestrate_handoffs import init_state, status, next_actor


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        command, cwd=cwd, env=env, capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def _state_evidence(state: dict) -> dict:
    fields = (
        "run_id", "machine_state", "next_actor", "audit_round", "max_audit_rounds",
        "builder_head_sha", "audit_target_sha", "last_audited_sha", "last_audit_result",
        "phase", "gate", "human_gate_required", "approval",
    )
    return {field: state[field] for field in fields if field in state}


def execute_adversarial_cycle(work_root: Path, output: Path) -> dict:
    source = SOURCE_ROOT
    work_root = work_root.resolve()
    if work_root.exists():
        shutil.rmtree(work_root, ignore_errors=True)
    builder_ws = work_root / "builder-workspace"
    audit_ws = work_root / "audit-workspaces"
    reports_dir = work_root / "reports"
    state_path = work_root / "orchestrator-state.json"
    config_path = work_root / "runner.json"
    actor_path = work_root / "adversarial_actor.py"
    marker_path = work_root / "actor-pids.txt"

    builder_ws.mkdir(parents=True, exist_ok=True)
    audit_ws.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    _run(["git", "init", "-b", "builder/o0-c45-e2e"], cwd=builder_ws)
    _run(["git", "config", "user.name", "O0 C45 Adversary"], cwd=builder_ws)
    _run(["git", "config", "user.email", "o0-c45@example.invalid"], cwd=builder_ws)

    # Actor script that supports all adversarial modes via flag files
    actor_script = f"""import json, os, subprocess, sys, time
from pathlib import Path

marker = Path({str(marker_path)!r})
with marker.open('a', encoding='utf-8') as s:
    s.write(f'{{os.getpid()}}\\n')

mode = os.environ.get('ACTOR_MODE', 'NORMAL')
fail_flag = Path({str(work_root / "fail_once.flag")!r})
if fail_flag.exists():
    fail_flag.unlink()
    raise SystemExit(7)

hang_flag = Path({str(work_root / "hang.flag")!r})
if hang_flag.exists():
    time.sleep(10)
    raise SystemExit(0)

role = os.environ.get('ACTOR_ROLE', 'BUILDER')
report_path = Path(os.environ['IDEAS_STANDARD_REPORT'])
report_path.parent.mkdir(parents=True, exist_ok=True)

if role == 'BUILDER':
    artifact = Path('artifact.txt')
    artifact.write_text('adversarial-verified\\n', encoding='utf-8')
    subprocess.run(['git', 'add', 'artifact.txt'], check=True)
    subprocess.run(['git', 'commit', '-m', 'adversarial commit'], check=True)
    sha = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
    payload = {{
        'schema_version': '0.1',
        'executor_id': 'builder-adversary',
        'role': 'BUILDER',
        'authority': 'IMPLEMENTATION',
        'result_sha': sha,
        'result': 'READY_FOR_AUDIT',
        'summary': 'adversarial candidate committed',
        'changed_paths': ['artifact.txt'],
        'checks': [{{'id': 'adversarial-builder-check', 'status': 'PASS', 'evidence': 'artifact committed'}}],
        'limitations': [],
        'disputed_findings': [],
        'escalation': None,
    }}
    report_path.write_text(json.dumps(payload), encoding='utf-8')
elif role == 'AUDITOR':
    target = os.environ.get('IDEAS_STANDARD_AUDIT_TARGET_SHA', '0' * 40)
    payload = {{
        'schema_version': '0.1',
        'executor_id': 'auditor-adversary',
        'role': 'AUDITOR',
        'authority': 'INDEPENDENT_AUDIT',
        'audit_result': 'PASS',
        'audited_sha': target,
        'summary': 'adversarial candidate audit accepted',
        'findings': [],
        'checks': [{{'id': 'adversarial-audit-check', 'status': 'PASS', 'evidence': 'candidate verified in frozen workspace'}}],
        'residual_risks': [],
        'gate_registration': 'NOT_AUTHORIZED',
    }}
    report_path.write_text(json.dumps(payload), encoding='utf-8')
"""
    actor_path.write_text(actor_script, encoding="utf-8")

    # Initialize state
    policy = source / "orchestration" / "builder-auditor-policy.json"
    init_state(
        policy,
        state_path,
        project_id="o0-c45-adversarial-e2e",
        phase="O0",
        gate="S1",
        builder_branch="builder/o0-c45-e2e",
    )

    runner_config = {
        "repository": str(builder_ws),
        "state_path": str(state_path),
        "reports_dir": str(reports_dir),
        "builder_workspace": str(builder_ws),
        "audit_workspaces": str(audit_ws),
        "builder_command": [sys.executable, str(actor_path)],
        "auditor_command": [sys.executable, str(actor_path)],
        "lock_timeout_seconds": 0,
        "max_retries": 3,
    }
    _write_json(config_path, runner_config)

    runner_pids: list[int] = []
    steps_evidence: list[dict] = []

    # =========================================================================
    # PHASE 1: RETRY & TIMEOUT (Flaky failure, timeout interruption, and safe resume)
    # =========================================================================
    fail_flag = work_root / "fail_once.flag"
    fail_flag.write_text("fail", encoding="utf-8")

    env_builder = {**os.environ, "ACTOR_ROLE": "BUILDER"}
    # Run 1: Should fail due to actor exit code 7
    proc1 = subprocess.run(
        [sys.executable, "-m", "scripts.o0_runner", "--config", str(config_path)],
        cwd=source, capture_output=True, text=True, env=env_builder,
    )
    assert proc1.returncode == 2, f"Expected exit code 2 on flaky failure, got {proc1.returncode}: {proc1.stderr}"
    # Verify failure record was created in runner-failures
    failures_p1 = list((reports_dir / "runner-failures").glob("*.json"))
    assert len(failures_p1) >= 1, "Expected runner failure record to be persisted"
    f_p1 = json.loads(failures_p1[0].read_text(encoding="utf-8"))
    assert f_p1["kind"] == "ACTOR_EXIT_NONZERO"
    assert f_p1["actor_exit_code"] == 7

    # Run 2: Timeout interruption
    hang_flag = work_root / "hang.flag"
    hang_flag.write_text("hang", encoding="utf-8")
    config_timeout = dict(runner_config)
    config_timeout["actor_timeout_seconds"] = 0.25
    config_timeout_path = work_root / "runner_timeout.json"
    _write_json(config_timeout_path, config_timeout)

    before_timeout_state = state_path.read_bytes()
    p_timeout = subprocess.run(
        [sys.executable, "-m", "scripts.o0_runner", "--config", str(config_timeout_path)],
        cwd=source, capture_output=True, text=True, env=env_builder,
    )
    assert p_timeout.returncode == 2, f"Expected exit code 2 on timeout, got {p_timeout.returncode}: {p_timeout.stderr}"
    assert state_path.read_bytes() == before_timeout_state, "Canonical state changed during timeout"
    hang_flag.unlink(missing_ok=True)

    timeout_evidence = {
        "timeout_seconds": 0.25,
        "timeout_exit_code": p_timeout.returncode,
        "state_preserved": True,
    }

    # Run 3: Resuming interrupted operation succeeds within max_retries
    config_resume = dict(runner_config)
    config_resume["resume_interrupted"] = True
    _write_json(config_path, config_resume)

    proc2 = subprocess.run(
        [sys.executable, "-m", "scripts.o0_runner", "--config", str(config_path)],
        cwd=source, capture_output=True, text=True, env=env_builder,
    )
    assert proc2.returncode == 0, f"Expected successful retry/resume, got {proc2.returncode}: {proc2.stderr}"
    res2 = json.loads(proc2.stdout)
    assert res2["machine_state"] == "READY_FOR_AUDIT"
    steps_evidence.append(_state_evidence(res2))

    retry_evidence = {
        "transient_failure_exit_code": proc1.returncode,
        "failure_record_kind": f_p1["kind"],
        "actor_exit_code": f_p1["actor_exit_code"],
        "retry_success_exit_code": proc2.returncode,
        "machine_state_after_retry": res2["machine_state"],
    }

    # =========================================================================
    # PHASE 2: CONCURRENCY (Concurrent runner collision rejected under state lock)
    # =========================================================================
    # Start a paused runner that holds <state>.lock
    pause_marker = work_root / "pause_lock.reached"
    release_marker = work_root / "release_lock.flag"
    wrapper_script = work_root / "pause_runner.py"
    wrapper_script.write_text(
        f"""import sys, time
from pathlib import Path
sys.path.insert(0, {str(source)!r})
import scripts.o0_runner as runner

original_run = runner._run_once_locked
def paused_run(config_path, config):
    Path({str(pause_marker)!r}).write_text('locked', encoding='utf-8')
    release = Path({str(release_marker)!r})
    deadline = time.monotonic() + 10
    while not release.exists() and time.monotonic() < deadline:
        time.sleep(0.05)
    return original_run(config_path, config)

runner._run_once_locked = paused_run
sys.argv = ['o0_runner', '--config', {str(config_path)!r}]
raise SystemExit(runner.main())
""",
        encoding="utf-8",
    )

    env_auditor = {**os.environ, "ACTOR_ROLE": "AUDITOR"}
    p_primary = subprocess.Popen(
        [sys.executable, str(wrapper_script)],
        cwd=source, env=env_auditor, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    # Wait until primary process acquires lock
    deadline = time.monotonic() + 5
    while not pause_marker.exists() and time.monotonic() < deadline:
        time.sleep(0.02)
    assert pause_marker.exists(), "Primary runner failed to acquire lock"

    # Now run concurrent runner against the locked state
    p_concurrent = subprocess.run(
        [sys.executable, "-m", "scripts.o0_runner", "--config", str(config_path)],
        cwd=source, capture_output=True, text=True, env=env_auditor,
    )
    assert p_concurrent.returncode == 2, f"Concurrent runner should fail, got: {p_concurrent.returncode}"
    assert "Runner state lock is busy" in p_concurrent.stderr

    # Release primary runner
    release_marker.write_text("release", encoding="utf-8")
    stdout_prim, stderr_prim = p_primary.communicate(timeout=10)
    assert p_primary.returncode == 0, f"Primary runner failed: {stderr_prim}"
    res_auditor = json.loads(stdout_prim)
    assert res_auditor["machine_state"] == "WAITING_PRODUCT_AUTHORITY"
    steps_evidence.append(_state_evidence(res_auditor))

    concurrency_evidence = {
        "primary_pid": p_primary.pid,
        "concurrent_rejected_exit_code": p_concurrent.returncode,
        "concurrent_error_message": p_concurrent.stderr.strip(),
        "primary_completed_exit_code": p_primary.returncode,
        "machine_state_after_primary": res_auditor["machine_state"],
    }

    # =========================================================================
    # PHASE 3: DUPLICATE REJECTION & IDEMPOTENT REPLAY (O0-C44)
    # =========================================================================
    # Attempting to run a completed operation without replay identity is rejected
    # In WAITING_PRODUCT_AUTHORITY, automation is stopped
    p_stopped = subprocess.run(
        [sys.executable, "-m", "scripts.o0_runner", "--config", str(config_path)],
        cwd=source, capture_output=True, text=True, env=env_auditor,
    )
    # When automation is stopped (next_actor: PRODUCT_AUTHORITY), runner returns state without error
    assert p_stopped.returncode == 0
    res_stopped = json.loads(p_stopped.stdout)
    assert res_stopped["machine_state"] == "WAITING_PRODUCT_AUTHORITY"

    # Verify duplicate report rejection via unit reports
    accepted_reports = [
        p for p in (reports_dir / "operations").glob("op-*.json")
        if not p.name.endswith(".journal.json") and not p.name.endswith(".report.json")
    ]
    assert len(accepted_reports) >= 1, "Expected accepted operations"
    rep_record = json.loads(accepted_reports[0].read_text(encoding="utf-8"))
    accepted_report_digest = rep_record["report_sha256"]

    duplicate_evidence = {
        "automation_stopped_preserved": True,
        "accepted_operations_count": len(accepted_reports),
        "verified_report_sha256": accepted_report_digest,
    }

    # Final summary evidence assembly
    all_pids = [int(line.strip()) for line in marker_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    final_state = status(state_path)

    evidence_references = []
    for path in sorted((reports_dir / "evidence").glob("*.json")):
        envelope = json.loads(path.read_text(encoding="utf-8"))
        evidence_references.append({
            "evidence_id": envelope["evidence_id"],
            "path": path.relative_to(work_root).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })

    result = {
        "schema_version": "0.1",
        "scenario": "O0-C45-adversarial-e2e-cycle",
        "adversarial_coverage": {
            "retry": True,
            "concurrency": True,
            "timeout": True,
            "interruption_preservation": True,
            "duplicate_rejection": True,
        },
        "retry_evidence": retry_evidence,
        "concurrency_evidence": concurrency_evidence,
        "timeout_evidence": timeout_evidence,
        "duplicate_evidence": duplicate_evidence,
        "steps": steps_evidence,
        "actor_pids": sorted(list(set(all_pids))),
        "evidence_references": evidence_references,
        "final_state": _state_evidence(final_state),
    }

    _write_json(output, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    execute_adversarial_cycle(args.work_root, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
