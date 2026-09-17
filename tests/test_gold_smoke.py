import unittest
from pathlib import Path


class GoldSmokeTest(unittest.TestCase):
    def test_gold_template_exists(self):
        root = Path(__file__).resolve().parents[1]
        self.assertTrue((root / "templates" / "gold" / "README.md").is_file())


if __name__ == "__main__":
    unittest.main()
