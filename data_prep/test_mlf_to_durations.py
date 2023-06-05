import unittest

import mlf_to_durations


class TestCalcDuration(unittest.TestCase):
    def test_calc_duration(self):
        self.assertEqual(22, mlf_to_durations.calc_duration("2500000", 0, 256, 22050))
        self.assertEqual(12, mlf_to_durations.calc_duration("4000000", 22, 256, 22050))
        self.assertEqual(13, mlf_to_durations.calc_duration("5400000", 34, 256, 22050))
        self.assertEqual(823, mlf_to_durations.calc_duration("95550000", 0, 256, 22050))
        self.assertEqual(805, mlf_to_durations.calc_duration("93460000", 0, 256, 22050))

    def test_fix_duration(self):
        self.assertEqual(0, mlf_to_durations.fix_duration(10, 2559, 256))
        self.assertEqual(1, mlf_to_durations.fix_duration(10, 2561, 256))
        self.assertEqual(1, mlf_to_durations.fix_duration(10, 2560, 256))


class TestAddDuration(unittest.TestCase):

    def get_durations(self, initial, punct, last):
        d = mlf_to_durations.LastData()
        d.punct = punct
        d.durations = initial
        d.last_phone = last
        durations = []
        d.add_to(durations)
        return durations

    def test_add_durations(self):
        self.assertEqual([10, 5], self.get_durations([10, 5], "", "a"))
        self.assertEqual([10, 5, 0], self.get_durations([10, 5], ",", "a"))
        self.assertEqual([10, 5], self.get_durations([10, 5], ",", "sp"))
        self.assertEqual([10, 3, 1], self.get_durations([10, 4], ",", "sil"))
        self.assertEqual([10, 5], self.get_durations([10, 5], "", "sp"))
        self.assertEqual([10, 4], self.get_durations([10, 4], "", "sil"))
        self.assertEqual([10, 5, 10, 30], self.get_durations([10, 5, 40], ",", "sil"))


if __name__ == '__main__':
    unittest.main()
