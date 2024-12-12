import re
import copy
from scripts.inflection.inflector import inflect
from scripts.file_tools import read_list_tsv

VOWELS = set('aeiouyäö')
PL2SG = {}
LEMMAS = {}
INFLECTIONS = {}

for row in read_list_tsv('aux-adjectives.tsv'):
	_, w, _, _, c, g, _, _, _, _ = row
	INFLECTIONS[w] = i = inflect(w, 'adjective', c, g)
	for wpl in i.get('pl|nom', []):
		INFLECTIONS[wpl] = i


def cap(form, lemma):
	return lemma[:1] + form[1:]


def segment(lemma):
	parts = re.split('([-|])', lemma)
	tail = parts.pop()
	head = ''.join(parts)
	return head, tail


def inflect_adjective(lemma, main_pos=None):

	head, tail = segment(lemma)
	tailkey = tail.lower()
	inflections = copy.deepcopy(INFLECTIONS[tailkey])

	for key, forms in inflections.items():
		inflections[key] = [f'{head}{cap(form, tail)}' for form in forms]

	inflections['@base'] = [lemma]
	if main_pos in ['noun-pl', 'proper-pl']:
		inflections = {key.replace('pl|', ''): val for key, val in inflections.items()}
		inflections['@stem:possessives:nom'] = inflections['nom']
	else:
		inflections['@stem:possessives:sg:nom'] = inflections['sg|nom']
		inflections['@stem:possessives:sg:gen'] = inflections['sg|gen']
		inflections['@stem:possessives:pl:nom'] = inflections['pl|nom']

	return inflections


def inflect_lemma(lemma, pos=None, kotus_class=None, gradation=None, harmony=None):

	"""
	Given a lemma, return all its homonyms and possible inflections as a dictionary.
	"""

	head, tail = segment(lemma)
	inflections = inflect(tail, pos, kotus_class, gradation, harmony)
	for key, forms in inflections.items():
		inflections[key] = [f'{head}{form}' for form in forms]

	if pos in ['noun-pl', 'proper-pl']:
		inflections['@stem:possessives:nom'] = inflections['@stem:possessives:nom']
	else:
		inflections['@stem:possessives:sg:nom'] = inflections['@stem:possessives']
		inflections['@stem:possessives:sg:gen'] = inflections['@stem:possessives']
		inflections['@stem:possessives:pl:nom'] = inflections['@stem:possessives']

	return inflections


def paste_congruent(tables: list):

	keys = {key for infl in tables for key in infl.keys()}
	for infl in tables:
		keys = keys & set(infl.keys())

	base = {key: [] for key in keys}
	for key in keys:
		combinations = ['']
		for infl in tables:
			combinations = [
				f'{f1}%{f2}' if f1 and f2 else
				f2 for f1 in combinations for f2 in infl[key]
			]
		base[key] = combinations
	return base


def inflect_51(s, pos=None, kotus_class=None, gradation=None, harmony=None):
	words = s.split('%')
	main = words.pop()
	tables = [inflect_adjective(word, main_pos=pos) for word in words] + \
			 [inflect_lemma(main, pos, kotus_class, gradation, harmony)]
	return paste_congruent(tables)


if __name__ == '__main__':
	from pprint import pprint
	pprint(inflect_51('Pienet%-Antillit', pos='noun-pl', kotus_class='6', gradation='nt:nn'))
	pprint(inflect_51('Uusi%-Seelanti', pos='noun', kotus_class='5', gradation='nt:nn'))
	pprint(inflect_51('oma%tunto', pos='noun', kotus_class='1', gradation='nt:nn'))
	pprint(inflect_51('Papua-Uusi%-Guinea', pos='noun', kotus_class='12', gradation=''))
	pprint(inflect_51('musta%viini|marja', 'noun', '9', ''))
	pprint(inflect_51('isot%aivot', 'noun-pl', '1', ''))
	pprint(inflect_51('nuori%isäntä', 'noun', '10', 'nt:nn'))
	pprint(inflect_51('iso|lentävä%koira', 'noun', '10', ''))
	pprint(inflect_51('comoron|lentävä%koira', 'noun', '10', ''))
