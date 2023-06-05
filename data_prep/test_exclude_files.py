import unittest

import exclude_files


class TestFix(unittest.TestCase):

    def test_fix_symbols(self):
        self.assertEqual("olia", exclude_files.get_fn("\"olia.lab\""))
        self.assertEqual("132131_1313", exclude_files.get_fn("\"132131_1313.lab\""))


if __name__ == '__main__':
    unittest.main()
