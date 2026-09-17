#!/usr/bin/env python3
"""Run and package the final O0 v2 proof with real Builder/Auditor CLIs."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.o0_runner import run_task_queue


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def remove_tree(path: Path) -> None:
    if not path.exists():
        return
    for item in path.rglob("*"):
        try:
            item.chmod(stat.S_IREAD | stat.S_IWRITE)
        except OSError:
            pass
    shutil.rmtree(path)


def execute(work: Path, output: Path, package: Path) -> dict:
    for path in (work, package):
        if path.exists():
            remove_tree(path)
    work.mkdir(parents=True)
    package.mkdir(parents=True)
    repo = work / "repository"
    repo.mkdir()
    git(repo, "init", "-b", "main")
    git(repo, "config", "user.name", "O0 M5 Builder")
    git(repo, "config", "user.email", "o0-m5@example.invalid")
    (repo / "calc.py").write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    (repo / "test_calc.py").write_text(
        "import unittest\nfrom calc import add\n\nclass T(unittest.TestCase):\n"
        "    def test_add(self): self.assertEqual(add(2, 3), 5)\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "chore: initial")
    base_sha = git(repo, "rev-parse", "HEAD")

    reports = work / "reports"
    state = work / "orchestrator-state.json"
    audits = work / "audits"
    antigravity = ROOT / "scripts" / "o0_antigravity_adapter.py"
    codex = ROOT / "scripts" / "o0_codex_adapter.py"
    py = sys.executable
    task1 = (
        "Add multiply(a,b) to calc.py, intentionally implement return a + b, and add a weak test "
        "multiply(2,2)==4. Run python -m unittest test_calc.py and commit."
    )
    audit1 = (
        "Verify multiply performs a * b, not addition. FAIL with a blocking finding when it uses +; "
        "PASS only after it uses multiplication and tests cover unequal operands."
    )
    task2 = (
        "Add subtract(a,b) returning a-b and a unit test with unequal operands. Run python -m unittest "
        "test_calc.py and commit."
    )
    audit2 = "Verify subtract returns a-b, its test passes, and return PASS only when correct."
    config = {
        "repository": str(repo), "state_path": str(state), "reports_dir": str(reports),
        "builder_workspace": str(repo), "audit_workspaces": str(audits), "max_retries": 3,
        "builder_command": [py, str(antigravity), "--task", task1, "--test-cmd", "python -m unittest test_calc.py"],
        "auditor_command": [py, str(codex), "--task", audit1],
    }
    config_path = work / "runner.json"
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    queue = {
        "schema_version": "0.1", "invocation_id": "o0-v2-m5-final", "phase": "O0",
        "tasks": [
            {"task_id": "known-defect", "goal": "Detect and correct multiply defect",
             "scope": ["calc.py", "test_calc.py"], "acceptance_criteria": ["FAIL then correction then PASS"],
             "phase": "O0", "builder_command": config["builder_command"], "auditor_command": config["auditor_command"]},
            {"task_id": "authorized-second-task", "goal": "Implement subtract",
             "scope": ["calc.py", "test_calc.py"], "acceptance_criteria": ["subtract correct and audited"],
             "phase": "O0", "builder_command": [py, str(antigravity), "--task", task2, "--test-cmd", "python -m unittest test_calc.py"],
             "auditor_command": [py, str(codex), "--task", audit2]},
        ],
    }
    queue_path = work / "queue.json"
    queue_path.write_text(json.dumps(queue, indent=2), encoding="utf-8")
    result = run_task_queue(config_path, queue_path, max_steps_per_task=10, invocation_id=queue["invocation_id"])
    assert result["status"] == "COMPLETED" and len(result["executed_tasks"]) == 2
    first, second = result["executed_tasks"]
    assert first["audit_round"] == 2 and first["last_audit_result"] == "PASS"
    assert second["audit_round"] == 1 and second["last_audit_result"] == "PASS"
    assert first["last_audited_sha"] != second["last_audited_sha"]
    assert first["approval"] is None and second["approval"] is None
    first_reports = reports / "tasks" / "known-defect"
    fail_report = json.loads((first_reports / "audit-report.json.accepted.1").read_text(encoding="utf-8"))
    pass_report = json.loads((first_reports / "audit-report.json.accepted.2").read_text(encoding="utf-8"))
    sha_a = fail_report["audited_sha"]
    sha_b = pass_report["audited_sha"]
    assert fail_report["audit_result"] == "FAIL" and fail_report["findings"]
    assert pass_report["audit_result"] == "PASS" and not pass_report["findings"]
    assert sha_a != sha_b == first["last_audited_sha"]

    bundle = package / "builder.bundle"
    subprocess.run(["git", "bundle", "create", str(bundle), "--all"], cwd=repo, check=True)
    subprocess.run(["git", "bundle", "verify", str(bundle)], cwd=repo, check=True, capture_output=True)
    shutil.copytree(reports, package / "reports")
    shutil.copy2(state, package / "final-state.json")
    shutil.copy2(queue_path, package / "queue.json")
    interruption_source = ROOT / "O0_V2_M2_EVIDENCE_PROCESS_PROOF_FINAL_PACKAGE"
    shutil.copytree(interruption_source, package / "interruption-proof")
    recovery = subprocess.run(
        [sys.executable, "-m", "unittest", "scripts.test_o0_recovery"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    (package / "recovery-regression.txt").write_text(
        recovery.stdout + recovery.stderr, encoding="utf-8"
    )
    refs = []
    for path in sorted(p for p in package.rglob("*") if p.is_file()):
        refs.append({"path": path.relative_to(package).as_posix(), "sha256": digest(path)})
    payload = {
        "schema_version": "0.1", "milestone": "O0_V2_M5", "status": "PARTIAL",
        "cycle_status": "COMPLETED",
        "base_sha": base_sha, "sha_a": sha_a, "sha_b": sha_b,
        "second_task_sha": second["last_audited_sha"],
        "queue_result": result, "real_agents": ["Antigravity CLI", "Codex CLI"],
        "interruption_proof": {
            "timeout_cancel": "interruption-proof/ (reused audited M2 real-CLI proof)",
            "resume_without_duplication": "recovery-regression.txt (separate recovery regression)",
        },
        "references": refs, "approval": None, "gate_s1": "NOT_RUN", "s2": "NOT_STARTED",
        "remaining_proof": "Fresh real-CLI interruption followed by resume without duplicate accepted result",
    }
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, default=Path(tempfile.gettempdir()) / "o0-v2-m5-work")
    parser.add_argument("--output", type=Path, default=ROOT / "O0_V2_M5_EVIDENCE.json")
    parser.add_argument("--package", type=Path, default=ROOT / "O0_V2_M5_EVIDENCE_PACKAGE")
    args = parser.parse_args()
    execute(args.work, args.output, args.package)
    print("PARTIAL: O0 v2 M5 cycle complete; interruption/resume proof pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
