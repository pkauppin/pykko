import json
from tools.utils import analyze


def show_test_failure(actual, expected):
	print('· ANALYSES:')
	for a in actual or ['']:
		print('', json.dumps(list(a), ensure_ascii=False), sep='\t')
	print('· SHOULD BE:')
	for a in expected or ['']:
		print('', json.dumps(list(a), ensure_ascii=False), sep='\t')


def filtered_analyses(wordform, has_source=None, has_pos=None, casematch=False, only_best=True):

	analyses = []

	# for analysis in analyze(wordform, only_best=False):
	# 	print('>', analysis)

	for analysis in analyze(wordform, only_best=only_best):

		_, source, lemma, pos, _, _, tags, weight = analysis

		if source not in (has_source or {source}):
			continue
		if pos not in (has_pos or {pos}):
			continue

		if casematch and lettercase(lemma) != lettercase(wordform):
			continue

		analyses.append((lemma, pos, tags))

	return set(analyses)


def lettercase(s):
	i = s[0:1]
	if i.upper() == i.lower() == i:
		return None
	if i.upper() == i:
		return 'uppercase'
	return 'lowercase'
