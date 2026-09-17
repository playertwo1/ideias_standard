import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.main import main


class MainTest(unittest.TestCase):
    def test_main_is_deterministic(self):
        self.assertEqual("hello gold", main())


if __name__ == "__main__":
    unittest.main()
