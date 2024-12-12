import os.path
from scripts.constants import scripts_path
from scripts.file_tools import read_tsv, save_tsv, read_list_tsv
from scripts.inflection.inflector import inflect

datapath = os.path.join(scripts_path, '..', 'lists', 'participles.tsv')


def sortkey(row):
	_, lemma, _, pos = row[0:4]
	return pos, lemma


data = read_tsv(datapath)

for row in read_list_tsv('lexicon.tsv'):

	_, lemma, hom, pos, kotus_class, grad, harmony, _, info, _ = row

	if pos != 'verb':
		continue
	if '|' in lemma or '-' in lemma:
		continue

	inflections = inflect(lemma, pos, kotus_class, grad, harmony)
	for lukematon in inflections.get('part_maton', []):
		row = ['', lukematon, '', 'participle', '34', 'tt:t', '', '', '', '']
		data.append(row)
	for lukeva in inflections.get('part_pres', []) + inflections.get('pass|part_pres', []):
		row = ['', lukeva, '', 'participle', '10', '', '', '', '+poss', '']
		data.append(row)

data = set(tuple(row) for row in data)
data = sorted(data, key=sortkey)
save_tsv(datapath, data)
