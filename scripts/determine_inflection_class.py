import re
from scripts.file_tools import read_list_tsv

SPECIAL = '.?!#€$&%+_‰@†°/’'
VOWELS = \
	'aeiouy' \
	'äëïöüÿ' \
	'áéíóúý' \
	'àèòìùỳ' \
	'âêîôûŷ' \
	'āēīōūȳ' \
	'ãẽĩõũỹ' \
	'ąęįǫų' \
	'ȧėȯẏ' \
	'åůăěűőøæœŵ'

# Regex character sets
VOICED = '[aeiouyäömnlr]'
SILENT = '[szxrłtdwjh]'

# Regex shorthands
V = '[%s]' % VOWELS
N = '([aeiouyäö]i|[aeiou]u|[äeiöy][y]|aa?|ee?|ii?|oo?|uu?|yy?|ää?|öö?|ie|uo|yö)'
D = '([aeiouyäö]i|[aeiou]u|[äeiöy][y]|aa|ee|ii|oo|uu|yy|ää|öö|ie|uo|yö)'
C = f'[^0-9{VOWELS}{SPECIAL}]'


def get_base(word):
	return re.split('[ %|-]', word)[-1]


def read_lemmas():
	lemmas = {}
	for row in \
		read_list_tsv('lexicon.tsv') + \
		read_list_tsv('guesser.tsv'):

		if len(row) != 10:
			continue

		pfx, lemma, _, pos, kotus_class, grad, _, _, _, _ = row

		if pfx and not ('|' in lemma or '-' in lemma):
			continue
		if not kotus_class:
			continue

		# key = lemma, pos
		# lemmas[key] = lemmas.get(key, []) + [(kotus_class, grad)]
		base = get_base(lemma)
		key = base, pos
		lemmas[key] = lemmas.get(key, []) + [(kotus_class, grad)]

	for key, vals in lemmas.items():
		lemmas[key] = sorted(set(vals))
	return lemmas


LEMMAS = read_lemmas()


def determine_by_lemma_list(word, pos):

	"""
	Return pairs of inflection type + gradation type.
	"""

	if '|' in word or '%' in word:
		pos = pos.replace('proper', 'noun')

	base = get_base(word)
	key = base, pos
	match = LEMMAS.get(key)
	print('·', word, '=>', (base, pos))
	return match


def deduce_gradation(word, pos=None):

	# Quantitaive gradation is unlikely in unadapted loans w/ following letters
	if re.findall('[xåø]', word):
		return ''

	# Quantitative gradation
	if re.fullmatch(f'.*{VOICED}pp{V}', word):
		return 'pp:p'
	if re.fullmatch(f'.*{VOICED}tt{V}', word):
		return 'tt:t'
	if re.fullmatch(f'.*{VOICED}kk{V}', word):
		return 'kk:k'

	# Qualitative gradation is unlikely in unadapted loans & foreign names
	if re.findall('[bqcfxzwåø]', word) or pos in ['proper', 'proper-pl']:
		return ''

	word = word.lower()

	# Qualitative gradation (often dubious)
	if re.fullmatch(f'.*{N}ht[aeiouyäö]', word):
		return '?t:d'
	if re.fullmatch(f'.*{N}mp[aeiouyäö]', word):
		return '?mp:mm'
	if re.fullmatch(f'.*{N}nk[aeiouyäö]', word):
		return '?nk:ng'
	if re.fullmatch(f'.*{N}nt[aeiouyäö]', word):
		return '?nt:nn'
	if re.fullmatch(f'.*{N}lt[aeiouyäö]', word):
		return '?lt:ll'
	if re.fullmatch(f'.*{N}rt[aeiouyäö]', word):
		return '?rt:rr'

	return ''


def determine_verb_class(word):

	"""
	★ PERFECT
	"""

	word = word.lower()

	if re.fullmatch(f'.+(oida|öidä)', word):
		return [('62', '')]

	if re.fullmatch(f'.+(ske|ste)(lla|llä)', word):
		return [('67', '')]
	if re.fullmatch(f'.+nne(lla|llä)', word):
		return [('67', 'nt:nn')]
	if re.fullmatch(f'.+lle(lla|llä)', word):
		return [('67', 'lt:ll')]
	if re.fullmatch(f'.+hde(lla|llä)', word):
		return [('67', 't:d')]
	if re.fullmatch(f'.+{VOICED}te(lla|llä)', word):
		return [('67', 'tt:t')]
	if re.fullmatch(f'.+{VOICED}pe(lla|llä)', word):
		return [('67', 'pp:p')]
	if re.fullmatch(f'.+{VOICED}ke(lla|llä)', word):
		return [('67', 'kk:k')]
	if re.fullmatch(f'.+(lla|llä)', word):
		return [('67', '')]

	if re.fullmatch(f'.+{VOICED}t(ata|ätä)', word):
		return [('73', 'tt:t')]
	if re.fullmatch(f'.+{VOICED}p(ata|ätä)', word):
		return [('73', 'pp:p')]
	if re.fullmatch(f'.+{VOICED}k(ata|ätä)', word):
		return [('73', 'kk:k')]
	if re.fullmatch(f'.+{V}[bgd](ata|ätä)', word):
		return [('73', '??')]
	if re.fullmatch(f'.+(ll|rr|nn)(ata|ätä)', word):
		return [('73', '??')]
	if re.fullmatch(f'.+(ata|ätä)', word):
		return [('73', '')]
	if re.fullmatch(f'.+(ytä|uta)', word):
		return [('74', '')]
	if re.fullmatch(f'.+(etä|eta)', word):
		return [('74', '')]
	if re.fullmatch(f'.+(ötä|ota)', word):
		return [('74', '')]

	if re.fullmatch(f'.+{V}(tua|tyä)', word):
		return [('52', 't:d')]
	if re.fullmatch(f'.+(ttua|ttyä)', word):
		return [('52', 'tt:t')]
	if re.fullmatch(f'.+(stua|styä)', word):
		return [('52', '')]
	if re.fullmatch(f'.+{V}(ntua|ntyä)', word):
		return [('52', 'nt:nn')]
	if re.fullmatch(f'.+(oa|ua)', word):
		return [('52', '??')]

	if re.fullmatch(f'.+(ttaa|ttää)', word):
		return [('53', 'tt:t')]
	if re.fullmatch(f'.+(htaa|htää)', word):
		return [('53', 't:d')]
	if re.fullmatch(f'.+(ntaa|ntää)', word):
		return [('53', 'nt:nn')]
	if re.fullmatch(f'.+(ltaa|ltää)', word):
		return [('53', 'lt:ll')]
	if re.fullmatch(f'.+(rtaa|rtää)', word):
		return [('53', 'rt:rr')]
	if re.fullmatch(f'.+(staa|stää)', word):
		return [('53', '')]
	if re.fullmatch(f'.+(taa|tää)', word):
		return [('53', 't:d')]

	if re.fullmatch(f'.+(ista|istä)', word):
		return [('66', '')]

	if re.fullmatch(f'.+(iä|ia)', word):
		return [('61', '')]

	# Verbs w/ limited inflection
	if re.fullmatch('.+(ajaa|äjää)', word):
		return [('77', '')]
	if re.fullmatch('.+(ee)', word):
		return [('ERKANEE', '')]

	print('WARNING! Unknown verb type:', word)
	return [('???', '')]


def determine_adjective_class(word):

	"""
	★ PERFECT
	"""

	word = word.lower()

	# lahjaton, kyvytön
	if re.fullmatch('.+(ton|tön)', word):
		return [('34', 'tt:t')]

	# suurehko, pienehkö
	if re.fullmatch('.+(hko|hkö)', word):
		return [('1', '')]

	# edustava, näyttävä, nähtävä, murhaava
	if re.fullmatch('.+(tt|st|ht|nt|pp)(ava|ävä)', word) or re.fullmatch('.+(aava|äävä|oava|oiva|öivä)', word):
		return [('10', '')]

	# menestyvä
	if re.fullmatch('.+(yvä|uva)', word):
		return [('10', '')]

	# mennyt, kadonnut, kuollut, kehittynyt, hermostunut
	if re.fullmatch('.+(nn|ss|rr|ll|hn)(ut|yt)', word) or re.fullmatch('.+(unut|ynyt)', word):
		return [('47', '')]

	# tärähtänyt
	if re.fullmatch('.+(nn|ss|rr|ll|hn)(ut|yt)', word) or re.fullmatch('.+(htänyt|htanut)', word):
		return [('47', '')]

	# haluttu, suosittu, piesty
	if re.fullmatch('.+(stu|sty|ttu|tty)', word):
		return [('1', '')]

	# andorralainen
	if re.fullmatch(f'.+inen', word):
		return [('38', '')]

	# ehompi, alempi, enempi
	if re.fullmatch(f'.+mpi', word):
		return [('16', 'mp:mm')]

	# varhin, alin, enin
	if re.fullmatch(f'.+in', word):
		return [('36', '')]

	# hälyisä, makoisa, kalaisa
	if re.fullmatch(f'.+{V}(isa|isä)', word):
		return [('10', '')]

	# kapea, sokea, pirteä
	if re.fullmatch('.+(ea|eä)', word):
		return [('15', '')]

	# kapea, sokea, pirteä
	if re.fullmatch('.+(ea|eä)', word):
		return [('15', '')]

	return determine_noun_class_1(word)


def determine_noun_pl_class(word, pos='noun-pl'):

	"""
	★ PERFECT
	"""

	word = word.lower()

	# tulukset
	if re.fullmatch('.+kset', word):
		return [('39', '')]

	# tuliaiset, uutiset
	if re.fullmatch('.+iset', word):
		return [('38', '')]
	# pulmuset, pakkaset
	if re.fullmatch(f'.+{V}set', word):
		return [('?38', '')]

	# antimet
	if re.fullmatch('.+imet', word):
		return [('33', '??')]

	# iltamat
	if re.fullmatch(f'.+{V}m[a]t', word):
		return [('10', '??')]

	# Pyreneet
	if re.fullmatch(f'.+eet', word) and pos == 'proper-pl':
		return [('?20', '')]
	# bileet
	if re.fullmatch(f'.+eet', word):
		return [('?48|20', '')]

	# "Lofootit"
	if re.fullmatch(f'.+{VOICED}tit', word):
		return [('5', 'tt:t')]
	# "Molukit"
	if re.fullmatch(f'.+{VOICED}kit', word):
		return [('5', 'kk:k')]
	# "Alpit"
	if re.fullmatch(f'.+{VOICED}pit', word):
		return [('5', 'pp:p')]

	# "kalsarit", "henkselit", "bikinit", "Kuriilit"
	if re.fullmatch(f'{C}*{N}{C}+(aa?|ii?|uu?|ee?|yy?|oo?|öö?|ää?)[lrn]it', word):
		return [('6', '')]

	# "universiadit"
	if re.fullmatch(f'.*{V}{C}+it', word):
		return [('5', '')]

	return determine_noun_class_1(word[:-1])


def determine_noun_class_1(word, pos='noun'):

	# likainen, lapsonen, lintunen, kymmenen
	if re.fullmatch(f'.*{V}{C}+{N}nen', word.lower()):
		return [('38', '')]
	# Jokioinen, Kauniainen, Nousiainen, Saarioinen
	if re.fullmatch(f'.+(ai|äi|ei|oi|öi)nen', word):
		return [('38', '')]

	# aikaistus, työllistys
	if re.fullmatch('.+(istus|istys)', word):
		return [('39', '')]
	# kavallus, kumarrus, parannus
	if re.fullmatch('.+(nn|ll|rr)(us|ys)', word):
		return [('39', '')]
	# ahtaus, hitaus, putous
	if re.fullmatch('.+(ou|au|äy)s', word):
		return [('39|40', '')]
	# pituus, kateus
	if re.fullmatch('.+(uu|yy|eu|ey|au|äy|öy)s', word) and pos == 'noun':
		return [('40', '')]

	# punos, tennis, viinas, köynnös, aakkostus, väsytys, kives
	if re.fullmatch(f'.+{V}{C}+[aeiouyäö]s', word):
		return [('39', '')]

	# organisaatio
	if re.fullmatch('.+aatio', word):
		return [('3', '')]

	# vuokraamo, heräämö, näyttämö, veistämö
	if re.fullmatch('.+(stamo|stämö|ttamo|ttämö|aamo|äämö)', word):
		return [('2', '')]

	# kulkija, kävijä
	if re.fullmatch(f'.*{V}{C}+(ija|ijä)', word):
		return [('12', '')]

	# kuvaaja, kerääjä, vakooja, tuottaja, veistäjä, johtaja
	if re.fullmatch(f'.*{V}{C}+(aaja|ääjä|ooja|oija|öijä)', word) or re.fullmatch('.+(tt|st|ht)(aja|äjä)', word):
		return [('10', '')]
	if re.fullmatch('.+t(aja|äjä)', word):
		return [('?10', '')]

	# englanti, hollanti
	if re.fullmatch(f'.*lanti', word):
		return [('5', 'nt:nn')]

	# boulderointi, debatointi
	if re.fullmatch(f'.*(ointi|öinti)', word):
		return [('5', 'nt:nn')]

	# arvuuttelu, hifistely
	if re.fullmatch('.*(st|tt|ht|lt|rt|nt)(elu|ely)', word):
		return [('2', '')]

	# nimistö / Kivistö
	if re.fullmatch('.*istö', word):
		return [('1', '')]

	# harvennin, kaiverrin, puhallin, kaihdin, tulostin, viivoitin
	if re.fullmatch('.+llin', word):
		return [('33', 'lt:ll')]
	if re.fullmatch('.+rrin', word):
		return [('33', 'rt:rr')]
	if re.fullmatch('.+nnin', word):
		return [('33', 'nt:nn')]
	if re.fullmatch('.+hdin', word):
		return [('33', 't:d')]
	if re.fullmatch('.+stin', word):
		return [('33', '')]
	if re.fullmatch('.+[aeiouyäö]tin', word):
		return [('?33', 'tt:t')]

	# laskeuma, avauma, murtuma
	if re.fullmatch('.+(uma|ymä)', word):
		return [('10', '')]

	return determine_noun_class_2(word, pos)


def determine_noun_class_2(word, pos='noun'):

	if re.fullmatch(f'.*[FLMNRSXZ7]\.?', word):
		return [('?10B', '')]
	if re.fullmatch(f'.*[ABCDEGPTVWIJHKOÅQUYÜÄÖÉ]\.?', word):
		return [('?18B', '')]

	if re.fullmatch(f'.*[12]', word):
		return [('31B', '')]
	if re.fullmatch(f'.*[34]', word):
		return [('8B', '')]
	if re.fullmatch(f'.*[56]', word):
		return [('27B', '')]
	if re.fullmatch(f'.*[789]', word):
		return [('10B', '')]
	if re.fullmatch(f'.*[0-9]0', word):
		return [('8B', '')]

	# TODO
	if re.fullmatch(f'.*[0-9+]', word):
		return [('??', '')]
	if re.fullmatch(f'[0-9].+', word):
		return [('??', '')]

	# file names and intenet domains – guesser should handle most of these
	if re.fullmatch(f'.*\.[a-z][a-z][a-z]?', word):
		return determine_noun_class_2(word.upper())
	if re.fullmatch(f'.*[{SPECIAL}]', word):
		return [('XX', '')]

	word = word.lower()
	grad = deduce_gradation(word, pos)

	# ––––––––––––––––––
	# Words ending in -i
	# ––––––––––––––––––

	# chi / Li, Yi, Xi
	if re.fullmatch(f'{C}*y?i', word):
		return [('18', '')]

	# samurai, paksoi, fengshui, lei / Huyndai, Petroskoi, Rapanui, Zelenskyi
	if re.fullmatch(f'.*{V}i', word):
		return [('18', '')]

	# kuppi, tölkki, pantti / Kamppi, Atlantti, Mansikki
	if re.fullmatch(f'.+(pp|tt|kk)i', word):
		return [('5', grad)]

	# dyyni, laguuni, etyyni vs. taifuuni, tribuuni
	if re.fullmatch('.+(uuni|yyni)', word):
		return [('?5|6', '')]

	# kvenelli, atolli / ...
	if re.fullmatch(f'{C}*{N}{C}*{V}lli', word):
		return [('6', '')]

	# diaari, kaleeri, frisyyri, rehtori / Berliini, Kajaani
	if re.fullmatch(f'{C}*{N}{C}*(aa|ee|ii|oo|uu|yy|ää|öö)[lrn]i', word):
		return [('6', '')]

	# aktuaari, portieeri, amatööri, dosentuuri
	if re.fullmatch(f'.*(aa|ee|ii|oo|uu|yy|ää|öö)[lrn]i', word):
		return [('5', '')]

	# Ficantieri, Alighieri, Khomeini
	if re.fullmatch(f'.*{V}{V}[nrl]i', word):
		return [('5', '')]

	# diopteri, glitteri, osmani, bageli, jysäri, crostini / Valtori, Flemari, Hesari, Brysseli
	if re.fullmatch(f'.*{V}{C}*{V}[nrl]i', word):
		return [('?6', '')]

	# seesami, foorumi, seerumi, daimoni
	if re.fullmatch(f'.*{D}{C}*{V}mi', word):
		return [('6', '')]

	# appsi, boosti, dekkaristi / Redi, Migri, Gucci, Swarovski
	if re.fullmatch(f'.*i', word):
		return [('5', grad)]

	# ––––––––––––––––––
	# Words ending in -e
	# ––––––––––––––––––

	# birdie, fruitie, fondue, pétanque / Vogue, PewDiePie, Carrie, Kanye
	if re.fullmatch(f'.*{V}{C}+[uiy]e', word):
		return [('8|21', '')]

	# taxfree / Kitee, Lee, Tennessee
	if re.fullmatch(f'.*ee', word):
		return [('?18|21|20', '')]

	# He, Le
	if re.fullmatch(f'{C}*y?e', word):
		return [('21', '')]

	# Unicode, Entresse, BirdLife
	if re.fullmatch(f'.*e', word) and grad:
		return [('8', '??')]
	if re.fullmatch(f'.*e', word):
		return [('8', '')]

	# ––––––––––––––––––
	# Words ending in -o, -ö
	# ––––––––––––––––––

	# koo
	if re.fullmatch(f'{C}*y?(oo|öö)', word):
		return [('18', '')]

	# Luo
	if re.fullmatch(f'{C}*y?(uo)', word):
		return [('1', '')]

	# Espoo, Lontoo, Porvoo, Sipoo, Inkoo
	if re.fullmatch(f'{C}*{N}{C}*(oo|öö)', word):
		return [('17', '')]

	# politbyroo, vindaloo, miljöö / Susanoo
	if re.fullmatch(f'.*(oo|öö)', word):
		return [('?20|18', '')]

	# Bo, Po
	if re.fullmatch(f'{C}*y?[oö]', word):
		return [('21', '')]

	# Mao, Gao, Zhao, Tao, Leo
	if re.fullmatch(f'{C}*y?[aäe][oö]', word):
		return [('1', '')]

	# video, radio, littiö / Mario, Bilbao, Kihniö
	if re.fullmatch(f'.*[aäei][oö]', word):
		return [('3', '')]

	# hiilikko, karismaatikko / Männikkö, Saarikko, Marokko
	if re.fullmatch(f'.*{V}{C}+{N}kk[oö]', word):
		return [('4', 'kk:k')]

	# kotilo, purtilo, henkilö, eskimo, gigolo, domino, karpalo, karkelo, kiwano / Kosovo
	if re.fullmatch(f'.*{V}{C}+{V}[lrnmvw][oö]', word):
		return [('2', '')]

	# Pyykkö, Ylppö
	if re.fullmatch(f'.*(kk|pp|tt)ö', word):
		return [('1', grad)]

	# Föglö
	if re.fullmatch(f'.*ö', word) and not grad:
		return [('?21', '')]

	# sello / Despacito, Fernando, Nato
	if re.fullmatch(f'.*[oö]', word):
		return [('1', grad)]

	# ––––––––––––––––––
	# Words ending in -y
	# ––––––––––––––––––

	# jersey, cowboy / Savoy, Yesterday, Disney, Lindøy
	if re.fullmatch(f'.*[aeoiø]y', word):
		return [('21', '')]

	# By
	if re.fullmatch(f'{C}*y', word):
		return [('21', '')]

	# kyy
	if re.fullmatch(f'{C}*yy', word):
		return [('18', '')]

	# menyy
	if re.fullmatch(f'.*yy', word):
		return [('20', '')]

	# Battery, Montgomery
	if re.fullmatch(f'.*{V}{C}*ery', word):
		return [('2', '')]

	# Amnesty, Sony, Banksy
	if re.fullmatch(f'.*y', word):
		return [('1', grad)]

	# ––––––––––––––––––
	# Words ending in -u
	# ––––––––––––––––––

	# Hu, Wu, Zhu, Ryu, Yu
	if re.fullmatch(f'{C}*y?u', word):
		return [('21', '')]

	# gnuu
	if re.fullmatch(f'{C}*y?uu', word):
		return [('18', '')]

	# kaipuu, epuu / Keuruu, Kainuu
	if re.fullmatch(f'{C}*{N}{C}*uu', word):
		return [('17', '')]

	# pistou, tiu, clou, tau / Macau, Palau, Guangzhou, Liu, Zhou
	if re.fullmatch(f'.*(iu|ou|au|eu)', word):
		return [('21', '')]

	# (hypothetical)
	if re.fullmatch(f'.*uu', word):
		return [('20', '')]

	# ???
	if re.fullmatch(f'.*u', word):
		return [('1', grad)]

	# ––––––––––––––––––
	# Words ending in -ä
	# ––––––––––––––––––

	# (hypothetical)
	if re.fullmatch(f'{C}*ä', word):
		return [('21', '')]

	# Hyvinkää
	if re.fullmatch(f'.*ää', word):
		return [('18', '')]

	# ätläkkä
	if re.fullmatch(f'.*{V}{C}+{V}kkä', word):
		return [('14', 'kk:k')]

	# Kittilä, Kärkölä
	if re.fullmatch(f'.*{V}{C}+{V}lä', word):
		return [('12', '')]

	# Tyrnävä
	if re.fullmatch(f'.*{V}{C}+{V}vä', word):
		return [('10', '')]

	# Pöytyä, Perähikiä
	if re.fullmatch(f'.*{V}{C}+[yi]ä', word):
		return [('12', '')]

	# väninä / Värttinä
	if re.fullmatch(f'.*{V}{C}+[äi]nä', word):
		return [('12', '')]

	# Sysmä, Ypäjä
	if re.fullmatch(f'.*ä', word):
		return [('10', grad)]

	# ––––––––––––––––––
	# Words ending in -a
	# ––––––––––––––––––

	# TODO: Camilla, kaldera, apila <> apina

	# Ra, Ma
	if re.fullmatch(f'{C}*y?[a]', word):
		return [('21', '')]

	# Mia, Lea
	if re.fullmatch(f'{C}*[ie][a]', word):
		return [('9', '')]

	# boa / Hua, Goa
	if re.fullmatch(f'{C}*[yuo][a]', word):
		return [('10', '')]

	# kvinoa
	if re.fullmatch(f'.*oa', word):
		return [('10', '')]

	# Laukaa, Vantaa
	if re.fullmatch(f'.*aa', word):
		return [('18', '')]

	# murikka / Kurikka, Puhakka, Afrikka, Laatokka
	if re.fullmatch(f'.*{V}{C}+{V}kka', word):
		return [('14', 'kk:k')]
	# ulappa / Holappa
	if re.fullmatch(f'.*{V}{C}+{V}ppa', word):
		return [('14', 'pp:p')]

	# Jukola vs. Mykola, Carola
	if re.fullmatch(f'.*{V}{C}+ola', word):
		return [('?12|10', '')]

	# Vaapukkala, Attila
	if re.fullmatch(f'{C}*{N}{C}+a[rln]a', word):
		return [('12', '')]
	if re.fullmatch(f'{C}*{N}{C}+[ei][rln]a', word):
		return [('13', '')]
	# Camilla
	if re.fullmatch(f'{C}*{N}{C}+illa', word):
		return [('13', '')]
	if re.fullmatch(f'.*{V}{C}+{V}la', word):
		return [('12', '')]

	# Tonava, Harkova, Kauhava, Sulkava
	if re.fullmatch(f'{C}*{N}{C}+{V}va', word):
		return [('?10|12', '')]

	# satama, valkama / Panama, Bahama, Gautama
	if re.fullmatch(f'{C}*{N}{C}+ama', word):
		return [('10', '')]

	# kahiseva / Bratislava
	if re.fullmatch(f'.*{V}{C}+[aei]va', word):
		return [('?10|9', '')]

	# ???
	if re.fullmatch(f'.*{V}{C}+{V}va', word):
		return [('10', '')]

	# Finlandia, Enya, Lapua, Galilea
	if re.fullmatch(f'.*{V}{C}+[iyue]a', word):
		return [('12', '')]

	# Cicciolina, Medina, Burana, Kiiruna
	if re.fullmatch(f'.*{V}{C}+[aiu]na', word):
		return [('?13', '')]

	# Aura, Eura, Teuva, Laura, Freya
	if re.fullmatch(f'{C}*[ae][uy]{C}+a', word):
		return [('9', grad)]

	# kanuuna, sitruuna, mureena / Ateena
	if re.fullmatch(f'.*{V}{C}+(uu|ee)na', word):
		return [('13', '')]

	# Ursa, Buddha, Madonna
	if re.fullmatch(f'(.*{C})?[yuoöüúűûūóőôōýŷø][iuy]?{C}*a', word):
		return [('10', grad)]

	# kooma / Luoma, Joona,
	if re.fullmatch(f'(.*{C})?(oo|uo){C}+a', word):
		return [('10', grad)]

	# Indokiina, Eveliina, Palestiina
	if re.fullmatch(f'.*iina', word):
		return [('9', '')]

	# sairaala, hetaira / Oliveira, Madeira, Ukraina
	if re.fullmatch(f'.*{V}{C}*{D}[rln]a', word):
		return [('?13|9', '')]

	# ...
	if re.fullmatch(f'.*a', word):
		return [('9', grad)]

	# ––––––––––––––––––

	# Rare vowels

	if re.fullmatch('.*[úűûūóőôōýŷøò]', word):
		return [('?21|1', '')]
	if re.fullmatch(f'.*[åáéíà]', word):
		return [('?21', '')]

	# Consonants

	if re.fullmatch(f'.*{V}{C}+[aeiou]s', word):
		return [('?39', '')]
	if re.fullmatch(f'.*{V}{C}+i[oau]s', word):
		return [('39', '')]

	if re.fullmatch(f'.*{D}+[rln]', word):
		return [('5', '')]
	if re.fullmatch(f'.*{V}{C}+(ul|ur)', word):
		return [('?5', '')]
	if re.fullmatch(f'.*[aäeou][iuy]er', word):
		return [('?6', '')]
	if re.fullmatch(f'.*{V}{C}+(on|an|er|al|en|or|el|ol|ar)', word):
		return [('?6', '')]
	if re.fullmatch(f'.+{C}{C}+', word):
		return [('5', '')]
	if re.fullmatch(f'.*(aw|ow|ew)', word):
		return [('?22|5', '')]
	if re.fullmatch(f'.+{SILENT}', word):
		return [('?5|22', '')]
	if re.fullmatch(f'{C}*{N}{C}+', word):
		return [('5', '')]
	if re.fullmatch(f'.+{C}', word):
		return [('5', '')]

	return [('???', '')]


def determine_inflection_class(word, pos):

	cl = []

	if '|' in word or '%' in word or '-' in word or ' ' in word:
		cl = determine_by_lemma_list(word, pos)
	if cl:
		return cl

	word = get_base(word)

	# TODO: Utilize guesser for proper nouns?

	if pos in ['noun', 'proper']:
		cl = determine_noun_class_1(word, pos=pos)
	elif pos in ['noun-pl', 'proper-pl']:
		cl = determine_noun_pl_class(word, pos=pos)
	elif pos == 'adjective':
		cl = determine_adjective_class(word)
	elif pos == 'verb':
		cl = determine_verb_class(word)
	return cl

