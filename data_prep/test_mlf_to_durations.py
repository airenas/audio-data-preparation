from data_prep import mlf_to_durations
from data_prep.mlf_to_durations import update_durations


def test_calc_duration():
    assert 22 == mlf_to_durations.calc_duration("2500000", 0, 256, 22050)
    assert 12 == mlf_to_durations.calc_duration("4000000", 22, 256, 22050)
    assert 13 == mlf_to_durations.calc_duration("5400000", 34, 256, 22050)
    assert 823 == mlf_to_durations.calc_duration("95550000", 0, 256, 22050)
    assert 805 == mlf_to_durations.calc_duration("93460000", 0, 256, 22050)


def test_fix_duration():
    assert 0 == mlf_to_durations.fix_duration(10, 2559, 256)
    assert 1 == mlf_to_durations.fix_duration(10, 2561, 256)
    assert 1 == mlf_to_durations.fix_duration(10, 2560, 256)


def get_durations(initial, punct, last):
    d = mlf_to_durations.LastData()
    d.punct = punct
    d.durations = initial
    d.last_phone = last
    durations = []
    d.add_to(durations)
    return durations


def test_add_durations():
    assert [10, 5] == get_durations([10, 5], "", "a")
    assert [10, 5, 0] == get_durations([10, 5], ",", "a")
    assert [10, 5] == get_durations([10, 5], ",", "sp")
    assert [10, 3, 1] == get_durations([10, 4], ",", "sil")
    assert [10, 5] == get_durations([10, 5], "", "sp")
    assert [10, 4] == get_durations([10, 4], "", "sil")
    assert [10, 5, 10, 30] == get_durations([10, 5, 40], ",", "sil")


def test_update_durations():
    assert [10, 5] == update_durations([10, 5], 0)
    assert [10, 5, 3] == update_durations([10, 5, 2], 1)
    assert [10, 5, 1] == update_durations([10, 5, 2], -1)
    assert [10, 3, 0] == update_durations([10, 5, 2], -4)
