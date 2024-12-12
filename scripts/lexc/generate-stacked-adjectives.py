import re
from collections import defaultdict
from scripts.constants import TAB
from scripts.inflection.inflector import inflect
from scripts.aligner.aligner import align_inflections, equalize_inflections
from scripts.utils import get_input_and_output_strings, determine_wordform_harmony, determine_separator
from scripts.file_tools import read_list_tsv, save_txt

P1 = f'{TAB}^adjective{TAB}{TAB}{TAB}'
P2 = '00000'

COMPARATIVES = defaultdict(list)
SUPERLATIVES = defaultdict(list)

for row in read_list_tsv('aux-adjectives.tsv'):

	_, lemma, _, _, kotus_class, gradation, _, _, _, _ = row

	inflections = inflect(lemma, pos='adjective', kotus_class=kotus_class, gradation=gradation)

	if lemma == 'moni':
		inflections['comparative'] = ['useampi']
		inflections['superlative'] = ['usein']

	inflections_trunc = {'@base': [lemma], 'comparative': inflections['comparative']}
	aligned = align_inflections(inflections_trunc, pos='adjective')
	equalized = equalize_inflections(aligned)
	COMPARATIVES[lemma] += equalized['comparative']

	[genitive] = inflections['sg|gen']

	for comparative in inflections['comparative']:
		comparative_inflections = inflect(comparative, pos='adjective', kotus_class='16', gradation='mp:mm')
		inflections_trunc = {'@base': inflections['sg|gen'], 'comparative': comparative_inflections['sg|gen']}
		aligned = align_inflections(inflections_trunc, pos='adjective')
		equalized = equalize_inflections(aligned)
		COMPARATIVES[genitive] += equalized['comparative']

	for superlative in inflections['superlative']:
		if superlative == 'paras':
			superlative_inflections = inflect(superlative, pos='adjective', kotus_class='41', gradation='rh:r')
		else:
			superlative_inflections = inflect(superlative, pos='adjective', kotus_class='36')
		inflections_trunc = {'@base': inflections['sg|gen'], 'superlative': superlative_inflections['sg|gen']}
		aligned = align_inflections(inflections_trunc, pos='adjective')
		equalized = equalize_inflections(aligned)
		SUPERLATIVES[genitive] += equalized['superlative']

lexc = 'LEXICON STACKED_ADJECTIVES\n'

for row in read_list_tsv('lexicon.tsv'):

	_, lemma, hom, pos, _, _, _, _, info, _ = row

	if 'stacked' not in info:
		continue

	w1, h1, w2 = re.fullmatch('(.+)([-|])(.+)', lemma).groups()
	w2 = w2[:-4]
	harmony = determine_wordform_harmony(w2)

	for comparative in COMPARATIVES[w1]:
		s1, s2 = get_input_and_output_strings(comparative)
		h2 = determine_separator(s2, w2, default='0')
		lexc += f'{s1}{h1}{w2}:{s2}{h2}{w2} INFL_COMPARATIVE_INEN_%s ;\n' % harmony

	for superlative in SUPERLATIVES.get(w1, []):
		s1, s2 = get_input_and_output_strings(superlative)
		h2 = determine_separator(s2, w2, default='0')
		lexc += f'{s1}{h1}{w2}:{s2}{h2}{w2} INFL_SUPERLATIVE_INEN_%s ;\n' % harmony

for degree in 'COMPARATIVE', 'SUPERLATIVE':

	tag = '+' + degree.lower()

	for harmony in 'FRONT', 'BACK':

		lexc += '\n'
		lexc += 'LEXICON INFL_%s_INEN_%s\n' % (degree, harmony)
		inflections = inflect('inen', pos='adjective', kotus_class='38', harmony=harmony.lower())
		aligned = align_inflections(inflections, pos='adjective')
		del aligned['comparative']
		del aligned['superlative']

		for forms in aligned.values():
			for pairs in forms:
				pairs.insert(4, (tag, '0'))
				pairs.insert(4, (P1, P2))

		for key, forms in aligned.items():
			if key.startswith('@'):
				continue
			for form in forms:
				s1, s2 = get_input_and_output_strings(form)
				lexc += f'{s1}:{s2} CLITIC_%s ;\n' % harmony

lexc += '\n'

save_txt('lexc-stacked-adjectives.txt', directory='scripts/lexc', text=lexc)

