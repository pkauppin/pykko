import json
from collections import defaultdict
from scripts.inflection.inflector import inflect
from scripts.file_tools import read_list_tsv, save_txt
from scripts.utils import unpack

adverb_degrees = {
	'hyvin': {'': ['hyvin'], 'comparative': ['paremmin'], 'superlative': ['parhaiten', 'parhaimmin']},
	'usein': {'': ['usein'], 'comparative': ['useammin'], 'superlative': ['useimmin', 'useiten']},
	'kovaa': {'': ['kovaa'], 'comparative': ['kovempaa'], 'superlative': ['kovimpaa', 'koviten']},
	'hiljaa': {'': ['hiljaa'], 'comparative': ['hiljempaa']},
	'lujaa': {'': ['lujaa'], 'comparative': ['lujempaa'], 'superlative': ['lujimpaa', 'lujiten']},
	'oikein': {'': ['oikein'], 'comparative': ['oikeammin'], 'superlative': ['oikeimmin', 'oikeiten']},
	'harvoin': {'': ['harvoin'], 'comparative': ['harvemmin'], 'superlative': ['harvimmin', 'harviten']},
	'harvaan': {'': ['harvaan'], 'comparative': ['harvemmin'], 'superlative': ['harvimmin']},
	'harvasti': {'': ['harvasti'], 'comparative': ['harvemmin'], 'superlative': ['harvimmin']},
	'myöhään': {'': ['myöhään'], 'comparative': ['myöhemmin'], 'superlative': ['myöhimmin']},
	'aikaisin': {'': ['aikaisin'], 'comparative': ['aikaisemmin'], 'superlative': ['aikaisimmin']},
	'varhain': {'': ['varhain'], 'comparative': ['varhemmin'], 'superlative': ['varhimmin', 'varhiten']},
	'paljon': {'': ['paljon'], 'comparative': ['enemmän'], 'superlative': ['eniten']},
	'vähän': {'': ['vähän'], 'comparative': ['vähemmän'], 'superlative': ['vähiten']},
	'pian': {'': ['pian'], 'comparative': ['pikemmin'], 'superlative': ['pikimmin']},
	'kauan': {'': ['kauan'], 'comparative': ['kauemmin'], 'superlative': ['kauimmin', 'kauiten']},
	'mieluusti': {'': ['mieluusti'], 'comparative': ['mieluummin'], 'superlative': ['mieluiten']},
	'äkisti': {'': ['äkisti'], 'comparative': ['äkimmin']},
	'ylös': {'': ['ylös'], 'comparative': ['ylemmäs'], 'superlative': ['ylimmäs']},
	'alas': {'': ['alas'], 'comparative': ['alemmas'], 'superlative': ['alimmas']},
	'kauas': {'': ['kauas'], 'comparative': ['kauemmas'], 'superlative': ['kauimmas']},
	'ahtaalle': {'': ['ahtaalle'], 'comparative': ['ahtaammalle'], 'superlative': ['ahtaimmalle']},
	'syvälle': {'': ['syvälle'], 'comparative': ['syvemmälle'], 'superlative': ['syvimmälle']},
	'kovalle': {'': ['kovalle'], 'comparative': ['kovemmalle'], 'superlative': ['kovimmalle']},
	'ahtaalla': {'': ['ahtaalla'], 'comparative': ['ahtaammalla'], 'superlative': ['ahtaimmalla']},
	'syvällä': {'': ['syvälla'], 'comparative': ['syvemmällä'], 'superlative': ['syvimmällä']},
	'kovalla': {'': ['kovalla'], 'comparative': ['kovemmalla'], 'superlative': ['kovimmalla']},
	'helpolla': {'': ['helpolla'], 'comparative': ['helpommalla'], 'superlative': ['helpoimmalla']},
	'syrjään': {'': ['syrjään'], 'comparative': ['syrjempään', 'syrjemmälle']},
	'kaukana': {'': ['kaukana'], 'comparative': ['kauempana'], 'superlative': ['kauimpana']},
	'kaukaa': {'': ['kaukaa'], 'comparative': ['kauempaa'], 'superlative': ['kauimpaa']},
	'pitkään': {'': ['pitkään'], 'comparative': ['pitempään'], 'superlative': ['pisimpään']},
	'lähelle': {'': ['lähelle'], 'comparative': ['lähemmäs'], 'superlative': ['lähimmäs']},
	'lähellä': {'': ['lähellä'], 'comparative': ['lähempänä'], 'superlative': ['lähimpänä', 'lähinnä']},
}

print('Generating adverbs.json...')

for row in read_list_tsv('lexicon.tsv'):

	# TODO:
	#  Compile list of adverbs ending in -sti that are absent from lexicon.tsv
	#  but whose comparative forms are present.

	_, hidas, _, pos, kotus_classes, gradations, harmonies, vowels, info, _ = row

	if pos != 'adjective':
		continue

	if info == '#' or kotus_classes == '!':
		continue

	forms = defaultdict(list)
	forms.update(
		{'': [], 'comparative': [], 'superlative': []}
	)

	for kotus_class, gradation, harmony, vowel in unpack(kotus_classes, gradations, harmonies, vowels):

		infl = inflect(hidas, pos, kotus_class, gradation)

		if not infl.get('comparative') or not infl.get('superlative'):
			continue

		# hitaa|n, tuhma|n, kiva|n => hitaasti, tuhmasti, kivasti
		for hitaan in infl['sg|gen']:
			hitaa = hitaan[:-1]
			forms[''] += [f'{hitaa}sti']

		# hitaa|mpi, tuhme|mpi, kive|mpi => hitaammin, tuhmemmin, kivemmin
		for hitaampi in infl['comparative']:
			hitaa = hitaampi[:-3]
			forms['comparative'] += [f'{hitaa}mmin']
		for mukavempi in infl.get('comparative|nstd', []):
			mukave = mukavempi[:-3]
			forms['comparative|nstd'] += [f'{mukave}mmin']

		# hita|in, tuhm|in, kivo|in => hitammin/hitaiten, tuhmimmin/tuhmiten, kivoimmin/kivoiten
		for hitain in infl['superlative']:
			hita = hitain[:-2]
			forms['superlative'] += [f'{hita}immin', f'{hita}iten']

		# kauneh|in => kaunehimmin/kaunehiten
		for kaunehin in infl.get('superlative|poet', []):
			kauneh = kaunehin[:-2]
			forms['superlative|poet'] += [f'{kauneh}immin', f'{kauneh}iten']

	for hitaasti in forms['']:
		for key, val in forms.items():
			forms[key] = sorted(set(val), key=lambda x: val.index(x))
		adverb_degrees[hitaasti] = forms


data = '{\n'
for key, val in sorted(adverb_degrees.items()):
	data += f'  "{key}": {json.dumps(val, ensure_ascii=False)},\n'
data += '}'
data = data.replace(',\n}', '\n}')
save_txt(filename='adverbs.json', directory='scripts/inflection', text=data)
