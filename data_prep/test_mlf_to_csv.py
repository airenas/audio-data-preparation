import unittest

import mlf_to_csv


class TestLattToText(unittest.TestCase):
    def get_phones(self, initial, punct, skip):
        d = mlf_to_csv.LastData()
        d.punct = punct
        d.phones = initial
        phones = []
        d.add_to(phones, skip)
        return phones

    def test_add_punct(self):
        self.assertEqual(["a"], self.get_phones(["a"], "", False))
        self.assertEqual(["a", ",", "sp"], self.get_phones(["a", "sp"], ",", False))
        self.assertEqual(["a", ","], self.get_phones(["a", "sp"], ",", True))
        self.assertEqual(["a", ",", "sil"], self.get_phones(["a", "sil"], ",", True))
        self.assertEqual(["a", "sp"], self.get_phones(["a", "sp"], "", True))
        self.assertEqual(["a", "sp", "b", ","], self.get_phones(["a", "sp", "b", "sp"], ",", True))
        self.assertEqual(["a", "sp", "b", "sp"], self.get_phones(["a", "sp", "b", "sp"], "", True))


if __name__ == '__main__':
    unittest.main()
