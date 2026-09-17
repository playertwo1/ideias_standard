"""Unit tests for Antigravity Builder adapter (o0_antigravity_adapter.py)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.o0_antigravity_adapter import main, _find_agy_binary


REAL_SUBPROCESS_RUN = subprocess.run


class TestO0AntigravityAdapter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_root = Path(self.temp_dir.name).resolve()
        self.workspace = self.temp_root / "repo"
        self.workspace.mkdir(parents=True, exist_ok=True)

        # Initialize a real git repo
        REAL_SUBPROCESS_RUN(["git", "init"], cwd=self.workspace, check=True, capture_output=True)
        REAL_SUBPROCESS_RUN(["git", "config", "user.name", "Test Builder"], cwd=self.workspace, check=True, capture_output=True)
        REAL_SUBPROCESS_RUN(["git", "config", "user.email", "builder@test.local"], cwd=self.workspace, check=True, capture_output=True)

        # Initial commit
        (self.workspace / "init.txt").write_text("initial", encoding="utf-8")
        REAL_SUBPROCESS_RUN(["git", "add", "init.txt"], cwd=self.workspace, check=True, capture_output=True)
        REAL_SUBPROCESS_RUN(["git", "commit", "-m", "chore: initial commit"], cwd=self.workspace, check=True, capture_output=True)

        self.report_path = self.temp_root / "reports" / "builder-report.json"
        self.state_path = self.temp_root / "orchestrator-state.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_find_agy_binary_override_not_found(self):
        with self.assertRaises(FileNotFoundError):
            _find_agy_binary("non_existent_binary_path_xyz")

    @patch("scripts.o0_antigravity_adapter.subprocess.run")
    @patch("scripts.o0_antigravity_adapter._find_agy_binary")
    def test_rejects_result_sha_equals_base_sha_outside_fix_required(self, mock_find_bin, mock_subproc_run):
        """Adapter must reject result_sha == base_sha when not in FIX_REQUIRED."""
        mock_find_bin.return_value = Path("agy.exe")

        def subproc_side_effect(*args, **kwargs):
            cmd = args[0] if args else kwargs.get("args")
            if isinstance(cmd, list) and cmd and cmd[0] == "git":
                return REAL_SUBPROCESS_RUN(*args, **kwargs)
            return subprocess.CompletedProcess(
                args=cmd, returncode=0, stdout=json.dumps({"status": "SUCCESS"}), stderr=""
            )

        mock_subproc_run.side_effect = subproc_side_effect

        # In workspace without changes (HEAD is base_sha, status is clean)
        env = {
            "IDEAS_STANDARD_REPORT": str(self.report_path),
            "IDEAS_STANDARD_STATE": str(self.state_path),
        }
        self.state_path.write_text(json.dumps({"machine_state": "READY_FOR_BUILD"}), encoding="utf-8")

        with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["o0_antigravity_adapter.py"]):
            old_cwd = Path.cwd()
            try:
                os.chdir(self.workspace)
                ret = main()
                self.assertEqual(1, ret)
                self.assertFalse(self.report_path.exists())
            finally:
                os.chdir(old_cwd)

    @patch("scripts.o0_antigravity_adapter.subprocess.run")
    @patch("scripts.o0_antigravity_adapter._find_agy_binary")
    def test_rejects_result_sha_equals_base_sha_in_fix_required(self, mock_find_bin, mock_subproc_run):
        """Adapter must reject result_sha == base_sha when in FIX_REQUIRED."""
        mock_find_bin.return_value = Path("agy.exe")

        def subproc_side_effect(*args, **kwargs):
            cmd = args[0] if args else kwargs.get("args")
            if isinstance(cmd, list) and cmd and cmd[0] == "git":
                return REAL_SUBPROCESS_RUN(*args, **kwargs)
            return subprocess.CompletedProcess(
                args=cmd, returncode=0, stdout=json.dumps({"status": "SUCCESS"}), stderr=""
            )

        mock_subproc_run.side_effect = subproc_side_effect

        env = {
            "IDEAS_STANDARD_REPORT": str(self.report_path),
            "IDEAS_STANDARD_STATE": str(self.state_path),
        }
        self.state_path.write_text(json.dumps({"machine_state": "FIX_REQUIRED"}), encoding="utf-8")

        with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["o0_antigravity_adapter.py"]):
            old_cwd = Path.cwd()
            try:
                os.chdir(self.workspace)
                ret = main()
                self.assertEqual(1, ret)
                self.assertFalse(self.report_path.exists())
            finally:
                os.chdir(old_cwd)

    @patch("scripts.o0_antigravity_adapter.subprocess.run")
    @patch("scripts.o0_antigravity_adapter._find_agy_binary")
    def test_accepts_when_new_commit_produced_without_test_cmd(self, mock_find_bin, mock_subproc_run):
        """Adapter generates valid report with specific evidence when new commit exists without explicit test_cmd."""
        mock_find_bin.return_value = Path("agy.exe")

        def subproc_side_effect(*args, **kwargs):
            cmd = args[0] if args else kwargs.get("args")
            if isinstance(cmd, list) and cmd and cmd[0] == "git":
                return REAL_SUBPROCESS_RUN(*args, **kwargs)
            # agy execution: write uncommitted file
            (self.workspace / "feature.py").write_text("def run(): pass\n", encoding="utf-8")
            return subprocess.CompletedProcess(
                args=cmd, returncode=0, stdout=json.dumps({"status": "SUCCESS"}), stderr=""
            )

        mock_subproc_run.side_effect = subproc_side_effect

        env = {
            "IDEAS_STANDARD_REPORT": str(self.report_path),
        }

        with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["o0_antigravity_adapter.py"]):
            old_cwd = Path.cwd()
            try:
                os.chdir(self.workspace)
                ret = main()
                self.assertEqual(0, ret)
                self.assertTrue(self.report_path.exists())
                report = json.loads(self.report_path.read_text(encoding="utf-8"))
                self.assertEqual("READY_FOR_AUDIT", report["result"])
                self.assertIn("feature.py", report["changed_paths"])
                check = report["checks"][0]
                self.assertEqual("PASS", check["status"])
                self.assertIn("modifying 1 path(s)", check["evidence"])
                self.assertNotIn("Unit tests verified by Antigravity Builder", check["evidence"])
            finally:
                os.chdir(old_cwd)

    @patch("scripts.o0_antigravity_adapter.subprocess.run")
    @patch("scripts.o0_antigravity_adapter._find_agy_binary")
    def test_runs_test_cmd_and_reports_evidence(self, mock_find_bin, mock_subproc_run):
        """Adapter runs test-cmd and includes specific test evidence in the report."""
        mock_find_bin.return_value = Path("agy.exe")

        def subproc_side_effect(*args, **kwargs):
            cmd = args[0] if args else kwargs.get("args")
            if isinstance(cmd, list) and cmd and cmd[0] == "git":
                return REAL_SUBPROCESS_RUN(*args, **kwargs)
            if isinstance(cmd, list) and "agy.exe" in str(cmd[0]):
                (self.workspace / "calc.py").write_text("def add(a, b): return a + b\n", encoding="utf-8")
                return subprocess.CompletedProcess(
                    args=cmd, returncode=0, stdout=json.dumps({"status": "SUCCESS"}), stderr=""
                )
            # test command execution via shell string
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="test pass", stderr="")

        mock_subproc_run.side_effect = subproc_side_effect

        env = {
            "IDEAS_STANDARD_REPORT": str(self.report_path),
            "IDEAS_STANDARD_TEST_CMD": f'"{sys.executable}" -c "print(\'tests passed\')"',
        }

        with patch.dict(os.environ, env, clear=False), patch("sys.argv", ["o0_antigravity_adapter.py"]):
            old_cwd = Path.cwd()
            try:
                os.chdir(self.workspace)
                ret = main()
                self.assertEqual(0, ret)
                self.assertTrue(self.report_path.exists())
                report = json.loads(self.report_path.read_text(encoding="utf-8"))
                self.assertEqual("READY_FOR_AUDIT", report["result"])
                check = report["checks"][0]
                self.assertEqual("PASS", check["status"])
                self.assertIn("passed successfully", check["evidence"])
            finally:
                os.chdir(old_cwd)


if __name__ == "__main__":
    unittest.main()
