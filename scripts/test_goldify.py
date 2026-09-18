import json
import subprocess
import sys
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
