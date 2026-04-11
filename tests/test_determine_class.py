import unittest
from scripts.determine_inflection_class import determine_inflection_class


def determine_class(word, pos):
    cl = determine_inflection_class(word, pos)
    return [(x.strip('?'), y) for x, y in cl]


class FiParserTests(unittest.TestCase):

    def test_all(self):

        self.assertEqual(determine_class('häritsiäiset', pos='noun-pl'), [('38', '')])
        self.assertEqual(determine_class('vihnekset', pos='noun-pl'), [('39', '')])
        self.assertEqual(determine_class('pulahdella', pos='verb'), [('67', 't:d')])
        self.assertEqual(determine_class('lofootti', pos='noun'), [('5', 'tt:t')])
        self.assertEqual(determine_class('lofootit', pos='noun-pl'), [('5', 'tt:t')])
        self.assertEqual(determine_class('garifi', pos='noun'), [('5', '')])
        self.assertEqual(determine_class('garif', pos='noun'), [('5', '')])
        self.assertEqual(determine_class('darkkari', pos='noun'), [('6', '')])
        self.assertEqual(determine_class('chanel', pos='noun'), [('6', '')])
        self.assertEqual(determine_class('halloween', pos='noun'), [('5', '')])
        self.assertEqual(determine_class('bottom', pos='noun'), [('5', '')])
        self.assertEqual(determine_class('läppäri', pos='noun'), [('6', '')])
        self.assertEqual(determine_class('länkkäri', pos='noun'), [('6', '')])
        self.assertEqual(determine_class('signaali', pos='noun'), [('6', '')])
        self.assertEqual(determine_class('ylppärit', pos='noun-pl'), [('6', '')])
        self.assertEqual(determine_class('henkkarit', pos='noun-pl'), [('6', '')])
        self.assertEqual(determine_class('fyrkkendaali', pos='noun'), [('5', '')])
        self.assertEqual(determine_class('funikulaari', pos='noun'), [('5', '')])
        self.assertEqual(determine_class('garnityyri', pos='noun'), [('5', '')])
        self.assertEqual(determine_class('eari', pos='noun'), [('5', '')])
        self.assertEqual(determine_class('piiri', pos='noun'), [('5', '')])
        self.assertEqual(determine_class('fyssa', pos='noun'), [('10', '')])
        self.assertEqual(determine_class('fyrkka', pos='noun'), [('10', 'kk:k')])
        self.assertEqual(determine_class('fygy', pos='noun'), [('1', '')])
        self.assertEqual(determine_class('fyffe', pos='noun'), [('8', '')])
        self.assertEqual(determine_class('tyty', pos='noun'), [('1', '')])
        self.assertEqual(determine_class('kätsy', pos='adjective'), [('1', '')])
        self.assertEqual(determine_class('ronkeli', pos='adjective'), [('6', '')])

        self.assertEqual(determine_class('säätää', pos='verb'), [('53', 't:d')])

        self.assertEqual(determine_class('Tom', pos='noun'), [('5', '')])
        self.assertEqual(determine_class('Ton', pos='noun'), [('5', '')])
        self.assertEqual(determine_class('Tol', pos='noun'), [('5', '')])

        self.assertEqual(determine_class('kommutatiivisuus', pos='noun'), [('40', '')])
        self.assertEqual(determine_class('stuoli', pos='noun'), [('5', '')])
        self.assertEqual(determine_class('ribsi', pos='noun'), [('5', '')])
        self.assertEqual(determine_class('cassoulet', pos='noun'), [('5|22', '')])

        self.assertEqual(determine_class('tavara', pos='noun'), [('12', '')])
        self.assertEqual(determine_class('Sahara', pos='noun'), [('12', '')])
        self.assertEqual(determine_class('kutoja', pos='noun'), [('10', '')])
        self.assertEqual(determine_class('Utøya', pos='noun'), [('10', '')])
        self.assertEqual(determine_class('Kahlua', pos='noun'), [('12', '')])
        self.assertEqual(determine_class('Camilla', pos='noun'), [('13', '')])
        self.assertEqual(determine_class('kaldera', pos='noun'), [('13', '')])
        self.assertEqual(determine_class('apila', pos='noun'), [('13', '')])
        self.assertEqual(determine_class('Bahama', pos='noun'), [('10', '')])
        self.assertEqual(determine_class('Hilkka', pos='noun'), [('9', 'kk:k')])
        self.assertEqual(determine_class('Marjatta', pos='noun'), [('9', 'tt:t')])
        self.assertEqual(determine_class('Ritva', pos='noun'), [('9', '')])

        # Lexicon-based

        self.assertEqual(determine_class('karboksyyli|happo', pos='noun'), [('1', 'pp:p')])
        self.assertEqual(determine_class('sunda|saaret', pos='noun-pl'), [('26', '')])
        self.assertEqual(determine_class('huippu|kallis', pos='adjective'), [('41', '')])
        self.assertEqual(determine_class('rescue|koira', pos='adjective'), [('10', '')])
        self.assertEqual(determine_class('sunda|saari', pos='noun'), [('26', '')])
        self.assertEqual(determine_class('Häkä|mies', pos='proper'), [('42', '')])


if __name__ == '__main__':
    unittest.main()
