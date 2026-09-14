import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.o0_runner import (
    HandoffError,
    load_config,
    prepare_audit_workspace,
    run_actor,
    validate_workspaces,
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

    def test_run_actor_starts_configured_command_and_requires_report(self):
        report = self.root / "reports" / "builder.json"

        def complete(command, **kwargs):
            report.write_text(json.dumps({"ok": True}), encoding="utf-8")
            return type("Result", (), {"returncode": 0})()

        with patch("scripts.o0_runner.subprocess.run", side_effect=complete) as mocked:
            run_actor(["provider", "run"], self.root, report, {"X": "1"})
        self.assertEqual(["provider", "run"], mocked.call_args.args[0])
        self.assertTrue(report.is_file())

    def test_audit_workspace_is_frozen_at_requested_sha(self):
        repository = self.root / "repo"
        repository.mkdir()
        import subprocess
        subprocess.run(["git", "init"], cwd=repository, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repository, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=repository, check=True)
        (repository / "file.txt").write_text("content", encoding="utf-8")
        subprocess.run(["git", "add", "file.txt"], cwd=repository, check=True)
        subprocess.run(["git", "commit", "-m", "fixture"], cwd=repository, check=True, capture_output=True)
        sha = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=repository, check=True, capture_output=True, text=True
        ).stdout.strip()

        workspace = prepare_audit_workspace(repository, self.root / "audits", sha)
        actual = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=workspace, check=True, capture_output=True, text=True
        ).stdout.strip()
        self.assertEqual(sha, actual)
        self.assertEqual(0, workspace.stat().st_mode & 0o222)


if __name__ == "__main__":
    unittest.main()
