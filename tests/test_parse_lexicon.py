import unittest
from tests.utils import filtered_analyses, show_test_failure
from scripts.file_tools import load_json


class FiParserTests(unittest.TestCase):

	def test_01(self):

		cases = load_json(filename='cases_lexicon.json')

		for word, target in cases.items():

			target = set(tuple(a) for a in target)
			analyses = filtered_analyses(word, has_source={'Lexicon', 'Lexicon|Num'})

			if target == analyses:
				print('[✓]', word)
			elif analyses:
				print('[✗]', word)
				show_test_failure(actual=analyses, expected=target)
			else:
				print('[ ]', word)
			# self.assertEqual(analyses, target)
		print('Ok.')