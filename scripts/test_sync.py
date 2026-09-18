import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SyncTest(unittest.TestCase):
    def run_sync(self, target, *extra):
        return subprocess.run([sys.executable, "scripts/sync.py", "fixtures/sync-new", str(target), "--json", *extra], cwd=ROOT, capture_output=True, text=True, check=True)

    def test_plan_classifies_missing_and_conflicting_files(self):
        report = json.loads(self.run_sync("fixtures/sync-target").stdout)
        self.assertIn("AGENTS.md", report["necessary"])
        self.assertIn("README.md", report["conflicting"])
        self.assertFalse(report["writes"])

    def test_second_apply_has_no_new_changes(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            target.mkdir()
            (target / "README.md").write_bytes((ROOT / "fixtures/sync-new/README.md").read_bytes())
            # A target with no conflicts receives only the missing AGENTS file.
            result = subprocess.run([sys.executable, "scripts/sync.py", "fixtures/sync-new", str(target), "--json", "--apply"], cwd=ROOT, capture_output=True, text=True, check=True)
            self.assertTrue(json.loads(result.stdout)["writes"])
            result = subprocess.run([sys.executable, "scripts/sync.py", "fixtures/sync-new", str(target), "--json", "--apply"], cwd=ROOT, capture_output=True, text=True, check=True)
            self.assertFalse(json.loads(result.stdout)["writes"])

    def test_generated_and_private_files_are_excluded(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            target = Path(tmp) / "target"
            (source / "__pycache__").mkdir(parents=True)
            target.mkdir()
            (target / "__pycache__").mkdir(parents=True)
            (source / "AGENTS.md").write_text("gold\n", encoding="utf-8")
            (source / "__pycache__" / "module.pyc").write_bytes(b"generated")
            (source / "module.pyc").write_bytes(b"generated")
            (source / ".env").write_text("SECRET=hidden\n", encoding="utf-8")
            (target / "__pycache__" / "local.pyc").write_bytes(b"local-generated")
            (target / "local.pyc").write_bytes(b"local-generated")
            (target / ".env").write_text("LOCAL=keep\n", encoding="utf-8")
            report = json.loads(subprocess.run(
                [sys.executable, "scripts/sync.py", str(source), str(target), "--json"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout)
            self.assertEqual(["AGENTS.md"], report["necessary"])
            self.assertNotIn(".env", report["necessary"])
            self.assertNotIn("module.pyc", report["necessary"])
            self.assertFalse(any("__pycache__" in path for path in report["necessary"]))
            applied = json.loads(subprocess.run(
                [sys.executable, "scripts/sync.py", str(source), str(target), "--json", "--apply"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout)
            self.assertTrue(applied["writes"])
            self.assertEqual("LOCAL=keep\n", (target / ".env").read_text(encoding="utf-8"))
            self.assertEqual(b"local-generated", (target / "local.pyc").read_bytes())
            self.assertEqual(b"local-generated", (target / "__pycache__" / "local.pyc").read_bytes())
            repeated = json.loads(subprocess.run(
                [sys.executable, "scripts/sync.py", str(source), str(target), "--json", "--apply"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout)
            self.assertFalse(repeated["writes"])

    def test_invalid_paths_fail_before_any_write(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            source.mkdir()
            missing = Path(tmp) / "missing"
            file_path = Path(tmp) / "target.txt"
            file_path.write_text("local", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "scripts/sync.py", str(missing), str(source), "--json", "--apply"],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("IS-SYNC-001", result.stderr)
            result = subprocess.run(
                [sys.executable, "scripts/sync.py", str(file_path), str(source), "--json", "--apply"],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("IS-SYNC-001", result.stderr)
            for target in (missing, file_path):
                result = subprocess.run(
                    [sys.executable, "scripts/sync.py", str(source), str(target), "--json", "--apply"],
                    cwd=ROOT, capture_output=True, text=True,
                )
                self.assertNotEqual(0, result.returncode)
                self.assertIn("IS-SYNC-001", result.stderr)
                self.assertFalse((target / "AGENTS.md").exists() if target.is_dir() else False)
