import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class GoldifyTest(unittest.TestCase):
    def test_fixture_produces_minimal_read_only_diff(self):
        target = ROOT / "fixtures" / "goldify-project"
        result = subprocess.run([sys.executable, "scripts/goldify.py", str(target), "--json"], cwd=ROOT, capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        self.assertFalse(report["writes"])
        self.assertTrue(any(item.startswith("AGENTS.md") for item in report["necessary"]))
        self.assertIn("README.md", report["user_owned"])

    def test_gold_example_has_no_required_gap(self):
        target = ROOT / "examples" / "gold-standard"
        result = subprocess.run([sys.executable, "scripts/goldify.py", str(target), "--json"], cwd=ROOT, capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        self.assertFalse(report["writes"])
        self.assertNotIn("README.md: explicar propósito e verificação", report["necessary"])

    def test_existing_scripts_check_is_detected_without_reorganization(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            (target / "scripts").mkdir(parents=True)
            (target / "scripts" / "check.py").write_text("# existing check\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "scripts/goldify.py", str(target), "--json"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
            report = json.loads(result.stdout)
            self.assertTrue(report["inventory"]["check"])
            self.assertNotIn("check reproduzível: documentar ou criar comando existente", report["recommended"])

    def test_invalid_paths_fail_before_any_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing"
            file_path = Path(tmp) / "project.txt"
            file_path.write_text("not a project", encoding="utf-8")
            for path in (missing, file_path):
                result = subprocess.run(
                    [sys.executable, "scripts/goldify.py", str(path), "--json"],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                self.assertNotEqual(0, result.returncode)
                self.assertIn("IS-GOLD-001", result.stderr)
