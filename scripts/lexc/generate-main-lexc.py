from glob import glob
from tqdm import tqdm

from scripts.utils import *
from scripts.constants import *
from scripts.lexc.utils import *
from scripts.lexc.cont_class_functions import get_cont_class_function, get_lexicon_rows
from scripts.aligner.aligner import align_all_inflections, align_ending
from scripts.file_tools import read_txt, read_tsv, save_txt, scripts_path, read_list
from scripts.inflection.inflector import inflect
from scripts.inflection.inflect_type_51 import inflect_51

PATTERNS = {}
INFLECTION_SUBLEXICA = {}
COUNTERS = defaultdict(int)
POS_SUBLEXICA = defaultdict(str)

CUTOFFS = set()

MULTICHAR_SYMBOLS = {
	TAB,
	"Lexicon",
	"Lexicon|Num",
	"Lexicon|Pfx",
	"Lexicon|Hyp",
	"Lexicon|Hyp+Pfx",
	"Lexicon|Gfx",
	"Lexicon|Gfx+Pfx",
	"Guesser|Any",
	"Guesser|Cap",
	"⁅HYPHEN⁆",
	"⁅BOUNDARY⁆",
}

UPPERCASE_REGEX = '[' + '|'.join(f'"{c}"' for c in ALPHA_UPPER_EXTENDED) + ']'
PSEUDO_PREFIXES = sorted(set(read_list('fi-prefixes-guesser.txt', directory='lists')))
PSEUDO_PREFIX_REGEX = '|'.join('{%s}' % pfx for pfx in PSEUDO_PREFIXES)

ROOT = f"""
!!
!! General guesser patterns
<[ "Guesser|Cap":0 "{TAB}":0 {UPPERCASE_REGEX} ?* ]> GUESSER_CAP_PROPER ;
<[ "Guesser|Cap":0 "{TAB}":0 {UPPERCASE_REGEX} ?* ]> GUESSER_CAP_PROPER-PL ;
"""
for POS in POS_TAGS:
	if '+' in POS:
		continue
	ROOT += f'<[ "Guesser|Any":0 "{TAB}":0 ?+ ]> GUESSER_ANY_{POS.upper()} ;\n'
	ROOT += f'<[ "Guesser|Any":0 "{TAB}":0 ?+ ["a"|"e"|"i"|"o"|"u"|"l"|"r"] ]> GUESSER_VA_{POS.upper()} ;\n'
	ROOT += f'<[ "Guesser|Any":0 "{TAB}":0 ?+ ["ä"|"e"|"i"|"ö"|"y"|"l"|"r"] ]> GUESSER_VÄ_{POS.upper()} ;\n'

ROOT += f"""!!
!! Compounding and prefixing
<[ "Lexicon|Pfx":0 "{TAB}":0 ]> NOUN_PFX ;
<[ "Lexicon|Pfx":0 "{TAB}":0 ]> VERB_PFX ;
<[ "Lexicon|Pfx":0 "{TAB}":0 ]> ADVERB_PFX ;
<[ "Lexicon|Pfx":0 "{TAB}":0 ]> ADJECTIVE_PFX ;
!!
!! Special compounding and prefixing
<[ "Lexicon|Hyp":0 "{TAB}":0 ?* "⁅HYPHEN⁆":"-" ]::2.0 > NOUN ;
<[ "Lexicon|Hyp":0 "{TAB}":0 ?* "⁅HYPHEN⁆":"-" ]::2.0 > NOUN-PL ;
<[ "Lexicon|Hyp":0 "{TAB}":0 ?* "⁅HYPHEN⁆":"-" ]::2.0 > PROPER ;
<[ "Lexicon|Hyp":0 "{TAB}":0 ?* "⁅HYPHEN⁆":"-" ]::2.0 > PROPER-PL ;
<[ "Lexicon|Hyp":0 "{TAB}":0 ?* "⁅HYPHEN⁆":"-" ]::2.0 > ADJECTIVE ;
<[ "Lexicon|Hyp":0 "{TAB}":0 ?* "⁅HYPHEN⁆":"-" ]::2.0 > ADVERB ;
<[ "Lexicon|Hyp+Pfx":0 "{TAB}":0 ?* "⁅HYPHEN⁆":"-" ]::3.0 > NOUN_PFX ;
<[ "Lexicon|Gfx":0 "{TAB}":0 ?+ [{PSEUDO_PREFIX_REGEX}] "|":0 ]::5.0 > NOUN ;
<[ "Lexicon|Gfx":0 "{TAB}":0 ?+ [{PSEUDO_PREFIX_REGEX}] "|":0 ]::5.0 > NOUN-PL ;
<[ "Lexicon|Gfx+Pfx":0 "{TAB}":0 ?+ [{PSEUDO_PREFIX_REGEX}] "|":0 ]::5.0 > NOUN_PFX ;
!!
!! Generated numerals & ordinals
<[ "Lexicon|Num":0 "{TAB}":0 ]> NUMERAL_AUX ;
<[ "Lexicon|Num":0 "{TAB}":0 ]> ORDINAL_AUX ;
!!
!! Plain parts-of-speech w/o compounding
<[ "Lexicon":0 "{TAB}":0 ]> STACKED_ADJECTIVES ;
<[ "Lexicon":0 "{TAB}":0 ]> NOUN_NOPFX ;
<[ "Lexicon":0 "{TAB}":0 ]> NOUN-PL_NOPFX ;
<[ "Lexicon":0 "{TAB}":0 ]> ADJECTIVE_NOPFX ;
<[ "Lexicon":0 "{TAB}":0 ]> ADVERB_NOPFX ;
<[ "Lexicon":0 "{TAB}":0 ]> VERB_NOPFX ;
<[ "Lexicon":0 "{TAB}":0 ? "{TAB}":0 "^none":0 "{TAB}":0 "{TAB}":0 "{TAB}":0 ]::2.0 > # ;
"""
for POS in POS_TAGS:
	ROOT += f'<[ "Lexicon":0 "{TAB}":0 ]> {POS.upper()} ;\n'
	MULTICHAR_SYMBOLS.add(f'^{POS}')


def name_and_add_sublexicon(lexicon, lemma=None, pos=None, auxname=None):

	if auxname:
		if INFLECTION_SUBLEXICA.get(lexicon):
			print(f'Warning! Cannot add aux lexicon "{auxname}" – identical lexicon exists already!')
			input('(Press any key to continue)')
			lexicon += f'!! {auxname}\n'
		INFLECTION_SUBLEXICA[lexicon] = auxname

	if INFLECTION_SUBLEXICA.get(lexicon):
		return INFLECTION_SUBLEXICA[lexicon]

	COUNTERS[pos] += 1
	number = str(COUNTERS[pos]).zfill(6)
	name = f'{number}_{lemma}_{pos}'.upper()\
		.replace(ZERO.upper(), '§ZERO§') \
		.replace(':', '§COLON§').replace('!', '§EXCLAMATION§')\
		.replace('<', '§LT§').replace('>', '§GT§').replace(' ', '§SPACE§')

	INFLECTION_SUBLEXICA[lexicon] = name
	return name


def get_wordform_head(aligned_inflections: dict):

	"""
	Return the longest leftmost shared string.
	"""

	def match(pairs1, pairs2):
		if not (pairs1 and pairs2):
			return False
		c1, c2 = pairs1[0]
		c3, c4 = pairs2[0]
		return c1 == c2 == c3 == c4

	all_forms = [tuple(form) for forms in aligned_inflections.values() for form in forms]

	stem, form0 = [],  all_forms[0]
	while all(match(form, form0) for form in all_forms):
		stem.append(form0[0][0])
		all_forms = [form[1:] for form in all_forms]
		form0 = all_forms[0]

	return ''.join(stem), len(stem)


def rework_lexicon_rows(lexicon_rows, auxtags, lemma_end, pos):
	auxtags = auxtags.strip('+').replace('+', '|')
	for pairs, cont_class in sorted(lexicon_rows):
		ending = get_output_string(pairs[:lemma_end])
		pairs[0:] = align_ending(ending, auxtags, pos) + pairs[lemma_end:]


def inflections2lexicon(inflections: dict, pos: str, harmony=None, separator=None, auxtags=None, info=''):

	[lemma] = inflections['@base']

	inflections_aligned = align_all_inflections(inflections, pos=pos)
	[lemma_aligned] = inflections_aligned.pop('@base')
	lemma_end = len(lemma_aligned)

	function = get_cont_class_function(pos, info)
	head, cutoff = get_wordform_head(inflections_aligned)
	inverse_cutoff = (cutoff - len(lemma.replace(ZERO, '0')))
	CUTOFFS.add(inverse_cutoff)

	lexicon_rows = []
	for tag, forms in inflections_aligned.items():
		for pairs in forms:
			lexicon_rows += get_lexicon_rows(function, lemma, pairs.copy(), morphtag=tag, harmony=harmony)

	# Auxtags => change handling
	if auxtags is not None:
		head, cutoff = '', 0
		rework_lexicon_rows(lexicon_rows, auxtags, lemma_end, pos)

	sep1 = ''.join(separator or [])
	sep2 = '0' * len(separator or [])

	lexicon = ''
	for pairs, cont_class in sorted(lexicon_rows):
		MULTICHAR_SYMBOLS.update(symbol for symbol, _ in pairs if len(symbol) > 1)
		seg1, seg2 = pairs[cutoff:lemma_end], pairs[lemma_end:]
		seg1p1, seg1p2 = get_input_and_output_strings(seg1)
		seg2p1, seg2p2 = get_input_and_output_strings(seg2)
		string1 = escape_lexc_string(f'{seg1p1}{sep1}{seg2p1}')
		string2 = escape_lexc_string(f'{seg1p2}{sep2}{seg2p2}')
		lexicon += f'{string1}:{string2} {cont_class} ; \n'
	return head, inverse_cutoff, lexicon


def add_word(lemma, pos, homonym=None, infl=None, style=None, inflections=None, regex_pfx=None, auxtags=None, auxname=None, weight=0.0):

	# Style tags
	if style:
		style = f'⟨{style}⟩'
		MULTICHAR_SYMBOLS.add(style)

	# Temporarily replace literal zeros in lemma
	lemma = lemma.replace('0', ZERO)

	infl = infl or NoneInfl
	compound_parts, lemma = get_compound_parts(lemma, irregular=bool(inflections))
	agreement = has_agreement(lemma)

	fharm = determine_wordform_harmony(lemma)
	pattern_key = lemma[-6:], homonym, pos, fharm, style, str(infl)  # Is style redundant?

	if PATTERNS.get(pattern_key) and not (inflections or auxname or agreement):
		head, inverse_cutoff, lexicon_name = PATTERNS[pattern_key]
		head = lemma[:inverse_cutoff] if inverse_cutoff else lemma

	else:
		if not inflections:
			inflections = \
				inflect_51(lemma, pos, infl.infl_class, infl.gradation, infl.harmony) if agreement else \
				inflect(lemma, pos, infl.infl_class, infl.gradation, infl.harmony, infl.chroneme, infl.info)

		if regex_pfx and 'deriv_action' in inflections:
			del inflections['deriv_action']

		separator = get_field_separators(pos, homonym=homonym, style=style, auxname=auxname)
		head, inverse_cutoff, lexicon = inflections2lexicon(inflections, pos=pos, separator=separator, harmony=infl.harmony, auxtags=auxtags, info=infl.info)
		lexicon_name = name_and_add_sublexicon(lexicon, lemma=lemma, pos=pos, auxname=auxname)

	if auxname:
		return

	pos_sublexicon_name = get_pos_sublexicon_name(pos=pos, regex_name=regex_pfx, lemma=lemma, info=infl.info)
	head1, head2 = get_lemma_head_strings(head, compound_parts)
	head1, head2 = escape_lexc_string(head1), escape_lexc_string(head2)
	POS_SUBLEXICA[pos_sublexicon_name] += f'{head1}:{head2} {lexicon_name} "weight: {weight}" ;\n'

	if regex_pfx:
		return

	# Add all-lowercase versions of proper names etc.
	if lemma.lower() != lemma and not regex_pfx:
		POS_SUBLEXICA[pos_sublexicon_name] += f'{head1}:{head2.lower()} {lexicon_name} "weight: {weight + 1.0}" ;\n'

	PATTERNS[pattern_key] = head, inverse_cutoff, lexicon_name


def add_auxiliary_lexica():

	"""
	These are used for verb participles, compared forms of adjectives etc.
	"""

	from scripts.lexc.auxiliary_lexica import auxiliary_forms
	for ending, pos, infl_class, gradation, harmony, tag, auxname in auxiliary_forms:
		infl = InflectionProperties(infl_class, gradation, harmony)
		add_word(ending, pos, infl=infl, auxtags=tag, auxname=auxname)


def add_irregular_forms():

	"""
	Individual irregular word forms w/ their analyses.
	"""

	for key, inflections in read_irregular().items():
		lemma, pos, style = key
		inflections['@base'] = [lemma]
		add_word(lemma, pos=pos, style=style, inflections=inflections)


def read_words():

	print('Reading words lists...')

	# Read basic word lists
	filenames = [
		'lexicon.tsv',
		'foreign.tsv',
		'guesser.tsv',
		'compound-only.tsv',
		'participles.tsv',
	]
	filenames += glob(os.path.join(scripts_path, '..', 'lists', 'gaz-*.tsv'))
	rows = [row for filename in filenames for row in read_tsv(filename, directory='lists')]

	for row in tqdm(rows):
		regex_pfx, lemma, homonym, pos, infl_classes, gradations, harmonies, chronemes, info, weight = row
		for infl_class, gradation, harmony, chroneme in unpack(infl_classes, gradations, harmonies, chronemes):
			infl = InflectionProperties(infl_class, gradation, harmony, chroneme, info)
			style = '|'.join(sorted(re.findall(f'{STYLE_TAG_REGEX}', info)))
			add_word(lemma, homonym=homonym, pos=pos, infl=infl, style=style, regex_pfx=regex_pfx, weight=float(weight or '0'))

	# Add auxuliary lexica
	add_auxiliary_lexica()

	# Add irregular wordforms
	add_irregular_forms()

	print('Done.')


def generate_lexc():

	# Write LexC
	lexc = ''
	lexc += 'Multichar_Symbols\n'
	for char in sorted(MULTICHAR_SYMBOLS):
		lexc += char + '\n'
	lexc += '\n'

	# Root
	lexc += 'LEXICON Root'
	lexc += ROOT
	lexc += '\n'

	# Prefixing and compounding
	lexc += 'LEXICON NOUN_PFX\n'
	lexc += read_txt('lexc-pfx_noun.txt', directory='scripts/lexc')
	lexc += '\n'
	lexc += 'LEXICON NOUN_PFX2\n'
	lexc += '|:0 NOUN_PFX ;\n'
	lexc += '-:- NOUN_PFX ;\n'
	lexc += '⁅BOUNDARY⁆:0 NOUN ;\n'
	lexc += '⁅BOUNDARY⁆:0 NOUN-PL ;\n'
	lexc += '⁅BOUNDARY⁆:0 COMPOUND_ONLY ;\n'
	lexc += '⁅HYPHEN⁆:- NOUN ;\n'
	lexc += '⁅HYPHEN⁆:- NOUN-PL ;\n'
	lexc += '\n'
	lexc += read_txt('lexc-pfx_misc.txt', directory='scripts/lexc')
	lexc += '\n'

	# Parts-of-speech sublexica
	for sublexicon_name, lexicon in POS_SUBLEXICA.items():
		lexc += f'LEXICON {sublexicon_name}\n'
		lexc += lexicon
		lexc += '\n'

	# Inflection class sublexica
	sublexicon_names = sorted((name, lexicon) for lexicon, name in INFLECTION_SUBLEXICA.items())
	for sublexicon_name, lexicon in sublexicon_names:
		lexc += f'LEXICON {sublexicon_name}\n'
		lexc += lexicon
		lexc += '\n'

	# Cardinal and ordinal number generatorss
	lexc += read_txt('lexc-numerals.txt', directory='scripts/lexc')
	lexc += read_txt('lexc-ordinals.txt', directory='scripts/lexc')

	# Stacked compound adjectives where the former part can have degrees of comparison, e.g.
	# "suuri|tuloinen" => "suurempi|tuloinen", "hyväntuoksuinen" => "parhaan|tuoksuinen"
	lexc += read_txt('lexc-stacked-adjectives.txt', directory='scripts/lexc')

	# Clitics
	lexc += read_txt('lexc-clitics.txt', directory='scripts/lexc')

	# Restore + escape literal zeros
	lexc = lexc.replace(ZERO, '%0')

	return lexc


def main():
	read_words()
	lexc = generate_lexc()
	save_txt(filename='fi.lexc', directory='.', text=lexc)

	# print(CUTOFFS)


main()