import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.o0_runner import (
    HandoffError,
    load_config,
    prepare_audit_workspace,
    run_actor,
    run_once,
    validate_auditor_boundaries,
    validate_workspaces,
    verify_audit_after,
)


class O0RunnerTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_config_requires_actor_commands(self):
        path = self.root / "config.json"
        path.write_text("{}", encoding="utf-8")
        with self.assertRaises(HandoffError):
            load_config(path)

    def test_builder_and_auditor_workspaces_must_be_separate(self):
        with self.assertRaises(HandoffError):
            validate_workspaces(self.root / "work", self.root / "work" / "audit")

    def test_report_write_scope_cannot_include_state_or_audit_workspace(self):
        with self.assertRaises(HandoffError):
            validate_auditor_boundaries(
                self.root / "state.json", self.root / "audits", self.root
            )

    def test_run_actor_starts_configured_command_and_requires_report(self):
        report = self.root / "reports" / "builder.json"

        def complete(command, **kwargs):
            report.write_text(json.dumps({"ok": True}), encoding="utf-8")
            return type("Result", (), {"returncode": 0})()

        with patch("scripts.o0_runner.subprocess.run", side_effect=complete) as mocked:
            run_actor(["provider", "run"], self.root, report, {"X": "1"})
        self.assertEqual(["provider", "run"], mocked.call_args.args[0])
        self.assertTrue(report.is_file())

    def _repository(self):
        repository = self.root / "repo"
        repository.mkdir()
        subprocess.run(["git", "init"], cwd=repository, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repository, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=repository, check=True)
        (repository / "file.txt").write_text("one", encoding="utf-8")
        subprocess.run(["git", "add", "file.txt"], cwd=repository, check=True)
        subprocess.run(["git", "commit", "-m", "one"], cwd=repository, check=True, capture_output=True)
        first = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=repository, check=True, capture_output=True, text=True
        ).stdout.strip()
        (repository / "file.txt").write_text("two", encoding="utf-8")
        subprocess.run(["git", "commit", "-am", "two"], cwd=repository, check=True, capture_output=True)
        second = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=repository, check=True, capture_output=True, text=True
        ).stdout.strip()
        return repository, first, second

    def test_auditor_cannot_restore_write_permission_or_write_target(self):
        repository, _, target = self._repository()
        workspace = prepare_audit_workspace(repository, self.root / "audits", target)
        report = self.root / "reports" / "audit.json"
        code = (
            "import json,os,pathlib;"
            "target=pathlib.Path('file.txt');blocked=False;"
            "\ntry:\n target.chmod(0o644);target.write_text('tampered')"
            "\nexcept PermissionError:\n blocked=True"
            "\npathlib.Path(os.environ['IDEAS_STANDARD_REPORT']).write_text(json.dumps({'blocked':blocked}))"
        )
        run_actor([sys.executable, "-c", code], workspace, report, {}, write_sandbox=True)
        self.assertTrue(json.loads(report.read_text())["blocked"])
        self.assertEqual("two", (workspace / "file.txt").read_text())

    def test_auditor_cannot_write_canonical_state(self):
        state = self.root / "state.json"
        state.write_text('{"audit_target_sha":"fixed"}', encoding="utf-8")
        workspace = self.root / "workspace"
        workspace.mkdir()
        report = self.root / "reports" / "audit.json"
        code = (
            "import json,os,pathlib;"
            "state=pathlib.Path(os.environ['CANONICAL']);blocked=False;"
            "\ntry:\n state.chmod(0o644);state.write_text('{}')"
            "\nexcept PermissionError:\n blocked=True"
            "\npathlib.Path(os.environ['IDEAS_STANDARD_REPORT']).write_text(json.dumps({'blocked':blocked}))"
        )
        run_actor(
            [sys.executable, "-c", code],
            workspace,
            report,
            {"CANONICAL": str(state)},
            write_sandbox=True,
        )
        self.assertTrue(json.loads(report.read_text())["blocked"])
        self.assertEqual('{"audit_target_sha":"fixed"}', state.read_text())

    def test_state_change_during_audit_is_rejected(self):
        repository, _, target = self._repository()
        workspace = prepare_audit_workspace(repository, self.root / "audits", target)
        state = self.root / "state.json"
        state.write_text('{"audit_target_sha":"before"}', encoding="utf-8")
        before = state.read_bytes()
        state.write_text('{"audit_target_sha":"after"}', encoding="utf-8")
        with self.assertRaisesRegex(HandoffError, "Canonical state changed"):
            verify_audit_after(workspace, state, target, before)

    def test_clean_checkout_at_wrong_head_is_rejected(self):
        repository, first, target = self._repository()
        workspace = prepare_audit_workspace(repository, self.root / "audits", target)
        for path in [workspace, *workspace.rglob("*")]:
            path.chmod(path.stat().st_mode | 0o200)
        subprocess.run(["git", "checkout", "--detach", first], cwd=workspace, check=True, capture_output=True)
        state = self.root / "state.json"
        state.write_text(
            json.dumps({
                "schema_version": "0.1",
                "project_id": "sample",
                "phase": "O0",
                "gate": "NONE",
                "machine_state": "READY_FOR_AUDIT",
                "builder_branch": "work",
                "builder_executor_id": "builder",
                "auditor_executor_id": None,
                "product_authority_id": "owner",
                "builder_head_sha": target,
                "audit_target_sha": target,
                "last_audited_sha": None,
                "audit_round": 0,
                "max_audit_rounds": 3,
                "last_builder_report": None,
                "last_audit_report": None,
                "last_audit_result": None,
                "human_gate_required": True,
                "approval": None,
                "updated_at": "now",
                "message": ""
            }),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(HandoffError, "HEAD changed"):
            verify_audit_after(workspace, state, target, state.read_bytes())

    def test_runner_audit_fail_transitions_to_fix_required(self):
        target = "a" * 40
        state = self.root / "state.json"
        state.write_text(
            json.dumps({
                "schema_version": "0.1",
                "project_id": "sample",
                "phase": "O0",
                "gate": "NONE",
                "machine_state": "READY_FOR_AUDIT",
                "builder_branch": "work",
                "builder_executor_id": "builder-executor",
                "auditor_executor_id": None,
                "product_authority_id": "owner",
                "builder_head_sha": target,
                "audit_target_sha": target,
                "last_audited_sha": None,
                "audit_round": 0,
                "max_audit_rounds": 3,
                "last_builder_report": None,
                "last_audit_report": None,
                "last_audit_result": None,
                "human_gate_required": True,
                "approval": None,
                "updated_at": "now",
                "message": ""
            }),
            encoding="utf-8",
        )
        (self.root / "builder").mkdir()
        config = self.root / "runner.json"
        config.write_text(
            json.dumps({
                "repository": "repo",
                "state_path": "state.json",
                "reports_dir": "reports",
                "builder_workspace": "builder",
                "audit_workspaces": "audits",
                "builder_command": ["builder"],
                "auditor_command": ["auditor"],
            }),
            encoding="utf-8",
        )

        def fail_audit(command, workspace, report, env, *, write_sandbox=False):
            report.parent.mkdir(parents=True, exist_ok=True)
            report.write_text(
                json.dumps({
                    "schema_version": "0.1",
                    "executor_id": "auditor-executor",
                    "role": "AUDITOR",
                    "authority": "INDEPENDENT_AUDIT",
                    "audit_result": "FAIL",
                    "audited_sha": target,
                    "summary": "Blocking finding found.",
                    "findings": [{
                        "id": "O0-TEST-001",
                        "severity": "HIGH",
                        "blocking": True,
                        "files": ["scripts/o0_runner.py"],
                        "evidence": "failure path",
                        "problem": "adversarial failure",
                        "violated_criterion": "O0-C14",
                        "resolution_condition": "return FIX_REQUIRED",
                    }],
                    "checks": [{"id": "o0-c14", "status": "FAIL", "evidence": "finding"}],
                    "residual_risks": [],
                    "gate_registration": "NOT_AUTHORIZED",
                }),
                encoding="utf-8",
            )

        workspace = self.root / "audit-workspace"
        workspace.mkdir()
        snapshot = self.root / "snapshot.json"
        with (
            patch("scripts.o0_runner.prepare_audit_workspace", return_value=workspace),
            patch("scripts.o0_runner.write_state_snapshot", return_value=snapshot),
            patch("scripts.o0_runner.verify_audit_after"),
            patch("scripts.o0_runner.run_actor", side_effect=fail_audit),
        ):
            result = run_once(config)

        self.assertEqual("FIX_REQUIRED", result["machine_state"])
        self.assertEqual("FAIL", result["last_audit_result"])
        self.assertEqual(1, result["audit_round"])


if __name__ == "__main__":
    unittest.main()
