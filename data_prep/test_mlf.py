import unittest

import mlf


class TestMlf(unittest.TestCase):

    def test_create(self):
        self.assertEqual("   8600000    9100000 p pa padėkojo / //",
                         mlf.from_str("   8600000    9100000 p pa padėkojo / //").str())
        self.assertEqual("   8600000    9100000 p pa padėkojo / //",
                         mlf.from_str("   8600000    9100000 p pa padėkojo / //").str())
        self.assertEqual("   8600000    9100000 p pa padėkojo",
                         mlf.from_str("   8600000    9100000 p pa padėkojo").str())

    def test_is_word(self):
        ml = mlf.from_str("   8600000    9100000 p pa padėkojo")
        self.assertTrue(ml.is_word())
        ml = mlf.from_str("   7500000    8600000 sil sp sp")
        self.assertFalse(ml.is_word())

    def test_punct(self):
        ml = mlf.from_str("   2500000    4000000 ^a: a Ačiū / //     ,")
        self.assertEqual(",", ml.punct)


if __name__ == '__main__':
    unittest.main()
