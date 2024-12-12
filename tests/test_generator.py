import unittest
from tests.cases_generator import data
from tools.generate import generate_wordform


class FiParserTests(unittest.TestCase):

	def test_generator(self):

		for analysis, forms in data:

			lemma, pos, homonym, morphtags = analysis

			forms = set(forms)
			generated = generate_wordform(lemma, pos, morphtags, homonym)
			checkbox = '✔️' if generated == forms else '❌'
			if forms != generated:
				print(checkbox, lemma, pos, morphtags, forms, '<>', generated)

	# TODO
	# - Rautalampi (homonymy?)
	# - Uusikaarlepyy (?)
