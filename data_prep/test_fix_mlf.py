import unittest

import fix_mlf


class TestFix(unittest.TestCase):

    def test_fix_symbols(self):
        self.assertEqual("olia", fix_mlf.fix_symbols('olia'))
        self.assertEqual("olia <-><-->", fix_mlf.fix_symbols('olia <�><-->'))
        self.assertEqual("olia <.>", fix_mlf.fix_symbols('olia <"><.><">'))

    def test_parse(self):
        r = fix_mlf.parse_line("2500000 4000000 -67.517197 ^a: a Aèiû _ / // <->")
        self.assertEqual("-", r.punct)
        self.assertEqual("/", r.phr)
        self.assertEqual("//", r.sent)
        self.assertEqual("a", r.syll)
        self.assertEqual("Aèiû", r.word)
        self.assertEqual("^a:", r.ph)
        self.assertEqual("   2500000", r.from_)
        self.assertEqual("   4000000", r.to)

    def test_parse_punct(self):
        r = fix_mlf.parse_line("2500000 4000000 -67.517197 ^a: a Aèiû4 <.>")
        self.assertEqual(".", r.punct)
        self.assertEqual("", r.phr)
        self.assertEqual("", r.sent)

    def test_parse_punct_3dot(self):
        r = fix_mlf.parse_line("2500000 4000000 -67.517197 ^a: a Aèiû4 <.><.><.>")
        self.assertEqual("...", r.punct)

    def test_parse_sill(self):
        r = fix_mlf.parse_line("2500000 4000000 -67.517197 sill sp sp sp sp <.>")
        self.assertEqual(".", r.punct)
        self.assertEqual("sil", r.ph)
        self.assertEqual("sp", r.phr)
        self.assertEqual("sp", r.sent)

    def test_fix_phone(self):
        self.assertEqual("sil", fix_mlf.fix_phone("sill"))
        self.assertEqual("\"o:", fix_mlf.fix_phone("'\"o:'"))
        self.assertEqual("p'", fix_mlf.fix_phone("p'"))

    def test_trim_accent(self):
        self.assertEqual("olia", fix_mlf.trim_accent("olia9"))
        self.assertEqual("olia", fix_mlf.trim_accent("oli3a"))
        self.assertEqual("olia", fix_mlf.trim_accent("o4lia"))

    def test_fix_ne(self):
        r = fix_mlf.parse_line("2500000 4000000 -67.517197 n ne ne / // <!>")
        self.assertEqual("!", r.punct)
        self.assertEqual("ne", r.word)
        fix_mlf.fix_ne_excl(r)
        self.assertEqual(".", r.punct)

    def test_fix_ne(self):
        res = [fix_mlf.parse_line("2500000 4000000 0 sp sp sp"),
               fix_mlf.parse_line("2500000 4000000 0 a"),
               fix_mlf.parse_line("2500000 4000000 0 s as As")]
        fix_mlf.fix_words(res)
        self.assertEqual("as", res[1].syll)
        self.assertEqual("As", res[1].word)
        self.assertEqual("", res[2].syll)
        self.assertEqual("", res[2].word)

    def test_drop_paranthese(self):
        res = fix_mlf.parse_line("2500000 4000000 0 sp sp sp / // (")
        fix_mlf.drop_parantheses(res)
        self.assertEqual("", res.punct)
        res = fix_mlf.parse_line("2500000 4000000 0 sp sp sp / // )")
        fix_mlf.drop_parantheses(res)
        self.assertEqual("", res.punct)

    def test_fix_sils(self):
        res = [fix_mlf.parse_line("2500000 4000000 0 sil sp sp")]
        fix_mlf.fix_sils(res)
        self.assertEqual("sp", res[0].ph)

    def test_fix_sp(self):
        res = [fix_mlf.parse_line("2500000 4000000 0 sp sp sp")]
        res = fix_mlf.fix_sp(res)
        self.assertEqual(1, len(res))
        res = [fix_mlf.parse_line("2500000 2500000 0 sp sp sp")]
        res = fix_mlf.fix_sp(res)
        self.assertEqual(0, len(res))

    def test_fix_lines(self):
        res = [fix_mlf.parse_line("2500000 2500000 0 sp sp sp")]
        res = fix_mlf.fix_lines(res)
        self.assertEqual(0, len(res))


if __name__ == '__main__':
    unittest.main()
