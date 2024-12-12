import unittest
from tools.utils import syllabify, pos_tag, lemmatize, add_compound_separators


class ToolTests(unittest.TestCase):

    def test_lemmatize(self):
        self.assertEqual(lemmatize('autoani'), {'auto'})
        self.assertEqual(lemmatize('kanssaan'), {'kanssa'})
        self.assertEqual(lemmatize('pimeää'), {'pimeä'})
        self.assertEqual(lemmatize('hienoiten'), {'hienosti'})
        self.assertEqual(lemmatize('hauskempaa'), {'hauska'})
        self.assertEqual(lemmatize('kuusi'), {'kuusi', 'kuu'})
        self.assertEqual(lemmatize('muista'), {'muistaa', 'muu'})
        self.assertEqual(lemmatize('myyhän'), {'myydä', 'myy'})
        self.assertEqual(lemmatize('hauista'), {'hauki', 'hauis', 'haku'})

    def test_pos_tag(self):
        # Nominals
        self.assertEqual(pos_tag('viini'), {'noun'})
        self.assertEqual(pos_tag('kuusi'), {'noun', 'numeral'})
        self.assertEqual(pos_tag('pimeä'), {'adjective', 'noun'})
        self.assertEqual(pos_tag('taata'), {'verb', 'noun'})
        # Adverbs
        self.assertEqual(pos_tag('myös'), {'adverb'})
        self.assertEqual(pos_tag('ulkona'), {'adverb'})
        self.assertEqual(pos_tag('kauniisti'), {'adverb'})
        self.assertEqual(pos_tag('puolestaan'), {'adverb'})
        self.assertEqual(pos_tag('hämillään'), {'adverb'})
        self.assertEqual(pos_tag('puoliksi'), {'adverb'})
        # Adverbs / Adpositions
        self.assertEqual(pos_tag('edessä'), {'adverb', 'adposition'})
        self.assertEqual(pos_tag('mukana'), {'adverb', 'adposition'})
        self.assertEqual(pos_tag('kanssa'), {'adverb', 'adposition'})
        # Adpositions
        self.assertEqual(pos_tag('takia'), {'adposition'})
        self.assertEqual(pos_tag('luona'), {'adposition'})
        self.assertEqual(pos_tag('tähden'), {'adposition'})
        self.assertEqual(pos_tag('aikana'), {'adposition'})

    def test_add_compound_separators(self):
        self.assertEqual(add_compound_separators('etäisyys'), {'etäisyys'})
        self.assertEqual(add_compound_separators('paloilta'), {'palo|ilta'})
        self.assertEqual(add_compound_separators('ratasilta'), {'ratas|ilta', 'rata|silta'})
        self.assertEqual(add_compound_separators('perheenisyys'), {'perheen|isyys'})
        self.assertEqual(add_compound_separators('iltapalasokeri'), {'ilta|pala|sokeri'})
        self.assertEqual(add_compound_separators('makuualustatalous'), {'makuu|alusta|talous'})
        # self.assertEqual(add_compound_separators('xxxläistoimittaja'), {'xxxläis|toimittaja'})  # FIXME

    def test_add_compound_separators_no_normalization(self):
        self.assertEqual(add_compound_separators('kesäkuu', normalize_separators=False), {'kesä|kuu'})
        self.assertEqual(add_compound_separators('paloilta', normalize_separators=False), {'palo⁅BOUNDARY⁆ilta'})
        self.assertEqual(add_compound_separators('ratasilta', normalize_separators=False), {'ratas⁅BOUNDARY⁆ilta', 'rata⁅BOUNDARY⁆silta'})

    def test_syllabification(self):
        self.assertEqual(syllabify('kala'), 'ka·la')
        self.assertEqual(syllabify('portti'), 'port·ti')
        self.assertEqual(syllabify('tärkeä'), 'tär·ke·ä')
        self.assertEqual(syllabify('kuitenkin'), 'kui·ten·kin')
        self.assertEqual(syllabify('vehnänalkio'), 'veh·nän|al·ki·o')
        self.assertEqual(syllabify('häivehävittäjälaivue'), 'häi·ve|hä·vit·tä·jä|lai·vu·e')
        self.assertEqual(syllabify('vaa’ankieliosavaltio'), 'vaa·’an|kie·li|o·sa|val·ti·o')
        self.assertEqual(syllabify('sisilisko'), 'si·si·lis·ko')
        self.assertEqual(syllabify('Harjavalta'), 'Har·ja·val·ta')
        self.assertEqual(syllabify('iktyologi'), 'ik·ty·o·lo·gi')
        self.assertEqual(syllabify('maya'), 'ma·ya')
        self.assertEqual(syllabify('yo-yo'), 'yo-yo')
        self.assertEqual(syllabify('kaksintaa'), 'kak·sin·taa')
        self.assertEqual(syllabify('liuottaa'), 'liu·ot·taa')
        self.assertEqual(syllabify('rääyttää'), 'rää·yt·tää')
        # self.assertEqual(syllabify('layout'), '')


if __name__ == '__main__':
    unittest.main()
