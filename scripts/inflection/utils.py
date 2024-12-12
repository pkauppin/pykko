import copy
import re
import unicodedata

C = '[^aeiouyäöü]'
V = '[aeiouyäöü]'
VV = '([aeiouyäö]|[aeiou][ui]|[äeiöy][yi]|ie|uo|yö|aa|ee|ii|oo|uu|yy|ää|öö)'

HARMONY_MAPPING = {
	'back': ('a', 'o', 'u', 'aa', 'oo', 'uu'),
	'front': ('ä', 'ö', 'y', 'ää', 'öö', 'yy'),
	'BACK': ('a', 'o', 'u', 'aa', 'oo', 'uu'),
	'FRONT': ('ä', 'ö', 'y', 'ää', 'öö', 'yy'),
}


def unaccent(s: str):
	return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def grad_strong(s, gradtype=None):

	if not gradtype:
		return s

	strong, weak = gradtype.split(':')

	if not re.fullmatch(f'.+{V}', s):
		print(f'Warning! Stem "{s}" (gradation type {weak} => {strong}) does not end in vowel!"')
		input()
		return s

	s = 'a' + s
	s = re.sub(f'(?<=.)({weak})(?={V}$)', strong, s)
	return s[1:]


def grad_weak(s, gradtype=None):

	if not gradtype:
		return s

	strong, weak = gradtype.split(':')

	if not re.fullmatch(f'.+{V}', s):
		print(f'Warning! Stem "{s}" (gradation type {strong} => {weak}) does not end in vowel!"')
		input()
		return s

	# "vaa'an", "rei'issä", "ruo'ot", "nau'un"
	if strong == 'k' and weak == '' and re.fullmatch(f'(.*{V})?(aka|äkä|iki|oko|ökö|eke|uku|yky)', s):
		weak = "’"

	s = 'a' + s
	s = re.sub(f'(.+)?{strong}({V})', f'\g<1>{weak}\g<2>', s)
	return s[1:]


def determine_harmony(s, kotus_class=None, allow_multiple=False):

	s = s.split('-').pop()
	s = s.split('|').pop()
	s = s.split(' ').pop()

	if s.endswith('ainen'):
		return 'back'
	if s.endswith('äinen'):
		return 'front'

	if kotus_class == '18B':
		c = s[-1].lower()
		if c in set('bcdefgjilmnprstvwxyzäöü'):
			return 'front'
		return 'back'

	if re.fullmatch('.*yy[^aou2368]*', s):
		return 'front'

	if re.fullmatch('.*[aou].*y[^aou]*', s) and allow_multiple:
		return 'front|back'

	for c in reversed(s.lower()):
		if c in set('aouáóúàòùâôû'):
			return 'back'
		if c in set('äöü'):
			return 'front'
		if c in set('2368'):
			return 'back'
	return 'front'


def determine_stem_vowel(word, kotus_class=None):

	# Initialisms "tv", "CNN"
	if kotus_class in ['18B', '10B']:
		c = word[-1].lower()
		if c in 'bcdegptvw':
			return 'e'
		if c in 'flmnrsxä':
			return 'ä'
		if c in 'az':
			return 'a'
		if c in 'hkoå':
			return 'o'
		if c in 'qu':
			return 'u'
		if c in 'yü':
			return 'y'
		if c in 'ij':
			return 'i'
		if c in 'ö':
			return 'ö'

	for v in reversed(word):
		if v in 'aeiouyäöü':
			return v
		u = unaccent(v)
		if u in 'aeiouy':
			return u
	return 'i'


def plural2singular(plural, kotus_class, gradation):

	"""
	Given a plurale tantum noun and its inflectional properties, return its (hypothetical) singular.
	e.g. "olympialaiset" => "olympialainen", "lauteet" => "laude", "Antillit" => "Antilli"
	"""

	# "yliset" => "ylinen"
	if kotus_class == '38':
		yli = plural[:-3]
		return f'{yli}nen'

	# "lauteet" => "laude"
	if kotus_class in ['48', '49b']:
		laude = grad_weak(plural[:-2], gradation)
		return f'{laude}'

	# "länget" => "länki"
	if kotus_class == '7':
		saks = grad_strong(plural[:-1], gradation)[:-1]
		return f'{saks}i'

	# "hohtimet" => "hohdin", "lämpimät" => "lämmin"
	if kotus_class in ['33', '35']:
		hohdi = grad_weak(plural[:-3], gradation)
		return f'{hohdi}n'

	# "ikenet" => "ien"
	if kotus_class == '32':
		ie = grad_weak(plural[:-3], gradation)
		n = plural[-3]
		return f'{ie}{n}'

	# "persukset" => "persus"
	if kotus_class == '39':
		persu = plural[:-4]
		return f'{persu}s'

	# "maltaat" => "mallas"
	if kotus_class == '41':
		malla = grad_weak(plural[:-2], gradation)
		return f'{malla}s'

	# "liittoutuneet" => "liittoutunut"
	if kotus_class == '47':
		liittoutun = plural[:-3]
		return f'{liittoutun}ut'

	# "vanhemmat" => "vanhempi"
	if kotus_class == '16':
		vanhem = plural[:-3]
		return f'{vanhem}pi'

	# "-immät" => "-in", "vasemmat" => "vasen"
	if kotus_class in ['36', '37']:
		vanhi = plural[:-4]
		return f'{vanhi}n'

	# "kannet" => "kansi"
	if kotus_class == '28':
		kan = plural[:-3]
		return f'{kan}si'

	# "vuodet" => "vuosi"
	if kotus_class == '27':
		vuo = plural[:-3]
		return f'{vuo}si'

	# "haahdet" => "haaksi"
	if kotus_class == '31':
		haa = plural[:-4]
		return f'{haa}ksi'

	# "vaikeudet" => "vaikeus"
	if kotus_class == '40':
		vaikeu = plural[:-3]
		return f'{vaikeu}s'

	# "unet" => "uni"
	if kotus_class in ['23', '24', '25', '26', '29', '30']:
		un = plural[:-2]
		return f'{un}i'

	# "auteret" => "auer"
	if kotus_class == '49':
		aue = grad_weak(plural[:-3], gradation)
		r = plural[-3]
		return f'{aue}{r}'

	# "oluet" => "olut"
	if kotus_class == '43':
		olu = plural[:-2]
		return f'{olu}t'
	# "keväät" => "kevät"
	if kotus_class == '44':
		keva = plural[:-2]
		return f'{keva}t'

	# "miehet" => "mies"
	if kotus_class == '42':
		mie = plural[:-3]
		return f'{mie}s'

	# "tuhannennet" => "tuhannes"
	if kotus_class == '45':
		tuhanne = plural[:-4]
		return f'{tuhanne}s'

	# "tuhannet" => "tuhat"
	if kotus_class == '46':
		tuha = plural[:-4]
		return f'{tuha}t'

	# "roux’t" => "roux"
	if kotus_class == '22':
		roux = plural[:-2]
		return f'{roux}'

	# "tumattomat" => "tumaton"
	if kotus_class == '34':
		tumato = grad_weak(plural[:-3], gradation)
		return f'{tumato}n'

	# "yt:t" => "yt"
	if kotus_class in ['1B', '5B', '6B', '8B', '10B', '18B', '27B', '31B', 'XX']:
		tv = plural[:-2]
		return f'{tv}'

	# "urut" => "urku", "pidot" => "pito", "häät" => "hää"
	if kotus_class in [
		'1', '2', '9', '14', '6', '11', '10', '18', '8', '5', '12',
		'3', '17', '13', '15', '19', '21', '18U', '21', '20', '4']:
		uru = plural[:-1]
		urku = grad_strong(uru, gradation)
		return f'{urku}'

	print('Unk class:', [kotus_class, plural])
	input()
	uru = plural[:-1]
	urku = grad_strong(uru, gradation)
	return f'{urku}'


def merge_inflections(inflections_primary: dict, inflections_secondary: dict, secondary_tag: str):

	keys = set(inflections_primary.keys()) & set(inflections_secondary.keys())

	tagged = {
		f'{key}|{secondary_tag}': sorted(set(inflections_secondary[key]) - set(inflections_primary[key]))
		for key in keys
	}
	tagged = {key: forms for key, forms in tagged.items() if forms}

	combined = copy.deepcopy(inflections_primary)
	combined.update(tagged)

	# FIXME
	if '@stem:clitics|nstd' in combined:
		del combined['@stem:clitics|nstd']

	return combined
