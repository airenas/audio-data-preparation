from data_prep import exclude_files


def test_fix_symbols():
    assert "olia" == exclude_files.get_fn("\"olia.lab\"")
    assert "132131_1313" == exclude_files.get_fn("\"132131_1313.lab\"")
