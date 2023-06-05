from data_prep import fix_mlf


def test_fix_symbols():
    assert "olia" == fix_mlf.fix_symbols('olia')
    assert "olia <-><-->" == fix_mlf.fix_symbols('olia <�><-->')
    assert "olia <.>" == fix_mlf.fix_symbols('olia <"><.><">')


def test_parse():
    r = fix_mlf.parse_line("2500000 4000000 -67.517197 ^a: a Aèiû _ / // <->")
    assert "-" == r.punct
    assert "/" == r.phr
    assert "//" == r.sent
    assert "a" == r.syll
    assert "Aèiû" == r.word
    assert "^a:" == r.ph
    assert "   2500000" == r.from_
    assert "   4000000" == r.to


def test_parse_punct():
    r = fix_mlf.parse_line("2500000 4000000 -67.517197 ^a: a Aèiû4 <.>")
    assert "." == r.punct
    assert "" == r.phr
    assert "" == r.sent


def test_parse_punct_3dot():
    r = fix_mlf.parse_line("2500000 4000000 -67.517197 ^a: a Aèiû4 <.><.><.>")
    assert "..." == r.punct


def test_parse_sill():
    r = fix_mlf.parse_line("2500000 4000000 -67.517197 sill sp sp sp sp <.>")
    assert "." == r.punct
    assert "sil" == r.ph
    assert "sp" == r.phr
    assert "sp" == r.sent


def test_fix_phone():
    assert "sil" == fix_mlf.fix_phone("sill")
    assert "\"o:" == fix_mlf.fix_phone("'\"o:'")
    assert "p'" == fix_mlf.fix_phone("p'")


def test_trim_accent():
    assert "olia" == fix_mlf.trim_accent("olia9")
    assert "olia" == fix_mlf.trim_accent("oli3a")
    assert "olia" == fix_mlf.trim_accent("o4lia")


def test_fix_ne():
    r = fix_mlf.parse_line("2500000 4000000 -67.517197 n ne ne / // <!>")
    assert "!" == r.punct
    assert "ne" == r.word
    fix_mlf.fix_ne_excl(r)
    assert "." == r.punct
    res = [fix_mlf.parse_line("2500000 4000000 0 sp sp sp"),
           fix_mlf.parse_line("2500000 4000000 0 a"),
           fix_mlf.parse_line("2500000 4000000 0 s as As")]
    fix_mlf.fix_words(res)
    assert "as" == res[1].syll
    assert "As" == res[1].word
    assert "" == res[2].syll
    assert "" == res[2].word


def test_drop_paranthese():
    res = fix_mlf.parse_line("2500000 4000000 0 sp sp sp / // (")
    fix_mlf.drop_parantheses(res)
    assert "" == res.punct
    res = fix_mlf.parse_line("2500000 4000000 0 sp sp sp / // )")
    fix_mlf.drop_parantheses(res)
    assert "" == res.punct


def test_fix_sils():
    res = [fix_mlf.parse_line("2500000 4000000 0 sil sp sp")]
    fix_mlf.fix_sils(res)
    assert "sp" == res[0].ph


def test_fix_sp():
    res = [fix_mlf.parse_line("2500000 4000000 0 sp sp sp")]
    res = fix_mlf.fix_sp(res)
    assert 1 == len(res)
    res = [fix_mlf.parse_line("2500000 2500000 0 sp sp sp")]
    res = fix_mlf.fix_sp(res)
    assert 0 == len(res)


def test_fix_lines():
    res = [fix_mlf.parse_line("2500000 2500000 0 sp sp sp")]
    res = fix_mlf.fix_lines(res)
    assert 0 == len(res)
