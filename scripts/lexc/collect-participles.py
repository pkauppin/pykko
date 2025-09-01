import os.path
import re

from scripts.constants import scripts_path
from scripts.file_tools import read_tsv, save_tsv, read_list_tsv
from scripts.inflection.inflector import inflect
from scripts.utils import unpack

datapath = os.path.join(scripts_path, '..', 'lists', 'participles.tsv')


def determine_gradation(participle):
	if re.fullmatch('.+st[uy]', participle):
		return '-'
	if re.fullmatch('.+tt[uy]', participle):
		return 'tt:t'
	if re.fullmatch('.+t[uy]', participle):
		return 't:d'
	return '-'


def sortkey(row):
	_, lemma, _, pos = row[0:4]
	return pos, lemma


# data = read_tsv(datapath)
data = []

for row in read_list_tsv('lexicon.tsv'):

	_, lemma, hom, pos, kotus_classes, gradations, harmonies, _, info, _ = row

	if pos != 'verb':
		continue
	if '|' in lemma or '-' in lemma:
		continue
	if 'dubious' in info:
		continue

	for kotus_class, gradation, harmony, _ in unpack(kotus_classes, gradations, harmonies):

		inflections = inflect(lemma, pos, kotus_class, gradation, harmony)

		for lukematon in inflections.get('part_maton', []):
			row = ['', lukematon, '', 'participle', '34', 'tt:t', '', '', '', '']
			data.append(row)
		for lukeva in inflections.get('part_pres', []) + inflections.get('pass|part_pres', []):
			row = ['', lukeva, '', 'participle', '10', '', '', '', '+poss', '']
			data.append(row)
		for lukenut in inflections.get('part_past', []):
			row = ['', lukenut, '', 'participle', '47', '', '', '', '+poss', '']
			data.append(row)
		for luettu in inflections.get('pass|part_past', []):
			grad = determine_gradation(luettu)
			row = ['', luettu, '', 'participle', '1', grad, '', '', '+poss', '']
			data.append(row)

data = set(tuple(row) for row in data)
data = sorted(data, key=sortkey)
save_tsv(datapath, data)
