from scripts.file_tools import read_list_tsv, save_txt
from scripts.inflection.inflector import inflect
from scripts.constants import TAB
from scripts.utils import ddict, get_input_and_output_strings, unpack, determine_wordform_harmony, get_lemma_length
from scripts.aligner.aligner import align_all_inflections, equalize_inflections

POS_IN = f'{TAB}^ordinal{TAB}{TAB}{TAB}'
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
} - {'pl|gen|nstd', 'pl|gen|rare'}

NUM = [
	'yhdes',
	'kahdes',
	'kolmas',
	'neljäs',
	'viides',
	'kuudes',
	'seitsemäs',
	'kahdeksas',
	'yhdeksäs',
]

print('Generating ordinals...')

lexc = ''
lexc += f'LEXICON ORDINAL_AUX\n'
for tag in TAGS:
	lexc += f'ORDINAL_{tag} ;\n'
lexc += '\n'

for tag in TAGS:

	lexc += f'LEXICON ORDINAL_{tag}\n'
	lexc += f'ORDINAL_{tag}_base_initial ;\n'
	lexc += f'ORDINAL_{tag}_multiplier_initial ;\n'
	lexc += f'ORDINAL_{tag}_base_final ;\n'
	lexc += f'ORDINAL_{tag}_multiplier_final ;\n'
	lexc += '\n'

	lexc += f'LEXICON ORDINAL_{tag}_base_initial\n'
	for ordinal in NUM:
		[pairs] = FORMS_EQUALIZED[ordinal][tag]
		string1, string2 = get_input_and_output_strings(pairs)
		lexc += f'{string1}|:{string2}0 ORDINAL_{tag} ;\n'
		lexc += f'{string1}|toista|:{string2}0toista0 ORDINAL_{tag} ;\n'
	lexc += '\n'

	lexc += f'LEXICON ORDINAL_{tag}_multiplier_initial\n'
	for ordinal in ['kymmenes', 'sadas', 'tuhannes']:
		[pairs] = FORMS_EQUALIZED[ordinal][tag]
		string1, string2 = get_input_and_output_strings(pairs)
		lexc += f'{string1}|:{string2}0 ORDINAL_{tag} ;\n'
	lexc += '\n'

	lexc += f'LEXICON ORDINAL_{tag}_base_final\n'
	for ordinal in NUM:
		H = determine_wordform_harmony(ordinal)
		cutoff = get_lemma_length(FORMS[ordinal])
		[pairs] = FORMS[ordinal][tag]
		string1, string2 = get_input_and_output_strings(pairs)
		string1 = string1[:cutoff] + POS_IN + string1[cutoff:]
		string2 = string2[:cutoff] + POS_OUT + string2[cutoff:]
		lexc += f'{string1}:{string2} CLITIC_{H} ;\n'
		""""""
		string1, string2 = get_input_and_output_strings(pairs)
		string1 = string1[:cutoff] + '|toista' + POS_IN + string1[cutoff:] + '0000000'
		string2 = string2[:cutoff] + '0000000' + POS_OUT + string2[cutoff:] + '0toista'
		lexc += f'{string1}:{string2} CLITIC_BACK ;\n'
	""""""
	for ordinal in ['ensimmäinen', 'toinen']:
		H = determine_wordform_harmony(ordinal)
		cutoff = get_lemma_length(FORMS[ordinal])
		[pairs] = FORMS[ordinal][tag]
		string1, string2 = get_input_and_output_strings(pairs)
		string1 = string1[:cutoff] + POS_IN + string1[cutoff:]
		string2 = string2[:cutoff] + POS_OUT + string2[cutoff:]
		lexc += f'{string1}:{string2} CLITIC_{H} ;\n'
	lexc += '\n'

	lexc += f'LEXICON ORDINAL_{tag}_multiplier_final\n'
	for ordinal in ['kymmenes', 'sadas', 'tuhannes']:
		H = determine_wordform_harmony(ordinal)
		cutoff = get_lemma_length(FORMS[ordinal])
		[pairs] = FORMS[ordinal][tag]
		string1, string2 = get_input_and_output_strings(pairs)
		string1 = string1[:cutoff] + POS_IN + string1[cutoff:]
		string2 = string2[:cutoff] + POS_OUT + string2[cutoff:]
		lexc += f'{string1}:{string2} CLITIC_{H} ;\n'
	lexc += '\n'

save_txt(filename='lexc-ordinals.txt', directory='scripts/lexc', text=lexc)
