import re
import os
from glob import glob
from scripts.constants import scripts_path
from scripts.utils import unpack
from scripts.file_tools import read_tsv, save_tsv, read_list_tsv
from scripts.inflection.inflector import inflect

filenames = ['lexicon.tsv'] + glob(os.path.join(scripts_path, '..', 'lists', 'gaz-*.tsv'))
adjectives = {}
gen2nom = {}
pl2sg = {}

for filename in filenames:
	for row in read_list_tsv(filename):

		_, lemma, _, pos, kotus_classes, gradations, _, _, _, _ = row

		if pos not in {'adjective', 'pronoun'}:
			continue

		if not kotus_classes.strip('!'):
			continue

		for kotus_class, grad, _, _ in unpack(kotus_classes, gradations):
			infl = inflect(lemma, 'adjective', kotus_class, grad)
			for gen in infl.get('sg|gen'):
				gen2nom[gen] = lemma
			for pl in infl.get('pl|nom'):
				pl2sg[pl] = lemma


for filename in filenames:
	for row in read_list_tsv(filename):

		_, lemma, _, pos, _, _, _, _, info, _ = row

		if 'stacked' in info:
			adj, _ = re.split('[|-]', lemma)
			adj = gen2nom.get(adj, adj)
			adjectives[adj] = False
			# print(lemma, '=>', adj)
			continue

		for adj in re.findall('[A-ZÅÄÖa-zåäö]+(?=%)', lemma):
			adj = adj.lower()
			adj = pl2sg.get(adj, adj)
			# print(lemma, '=>', adj)
			adjectives[adj] = False

datapath = os.path.join(scripts_path, '..', 'lists', 'aux-adjectives.tsv')
data = set(tuple(row) for row in read_list_tsv(datapath))

for filename in filenames:
	for row in read_list_tsv(filename):
		_, lemma, hom, pos, kotus_class, grad, harmony, _, info, _ = row
		if lemma in adjectives and pos in {'adjective', 'noun', 'ordinal', 'pronoun'}:
			row = '', lemma, '', 'adjective', kotus_class, grad, '', '', '', ''
			data.add(row)
			adjectives[lemma] = True

data = sorted(data)
save_tsv(datapath, data)
