import re

from tools.utils import syllabify

V = '[aeioyuäö]'
C = '[^aeiouyäö]'

IRREGULAR_ACTIONS = {
	'hajota': ['hajonta'],
	'hakea': ['haku', 'haenta'],
	'hallita': ['hallinta'],
	'harkita': ['harkinta'],
	'hillitä': ['hillintä'],
	'hoitaa': ['hoito'],
	'hokea': ['hoku', 'hoenta'],
	'holhota': ['holhonta'],
	'huolita': ['huolinta'],
	'huutaa': ['huuto'],
	'hyytää': ['hyytö'],
	'hyötää': ['hyötö'],
	'häiritä': ['häirintä'],
	'häätää': ['häätö'],
	'imeä': ['imu', 'imentä'],
	'iskeä': ['isku', 'iskentä'],
	'itkeä': ['itku', 'itkentä'],
	'juosta': ['juoksu'],
	'kaataa': ['kaato'],
	'kaitsea': ['kaitsenta'],
	'karhita': ['karhinta'],
	'kaulita': ['kaulinta'],
	'kaupita': ['kaupinta'],
	'keritä': ['kerintä'],
	'kestitä': ['kestitys'],
	'kiitää': ['kiito'],
	'kitkeä': ['kitkentä'],
	'kulkea': ['kulku', 'kuljenta'],
	'kuohita': ['kuohinta'],
	'kuohuta': ['kuohunta'],
	'kutea': ['kutu', 'kudenta'],
	'kytkeä': ['kytky', 'kytkentä'],
	'kätkeä': ['kätkentä'],
	'laskea': ['lasku', 'laskenta'],
	'levitä': ['levintä'],
	'liitää': ['liito'],
	'loiskuta': ['loiskunta'],
	'lukea': ['luku', 'luenta'],
	'lumota': ['lumonta', 'lumous'],
	'lähteä': ['lähtö'],
	'lääkitä': ['lääkintä'],
	'mainita': ['maininta'],
	'merkitä': ['merkintä'],
	'muodota': ['muodonta'],
	'niellä': ['nielentä'],
	'noutaa': ['nouto'],
	'nuolla': ['nuolenta'],
	'nylkeä': ['nylky', 'nyljentä'],
	'nähdä': ['näkö'],
	'olla': ['olo'],
	'parkita': ['parkinta'],
	'pitää': ['pito'],
	'polkea': ['poljenta'],
	'punnita': ['punninta'],
	'purra': ['purenta'],
	'puskea': ['pusku', 'puskenta'],
	'rosvota': ['rosvous'],
	'sietää': ['sieto'],
	'siivota': ['siivous'],
	'sirota': ['sironta'],
	'solmita': ['solminta'],
	'sulkea': ['sulku', 'suljenta'],
	'suotaa': ['suoto'],
	'surra': ['surenta'],
	'sylkeä': ['sylky', 'syljentä'],
	'säätää': ['säätö'],
	'tajuta': ['tajunta'],
	'tappaa': ['tappo'],
	'tarjota': ['tarjonta'],
	'tehdä': ['teko'],
	'tilkitä': ['tilkintä'],
	'tukea': ['tuenta'],
	'tulkita': ['tulkinta'],
	'tulla': ['tulo'],
	'valita': ['valinta'],
	'vetää': ['veto'],
	'vuolla': ['vuolu', 'vuolenta'],
	'vuotaa': ['vuoto'],
}


def derive_action_noun(inflections):

	[lemma] = inflections['@base']

	if lemma in IRREGULAR_ACTIONS:
		return IRREGULAR_ACTIONS[lemma]

	a = lemma[-1]
	u = 'u' if a == 'a' else 'y'

	syllabified = syllabify(lemma, compound=False)
	syllable_count = len(syllabified.split('·'))

	# "harpata", "jankata", "jodlata",
	# => "harppaus", "jankkaus", "jodlaus"
	if re.fullmatch('.+(ata|ätä)', lemma):
		[harppaan] = inflections['pres|1sg']
		harppa = harppaan[:-2]
		result = [f'{harppa}{u}s']
		return result

	# "luoda", "käydä", "uida", "myydä", "lyödä," "soida", "organisoida", "isännöidä"
	# => "luonti", "käynti", "uinti", "myynti", "lyönti", "sointi", "organisointi", "isännöinti"
	if re.fullmatch('.+(da|dä)', lemma):
		voi = lemma[:-2]
		result = [f'{voi}nti']
		return result

	# "puraista", "hipaista", "tönäistä"
	# => "puraisu", "hipaisu", "tönäisy"
	if re.fullmatch('.+(aista|äistä)', lemma):
		hipais = lemma[:-2]
		result = [f'{hipais}{u}']
		return result

	# "tapella", "arkailla"
	# => "tappelu", "arkailu"
	if re.fullmatch('.+(ella|ellä|illa|illä)', lemma) and syllable_count > 2:
		[tappelevat] = inflections['pres|3pl']
		tappel = tappelevat[:-4]
		result = [f'{tappel}{u}']
		return result

	# "narista", "vapista", "turista", "hälistä"
	# => "narina", "vapina", "turina", "hälinä"
	if re.fullmatch(f'.+{C}(ista|istä)', lemma):
		vapi = lemma[:-3]
		result = [f'{vapi}n{a}']
		return result

	# "paheksua", "väheksyä"
	# => "paheksunta", "väheksyntä"
	if re.fullmatch(f'.+ks(ua|yä)', lemma):
		[paheksun] = inflections['pres|1sg']
		result = [f'{paheksun}t{a}']
		return result

	# "rakentaa", "pakertaa", "verottaa", "välittää", "puhdistaa", "inahtaa", "ärsyttää"
	# => "rakennus", "pakerrus", "verotus", "välitys", "puhdistus", "inahdus", "ärsytys"
	if re.fullmatch('.+(tää|taa)', lemma) and syllable_count == 3:
		[rakennan] = inflections['pres|1sg']
		rakenn = rakennan[:-2]
		result = [f'{rakenn}{u}s']
		return result

	"""
	The cases below may be dubious
	"""

	# "oirehtia", "hyljeksiä"
	# => "oirehdinta", "hyljeksintä" (?)
	if re.fullmatch('.+(ia|iä)', lemma) and syllable_count == 4:
		[oirehdin] = inflections['pres|1sg']
		result = [f'{oirehdin}t{a}']
		return result

	# "kestää", "antaa", "ottaa", "paistaa", "viettää", "kantaa", "paahtaa", "huoltaa", "kääntää", "työntää"
	# => "kesto", "anto", "otto", "paisto", "vietto", "kanto", "paahto", "huolto", "kääntö", "työntö" (?)
	if re.fullmatch(f'.+({C}tää|{C}taa)', lemma) and syllable_count == 2:
		viett = lemma[:-2]
		o = 'ö' if re.findall('[äöy]', viett) else 'o'
		result = [f'{viett}{o}']
		return result

	# "toimia", "huuhtoa", "hyppiä", "astua", "liittyä"
	# => "toiminta", "huuhdonta", "hypintä", "astunta", "liityntä" (?)
	if re.fullmatch('.+(oa|öä|ua|yä|ia|iä)', lemma) and syllable_count == 3:
		[huuhdon] = inflections['pres|1sg']
		result = [f'{huuhdon}t{a}']
		return result

	return []


def derive_agent_noun(inflections):

	result = []
	for kulkevat in inflections.get('pres|3pl', []) + inflections.get('pres|3pl|rare', []):
		a = kulkevat[-2]
		kulki = kulkevat[:-4] + 'i' if kulkevat[-4] == 'e' else kulkevat[:-3]
		result.append(f'{kulki}j{a}')
	return result


"""
for row in read_list_tsv('lexicon.tsv'):

	_, lemma, hom, pos, kotus_class, grad, harmony, _, info, _ = row

	if '|' in lemma or '-' in lemma:
		continue

	if pos != 'verb':
		continue

	inflections = inflect(lemma, pos, kotus_class, grad, harmony)

	derive_agent(inflections)
	derive_action(inflections)
"""