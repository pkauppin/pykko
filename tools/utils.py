import re
import hfst
from scripts.constants import PARSER_FST_PATH, FIELD_STRING

C = "[bcdfghjklmnpqrstvwxzšžčśźćń'’]"
V = '[aeiouyäöüåáéíóúâêîôûãø]'

try:
	input_stream = hfst.HfstInputStream(PARSER_FST_PATH)
	PARSER_FST = input_stream.read()
	input_stream.close()
except:
	PARSER_FST = hfst.regex('?*')


inf = float('inf')


def unk_result(wordform):
	return FIELD_STRING % wordform


def remove_separators(lemma, wordform=None):

	# TODO: Actually do this in a way that takes vertical lines in wordform into consideration.

	return lemma.replace('|', '').replace('⁅HYPHEN⁆', '-').replace('⁅BOUNDARY⁆', '')


def lookup(wordform):
	return PARSER_FST.lookup(wordform)


def analyze(word, only_best=True, normalize_separators=True, ignore_derivatives=True):

	"""
	Return list of tuples (morphological analyses) with duplicates removed.
	Only best analyses are returned by default.
	"""

	analyses = []
	taken = {}
	best_weight = inf
	for analysis_string, weight in PARSER_FST.lookup(word):

		if normalize_separators:
			analysis_string = analysis_string.replace('⁅BOUNDARY⁆', '|').replace('⁅HYPHEN⁆', '-')

		if taken.get(analysis_string):
			continue

		if only_best and weight >= best_weight:
			break

		taken[analysis_string] = True
		analysis = [word] + analysis_string.split('\t') + [weight]
		analyses.append(analysis)
		best_weight = weight

	filtered = analyses
	filtered = filtered or [([word] + unk_result(word).split('\t') + [inf])]

	return [tuple(a) for a in filtered]


def add_compound_separators(word, pos=None, normalize_separators=True, pick_first=False):

	# TODO: Allow adding separators to non-lemma words?

	valid = set()
	best = inf
	for a in analyze(word, only_best=False, normalize_separators=normalize_separators):
		_, _, lemma, p, _, _, _, weight = a
		if pos and p != pos:
			continue
		if weight > best:
			break
		if remove_separators(lemma) == word:
			valid.add(lemma)
			best = weight
	if pick_first:
		return sorted(valid or {word})[0]
	return valid or {word}


def is_plural(word):
	for _, _, lemma, pos, _, _, morphtags, weight in analyze(word, only_best=True):
		if morphtags == '+pl+nom':
			return lemma
		if pos == 'noun-pl' and morphtags == '+nom':
			return lemma
	return False


def singularize(word):
	return is_plural(word) or word


def pos_tag(word, force_match=False, max_weight=inf):

	if force_match:
		tags = set()
		best_weight = max_weight
		for _, _, w, pos, _, _, _, weight in analyze(word, only_best=False):
			if weight == inf or weight > best_weight:
				break
			if remove_separators(w) == word and pos:
				tags.add(pos)
				best_weight = weight
		return tags

	return set(
		pos for _, _, w, pos, _, _, _, weight in analyze(word, only_best=True) if remove_separators(w) == word and pos
		if weight <= max_weight
	)


def lemmatize(word, pos=None):
	valid = set()
	for a in analyze(word, only_best=True):
		_, _, w, p, _, _, _, _ = a
		if pos and p != pos:
			continue
		valid.add(w)
	return valid


def syllabify(word, pos=None, compound=True, big_words=False):

	word = add_compound_separators(word, pos, pick_first=True) if compound else word

	# lito·grafia, mikro·skooppi (alternative syllabification)
	if big_words:
		word = re.sub(f'(?<=[a-zåäö])(sfääri|skooppi|skopia|skooppinen|struktio|stratus|steroli|globiini|glossa|glossia|grafia|grafinen|grafi|glasiaalinen|staattinen)$', r'·\1', word)
		word = re.sub(f'^(ambi|amfi|andro|anti|antropo|arkeo|astro|ekstra|endo|ferro|geo|heksa|hepta|hetero|homo|hydro|hygro|hyper|hypo|iktyo|inter|intra|karbo|kata|kontra|kryo|krypto|kseno|labio|leuko|lito|magneto|makro|media|meta|mikro|okta|penta|pyro|sub|super|supra|tetra|ultra)(?=[a-zåäö])', r'\1·', word)
	if big_words:
		word = re.sub(f'(?<=[a-zåäöü])(stad|stadt|stetten|städte|bridge|brücken|spitz|spitze|spitzen|thorpe|shire|chester|grad|sted|stead|stedt)$', r'·\1', word)

	# ma·ya
	word = re.sub(f'(?<=[aeiou])(?=y[aeou])', '·', word)

	# ikty·ologi, viipy·ä
	word = re.sub(f'(?<=[a-zåäö]y)(?=[äo])', '·', word)

	# make·a
	word = re.sub(f'(?<=[eiouö])(?=[aä])', '·', word)

	# selvi·ö
	word = re.sub(f'(?<=[aeiouä])(?=ö)', '·', word)

	# alki·o
	word = re.sub(f'(?<=[aeiäö])(?=o)', '·', word)

	# ko·e
	word = re.sub(f'(?<=[aouäö])(?=e)', '·', word)

	# kan·si, kant·ti, angs·ti, halst·rata
	word = re.sub(f'(?<={V})({C}+)(?={C}{V})', r'\1·', word)
	word = re.sub(f'(?<={V})({C}+)(?={C}{V})', r'\1·', word)

	# ka·la
	word = re.sub(f'(?<={V})(?={C}{V})', '·', word)

	# kofe·iini, Mari·aanit
	word = re.sub(f'(?<={V})(?=aa|ee|ii|oo|uu|yy|ää|öö)', '·', word)

	# kau·an, liu·os
	word = re.sub(f'(?<=[aeiou][iu])(?={V})', '·', word)

	# nei·yt
	word = re.sub(f'(?<=[äeiöy][iy])(?={V})', '·', word)

	# ruo·an
	word = re.sub(f'(?<=ie|uo|yö)(?={V})', '·', word)

	# raa·istua
	word = re.sub(f'(?<=aa|ee|ii|oo|uu|yy|ää|öö)(?={V})', '·', word)

	# cesi·um
	word = re.sub(f'(?<=[ei])(?=um)', '·', word)

	return word


def add_compound_separators_to_proper_name(name):

	def restore_letter_case(s, n):
		segments = []
		for part in s.split('|'):
			segment, n = n[:len(part)], n[len(part):]
			segments.append(segment)
		return '|'.join(segments)

	for pos in 'proper-pl', 'proper':
		separated = add_compound_separators(name, pos)
		if separated != {name}:
			return separated
	word = name.lower()
	for pos in 'noun-pl', 'noun':
		separated = add_compound_separators(word, pos)
		if separated != {word}:
			separated = {restore_letter_case(s, name) for s in separated}
			return separated

	return {name}


def transfer_separators(source, target):

	"""
	Copy compound separators from source string to target string (which may be different inflected form and/or use different lettercase).
	"""

	target0 = target
	segments = []
	for part in source.split('|')[:-1]:
		if target.lower().startswith(part.lower()):
			segments.append(target[:len(part)])
			target = target[len(part):]
		else:
			return target0
	segments.append(target)
	return '|'.join(segments)