import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ExampleDigestTest(unittest.TestCase):
    def test_compact_example_is_checked(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/check.py", "examples/ideas-first-project", "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["result"], "PASS")

    def test_digest_is_stable_json(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/example_digest.py", "examples/ideas-first-project"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(json.loads(result.stdout)["files"]), 2)


if __name__ == "__main__":
    unittest.main()
