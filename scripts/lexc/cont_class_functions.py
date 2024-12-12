import copy
import re
from scripts.utils import get_wordform, get_tags, determine_wordform_harmony, INTERROGATIVES
from scripts.constants import STYLE_TAGS


def noun_cont_class(_, pairs, morphtag, harmony=None):

	rows = []
	wordform = get_wordform(pairs)
	harmony = determine_wordform_harmony(wordform, harmony)
	tags = get_tags(morphtag)

	# Clitics should be attached to separate stem
	if morphtag == 'sg|nom':
		rows += [(pairs, '#')]

	# Possessive forms (sg|nom, sg|gen, pl|nom)
	# "käte-" + "-nsä"
	elif morphtag == '@stem:possessives':
		pairs_sg_nom = pairs + [('+sg', '0'), ('+nom', '0')]
		pairs_sg_gen = pairs + [('+sg', '0'), ('+gen', '0')]
		pairs_pl_nom = pairs + [('+pl', '0'), ('+nom', '0')]
		rows += [(pairs_sg_nom, 'POSS_%s' % harmony)]
		rows += [(pairs_sg_gen, 'POSS_%s' % harmony)]
		rows += [(pairs_pl_nom, 'POSS_%s' % harmony)]
	elif morphtag == '@stem:possessives:sg:nom':
		pairs += [('+sg', '0'), ('+nom', '0')]
		rows += [(pairs, 'POSS_%s' % harmony)]
	elif morphtag == '@stem:possessives:sg:gen':
		pairs += [('+sg', '0'), ('+gen', '0')]
		rows += [(pairs, 'POSS_%s' % harmony)]
	elif morphtag == '@stem:possessives:pl:nom':
		pairs += [('+pl', '0'), ('+nom', '0')]
		rows += [(pairs, 'POSS_%s' % harmony)]
	elif morphtag == '@stem:possessives:nom':
		pairs_nom = pairs + [('+nom', '0')]
		rows += [(pairs_nom, 'POSS_%s' % harmony)]

	# "BBC" => "BBC:kin"
	elif morphtag == '@stem:clitics':
		pairs += [('+sg', '0'), ('+nom', '0')]
		rows += [(pairs, 'CLITIC_%s_MANDATORY' % harmony)]

	# "koirain", "nallein" -> no possessive suffix
	elif morphtag == 'pl|gen' and re.fullmatch('.+[aäoöuye]in', wordform):
		rows += [(pairs, 'CLITIC_%s' % harmony)]
	elif morphtag == 'gen' and re.fullmatch('.+[aäoöuye]in', wordform):
		rows += [(pairs, 'CLITIC_%s' % harmony)]

	# "käden" -> no possessive suffix
	elif 'sg|gen' in morphtag:
		rows += [(pairs, 'CLITIC_%s' % harmony)]

	# "kätte|n"/"käsie|n" => "kätte-"/"käsie-" + "-nsä"
	elif 'pl|gen' in morphtag:
		pairs_gen = pairs[:-1] + [('+gen', '0')]
		rows += [(pairs_gen, 'POSS_%s' % harmony)]
		rows += [(pairs, 'CLITIC_%s' % harmony)]
	elif tags & {'gen'}:
		pairs_gen = pairs[:-1] + [('+gen', '0')]
		rows += [(pairs_gen, 'POSS_%s' % harmony)]
		rows += [(pairs, 'CLITIC_%s' % harmony)]

	# "käsin" -> no possessive suffix, "käsi" -> no possessive suffix
	elif tags & {'ins', 'nom'}:
		rows += [(pairs, 'CLITIC_%s' % harmony)]

	# "kätee|n" => "kätee-" + "-nsä"
	elif tags & {'ill'}:
		rows += [(pairs[:-1], 'POSS_%s' % harmony)]
		rows += [(pairs, 'CLITIC_%s' % harmony)]

	# "kädellä" + "-än"/"-nsä"
	elif tags & {'ine', 'ade', 'ess', 'abl', 'abe', 'ela'}:
		rows += [(pairs, 'POSS_A_%s' % harmony)]
		rows += [(pairs, 'CLITIC_%s' % harmony)]

	# "kättä" + ""-än"/"-nsä"
	elif tags & {'par'} and not re.fullmatch('.+(aa|ää)', wordform):
		rows += [(pairs, 'POSS_A_%s' % harmony)]
		rows += [(pairs, 'CLITIC_%s' % harmony)]

	# "kädeks|i" => "kädekse-" + "-en"/"-nsä"
	elif tags & {'tra', 'all'}:
		case, _ = pairs[-1]
		pairs_e = pairs[:-1] + [(case, 'e')]
		rows += [(pairs_e, 'POSS_E_%s' % harmony)]
		rows += [(pairs, 'CLITIC_%s' % harmony)]

	# "käsine-" + "-en"/"-nsä"
	elif tags & {'com'}:
		rows += [(pairs, 'POSS_E_%s' % harmony)]

	# "kissaa" + "-nsa"
	elif tags & {'par'}:
		rows += [(pairs, f'CLITIC_POSS_%s' % harmony)]

	elif not morphtag:
		rows += [(pairs, f'CLITIC_POSS_%s' % harmony)]

	# ???
	elif morphtag == 'comparative':
		pairs = pairs[:-3]
		rows += [(pairs, f'COMPARATIVE_MPI_%s' % harmony)]
	# ???
	elif morphtag == 'superlative':
		pairs = pairs[:-2]
		rows += [(pairs, f'SUPERLATIVE_IN_%s' % harmony)]

	# "???"
	else:
		print('Unknown lexicon row case:', wordform, tags)
		input('???')
		rows += [(pairs, f'CLITIC_POSS_%s' % harmony)]

	return copy.deepcopy(rows)


def adjective_cont_class(lemma, pairs, morphtag, harmony=None):

	rows = []
	wordform = get_wordform(pairs)
	harmony = determine_wordform_harmony(wordform, harmony)
	tags = get_tags(morphtag)

	if morphtag == '@stem:clitics':
		return []
	if morphtag == '@stem:possessives':
		return []

	# Inflected forms or "paras"
	if lemma == 'hyvä' and (tags > {'superlative', 'sg'} or tags > {'superlative', 'pl'}):
		rows = [(pairs, f'CLITIC_%s' % harmony)]
	elif lemma == 'hyvä' and wordform == 'paras':
		return []  # ?

	# [suur]immilla|an
	elif lemma.endswith('in') and (wordform.endswith('immilla') or wordform.endswith('immillä')):
		rows += [(pairs, f'POSS_A_%s' % harmony)]
		rows += [(pairs, f'CLITIC_%s' % harmony)]
	# [suur]immille|en
	elif lemma.endswith('in') and wordform.endswith('immille'):
		rows += [(pairs, f'POSS_E_%s' % harmony)]
		rows += [(pairs, f'CLITIC_%s' % harmony)]
	# [suur]immilta|an
	elif lemma.endswith('in') and (wordform.endswith('immilta') or wordform.endswith('immiltä')):
		rows += [(pairs, f'POSS_A_%s' % harmony)]
		rows += [(pairs, f'CLITIC_%s' % harmony)]

	# suure|mpi
	elif morphtag == 'comparative':
		pairs = pairs[:-3]
		rows += [(pairs, f'COMPARATIVE_MPI_%s' % harmony)]
	# suur|in
	elif morphtag == 'superlative':
		pairs = pairs[:-2]
		rows += [(pairs, f'SUPERLATIVE_IN_%s' % harmony)]

	# kaltaise => -ni/-si/-nsa
	elif morphtag == '@stem:possessives':
		rows = [(pairs, f'POSS_%s' % harmony)]

	else:
		rows = [(pairs, f'CLITIC_%s' % harmony)]

	return copy.deepcopy(rows)


def noun_adjective_cont_class(lemma, pairs, morphtag, harmony=None):
	return noun_cont_class(lemma, pairs, morphtag, harmony) + adjective_cont_class(lemma, pairs, morphtag, harmony)


def verb_cont_class(lemma, pairs, morphtag, harmony=None):

	rows = []
	wordform = get_wordform(pairs)
	harmony = determine_wordform_harmony(wordform, harmony)
	tags = get_tags(morphtag)

	if lemma == 'ei' and 'imper' in morphtag:
		return [(pairs, f'CLIT_ÄLÄ')]
	if lemma == 'ei':
		return [(pairs, f'CLIT_EI')]

	if 'conneg' in tags:
		rows += [(pairs, f'KAAN_%s' % harmony)]

	elif morphtag in ['imper|2sg', 'imper|2pl']:
		rows += [(pairs, f'PAS_%s' % harmony)]
		rows += [(pairs, f'KIN')]

	elif 'imper' in tags:
		rows += [(pairs, f'KIN')]

	# sano|ma
	elif 'part_ma' in tags:
		trunc = pairs[:-1]
		rows += [(trunc, f'PARTICIPLE_M|A_%s' % harmony)]

	# sanottav|a
	elif 'part_pres' in tags and 'pass' in tags:
		# sanottavaansa
		rows += [(pairs[:-1], f'PARTICIPLE_M|A_%s' % harmony)]
		# sanottavampi
		rows += [(pairs[:-1], f'PARTICIPLE_V|A_%s' % harmony)]

	# sanov|a
	elif 'part_pres' in tags:
		rows += [(pairs[:-1], f'PARTICIPLE_V|A_%s' % harmony)]
		# sanovinaan
		rows += [(pairs[:-1] + [('+pl', 'i'), ('+ess', 'n'), pairs[-1]], f'POSS_A_%s' % harmony)]
		# sanovansa
		rows += [(pairs, f'POSS_%s' % harmony)]

	# sanon|ut, sanon|eeni
	elif morphtag == 'part_past':
		trunc = pairs[:-2] + [('0', 'e'), ('0', 'e')]
		rows += [(pairs[:-2], f'PARTICIPLE_N|UT_%s' % harmony)]
		rows += [(trunc, f'POSS_%s' % harmony)]

	# sano|ttu
	elif morphtag == 'pass|part_past' and re.fullmatch('.+tt[uy]', wordform):
		trunc = pairs[:-2]
		rows += [(trunc, f'PARTICIPLE_T|TU_%s' % harmony.upper())]
	# juos|tu, kuol|tu
	elif morphtag == 'pass|part_past' and re.fullmatch('.+[lrns]t[uy]', wordform):
		C = re.fullmatch('.+([lrns])t[uy]', wordform).group(1).upper()
		trunc = pairs[:-2]
		rows += [(trunc, f'PARTICIPLE_{C}|TU_%s' % harmony.upper())]
	# juo|tu
	elif morphtag == 'pass|part_past' and re.fullmatch('.+t[uy]', wordform):
		trunc = pairs[:-2]
		rows += [(trunc, f'PARTICIPLE_TU_%s' % harmony)]  # TODO: transitive verbs only?

	# sanottua|ni
	elif morphtag == 'pass|part_past|sg|par':
		rows += [(pairs, f'POSS_A_%s' % harmony)]

	# sano|maton
	elif 'part_maton' in tags:
		trunc = pairs[:-5]
		rows += [(trunc, f'PARTICIPLE_MATON_%s' % harmony)]

	# sanoakse[en]
	elif morphtag == 'inf1|tra':
		trunc = pairs[:-2]
		rows += [(trunc, f'POSS_E_%s' % harmony)]

	# sanoessa
	elif morphtag == 'inf2|ine':
		rows += [(pairs, f'POSS_A_%s' % harmony)]
		rows += [(pairs, f'CLITIC_%s' % harmony)]

	# sano|minen
	elif morphtag == 'inf4':
		trunc = pairs[:-5]
		rows += [(trunc, f'INFINITIVE_MINEN_%s' % harmony)]

	# sanomaisilla|an
	elif morphtag == 'inf5':
		trunc = pairs[:-2]
		rows += [(trunc, f'POSS_A_%s' % harmony)]

	# juoksi|ja, kuvaa|ja
	elif morphtag == 'deriv_agent' and re.fullmatch('.+(ija|ijä)', wordform):
		trunc = pairs[:-2]
		rows += [(trunc, f'DERIV_AGENT_IJA_%s' % harmony)]
	elif morphtag == 'deriv_agent':
		trunc = pairs[:-2]
		rows += [(trunc, f'DERIV_AGENT_AJA_%s' % harmony)]

	# lata|us
	elif morphtag == 'deriv_action':
		ending = re.fullmatch('.+(nti|nta|ntä|na|nä|us|ys|[uyoö])', wordform).group(1).upper()
		trunc = pairs[:-len(ending)]
		rows += [(trunc, f'DERIV_ACTION_{ending}_%s' % harmony)]

	else:
		rows += [(pairs, f'CLITIC_%s' % harmony)]

	return copy.deepcopy(rows)


def adposition_cont_class(lemma, pairs, morphtag, harmony=None):

	rows = []
	wordform = get_wordform(pairs)
	harmony = determine_wordform_harmony(wordform, harmony)

	if morphtag != '@stem:possessives':
		return [(pairs, f'CLITIC_%s' % harmony)]

	# mukaansa, viereensä
	elif re.fullmatch('.*(aa|ee|ii|oo|uu|yy|ää|öö)', wordform):
		rows += [(pairs, f'POSS_%s' % harmony)]

	# nähtensä, tähtensä
	elif lemma in {'nähden', 'tähden'}:
		rows += [(pairs, f'POSS_%s' % harmony)]

	# vuokseen, luokseen
	elif wordform.endswith('e'):
		rows += [(pairs, f'POSS_E_%s' % harmony)]

	# takana, vieressä
	elif wordform.endswith('a') or wordform.endswith('ä'):
		rows += [(pairs, f'POSS_A_%s' % harmony)]

	elif lemma == 'tykö':
		rows += [(pairs, f'POSS_%s' % harmony)]

	# Unknown cases
	else:
		print('???', wordform, morphtag)
		input()

	rows += [(pairs, f'CLITIC_%s' % harmony)]
	return copy.deepcopy(rows)


def adverb_cont_class(_, pairs, morphtag, harmony=None):

	rows = []
	wordform = get_wordform(pairs)
	harmony = determine_wordform_harmony(wordform, harmony)

	# itsekseen, kallelleen / pahoillaan, mielissään
	if morphtag == '@stem:possessives' and wordform.endswith('e'):
		rows += [(pairs, f'POSS_E_%s' % harmony)]
	elif morphtag == '@stem:possessives' and wordform.endswith('a'):
		rows += [(pairs, f'POSS_A_%s' % harmony)]
	elif morphtag == '@stem:possessives' and wordform.endswith('ä'):
		rows += [(pairs, f'POSS_A_%s' % harmony)]
	elif morphtag == '@stem:possessives':
		rows += [(pairs, f'POSS_%s' % harmony)]

	# miksi, mihin => do not take clitic -s
	elif wordform in ['miksi', 'miten', 'milloin', 'mihin']:
		rows += [(pairs, f'CLITIC_%s' % harmony)]

	# missä + -s, kuinka + -s
	elif wordform in INTERROGATIVES:
		rows += [(pairs, f'PAS_%s' % harmony)]
		rows += [(pairs, f'CLITIC_%s' % harmony)]

	# missään, mistään => do not take clitic -ko/-kö
	elif wordform in ['missään', 'mistään']:
		rows += [(pairs, f'HAN_%s' % harmony)]

	# tuskin => do not take clitic -pas, -päs
	elif wordform == 'tuskin':
		rows += [(pairs, f'HANPA')]

	# jotenkin, kuitenkin => only take clitic -han
	elif wordform.endswith('kin'):
		rows += [(pairs, f'HAN_%s' % harmony)]

	# sekaan, mukaan => any clitic
	elif wordform in {
		'sekaan', 'mukaan', 'vikaan', 'hukkaan', 'livohkaan', 'sitkaan', 'synkkaan', 'tarkkaan',
		'tinkaan', 'tiukkaan', 'verkkaan', 'vitkaan', 'sukaan', 'karvaan', 'malkaan', 'jalkaan',
		'ikään', 'mynkään', 'mönkään', 'pitkään', 'selkään', 'mähkään',
	}:
		rows += [(pairs, f'CLITIC_%s' % harmony)]

	# mitenkään, kuitenkaan => do not take any clitics
	elif wordform.endswith('kään') or wordform.endswith('kaan'):
		rows += [(pairs, '#')]

	else:
		rows += [(pairs, f'CLITIC_%s' % harmony)]

	return copy.deepcopy(rows)


def pronoun_cont_class(lemma, pairs, morphtag=None, harmony=None):

	rows = []
	wordform = get_wordform(pairs)
	harmony = determine_wordform_harmony(wordform, harmony)

	if morphtag == '@stem:clitics':
		return []

	# "millekä(s)", "kehenkä(s)"
	if lemma in ['mikä', 'kuka'] and not re.fullmatch('.+[aä]', wordform):
		rows += [(pairs, f'KAS_%s' % harmony)]

	elif lemma in {'kumpi'}:
		rows += [(pairs, f'HAN_%s' % harmony)]
		rows += [(pairs, f'KO_%s' % harmony)]

	# "mikäs", "ketäs", "kelles"f
	if lemma in INTERROGATIVES and not re.fullmatch('.+(ksi|n)', wordform):
		rows += [(pairs, f'PAS_%s' % harmony)]
		rows += [(pairs, f'CLITIC_%s' % harmony)]

	# "mikään" => only take clitic -han/-hän
	elif lemma.endswith('kin') or lemma.endswith('kään') or lemma.endswith('kaan'):
		rows += [(pairs, f'HAN_%s' % harmony)]

	else:
		rows += [(pairs, f'CLITIC_%s' % harmony)]

	return copy.deepcopy(rows)


def ettei_cont_class(_, pairs, morphtag=None, harmony=None):
	return [(pairs, 'CLIT_ETTEI')]


def default_cont_class(_, pairs, morphtag=None, harmony=None):

	wordform = get_wordform(pairs)
	harmony = determine_wordform_harmony(wordform, harmony)

	return [(pairs, f'CLITIC_%s' % harmony)]


def noclit_cont_class(_, pairs, morphtag=None, harmony=None):
	return [(pairs, '#')]


def get_lexicon_rows(function, lemma, pairs, morphtag, harmony):

	# Separate style tags
	style_pairs = []
	tag, char = pairs[-1] if pairs else ('', '')
	if tag in STYLE_TAGS:
		tag, char = pairs.pop()
		style_pairs = [(tag, char)]
		morphtag = morphtag[:-len(tag)]

	# Determine rows and re-attach style tags
	rows = function(lemma, pairs, morphtag, harmony)
	rows = [(pairs + style_pairs, cont_class) for pairs, cont_class in rows]
	return rows


def get_cont_class_function(pos, info=None):

	info = info or ''

	if info == '#':
		return default_cont_class
	if pos == 'noun':
		return noun_cont_class
	if pos == 'noun-pl':
		return noun_cont_class
	if pos == 'proper':
		return noun_cont_class
	if pos == 'proper-pl':
		return noun_cont_class
	if pos == 'ordinal':
		return adjective_cont_class
	if pos == 'numeral':
		return adjective_cont_class
	if pos == 'verb':
		return verb_cont_class
	if pos == 'adposition':
		return adposition_cont_class
	if pos == 'adverb':
		return adverb_cont_class
	if pos == 'conjunction+verb':
		return ettei_cont_class
	if pos == 'adjective' and '+poss' in info:
		return noun_adjective_cont_class
	if pos == 'adjective':
		return adjective_cont_class
	if pos == 'pronoun' and '+poss' in info:
		return noun_cont_class
	if pos == 'noun|adjective':
		return noun_adjective_cont_class
	if pos == 'pronoun':
		return pronoun_cont_class
	if pos == 'pronoun-pl':
		return pronoun_cont_class
	if pos == 'conjunction':
		return noclit_cont_class
	if pos == 'interjection':
		return noclit_cont_class
	if pos == 'none':
		return noclit_cont_class
	if pos == 'adverb+verb':
		return ettei_cont_class
	if pos == 'participle' and '+poss' in info:
		return noun_cont_class
	if pos == 'participle':
		return adjective_cont_class

	input('!!! <= ' + pos)

