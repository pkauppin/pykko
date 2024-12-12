import unittest
from tests.utils import filtered_analyses


class FiParserTests(unittest.TestCase):

    def test_numeral_8(self):
        analyses = filtered_analyses('kahdeksan', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {
            ('kahdeksan', 'numeral', '+sg+nom'),
            ('kahdeksan', 'numeral', '+sg+gen'),
        })

    def test_numeral_18(self):
        analyses = filtered_analyses('kahdeksantoista', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {
            ('kahdeksan|toista', 'numeral', '+sg+nom'),
            ('kahdeksan|toista', 'numeral', '+sg+gen'),
        })

    def test_numeral_3(self):
        analyses = filtered_analyses('kolmen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme', 'numeral', '+sg+gen')})

    def test_numeral_13(self):
        analyses = filtered_analyses('kolmentoista', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme|toista', 'numeral', '+sg+gen')})

    def test_numeral_30(self):
        analyses = filtered_analyses('kolmenkymmenen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme|kymmentä', 'numeral', '+sg+gen')})

    def test_numeral_300(self):
        analyses = filtered_analyses('kolmensadan', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme|sataa', 'numeral', '+sg+gen')})

    def test_numeral_3000(self):
        analyses = filtered_analyses('kolmentuhannen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme|tuhatta', 'numeral', '+sg+gen')})

    def test_numeral_13000(self):
        analyses = filtered_analyses('kolmentoistatuhannen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme|toista|tuhatta', 'numeral', '+sg+gen')})

    def test_numeral_30000(self):
        analyses = filtered_analyses('kolmenkymmenentuhannen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme|kymmentä|tuhatta', 'numeral', '+sg+gen')})

    def test_numeral_300000(self):
        analyses = filtered_analyses('kolmensadantuhannen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme|sataa|tuhatta', 'numeral', '+sg+gen')})

    def test_numeral_33(self):
        analyses = filtered_analyses('kolmenkymmenenkolmen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme|kymmentä|kolme', 'numeral', '+sg+gen')})

    def test_numeral_313(self):
        analyses = filtered_analyses('kolmensadankolmentoista', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme|sataa|kolme|toista', 'numeral', '+sg+gen')})

    def test_numeral_333(self):
        analyses = filtered_analyses('kolmensadankolmenkymmenenkolmen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme|sataa|kolme|kymmentä|kolme', 'numeral', '+sg+gen')})

    def test_numeral_3_333(self):
        analyses = filtered_analyses('kolmentuhannenkolmensadankolmenkymmenenkolmen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme|tuhatta|kolme|sataa|kolme|kymmentä|kolme', 'numeral', '+sg+gen')})

    def test_numeral_33_333(self):
        analyses = filtered_analyses('kolmenkymmenenkolmentuhannenkolmensadankolmenkymmenenkolmen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme|kymmentä|kolme|tuhatta|kolme|sataa|kolme|kymmentä|kolme', 'numeral', '+sg+gen')})

    def test_numeral_333_333(self):
        analyses = filtered_analyses('kolmensadankolmenkymmenenkolmentuhannenkolmensadankolmenkymmenenkolmen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme|sataa|kolme|kymmentä|kolme|tuhatta|kolme|sataa|kolme|kymmentä|kolme', 'numeral', '+sg+gen')})

    def test_numeral_203(self):
        analyses = filtered_analyses('kolmensadankolmen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme|sataa|kolme', 'numeral', '+sg+gen')})

    def test_numeral_100(self):
        analyses = filtered_analyses('sadan', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('sata', 'numeral', '+sg+gen')})

    def test_numeral_103(self):
        analyses = filtered_analyses('sadankolmen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('sata|kolme', 'numeral', '+sg+gen')})

    def test_numeral_113(self):
        analyses = filtered_analyses('sadankolmentoista', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('sata|kolme|toista', 'numeral', '+sg+gen')})

    def test_numeral_130(self):
        analyses = filtered_analyses('sadankolmenkymmenen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('sata|kolme|kymmentä', 'numeral', '+sg+gen')})

    def test_numeral_1003(self):
        analyses = filtered_analyses('tuhannenkolmen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('tuhat|kolme', 'numeral', '+sg+gen')})

    def test_numeral_1013(self):
        analyses = filtered_analyses('tuhannenkolmentoista', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('tuhat|kolme|toista', 'numeral', '+sg+gen')})

    def test_numeral_1030(self):
        analyses = filtered_analyses('tuhannenkolmenkymmenen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('tuhat|kolme|kymmentä', 'numeral', '+sg+gen')})

    def test_numeral_110(self):
        analyses = filtered_analyses('sadankymmenen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('sata|kymmenen', 'numeral', '+sg+gen')})

    def test_numeral_1010(self):
        analyses = filtered_analyses('tuhannenkymmenen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('tuhat|kymmenen', 'numeral', '+sg+gen')})

    def test_numeral_1100(self):
        analyses = filtered_analyses('tuhannensadan', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('tuhat|sata', 'numeral', '+sg+gen')})

    def test_numeral_1300(self):
        analyses = filtered_analyses('tuhannenkolmensadan', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('tuhat|kolme|sataa', 'numeral', '+sg+gen')})

    """"""

    def test_numeral_kolmienkymmenien(self):
        analyses = filtered_analyses('kolmienkymmenien', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme|kymmentä', 'numeral', '+pl+gen')})

    def test_numeral_kolmissakymmenissa(self):
        analyses = filtered_analyses('kolmissakymmenissä', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolme|kymmentä', 'numeral', '+pl+ine')})

    def test_numeral_kaksiensatojenkaksienkymmenienkin(self):
        analyses = filtered_analyses('kaksiensatojenkaksienkymmenienkin', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kaksi|sataa|kaksi|kymmentä', 'numeral', '+pl+gen+kin')})

    def test_numeral_sadantuhannen(self):
        analyses = filtered_analyses('sadantuhannen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('sata|tuhatta', 'numeral', '+sg+gen')})

    def test_numeral_satojentuhansien(self):
        analyses = filtered_analyses('satojentuhansien', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('sata|tuhatta', 'numeral', '+pl+gen')})

    def test_numeral_tuhansien(self):
        analyses = filtered_analyses('tuhansien', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('tuhat', 'numeral', '+pl+gen')})

    def test_numeral_tuhatta(self):
        analyses = filtered_analyses('tuhatta', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('tuhat', 'numeral', '+sg+par')})

    """"""

    def test_ordinal_20(self):
        analyses = filtered_analyses('kahdennenkymmenennen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kahdes|kymmenes', 'ordinal', '+sg+gen')})

    def test_ordinal_12(self):
        analyses = filtered_analyses('kahdennentoista', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kahdes|toista', 'ordinal', '+sg+gen')})

    def test_ordinal_200(self):
        analyses = filtered_analyses('kahdennensadannen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kahdes|sadas', 'ordinal', '+sg+gen')})

    def test_ordinal_2000(self):
        analyses = filtered_analyses('kahdennentuhannennen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kahdes|tuhannes', 'ordinal', '+sg+gen')})

    def test_ordinal_203(self):
        analyses = filtered_analyses('kahdennensadannenkolmannen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kahdes|sadas|kolmas', 'ordinal', '+sg+gen')})

    def test_ordinal_2003(self):
        analyses = filtered_analyses('kahdennentuhannennenkolmannen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kahdes|tuhannes|kolmas', 'ordinal', '+sg+gen')})

    def test_ordinal_210(self):
        analyses = filtered_analyses('kahdennensadannenkymmenennen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kahdes|sadas|kymmenes', 'ordinal', '+sg+gen')})

    def test_ordinal_2010(self):
        analyses = filtered_analyses('kahdennentuhannennenkymmenennen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kahdes|tuhannes|kymmenes', 'ordinal', '+sg+gen')})

    def test_ordinal_2100(self):
        analyses = filtered_analyses('kahdennentuhannennensadannen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kahdes|tuhannes|sadas', 'ordinal', '+sg+gen')})

    def test_ordinal_30pl(self):
        analyses = filtered_analyses('kolmansienkymmenensien', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('kolmas|kymmenes', 'ordinal', '+pl+gen')})

    def test_ordinal_100000(self):
        analyses = filtered_analyses('sadannentuhannennen', has_source={'Lexicon|Num'})
        self.assertEqual(analyses, {('sadas|tuhannes', 'ordinal', '+sg+gen')})


if __name__ == '__main__':
    unittest.main()
