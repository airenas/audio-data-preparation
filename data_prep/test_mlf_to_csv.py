from data_prep import mlf_to_csv


def get_phones(initial, punct, skip):
    d = mlf_to_csv.LastData()
    d.punct = punct
    d.phones = initial
    phones = []
    d.add_to(phones, skip)
    return phones


def test_add_punct():
    assert ["a"] == get_phones(["a"], "", False)
    assert ["a", ",", "sp"] == get_phones(["a", "sp"], ",", False)
    assert ["a", ","] == get_phones(["a", "sp"], ",", True)
    assert ["a", ",", "sil"] == get_phones(["a", "sil"], ",", True)
    assert ["a", "sp"] == get_phones(["a", "sp"], "", True)
    assert ["a", "sp", "b", ","] == get_phones(["a", "sp", "b", "sp"], ",", True)
    assert ["a", "sp", "b", "sp"] == get_phones(["a", "sp", "b", "sp"], "", True)
