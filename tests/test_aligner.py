from scripts.aligner.aligner import align_all_inflections, print_pairs
import unittest

keys = [
	'@base',
	'@stem:possessives',
	'@stem:possessives:nom',
	'@stem:possessives:sg:nom',
	'@stem:possessives:sg:gen',
	'@stem:possessives:pl:nom',
	'',
	'sg|nom',
	'sg|gen',
	'sg|gen|rare',
	'sg|acc',
	'sg|acc|rare',
	'sg|par',
	'sg|ill',
	'sg|ine',
	'sg|ela',
	'sg|all',
	'sg|ade',
	'sg|abl',
	'sg|ess',
	'sg|tra',
	'sg|abe',
	'pl|nom',
	'pl|gen',
	'pl|gen|rare',
	'pl|par',
	'pl|ill',
	'pl|ine',
	'pl|ela',
	'pl|all',
	'pl|ade',
	'pl|abl',
	'pl|ess',
	'pl|tra',
	'pl|abe',
	'pl|com',
	'pl|ins',

	'nom',
	'gen',
	'gen|rare',
	'acc',
	'par',
	'ill',
	'ine',
	'ela',
	'all',
	'ade',
	'abl',
	'ess',
	'tra',
	'abe',
	'com',
	'ins',

	'comparative',
	'superlative',
	'comparative|nstd',

	'inf1',
	'inf1|tra',
	'inf2|ins',
	'inf2|ine',
	'inf3|ine',
	'inf3|ela',
	'inf3|ill',
	'inf3|ade',
	'inf3|abe',
	'inf3|ins',
	'inf4',
	'inf5',
	'part_pres',
	'part_past',
	'part_ma',
	'part_maton',
	'pres|1sg',
	'pres|2sg',
	'pres|3sg',
	'pres|1pl',
	'pres|2pl',
	'pres|3pl',
	'pres|conneg',
	'past|1sg',
	'past|2sg',
	'past|3sg',
	'past|1pl',
	'past|2pl',
	'past|3pl',
	'past|conneg',
	'cond|1sg',
	'cond|2sg',
	'cond|3sg',
	'cond|1pl',
	'cond|2pl',
	'cond|3pl',
	'cond|conneg',
	'poten|1sg',
	'poten|2sg',
	'poten|3sg',
	'poten|1pl',
	'poten|2pl',
	'poten|3pl',
	'poten|conneg',
	'imper|2sg',
	'imper|3sg',
	'imper|1pl',
	'imper|2pl',
	'imper|3pl',
	'imper|2sg|conneg',
	'imper|3sg|conneg',
	'imper|pl|conneg',
	'imper|2pl|rare',
	'imper|2pl|arch',
	'imper|2pl|nstd',
	'pass|pres',
	'pass|past',
	'pass|cond',
	'pass|poten',
	'pass|imper',
	'pass|pres|conneg',
	'pass|past|conneg',
	'pass|cond|conneg',
	'pass|poten|conneg',
	'pass|imper|conneg',
	'pass|inf2|ine',
	'pass|inf3|ins',
	'pass|part_pres',
	'pass|part_past',
]


def align(inflections, pos):

	aligned = align_all_inflections(inflections, pos)

	for key in aligned:
		if key not in keys:
			print(f"'{key}',")
			keys.extend([key])

	pairs = sorted(aligned.items(), key=lambda pair: keys.index(pair[0]))
	# for key, forms in pairs:
	# 	for form in forms:
	# 		p1 = (f"'{key}'," + ' ' * 28)[:28] + f"'{print_pairs(form)}'"
	# 		print(f"({p1}),")
	return [(key, print_pairs(form)) for key, forms in pairs for form in forms]


class FiParserTests(unittest.TestCase):

	# Nouns

	def test_noun_aallokko(self):
		inflections = {
			'@base':  ['aallokko'],
			'sg|nom': ['aallokko'],
			'sg|gen': ['aallokon'],
			'sg|par': ['aallokkoa'],
			'sg|ill': ['aallokkoon'],
			'sg|ine': ['aallokossa'],
			'sg|ela': ['aallokosta'],
			'sg|all': ['aallokolle'],
			'sg|ade': ['aallokolla'],
			'sg|abl': ['aallokolta'],
			'sg|ess': ['aallokkona'],
			'sg|tra': ['aallokoksi'],
			'sg|abe': ['aallokotta'],
			'pl|nom': ['aallokot'],
			'pl|gen': ['aallokkojen', 'aallokoiden', 'aallokoitten'],
			'pl|par': ['aallokkoja', 'aallokoita'],
			'pl|ill': ['aallokkoihin', 'aallokoihin'],
			'pl|ine': ['aallokoissa'],
			'pl|ela': ['aallokoista'],
			'pl|all': ['aallokoille'],
			'pl|ade': ['aallokoilla'],
			'pl|abl': ['aallokoilta'],
			'pl|ess': ['aallokkoina'],
			'pl|tra': ['aallokoiksi'],
			'pl|abe': ['aallokoitta'],
			'pl|com': ['aallokkoine'],
			'pl|ins': ['aallokoin'],
			'@stem:possessives': ['aallokko'],
		}
		aligned = align(inflections, pos='noun')
		self.assertEqual(aligned, [
			('@base',                'a:a a:a l:l l:l o:o k:k k:k o:o'),
			('@stem:possessives',    'a:a a:a l:l l:l o:o k:k k:k o:o'),
			('sg|nom',               'a:a a:a l:l l:l o:o k:k k:k o:o +sg:0 +nom:0'),
			('sg|gen',               'a:a a:a l:l l:l o:o k:k k:0 o:o +sg:0 +gen:n'),
			('sg|par',               'a:a a:a l:l l:l o:o k:k k:k o:o +sg:0 +par:a'),
			('sg|ill',               'a:a a:a l:l l:l o:o k:k k:k o:o +sg:0 +ill:o 0:n'),
			('sg|ine',               'a:a a:a l:l l:l o:o k:k k:0 o:o +sg:0 +ine:s 0:s 0:a'),
			('sg|ela',               'a:a a:a l:l l:l o:o k:k k:0 o:o +sg:0 +ela:s 0:t 0:a'),
			('sg|all',               'a:a a:a l:l l:l o:o k:k k:0 o:o +sg:0 +all:l 0:l 0:e'),
			('sg|ade',               'a:a a:a l:l l:l o:o k:k k:0 o:o +sg:0 +ade:l 0:l 0:a'),
			('sg|abl',               'a:a a:a l:l l:l o:o k:k k:0 o:o +sg:0 +abl:l 0:t 0:a'),
			('sg|ess',               'a:a a:a l:l l:l o:o k:k k:k o:o +sg:0 +ess:n 0:a'),
			('sg|tra',               'a:a a:a l:l l:l o:o k:k k:0 o:o +sg:0 +tra:k 0:s 0:i'),
			('sg|abe',               'a:a a:a l:l l:l o:o k:k k:0 o:o +sg:0 +abe:t 0:t 0:a'),
			('pl|nom',               'a:a a:a l:l l:l o:o k:k k:0 o:o +pl:t +nom:0'),
			('pl|gen',               'a:a a:a l:l l:l o:o k:k k:k o:o +pl:j 0:e +gen:n'),
			('pl|gen',               'a:a a:a l:l l:l o:o k:k k:0 o:o +pl:i 0:d 0:e +gen:n'),
			('pl|gen',               'a:a a:a l:l l:l o:o k:k k:0 o:o +pl:i 0:t 0:t 0:e +gen:n'),
			('pl|par',               'a:a a:a l:l l:l o:o k:k k:k o:o +pl:j +par:a'),
			('pl|par',               'a:a a:a l:l l:l o:o k:k k:0 o:o +pl:i +par:t 0:a'),
			('pl|ill',               'a:a a:a l:l l:l o:o k:k k:k o:o +pl:i +ill:h 0:i 0:n'),
			('pl|ill',               'a:a a:a l:l l:l o:o k:k k:0 o:o +pl:i +ill:h 0:i 0:n'),
			('pl|ine',               'a:a a:a l:l l:l o:o k:k k:0 o:o +pl:i +ine:s 0:s 0:a'),
			('pl|ela',               'a:a a:a l:l l:l o:o k:k k:0 o:o +pl:i +ela:s 0:t 0:a'),
			('pl|all',               'a:a a:a l:l l:l o:o k:k k:0 o:o +pl:i +all:l 0:l 0:e'),
			('pl|ade',               'a:a a:a l:l l:l o:o k:k k:0 o:o +pl:i +ade:l 0:l 0:a'),
			('pl|abl',               'a:a a:a l:l l:l o:o k:k k:0 o:o +pl:i +abl:l 0:t 0:a'),
			('pl|ess',               'a:a a:a l:l l:l o:o k:k k:k o:o +pl:i +ess:n 0:a'),
			('pl|tra',               'a:a a:a l:l l:l o:o k:k k:0 o:o +pl:i +tra:k 0:s 0:i'),
			('pl|abe',               'a:a a:a l:l l:l o:o k:k k:0 o:o +pl:i +abe:t 0:t 0:a'),
			('pl|com',               'a:a a:a l:l l:l o:o k:k k:k o:o +pl:i +com:n 0:e'),
			('pl|ins',               'a:a a:a l:l l:l o:o k:k k:0 o:o +pl:i +ins:n'),
		])

	def test_noun_ruis(self):
		inflections = {
			"@base":  ['ruis'],
			"sg|nom": ['ruis'],
			"sg|gen": ['rukiin'],
			"sg|par": ['ruista'],
			"sg|ine": ['rukiissa'],
			"sg|ess": ['rukiina'],
			"pl|nom": ['rukiit'],
			"pl|gen": ['rukiiden', 'rukiitten'],
			"pl|par": ['rukiita'],
			"pl|ine": ['rukiissa'],
		}
		aligned = align(inflections, pos='noun')
		self.assertEqual(aligned, [
			('@base',  'r:r u:u 0:0 i:i s:s 0:0'),
			('sg|nom', 'r:r u:u 0:0 i:i s:s 0:0 +sg:0 +nom:0'),
			('sg|gen', 'r:r u:u 0:k i:i s:0 0:i +sg:0 +gen:n'),
			('sg|par', 'r:r u:u 0:0 i:i s:s 0:0 +sg:0 +par:t 0:a'),
			('sg|ine', 'r:r u:u 0:k i:i s:0 0:i +sg:0 +ine:s 0:s 0:a'),
			('sg|ess', 'r:r u:u 0:k i:i s:0 0:i +sg:0 +ess:n 0:a'),
			('pl|nom', 'r:r u:u 0:k i:i s:0 0:i +pl:t +nom:0'),
			('pl|gen', 'r:r u:u 0:k i:i s:0 0:0 +pl:i 0:d 0:e +gen:n'),
			('pl|gen', 'r:r u:u 0:k i:i s:0 0:0 +pl:i 0:t 0:t 0:e +gen:n'),
			('pl|par', 'r:r u:u 0:k i:i s:0 0:0 +pl:i +par:t 0:a'),
			('pl|ine', 'r:r u:u 0:k i:i s:0 0:0 +pl:i +ine:s 0:s 0:a'),
		])

	def test_noun_vuosi(self):
		inflections = {
			"@base":  ['vuosi'],
			"sg|nom": ['vuosi'],
			"sg|gen": ['vuoden'],
			"sg|par": ['vuotta'],
			"sg|ine": ['vuodessa'],
			"sg|ess": ['vuotena'],
			"pl|nom": ['vuodet'],
			"pl|gen": ['vuosien', 'vuotten'],
			"pl|par": ['vuosia'],
			"pl|ine": ['vuosissa'],
		}
		aligned = align(inflections, pos='noun')
		self.assertEqual(aligned, [
			('@base',  'v:v u:u o:o s:s i:i'),
			('sg|nom', 'v:v u:u o:o s:s i:i +sg:0 +nom:0'),
			('sg|gen', 'v:v u:u o:o s:d i:e +sg:0 +gen:n'),
			('sg|par', 'v:v u:u o:o s:t i:0 +sg:0 +par:t 0:a'),
			('sg|ine', 'v:v u:u o:o s:d i:e +sg:0 +ine:s 0:s 0:a'),
			('sg|ess', 'v:v u:u o:o s:t i:e +sg:0 +ess:n 0:a'),
			('pl|nom', 'v:v u:u o:o s:d i:e +pl:t +nom:0'),
			('pl|gen', 'v:v u:u o:o s:s i:0 +pl:i 0:e +gen:n'),
			('pl|gen', 'v:v u:u o:o s:t i:0 +pl:t 0:e +gen:n'),
			('pl|par', 'v:v u:u o:o s:s i:0 +pl:i +par:a'),
			('pl|ine', 'v:v u:u o:o s:s i:0 +pl:i +ine:s 0:s 0:a'),
		])

	def test_noun_vanhempi(self):
		inflections = {
			"@base":  ['vanhempi'],
			"sg|nom": ['vanhempi'],
			"sg|gen": ['vanhemman'],
			"sg|par": ['vanhempia'],
			"sg|ine": ['vanhemmassa'],
			"sg|ess": ['vanhempana'],
			"pl|nom": ['vanhemmat'],
			"pl|gen": ['vanhempien'],
			"pl|par": ['vanhempia'],
			"pl|ine": ['vanhemmissa'],
		}
		aligned = align(inflections, pos='noun')
		self.assertEqual(aligned, [
			('@base',  'v:v a:a n:n h:h e:e m:m p:p i:i'),
			('sg|nom', 'v:v a:a n:n h:h e:e m:m p:p i:i +sg:0 +nom:0'),
			('sg|gen', 'v:v a:a n:n h:h e:e m:m p:m i:a +sg:0 +gen:n'),
			('sg|par', 'v:v a:a n:n h:h e:e m:m p:p i:i +sg:0 +par:a'),
			('sg|ine', 'v:v a:a n:n h:h e:e m:m p:m i:a +sg:0 +ine:s 0:s 0:a'),
			('sg|ess', 'v:v a:a n:n h:h e:e m:m p:p i:a +sg:0 +ess:n 0:a'),
			('pl|nom', 'v:v a:a n:n h:h e:e m:m p:m i:a +pl:t +nom:0'),
			('pl|gen', 'v:v a:a n:n h:h e:e m:m p:p i:0 +pl:i 0:e +gen:n'),
			('pl|par', 'v:v a:a n:n h:h e:e m:m p:p i:0 +pl:i +par:a'),
			('pl|ine', 'v:v a:a n:n h:h e:e m:m p:m i:0 +pl:i +ine:s 0:s 0:a'),
		])

	def test_noun_suo(self):
		inflections = {
			"@base":  ['suo'],
			"sg|nom": ['suo'],
			"sg|gen": ['suon'],
			"sg|par": ['suota'],
			"sg|ine": ['suossa'],
			"sg|ess": ['suona'],
			"pl|nom": ['suot'],
			"pl|gen": ['soiden', 'soitten'],
			"pl|par": ['soita'],
			"pl|ine": ['soissa'],
		}
		aligned = align(inflections, pos='noun')
		self.assertEqual(aligned, [
			('@base',  's:s u:u o:o'),
			('sg|nom', 's:s u:u o:o +sg:0 +nom:0'),
			('sg|gen', 's:s u:u o:o +sg:0 +gen:n'),
			('sg|par', 's:s u:u o:o +sg:0 +par:t 0:a'),
			('sg|ine', 's:s u:u o:o +sg:0 +ine:s 0:s 0:a'),
			('sg|ess', 's:s u:u o:o +sg:0 +ess:n 0:a'),
			('pl|nom', 's:s u:u o:o +pl:t +nom:0'),
			('pl|gen', 's:s u:o o:0 +pl:i 0:d 0:e +gen:n'),
			('pl|gen', 's:s u:o o:0 +pl:i 0:t 0:t 0:e +gen:n'),
			('pl|par', 's:s u:o o:0 +pl:i +par:t 0:a'),
			('pl|ine', 's:s u:o o:0 +pl:i +ine:s 0:s 0:a'),
		])

	"""
	def test_proper_Kauniainen(self):
		inflections = {
			'@base': ['Kauniainen'],
			'@stem:possessives:nom': ['Kauniaise'],
			'@stem:possessives:gen': ['Kauniaiste', 'Kauniaisie'],
			'sg|nom': ['Kauniainen'],
			'sg|gen': ['Kauniaisten'],
			'sg|gen|rare': ['Kauniaisien'],
			'sg|acc': ['Kauniainen', 'Kauniaisen'],
			'sg|par': ['Kauniaisia'],
			'sg|ill': ['Kauniaisiin'],
			'sg|ine': ['Kauniaisissa'],
			'sg|ela': ['Kauniaisista'],
			'sg|all': ['Kauniaisille'],
			'sg|ade': ['Kauniaisilla'],
			'sg|abl': ['Kauniaisilta'],
			'sg|ess': ['Kauniaisina'],
			'sg|tra': ['Kauniaisiksi'],
			'sg|abe': ['Kauniaisitta'],
			'sg|ins': ['Kauniaisin'],
			'sg|com': ['Kauniaisine'],
		}
		aligned = align(inflections, pos='proper')
		self.assertEqual(aligned, [
			('@base',  's:s u:u o:o'),
			('sg|nom', 's:s u:u o:o +sg:0 +nom:0'),
			('sg|gen', 's:s u:u o:o +sg:0 +gen:n'),
			('sg|par', 's:s u:u o:o +sg:0 +par:t 0:a'),
			('sg|ine', 's:s u:u o:o +sg:0 +ine:s 0:s 0:a'),
			('sg|ess', 's:s u:u o:o +sg:0 +ess:n 0:a'),
			('pl|nom', 's:s u:u o:o +pl:t +nom:0'),
			('pl|gen', 's:s u:o o:0 +pl:i 0:d 0:e +gen:n'),
			('pl|gen', 's:s u:o o:0 +pl:i 0:t 0:t 0:e +gen:n'),
			('pl|par', 's:s u:o o:0 +pl:i +par:t 0:a'),
			('pl|ine', 's:s u:o o:0 +pl:i +ine:s 0:s 0:a'),
		])
	"""

	# Pluralia tantum

	def test_noun_pl_farkut(self):
		inflections = {
			"@base": ['farkut'],
			"@stem:possessives": ['farkku'],
			"nom":   ['farkut'],
			"gen":   ['farkkujen'],
			"par":   ['farkkuja'],
			"ine":   ['farkuissa'],
			"ess":   ['farkkuina'],
		}
		aligned = align(inflections, pos='noun-pl')
		self.assertEqual(aligned, [
			('@base',             'f:f a:a r:r k:k 0:0 u:u t:t'),
			('@stem:possessives', 'f:f a:a r:r k:k 0:k u:u t:0'),
			('nom',               'f:f a:a r:r k:k 0:0 u:u t:t +nom:0'),
			('gen',               'f:f a:a r:r k:k 0:k u:u t:j 0:e +gen:n'),
			('par',               'f:f a:a r:r k:k 0:k u:u t:j +par:a'),
			('ine',               'f:f a:a r:r k:k 0:0 u:u t:i +ine:s 0:s 0:a'),
			('ess',               'f:f a:a r:r k:k 0:k u:u t:i +ess:n 0:a'),
		])

	def test_noun_pl_avajaiset(self):
		inflections = {
			"@base": ['avajaiset'],
			"nom":   ['avajaiset'],
			"gen":   ['avajaisien', 'avajaisten'],
			"par":   ['avajaisia'],
			"ine":   ['avajaisissa'],
			"ess":   ['avajaisina'],
		}
		aligned = align(inflections, pos='noun-pl')
		self.assertEqual(aligned, [
			('@base', 'a:a v:v a:a j:j a:a i:i s:s e:e t:t'),
			('nom',   'a:a v:v a:a j:j a:a i:i s:s e:e t:t +nom:0'),
			('gen',   'a:a v:v a:a j:j a:a i:i s:s e:0 t:i 0:e +gen:n'),
			('gen',   'a:a v:v a:a j:j a:a i:i s:s e:0 t:t 0:e +gen:n'),
			('par',   'a:a v:v a:a j:j a:a i:i s:s e:0 t:i +par:a'),
			('ine',   'a:a v:v a:a j:j a:a i:i s:s e:0 t:i +ine:s 0:s 0:a'),
			('ess',   'a:a v:v a:a j:j a:a i:i s:s e:0 t:i +ess:n 0:a'),
		])

	def test_noun_pl_haat(self):
		inflections = {
			"@base": ['häät'],
			"nom":   ['häät'],
			"gen":   ['häiden'],
			"par":   ['häitä'],
			"ine":   ['häissä'],
			"ess":   ['häinä'],
		}
		aligned = align(inflections, pos='noun-pl')
		self.assertEqual(aligned, [
			('@base', 'h:h ä:ä ä:ä t:t'),
			('nom', 'h:h ä:ä ä:ä t:t +nom:0'),
			('gen', 'h:h ä:ä ä:0 t:i 0:d 0:e +gen:n'),
			('par', 'h:h ä:ä ä:0 t:i +par:t 0:ä'),
			('ine', 'h:h ä:ä ä:0 t:i +ine:s 0:s 0:ä'),
			('ess', 'h:h ä:ä ä:0 t:i +ess:n 0:ä'),
		])

	def test_noun_pl_lahtokuopat(self):
		inflections = {
			'@base': ['lähtö|kuopat'],
			'@stem:possessives:nom': ['lähtö|kuoppa'],
			'nom': ['lähtö|kuopat'],
			'gen': ['lähtö|kuoppien'],
			'gen|rare': ['lähtö|kuoppain'],
			'par': ['lähtö|kuoppia'],
			'ill': ['lähtö|kuoppiin'],
			'ine': ['lähtö|kuopissa'],
			'ela': ['lähtö|kuopista'],
			'all': ['lähtö|kuopille'],
			'ade': ['lähtö|kuopilla'],
			'abl': ['lähtö|kuopilta'],
			'ess': ['lähtö|kuoppina'],
			'tra': ['lähtö|kuopiksi'],
			'abe': ['lähtö|kuopitta'],
			'com': ['lähtö|kuoppine'],
			'ins': ['lähtö|kuopin'],
		}

		aligned = align(inflections, pos='noun-pl')
		self.assertEqual(aligned, [
			('@base',                  'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:0 a:a t:t'),
			('@stem:possessives:nom',  'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:p a:a t:0'),
			('nom',                    'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:0 a:a t:t +nom:0'),
			('gen',                    'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:p a:0 t:i 0:e +gen:n'),
			('gen|rare',               'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:p a:a t:i +gen:n +rare:0'),
			('par',                    'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:p a:0 t:i +par:a'),
			('ill',                    'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:p a:0 t:i +ill:i 0:n'),
			('ine',                    'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:0 a:0 t:i +ine:s 0:s 0:a'),
			('ela',                    'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:0 a:0 t:i +ela:s 0:t 0:a'),
			('all',                    'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:0 a:0 t:i +all:l 0:l 0:e'),
			('ade',                    'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:0 a:0 t:i +ade:l 0:l 0:a'),
			('abl',                    'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:0 a:0 t:i +abl:l 0:t 0:a'),
			('ess',                    'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:p a:0 t:i +ess:n 0:a'),
			('tra',                    'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:0 a:0 t:i +tra:k 0:s 0:i'),
			('abe',                    'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:0 a:0 t:i +abe:t 0:t 0:a'),
			('com',                    'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:p a:0 t:i +com:n 0:e'),
			('ins',                    'l:l ä:ä h:h t:t ö:ö |:| k:k u:u o:o p:p 0:0 a:0 t:i +ins:n'),
		])

	# Internal agreement

	def test_noun_puolipaiva(self):
		inflections = {
			'@base': ['puoli%päivä'],
			'@stem:possessives:sg:nom': ['puoli%päivä'],
			'@stem:possessives:sg:gen': ['puolen%päivä'],
			'@stem:possessives:pl:nom': ['puolet%päivä'],
			'sg|nom': ['puoli%päivä'],
			'sg|gen': ['puolen%päivän'],
			'sg|par': ['puolta%päivää'],
			'sg|ill': ['puoleen%päivään'],
			'sg|ine': ['puolessa%päivässä'],
			'sg|ela': ['puolesta%päivästä'],
			'sg|all': ['puolelle%päivälle'],
			'sg|ade': ['puolella%päivällä'],
			'sg|abl': ['puolelta%päivältä'],
			'sg|ess': ['puolena%päivänä'],
			'sg|tra': ['puoleksi%päiväksi'],
			'sg|abe': ['puoletta%päivättä'],
			'pl|nom': ['puolet%päivät'],
			'pl|gen': ['puolten%päivien', 'puolien%päivien'],
			'pl|par': ['puolia%päiviä'],
			'pl|ill': ['puoliin%päiviin'],
			'pl|ine': ['puolissa%päivissä'],
			'pl|ela': ['puolista%päivistä'],
			'pl|all': ['puolille%päiville'],
			'pl|ade': ['puolilla%päivillä'],
			'pl|abl': ['puolilta%päiviltä'],
			'pl|ess': ['puolina%päivinä'],
			'pl|tra': ['puoliksi%päiviksi'],
			'pl|abe': ['puolitta%päivittä'],
			'pl|com': ['puoline%päivine'],
			'pl|ins': ['puolin%päivin'],
		}
		aligned = align(inflections, pos='noun')
		self.assertEqual(aligned, [
			('@base',  'p:p u:u o:o l:l i:i 0:0 0:0 0:0 0:0 |:0 p:p ä:ä i:i v:v ä:ä'),
			('@stem:possessives:sg:nom', 'p:p u:u o:o l:l i:i 0:0 0:0 0:0 0:0 |:0 p:p ä:ä i:i v:v ä:ä'),
			('@stem:possessives:sg:gen', 'p:p u:u o:o l:l i:e 0:n 0:0 0:0 0:0 |:0 p:p ä:ä i:i v:v ä:ä'),
			('@stem:possessives:pl:nom', 'p:p u:u o:o l:l i:e 0:t 0:0 0:0 0:0 |:0 p:p ä:ä i:i v:v ä:ä'),
			('sg|nom', 'p:p u:u o:o l:l i:i 0:0 0:0 0:0 0:0 |:0 p:p ä:ä i:i v:v ä:ä +sg:0 +nom:0'),
			('sg|gen', 'p:p u:u o:o l:l i:e 0:0 0:n 0:0 0:0 |:0 p:p ä:ä i:i v:v ä:ä +sg:0 +gen:n'),
			('sg|par', 'p:p u:u o:o l:l i:0 0:0 0:t 0:a 0:0 |:0 p:p ä:ä i:i v:v ä:ä +sg:0 +par:ä'),
			('sg|ill', 'p:p u:u o:o l:l i:e 0:0 0:e 0:n 0:0 |:0 p:p ä:ä i:i v:v ä:ä +sg:0 +ill:ä 0:n'),
			('sg|ine', 'p:p u:u o:o l:l i:e 0:0 0:s 0:s 0:a |:0 p:p ä:ä i:i v:v ä:ä +sg:0 +ine:s 0:s 0:ä'),
			('sg|ela', 'p:p u:u o:o l:l i:e 0:0 0:s 0:t 0:a |:0 p:p ä:ä i:i v:v ä:ä +sg:0 +ela:s 0:t 0:ä'),
			('sg|all', 'p:p u:u o:o l:l i:e 0:0 0:l 0:l 0:e |:0 p:p ä:ä i:i v:v ä:ä +sg:0 +all:l 0:l 0:e'),
			('sg|ade', 'p:p u:u o:o l:l i:e 0:0 0:l 0:l 0:a |:0 p:p ä:ä i:i v:v ä:ä +sg:0 +ade:l 0:l 0:ä'),
			('sg|abl', 'p:p u:u o:o l:l i:e 0:0 0:l 0:t 0:a |:0 p:p ä:ä i:i v:v ä:ä +sg:0 +abl:l 0:t 0:ä'),
			('sg|ess', 'p:p u:u o:o l:l i:e 0:0 0:n 0:a 0:0 |:0 p:p ä:ä i:i v:v ä:ä +sg:0 +ess:n 0:ä'),
			('sg|tra', 'p:p u:u o:o l:l i:e 0:0 0:k 0:s 0:i |:0 p:p ä:ä i:i v:v ä:ä +sg:0 +tra:k 0:s 0:i'),
			('sg|abe', 'p:p u:u o:o l:l i:e 0:0 0:t 0:t 0:a |:0 p:p ä:ä i:i v:v ä:ä +sg:0 +abe:t 0:t 0:ä'),
			('pl|nom', 'p:p u:u o:o l:l i:e 0:t 0:0 0:0 0:0 |:0 p:p ä:ä i:i v:v ä:ä +pl:t +nom:0'),
			('pl|gen', 'p:p u:u o:o l:l i:0 0:t 0:e 0:n 0:0 |:0 p:p ä:ä i:i v:v ä:0 +pl:i 0:e +gen:n'),
			('pl|gen', 'p:p u:u o:o l:l i:0 0:i 0:e 0:n 0:0 |:0 p:p ä:ä i:i v:v ä:0 +pl:i 0:e +gen:n'),
			('pl|par', 'p:p u:u o:o l:l i:0 0:i 0:a 0:0 0:0 |:0 p:p ä:ä i:i v:v ä:0 +pl:i +par:ä'),
			('pl|ill', 'p:p u:u o:o l:l i:0 0:i 0:i 0:n 0:0 |:0 p:p ä:ä i:i v:v ä:0 +pl:i +ill:i 0:n'),
			('pl|ine', 'p:p u:u o:o l:l i:0 0:i 0:s 0:s 0:a |:0 p:p ä:ä i:i v:v ä:0 +pl:i +ine:s 0:s 0:ä'),
			('pl|ela', 'p:p u:u o:o l:l i:0 0:i 0:s 0:t 0:a |:0 p:p ä:ä i:i v:v ä:0 +pl:i +ela:s 0:t 0:ä'),
			('pl|all', 'p:p u:u o:o l:l i:0 0:i 0:l 0:l 0:e |:0 p:p ä:ä i:i v:v ä:0 +pl:i +all:l 0:l 0:e'),
			('pl|ade', 'p:p u:u o:o l:l i:0 0:i 0:l 0:l 0:a |:0 p:p ä:ä i:i v:v ä:0 +pl:i +ade:l 0:l 0:ä'),
			('pl|abl', 'p:p u:u o:o l:l i:0 0:i 0:l 0:t 0:a |:0 p:p ä:ä i:i v:v ä:0 +pl:i +abl:l 0:t 0:ä'),
			('pl|ess', 'p:p u:u o:o l:l i:0 0:i 0:n 0:a 0:0 |:0 p:p ä:ä i:i v:v ä:0 +pl:i +ess:n 0:ä'),
			('pl|tra', 'p:p u:u o:o l:l i:0 0:i 0:k 0:s 0:i |:0 p:p ä:ä i:i v:v ä:0 +pl:i +tra:k 0:s 0:i'),
			('pl|abe', 'p:p u:u o:o l:l i:0 0:i 0:t 0:t 0:a |:0 p:p ä:ä i:i v:v ä:0 +pl:i +abe:t 0:t 0:ä'),
			('pl|com', 'p:p u:u o:o l:l i:0 0:i 0:n 0:e 0:0 |:0 p:p ä:ä i:i v:v ä:0 +pl:i +com:n 0:e'),
			('pl|ins', 'p:p u:u o:o l:l i:0 0:i 0:n 0:0 0:0 |:0 p:p ä:ä i:i v:v ä:0 +pl:i +ins:n'),
		])

	def test_noun_isotaivot(self):
		inflections = {
			'@base': ['isot%aivot'],
			'@stem:possessives:nom': ['isot%aivo'],
			'nom': ['isot%aivot'],
			'gen': ['isojen%aivojen'],
			'par': ['isoja%aivoja'],
			'ill': ['isoihin%aivoihin'],
			'ine': ['isoissa%aivoissa'],
			'ela': ['isoista%aivoista'],
			'all': ['isoille%aivoille'],
			'ade': ['isoilla%aivoilla'],
			'abl': ['isoilta%aivoilta'],
			'ess': ['isoina%aivoina'],
			'tra': ['isoiksi%aivoiksi'],
			'abe': ['isoitta%aivoitta'],
			'com': ['isoine%aivoine'],
			'ins': ['isoin%aivoin'],
		}
		aligned = align(inflections, pos='noun-pl')
		self.assertEqual(aligned, [
			('@base', 'i:i s:s o:o t:t 0:0 0:0 0:0 |:0 a:a i:i v:v o:o t:t'),
			('@stem:possessives:nom', 'i:i s:s o:o t:t 0:0 0:0 0:0 |:0 a:a i:i v:v o:o t:0'),
			('nom',   'i:i s:s o:o t:t 0:0 0:0 0:0 |:0 a:a i:i v:v o:o t:t +nom:0'),
			('gen',   'i:i s:s o:o t:j 0:e 0:n 0:0 |:0 a:a i:i v:v o:o t:j 0:e +gen:n'),
			('par',   'i:i s:s o:o t:j 0:a 0:0 0:0 |:- a:a i:i v:v o:o t:j +par:a'),
			('ill',   'i:i s:s o:o t:i 0:h 0:i 0:n |:0 a:a i:i v:v o:o t:i +ill:h 0:i 0:n'),
			('ine',   'i:i s:s o:o t:i 0:s 0:s 0:a |:- a:a i:i v:v o:o t:i +ine:s 0:s 0:a'),
			('ela',   'i:i s:s o:o t:i 0:s 0:t 0:a |:- a:a i:i v:v o:o t:i +ela:s 0:t 0:a'),
			('all',   'i:i s:s o:o t:i 0:l 0:l 0:e |:0 a:a i:i v:v o:o t:i +all:l 0:l 0:e'),
			('ade',   'i:i s:s o:o t:i 0:l 0:l 0:a |:- a:a i:i v:v o:o t:i +ade:l 0:l 0:a'),
			('abl',   'i:i s:s o:o t:i 0:l 0:t 0:a |:- a:a i:i v:v o:o t:i +abl:l 0:t 0:a'),
			('ess',   'i:i s:s o:o t:i 0:n 0:a 0:0 |:- a:a i:i v:v o:o t:i +ess:n 0:a'),
			('tra',   'i:i s:s o:o t:i 0:k 0:s 0:i |:0 a:a i:i v:v o:o t:i +tra:k 0:s 0:i'),
			('abe',   'i:i s:s o:o t:i 0:t 0:t 0:a |:- a:a i:i v:v o:o t:i +abe:t 0:t 0:a'),
			('com',   'i:i s:s o:o t:i 0:n 0:e 0:0 |:0 a:a i:i v:v o:o t:i +com:n 0:e'),
			('ins',   'i:i s:s o:o t:i 0:n 0:0 0:0 |:0 a:a i:i v:v o:o t:i +ins:n'),
		])

	def test_noun_nuori_isanta(self):
		inflections = {
			'@base': ['nuori%isäntä'],
			'@stem:possessives:sg:nom': ['nuori%isäntä'],
			'@stem:possessives:sg:gen': ['nuoren%isäntä'],
			'@stem:possessives:pl:nom': ['nuoret%isäntä'],
			'sg|nom': ['nuori%isäntä'],
			'sg|gen': ['nuoren%isännän'],
			'sg|par': ['nuorta%isäntää'],
			'sg|ill': ['nuoreen%isäntään'],
			'sg|ine': ['nuoressa%isännässä'],
			'sg|ela': ['nuoresta%isännästä'],
			'sg|all': ['nuorelle%isännälle'],
			'sg|ade': ['nuorella%isännällä'],
			'sg|abl': ['nuorelta%isännältä'],
			'sg|ess': ['nuorena%isäntänä'],
			'sg|tra': ['nuoreksi%isännäksi'],
			'sg|abe': ['nuoretta%isännättä'],
			'pl|nom': ['nuoret%isännät'],
			'pl|gen': ['nuorten%isäntien', 'nuorien%isäntien'],
			'pl|par': ['nuoria%isäntiä'],
			'pl|ill': ['nuoriin%isäntiin'],
			'pl|ine': ['nuorissa%isännissä'],
			'pl|ela': ['nuorista%isännistä'],
			'pl|all': ['nuorille%isännille'],
			'pl|ade': ['nuorilla%isännillä'],
			'pl|abl': ['nuorilta%isänniltä'],
			'pl|ess': ['nuorina%isäntinä'],
			'pl|tra': ['nuoriksi%isänniksi'],
			'pl|abe': ['nuoritta%isännittä'],
			'pl|com': ['nuorine%isäntine'],
			'pl|ins': ['nuorin%isännin'],
		}
		aligned = align(inflections, pos='noun')
		self.assertEqual(aligned, [
			('@base',  'n:n u:u o:o r:r i:i 0:0 0:0 0:0 0:0 -:- i:i s:s ä:ä n:n t:t ä:ä'),
			('@stem:possessives:sg:nom', 'n:n u:u o:o r:r i:i 0:0 0:0 0:0 0:0 -:- i:i s:s ä:ä n:n t:t ä:ä'),
			('@stem:possessives:sg:gen', 'n:n u:u o:o r:r i:e 0:n 0:0 0:0 0:0 -:0 i:i s:s ä:ä n:n t:t ä:ä'),
			('@stem:possessives:pl:nom', 'n:n u:u o:o r:r i:e 0:t 0:0 0:0 0:0 -:0 i:i s:s ä:ä n:n t:t ä:ä'),
			('sg|nom', 'n:n u:u o:o r:r i:i 0:0 0:0 0:0 0:0 -:- i:i s:s ä:ä n:n t:t ä:ä +sg:0 +nom:0'),
			('sg|gen', 'n:n u:u o:o r:r i:e 0:0 0:n 0:0 0:0 -:0 i:i s:s ä:ä n:n t:n ä:ä +sg:0 +gen:n'),
			('sg|par', 'n:n u:u o:o r:r i:0 0:0 0:t 0:a 0:0 -:0 i:i s:s ä:ä n:n t:t ä:ä +sg:0 +par:ä'),
			('sg|ill', 'n:n u:u o:o r:r i:e 0:0 0:e 0:n 0:0 -:0 i:i s:s ä:ä n:n t:t ä:ä +sg:0 +ill:ä 0:n'),
			('sg|ine', 'n:n u:u o:o r:r i:e 0:0 0:s 0:s 0:a -:0 i:i s:s ä:ä n:n t:n ä:ä +sg:0 +ine:s 0:s 0:ä'),
			('sg|ela', 'n:n u:u o:o r:r i:e 0:0 0:s 0:t 0:a -:0 i:i s:s ä:ä n:n t:n ä:ä +sg:0 +ela:s 0:t 0:ä'),
			('sg|all', 'n:n u:u o:o r:r i:e 0:0 0:l 0:l 0:e -:0 i:i s:s ä:ä n:n t:n ä:ä +sg:0 +all:l 0:l 0:e'),
			('sg|ade', 'n:n u:u o:o r:r i:e 0:0 0:l 0:l 0:a -:0 i:i s:s ä:ä n:n t:n ä:ä +sg:0 +ade:l 0:l 0:ä'),
			('sg|abl', 'n:n u:u o:o r:r i:e 0:0 0:l 0:t 0:a -:0 i:i s:s ä:ä n:n t:n ä:ä +sg:0 +abl:l 0:t 0:ä'),
			('sg|ess', 'n:n u:u o:o r:r i:e 0:0 0:n 0:a 0:0 -:0 i:i s:s ä:ä n:n t:t ä:ä +sg:0 +ess:n 0:ä'),
			('sg|tra', 'n:n u:u o:o r:r i:e 0:0 0:k 0:s 0:i -:- i:i s:s ä:ä n:n t:n ä:ä +sg:0 +tra:k 0:s 0:i'),
			('sg|abe', 'n:n u:u o:o r:r i:e 0:0 0:t 0:t 0:a -:0 i:i s:s ä:ä n:n t:n ä:ä +sg:0 +abe:t 0:t 0:ä'),
			('pl|nom', 'n:n u:u o:o r:r i:e 0:t 0:0 0:0 0:0 -:0 i:i s:s ä:ä n:n t:n ä:ä +pl:t +nom:0'),
			('pl|gen', 'n:n u:u o:o r:r i:0 0:t 0:e 0:n 0:0 -:0 i:i s:s ä:ä n:n t:t ä:0 +pl:i 0:e +gen:n'),
			('pl|gen', 'n:n u:u o:o r:r i:0 0:i 0:e 0:n 0:0 -:0 i:i s:s ä:ä n:n t:t ä:0 +pl:i 0:e +gen:n'),
			('pl|par', 'n:n u:u o:o r:r i:0 0:i 0:a 0:0 0:0 -:0 i:i s:s ä:ä n:n t:t ä:0 +pl:i +par:ä'),
			('pl|ill', 'n:n u:u o:o r:r i:0 0:i 0:i 0:n 0:0 -:0 i:i s:s ä:ä n:n t:t ä:0 +pl:i +ill:i 0:n'),
			('pl|ine', 'n:n u:u o:o r:r i:0 0:i 0:s 0:s 0:a -:0 i:i s:s ä:ä n:n t:n ä:0 +pl:i +ine:s 0:s 0:ä'),
			('pl|ela', 'n:n u:u o:o r:r i:0 0:i 0:s 0:t 0:a -:0 i:i s:s ä:ä n:n t:n ä:0 +pl:i +ela:s 0:t 0:ä'),
			('pl|all', 'n:n u:u o:o r:r i:0 0:i 0:l 0:l 0:e -:0 i:i s:s ä:ä n:n t:n ä:0 +pl:i +all:l 0:l 0:e'),
			('pl|ade', 'n:n u:u o:o r:r i:0 0:i 0:l 0:l 0:a -:0 i:i s:s ä:ä n:n t:n ä:0 +pl:i +ade:l 0:l 0:ä'),
			('pl|abl', 'n:n u:u o:o r:r i:0 0:i 0:l 0:t 0:a -:0 i:i s:s ä:ä n:n t:n ä:0 +pl:i +abl:l 0:t 0:ä'),
			('pl|ess', 'n:n u:u o:o r:r i:0 0:i 0:n 0:a 0:0 -:0 i:i s:s ä:ä n:n t:t ä:0 +pl:i +ess:n 0:ä'),
			('pl|tra', 'n:n u:u o:o r:r i:0 0:i 0:k 0:s 0:i -:- i:i s:s ä:ä n:n t:n ä:0 +pl:i +tra:k 0:s 0:i'),
			('pl|abe', 'n:n u:u o:o r:r i:0 0:i 0:t 0:t 0:a -:0 i:i s:s ä:ä n:n t:n ä:0 +pl:i +abe:t 0:t 0:ä'),
			('pl|com', 'n:n u:u o:o r:r i:0 0:i 0:n 0:e 0:0 -:0 i:i s:s ä:ä n:n t:t ä:0 +pl:i +com:n 0:e'),
			('pl|ins', 'n:n u:u o:o r:r i:0 0:i 0:n 0:0 0:0 -:0 i:i s:s ä:ä n:n t:n ä:0 +pl:i +ins:n'),
		])

	def test_noun_Papua_Uusi_Guinea(self):
		inflections = {
			'@base': ['Papua-Uusi%-Guinea'],
			'@stem:possessives:sg:nom': ['Papua-Uusi%-Guinea'],
			'@stem:possessives:sg:gen': ['Papua-Uuden%-Guinea'],
			'@stem:possessives:pl:nom': ['Papua-Uudet%-Guinea'],
			'sg|nom': ['Papua-Uusi%-Guinea'],
			'sg|gen': ['Papua-Uuden%-Guinean'],
			'sg|par': ['Papua-Uutta%-Guineaa'],
			'sg|ill': ['Papua-Uuteen%-Guineaan'],
			'sg|ine': ['Papua-Uudessa%-Guineassa'],
			'sg|ela': ['Papua-Uudesta%-Guineasta'],
			'sg|all': ['Papua-Uudelle%-Guinealle'],
			'sg|ade': ['Papua-Uudella%-Guinealla'],
			'sg|abl': ['Papua-Uudelta%-Guinealta'],
			'sg|ess': ['Papua-Uutena%-Guineana'],
			'sg|tra': ['Papua-Uudeksi%-Guineaksi'],
			'sg|abe': ['Papua-Uudetta%-Guineatta'],
			'pl|nom': ['Papua-Uudet%-Guineat'],
			'pl|gen': ['Papua-Uusien%-Guineoiden', 'Papua-Uusien%-Guineoitten'],
			'pl|gen|rare': ['Papua-Uutten%-Guineain'],
			'pl|par': ['Papua-Uusia%-Guineoita'],
			'pl|ill': ['Papua-Uusiin%-Guineoihin'],
			'pl|ine': ['Papua-Uusissa%-Guineoissa'],
			'pl|ela': ['Papua-Uusista%-Guineoista'],
			'pl|all': ['Papua-Uusille%-Guineoille'],
			'pl|ade': ['Papua-Uusilla%-Guineoilla'],
			'pl|abl': ['Papua-Uusilta%-Guineoilta'],
			'pl|ess': ['Papua-Uusina%-Guineoina'],
			'pl|tra': ['Papua-Uusiksi%-Guineoiksi'],
			'pl|abe': ['Papua-Uusitta%-Guineoitta'],
			'pl|com': ['Papua-Uusine%-Guineoine'],
			'pl|ins': ['Papua-Uusin%-Guineoin'],
			'@stem:clitics': ['Papua-Uusi%-Guinea'],
		}
		aligned = align(inflections, pos='proper')
		self.assertEqual(aligned, [
			('@base',                    'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:i 0:0 0:0 0:0 0:0 -:- G:G u:u i:i n:n e:e a:a'),
			('@stem:possessives:sg:nom', 'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:i 0:0 0:0 0:0 0:0 -:- G:G u:u i:i n:n e:e a:a'),
			('@stem:possessives:sg:gen', 'P:P a:a p:p u:u a:a -:- U:U u:u s:d i:e 0:n 0:0 0:0 0:0 -:- G:G u:u i:i n:n e:e a:a'),
			('@stem:possessives:pl:nom', 'P:P a:a p:p u:u a:a -:- U:U u:u s:d i:e 0:t 0:0 0:0 0:0 -:- G:G u:u i:i n:n e:e a:a'),
			('sg|nom',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:i 0:0 0:0 0:0 0:0 -:- G:G u:u i:i n:n e:e a:a +sg:0 +nom:0'),
			('sg|gen',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:d i:e 0:0 0:n 0:0 0:0 -:- G:G u:u i:i n:n e:e a:a +sg:0 +gen:n'),
			('sg|par',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:t i:0 0:0 0:t 0:a 0:0 -:- G:G u:u i:i n:n e:e a:a +sg:0 +par:a'),
			('sg|ill',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:t i:e 0:0 0:e 0:n 0:0 -:- G:G u:u i:i n:n e:e a:a +sg:0 +ill:a 0:n'),
			('sg|ine',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:d i:e 0:0 0:s 0:s 0:a -:- G:G u:u i:i n:n e:e a:a +sg:0 +ine:s 0:s 0:a'),
			('sg|ela',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:d i:e 0:0 0:s 0:t 0:a -:- G:G u:u i:i n:n e:e a:a +sg:0 +ela:s 0:t 0:a'),
			('sg|all',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:d i:e 0:0 0:l 0:l 0:e -:- G:G u:u i:i n:n e:e a:a +sg:0 +all:l 0:l 0:e'),
			('sg|ade',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:d i:e 0:0 0:l 0:l 0:a -:- G:G u:u i:i n:n e:e a:a +sg:0 +ade:l 0:l 0:a'),
			('sg|abl',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:d i:e 0:0 0:l 0:t 0:a -:- G:G u:u i:i n:n e:e a:a +sg:0 +abl:l 0:t 0:a'),
			('sg|ess',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:t i:e 0:0 0:n 0:a 0:0 -:- G:G u:u i:i n:n e:e a:a +sg:0 +ess:n 0:a'),
			('sg|tra',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:d i:e 0:0 0:k 0:s 0:i -:- G:G u:u i:i n:n e:e a:a +sg:0 +tra:k 0:s 0:i'),
			('sg|abe',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:d i:e 0:0 0:t 0:t 0:a -:- G:G u:u i:i n:n e:e a:a +sg:0 +abe:t 0:t 0:a'),
			('pl|nom',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:d i:e 0:t 0:0 0:0 0:0 -:- G:G u:u i:i n:n e:e a:a +pl:t +nom:0'),
			('pl|gen',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:0 0:i 0:e 0:n 0:0 -:- G:G u:u i:i n:n e:e a:o +pl:i 0:d 0:e +gen:n'),
			('pl|gen',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:0 0:i 0:e 0:n 0:0 -:- G:G u:u i:i n:n e:e a:o +pl:i 0:t 0:t 0:e +gen:n'),
			('pl|gen|rare',              'P:P a:a p:p u:u a:a -:- U:U u:u s:t i:0 0:t 0:e 0:n 0:0 -:- G:G u:u i:i n:n e:e a:a +pl:i +gen:n +rare:0'),
			('pl|par',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:0 0:i 0:a 0:0 0:0 -:- G:G u:u i:i n:n e:e a:o +pl:i +par:t 0:a'),
			('pl|ill',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:0 0:i 0:i 0:n 0:0 -:- G:G u:u i:i n:n e:e a:o +pl:i +ill:h 0:i 0:n'),
			('pl|ine',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:0 0:i 0:s 0:s 0:a -:- G:G u:u i:i n:n e:e a:o +pl:i +ine:s 0:s 0:a'),
			('pl|ela',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:0 0:i 0:s 0:t 0:a -:- G:G u:u i:i n:n e:e a:o +pl:i +ela:s 0:t 0:a'),
			('pl|all',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:0 0:i 0:l 0:l 0:e -:- G:G u:u i:i n:n e:e a:o +pl:i +all:l 0:l 0:e'),
			('pl|ade',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:0 0:i 0:l 0:l 0:a -:- G:G u:u i:i n:n e:e a:o +pl:i +ade:l 0:l 0:a'),
			('pl|abl',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:0 0:i 0:l 0:t 0:a -:- G:G u:u i:i n:n e:e a:o +pl:i +abl:l 0:t 0:a'),
			('pl|ess',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:0 0:i 0:n 0:a 0:0 -:- G:G u:u i:i n:n e:e a:o +pl:i +ess:n 0:a'),
			('pl|tra',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:0 0:i 0:k 0:s 0:i -:- G:G u:u i:i n:n e:e a:o +pl:i +tra:k 0:s 0:i'),
			('pl|abe',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:0 0:i 0:t 0:t 0:a -:- G:G u:u i:i n:n e:e a:o +pl:i +abe:t 0:t 0:a'),
			('pl|com',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:0 0:i 0:n 0:e 0:0 -:- G:G u:u i:i n:n e:e a:o +pl:i +com:n 0:e'),
			('pl|ins',                   'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:0 0:i 0:n 0:0 0:0 -:- G:G u:u i:i n:n e:e a:o +pl:i +ins:n'),
			('@stem:clitics',            'P:P a:a p:p u:u a:a -:- U:U u:u s:s i:i 0:0 0:0 0:0 0:0 -:- G:G u:u i:i n:n e:e a:a'),
		])

	def test_noun_mustaviinimarja(self):
		inflections = {
			'@base': ['musta%viini|marja'],
			'@stem:possessives:sg:nom': ['musta%viini|marja'],
			'@stem:possessives:sg:gen': ['mustan%viini|marja'],
			'@stem:possessives:pl:nom': ['mustat%viini|marja'],
			'sg|nom': ['musta%viini|marja'],
			'sg|gen': ['mustan%viini|marjan'],
			'sg|par': ['mustaa%viini|marjaa'],
			'sg|ill': ['mustaan%viini|marjaan'],
			'sg|ine': ['mustassa%viini|marjassa'],
			'sg|ela': ['mustasta%viini|marjasta'],
			'sg|all': ['mustalle%viini|marjalle'],
			'sg|ade': ['mustalla%viini|marjalla'],
			'sg|abl': ['mustalta%viini|marjalta'],
			'sg|ess': ['mustana%viini|marjana'],
			'sg|tra': ['mustaksi%viini|marjaksi'],
			'sg|abe': ['mustatta%viini|marjatta'],
			'pl|nom': ['mustat%viini|marjat'],
			'pl|gen': ['mustien%viini|marjojen'],
			'pl|gen|rare': ['mustain%viini|marjain'],
			'pl|par': ['mustia%viini|marjoja'],
			'pl|ill': ['mustiin%viini|marjoihin'],
			'pl|ine': ['mustissa%viini|marjoissa'],
			'pl|ela': ['mustista%viini|marjoista'],
			'pl|all': ['mustille%viini|marjoille'],
			'pl|ade': ['mustilla%viini|marjoilla'],
			'pl|abl': ['mustilta%viini|marjoilta'],
			'pl|ess': ['mustina%viini|marjoina'],
			'pl|tra': ['mustiksi%viini|marjoiksi'],
			'pl|abe': ['mustitta%viini|marjoitta'],
			'pl|com': ['mustine%viini|marjoine'],
			'pl|ins': ['mustin%viini|marjoin'],
		}

		aligned = align(inflections, pos='noun')
		self.assertEqual(aligned, [
			('@base',                    'm:m u:u s:s t:t a:a 0:0 0:0 0:0 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a'),
			('@stem:possessives:sg:nom', 'm:m u:u s:s t:t a:a 0:0 0:0 0:0 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a'),
			('@stem:possessives:sg:gen', 'm:m u:u s:s t:t a:a 0:n 0:0 0:0 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a'),
			('@stem:possessives:pl:nom', 'm:m u:u s:s t:t a:a 0:t 0:0 0:0 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a'),
			('sg|nom',                   'm:m u:u s:s t:t a:a 0:0 0:0 0:0 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a +sg:0 +nom:0'),
			('sg|gen',                   'm:m u:u s:s t:t a:a 0:0 0:n 0:0 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a +sg:0 +gen:n'),
			('sg|par',                   'm:m u:u s:s t:t a:a 0:0 0:a 0:0 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a +sg:0 +par:a'),
			('sg|ill',                   'm:m u:u s:s t:t a:a 0:0 0:a 0:n 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a +sg:0 +ill:a 0:n'),
			('sg|ine',                   'm:m u:u s:s t:t a:a 0:0 0:s 0:s 0:a |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a +sg:0 +ine:s 0:s 0:a'),
			('sg|ela',                   'm:m u:u s:s t:t a:a 0:0 0:s 0:t 0:a |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a +sg:0 +ela:s 0:t 0:a'),
			('sg|all',                   'm:m u:u s:s t:t a:a 0:0 0:l 0:l 0:e |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a +sg:0 +all:l 0:l 0:e'),
			('sg|ade',                   'm:m u:u s:s t:t a:a 0:0 0:l 0:l 0:a |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a +sg:0 +ade:l 0:l 0:a'),
			('sg|abl',                   'm:m u:u s:s t:t a:a 0:0 0:l 0:t 0:a |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a +sg:0 +abl:l 0:t 0:a'),
			('sg|ess',                   'm:m u:u s:s t:t a:a 0:0 0:n 0:a 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a +sg:0 +ess:n 0:a'),
			('sg|tra',                   'm:m u:u s:s t:t a:a 0:0 0:k 0:s 0:i |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a +sg:0 +tra:k 0:s 0:i'),
			('sg|abe',                   'm:m u:u s:s t:t a:a 0:0 0:t 0:t 0:a |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a +sg:0 +abe:t 0:t 0:a'),
			('pl|nom',                   'm:m u:u s:s t:t a:a 0:t 0:0 0:0 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a +pl:t +nom:0'),
			('pl|gen',                   'm:m u:u s:s t:t a:0 0:i 0:e 0:n 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:o +pl:j 0:e +gen:n'),
			('pl|gen|rare',              'm:m u:u s:s t:t a:a 0:i 0:n 0:0 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:a +pl:i +gen:n +rare:0'),
			('pl|par',                   'm:m u:u s:s t:t a:0 0:i 0:a 0:0 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:o +pl:j +par:a'),
			('pl|ill',                   'm:m u:u s:s t:t a:0 0:i 0:i 0:n 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:o +pl:i +ill:h 0:i 0:n'),
			('pl|ine',                   'm:m u:u s:s t:t a:0 0:i 0:s 0:s 0:a |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:o +pl:i +ine:s 0:s 0:a'),
			('pl|ela',                   'm:m u:u s:s t:t a:0 0:i 0:s 0:t 0:a |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:o +pl:i +ela:s 0:t 0:a'),
			('pl|all',                   'm:m u:u s:s t:t a:0 0:i 0:l 0:l 0:e |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:o +pl:i +all:l 0:l 0:e'),
			('pl|ade',                   'm:m u:u s:s t:t a:0 0:i 0:l 0:l 0:a |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:o +pl:i +ade:l 0:l 0:a'),
			('pl|abl',                   'm:m u:u s:s t:t a:0 0:i 0:l 0:t 0:a |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:o +pl:i +abl:l 0:t 0:a'),
			('pl|ess',                   'm:m u:u s:s t:t a:0 0:i 0:n 0:a 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:o +pl:i +ess:n 0:a'),
			('pl|tra',                   'm:m u:u s:s t:t a:0 0:i 0:k 0:s 0:i |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:o +pl:i +tra:k 0:s 0:i'),
			('pl|abe',                   'm:m u:u s:s t:t a:0 0:i 0:t 0:t 0:a |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:o +pl:i +abe:t 0:t 0:a'),
			('pl|com',                   'm:m u:u s:s t:t a:0 0:i 0:n 0:e 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:o +pl:i +com:n 0:e'),
			('pl|ins',                   'm:m u:u s:s t:t a:0 0:i 0:n 0:0 0:0 |:0 v:v i:i i:i n:n i:i |:0 m:m a:a r:r j:j a:o +pl:i +ins:n'),
		])

	def test_noun_Pienet_Antillit(self):
		inflections = {
			'@base': ['Pienet%-Antillit'],
			'@stem:possessives:nom': ['Pienet%-Antilli'],
			'nom': ['Pienet%-Antillit'],
			'gen': ['Pienten%-Antilleiden', 'Pienten%-Antilleitten', 'Pienten%-Antillien', 'Pienien%-Antilleiden', 'Pienien%-Antilleitten', 'Pienien%-Antillien'],
			'par': ['Pieniä%-Antilleita', 'Pieniä%-Antilleja'],
			'ill': ['Pieniin%-Antilleihin'],
			'ine': ['Pienissä%-Antilleissa'],
			'ela': ['Pienistä%-Antilleista'],
			'all': ['Pienille%-Antilleille'],
			'ade': ['Pienillä%-Antilleilla'],
			'abl': ['Pieniltä%-Antilleilta'],
			'ess': ['Pieninä%-Antilleina'],
			'tra': ['Pieniksi%-Antilleiksi'],
			'abe': ['Pienittä%-Antilleitta'],
			'com': ['Pienine%-Antilleine'],
			'ins': ['Pienin%-Antillein'],
		}
		aligned = align(inflections, pos='proper-pl')
		self.assertEqual(aligned, [
			('@base',                    'P:P i:i e:e n:n e:e t:t 0:0 0:0 0:0 -:- A:A n:n t:t i:i l:l l:l i:i t:t'),
			('@stem:possessives:nom',    'P:P i:i e:e n:n e:e t:t 0:0 0:0 0:0 -:- A:A n:n t:t i:i l:l l:l i:i t:0'),
			('nom',                      'P:P i:i e:e n:n e:e t:t 0:0 0:0 0:0 -:- A:A n:n t:t i:i l:l l:l i:i t:t +nom:0'),
			('gen',                      'P:P i:i e:e n:n e:0 t:t 0:e 0:n 0:0 -:- A:A n:n t:t i:i l:l l:l i:e t:i 0:d 0:e +gen:n'),
			('gen',                      'P:P i:i e:e n:n e:0 t:t 0:e 0:n 0:0 -:- A:A n:n t:t i:i l:l l:l i:e t:i 0:t 0:t 0:e +gen:n'),
			('gen',                      'P:P i:i e:e n:n e:0 t:t 0:e 0:n 0:0 -:- A:A n:n t:t i:i l:l l:l i:0 t:i 0:e +gen:n'),
			('gen',                      'P:P i:i e:e n:n e:0 t:i 0:e 0:n 0:0 -:- A:A n:n t:t i:i l:l l:l i:e t:i 0:d 0:e +gen:n'),
			('gen',                      'P:P i:i e:e n:n e:0 t:i 0:e 0:n 0:0 -:- A:A n:n t:t i:i l:l l:l i:e t:i 0:t 0:t 0:e +gen:n'),
			('gen',                      'P:P i:i e:e n:n e:0 t:i 0:e 0:n 0:0 -:- A:A n:n t:t i:i l:l l:l i:0 t:i 0:e +gen:n'),
			('par',                      'P:P i:i e:e n:n e:0 t:i 0:ä 0:0 0:0 -:- A:A n:n t:t i:i l:l l:l i:e t:i +par:t 0:a'),
			('par',                      'P:P i:i e:e n:n e:0 t:i 0:ä 0:0 0:0 -:- A:A n:n t:t i:i l:l l:l i:e t:j +par:a'),
			('ill',                      'P:P i:i e:e n:n e:0 t:i 0:i 0:n 0:0 -:- A:A n:n t:t i:i l:l l:l i:e t:i +ill:h 0:i 0:n'),
			('ine',                      'P:P i:i e:e n:n e:0 t:i 0:s 0:s 0:ä -:- A:A n:n t:t i:i l:l l:l i:e t:i +ine:s 0:s 0:a'),
			('ela',                      'P:P i:i e:e n:n e:0 t:i 0:s 0:t 0:ä -:- A:A n:n t:t i:i l:l l:l i:e t:i +ela:s 0:t 0:a'),
			('all',                      'P:P i:i e:e n:n e:0 t:i 0:l 0:l 0:e -:- A:A n:n t:t i:i l:l l:l i:e t:i +all:l 0:l 0:e'),
			('ade',                      'P:P i:i e:e n:n e:0 t:i 0:l 0:l 0:ä -:- A:A n:n t:t i:i l:l l:l i:e t:i +ade:l 0:l 0:a'),
			('abl',                      'P:P i:i e:e n:n e:0 t:i 0:l 0:t 0:ä -:- A:A n:n t:t i:i l:l l:l i:e t:i +abl:l 0:t 0:a'),
			('ess',                      'P:P i:i e:e n:n e:0 t:i 0:n 0:ä 0:0 -:- A:A n:n t:t i:i l:l l:l i:e t:i +ess:n 0:a'),
			('tra',                      'P:P i:i e:e n:n e:0 t:i 0:k 0:s 0:i -:- A:A n:n t:t i:i l:l l:l i:e t:i +tra:k 0:s 0:i'),
			('abe',                      'P:P i:i e:e n:n e:0 t:i 0:t 0:t 0:ä -:- A:A n:n t:t i:i l:l l:l i:e t:i +abe:t 0:t 0:a'),
			('com',                      'P:P i:i e:e n:n e:0 t:i 0:n 0:e 0:0 -:- A:A n:n t:t i:i l:l l:l i:e t:i +com:n 0:e'),
			('ins',                      'P:P i:i e:e n:n e:0 t:i 0:n 0:0 0:0 -:- A:A n:n t:t i:i l:l l:l i:e t:i +ins:n'),
		])

	# Adjectives

	def test_adjective_suolainen(self):
		inflections = {
			"@base":  ['suolainen'],
			"sg|nom": ['suolainen'],
			"sg|gen": ['suolaisen'],
			"sg|par": ['suolaista'],
			"sg|ine": ['suolaisessa'],
			"sg|ess": ['suolaisena'],
			"pl|nom": ['suolaiset'],
			"pl|gen": ['suolaisien', 'suolaisten'],
			"pl|par": ['suolaisia'],
			"pl|ine": ['suolaisissa'],
			"comparative": ['suolaisempi'],
			"superlative": ['suolaisin'],
		}
		aligned = align(inflections, pos='adjective')
		self.assertEqual(aligned, [
			('@base',       's:s u:u o:o l:l a:a i:i n:n e:e n:n'),
			('sg|nom',      's:s u:u o:o l:l a:a i:i n:n e:e n:n +sg:0 +nom:0'),
			('sg|gen',      's:s u:u o:o l:l a:a i:i n:s e:e n:0 +sg:0 +gen:n'),
			('sg|par',      's:s u:u o:o l:l a:a i:i n:s e:0 n:0 +sg:0 +par:t 0:a'),
			('sg|ine',      's:s u:u o:o l:l a:a i:i n:s e:e n:0 +sg:0 +ine:s 0:s 0:a'),
			('sg|ess',      's:s u:u o:o l:l a:a i:i n:s e:e n:0 +sg:0 +ess:n 0:a'),
			('pl|nom',      's:s u:u o:o l:l a:a i:i n:s e:e n:0 +pl:t +nom:0'),
			('pl|gen',      's:s u:u o:o l:l a:a i:i n:s e:0 n:0 +pl:i 0:e +gen:n'),
			('pl|gen',      's:s u:u o:o l:l a:a i:i n:s e:0 n:0 +pl:t 0:e +gen:n'),
			('pl|par',      's:s u:u o:o l:l a:a i:i n:s e:0 n:0 +pl:i +par:a'),
			('pl|ine',      's:s u:u o:o l:l a:a i:i n:s e:0 n:0 +pl:i +ine:s 0:s 0:a'),
			('comparative', 's:s u:u o:o l:l a:a i:i n:s e:e n:0 +comparative:m 0:p 0:i'),
			('superlative', 's:s u:u o:o l:l a:a i:i n:s e:0 n:0 +superlative:i 0:n'),
		])

	def test_adjective_kuiva(self):
		inflections = {
			"@base":  ['kuiva'],
			"sg|nom": ['kuiva'],
			"sg|gen": ['kuivan'],
			"sg|par": ['kuivaa'],
			"sg|ine": ['kuivassa'],
			"sg|ess": ['kuivana'],
			"pl|nom": ['kuivat'],
			"pl|gen": ['kuivien'],
			"pl|gen|rare": ['kuivain'],
			"pl|par": ['kuivia'],
			"pl|ine": ['kuivissa'],
			"comparative": ['kuivempi'],
			"superlative": ['kuivin'],
		}
		aligned = align(inflections, pos='adjective')
		self.assertEqual(aligned, [
			('@base',       'k:k u:u i:i v:v a:a'),
			('sg|nom',      'k:k u:u i:i v:v a:a +sg:0 +nom:0'),
			('sg|gen',      'k:k u:u i:i v:v a:a +sg:0 +gen:n'),
			('sg|par',      'k:k u:u i:i v:v a:a +sg:0 +par:a'),
			('sg|ine',      'k:k u:u i:i v:v a:a +sg:0 +ine:s 0:s 0:a'),
			('sg|ess',      'k:k u:u i:i v:v a:a +sg:0 +ess:n 0:a'),
			('pl|nom',      'k:k u:u i:i v:v a:a +pl:t +nom:0'),
			('pl|gen',      'k:k u:u i:i v:v a:0 +pl:i 0:e +gen:n'),
			('pl|gen|rare', 'k:k u:u i:i v:v a:a +pl:i +gen:n +rare:0'),
			('pl|par',      'k:k u:u i:i v:v a:0 +pl:i +par:a'),
			('pl|ine',      'k:k u:u i:i v:v a:0 +pl:i +ine:s 0:s 0:a'),
			('comparative', 'k:k u:u i:i v:v a:e +comparative:m 0:p 0:i'),
			('superlative', 'k:k u:u i:i v:v a:0 +superlative:i 0:n'),

		])

	def test_adjective_kuollut(self):
		inflections = {
			"@base":  ['kuollut'],
			"sg|nom": ['kuollut'],
			"sg|gen": ['kuolleen'],
			"sg|par": ['kuollutta'],
			"sg|ine": ['kuolleessa'],
			"sg|ess": ['kuolleena'],
			"pl|nom": ['kuolleet'],
			"pl|gen": ['kuolleiden', 'kuolleitten'],
			"pl|par": ['kuolleita'],
			"pl|ine": ['kuolleissa'],
			"comparative": ['kuolleempi'],
			"superlative": ['kuollein'],
		}
		aligned = align(inflections, pos='adjective')
		self.assertEqual(aligned, [
			('@base',       'k:k u:u o:o l:l l:l u:u t:t 0:0'),
			('sg|nom',      'k:k u:u o:o l:l l:l u:u t:t 0:0 +sg:0 +nom:0'),
			('sg|gen',      'k:k u:u o:o l:l l:l u:e t:0 0:e +sg:0 +gen:n'),
			('sg|par',      'k:k u:u o:o l:l l:l u:u t:t 0:0 +sg:0 +par:t 0:a'),
			('sg|ine',      'k:k u:u o:o l:l l:l u:e t:0 0:e +sg:0 +ine:s 0:s 0:a'),
			('sg|ess',      'k:k u:u o:o l:l l:l u:e t:0 0:e +sg:0 +ess:n 0:a'),
			('pl|nom',      'k:k u:u o:o l:l l:l u:e t:0 0:e +pl:t +nom:0'),
			('pl|gen',      'k:k u:u o:o l:l l:l u:e t:0 0:0 +pl:i 0:d 0:e +gen:n'),
			('pl|gen',      'k:k u:u o:o l:l l:l u:e t:0 0:0 +pl:i 0:t 0:t 0:e +gen:n'),
			('pl|par',      'k:k u:u o:o l:l l:l u:e t:0 0:0 +pl:i +par:t 0:a'),
			('pl|ine',      'k:k u:u o:o l:l l:l u:e t:0 0:0 +pl:i +ine:s 0:s 0:a'),
			('comparative', 'k:k u:u o:o l:l l:l u:e t:0 0:e +comparative:m 0:p 0:i'),
			('superlative', 'k:k u:u o:o l:l l:l u:e t:0 0:0 +superlative:i 0:n'),
		])

	def test_adjective_hyva(self):
		inflections = {
			"@base":  ['hyvä'],
			"sg|nom": ['hyvä'],
			"sg|gen": ['hyvän'],
			"sg|par": ['hyvää'],
			"sg|ine": ['hyvässä'],
			"sg|ess": ['hyvänä'],
			"pl|nom": ['hyvät'],
			"pl|gen": ['hyvien'],
			"pl|gen|rare": ['hyväin'],
			"pl|par": ['hyviä'],
			"pl|ine": ['hyvissä'],
			"comparative": ['parempi'],
			"superlative": ['paras'],
		}
		aligned = align(inflections, pos='adjective')
		self.assertEqual(aligned, [
			('@base',       'h:h y:y v:v ä:ä'),
			('sg|nom',      'h:h y:y v:v ä:ä +sg:0 +nom:0'),
			('sg|gen',      'h:h y:y v:v ä:ä +sg:0 +gen:n'),
			('sg|par',      'h:h y:y v:v ä:ä +sg:0 +par:ä'),
			('sg|ine',      'h:h y:y v:v ä:ä +sg:0 +ine:s 0:s 0:ä'),
			('sg|ess',      'h:h y:y v:v ä:ä +sg:0 +ess:n 0:ä'),
			('pl|nom',      'h:h y:y v:v ä:ä +pl:t +nom:0'),
			('pl|gen',      'h:h y:y v:v ä:0 +pl:i 0:e +gen:n'),
			('pl|gen|rare', 'h:h y:y v:v ä:ä +pl:i +gen:n +rare:0'),
			('pl|par',      'h:h y:y v:v ä:0 +pl:i +par:ä'),
			('pl|ine',      'h:h y:y v:v ä:0 +pl:i +ine:s 0:s 0:ä'),
			('comparative', 'h:p y:a v:r ä:e +comparative:m 0:p 0:i'),
			('superlative', 'h:p y:a v:r ä:a +superlative:s'),
		])

	def test_adjective_hapan(self):
		inflections = {
			"@base":  ['hapan'],
			"sg|nom": ['hapan'],
			"sg|gen": ['happaman', 'happamen'],
			"sg|par": ['hapanta', 'happamaa'],
			"sg|ine": ['happamassa', 'happamessa'],
			"sg|ess": ['happamana', 'happamena'],
			"pl|nom": ['happamat', 'happamet'],
			"pl|gen": ['happamien', 'hapanten'],
			"pl|par": ['happamia'],
			"pl|ine": ['happamissa'],
			"comparative": ['happamampi', 'happamempi'],
			"superlative": ['happamin'],
		}
		aligned = align(inflections, pos='adjective')
		self.assertEqual(aligned, [
			('@base',       'h:h a:a p:p 0:0 a:a n:n 0:0'),
			('sg|nom',      'h:h a:a p:p 0:0 a:a n:n 0:0 +sg:0 +nom:0'),
			('sg|gen',      'h:h a:a p:p 0:p a:a n:m 0:a +sg:0 +gen:n'),
			('sg|gen',      'h:h a:a p:p 0:p a:a n:m 0:e +sg:0 +gen:n'),
			('sg|par',      'h:h a:a p:p 0:0 a:a n:n 0:0 +sg:0 +par:t 0:a'),
			('sg|par',      'h:h a:a p:p 0:p a:a n:m 0:a +sg:0 +par:a'),
			('sg|ine',      'h:h a:a p:p 0:p a:a n:m 0:a +sg:0 +ine:s 0:s 0:a'),
			('sg|ine',      'h:h a:a p:p 0:p a:a n:m 0:e +sg:0 +ine:s 0:s 0:a'),
			('sg|ess',      'h:h a:a p:p 0:p a:a n:m 0:a +sg:0 +ess:n 0:a'),
			('sg|ess',      'h:h a:a p:p 0:p a:a n:m 0:e +sg:0 +ess:n 0:a'),
			('pl|nom',      'h:h a:a p:p 0:p a:a n:m 0:a +pl:t +nom:0'),
			('pl|nom',      'h:h a:a p:p 0:p a:a n:m 0:e +pl:t +nom:0'),
			('pl|gen',      'h:h a:a p:p 0:p a:a n:m 0:0 +pl:i 0:e +gen:n'),
			('pl|gen',      'h:h a:a p:p 0:0 a:a n:n 0:0 +pl:t 0:e +gen:n'),
			('pl|par',      'h:h a:a p:p 0:p a:a n:m 0:0 +pl:i +par:a'),
			('pl|ine',      'h:h a:a p:p 0:p a:a n:m 0:0 +pl:i +ine:s 0:s 0:a'),
			('comparative', 'h:h a:a p:p 0:p a:a n:m 0:a +comparative:m 0:p 0:i'),
			('comparative', 'h:h a:a p:p 0:p a:a n:m 0:e +comparative:m 0:p 0:i'),
			('superlative', 'h:h a:a p:p 0:p a:a n:m 0:0 +superlative:i 0:n'),
		])

	# Numerals

	def test_numeral_kaksi(self):
		inflections = {
			"@base":  ['kaksi'],
			"sg|nom": ['kaksi'],
			"sg|gen": ['kahden'],
			"sg|par": ['kahta'],
			"sg|ine": ['kahdessa'],
			"sg|ess": ['kahtena'],
			"pl|nom": ['kahdet'],
			"pl|gen": ['kaksien'],
			"pl|par": ['kaksia'],
			"pl|ine": ['kaksissa'],
		}
		aligned = align(inflections, pos='numeral')
		self.assertEqual(aligned, [
			('@base',  'k:k a:a k:k s:s i:i'),
			('sg|nom', 'k:k a:a k:k s:s i:i +sg:0 +nom:0'),
			('sg|gen', 'k:k a:a k:h s:d i:e +sg:0 +gen:n'),
			('sg|par', 'k:k a:a k:h s:0 i:0 +sg:0 +par:t 0:a'),
			('sg|ine', 'k:k a:a k:h s:d i:e +sg:0 +ine:s 0:s 0:a'),
			('sg|ess', 'k:k a:a k:h s:t i:e +sg:0 +ess:n 0:a'),
			('pl|nom', 'k:k a:a k:h s:d i:e +pl:t +nom:0'),
			('pl|gen', 'k:k a:a k:k s:s i:0 +pl:i 0:e +gen:n'),
			('pl|par', 'k:k a:a k:k s:s i:0 +pl:i +par:a'),
			('pl|ine', 'k:k a:a k:k s:s i:0 +pl:i +ine:s 0:s 0:a'),
		])

	def test_numeral_tuhat(self):
		inflections = {
			"@base":  ['tuhat'],
			"sg|nom": ['tuhat'],
			"sg|gen": ['tuhannen'],
			"sg|par": ['tuhatta'],
			"sg|ine": ['tuhannessa'],
			"sg|ess": ['tuhantena'],
			"pl|nom": ['tuhannet'],
			"pl|gen": ['tuhansien', 'tuhanten'],
			"pl|par": ['tuhansia'],
			"pl|ine": ['tuhansissa'],
		}
		aligned = align(inflections, pos='numeral')
		self.assertEqual(aligned, [
			('@base',  't:t u:u h:h a:a 0:0 t:t 0:0'),
			('sg|nom', 't:t u:u h:h a:a 0:0 t:t 0:0 +sg:0 +nom:0'),
			('sg|gen', 't:t u:u h:h a:a 0:n t:n 0:e +sg:0 +gen:n'),
			('sg|par', 't:t u:u h:h a:a 0:0 t:t 0:0 +sg:0 +par:t 0:a'),
			('sg|ine', 't:t u:u h:h a:a 0:n t:n 0:e +sg:0 +ine:s 0:s 0:a'),
			('sg|ess', 't:t u:u h:h a:a 0:n t:t 0:e +sg:0 +ess:n 0:a'),
			('pl|nom', 't:t u:u h:h a:a 0:n t:n 0:e +pl:t +nom:0'),
			('pl|gen', 't:t u:u h:h a:a 0:n t:s 0:0 +pl:i 0:e +gen:n'),
			('pl|gen', 't:t u:u h:h a:a 0:n t:0 0:0 +pl:t 0:e +gen:n'),
			('pl|par', 't:t u:u h:h a:a 0:n t:s 0:0 +pl:i +par:a'),
			('pl|ine', 't:t u:u h:h a:a 0:n t:s 0:0 +pl:i +ine:s 0:s 0:a'),
		])

	def test_numeral_kymmenen(self):
		inflections = {
			"@base":  ['kymmenen'],
			"sg|nom": ['kymmenen'],
			"sg|gen": ['kymmenen'],
			"sg|par": ['kymmentä'],
			"sg|ine": ['kymmenessä'],
			"sg|ess": ['kymmenenä'],
			"pl|nom": ['kymmenet'],
			"pl|gen": ['kymmenien', 'kymmenten'],
			"pl|par": ['kymmeniä'],
			"pl|ine": ['kymmenissä'],
		}
		aligned = align(inflections, pos='numeral')
		self.assertEqual(aligned, [
			('@base',  'k:k y:y m:m m:m e:e n:n e:e n:n'),
			('sg|nom', 'k:k y:y m:m m:m e:e n:n e:e n:n +sg:0 +nom:0'),
			('sg|gen', 'k:k y:y m:m m:m e:e n:n e:e n:0 +sg:0 +gen:n'),
			('sg|par', 'k:k y:y m:m m:m e:e n:n e:0 n:0 +sg:0 +par:t 0:ä'),
			('sg|ine', 'k:k y:y m:m m:m e:e n:n e:e n:0 +sg:0 +ine:s 0:s 0:ä'),
			('sg|ess', 'k:k y:y m:m m:m e:e n:n e:e n:0 +sg:0 +ess:n 0:ä'),
			('pl|nom', 'k:k y:y m:m m:m e:e n:n e:e n:0 +pl:t +nom:0'),
			('pl|gen', 'k:k y:y m:m m:m e:e n:n e:0 n:0 +pl:i 0:e +gen:n'),
			('pl|gen', 'k:k y:y m:m m:m e:e n:n e:0 n:0 +pl:t 0:e +gen:n'),
			('pl|par', 'k:k y:y m:m m:m e:e n:n e:0 n:0 +pl:i +par:ä'),
			('pl|ine', 'k:k y:y m:m m:m e:e n:n e:0 n:0 +pl:i +ine:s 0:s 0:ä'),
		])

	def test_numeral_yksitoista(self):
		inflections = {
			"@base":  ['yksitoista'],
			"sg|nom": ['yksitoista'],
			"sg|gen": ['yhdentoista'],
			"sg|par": ['yhtätoista'],
			"sg|ine": ['yhdessätoista'],
			"sg|ess": ['yhtenätoista'],
			"pl|nom": ['yhdettoista'],
			"pl|gen": ['yksientoista'],
			"pl|par": ['yksiätoista'],
			"pl|ine": ['yksissätoista'],
		}
		aligned = align(inflections, pos='numeral')
		self.assertEqual(aligned, [
			('@base',  'y:y k:k s:s i:i t:t o:o i:i s:s t:t a:a'),
			('sg|nom', 'y:y k:k s:s i:i t:0 o:0 i:0 s:0 t:0 a:0 +sg:0 +nom:0 0:t 0:o 0:i 0:s 0:t 0:a'),
			('sg|gen', 'y:y k:h s:d i:e t:0 o:0 i:0 s:0 t:0 a:0 +sg:0 +gen:n 0:t 0:o 0:i 0:s 0:t 0:a'),
			('sg|par', 'y:y k:h s:0 i:0 t:0 o:0 i:0 s:0 t:0 a:0 +sg:0 +par:t 0:ä 0:t 0:o 0:i 0:s 0:t 0:a'),
			('sg|ine', 'y:y k:h s:d i:e t:0 o:0 i:0 s:0 t:0 a:0 +sg:0 +ine:s 0:s 0:ä 0:t 0:o 0:i 0:s 0:t 0:a'),
			('sg|ess', 'y:y k:h s:t i:e t:0 o:0 i:0 s:0 t:0 a:0 +sg:0 +ess:n 0:ä 0:t 0:o 0:i 0:s 0:t 0:a'),
			('pl|nom', 'y:y k:h s:d i:e t:0 o:0 i:0 s:0 t:0 a:0 +pl:t +nom:0 0:t 0:o 0:i 0:s 0:t 0:a'),
			('pl|gen', 'y:y k:k s:s i:0 t:0 o:0 i:0 s:0 t:0 a:0 +pl:i 0:e +gen:n 0:t 0:o 0:i 0:s 0:t 0:a'),
			('pl|par', 'y:y k:k s:s i:0 t:0 o:0 i:0 s:0 t:0 a:0 +pl:i +par:ä 0:t 0:o 0:i 0:s 0:t 0:a'),
			('pl|ine', 'y:y k:k s:s i:0 t:0 o:0 i:0 s:0 t:0 a:0 +pl:i +ine:s 0:s 0:ä 0:t 0:o 0:i 0:s 0:t 0:a'),
		])

	# Verbs

	def test_verb_kaatua(self):
		inflections = {
			"@base":    ['kaatua'],
			"inf1":     ['kaatua'],
			"pres|1sg": ['kaadun'],
			"pres|3sg": ['kaatuu'],
			"pres|3pl": ['kaatuvat'],
			"past|1sg": ['kaaduin'],
			"past|3sg": ['kaatui'],
			"past|3pl": ['kaatuivat'],
		}
		aligned = align(inflections, pos='verb')
		self.assertEqual(aligned, [
			('@base',    'k:k a:a a:a t:t u:u a:0'),
			('inf1', 	 'k:k a:a a:a t:t u:u a:0 +inf1:a'),
			('pres|1sg', 'k:k a:a a:a t:d u:u a:0 +pres:0 +1sg:n'),
			('pres|3sg', 'k:k a:a a:a t:t u:u a:0 +pres:0 +3sg:u'),
			('pres|3pl', 'k:k a:a a:a t:t u:u a:0 +pres:0 +3pl:v 0:a 0:t'),
			('past|1sg', 'k:k a:a a:a t:d u:u a:0 +past:i +1sg:n'),
			('past|3sg', 'k:k a:a a:a t:t u:u a:0 +past:i +3sg:0'),
			('past|3pl', 'k:k a:a a:a t:t u:u a:0 +past:i +3pl:v 0:a 0:t'),
		])

	def test_verb_tulla(self):
		inflections = {

			'@base': ['tulla'],

			'inf1': ['tulla'],
			'inf1|tra': ['tullakseen'],
			'inf2|ins': ['tullen'],
			'inf2|ine': ['tullessa'],
			'inf3|ine': ['tulemassa'],
			'inf3|ela': ['tulemasta'],
			'inf3|ill': ['tulemaan'],
			'inf3|ade': ['tulemalla'],
			'inf3|abe': ['tulematta'],
			'inf3|ins': ['tuleman'],
			'inf4': ['tuleminen'],
			'inf5': ['tulemaisillaan'],

			'pres|1sg': ['tulen'],
			'pres|2sg': ['tulet'],
			'pres|3sg': ['tulee'],
			'pres|1pl': ['tulemme'],
			'pres|2pl': ['tulette'],
			'pres|3pl': ['tulevat'],
			'pres|conneg': ['tule'],

			'past|1sg': ['tulin'],
			'past|2sg': ['tulit'],
			'past|3sg': ['tuli'],
			'past|1pl': ['tulimme'],
			'past|2pl': ['tulitte'],
			'past|3pl': ['tulivat'],
			'past|conneg': ['tullut'],

			'cond|1sg': ['tulisin'],
			'cond|2sg': ['tulisit'],
			'cond|3sg': ['tulisi'],
			'cond|1pl': ['tulisimme'],
			'cond|2pl': ['tulisitte'],
			'cond|3pl': ['tulisivat'],
			'cond|conneg': ['tulisi'],

			'poten|1sg': ['tullen'],
			'poten|2sg': ['tullet'],
			'poten|3sg': ['tullee'],
			'poten|1pl': ['tullemme'],
			'poten|2pl': ['tullette'],
			'poten|3pl': ['tullevat'],
			'poten|conneg': ['tulle'],

			'imper|2sg': ['tule'],
			'imper|2pl': ['tulkaa'],
			'imper|3sg': ['tulkoon'],
			'imper|3pl': ['tulkoot'],
			'imper|2pl|rare': ['tulkaatte'],
			'imper|2sg|conneg': ['tule'],
			'imper|1pl': ['tulkaamme'],
			'imper|2pl|arch': ['tulkaat'],
			'imper|2pl|nstd': ['tulkaatten'],
			'imper|pl|conneg': ['tulko'],
			'imper|3sg|conneg': ['tulko'],

			'part_pres': ['tuleva'],
			'part_past': ['tullut'],
			'part_ma': ['tulema'],
			'part_maton': ['tulematon'],

			'pass|pres': ['tullaan'],
			'pass|past': ['tultiin'],
			'pass|cond': ['tultaisiin'],
			'pass|poten': ['tultaneen'],
			'pass|imper': ['tultakoon'],
			'pass|pres|conneg': ['tulla'],
			'pass|past|conneg': ['tultu'],
			'pass|cond|conneg': ['tultaisi'],
			'pass|poten|conneg': ['tultane'],
			'pass|imper|conneg': ['tultako'],
			'pass|inf2|ine': ['tultaessa'],
			'pass|part_pres': ['tultava'],
			'pass|part_past': ['tultu'],
			'pass|inf3|ins': ['tultaman'],
		}
		aligned = align(inflections, pos='verb')
		self.assertEqual(aligned, [
			('@base',                't:t u:u l:l 0:0 l:0 a:0'),

			('inf1',                 't:t u:u l:l 0:0 l:0 a:0 +inf1:l 0:a'),
			('inf1|tra',             't:t u:u l:l 0:0 l:0 a:0 +inf1:l 0:a +tra:k 0:s 0:e 0:e 0:n'),
			('inf2|ins',             't:t u:u l:l 0:0 l:0 a:0 +inf2:l 0:e +ins:n'),
			('inf2|ine',             't:t u:u l:l 0:0 l:0 a:0 +inf2:l 0:e +ine:s 0:s 0:a'),
			('inf3|ine',             't:t u:u l:l 0:e l:0 a:0 +inf3:m 0:a +ine:s 0:s 0:a'),
			('inf3|ela',             't:t u:u l:l 0:e l:0 a:0 +inf3:m 0:a +ela:s 0:t 0:a'),
			('inf3|ill',             't:t u:u l:l 0:e l:0 a:0 +inf3:m 0:a +ill:a 0:n'),
			('inf3|ade',             't:t u:u l:l 0:e l:0 a:0 +inf3:m 0:a +ade:l 0:l 0:a'),
			('inf3|abe',             't:t u:u l:l 0:e l:0 a:0 +inf3:m 0:a +abe:t 0:t 0:a'),
			('inf3|ins',             't:t u:u l:l 0:e l:0 a:0 +inf3:m 0:a +ins:n'),
			('inf4',                 't:t u:u l:l 0:e l:0 a:0 +inf4:m 0:i 0:n 0:e 0:n'),
			('inf5',                 't:t u:u l:l 0:e l:0 a:0 +inf5:m 0:a 0:i 0:s 0:i 0:l 0:l 0:a 0:a 0:n'),

			('part_pres',            't:t u:u l:l 0:e l:0 a:0 +part_pres:v 0:a'),
			('part_past',            't:t u:u l:l 0:0 l:0 a:0 +part_past:l 0:u 0:t'),
			('part_ma',              't:t u:u l:l 0:e l:0 a:0 +part_ma:m 0:a'),
			('part_maton',           't:t u:u l:l 0:e l:0 a:0 +part_maton:m 0:a 0:t 0:o 0:n'),

			('pres|1sg',             't:t u:u l:l 0:e l:0 a:0 +pres:0 +1sg:n'),
			('pres|2sg',             't:t u:u l:l 0:e l:0 a:0 +pres:0 +2sg:t'),
			('pres|3sg',             't:t u:u l:l 0:e l:0 a:0 +pres:0 +3sg:e'),
			('pres|1pl',             't:t u:u l:l 0:e l:0 a:0 +pres:0 +1pl:m 0:m 0:e'),
			('pres|2pl',             't:t u:u l:l 0:e l:0 a:0 +pres:0 +2pl:t 0:t 0:e'),
			('pres|3pl',             't:t u:u l:l 0:e l:0 a:0 +pres:0 +3pl:v 0:a 0:t'),
			('pres|conneg',          't:t u:u l:l 0:e l:0 a:0 +pres:0 +conneg:0'),

			('past|1sg',             't:t u:u l:l 0:0 l:0 a:0 +past:i +1sg:n'),
			('past|2sg',             't:t u:u l:l 0:0 l:0 a:0 +past:i +2sg:t'),
			('past|3sg',             't:t u:u l:l 0:0 l:0 a:0 +past:i +3sg:0'),
			('past|1pl',             't:t u:u l:l 0:0 l:0 a:0 +past:i +1pl:m 0:m 0:e'),
			('past|2pl',             't:t u:u l:l 0:0 l:0 a:0 +past:i +2pl:t 0:t 0:e'),
			('past|3pl',             't:t u:u l:l 0:0 l:0 a:0 +past:i +3pl:v 0:a 0:t'),
			('past|conneg',          't:t u:u l:l 0:0 l:0 a:0 +past:l 0:u 0:t +conneg:0'),

			('cond|1sg',             't:t u:u l:l 0:0 l:0 a:0 +cond:i 0:s 0:i +1sg:n'),
			('cond|2sg',             't:t u:u l:l 0:0 l:0 a:0 +cond:i 0:s 0:i +2sg:t'),
			('cond|3sg',             't:t u:u l:l 0:0 l:0 a:0 +cond:i 0:s 0:i +3sg:0'),
			('cond|1pl',             't:t u:u l:l 0:0 l:0 a:0 +cond:i 0:s 0:i +1pl:m 0:m 0:e'),
			('cond|2pl',             't:t u:u l:l 0:0 l:0 a:0 +cond:i 0:s 0:i +2pl:t 0:t 0:e'),
			('cond|3pl',             't:t u:u l:l 0:0 l:0 a:0 +cond:i 0:s 0:i +3pl:v 0:a 0:t'),
			('cond|conneg',          't:t u:u l:l 0:0 l:0 a:0 +cond:i 0:s 0:i +conneg:0'),

			('poten|1sg',            't:t u:u l:l 0:0 l:0 a:0 +poten:l 0:e +1sg:n'),
			('poten|2sg',            't:t u:u l:l 0:0 l:0 a:0 +poten:l 0:e +2sg:t'),
			('poten|3sg',            't:t u:u l:l 0:0 l:0 a:0 +poten:l 0:e +3sg:e'),
			('poten|1pl',            't:t u:u l:l 0:0 l:0 a:0 +poten:l 0:e +1pl:m 0:m 0:e'),
			('poten|2pl',            't:t u:u l:l 0:0 l:0 a:0 +poten:l 0:e +2pl:t 0:t 0:e'),
			('poten|3pl',            't:t u:u l:l 0:0 l:0 a:0 +poten:l 0:e +3pl:v 0:a 0:t'),
			('poten|conneg',         't:t u:u l:l 0:0 l:0 a:0 +poten:l 0:e +conneg:0'),

			('imper|2sg',            't:t u:u l:l 0:e l:0 a:0 +imper:0 +2sg:0'),
			('imper|3sg',            't:t u:u l:l 0:0 l:0 a:0 +imper:k 0:o 0:o +3sg:n'),
			('imper|1pl',            't:t u:u l:l 0:0 l:0 a:0 +imper:k 0:a 0:a +1pl:m 0:m 0:e'),
			('imper|2pl',            't:t u:u l:l 0:0 l:0 a:0 +imper:k 0:a +2pl:a'),
			('imper|3pl',            't:t u:u l:l 0:0 l:0 a:0 +imper:k 0:o 0:o +3pl:t'),
			('imper|2sg|conneg',     't:t u:u l:l 0:e l:0 a:0 +imper:0 +2sg:0 +conneg:0'),
			('imper|3sg|conneg',     't:t u:u l:l 0:0 l:0 a:0 +imper:k +3sg:o +conneg:0'),
			('imper|pl|conneg',      't:t u:u l:l 0:0 l:0 a:0 +imper:k +pl:o +conneg:0'),
			('imper|2pl|rare',       't:t u:u l:l 0:0 l:0 a:0 +imper:k 0:a 0:a +2pl:t 0:t 0:e +rare:0'),
			('imper|2pl|arch',       't:t u:u l:l 0:0 l:0 a:0 +imper:k 0:a 0:a +2pl:t +arch:0'),
			('imper|2pl|nstd',       't:t u:u l:l 0:0 l:0 a:0 +imper:k 0:a 0:a +2pl:t 0:t 0:e 0:n +nstd:0'),

			('pass|pres',            't:t u:u l:l 0:0 l:0 a:0 +pass:l 0:a 0:a 0:n +pres:0'),
			('pass|past',            't:t u:u l:l 0:0 l:0 a:0 +pass:t +past:i 0:i 0:n'),
			('pass|cond',            't:t u:u l:l 0:0 l:0 a:0 +pass:t 0:a +cond:i 0:s 0:i 0:i 0:n'),
			('pass|poten',           't:t u:u l:l 0:0 l:0 a:0 +pass:t 0:a +poten:n 0:e 0:e 0:n'),
			('pass|imper',           't:t u:u l:l 0:0 l:0 a:0 +pass:t 0:a +imper:k 0:o 0:o 0:n'),
			('pass|pres|conneg',     't:t u:u l:l 0:0 l:0 a:0 +pass:l 0:a +pres:0 +conneg:0'),
			('pass|past|conneg',     't:t u:u l:l 0:0 l:0 a:0 +pass:t +past:u +conneg:0'),
			('pass|cond|conneg',     't:t u:u l:l 0:0 l:0 a:0 +pass:t 0:a +cond:i 0:s 0:i +conneg:0'),
			('pass|poten|conneg',    't:t u:u l:l 0:0 l:0 a:0 +pass:t 0:a +poten:n 0:e +conneg:0'),
			('pass|imper|conneg',    't:t u:u l:l 0:0 l:0 a:0 +pass:t 0:a +imper:k 0:o +conneg:0'),
			('pass|inf2|ine',        't:t u:u l:l 0:0 l:0 a:0 +pass:t 0:a +inf2:e +ine:s 0:s 0:a'),
			('pass|inf3|ins',        't:t u:u l:l 0:0 l:0 a:0 +pass:t 0:a +inf3:m 0:a +ins:n'),
			('pass|part_pres',       't:t u:u l:l 0:0 l:0 a:0 +pass:t 0:a +part_pres:v 0:a'),
			('pass|part_past',       't:t u:u l:l 0:0 l:0 a:0 +pass:t +part_past:u'),
		])

	def test_verb_nahda(self):
		inflections = {
			"@base":    ['nähdä'],
			"inf1":     ['nähdä'],
			"pres|1sg": ['näen'],
			"pres|3sg": ['näkee'],
			"pres|3pl": ['näkevät'],
			"past|1sg": ['näin'],
			"past|3sg": ['näki'],
			"past|3pl": ['näkivät'],
		}
		aligned = align(inflections, pos='verb')
		self.assertEqual(aligned, [
			('@base',    'n:n ä:ä h:h 0:0 d:0 ä:0'),
			('inf1',     'n:n ä:ä h:h 0:0 d:0 ä:0 +inf1:d 0:ä'),
			('pres|1sg', 'n:n ä:ä h:0 0:e d:0 ä:0 +pres:0 +1sg:n'),
			('pres|3sg', 'n:n ä:ä h:k 0:e d:0 ä:0 +pres:0 +3sg:e'),
			('pres|3pl', 'n:n ä:ä h:k 0:e d:0 ä:0 +pres:0 +3pl:v 0:ä 0:t'),
			('past|1sg', 'n:n ä:ä h:0 0:0 d:0 ä:0 +past:i +1sg:n'),
			('past|3sg', 'n:n ä:ä h:k 0:0 d:0 ä:0 +past:i +3sg:0'),
			('past|3pl', 'n:n ä:ä h:k 0:0 d:0 ä:0 +past:i +3pl:v 0:ä 0:t'),
		])

	def test_verb_hakata(self):
		inflections = {

			"@base":    ['hakata'],

			'inf1': ['hakata'],
			'inf1|tra': ['hakatakseen'],
			'inf2|ins': ['hakaten'],
			'inf2|ine': ['hakatessa'],
			'inf3|ine': ['hakkaamassa'],
			'inf3|ela': ['hakkaamasta'],
			'inf3|ill': ['hakkaamaan'],
			'inf3|ade': ['hakkaamalla'],
			'inf3|abe': ['hakkaamatta'],
			'inf3|ins': ['hakkaaman'],
			'inf4': ['hakkaaminen'],
			'inf5': ['hakkaamaisillaan'],

			'part_pres': ['hakkaava'],
			'part_past': ['hakannut'],
			'part_ma': ['hakkaama'],
			'part_maton': ['hakkaamaton'],

			'pres|1sg': ['hakkaan'],
			'pres|2sg': ['hakkaat'],
			'pres|3sg': ['hakkaa'],
			'pres|1pl': ['hakkaamme'],
			'pres|2pl': ['hakkaatte'],
			'pres|3pl': ['hakkaavat'],
			'pres|conneg': ['hakkaa'],

			'past|1sg': ['hakkasin'],
			'past|2sg': ['hakkasit'],
			'past|3sg': ['hakkasi'],
			'past|1pl': ['hakkasimme'],
			'past|2pl': ['hakkasitte'],
			'past|3pl': ['hakkasivat'],
			'past|conneg': ['hakannut'],

			'cond|1sg': ['hakkaisin'],
			'cond|2sg': ['hakkaisit'],
			'cond|3sg': ['hakkaisi'],
			'cond|1pl': ['hakkaisimme'],
			'cond|2pl': ['hakkaisitte'],
			'cond|3pl': ['hakkaisivat'],
			'cond|conneg': ['hakkaisi'],

			'poten|1sg': ['hakannen'],
			'poten|2sg': ['hakannet'],
			'poten|3sg': ['hakannee'],
			'poten|1pl': ['hakannemme'],
			'poten|2pl': ['hakannette'],
			'poten|3pl': ['hakannevat'],
			'poten|conneg': ['hakanne'],

			'imper|2sg': ['hakkaa'],
			'imper|3sg': ['hakatkoon'],
			'imper|1pl': ['hakatkaamme'],
			'imper|2pl': ['hakatkaa'],
			'imper|3pl': ['hakatkoot'],
			'imper|2sg|conneg': ['hakkaa'],
			'imper|3sg|conneg': ['hakatko'],
			'imper|pl|conneg': ['hakatko'],
			'imper|2pl|rare': ['hakatkaatte'],
			'imper|2pl|arch': ['hakatkaat'],
			'imper|2pl|nstd': ['hakatkaatten'],

			'pass|pres': ['hakataan'],
			'pass|past': ['hakattiin'],
			'pass|cond': ['hakattaisiin'],
			'pass|poten': ['hakattaneen'],
			'pass|imper': ['hakattakoon'],

			'pass|pres|conneg': ['hakata'],
			'pass|past|conneg': ['hakattu'],
			'pass|cond|conneg': ['hakattaisi'],
			'pass|poten|conneg': ['hakattane'],
			'pass|imper|conneg': ['hakattako'],

			'pass|inf2|ine': ['hakattaessa'],
			'pass|inf3|ins': ['hakattaman'],
			'pass|part_pres': ['hakattava'],
			'pass|part_past': ['hakattu'],

		}
		aligned = align(inflections, pos='verb')
		self.assertEqual(aligned, [

			('@base',                'h:h a:a k:k 0:0 a:a 0:0 0:0 t:0 a:0'),

			# OK
			('inf1',                 'h:h a:a k:k 0:0 a:a 0:0 0:0 t:0 a:0 +inf1:t 0:a'),
			('inf1|tra',             'h:h a:a k:k 0:0 a:a 0:0 0:0 t:0 a:0 +inf1:t 0:a +tra:k 0:s 0:e 0:e 0:n'),
			('inf2|ins',             'h:h a:a k:k 0:0 a:a 0:0 0:0 t:0 a:0 +inf2:t 0:e +ins:n'),
			('inf2|ine',             'h:h a:a k:k 0:0 a:a 0:0 0:0 t:0 a:0 +inf2:t 0:e +ine:s 0:s 0:a'),
			('inf3|ine',             'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +inf3:m 0:a +ine:s 0:s 0:a'),
			('inf3|ela',             'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +inf3:m 0:a +ela:s 0:t 0:a'),
			('inf3|ill',             'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +inf3:m 0:a +ill:a 0:n'),
			('inf3|ade',             'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +inf3:m 0:a +ade:l 0:l 0:a'),
			('inf3|abe',             'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +inf3:m 0:a +abe:t 0:t 0:a'),
			('inf3|ins',             'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +inf3:m 0:a +ins:n'),
			('inf4',                 'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +inf4:m 0:i 0:n 0:e 0:n'),
			('inf5',                 'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +inf5:m 0:a 0:i 0:s 0:i 0:l 0:l 0:a 0:a 0:n'),

			# OK
			('part_pres',            'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +part_pres:v 0:a'),
			('part_past',            'h:h a:a k:k 0:0 a:a 0:n 0:0 t:0 a:0 +part_past:n 0:u 0:t'),
			('part_ma',              'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +part_ma:m 0:a'),
			('part_maton',           'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +part_maton:m 0:a 0:t 0:o 0:n'),

			# OK
			('pres|1sg',             'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +pres:0 +1sg:n'),
			('pres|2sg',             'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +pres:0 +2sg:t'),
			('pres|3sg',             'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +pres:0 +3sg:0'),
			('pres|1pl',             'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +pres:0 +1pl:m 0:m 0:e'),
			('pres|2pl',             'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +pres:0 +2pl:t 0:t 0:e'),
			('pres|3pl',             'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +pres:0 +3pl:v 0:a 0:t'),
			('pres|conneg',          'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +pres:0 +conneg:0'),

			# OK
			('past|1sg',             'h:h a:a k:k 0:k a:a 0:s 0:0 t:0 a:0 +past:i +1sg:n'),
			('past|2sg',             'h:h a:a k:k 0:k a:a 0:s 0:0 t:0 a:0 +past:i +2sg:t'),
			('past|3sg',             'h:h a:a k:k 0:k a:a 0:s 0:0 t:0 a:0 +past:i +3sg:0'),
			('past|1pl',             'h:h a:a k:k 0:k a:a 0:s 0:0 t:0 a:0 +past:i +1pl:m 0:m 0:e'),
			('past|2pl',             'h:h a:a k:k 0:k a:a 0:s 0:0 t:0 a:0 +past:i +2pl:t 0:t 0:e'),
			('past|3pl',             'h:h a:a k:k 0:k a:a 0:s 0:0 t:0 a:0 +past:i +3pl:v 0:a 0:t'),
			('past|conneg',          'h:h a:a k:k 0:0 a:a 0:n 0:0 t:0 a:0 +past:n 0:u 0:t +conneg:0'),

			# OK
			('cond|1sg',             'h:h a:a k:k 0:k a:a 0:0 0:0 t:0 a:0 +cond:i 0:s 0:i +1sg:n'),
			('cond|2sg',             'h:h a:a k:k 0:k a:a 0:0 0:0 t:0 a:0 +cond:i 0:s 0:i +2sg:t'),
			('cond|3sg',             'h:h a:a k:k 0:k a:a 0:0 0:0 t:0 a:0 +cond:i 0:s 0:i +3sg:0'),
			('cond|1pl',             'h:h a:a k:k 0:k a:a 0:0 0:0 t:0 a:0 +cond:i 0:s 0:i +1pl:m 0:m 0:e'),
			('cond|2pl',             'h:h a:a k:k 0:k a:a 0:0 0:0 t:0 a:0 +cond:i 0:s 0:i +2pl:t 0:t 0:e'),
			('cond|3pl',             'h:h a:a k:k 0:k a:a 0:0 0:0 t:0 a:0 +cond:i 0:s 0:i +3pl:v 0:a 0:t'),
			('cond|conneg',          'h:h a:a k:k 0:k a:a 0:0 0:0 t:0 a:0 +cond:i 0:s 0:i +conneg:0'),

			# OK
			('poten|1sg',            'h:h a:a k:k 0:0 a:a 0:n 0:0 t:0 a:0 +poten:n 0:e +1sg:n'),
			('poten|2sg',            'h:h a:a k:k 0:0 a:a 0:n 0:0 t:0 a:0 +poten:n 0:e +2sg:t'),
			('poten|3sg',            'h:h a:a k:k 0:0 a:a 0:n 0:0 t:0 a:0 +poten:n 0:e +3sg:e'),
			('poten|1pl',            'h:h a:a k:k 0:0 a:a 0:n 0:0 t:0 a:0 +poten:n 0:e +1pl:m 0:m 0:e'),
			('poten|2pl',            'h:h a:a k:k 0:0 a:a 0:n 0:0 t:0 a:0 +poten:n 0:e +2pl:t 0:t 0:e'),
			('poten|3pl',            'h:h a:a k:k 0:0 a:a 0:n 0:0 t:0 a:0 +poten:n 0:e +3pl:v 0:a 0:t'),
			('poten|conneg',         'h:h a:a k:k 0:0 a:a 0:n 0:0 t:0 a:0 +poten:n 0:e +conneg:0'),

			# OK
			('imper|2sg',            'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +imper:0 +2sg:0'),
			('imper|3sg',            'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +imper:k 0:o 0:o +3sg:n'),
			('imper|1pl',            'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +imper:k 0:a 0:a +1pl:m 0:m 0:e'),
			('imper|2pl',            'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +imper:k 0:a +2pl:a'),
			('imper|3pl',            'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +imper:k 0:o 0:o +3pl:t'),
			('imper|2sg|conneg',     'h:h a:a k:k 0:k a:a 0:0 0:a t:0 a:0 +imper:0 +2sg:0 +conneg:0'),
			('imper|3sg|conneg',     'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +imper:k +3sg:o +conneg:0'),
			('imper|pl|conneg',      'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +imper:k +pl:o +conneg:0'),
			('imper|2pl|rare',       'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +imper:k 0:a 0:a +2pl:t 0:t 0:e +rare:0'),
			('imper|2pl|arch',       'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +imper:k 0:a 0:a +2pl:t +arch:0'),
			('imper|2pl|nstd',       'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +imper:k 0:a 0:a +2pl:t 0:t 0:e 0:n +nstd:0'),

			# OK
			('pass|pres',            'h:h a:a k:k 0:0 a:a 0:0 0:0 t:0 a:0 +pass:t 0:a 0:a 0:n +pres:0'),
			('pass|past',            'h:h a:a k:k 0:0 a:a 0:0 0:0 t:0 a:0 +pass:t 0:t +past:i 0:i 0:n'),
			('pass|cond',            'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +pass:t 0:a +cond:i 0:s 0:i 0:i 0:n'),
			('pass|poten',           'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +pass:t 0:a +poten:n 0:e 0:e 0:n'),
			('pass|imper',           'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +pass:t 0:a +imper:k 0:o 0:o 0:n'),
			('pass|pres|conneg',     'h:h a:a k:k 0:0 a:a 0:0 0:0 t:0 a:0 +pass:t 0:a +pres:0 +conneg:0'),
			('pass|past|conneg',     'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +pass:t +past:u +conneg:0'),
			('pass|cond|conneg',     'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +pass:t 0:a +cond:i 0:s 0:i +conneg:0'),
			('pass|poten|conneg',    'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +pass:t 0:a +poten:n 0:e +conneg:0'),
			('pass|imper|conneg',    'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +pass:t 0:a +imper:k 0:o +conneg:0'),
			('pass|inf2|ine',        'h:h a:a k:k 0:0 a:a 0:0 0:0 t:0 a:0 +pass:t 0:t 0:a +inf2:e +ine:s 0:s 0:a'),
			('pass|inf3|ins',        'h:h a:a k:k 0:0 a:a 0:0 0:0 t:0 a:0 +pass:t 0:t 0:a +inf3:m 0:a +ins:n'),
			('pass|part_pres',       'h:h a:a k:k 0:0 a:a 0:0 0:0 t:0 a:0 +pass:t 0:t 0:a +part_pres:v 0:a'),
			('pass|part_past',       'h:h a:a k:k 0:0 a:a 0:t 0:0 t:0 a:0 +pass:t +part_past:u'),
		])

	def test_verb_kaveta(self):
		inflections = {
			"@base":    ['kaveta'],
			"inf1":     ['kaveta'],
			"pres|1sg": ['kapenen'],
			"pres|3sg": ['kapenee'],
			"pres|3pl": ['kapenevat'],
			"past|1sg": ['kapenin'],
			"past|3sg": ['kapeni'],
			"past|3pl": ['kapenivat'],

			"poten|3sg": ['kavennee'],
			"cond|3sg":  ['kapenisi'],
			"imper|3sg": ['kavetkoon'],
		}
		aligned = align(inflections, pos='verb')
		self.assertEqual(aligned, [
			('@base',     'k:k a:a v:v e:e 0:0 0:0 t:0 a:0'),
			('inf1',      'k:k a:a v:v e:e 0:0 0:0 t:0 a:0 +inf1:t 0:a'),
			('pres|1sg',  'k:k a:a v:p e:e 0:n 0:e t:0 a:0 +pres:0 +1sg:n'),
			('pres|3sg',  'k:k a:a v:p e:e 0:n 0:e t:0 a:0 +pres:0 +3sg:e'),
			('pres|3pl',  'k:k a:a v:p e:e 0:n 0:e t:0 a:0 +pres:0 +3pl:v 0:a 0:t'),
			('past|1sg',  'k:k a:a v:p e:e 0:n 0:0 t:0 a:0 +past:i +1sg:n'),
			('past|3sg',  'k:k a:a v:p e:e 0:n 0:0 t:0 a:0 +past:i +3sg:0'),
			('past|3pl',  'k:k a:a v:p e:e 0:n 0:0 t:0 a:0 +past:i +3pl:v 0:a 0:t'),
			('cond|3sg',  'k:k a:a v:p e:e 0:n 0:0 t:0 a:0 +cond:i 0:s 0:i +3sg:0'),
			('poten|3sg', 'k:k a:a v:v e:e 0:n 0:0 t:0 a:0 +poten:n 0:e +3sg:e'),
			('imper|3sg', 'k:k a:a v:v e:e 0:t 0:0 t:0 a:0 +imper:k 0:o 0:o +3sg:n'),
		])

	def test_verb_valita(self):
		inflections = {
			"@base": ['valita'],
			"inf1": ['valita'],
			"pres|1sg": ['valitsen'],
			"pres|3sg": ['valitsee'],
			"pres|3pl": ['valitsevat'],
			"past|1sg": ['valitsin'],
			"past|3sg": ['valitsi'],
			"past|3pl": ['valitsivat'],
			"poten|3sg": ['valinnee'],
			"cond|3sg": ['valitsisi'],
			"imper|3sg": ['valitkoon'],
		}
		aligned = align(inflections, pos='verb')
		self.assertEqual(aligned, [
			('@base',     'v:v a:a l:l i:i 0:0 0:0 0:0 t:0 a:0'),
			('inf1',      'v:v a:a l:l i:i 0:0 0:0 0:0 t:0 a:0 +inf1:t 0:a'),
			('pres|1sg',  'v:v a:a l:l i:i 0:t 0:s 0:e t:0 a:0 +pres:0 +1sg:n'),
			('pres|3sg',  'v:v a:a l:l i:i 0:t 0:s 0:e t:0 a:0 +pres:0 +3sg:e'),
			('pres|3pl',  'v:v a:a l:l i:i 0:t 0:s 0:e t:0 a:0 +pres:0 +3pl:v 0:a 0:t'),
			('past|1sg',  'v:v a:a l:l i:i 0:t 0:s 0:0 t:0 a:0 +past:i +1sg:n'),
			('past|3sg',  'v:v a:a l:l i:i 0:t 0:s 0:0 t:0 a:0 +past:i +3sg:0'),
			('past|3pl',  'v:v a:a l:l i:i 0:t 0:s 0:0 t:0 a:0 +past:i +3pl:v 0:a 0:t'),
			('cond|3sg',  'v:v a:a l:l i:i 0:t 0:s 0:0 t:0 a:0 +cond:i 0:s 0:i +3sg:0'),
			('poten|3sg', 'v:v a:a l:l i:i 0:n 0:0 0:0 t:0 a:0 +poten:n 0:e +3sg:e'),
			('imper|3sg', 'v:v a:a l:l i:i 0:t 0:0 0:0 t:0 a:0 +imper:k 0:o 0:o +3sg:n'),

		])

	def test_verb_juosta(self):
		inflections = {
			"@base":    ['juosta'],
			"inf1":     ['juosta'],
			"pres|1sg": ['juoksen'],
			"pres|3sg": ['juoksee'],
			"pres|3pl": ['juoksevat'],
			"past|1sg": ['juoksin'],
			"past|3sg": ['juoksi'],
			"past|3pl": ['juoksivat'],

			"poten|3sg": ['juossee'],
			"cond|3sg": ['juoksisi'],
			"imper|3sg": ['juoskoon'],
		}
		aligned = align(inflections, pos='verb')
		self.assertEqual(aligned, [
			('@base',     'j:j u:u o:o 0:0 s:s 0:0 t:0 a:0'),
			('inf1',      'j:j u:u o:o 0:0 s:s 0:0 t:0 a:0 +inf1:t 0:a'),
			('pres|1sg',  'j:j u:u o:o 0:k s:s 0:e t:0 a:0 +pres:0 +1sg:n'),
			('pres|3sg',  'j:j u:u o:o 0:k s:s 0:e t:0 a:0 +pres:0 +3sg:e'),
			('pres|3pl',  'j:j u:u o:o 0:k s:s 0:e t:0 a:0 +pres:0 +3pl:v 0:a 0:t'),
			('past|1sg',  'j:j u:u o:o 0:k s:s 0:0 t:0 a:0 +past:i +1sg:n'),
			('past|3sg',  'j:j u:u o:o 0:k s:s 0:0 t:0 a:0 +past:i +3sg:0'),
			('past|3pl',  'j:j u:u o:o 0:k s:s 0:0 t:0 a:0 +past:i +3pl:v 0:a 0:t'),
			('cond|3sg',  'j:j u:u o:o 0:k s:s 0:0 t:0 a:0 +cond:i 0:s 0:i +3sg:0'),
			('poten|3sg', 'j:j u:u o:o 0:0 s:s 0:0 t:0 a:0 +poten:s 0:e +3sg:e'),
			('imper|3sg', 'j:j u:u o:o 0:0 s:s 0:0 t:0 a:0 +imper:k 0:o 0:o +3sg:n'),
		])

	def test_verb_olla(self):
		inflections = {
			"@base":    ['olla'],
			"inf1":     ['olla'],
			"pres|1sg": ['olen'],
			"pres|3sg": ['on'],
			"pres|3pl": ['ovat'],
			"past|1sg": ['olin'],
			"past|3sg": ['oli'],
			"past|3pl": ['olivat'],

			"poten|3sg": ['lienee'],
			"cond|3sg": ['olisi'],
			"imper|3sg": ['olkoon'],
		}
		aligned = align(inflections, pos='verb')
		self.assertEqual(aligned, [
			('@base',     'o:o l:l 0:0 l:0 a:0'),
			('inf1',      'o:o l:l 0:0 l:0 a:0 +inf1:l 0:a'),
			('pres|1sg',  'o:o l:l 0:e l:0 a:0 +pres:0 +1sg:n'),
			('pres|3sg',  'o:o l:0 0:0 l:0 a:0 +pres:0 +3sg:n'),
			('pres|3pl',  'o:o l:0 0:0 l:0 a:0 +pres:0 +3pl:v 0:a 0:t'),
			('past|1sg',  'o:o l:l 0:0 l:0 a:0 +past:i +1sg:n'),
			('past|3sg',  'o:o l:l 0:0 l:0 a:0 +past:i +3sg:0'),
			('past|3pl',  'o:o l:l 0:0 l:0 a:0 +past:i +3pl:v 0:a 0:t'),
			('cond|3sg',  'o:o l:l 0:0 l:0 a:0 +cond:i 0:s 0:i +3sg:0'),
			('poten|3sg', 'o:l l:i 0:e l:0 a:0 +poten:n 0:e +3sg:e'),
			('imper|3sg', 'o:o l:l 0:0 l:0 a:0 +imper:k 0:o 0:o +3sg:n'),
		])

	def test_verb_erkanee(self):
		inflections = {

			'@base': ['erkanee'],
			'inf3|ine': ['erkanemassa'],
			'inf3|ela': ['erkanemasta'],
			'inf3|ill': ['erkanemaan'],
			'inf3|ade': ['erkanemalla'],
			'inf3|abe': ['erkanematta'],
			'inf3|ins': ['erkaneman'],
			'inf4': ['erkaneminen'],
			'inf5': ['erkanemaisillaan'],

			'part_pres': ['erkaneva'],
			'part_maton': ['erkanematon'],

			'pres|1sg': ['erkanen'],
			'pres|2sg': ['erkanet'],
			'pres|3sg': ['erkanee'],
			'pres|1pl': ['erkanemme'],
			'pres|2pl': ['erkanette'],
			'pres|3pl': ['erkanevat'],
			'pres|conneg': ['erkane'],

			'past|1sg': ['erkanin'],
			'past|2sg': ['erkanit'],
			'past|3sg': ['erkani'],
			'past|1pl': ['erkanimme'],
			'past|2pl': ['erkanitte'],
			'past|3pl': ['erkanivat'],

			'cond|1sg': ['erkanisin'],
			'cond|2sg': ['erkanisit'],
			'cond|3sg': ['erkanisi'],
			'cond|1pl': ['erkanisimme'],
			'cond|2pl': ['erkanisitte'],
			'cond|3pl': ['erkanisivat'],
			'cond|conneg': ['erkanisi'],

			'imper|2sg': ['erkane'],
			'imper|2sg|conneg': ['erkane'],
		}
		aligned = align(inflections, pos='verb')
		self.assertEqual(aligned, [
			('@base',    'e:e r:r k:k a:a n:n e:e e:0'),
			('inf3|ine', 'e:e r:r k:k a:a n:n e:e e:0 +inf3:m 0:a +ine:s 0:s 0:a'),
			('inf3|ela', 'e:e r:r k:k a:a n:n e:e e:0 +inf3:m 0:a +ela:s 0:t 0:a'),
			('inf3|ill', 'e:e r:r k:k a:a n:n e:e e:0 +inf3:m 0:a +ill:a 0:n'),
			('inf3|ade', 'e:e r:r k:k a:a n:n e:e e:0 +inf3:m 0:a +ade:l 0:l 0:a'),
			('inf3|abe', 'e:e r:r k:k a:a n:n e:e e:0 +inf3:m 0:a +abe:t 0:t 0:a'),
			('inf3|ins', 'e:e r:r k:k a:a n:n e:e e:0 +inf3:m 0:a +ins:n'),
			('inf4',     'e:e r:r k:k a:a n:n e:e e:0 +inf4:m 0:i 0:n 0:e 0:n'),
			('inf5',     'e:e r:r k:k a:a n:n e:e e:0 +inf5:m 0:a 0:i 0:s 0:i 0:l 0:l 0:a 0:a 0:n'),
			('part_pres', 'e:e r:r k:k a:a n:n e:e e:0 +part_pres:v 0:a'),
			('part_maton', 'e:e r:r k:k a:a n:n e:e e:0 +part_maton:m 0:a 0:t 0:o 0:n'),
			('pres|1sg', 'e:e r:r k:k a:a n:n e:e e:0 +pres:0 +1sg:n'),
			('pres|2sg', 'e:e r:r k:k a:a n:n e:e e:0 +pres:0 +2sg:t'),
			('pres|3sg', 'e:e r:r k:k a:a n:n e:e e:0 +pres:0 +3sg:e'),
			('pres|1pl', 'e:e r:r k:k a:a n:n e:e e:0 +pres:0 +1pl:m 0:m 0:e'),
			('pres|2pl', 'e:e r:r k:k a:a n:n e:e e:0 +pres:0 +2pl:t 0:t 0:e'),
			('pres|3pl', 'e:e r:r k:k a:a n:n e:e e:0 +pres:0 +3pl:v 0:a 0:t'),
			('pres|conneg', 'e:e r:r k:k a:a n:n e:e e:0 +pres:0 +conneg:0'),
			('past|1sg', 'e:e r:r k:k a:a n:n e:0 e:0 +past:i +1sg:n'),
			('past|2sg', 'e:e r:r k:k a:a n:n e:0 e:0 +past:i +2sg:t'),
			('past|3sg', 'e:e r:r k:k a:a n:n e:0 e:0 +past:i +3sg:0'),
			('past|1pl', 'e:e r:r k:k a:a n:n e:0 e:0 +past:i +1pl:m 0:m 0:e'),
			('past|2pl', 'e:e r:r k:k a:a n:n e:0 e:0 +past:i +2pl:t 0:t 0:e'),
			('past|3pl', 'e:e r:r k:k a:a n:n e:0 e:0 +past:i +3pl:v 0:a 0:t'),
			('cond|1sg', 'e:e r:r k:k a:a n:n e:0 e:0 +cond:i 0:s 0:i +1sg:n'),
			('cond|2sg', 'e:e r:r k:k a:a n:n e:0 e:0 +cond:i 0:s 0:i +2sg:t'),
			('cond|3sg', 'e:e r:r k:k a:a n:n e:0 e:0 +cond:i 0:s 0:i +3sg:0'),
			('cond|1pl', 'e:e r:r k:k a:a n:n e:0 e:0 +cond:i 0:s 0:i +1pl:m 0:m 0:e'),
			('cond|2pl', 'e:e r:r k:k a:a n:n e:0 e:0 +cond:i 0:s 0:i +2pl:t 0:t 0:e'),
			('cond|3pl', 'e:e r:r k:k a:a n:n e:0 e:0 +cond:i 0:s 0:i +3pl:v 0:a 0:t'),
			('cond|conneg', 'e:e r:r k:k a:a n:n e:0 e:0 +cond:i 0:s 0:i +conneg:0'),
			('imper|2sg', 'e:e r:r k:k a:a n:n e:e e:0 +imper:0 +2sg:0'),
			('imper|2sg|conneg', 'e:e r:r k:k a:a n:n e:e e:0 +imper:0 +2sg:0 +conneg:0'),
		])

	# Pronouns

	def test_pronoun_mina(self):
		inflections = {
			"@base":  ['minä'],
			"sg|nom": ['minä'],
			"sg|gen": ['minun'],
			"sg|acc": ['minut'],
			"sg|par": ['minua'],
			"sg|ine": ['minussa'],
			"sg|ess": ['minuna'],
		}
		aligned = align(inflections, pos='pronoun')
		self.assertEqual(aligned, [
			('@base',  'm:m i:i n:n ä:ä'),
			('sg|nom', 'm:m i:i n:n ä:ä +sg:0 +nom:0'),
			('sg|gen', 'm:m i:i n:n ä:u +sg:0 +gen:n'),
			('sg|acc', 'm:m i:i n:n ä:u +sg:0 +acc:t'),
			('sg|par', 'm:m i:i n:n ä:u +sg:0 +par:a'),
			('sg|ine', 'm:m i:i n:n ä:u +sg:0 +ine:s 0:s 0:a'),
			('sg|ess', 'm:m i:i n:n ä:u +sg:0 +ess:n 0:a'),
		])

	def test_pronoun_mika(self):
		inflections = {
			"@base":  ['mikä'],
			"sg|nom": ['mikä'],
			"sg|gen": ['minkä'],
			"sg|par": ['mitä'],
			"sg|ine": ['missä'],
			"sg|ill": ['mihin'],
			"sg|all": ['mille', 'millekä'],
			"sg|ess": ['minä'],
			"pl|nom": ['mitkä'],
			"pl|gen": ['minkä'],
			"pl|par": ['mitä'],
			"pl|ine": ['missä'],
			"pl|ill": ['mihin'],
		}
		aligned = align(inflections, pos='pronoun')
		self.assertEqual(aligned, [
			('@base',  'm:m i:i k:k ä:ä'),
			('sg|nom', 'm:m i:i k:0 ä:0 +sg:0 +nom:0 0:k 0:ä'),
			('sg|gen', 'm:m i:i k:0 ä:0 +sg:0 +gen:n 0:k 0:ä'),
			('sg|par', 'm:m i:i k:0 ä:0 +sg:0 +par:t 0:ä'),
			('sg|ill', 'm:m i:i k:0 ä:0 +sg:0 +ill:h 0:i 0:n'),
			('sg|ine', 'm:m i:i k:0 ä:0 +sg:0 +ine:s 0:s 0:ä'),
			('sg|all', 'm:m i:i k:0 ä:0 +sg:0 +all:l 0:l 0:e'),
			('sg|all', 'm:m i:i k:0 ä:0 +sg:0 +all:l 0:l 0:e 0:k 0:ä'),
			('sg|ess', 'm:m i:i k:0 ä:0 +sg:0 +ess:n 0:ä'),
			('pl|nom', 'm:m i:i k:0 ä:0 +pl:t +nom:0 0:k 0:ä'),
			('pl|gen', 'm:m i:0 k:0 ä:0 +pl:i +gen:n 0:k 0:ä'),
			('pl|par', 'm:m i:0 k:0 ä:0 +pl:i +par:t 0:ä'),
			('pl|ill', 'm:m i:0 k:0 ä:0 +pl:i +ill:h 0:i 0:n'),
			('pl|ine', 'm:m i:0 k:0 ä:0 +pl:i +ine:s 0:s 0:ä'),
		])

	def test_pronoun_mikaan(self):
		inflections = {
			"@base":  ['mikään'],
			"sg|nom": ['mikään'],
			"sg|gen": ['minkään'],
			"sg|par": ['mitään'],
			"sg|ine": ['missään'],
			"sg|ill": ['mihinkään'],
			"sg|ess": ['minään'],
			"pl|nom": ['mitkään'],
			"pl|gen": ['minkään'],
			"pl|par": ['mitään'],
			"pl|ine": ['missään'],
			"pl|ill": ['mihinkään'],
		}
		aligned = align(inflections, pos='pronoun')
		self.assertEqual(aligned, [
			('@base',  'm:m i:i k:k ä:ä ä:ä n:n'),
			('sg|nom', 'm:m i:i k:0 ä:0 ä:0 n:0 +sg:0 +nom:0 0:k 0:ä 0:ä 0:n'),
			('sg|gen', 'm:m i:i k:0 ä:0 ä:0 n:0 +sg:0 +gen:n 0:k 0:ä 0:ä 0:n'),
			('sg|par', 'm:m i:i k:0 ä:0 ä:0 n:0 +sg:0 +par:t 0:ä 0:ä 0:n'),
			('sg|ill', 'm:m i:i k:0 ä:0 ä:0 n:0 +sg:0 +ill:h 0:i 0:n 0:k 0:ä 0:ä 0:n'),
			('sg|ine', 'm:m i:i k:0 ä:0 ä:0 n:0 +sg:0 +ine:s 0:s 0:ä 0:ä 0:n'),
			('sg|ess', 'm:m i:i k:0 ä:0 ä:0 n:0 +sg:0 +ess:n 0:ä 0:ä 0:n'),
			('pl|nom', 'm:m i:i k:0 ä:0 ä:0 n:0 +pl:t +nom:0 0:k 0:ä 0:ä 0:n'),
			('pl|gen', 'm:m i:0 k:0 ä:0 ä:0 n:0 +pl:i +gen:n 0:k 0:ä 0:ä 0:n'),
			('pl|par', 'm:m i:0 k:0 ä:0 ä:0 n:0 +pl:i +par:t 0:ä 0:ä 0:n'),
			('pl|ill', 'm:m i:0 k:0 ä:0 ä:0 n:0 +pl:i +ill:h 0:i 0:n 0:k 0:ä 0:ä 0:n'),
			('pl|ine', 'm:m i:0 k:0 ä:0 ä:0 n:0 +pl:i +ine:s 0:s 0:ä 0:ä 0:n'),

		])

	def test_pronoun_kukaan(self):
		inflections = {
			"@base":  ['kukaan'],
			"sg|nom": ['kukaan'],
			"sg|gen": ['kenenkään'],
			"sg|acc|rare": ['kenetkään'],  # Add to paradigm!!!
			"sg|par": ['ketään'],
			"sg|ine": ['kenessäkään'],
			"sg|ess": ['kenään'],
			"pl|nom": ['ketkään'],
			"pl|gen": ['keidenkään'],
			"pl|par": ['keitään'],
			"pl|ine": ['keissään'],
		}
		aligned = align(inflections, pos='pronoun')
		self.assertEqual(aligned, [
			('@base',  'k:k u:u k:k a:a a:a n:n'),
			('sg|nom', 'k:k u:u k:0 a:0 a:0 n:0 +sg:0 +nom:0 0:k 0:a 0:a 0:n'),
			('sg|gen', 'k:k u:e k:n a:e a:0 n:0 +sg:0 +gen:n 0:k 0:ä 0:ä 0:n'),
			('sg|acc|rare', 'k:k u:e k:n a:e a:0 n:0 +sg:0 +acc:t +rare:0 0:k 0:ä 0:ä 0:n'),
			('sg|par', 'k:k u:e k:0 a:0 a:0 n:0 +sg:0 +par:t 0:ä 0:ä 0:n'),
			('sg|ine', 'k:k u:e k:n a:e a:0 n:0 +sg:0 +ine:s 0:s 0:ä 0:k 0:ä 0:ä 0:n'),
			('sg|ess', 'k:k u:e k:0 a:0 a:0 n:0 +sg:0 +ess:n 0:ä 0:ä 0:n'),
			('pl|nom', 'k:k u:e k:0 a:0 a:0 n:0 +pl:t +nom:0 0:k 0:ä 0:ä 0:n'),
			('pl|gen', 'k:k u:e k:0 a:0 a:0 n:0 +pl:i 0:d 0:e +gen:n 0:k 0:ä 0:ä 0:n'),
			('pl|par', 'k:k u:e k:0 a:0 a:0 n:0 +pl:i +par:t 0:ä 0:ä 0:n'),
			('pl|ine', 'k:k u:e k:0 a:0 a:0 n:0 +pl:i +ine:s 0:s 0:ä 0:ä 0:n'),

		])

	def test_pronoun_jokin(self):
		inflections = {
			"@base":  ['jokin'],
			"sg|nom": ['jokin'],
			"sg|gen": ['jonkin'],
			"sg|par": ['jotakin', 'jotain'],
			"sg|ine": ['jossakin', 'jossain'],
			"sg|ess": ['jonakin', 'jonain'],
			"pl|nom": ['jotkin'],
			"pl|gen": ['joidenkin'],
			"pl|par": ['joitakin'],
			"pl|ine": ['joissakin'],
		}
		aligned = align(inflections, pos='pronoun')
		self.assertEqual(aligned, [
			('@base',  'j:j o:o k:k i:i n:n'),
			('sg|nom', 'j:j o:o k:0 i:0 n:0 +sg:0 +nom:0 0:k 0:i 0:n'),
			('sg|gen', 'j:j o:o k:0 i:0 n:0 +sg:0 +gen:n 0:k 0:i 0:n'),
			('sg|par', 'j:j o:o k:0 i:0 n:0 +sg:0 +par:t 0:a 0:k 0:i 0:n'),
			('sg|par', 'j:j o:o k:0 i:0 n:0 +sg:0 +par:t 0:a 0:i 0:n'),
			('sg|ine', 'j:j o:o k:0 i:0 n:0 +sg:0 +ine:s 0:s 0:a 0:k 0:i 0:n'),
			('sg|ine', 'j:j o:o k:0 i:0 n:0 +sg:0 +ine:s 0:s 0:a 0:i 0:n'),
			('sg|ess', 'j:j o:o k:0 i:0 n:0 +sg:0 +ess:n 0:a 0:k 0:i 0:n'),
			('sg|ess', 'j:j o:o k:0 i:0 n:0 +sg:0 +ess:n 0:a 0:i 0:n'),
			('pl|nom', 'j:j o:o k:0 i:0 n:0 +pl:t +nom:0 0:k 0:i 0:n'),
			('pl|gen', 'j:j o:o k:0 i:0 n:0 +pl:i 0:d 0:e +gen:n 0:k 0:i 0:n'),
			('pl|par', 'j:j o:o k:0 i:0 n:0 +pl:i +par:t 0:a 0:k 0:i 0:n'),
			('pl|ine', 'j:j o:o k:0 i:0 n:0 +pl:i +ine:s 0:s 0:a 0:k 0:i 0:n'),
		])

	def test_pronoun_joku(self):
		inflections = {
			"@base":  ['joku'],
			"sg|nom": ['joku'],
			"sg|gen": ['jonkun'],
			"sg|par": ['jotakuta'],
			"sg|ine": ['jossakussa'],
			"sg|ess": ['jonakuna'],
			"pl|nom": ['jotkut'],
			"pl|gen": ['joidenkuiden'],
			"pl|par": ['joitakuita'],
			"pl|ine": ['joissakuissa'],
		}
		aligned = align(inflections, pos='pronoun')
		self.assertEqual(aligned, [
			('@base',  'j:j o:o 0:0 0:0 0:0 0:0 k:k u:u'),
			('sg|nom', 'j:j o:o 0:0 0:0 0:0 0:0 k:k u:u +sg:0 +nom:0'),
			('sg|gen', 'j:j o:o 0:0 0:n 0:0 0:0 k:k u:u +sg:0 +gen:n'),
			('sg|par', 'j:j o:o 0:0 0:t 0:a 0:0 k:k u:u +sg:0 +par:t 0:a'),
			('sg|ine', 'j:j o:o 0:0 0:s 0:s 0:a k:k u:u +sg:0 +ine:s 0:s 0:a'),
			('sg|ess', 'j:j o:o 0:0 0:n 0:a 0:0 k:k u:u +sg:0 +ess:n 0:a'),
			('pl|nom', 'j:j o:o 0:t 0:0 0:0 0:0 k:k u:u +pl:t +nom:0'),
			('pl|gen', 'j:j o:o 0:i 0:d 0:e 0:n k:k u:u +pl:i 0:d 0:e +gen:n'),
			('pl|par', 'j:j o:o 0:i 0:t 0:a 0:0 k:k u:u +pl:i +par:t 0:a'),
			('pl|ine', 'j:j o:o 0:i 0:s 0:s 0:a k:k u:u +pl:i +ine:s 0:s 0:a'),
		])

	def test_pronoun_jompikumpi(self):
		inflections = {
			"@base":  ['jompikumpi'],
			"sg|nom": ['jompikumpi'],
			"sg|gen": ['jommankumman'],
			"sg|par": ['jompaakumpaa'],
			"sg|ine": ['jommassakummassa'],
			"sg|ess": ['jompanakumpana'],
			"pl|nom": ['jommatkummat'],
			"pl|gen": ['jompienkumpien'],
			"pl|par": ['jompiakumpia'],
			"pl|ine": ['jommissakummissa'],
		}
		aligned = align(inflections, pos='pronoun')
		self.assertEqual(aligned, [
			('@base',  'j:j o:o m:m p:p i:i 0:0 0:0 0:0 0:0 |:0 k:k u:u m:m p:p i:i'),
			('sg|nom', 'j:j o:o m:m p:p i:i 0:0 0:0 0:0 0:0 |:0 k:k u:u m:m p:p i:i +sg:0 +nom:0'),
			('sg|gen', 'j:j o:o m:m p:m i:a 0:0 0:n 0:0 0:0 |:0 k:k u:u m:m p:m i:a +sg:0 +gen:n'),
			('sg|par', 'j:j o:o m:m p:p i:a 0:0 0:a 0:0 0:0 |:0 k:k u:u m:m p:p i:a +sg:0 +par:a'),
			('sg|ine', 'j:j o:o m:m p:m i:a 0:0 0:s 0:s 0:a |:0 k:k u:u m:m p:m i:a +sg:0 +ine:s 0:s 0:a'),
			('sg|ess', 'j:j o:o m:m p:p i:a 0:0 0:n 0:a 0:0 |:0 k:k u:u m:m p:p i:a +sg:0 +ess:n 0:a'),
			('pl|nom', 'j:j o:o m:m p:m i:a 0:t 0:0 0:0 0:0 |:0 k:k u:u m:m p:m i:a +pl:t +nom:0'),
			('pl|gen', 'j:j o:o m:m p:p i:0 0:i 0:e 0:n 0:0 |:0 k:k u:u m:m p:p i:0 +pl:i 0:e +gen:n'),
			('pl|par', 'j:j o:o m:m p:p i:0 0:i 0:a 0:0 0:0 |:0 k:k u:u m:m p:p i:0 +pl:i +par:a'),
			('pl|ine', 'j:j o:o m:m p:m i:0 0:i 0:s 0:s 0:a |:0 k:k u:u m:m p:m i:0 +pl:i +ine:s 0:s 0:a'),
		])

	def test_pronoun_mikalie(self):
		inflections = {
			'@base': ['mikä|lie'],
			'sg|nom': ['mikälie'],
			'sg|gen': ['minkälie'],
			'sg|par': ['mitälie'],
			'sg|ill': ['mihinlie'],
			'sg|ine': ['missälie'],
			'sg|ela': ['mistälie'],
			'sg|all': ['millelie'],
			'sg|ade': ['millälie'],
			'sg|abl': ['miltälie'],
			'sg|tra': ['miksilie'],
			'sg|ess': ['minälie'],
			'pl|nom': ['mitkälie'],
			'pl|gen': ['minkälie'],
			'pl|par': ['mitälie'],
			'pl|ill': ['mihinlie'],
			'pl|ine': ['missälie'],
			'pl|ela': ['mistälie'],
			'pl|all': ['millelie'],
			'pl|ade': ['millälie'],
			'pl|abl': ['miltälie'],
			'pl|tra': ['miksilie'],
			'pl|ess': ['minälie'],
		}
		aligned = align(inflections, pos='pronoun')
		self.assertEqual(aligned, [
			('@base',  'm:m i:i k:k ä:ä |:| l:l i:i e:e'),
			('sg|nom', 'm:m i:i k:0 ä:0 |:0 l:0 i:0 e:0 +sg:0 +nom:0 0:k 0:ä 0:l 0:i 0:e'),
			('sg|gen', 'm:m i:i k:0 ä:0 |:0 l:0 i:0 e:0 +sg:0 +gen:n 0:k 0:ä 0:l 0:i 0:e'),
			('sg|par', 'm:m i:i k:0 ä:0 |:0 l:0 i:0 e:0 +sg:0 +par:t 0:ä 0:l 0:i 0:e'),
			('sg|ill', 'm:m i:i k:0 ä:0 |:0 l:0 i:0 e:0 +sg:0 +ill:h 0:i 0:n 0:l 0:i 0:e'),
			('sg|ine', 'm:m i:i k:0 ä:0 |:0 l:0 i:0 e:0 +sg:0 +ine:s 0:s 0:ä 0:l 0:i 0:e'),
			('sg|ela', 'm:m i:i k:0 ä:0 |:0 l:0 i:0 e:0 +sg:0 +ela:s 0:t 0:ä 0:l 0:i 0:e'),
			('sg|all', 'm:m i:i k:0 ä:0 |:0 l:0 i:0 e:0 +sg:0 +all:l 0:l 0:e 0:l 0:i 0:e'),
			('sg|ade', 'm:m i:i k:0 ä:0 |:0 l:0 i:0 e:0 +sg:0 +ade:l 0:l 0:ä 0:l 0:i 0:e'),
			('sg|abl', 'm:m i:i k:0 ä:0 |:0 l:0 i:0 e:0 +sg:0 +abl:l 0:t 0:ä 0:l 0:i 0:e'),
			('sg|ess', 'm:m i:i k:0 ä:0 |:0 l:0 i:0 e:0 +sg:0 +ess:n 0:ä 0:l 0:i 0:e'),
			('sg|tra', 'm:m i:i k:0 ä:0 |:0 l:0 i:0 e:0 +sg:0 +tra:k 0:s 0:i 0:l 0:i 0:e'),
			('pl|nom', 'm:m i:i k:0 ä:0 |:0 l:0 i:0 e:0 +pl:t +nom:0 0:k 0:ä 0:l 0:i 0:e'),
			('pl|gen', 'm:m i:0 k:0 ä:0 |:0 l:0 i:0 e:0 +pl:i +gen:n 0:k 0:ä 0:l 0:i 0:e'),
			('pl|par', 'm:m i:0 k:0 ä:0 |:0 l:0 i:0 e:0 +pl:i +par:t 0:ä 0:l 0:i 0:e'),
			('pl|ill', 'm:m i:0 k:0 ä:0 |:0 l:0 i:0 e:0 +pl:i +ill:h 0:i 0:n 0:l 0:i 0:e'),
			('pl|ine', 'm:m i:0 k:0 ä:0 |:0 l:0 i:0 e:0 +pl:i +ine:s 0:s 0:ä 0:l 0:i 0:e'),
			('pl|ela', 'm:m i:0 k:0 ä:0 |:0 l:0 i:0 e:0 +pl:i +ela:s 0:t 0:ä 0:l 0:i 0:e'),
			('pl|all', 'm:m i:0 k:0 ä:0 |:0 l:0 i:0 e:0 +pl:i +all:l 0:l 0:e 0:l 0:i 0:e'),
			('pl|ade', 'm:m i:0 k:0 ä:0 |:0 l:0 i:0 e:0 +pl:i +ade:l 0:l 0:ä 0:l 0:i 0:e'),
			('pl|abl', 'm:m i:0 k:0 ä:0 |:0 l:0 i:0 e:0 +pl:i +abl:l 0:t 0:ä 0:l 0:i 0:e'),
			('pl|ess', 'm:m i:0 k:0 ä:0 |:0 l:0 i:0 e:0 +pl:i +ess:n 0:ä 0:l 0:i 0:e'),
			('pl|tra', 'm:m i:0 k:0 ä:0 |:0 l:0 i:0 e:0 +pl:i +tra:k 0:s 0:i 0:l 0:i 0:e'),
		])

	def test_pronoun_pl_molemmat(self):
		inflections = {
			'@base': ['molemmat'],
			'@stem:possessives:nom': ['molempa'],
			'gen': ['molempien'],
			'gen|rare': ['molempain'],
			'par': ['molempia'],
			'ill': ['molempiin'],
			'ine': ['molemmissa'],
			'ess': ['molempina'],
			'nom': ['molemmat'],
			'all': ['molemmille'],
			'ade': ['molemmilla'],
			'abl': ['molemmilta'],
			'ela': ['molemmista'],
			'tra': ['molemmiksi'],
			'abe': ['molemmitta'],
			'ins': ['molemmin'],
			'com': ['molempine'],
		}
		aligned = align(inflections, pos='pronoun-pl')
		self.assertEqual(aligned, [
			('@base',                    'm:m o:o l:l e:e m:m m:m a:a t:t'),
			('@stem:possessives:nom',    'm:m o:o l:l e:e m:m m:p a:a t:0'),
			('nom',                      'm:m o:o l:l e:e m:m m:m a:a t:t +nom:0'),
			('gen',                      'm:m o:o l:l e:e m:m m:p a:0 t:i 0:e +gen:n'),
			('gen|rare',                 'm:m o:o l:l e:e m:m m:p a:a t:i +gen:n +rare:0'),
			('par',                      'm:m o:o l:l e:e m:m m:p a:0 t:i +par:a'),
			('ill',                      'm:m o:o l:l e:e m:m m:p a:0 t:i +ill:i 0:n'),
			('ine',                      'm:m o:o l:l e:e m:m m:m a:0 t:i +ine:s 0:s 0:a'),
			('ela',                      'm:m o:o l:l e:e m:m m:m a:0 t:i +ela:s 0:t 0:a'),
			('all',                      'm:m o:o l:l e:e m:m m:m a:0 t:i +all:l 0:l 0:e'),
			('ade',                      'm:m o:o l:l e:e m:m m:m a:0 t:i +ade:l 0:l 0:a'),
			('abl',                      'm:m o:o l:l e:e m:m m:m a:0 t:i +abl:l 0:t 0:a'),
			('ess',                      'm:m o:o l:l e:e m:m m:p a:0 t:i +ess:n 0:a'),
			('tra',                      'm:m o:o l:l e:e m:m m:m a:0 t:i +tra:k 0:s 0:i'),
			('abe',                      'm:m o:o l:l e:e m:m m:m a:0 t:i +abe:t 0:t 0:a'),
			('com',                      'm:m o:o l:l e:e m:m m:p a:0 t:i +com:n 0:e'),
			('ins',                      'm:m o:o l:l e:e m:m m:m a:0 t:i +ins:n'),
		])

	def test_pronoun_pl_me(self):
		inflections = {
			'@base': ['me'],
			'nom': ['me'],
			'gen': ['meidän'],
			'acc': ['meidät'],
			'par': ['meitä'],
			'ill': ['meihin'],
			'ine': ['meissä'],
			'ela': ['meistä'],
			'all': ['meille'],
			'ade': ['meillä'],
			'abl': ['meiltä'],
			'ess': ['meinä'],
			'tra': ['meiksi'],
			'abe': ['meittä'],
		}
		aligned = align(inflections, pos='pronoun-pl')
		self.assertEqual(aligned, [
			('@base', 'm:m e:e 0:0'),
			('nom',   'm:m e:e 0:0 +nom:0'),
			('gen',   'm:m e:e 0:i 0:d 0:ä +gen:n'),
			('acc',   'm:m e:e 0:i 0:d 0:ä +acc:t'),
			('par',   'm:m e:e 0:i +par:t 0:ä'),
			('ill',   'm:m e:e 0:i +ill:h 0:i 0:n'),
			('ine',   'm:m e:e 0:i +ine:s 0:s 0:ä'),
			('ela',   'm:m e:e 0:i +ela:s 0:t 0:ä'),
			('all',   'm:m e:e 0:i +all:l 0:l 0:e'),
			('ade',   'm:m e:e 0:i +ade:l 0:l 0:ä'),
			('abl',   'm:m e:e 0:i +abl:l 0:t 0:ä'),
			('ess',   'm:m e:e 0:i +ess:n 0:ä'),
			('tra',   'm:m e:e 0:i +tra:k 0:s 0:i'),
			('abe',   'm:m e:e 0:i +abe:t 0:t 0:ä'),
		])

	# Adverbs

	def test_adverb_mukavasti(self):
		inflections = {
			"@base":  ['mukavasti'],
			"": ['mukavasti'],
			"comparative": ['mukavammin'],
			"comparative|nstd": ['mukavemmin'],
			"superlative": ['mukavimmin', 'mukaviten'],
		}
		aligned = align(inflections, pos='adverb')
		self.assertEqual(aligned, [
			('@base',       'm:m u:u k:k a:a v:v a:a s:s t:t i:i'),
			('',            'm:m u:u k:k a:a v:v a:a s:s t:t i:i'),
			('comparative', 'm:m u:u k:k a:a v:v a:a s:0 t:0 i:0 +comparative:m 0:m 0:i 0:n'),
			('superlative', 'm:m u:u k:k a:a v:v a:0 s:0 t:0 i:0 +superlative:i 0:m 0:m 0:i 0:n'),
			('superlative', 'm:m u:u k:k a:a v:v a:0 s:0 t:0 i:0 +superlative:i 0:t 0:e 0:n'),
			('comparative|nstd', 'm:m u:u k:k a:a v:v a:e s:0 t:0 i:0 +comparative:m 0:m 0:i 0:n +nstd:0'),
		])

	def test_adverb_lujaa(self):
		inflections = {
			"@base":  ['lujaa'],
			"": ['lujaa'],
			"comparative": ['lujempaa'],
			"superlative": ['lujimpaa', 'lujiten'],
		}
		aligned = align(inflections, pos='adverb')
		self.assertEqual(aligned, [
			('@base', 'l:l u:u j:j a:a a:a'),
			('',      'l:l u:u j:j a:a a:a'),
			('comparative', 'l:l u:u j:j a:e a:0 +comparative:m 0:p 0:a 0:a'),
			('superlative', 'l:l u:u j:j a:0 a:0 +superlative:i 0:m 0:p 0:a 0:a'),
			('superlative', 'l:l u:u j:j a:0 a:0 +superlative:i 0:t 0:e 0:n'),
		])

	def test_adverb_kauas(self):
		inflections = {
			"@base":  ['kauas'],
			"": ['kauas'],
			"comparative": ['kauemmas'],
			"superlative": ['kauimmas'],
		}
		aligned = align(inflections, pos='adverb')
		self.assertEqual(aligned, [
			('@base', 'k:k a:a u:u a:a s:s'),
			('', 'k:k a:a u:u a:a s:s'),
			('comparative', 'k:k a:a u:u a:e s:0 +comparative:m 0:m 0:a 0:s'),
			('superlative', 'k:k a:a u:u a:0 s:0 +superlative:i 0:m 0:m 0:a 0:s'),
		])

	def test_adverb_kaukaa(self):
		inflections = {
			"@base":  ['kaukaa'],
			"": ['kaukaa'],
			"comparative": ['kauempaa'],
			"superlative": ['kauimpaa'],
		}
		aligned = align(inflections, pos='adverb')
		self.assertEqual(aligned, [
			('@base', 'k:k a:a u:u k:k a:a a:a'),
			('', 'k:k a:a u:u k:k a:a a:a'),
			('comparative', 'k:k a:a u:u k:0 a:e a:0 +comparative:m 0:p 0:a 0:a'),
			('superlative', 'k:k a:a u:u k:0 a:0 a:0 +superlative:i 0:m 0:p 0:a 0:a'),
		])

	def test_adverb_kaukana(self):
		inflections = {
			"@base":  ['kaukana'],
			"": ['kaukana'],
			"comparative": ['kauempana'],
			"superlative": ['kauimpana'],
		}
		aligned = align(inflections, pos='adverb')
		self.assertEqual(aligned, [
			('@base', 'k:k a:a u:u k:k a:a n:n a:a'),
			('', 'k:k a:a u:u k:k a:a n:n a:a'),
			('comparative', 'k:k a:a u:u k:0 a:e n:0 a:0 +comparative:m 0:p 0:a 0:n 0:a'),
			('superlative', 'k:k a:a u:u k:0 a:0 n:0 a:0 +superlative:i 0:m 0:p 0:a 0:n 0:a'),
		])

	def test_adverb_kauan(self):
		inflections = {
			"@base":  ['kauan'],
			"": ['kauan'],
			"comparative": ['kauemmin'],
			"superlative": ['kauimmin', 'kauiten'],
		}
		aligned = align(inflections, pos='adverb')
		self.assertEqual(aligned, [
			('@base', 'k:k a:a u:u a:a n:n'),
			('', 'k:k a:a u:u a:a n:n'),
			('comparative', 'k:k a:a u:u a:e n:0 +comparative:m 0:m 0:i 0:n'),
			('superlative', 'k:k a:a u:u a:0 n:0 +superlative:i 0:m 0:m 0:i 0:n'),
			('superlative', 'k:k a:a u:u a:0 n:0 +superlative:i 0:t 0:e 0:n'),
		])

	def test_adverb_helpolla(self):
		inflections = {
			"@base":  ['helpolla'],
			"": ['helpolla'],
			"comparative": ['helpommalla'],
			"superlative": ['helpoimmalla'],
		}
		aligned = align(inflections, pos='adverb')
		self.assertEqual(aligned, [
			('@base', 'h:h e:e l:l p:p o:o l:l l:l a:a'),
			('', 'h:h e:e l:l p:p o:o l:l l:l a:a'),
			('comparative', 'h:h e:e l:l p:p o:o l:0 l:0 a:0 +comparative:m 0:m 0:a 0:l 0:l 0:a'),
			('superlative', 'h:h e:e l:l p:p o:o l:0 l:0 a:0 +superlative:i 0:m 0:m 0:a 0:l 0:l 0:a'),
		])

	def test_adverb_syrjaan(self):
		inflections = {
			"@base":  ['syrjään'],
			"": ['syrjään'],
			"comparative": ['syrjempään'],
		}
		aligned = align(inflections, pos='adverb')
		self.assertEqual(aligned, [
			('@base', 's:s y:y r:r j:j ä:ä ä:ä n:n'),
			('', 's:s y:y r:r j:j ä:ä ä:ä n:n'),
			('comparative', 's:s y:y r:r j:j ä:e ä:0 n:0 +comparative:m 0:p 0:ä 0:ä 0:n'),
		])

	def test_adverb_pian(self):
		inflections = {
			"@base":  ['pian'],
			"": ['pian'],
			"comparative": ['pikemmin'],
			"superlative": ['pikimmin'],
		}
		aligned = align(inflections, pos='adverb')
		self.assertEqual(aligned, [
			('@base', 'p:p i:i 0:0 a:a n:n'),
			('', 'p:p i:i 0:0 a:a n:n'),
			('comparative', 'p:p i:i 0:k a:e n:0 +comparative:m 0:m 0:i 0:n'),
			('superlative', 'p:p i:i 0:k a:0 n:0 +superlative:i 0:m 0:m 0:i 0:n'),
		])