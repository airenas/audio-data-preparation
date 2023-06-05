from data_prep import mlf


def test_create():
    assert "   8600000    9100000 p pa padėkojo / //" == mlf.from_str("   8600000    9100000 p pa padėkojo / //").str()
    assert "   8600000    9100000 p pa padėkojo / //" == mlf.from_str("   8600000    9100000 p pa padėkojo / //").str()
    assert "   8600000    9100000 p pa padėkojo" == mlf.from_str("   8600000    9100000 p pa padėkojo").str()


def test_is_word():
    ml = mlf.from_str("   8600000    9100000 p pa padėkojo")
    assert ml.is_word()
    ml = mlf.from_str("   7500000    8600000 sil sp sp")
    assert ml.is_word() is False


def test_punct():
    ml = mlf.from_str("   2500000    4000000 ^a: a Ačiū / //     ,")
    assert "," == ml.punct
