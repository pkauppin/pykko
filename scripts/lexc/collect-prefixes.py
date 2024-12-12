import re
from scripts.inflection.inflector import inflect
from scripts.inflection.inflect_type_51 import inflect_51
from scripts.inflection.utils import plural2singular
from scripts.utils import unpack
from scripts.file_tools import read_list_tsv, save_txt, read_list

DUBIOUS = {
	'aa', 'as', 'bi', 'di', 'do', 'ee', 'es', 'fa', 'fu', 'id', 'ii', 'in', 'la', 'mi', 'on', 'oo', 're', 'so', 'ti',
	'to', 'up', 'uu', 'vu', 'yy', 'ää', 'öö', 'air', 'ais', 'boy', 'cee', 'ces', 'cha', 'chi', 'cow', 'cup', 'des',
	'dis', 'dur', 'eis', 'fan', 'fes', 'fis', 'fär', 'ges', 'gis', 'hip', 'hiv', 'hop', 'how', 'ian', 'jet', 'jin',
	'kik', 'käs', 'lei', 'leu', 'lev', 'lux', 'mis', 'mys', 'net', 'new', 'non', 'off', 'out', 'pan', 'par', 'pre',
	'pro', 'rai', 'sen', 'tag', 'tec', 'tic', 'vip', 'yht', 'yin', 'zen', 'lais', 'vent', 'kalais', 'salais', 'jollais',
	'kuplais', 'mahlais', 'millais', 'sellais', 'suklais', 'suolais', 'tällais', 'jumalais', 'kuoppais', 'tuollais',
	'piikkis', 'karvais',
}

RARE = {
	# TODO: compile complete list of these cases
	'pappi', 'syksy', 'suuri', 'pieni', 'anti',
}


def get_weight(pfx):

	"""
	Assign higher weights to words that have specific prefix forms, e.g.
	- *pappi vs. pappis-
	- *syksy vs. syys-
	"""

	if pfx in RARE:
		return 2.0
	return 1.0


def prefix_form_gen(genitive):

	"""
	"Saharan", "Itä-Euroopan", "Uuden-Guinean" => "saharan-", "itä|euroopan-", "uuden|guinean-"
	"""

	pfx = genitive.lower()
	pfx = re.sub('([aeiouyäö])-\1', '\g<1> | \g<1>', pfx)
	pfx = pfx.replace('-', '|').replace(' | ', '-')
	pfx = pfx.replace('0', '')

	return pfx


def prefix_form(lemma, kotus_class):

	"""
	"nainen" => "nais-"
	"""

	pfx = lemma.lower()
	pfx = pfx.replace('0', '')
	pfx = pfx.replace('%', '|')
	if kotus_class == '38':
		return pfx[:-3] + 's'
	return pfx


def collect_noun_prefixes():

	"""
	Read master.tsv and fi-prefixes.txt
	Return list of forms to use as prefixes in noun compounds
	"""

	prefixes = set(read_list('fi-prefixes_N.txt', directory='lists'))

	for row in \
		read_list_tsv('lexicon.tsv'):
		# read_list_tsv('lexicon.tsv') + \
		# read_list_tsv('gaz-loc-geo-regions.tsv') + \
		# read_list_tsv('gaz-loc-geo-islands.tsv'):

		regex, lemma, homonym, pos, classes, gradations, harmonies, vowels, info, _ = row

		if regex:
			continue
		if ' ' in lemma:
			continue
		if '%' in lemma and pos not in ['proper', 'proper-pl']:
			continue

		# Remove everything followed by a hyphen, then split at morpheme boundaries
		if pos in ['proper', 'proper-pl']:
			segments = []
			word = lemma
		else:
			segments = lemma.split('-').pop().split('|')
			word = segments.pop()

		if len(word) <= 2 and word != 'yö':
			continue

		if re.findall('foreign|abbr|unit|symbol|non-compounding', info):
			continue

		if not re.fullmatch('.*[a-zåäöüé]', word):
			continue

		if 'B' in classes or classes == 'XX':
			continue

		# Collect prefixes from given word
		if pos in ['noun', 'noun-pl']:
			for segment in segments:
				if len(segment) <= 2:
					continue
				if not re.fullmatch('[a-zåäöüé].*[a-zåäöüé]', segment):
					continue
				prefixes.add(segment)

		words = [word]
		if re.fullmatch('[a-zåäö]+[|-][a-zäö]+', lemma) and pos in ['noun', 'noun-pl']:
			words.append(lemma)

		for kotus_class, gradation, harmony, vowel in unpack(classes, gradations, harmonies, vowels, ignore_styles=True):

			if not kotus_class:
				continue

			for word in words:

				if '%' in word:
					infl = inflect_51(word, pos, kotus_class, gradation)
				else:
					infl = inflect(word, pos, kotus_class, gradation, harmony, vowel)

				if pos == 'verb' and 'inf4' in infl:

					# Add prefix forms of 4th infinitive
					# e.g. "rakentaa" : "rakentaminen" => "rakentamis-"
					prefixes.update(prefix_form(inf4, kotus_class='38') for inf4 in infl['inf4'])

				elif pos == 'proper-pl':

					# Add genitive forms of proper names, e.g. "isojen|antillien-"
					forms = infl['gen']
					prefixes.update(prefix_form_gen(form) for form in forms)

				elif pos == 'proper':

					# Add genitive forms of proper names, e.g. "saharan-", "itä|euroopan-", "uuden|guinean-"
					forms = infl['sg|gen']
					prefixes.update(prefix_form_gen(form) for form in forms)

				elif pos == 'noun-pl':

					# Pluralia tantum: "sakset" => add "saksi-", "olympialaiset" => add "olympialais-"
					singular = plural2singular(word, kotus_class=kotus_class, gradation=gradation)
					pfx = prefix_form(singular, kotus_class=kotus_class)
					prefixes.add(pfx)

					# TODO
					# # Add genitive forms
					# forms = infl['gen'] + infl.get('gen|rare', [])
					# prefixes.update(prefix_form(form, kotus_class='') for form in forms)

				elif pos == 'noun':

					# Add prefix form of given noun
					pfx = prefix_form(word, kotus_class=kotus_class)
					prefixes.add(pfx)

					# Add genitive forms
					forms = infl['sg|gen'] + infl.get('sg|gen|rare', [])
					prefixes.update(prefix_form(form, kotus_class='') for form in forms)

				elif pos == 'adjective' and kotus_class == '38' and re.fullmatch('.+l[aä]inen', word):

					# Adjective like "suomalainen" => add "suomalais-"
					# NOTE: Not all words ending in -(i)nen yield a valid prefix, so limit to -lainen/-läinen for now

					pfx = prefix_form(word, kotus_class=kotus_class)
					prefixes.add(pfx)

				# TODO: Add non-compounded adjectives?

	return sorted(prefixes - DUBIOUS)


def main():

	# Nouns
	print('Extracting noun prefixes...')
	prefixes = collect_noun_prefixes()
	print(len(prefixes), 'prefixes extracted.')

	lexicon = ''
	lexicon += ''.join(
		f'{pfx}:{pfx.replace("|", "0")} NOUN_PFX2 "weight: {get_weight(pfx)}" ;\n'
		for pfx in prefixes
	)
	save_txt(filename='lexc-pfx_noun.txt', directory='scripts/lexc', text=lexicon)

	# Adjectives, adverbs, verbs
	lexc = ''
	for POS, KEY in [
		('ADJECTIVE', 'A'),
		('ADVERB', 'A'),
		('VERB', 'V'),
	]:
		lexc += f'LEXICON {POS}_PFX\n'
		for pfx in read_list(f'fi-prefixes_{KEY}.txt', directory='lists'):
			lexc += f'{pfx}|:{pfx}0 {POS} "weight: 1.0" ;\n'
		lexc += '\n'
	save_txt(filename='lexc-pfx_misc.txt', directory='scripts/lexc', text=lexc)


main()
