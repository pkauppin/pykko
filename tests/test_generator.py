import unittest
from tests.cases_generator import data_placenames
from tools.generate import generate_wordform


class FiParserTests(unittest.TestCase):

	def test_general(self):

		self.


	@staticmethod
	def test_generator_placenames():

		for analysis, forms in data_placenames:
			lemma, pos, homonym, morphtags = analysis
			forms = set(forms)
			generated = generate_wordform(lemma, pos, morphtags, homonym)
			checkbox = '✔️' if generated == forms else '❌'
			if forms != generated:
				print(checkbox, lemma, pos, morphtags, forms, '<>', generated)


