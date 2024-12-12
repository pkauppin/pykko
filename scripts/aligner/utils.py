import re
from scripts.constants import ZERO

VOWELS = set('aeiouyäö')
NULL = '0'
PL_PRONOUNS = {'me', 'te', 'he', 'nämä', 'nuo', 'ne'}

IRREGULAR = [
	('hyv',  'par'),
	('käy',  'käv'),
	('ole',  'lie'),
	('kuk',  'ken'),
	('pitk', 'pit0'),
	('pitk', 'pid0'),
	('pitk', 'pis0'),
	('palj', 'en00'),
	('use', 'mon'),
	('ei',  'äl'),
	('ei',  'el'),
]

MUTATIONS = [
	('se0', 'nen'),
	('s00', 'nen'),
	('nt', '0t'),

	('ks', '0s'),
	('ps', '0s'),
	('ts', '0s'),

	('ik', '0j'),

	('p',  'm'),
	('p',  'v'),

	('k',  'k'),
	('k',  'g'),
	('k',  'h'),
	('k',  'v'),
	('k',  'j'),
	('k',  '’'),
	('k',  '0'),

	('t',  'n'),
	('t',  's'),
	('t',  'd'),
	('t',  '0'),
	('d',  's'),

	('s',  '0'),
	('m',  'n'),

	('|', '0'),
]


def has_mutation(stem1, stem2):
	for seg1, seg2 in MUTATIONS:
		seg3, seg4 = seg1.replace(NULL, ''), seg2.replace(NULL, '')
		if stem1.startswith(seg1) and stem2.startswith(seg2):
			return seg1, seg2, seg1, seg2
		if stem1.startswith(seg2) and stem2.startswith(seg1):
			return seg2, seg1, seg2, seg1
		if stem1.startswith(seg3) and stem2.startswith(seg4):
			return seg1, seg2, seg3, seg4
		if stem1.startswith(seg4) and stem2.startswith(seg3):
			return seg2, seg1, seg4, seg3


STYLE_TAGS = [
	('+rare', ''),
	('+dial', ''),
	('+nstd', ''),
	('+arch', ''),
]

MORPH_ENDINGS = {
	'noun': STYLE_TAGS + [
		('+pl+par',	'ita'),
		('+pl+par',	'itä'),
		('+pl+par',	'ja'),
		('+pl+par',	'jä'),
		('+pl+par',	'ia'),
		('+pl+par',	'iä'),
		('+pl+gen',	'itten'),
		('+pl+gen',	'iden'),
		('+pl+gen',	'ien'),
		('+pl+gen',	'jen'),
		('+pl+gen', 'in'),
		('+pl+gen',	'ten'),
		('+pl+nom',	't'),
		('+pl+acc',	't'),
		('+pl+nom',	''),  # "ne"

		('+sg+nom',	''),
		('+sg+gen',	'n'),
		('+sg+par',	'ta'),
		('+sg+par',	'tä'),
		('+sg+par',	'a'),
		('+sg+par',	'ä'),
		('+sg+acc', 't'),
		('+acc',    't'),
		('+gen',    'n'),
		('+ess',	'na'),
		('+ess',	'nä'),
		('+ine',	'ssa'),
		('+ine',	'ssä'),
		#('+ill',	'hin'),
		#('+ill', 	'hon'),
		#('+ill', 	'hun'),
		#('+ill', 	'han'),
		#('+ill',	'an'),
		('+ela',	'sta'),
		('+ela',	'stä'),
		('+ade',	'lla'),
		('+ade',	'llä'),
		('+abl',	'lta'),
		('+abl',	'ltä'),
		('+all',	'lle'),
		('+tra',	'ksi'),
		('+tra',	'kse'),
		('+pl',		'i'),
		('+pl',     'j'),
		('+pl',     't'),
		('+sg',		''),
		('+comparative', 'mpi'),
		('+comparative', 'mma'),
		('+comparative', 'mmä'),
		('+comparative', 'mp'),
		('+comparative', 'mm'),
		# ('+comparative', ''),	 # e.g. "pienempituloinen"?
		('+superlative', 'in'),
		('+superlative', 'imma'),
		('+superlative', 'immä'),
		('+superlative', 'imm'),
		('+superlative', 's'),
	],
	'noun-pl': STYLE_TAGS + [
		('+ess',	'na'),
		('+ess',	'nä'),
		('+ine',	'ssa'),
		('+ine',	'ssä'),
		('+ela',	'sta'),
		('+ela',	'stä'),
		('+ade',	'lla'),
		('+ade',	'llä'),
		('+abl',	'lta'),
		('+abl',	'ltä'),
		('+all',	'lle'),
		('+tra',	'ksi'),
		('+tra',	'kse'),
		('+nom', ''),
		('+gen', 'n'),
		('+acc', 't'),
		('+par', 'ta'),
		('+par', 'tä'),
		('+par', 'a'),
		('+par', 'ä'),
		('', 'i'),
		('', 'j'),
		('', 't'),
		('', 'itte'),
		('', 'ide'),
		('', 'idä'),
		('', 'te'),
		('', 'ie'),
		('', 'je'),
		# ('', 'h'),
	],
	'verb': STYLE_TAGS + [

		('+deriv_action', 'nti'),
		('+deriv_action', 'nta'),
		('+deriv_action', 'ntä'),
		('+deriv_action', 'na'),
		('+deriv_action', 'nä'),
		('+deriv_action', 'us'),
		('+deriv_action', 'ys'),
		('+deriv_action', 'o'),
		('+deriv_action', 'ö'),
		('+deriv_action', 'u'),
		('+deriv_action', 'y'),

		('+deriv_agent', 'ja'),
		('+deriv_agent', 'jä'),

		('+ka', 'ka'),
		('+ka', 'kä'),
		('+ko', 'ko'),
		('+ko', 'kö'),

		('+1sg', 'n'),
		('+2sg', 't'),
		('+1pl', 'mme'),
		('+2pl', 'tten'),
		('+2pl', 'tte'),
		('+3pl', 'vat'),
		('+3pl', 'vät'),

		('+optat', 'lös'),
		('+optat', 'los'),
		('+optat', 'ös'),
		('+optat', 'os'),

		('+imper+2sg', ''),
		('+imper+2pl', 'kaa'),
		('+imper+2pl', 'kää'),
		('+imper+3sg', 'koon'),
		('+imper+3pl', 'koot'),
		('+imper+3sg', 'köön'),
		('+imper+3pl', 'kööt'),
		('+imper', 'koo'),
		('+imper', 'köö'),
		('+imper', 'kaa'),
		('+imper', 'kää'),

		('+2pl', 'a'),  # imperative
		('+2pl', 'ä'),  # imperative

		('+ade', 'lla'),
		('+ade', 'llä'),
		('+ine', 'ssa'),
		('+ine', 'ssä'),
		('+ins', 'n'),
		('+tra', 'kseen'),

		('+inf1', 'ta'),
		('+inf1', 'tä'),
		('+inf1', 'da'),
		('+inf1', 'dä'),
		('+inf1', 'ra'),
		('+inf1', 'rä'),
		('+inf1', 'la'),
		('+inf1', 'lä'),
		('+inf1', 'na'),
		('+inf1', 'nä'),
		('+inf1', 'a'),
		('+inf1', 'ä'),

		('+pass+pres+conneg', 'ta'),
		('+pass+pres+conneg', 'tä'),
		('+pass+pres+conneg', 'da'),
		('+pass+pres+conneg', 'dä'),
		('+pass+pres+conneg', 'ra'),
		('+pass+pres+conneg', 'rä'),
		('+pass+pres+conneg', 'la'),
		('+pass+pres+conneg', 'lä'),
		('+pass+pres+conneg', 'na'),
		('+pass+pres+conneg', 'nä'),

		('+pass+pres', 'taan'),
		('+pass+pres', 'tään'),
		('+pass+pres', 'daan'),
		('+pass+pres', 'dään'),
		('+pass+pres', 'raan'),
		('+pass+pres', 'rään'),
		('+pass+pres', 'laan'),
		('+pass+pres', 'lään'),
		('+pass+pres', 'naan'),
		('+pass+pres', 'nään'),
		('+pass+past', 'ttiin'),
		('+pass+past', 'tiin'),

		('+inf2', 'te'),
		('+inf2', 'de'),
		('+inf2', 'ne'),
		('+inf2', 'le'),
		('+inf2', 're'),
		('+inf2', 'e'),

		('+inf3', 'ma'),
		('+inf3', 'mä'),
		('+part_maton', 'maton'),
		('+part_maton', 'mäton'),
		('+part_ma', 'ma'),
		('+part_va', 'mä'),
		('+part_pres', 'va'),
		('+part_pres', 'vä'),

		('+pass+part_past', 'tu'),
		('+pass+part_past', 'ty'),

		('+part_past', 'nut'),
		('+part_past', 'nyt'),
		('+part_past', 'sut'),
		('+part_past', 'syt'),
		('+part_past', 'lut'),
		('+part_past', 'lyt'),
		('+part_past', 'rut'),
		('+part_past', 'ryt'),

		('+cond', 'isi'),
		('+poten', 'ne'),
		('+poten', 'se'),
		('+poten', 're'),
		('+poten', 'le'),

		('+pass', 'tta'),
		('+pass', 'ttä'),
		('+pass', 'tt'),

		('+conneg', ''),

		('+pass', 'ta'),
		('+pass', 'tä'),

		#('+ela', 'sta'),
		#('+ela', 'stä'),
		#('+ill', 'an'),
		#('+ill', 'än'),
		#('+tra', 'kse'),
		#('+tra', 'ksi'),
		#('+par', 'a'),
		#('+par', 'ä'),
		# ('+tra', 'kseen'),
		# ('+tra', 'kse'),
		# ('+tra', 'ksi'),
		# ('+ins', 'n'),
		# ('+par', 'a'),
		# ('+par', 'ä'),

		('+pres', ''),
	],
	'adverb': STYLE_TAGS + [
		('+superlative', 'immalla'),
		('+superlative', 'immällä'),
		('+superlative', 'immassa'),
		('+superlative', 'immässä'),
		('+superlative', 'immälle'),
		('+superlative', 'immalle'),
		('+superlative', 'impana'),
		('+superlative', 'impänä'),
		('+superlative', 'impaan'),
		('+superlative', 'impään'),
		('+superlative', 'impaa'),
		('+superlative', 'impää'),
		('+superlative', 'immas'),
		('+superlative', 'immäs'),
		('+superlative', 'immin'),
		('+superlative', 'iten'),

		('+comparative', 'mmalla'),
		('+comparative', 'mmällä'),
		('+comparative', 'mmassa'),
		('+comparative', 'mmässä'),
		('+comparative', 'mmälle'),
		('+comparative', 'mmalle'),
		('+comparative', 'mpana'),
		('+comparative', 'mpänä'),
		('+comparative', 'mpaan'),
		('+comparative', 'mpään'),
		('+comparative', 'mpaa'),
		('+comparative', 'mpää'),
		('+comparative', 'mmas'),
		('+comparative', 'mmäs'),
		('+comparative', 'mmin'),
		('+comparative', 'mman'),
		('+comparative', 'mmän'),
	],
	'none': [
	],
}

MORPH_ENDINGS['numeral'] = MORPH_ENDINGS['noun']
MORPH_ENDINGS['adjective'] = MORPH_ENDINGS['noun']
MORPH_ENDINGS['noun|adjective'] = MORPH_ENDINGS['noun']
MORPH_ENDINGS['ordinal'] = MORPH_ENDINGS['noun']
MORPH_ENDINGS['pronoun'] = MORPH_ENDINGS['noun']
MORPH_ENDINGS['pronoun-pl'] = MORPH_ENDINGS['noun-pl']
MORPH_ENDINGS['proper'] = MORPH_ENDINGS['noun']
MORPH_ENDINGS['proper-pl'] = MORPH_ENDINGS['noun-pl']
MORPH_ENDINGS['adposition'] = MORPH_ENDINGS['none']
MORPH_ENDINGS['interjection'] = MORPH_ENDINGS['none']
MORPH_ENDINGS['conjunction'] = MORPH_ENDINGS['none']
MORPH_ENDINGS['conjunction+verb'] = MORPH_ENDINGS['verb']
MORPH_ENDINGS['adverb+verb'] = MORPH_ENDINGS['verb']
MORPH_ENDINGS['participle'] = MORPH_ENDINGS['noun']

FOSSILIZED = {
	('mikä', 'pronoun'): ['kä'],
	('kuka', 'pronoun'): ['ka', 'kä'],
	('mikä|lie', 'pronoun'): ['kä|lie', '|lie', 'kälie', 'lie'],
	('mikään', 'pronoun'): ['kään', 'än'],
	('kukaan', 'pronoun'): ['kaan', 'an', 'kään', 'än'],
	('kumpikaan', 'pronoun'): ['kaan', 'an'],
	('jokin', 'pronoun'): ['kin', 'in'],
	('kukin', 'pronoun'): ['kin', 'in'],
	('kumpainenkin', 'pronoun'): ['kin', 'in'],
	('kumpainenkaan', 'pronoun'): ['kaan', 'an'],
	('kumpikin', 'pronoun'): ['kin', 'in'],
	('mikin', 'pronoun'): ['kin', 'in'],
	('kulloinenkin', 'pronoun'): ['kin'],
	('joltinenkin', 'pronoun'): ['kin'],
	('jommoinenkin', 'pronoun'): ['kin'],
	('kulloinenkin', 'adjective'): ['kin'],
	('joltinenkin', 'adjective'): ['kin'],
	('jommoinenkin', 'adjective'): ['kin'],
	('yksitoista', 'numeral'): ['toista'],
	('kaksitoista', 'numeral'): ['toista'],
	('kolmetoista', 'numeral'): ['toista'],
	('neljätoista', 'numeral'): ['toista'],
	('viisitoista', 'numeral'): ['toista'],
	('kuusitoista', 'numeral'): ['toista'],
	('seitsemäntoista', 'numeral'): ['toista'],
	('kahdeksantoista', 'numeral'): ['toista'],
}


def separate_fossilized_clitic(form, fossilized):

	"""
	Separate fossilized clitics (-kin, -kään/-kaan  etc.)
	"""

	clitic = ''
	for ending in fossilized or []:
		if form.endswith(ending):
			form = form[:-len(ending)]
			clitic = ending
			break
	return form, clitic


def strip_fossilized_clitics(inflections, fossilized):

	"""
	Return copy of given inflections with fossilized clitics stripped,
	"""

	return {
		key: [separate_fossilized_clitic(form, fossilized)[0] for form in forms]
		for key, forms in inflections.items()
	}


def get_fossilized_clitics(baseform, pos):
	baseform = baseform.replace('0', '')
	key = baseform, pos
	return FOSSILIZED.get(key, [])


def get_tags(tag_string):
	return re.findall('[+][^+]+', tag_string)


def print_pairs(pairs):
	return ' '.join(f'{c1}:{c2}' for c1, c2 in pairs)


def as_pairs(filled1, filled2):
	filled1 = re.findall(f'({ZERO}|.)', filled1)
	filled2 = re.findall(f'({ZERO}|.)', filled2)
	return [(c1, c2) for c1, c2 in zip(filled1, filled2)]


def get_auxiliary_stems_noun(inflections):
	auxiliary_stems = []
	auxiliary_stems += [('+sg', form[:-1]) for form in getf(inflections, 'sg|gen')]  # luva|n
	auxiliary_stems += [('+sg', form[:-2]) for form in getf(inflections, 'sg|ess')]  # lupa|na
	auxiliary_stems += [('+pl', form[:-4]) for form in getf(inflections, 'pl|ine')]  # luv|issa
	auxiliary_stems += [('+pl', form[:-3]) for form in getf(inflections, 'pl|ess')]  # lup|ina
	auxiliary_stems += [('+superlative', form[:-2]) for form in getf(inflections, 'superlative')]  # altte|in, altteh|in
	auxiliary_stems += [('@stem:possessives', form[:-2]) for form in getf(inflections, 'sg|ess')]  # lupa|na  # altte|in, altteh|in
	auxiliary_stems += [('@stem:possessives', form) for form in getf(inflections, 'sg|nom')]  # lupa|na  # altte|in, altteh|in
	auxiliary_stems += [('@stem:possessives', form[:-1]) for form in getf(inflections, 'sg|gen')]  # luva|n
	auxiliary_stems += [('+pl', form) for form in getf(inflections, 'pl|nom')]  # ne
	return auxiliary_stems


def get_auxiliary_stems_noun_pl(inflections):
	auxiliary_stems = []
	auxiliary_stems += [('@stem:possessives:nom', form.rstrip('t')) for form in getf(inflections, '@stem:possessives:nom')]  # farkku
	auxiliary_stems += [('', form[:-3]) for form in getf(inflections, 'ess')]  # farkku|ina
	auxiliary_stems += [('', form[:-4]) for form in getf(inflections, 'ine')]  # farku|issa
	auxiliary_stems += [('', form[:-1]) for form in getf(inflections, 'nom')]  # farku|issa
	return auxiliary_stems


def get_auxiliary_stems_verb(inflections):
	auxiliary_stems = []
	auxiliary_stems += [('+pres', form[:-3]) for form in getf(inflections, 'pres|3pl')]   # kaata|vat, hakkaa|vat
	auxiliary_stems += [('+past', form[:-4]) for form in getf(inflections, 'past|3pl')]   # kaato|ivat, hakkas|ivat
	auxiliary_stems += [('+pres', form[:-1]) for form in getf(inflections, 'pres|1sg')]   # kaada|n, hakkaa|n
	auxiliary_stems += [('+past', form[:-2]) for form in getf(inflections, 'past|1sg')]   # kaado|in, hakkas|in
	auxiliary_stems += [('+cond', form[:-3]) for form in getf(inflections, 'cond|3sg')]   # kaata|vat, hakkaa|vat
	auxiliary_stems += [('+poten', form[:-3]) for form in getf(inflections, 'poten|3sg')] # kaata|nee, hakan|nee
	auxiliary_stems += [('+imper+2sg', form) for form in getf(inflections, 'imper|2sg')]  # kaada, hakkaa  # !!!
	auxiliary_stems += [('+imper', form[:-4]) for form in getf(inflections, 'imper|3sg')] # kaata|koon, hakat|koon
	auxiliary_stems += [('+pass', form[:-4]) for form in getf(inflections, 'pass|past')]  # kaadet|tiin, hakat|tiin
	auxiliary_stems += [('', form[:-2]) for form in getf(inflections, 'part_ma')]         # kaata|ma, hakkaa|ma
	auxiliary_stems += [('', form[:-5]) for form in getf(inflections, 'inf3|ine')]        # kaata|massa, hakkaa|massa
	auxiliary_stems += [('', form[:-3]) for form in getf(inflections, 'part_past')]       # kaata|nut, hakan|nut
	auxiliary_stems += [('', form[:-3]) for form in getf(inflections, 'pres|3pl')]        # kaata|vat, hakkaa|vat
	auxiliary_stems += [('', form) for form in getf(inflections, '@base')]                # ei
	return auxiliary_stems


def get_pivot_stem_noun(inflections):
	return max((form for form, _, _ in inflections.get('sg|ess', []) + inflections.get('sg|nom', []) + inflections['@base']), key=len)


def get_pivot_stem_noun_pl(inflections):
	return max((form for form, _, _ in inflections.get('ess', []) + inflections.get('nom', []) + inflections['@base']), key=len)


def get_pivot_stem_verb(inflections):
	return max((form for form, _, _ in inflections.get('pres|3pl') or inflections.get('inf1') or inflections['@base']), key=len)


def get_pivot_stem_adverb(inflections):
	return max((form for form, _, _ in inflections.get('@stem:possessives') or inflections.get('comparative') or inflections['@base']), key=len)


def get_pivot_stem_adposition(inflections):
	return max((form for form, _, _ in inflections.get('@stem:possessives') or inflections['@base']), key=len)


AUXILIARY_STEM_MAPPING = {
	'noun': get_auxiliary_stems_noun,
	'noun-pl': get_auxiliary_stems_noun_pl,
	'proper': get_auxiliary_stems_noun,
	'proper-pl': get_auxiliary_stems_noun_pl,
	'pronoun': get_auxiliary_stems_noun,
	'pronoun-pl': get_auxiliary_stems_noun_pl,
	'adjective': get_auxiliary_stems_noun,
	'ordinal': get_auxiliary_stems_noun,
	'numeral': get_auxiliary_stems_noun,
	'verb': get_auxiliary_stems_verb,
	'noun|adjective': get_auxiliary_stems_noun,
	'participle': get_auxiliary_stems_noun,
}

PIVOT_STEM_MAPPING = {
	'noun': get_pivot_stem_noun,
	'noun-pl': get_pivot_stem_noun_pl,
	'proper': get_pivot_stem_noun,
	'proper-pl': get_pivot_stem_noun_pl,
	'pronoun': get_pivot_stem_noun,
	'pronoun-pl': get_pivot_stem_noun_pl,
	'adjective': get_pivot_stem_noun,
	'ordinal': get_pivot_stem_noun,
	'numeral': get_pivot_stem_noun,
	'verb': get_pivot_stem_verb,
	'adverb': get_pivot_stem_adverb,
	'adposition': get_pivot_stem_adposition,
	'noun|adjective': get_pivot_stem_noun,
	'participle': get_pivot_stem_noun,
}


def get_auxiliary_stems(inflections, pos, fossilized=None):

	"""
	Compile list of auxiliary stems.
	Auxiliary stems can be used to segment inflected forms where segmentation by inflectional ending might go wrong,
	e.g. singular and plural inessives.
	"""

	pos = pos.split('+')[-1]
	if pos not in AUXILIARY_STEM_MAPPING:
		return []

	if fossilized:
		inflections = strip_fossilized_clitics(inflections, fossilized)

	return AUXILIARY_STEM_MAPPING[pos](inflections)


def get_pivot_stem(inflections, pos):

	"""
	Return the most complete stem.
	"""

	pos = pos.split('+')[-1]
	if pos not in PIVOT_STEM_MAPPING:
		form, _, _ = inflections['@base'][0]
		return form

	return PIVOT_STEM_MAPPING[pos](inflections)


def getf(inflections, tag):
	forms = []
	for style in '', '|rare', '|nstd', '|poet', '|arch', '|dial':
		for form in inflections.get(f'{tag}{style}', []):
			forms.append(form)
	return sorted(forms, key=lambda f: -len(f))


def offset_plural(extended_stems):
	return {
		key: [(stem + ending[0:1], ending[1:], fclitic) for stem, ending, fclitic in stems]
		for key, stems in extended_stems.items()
	}


def join_pairs(pairs1, pairs2, add_separator=True):

	def get_separator():

		if not add_separator:
			return []

		l1 = ''.join(c for c, _ in pairs1 if c != '0')
		l2 = ''.join(c for c, _ in pairs2 if c != '0')
		r1 = ''.join(c for _, c in pairs1 if c != '0')
		r2 = ''.join(c for _, c in pairs2 if c != '0')
		c1, c2 = l1[-1], l2[0]
		c3, c4 = r1[-1], r2[0]

		if c2 == '-':
			return []
		if c4 == '-':
			return [('-', '-')]
		s1, s2 = '|', '0'
		if c1 == c2 and c2 in VOWELS:
			s1 = '-'
		if c3 == c4 and c4 in VOWELS:
			s2 = '-'
		return [(s1, s2)]

	separator = get_separator()
	result = fix_compound_separators(pairs1) + separator + fix_compound_separators(pairs2)
	return result


def fix_compound_separators(pairs):
	return [(c1, '0') if c1 == '|' else (c1, c2) for c1, c2 in pairs]


def equalize_inflections(inflections: dict):

	def equalize_form(form):
		return (form[:cutoff] + [('0', c) for _, c in form][cutoff:] + [('0', '0')] * maxlength)[: maxlength]

	[lemma] = inflections['@base']
	cutoff = len(lemma)
	maxlength = max((len(form) for forms in inflections.values() for form in forms))
	return {tag: [equalize_form(form) for form in forms] for tag, forms in inflections.items()}