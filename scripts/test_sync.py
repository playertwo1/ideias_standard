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
