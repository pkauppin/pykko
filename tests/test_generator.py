import unittest
from tests.cases_generator import data_placenames
from tools.generate import generate_wordform as wordform, generate_forms, generate_inflection_paradigm


class FiParserTests(unittest.TestCase):

	def test_generate_wordform(self):

		self.assertEqual(wordform('suuri', 'adjective', '+sg+gen'), {'suuren'})
		self.assertEqual(wordform('kissakoira', 'noun', '+pl+par', source='Lexicon|Pfx'), {'kissakoiria'})
		self.assertEqual(wordform('-rakenteinen', 'adjective', '+sg+ine', source='Lexicon|Hyp'), {'-rakenteisessa'})
		self.assertEqual(wordform('-valkoinen', 'adjective', '+sg+ine', source='Lexicon|Hyp'), {'-valkoisessa'})
		self.assertEqual(wordform('a-rakenteinen', 'adjective', '+sg+ine', source='Lexicon|Hyp'), {'a-rakenteisessa'})
		self.assertEqual(wordform('a-valkoinen', 'adjective', '+sg+ine', source='Lexicon|Hyp'), {'a-valkoisessa'})
		self.assertEqual(wordform('16', 'numeral', '+sg+ine', source='Lexicon'), {'16:ssa'})
		self.assertEqual(wordform('16:s', 'ordinal', '+sg+ine', source='Lexicon'), {'16:nnessa'})

	def test_generate_forms(self):

		self.assertTrue(generate_forms('koira') > {'koiran', 'koiraa', 'koirat'}),

		self.assertTrue(generate_forms('taata') > {'taatan', 'taataa', 'taatoja', 'takaan', 'takaa', 'takasi'}),
		self.assertTrue(generate_forms('taata', pos='verb') > {'takaan', 'takaa', 'takasi'})
		self.assertTrue(generate_forms('taata', pos='noun') > {'taatan', 'taataa', 'taatoja'})

		self.assertTrue(generate_forms('tavata') > {'tapaan', 'tavaan', 'tapaa', 'tavaa', 'tapasi', 'tavasi'})
		self.assertTrue(generate_forms('tavata', homonym="1") > {'tapaan', 'tapaa', 'tapasi'})
		self.assertTrue(generate_forms('tavata', homonym="2") > {'tavaan', 'tavaa', 'tavasi'})

		self.assertTrue(generate_forms('ahtaus') > {'ahtauden', 'ahtauksen', 'ahtautta', 'ahtausta', 'ahtauksia'})
		self.assertTrue(generate_forms('ahtaus', homonym="1") > {'ahtauden', 'ahtautta', 'ahtauksia'})
		self.assertTrue(generate_forms('ahtaus', homonym="2") > {'ahtauksen', 'ahtausta', 'ahtauksia'})

		self.assertTrue(generate_forms('ettei') >= {'etten', 'ettet', 'ettei', 'ettemme', 'ettette', 'etteivät'})
		self.assertTrue(generate_forms('possukala') > {'possukalan', 'possukalaa', 'possukaloja'})

	def test_generate_inflection_paradigm(self):

		self.assertTrue(generate_inflection_paradigm('jihuu', pos='interjection')[''], ['jihuu'])
		self.assertTrue(generate_inflection_paradigm('kissa', pos='noun')['+sg+gen'], ['kissan'])
		self.assertTrue(generate_inflection_paradigm('possukala', pos='noun')['+sg+gen'], ['possukalan'])
		self.assertTrue(generate_inflection_paradigm('yltiöharmoninen', pos='adjective')['+sg+gen'], ['yltiöharmonisen'])
		self.assertTrue(generate_inflection_paradigm('myötäsekoittaa', pos='verb')['+pres+1sg'], ['myötäsekoitan'])

	def test_generator_placenames(self):

		for analysis, forms in data_placenames:
			lemma, pos, homonym, morphtags = analysis
			forms = set(forms)
			generated = wordform(lemma, pos, morphtags, homonym)
			checkbox = '✔️' if generated == forms else '❌'
			if forms != generated:
				print(checkbox, lemma, pos, morphtags, forms, '<>', generated)


