from scripts.file_tools import read_list_tsv, save_txt
from scripts.inflection.inflector import inflect
from scripts.constants import TAB
from scripts.utils import ddict, get_input_and_output_strings, get_output_string, unpack, determine_wordform_harmony, get_lemma_length
from scripts.aligner.aligner import align_all_inflections, equalize_inflections

POS_IN = f'{TAB}^numeral{TAB}{TAB}{TAB}'
POS_OUT = '00000'

FORMS = {}
for row in read_list_tsv('aux-numerals.tsv'):
	_, lemma, _, pos, kotus_classes, gradations, harmonies, vowels, _, _ = row
	for kotus_class, gradation, harmony, vowel in unpack(kotus_classes, gradations, harmonies, vowels):
		inflections = inflect(lemma, pos, kotus_class, gradation)
		FORMS[lemma] = ddict(align_all_inflections(inflections, pos='numeral'))

FORMS_EQUALIZED = {
	lemma: ddict(equalize_inflections(inflections)) for lemma, inflections in FORMS.items()
}

TAGS = {
	tag for inflections in FORMS.values() for tag in inflections.keys() if not tag.startswith('@')
} - {'pl|gen|nstd'}

MULTIPLIER_PARTITIVE = {
	'kymmenen': FORMS_EQUALIZED['kymmenen']['sg|par'][0],
	'sata': FORMS_EQUALIZED['sata']['sg|par'][0],
	'tuhat': FORMS_EQUALIZED['tuhat']['sg|par'][0],
}

NUM = [
	'yksi',
	'kaksi',
	'kolme',
	'neljä',
	'viisi',
	'kuusi',
	'seitsemän',
	'kahdeksan',
	'yhdeksän',
]

print('Generating numerals...')

lexc = ''
lexc += f'LEXICON NUMERAL_AUX\n'
for tag in TAGS:
	lexc += f'NUMERAL_{tag} ;\n'
lexc += '\n'

for tag in TAGS:

	lexc += f'LEXICON NUMERAL_{tag}\n'
	lexc += f'NUMERAL_{tag}_2x ;\n'
	lexc += f'NUMERAL_{tag}_+2f ;\n'
	lexc += f'NUMERAL_{tag}_100+ ;\n'
	lexc += f'NUMERAL_{tag}_+1000f ;\n'
	lexc += '\n'

	lexc += f'LEXICON NUMERAL_{tag}_100+\n'
	for numeral in ['sata', 'tuhat']:
		for pairs in FORMS_EQUALIZED[numeral][tag]:
			string1, string2 = get_input_and_output_strings(pairs)
			lexc += f'{string1}|:{string2}0 NUMERAL_{tag}_+2f ;\n'
			lexc += f'{string1}|:{string2}0 NUMERAL_{tag}_2x ;\n'
	for numeral in ['sata', 'kymmenen']:
		for pairs in FORMS_EQUALIZED[numeral][tag]:
			string1, string2 = get_input_and_output_strings(pairs)
			lexc += f'{string1}|:{string2}0 NUMERAL_{tag}_x1000 ;\n'

	lexc += f'LEXICON NUMERAL_{tag}_2x\n'
	for numeral in NUM + ['puoli', 'pari']:
		for pairs in FORMS_EQUALIZED[numeral][tag]:
			string1, string2 = get_input_and_output_strings(pairs)
			lexc += f'{string1}|:{string2}0 NUMERAL_{tag}_x10 ;\n'
			lexc += f'{string1}|:{string2}0 NUMERAL_{tag}_x100 ;\n'
			lexc += f'{string1}|:{string2}0 NUMERAL_{tag}_x1000 ;\n'
	for numeral in NUM + ['puoli']:
		for pairs in FORMS_EQUALIZED[numeral][tag]:
			string1, string2 = get_input_and_output_strings(pairs)
			lexc += f'{string1}|toista|:{string2}0toista0 NUMERAL_{tag}_x1000 ;\n'
	lexc += '\n'

	""""""

	lexc += f'LEXICON NUMERAL_{tag}_x10\n'
	lexc += f'NUMERAL_{tag}_x10+ ;\n'
	lexc += f'NUMERAL_{tag}_x10f ;\n'
	lexc += '\n'

	lexc += f'LEXICON NUMERAL_{tag}_x100\n'
	lexc += f'NUMERAL_{tag}_x100+ ;\n'
	lexc += f'NUMERAL_{tag}_x100f ;\n'
	lexc += '\n'

	lexc += f'LEXICON NUMERAL_{tag}_x1000\n'
	lexc += f'NUMERAL_{tag}_x1000+ ;\n'
	lexc += f'NUMERAL_{tag}_x1000f ;\n'
	lexc += '\n'

	numeral = 'kymmenen'
	if FORMS[numeral][tag]:
		lexc += f'LEXICON NUMERAL_{tag}_x10+\n'
		for pairs in FORMS_EQUALIZED[numeral]['sg|par' if tag == 'sg|nom' else tag]:
			string1 = get_output_string(MULTIPLIER_PARTITIVE[numeral])
			string2 = get_output_string(pairs)
			lexc += f'{string1}|:{string2}0 NUMERAL_{tag}_+2f ;\n'
			lexc += f'{string1}|:{string2}0 NUMERAL_{tag}_2x ;\n'
			lexc += f'{string1}|:{string2}0 NUMERAL_{tag}_x1000 ;\n'
		lexc += '\n'

	numeral = 'sata'
	if FORMS[numeral][tag]:
		lexc += f'LEXICON NUMERAL_{tag}_x100+\n'
		for pairs in FORMS_EQUALIZED[numeral]['sg|par' if tag == 'sg|nom' else tag]:
			string1 = get_output_string(MULTIPLIER_PARTITIVE[numeral])
			string2 = get_output_string(pairs)
			lexc += f'{string1}|:{string2}0 NUMERAL_{tag}_+2f ;\n'
			lexc += f'{string1}|:{string2}0 NUMERAL_{tag}_2x ;\n'
			lexc += f'{string1}|:{string2}0 NUMERAL_{tag}_x1000 ;\n'
		lexc += '\n'

	numeral = 'tuhat'
	if FORMS[numeral][tag]:
		lexc += f'LEXICON NUMERAL_{tag}_x1000+\n'
		for pairs in FORMS_EQUALIZED[numeral]['sg|par' if tag == 'sg|nom' else tag]:
			string1 = get_output_string(MULTIPLIER_PARTITIVE[numeral])
			string2 = get_output_string(pairs)
			lexc += f'{string1}|:{string2}0 NUMERAL_{tag}_+2f ;\n'
			lexc += f'{string1}|:{string2}0 NUMERAL_{tag}_2x ;\n'
			lexc += f'{string1}|:{string2}0 NUMERAL_{tag}_100+ ;\n'
		lexc += '\n'

	""""""

	numeral = 'kymmenen'
	if FORMS[numeral][tag]:
		lexc += f'LEXICON NUMERAL_{tag}_x10f\n'
		harmony = determine_wordform_harmony(numeral)
		cutoff = get_lemma_length(FORMS[numeral])
		for pairs in FORMS[numeral][tag]:
			string1 = get_output_string(MULTIPLIER_PARTITIVE[numeral])
			string2 = string1 if tag == 'sg|nom' else get_output_string(pairs[:cutoff])
			string2 += '0' * (len(string1) - len(string2))
			tags, ending = get_input_and_output_strings(pairs[cutoff:])
			string1 = string1 + POS_IN + tags
			string2 = string2 + POS_OUT + ending
			lexc += f'{string1}:{string2} CLITIC_{harmony} ;\n'
		lexc += '\n'

	numeral = 'sata'
	if FORMS[numeral][tag]:
		lexc += f'LEXICON NUMERAL_{tag}_x100f\n'
		harmony = determine_wordform_harmony(numeral)
		cutoff = get_lemma_length(FORMS[numeral])
		for pairs in FORMS[numeral][tag]:
			string1 = get_output_string(MULTIPLIER_PARTITIVE[numeral])
			string2 = string1 if tag == 'sg|nom' else get_output_string(pairs[:cutoff])
			string2 += '0' * (len(string1) - len(string2))
			tags, ending = get_input_and_output_strings(pairs[cutoff:])
			string1 = string1 + POS_IN + tags
			string2 = string2 + POS_OUT + ending
			lexc += f'{string1}:{string2} CLITIC_{harmony} ;\n'
		lexc += '\n'

	numeral = 'tuhat'
	if FORMS[numeral][tag]:
		lexc += f'LEXICON NUMERAL_{tag}_x1000f\n'
		harmony = determine_wordform_harmony(numeral)
		cutoff = get_lemma_length(FORMS[numeral])
		for pairs in FORMS[numeral][tag]:
			string1 = get_output_string(MULTIPLIER_PARTITIVE[numeral])
			string2 = string1 if tag == 'sg|nom' else get_output_string(pairs[:cutoff])
			string2 += '0' * (len(string1) - len(string2))
			tags, ending = get_input_and_output_strings(pairs[cutoff:])
			string1 = string1 + POS_IN + tags
			string2 = string2 + POS_OUT + ending
			lexc += f'{string1}:{string2} CLITIC_{harmony} ;\n'
		lexc += '\n'

	""""""

	lexc += f'LEXICON NUMERAL_{tag}_+2f\n'
	for numeral in NUM + ['kymmenen', 'sata']:
		harmony = determine_wordform_harmony(numeral)
		cutoff = get_lemma_length(FORMS[numeral])
		for pairs in FORMS[numeral][tag]:
			string1, string2 = get_input_and_output_strings(pairs[:cutoff])
			tags, ending = get_input_and_output_strings(pairs[cutoff:])
			string1 = string1 + POS_IN + tags
			string2 = string2 + POS_OUT + ending
			lexc += f'{string1}:{string2} CLITIC_{harmony} ;\n'
	for numeral in NUM + ['puoli']:
		harmony = determine_wordform_harmony(numeral)
		cutoff = get_lemma_length(FORMS[numeral])
		for pairs in FORMS[numeral][tag]:
			string1, string2 = get_input_and_output_strings(pairs[:cutoff])
			tags, ending = get_input_and_output_strings(pairs[cutoff:])
			string1 = string1 + '|toista' + POS_IN + tags + '0000000'
			string2 = string2 + '0000000' + POS_OUT + ending + '0toista'
			lexc += f'{string1}:{string2} CLITIC_{harmony} ;\n'
	lexc += '\n'

	numeral = 'tuhat'
	if FORMS[numeral][tag]:
		lexc += f'LEXICON NUMERAL_{tag}_+1000f\n'
		harmony = determine_wordform_harmony(numeral)
		cutoff = get_lemma_length(FORMS[numeral])
		for pairs in FORMS[numeral][tag]:
			string1, string2 = get_input_and_output_strings(pairs[:cutoff])
			tags, ending = get_input_and_output_strings(pairs[cutoff:])
			string1 = string1 + POS_IN + tags
			string2 = string2 + POS_OUT + ending
			lexc += f'{string1}:{string2} CLITIC_{harmony} ;\n'
		lexc += '\n'

save_txt(filename='lexc-numerals.txt', directory='scripts/lexc', text=lexc)
