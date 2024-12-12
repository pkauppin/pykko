from scripts.aligner.utils import *
from scripts.utils import get_morphtag_characters, has_agreement


def separate_stem_with_morphtags(form: str, morphtags: str, pos: str, fossilized: list):

	"""
	Determine stem by finding matching inflectional endings in word form.
	"""

	endings = ''
	form, clitic = separate_fossilized_clitic(form, fossilized)

	for tags, ending in MORPH_ENDINGS[pos]:
		if form.endswith(ending) and morphtags.endswith(tags):
			form = form[:-len(ending)] if ending else form
			endings = ending + endings
			morphtags = morphtags[:-len(tags)] if tags else morphtags

	if morphtags:
		return None

	return form, endings, clitic


def separate_stem_by_auxiliary_stems(form: str, morphtags: str, auxiliary_stems: list):

	"""
	Determine stem by finding matching auxiliary stem.
	"""

	if not auxiliary_stems:
		return form, '', ''

	for tag, stem in auxiliary_stems:
		if morphtags.startswith(tag) and form.startswith(stem):
			ending = form[len(stem):]
			return stem, ending, ''
	print('???', [form, morphtags])
	input()
	return form, '', ''


def separate_stem(form: str, morphtags: str, pos: str, auxiliary_stems: list, fossilized: list):

	# Special cases
	if morphtags == '@stem:clitics':
		return form, '', ''
	if morphtags == '@base' and pos == 'verb':
		return separate_stem(form, 'inf1', 'verb', auxiliary_stems, fossilized)
	if morphtags == '@base' and pos.endswith('-pl') and form in PL_PRONOUNS:
		return form, '0', ''
	if morphtags == '@base' and pos.endswith('-pl'):
		return form[:-1], 't', ''
	if morphtags == '@base':
		return form, '', ''

	morphtags = morphtags if '@' in morphtags else '+' + morphtags.replace('|', '+') if morphtags else ''

	stem, ending, clitic = \
		separate_stem_with_morphtags(form, morphtags, pos, fossilized) or \
		separate_stem_by_auxiliary_stems(form, morphtags, auxiliary_stems)

	return stem, ending, clitic


def separate_stems(inflections: dict, pos: str):

	[baseform] = inflections['@base']
	fossilized = get_fossilized_clitics(baseform, pos)

	auxiliary_stems = get_auxiliary_stems(inflections, pos, fossilized)
	stems = {
		morphtags: [separate_stem(form, morphtags, pos, auxiliary_stems, fossilized) for form in forms]
		for morphtags, forms in inflections.items()
	}
	return stems


def align_ending(ending: str, morphtags: str, pos: str):

	if morphtags == '@base':
		return []

	morphtags = get_morphtag_characters(morphtags)

	aligned_right = []
	for tag, sfx in MORPH_ENDINGS[pos]:
		if not (ending and morphtags):
			break
		if ending.endswith(sfx) and morphtags[-1] == tag:
			tag_chars = [tag] + [NULL] * 999
			aligned_right = list(zip(tag_chars, sfx or '0')) + aligned_right
			ending = ending[:-len(sfx)] if sfx else ending
			del morphtags[-1]

	aligned_left = []
	for tag, sfx in MORPH_ENDINGS[pos]:
		if not (ending and morphtags):
			break
		if ending.startswith(sfx) and morphtags[0] == tag:
			tag_chars = [tag] + [NULL] * 999
			aligned_left += list(zip(tag_chars, sfx or '0'))
			ending = ending[len(sfx):] if sfx else ending
			del morphtags[0]

	length = max(len(morphtags), len(ending))
	tag_chars = morphtags + [NULL] * (length - len(morphtags))
	ending += '0' * (length - len(ending))
	aligned_center = list(zip(tag_chars, ending))

	aligned = aligned_left + aligned_center + aligned_right
	return aligned


def align_stems(stem1: str, stem2: str):

	filled1 = ''
	filled2 = ''

	if stem1 == stem2:
		return stem1, stem2

	# Handle irregular stems, e.g. hyvä : parempi : paras
	for s1, s2 in IRREGULAR:
		n1, n2 = s1.replace('0', ''), s2.replace('0', '')
		if stem1.startswith(n1) and stem2.startswith(n2):
			filled1 += s1
			filled2 += s2
			stem1 = stem1[len(n1):]
			stem2 = stem2[len(n2):]
			break
		if stem1.startswith(n2) and stem2.startswith(n1):
			filled1 += s2
			filled2 += s1
			stem1 = stem1[len(n2):]
			stem2 = stem2[len(n1):]
			break

	while stem1 or stem2:

		c1, c2 = stem1[:1], stem2[:1]

		if not stem2:
			filled1 += c1
			filled2 += NULL
			stem1 = stem1[1:]
			continue
		if not stem1:
			filled1 += NULL
			filled2 += c2
			stem2 = stem2[1:]
			continue
		if c1 == c2:
			filled1 += c1
			filled2 += c2
			stem1 = stem1[1:]
			stem2 = stem2[1:]
			continue

		match = has_mutation(stem1, stem2)
		if match:
			seg1, seg2, seg3, seg4 = match
			stem1 = stem1[len(seg3):]
			stem2 = stem2[len(seg4):]
			filled1 += seg1
			filled2 += seg2
			continue

		if c1 in VOWELS and c2 in VOWELS:
			filled1 += c1
			filled2 += c2
			stem1 = stem1[1:]
			stem2 = stem2[1:]
			continue
		if c1 in VOWELS and c2 == NULL:
			filled1 += c1
			filled2 += c2
			stem1 = stem1[1:]
			stem2 = stem2[1:]
			continue
		if c2 in VOWELS and c1 == NULL:
			filled1 += c1
			filled2 += c2
			stem1 = stem1[1:]
			stem2 = stem2[1:]
			continue
		if c1 in VOWELS:
			filled1 += NULL
			filled2 += c2
			stem2 = stem2[1:]
			continue
		if c2 in VOWELS:
			filled1 += c1
			filled2 += NULL
			stem1 = stem1[1:]
			continue

		print(filled1, '|', stem1)
		print(filled2, '|', stem2)
		input('Warning! Unexpected phonological correspondence encountered! (Press enter to continue)')
		filled1 += c1
		filled2 += c2
		stem1 = stem1[1:]
		stem2 = stem2[1:]

	return filled1, filled2


def expand_stem(inflected_stem: str, short_stem: str, long_stem: str):

	if len(long_stem) == len(short_stem):
		return inflected_stem

	inflected_stem_filled = ''
	while short_stem and long_stem:
		if long_stem[0] == '0' != short_stem[0]:
			inflected_stem_filled += '0'
			long_stem = long_stem[1:]
			continue
		inflected_stem_filled += inflected_stem[0]
		inflected_stem = inflected_stem[1:]
		short_stem = short_stem[1:]
		long_stem = long_stem[1:]

	return inflected_stem_filled + long_stem


def add_stem_epsilons(inflections_stems: dict, pos: str):

	pivot_stem = get_pivot_stem(inflections_stems, pos)

	extended_stems = {
		key: [align_stems(stem1=pivot_stem, stem2=stem) + (ending, fclitic) for stem, ending, fclitic in stems]
		for key, stems in inflections_stems.items()
	}
	longest_stem = str(max((stem for _, stems in extended_stems.items() for stem, _, _, _ in stems), key=len))
	extended_stems = {
		key: [
			(expand_stem(stem2, short_stem=stem1, long_stem=longest_stem), ending, fclitic)
			for stem1, stem2, ending, fclitic in stems
		]
		for key, stems in extended_stems.items()
	}

	# Reattach plural markers to stems for pluralia tantum
	if pos.endswith('-pl'):
		extended_stems = offset_plural(extended_stems)

	return extended_stems


def expand_and_align(inflections_stems: dict, pos: str):

	extended_stems = add_stem_epsilons(inflections_stems, pos)
	lemma_stem, _, _ = extended_stems['@base'][0]
	_, lemma_tail, _ = inflections_stems['@base'][0]
	empty_tail = '0' * len(lemma_tail)
	if lemma_stem not in PL_PRONOUNS and pos.endswith('-pl'):
		lemma_tail = ''

	aligned_forms = {}
	for key, stems in extended_stems.items():
		aligned_forms[key] = [
			as_pairs(lemma_stem + lemma_tail, stem + empty_tail) +
			align_ending(ending, morphtags=key, pos=pos) +
			as_pairs('0' * len(fclitic), fclitic)
			for stem, ending, fclitic in stems
		]

	return aligned_forms


def align_type_51(inflections, pos):

	"""
	Align type 51 nominals and other words internal agreement
	"""

	[lemma] = inflections['@base']

	if has_agreement(lemma):
		split_regex = re.compile('(.+)%(.+)')
	elif pos == 'pronoun' and lemma in {'joku', 'jompikumpi'}:
		split_regex = re.compile('(jo.*)(ku.*)')
	else:
		return

	prefixes = {
		tag: [re.fullmatch(split_regex, form).group(1) for form in forms]
		for tag, forms in inflections.items()
	}
	inflections = {
		tag: [re.fullmatch(split_regex, form).group(2) for form in forms]
		for tag, forms in inflections.items()
	}

	prefixes = align_inflections(prefixes, pos=pos)
	prefixes = equalize_inflections(prefixes)
	aligned = align_inflections(inflections, pos=pos)

	aligned = {
		tag: [join_pairs(pairs1, pairs2, add_separator=(lemma != 'joku'))
		for pairs1, pairs2 in zip(prefixes[tag], aligned[tag])]
		for tag in aligned
	}

	return aligned


def align_inflections(inflections: dict, pos: str):
	stems_and_endings = separate_stems(inflections, pos)
	aligned = expand_and_align(stems_and_endings, pos)
	return aligned


def align_all_inflections(inflections: dict, pos: str):

	aligned = align_type_51(inflections, pos)
	if aligned:
		return aligned

	return align_inflections(inflections, pos)
