import unittest

from src.main import main


class MainTest(unittest.TestCase):
    def test_main_is_deterministic(self):
        self.assertEqual("hello gold", main())


if __name__ == "__main__":
    unittest.main()
