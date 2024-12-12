import re
import copy
from collections import defaultdict
from scripts.inflection.utils import \
	C, V, VV, \
	grad_strong, grad_weak, \
	HARMONY_MAPPING, determine_harmony, determine_stem_vowel, \
	plural2singular, merge_inflections
from scripts.utils import ADVERB_INFLECTIONS, clean
from scripts.inflection.verb_derivations import derive_agent_noun, derive_action_noun


def get_comparison(adjective, inflections, kotus_class=''):

	"""
	Return all possible comparatives and superlatives for given Finnish adjective.
	"""

	parts = re.split('([|-])', adjective)
	base = parts.pop()
	sika = ''.join(parts)
	all_forms = defaultdict(list)

	if not inflections:
		all_forms['comparative'] = []
		all_forms['superlative'] = []

	elif adjective != base == 'hyvä':
		all_forms['comparative'] = []
		all_forms['superlative'] = []

	elif adjective == 'hyvä':
		all_forms['comparative'] = ['parempi']
		all_forms['superlative'] = ['paras', 'parhain']
		all_forms['comparative|nstd'] = ['hyvempi']

	elif base == 'kiva':
		all_forms['comparative'] = [f'{sika}kivempi', f'{sika}kivampi']
		all_forms['superlative'] = [f'{sika}kivin', f'{sika}kivoin']

	elif base == 'pitkä':
		all_forms['comparative'] = [f'{sika}pitempi', f'{sika}pidempi']
		all_forms['superlative'] = [f'{sika}pisin']

	elif base == 'lyhyt':
		all_forms['comparative'] = [f'{sika}lyhyempi', f'{sika}lyhempi']
		all_forms['superlative'] = [f'{sika}lyhyin', f'{sika}lyhin']

	# "vasen", "ainut", "paras" => ei komparaatiota
	elif adjective in ['vasen', 'ainut', 'paras']:
		all_forms['comparative'] = []
		all_forms['superlative'] = []

	# "alempi", "enempi", "alin", "enin" => ei komparaatiota
	elif kotus_class in ['16', '36']:
		all_forms['comparative'] = []
		all_forms['superlative'] = []

	# "kuiva", "kova", "niukka"
	elif base in ["kuiva", "kova", "niukka"]:
		niuk = inflections['sg|gen'][0][:-2]
		all_forms['comparative'] = [f'{niuk}empi']
		all_forms['superlative'] = inflections['pl|ins']

	# kaksitavuiset: "syvä", "kuuma", "turta"
	elif kotus_class in ['10'] and re.fullmatch(f'{C}*{VV}{C}+{V}', base):
		turr = inflections['sg|gen'][0][:-2]
		all_forms['comparative'] = [f'{turr}empi']
		all_forms['superlative'] = inflections['pl|ins']

	# useampitavuiset: "mukava", "huutava", "juureva", "terävä", "uskova"
	elif kotus_class in ['10']:
		mukava = inflections['sg|gen'][0][:-1]
		mukav = inflections['sg|gen'][0][:-2]
		all_forms['comparative'] = [f'{mukava}mpi']
		all_forms['superlative'] = inflections['pl|ins']
		all_forms['comparative|nstd'] = [f'{mukav}empi']

	# "tarkka", "hauska"
	elif kotus_class in ["9", "10"]:
		tark = inflections['sg|gen'][0][:-2]
		all_forms['comparative'] = [f'{tark}empi']
		all_forms['superlative'] = [f'{tark}in']

	# "punakka", "tomäkkä"
	elif kotus_class in ["14"]:
		punaka = inflections['sg|gen'][0][:-1]
		all_forms['comparative'] = [f'{punaka}mpi']
		all_forms['superlative'] = inflections['pl|ins']

	# "kaunis", "aulis", "valmis", "altis", "kallis"
	elif kotus_class in ["41"] and adjective.endswith('is'):
		kaun = inflections['sg|gen'][0][:-3]
		all_forms['comparative'] = [f'{kaun}iimpi']
		all_forms['superlative'] = [f'{kaun}ein']
		all_forms['superlative|poet'] = [f'{kaun}ehin']

	# "huono", "juoppo", "luokaton"
	elif kotus_class:
		juopo = inflections['sg|gen'][0][:-1]
		all_forms['comparative'] = [f'{juopo}mpi']
		all_forms['superlative'] = inflections['pl|ins']

	return clean(all_forms)


def inflect_noun(word, kotus_class, gradtype=None, harmony=None, vowel=None):

	"""
	Return all possible numbers and cases of given Finnish noun, adjective, ordinal number etc.
	"""

	vowel = vowel or determine_stem_vowel(word, kotus_class)
	harmony = harmony or determine_harmony(word, kotus_class)
	a, o, u, aa, oo, _ = HARMONY_MAPPING[harmony]

	if not kotus_class:
		return {'': [word], '@base': [word]}

	all_forms = defaultdict(list)
	all_forms['sg|nom'] = [word]

	# "meri", "veri"
	if kotus_class in ["24", "26"] and re.fullmatch(".*(meri|veri)", word):
		mer = word[:-1]
		#
		all_forms['sg|gen'] = [f"{mer}en"]
		all_forms['sg|par'] = [f"{mer}ta"]
		all_forms['sg|ill'] = [f"{mer}een"]
		all_forms['pl|gen'] = [f"{mer}ien", f"{mer}ten"]
		all_forms['pl|par'] = [f"{mer}iä"]
		all_forms['pl|ill'] = [f"{mer}iin"]
		all_forms['pl|ine'] = [f"{mer}issä"]
		all_forms['sg|ess'] = [f"{mer}enä"]
		all_forms['pl|ess'] = [f"{mer}inä"]

	# "veli"
	elif kotus_class == "7" and word.endswith("veli"):
		iso = word[:-4]
		#
		all_forms['sg|gen'] = [f"{iso}veljen"]
		all_forms['sg|par'] = [f"{iso}veljeä"]
		all_forms['sg|ill'] = [f"{iso}veljeen"]
		all_forms['pl|gen'] = [f"{iso}veljien"]
		all_forms['pl|par'] = [f"{iso}veljiä"]
		all_forms['pl|ill'] = [f"{iso}veljiin"]
		all_forms['pl|ine'] = [f"{iso}veljissä"]
		all_forms['sg|ess'] = [f"{iso}veljenä"]
		all_forms['pl|ess'] = [f"{iso}veljinä"]

	# "valo"
	elif kotus_class == "1":
		katto = word
		kattoo = katto + vowel
		kato = grad_weak(word, gradtype)
		#
		all_forms['sg|gen'] = [f"{kato}n"]
		all_forms['sg|par'] = [f"{katto}{a}"]
		all_forms['sg|ill'] = [f"{kattoo}n"]
		all_forms['pl|gen'] = [f"{katto}jen"]
		all_forms['pl|par'] = [f"{katto}j{a}"]
		all_forms['pl|ill'] = [f"{katto}ihin"]
		all_forms['pl|ine'] = [f"{kato}iss{a}"]
		all_forms['sg|ess'] = [f"{katto}n{a}"]
		all_forms['pl|ess'] = [f"{katto}in{a}"]

	# "€"
	elif kotus_class == "1B":
		d = word
		#
		all_forms['sg|nom'] = [f"{d}"]
		all_forms['sg|gen'] = [f"{d}:n"]
		all_forms['sg|par'] = [f"{d}:{a}"]
		all_forms['sg|ill'] = [f"{d}:{oo}n", f"{d}:{o}n"]
		all_forms['pl|gen'] = [f"{d}:jen"]
		all_forms['pl|par'] = [f"{d}:j{a}"]
		all_forms['pl|ill'] = [f"{d}:ihin"]
		all_forms['pl|ine'] = [f"{d}:iss{a}"]
		all_forms['sg|ess'] = [f"{d}:n{a}"]
		all_forms['pl|ess'] = [f"{d}:in{a}"]
		all_forms['@stem:clitics'] = [f"{d}:"]

	# "palvelu"
	elif kotus_class == "2":
		palvelu = word
		palveluu = palvelu + vowel
		#
		all_forms['sg|gen'] = [f"{palvelu}n"]
		all_forms['sg|par'] = [f"{palvelu}{a}"]
		all_forms['sg|ill'] = [f"{palveluu}n"]
		all_forms['pl|gen'] = [f"{palvelu}jen", f"{palvelu}iden", f"{palvelu}itten"]
		all_forms['pl|par'] = [f"{palvelu}j{a}", f"{palvelu}it{a}"]
		all_forms['pl|ill'] = [f"{palvelu}ihin"]
		all_forms['pl|ine'] = [f"{palvelu}iss{a}"]
		all_forms['sg|ess'] = [f"{palvelu}n{a}"]
		all_forms['pl|ess'] = [f"{palvelu}in{a}"]

	# "valtio"
	elif kotus_class == "3":
		valtio = word
		valtioo = word + vowel
		#
		all_forms['sg|gen'] = [f"{valtio}n"]
		all_forms['sg|par'] = [f"{valtio}t{a}"]
		all_forms['sg|ill'] = [f"{valtioo}n"]
		all_forms['pl|gen'] = [f"{valtio}iden", f"{valtio}itten"]
		all_forms['pl|par'] = [f"{valtio}it{a}"]
		all_forms['pl|ill'] = [f"{valtio}ihin"]
		all_forms['pl|ine'] = [f"{valtio}iss{a}"]
		all_forms['sg|ess'] = [f"{valtio}n{a}"]
		all_forms['pl|ess'] = [f"{valtio}in{a}"]
		all_forms['pl|gen|nstd'] = [f"{valtio}jen"]

	# "laatikko"
	elif kotus_class == "4":
		laatikko = word
		laatiko = grad_weak(word, gradtype)
		#
		all_forms['sg|gen'] = [f"{laatiko}n"]
		all_forms['sg|par'] = [f"{laatikko}{a}"]
		all_forms['sg|ill'] = [f"{laatikko}{o}n"]
		all_forms['pl|gen'] = [f"{laatikko}jen", f"{laatiko}iden", f"{laatiko}itten"]
		all_forms['pl|par'] = [f"{laatikko}j{a}", f"{laatiko}it{a}"]
		all_forms['pl|ill'] = [f"{laatikko}ihin", f"{laatiko}ihin"]
		all_forms['pl|ine'] = [f"{laatiko}iss{a}"]
		all_forms['sg|ess'] = [f"{laatikko}n{a}"]
		all_forms['pl|ess'] = [f"{laatikko}in{a}"]

	# "risti"
	elif kotus_class == "5" and word.endswith('i'):
		takki = word
		takke = takki[:-1] + 'e'
		taki = grad_weak(takki, gradtype)
		take = grad_weak(takke, gradtype)
		#
		all_forms['sg|gen'] = [f"{taki}n"]
		all_forms['sg|par'] = [f"{takki}{a}"]
		all_forms['sg|ill'] = [f"{takki}in"]
		all_forms['pl|gen'] = [f"{takki}en"]
		all_forms['pl|par'] = [f"{takke}j{a}"]
		all_forms['pl|ill'] = [f"{takke}ihin"]
		all_forms['pl|ine'] = [f"{take}iss{a}"]
		all_forms['sg|ess'] = [f"{takki}n{a}"]
		all_forms['pl|ess'] = [f"{takke}in{a}"]
		all_forms['pl|gen|nstd'] = [f"{takke}jen"]

	# "pop"
	elif kotus_class == "5":
		pop = word
		popi = word + 'i'
		popp = grad_strong(popi, gradtype)[:-1]
		all_forms['sg|nom'] = [f"{pop}"]
		all_forms['sg|gen'] = [f"{pop}in"]
		all_forms['sg|par'] = [f"{popp}i{a}"]
		all_forms['sg|ill'] = [f"{popp}iin"]
		all_forms['pl|gen'] = [f"{popp}ien"]
		all_forms['pl|par'] = [f"{popp}ej{a}"]
		all_forms['pl|ill'] = [f"{popp}eihin"]
		all_forms['pl|ine'] = [f"{pop}eiss{a}"]
		all_forms['sg|ess'] = [f"{popp}in{a}"]
		all_forms['pl|ess'] = [f"{popp}ein{a}"]
		all_forms['pl|gen|nstd'] = [f"{popp}ejen"]

	# "%"
	elif kotus_class == "5B":
		p = word
		#
		all_forms['sg|gen'] = [f"{p}:n"]
		all_forms['sg|par'] = [f"{p}:i{a}", f"{p}:{a}"]
		all_forms['sg|ill'] = [f"{p}:iin"]
		all_forms['pl|gen'] = [f"{p}:ien"]
		all_forms['pl|par'] = [f"{p}:ej{a}"]
		all_forms['pl|ill'] = [f"{p}:eihin"]
		all_forms['pl|ine'] = [f"{p}:eiss{a}"]
		all_forms['sg|ess'] = [f"{p}:in{a}"]
		all_forms['pl|ess'] = [f"{p}:ein{a}"]
		all_forms['@stem:clitics'] = [f"{p}:"]

	# "paperi"
	elif kotus_class == "6":
		paper = word[:-1] if word[-1] == "i" else word
		#
		all_forms['sg|gen'] = [f"{paper}in"]
		all_forms['sg|par'] = [f"{paper}i{a}"]
		all_forms['sg|ill'] = [f"{paper}iin"]
		all_forms['pl|gen'] = [f"{paper}eiden", f"{paper}eitten", f"{paper}ien"]
		all_forms['pl|par'] = [f"{paper}eit{a}", f"{paper}ej{a}"]
		all_forms['pl|ill'] = [f"{paper}eihin"]
		all_forms['pl|ine'] = [f"{paper}eiss{a}"]
		all_forms['sg|ess'] = [f"{paper}in{a}"]
		all_forms['pl|ess'] = [f"{paper}ein{a}"]

	# "$"
	elif kotus_class == "6B":
		d = word
		#
		all_forms['sg|nom'] = [f"{d}"]
		all_forms['sg|gen'] = [f"{d}:in"]
		all_forms['sg|par'] = [f"{d}:i{a}"]
		all_forms['sg|ill'] = [f"{d}:iin"]
		all_forms['pl|gen'] = [f"{d}:eiden", f"{d}:eitten", f"{d}:ien"]
		all_forms['pl|par'] = [f"{d}:eit{a}", f"{d}:ej{a}"]
		all_forms['pl|ill'] = [f"{d}:eihin"]
		all_forms['pl|ine'] = [f"{d}:eiss{a}"]
		all_forms['sg|ess'] = [f"{d}:in{a}"]
		all_forms['pl|ess'] = [f"{d}:ein{a}"]
		all_forms['@stem:clitics'] = [f"{d}:"]

	# "ovi", "kolme"
	elif kotus_class == "7":
		kaikki = word[:-1] + 'i'
		kaikke = word[:-1] + 'e'
		kaiki = grad_weak(kaikki, gradtype)
		kaike = grad_weak(kaikke, gradtype)
		#
		all_forms['sg|nom'] = [word]
		all_forms['sg|gen'] = [f"{kaike}n"]
		all_forms['sg|par'] = [f"{kaikke}{a}"]
		all_forms['sg|ill'] = [f"{kaikke}en"]
		all_forms['pl|gen'] = [f"{kaikki}en"]
		all_forms['pl|par'] = [f"{kaikki}{a}"]
		all_forms['pl|ill'] = [f"{kaikki}in"]
		all_forms['pl|ine'] = [f"{kaiki}ss{a}"]
		all_forms['sg|ess'] = [f"{kaikke}n{a}"]
		all_forms['pl|ess'] = [f"{kaikki}n{a}"]

	# "nalle"
	elif kotus_class == "8":
		nukke = word
		nuke = grad_weak(word, gradtype)
		#
		all_forms['sg|gen'] = [f"{nuke}n"]
		all_forms['sg|par'] = [f"{nukke}{a}"]
		all_forms['sg|ill'] = [f"{nukke}en"]
		all_forms['pl|gen'] = [f"{nukke}jen"]
		all_forms['pl|par'] = [f"{nukke}j{a}"]
		all_forms['pl|ill'] = [f"{nukke}ihin"]
		all_forms['pl|ine'] = [f"{nuke}iss{a}"]
		all_forms['sg|ess'] = [f"{nukke}n{a}"]
		all_forms['pl|ess'] = [f"{nukke}in{a}"]
		all_forms['pl|gen|rare'] = [f"{nukke}in"]

	# "kala"
	elif kotus_class == "9":
		takka = word
		taka = grad_weak(word, gradtype)
		takko = word[:-1] + o
		tako = grad_weak(takko, gradtype)
		#
		all_forms['sg|gen'] = [f"{taka}n"]
		all_forms['sg|par'] = [f"{takka}{a}"]
		all_forms['sg|ill'] = [f"{takka}{a}n"]
		all_forms['pl|gen'] = [f"{takko}jen"]
		all_forms['pl|par'] = [f"{takko}j{a}"]
		all_forms['pl|ill'] = [f"{takko}ihin"]
		all_forms['pl|ine'] = [f"{tako}iss{a}"]
		all_forms['sg|ess'] = [f"{takka}n{a}"]
		all_forms['pl|ess'] = [f"{takko}in{a}"]
		all_forms['pl|gen|rare'] = [f"{takka}in"]

	# "koira"
	elif kotus_class == "10" and word[-1] in 'aä':
		tukka = word
		tukki = tukka[:-1] + 'i'
		tuka = grad_weak(tukka, gradtype)
		tuki = grad_weak(tukki, gradtype)
		#
		all_forms['sg|gen'] = [f"{tuka}n"]
		all_forms['sg|par'] = [f"{tukka}{a}"]
		all_forms['sg|ill'] = [f"{tukka}{a}n"]
		all_forms['pl|gen'] = [f"{tukki}en"]
		all_forms['pl|par'] = [f"{tukki}{a}"]
		all_forms['pl|ill'] = [f"{tukki}in"]
		all_forms['pl|ine'] = [f"{tuki}ss{a}"]
		all_forms['sg|ess'] = [f"{tukka}n{a}"]
		all_forms['pl|ess'] = [f"{tukki}n{a}"]
		all_forms['pl|gen|rare'] = [f"{tukka}in"]

		# # "hunajata", "veräjätä", "petäjätä", "keittäjätä", but not: *"jäteläjätä"
		# if re.fullmatch('.+[^a]aja', word) or re.fullmatch('.*(t|el|ver|en|ps|ks)äjä', word):
		# 	hunaja = word
		# 	all_forms['sg|par|nstd'] += [f"{hunaja}t{a}"]

	# "kahdeksan"
	elif kotus_class == "10":
		kahdeksa = word[:-1]
		kahdeks = word[:-2]
		#
		all_forms['sg|nom'] = [f"{kahdeksa}n"]
		all_forms['sg|gen'] = [f"{kahdeksa}n"]
		all_forms['sg|par'] = [f"{kahdeksa}{a}"]
		all_forms['sg|ill'] = [f"{kahdeksa}{a}n"]
		all_forms['pl|gen'] = [f"{kahdeks}ien"]
		all_forms['pl|par'] = [f"{kahdeks}i{a}"]
		all_forms['pl|ill'] = [f"{kahdeks}iin"]
		all_forms['pl|ine'] = [f"{kahdeks}iss{a}"]
		all_forms['sg|ess'] = [f"{kahdeksa}n{a}"]
		all_forms['pl|ess'] = [f"{kahdeks}in{a}"]
		all_forms['pl|gen|rare'] = [f"{kahdeksa}in"]

	# "HSL"
	elif kotus_class == "10B":
		#
		HSL = word
		all_forms['sg|gen'] = [f"{HSL}:n"]
		all_forms['sg|par'] = [f"{HSL}:{aa}", f"{HSL}:{a}"]
		all_forms['sg|ill'] = [f"{HSL}:{aa}n"]
		all_forms['pl|gen'] = [f"{HSL}:ien"]
		all_forms['pl|par'] = [f"{HSL}:i{a}"]
		all_forms['pl|ill'] = [f"{HSL}:iin"]
		all_forms['pl|ine'] = [f"{HSL}:iss{a}"]
		all_forms['sg|ess'] = [f"{HSL}:n{a}"]
		all_forms['pl|ess'] = [f"{HSL}:in{a}"]
		all_forms['@stem:clitics'] = [f"{HSL}:"]

	# "omena"
	elif kotus_class == "11":
		omena = word
		omen = word[:-1]
		omeno = word[:-1] + o
		#
		all_forms['sg|gen'] = [f"{omena}n"]
		all_forms['sg|par'] = [f"{omena}{a}"]
		all_forms['sg|ill'] = [f"{omena}{a}n"]
		all_forms['pl|gen'] = [f"{omen}ien", f"{omeno}iden", f"{omeno}itten"]
		all_forms['pl|par'] = [f"{omen}i{a}", f"{omeno}it{a}"]
		all_forms['pl|ill'] = [f"{omen}iin", f"{omeno}ihin"]
		all_forms['pl|ine'] = [f"{omen}iss{a}", f"{omeno}iss{a}"]
		all_forms['sg|ess'] = [f"{omena}n{a}"]
		all_forms['pl|ess'] = [f"{omeno}in{a}", f"{omen}in{a}"]
		all_forms['pl|gen|rare'] = [f"{omeno}jen", f"{omena}in"]
		all_forms['pl|par|rare'] = [f"{omeno}j{a}"]
		all_forms['sg|par|nstd'] = [f"{omena}t{a}"]

	# "kulkija"
	elif kotus_class == "12":
		kulkija = word
		kulkijo = word[:-1] + o
		#
		all_forms['sg|gen'] = [f"{kulkija}n"]
		all_forms['sg|par'] = [f"{kulkija}{a}"]
		all_forms['sg|ill'] = [f"{kulkija}{a}n"]
		all_forms['pl|gen'] = [f"{kulkijo}iden", f"{kulkijo}itten"]
		all_forms['pl|par'] = [f"{kulkijo}it{a}"]
		all_forms['pl|ill'] = [f"{kulkijo}ihin"]
		all_forms['pl|ine'] = [f"{kulkijo}iss{a}"]
		all_forms['sg|ess'] = [f"{kulkija}n{a}"]
		all_forms['pl|ess'] = [f"{kulkijo}in{a}"]
		all_forms['pl|gen|rare'] = [f"{kulkija}in"]
		all_forms['sg|par|nstd'] = [f"{kulkija}t{a}"]

		if not (word.endswith('ija') or word.endswith('ijä')):
			kamero = word[:-1] + o
			all_forms['pl|gen|nstd'] = [f"{kamero}jen"]
			all_forms['pl|par|nstd'] = [f"{kamero}j{a}"]

	# "katiska"
	elif kotus_class == "13":
		katiska = word
		katisko = word[:-1] + o
		#
		all_forms['sg|gen'] = [f"{katiska}n"]
		all_forms['sg|par'] = [f"{katiska}{a}"]
		all_forms['sg|ill'] = [f"{katiska}{a}n"]
		all_forms['pl|gen'] = [f"{katisko}iden", f"{katisko}itten", f"{katisko}jen"]
		all_forms['pl|par'] = [f"{katisko}it{a}", f"{katisko}j{a}"]
		all_forms['pl|ill'] = [f"{katisko}ihin"]
		all_forms['pl|ine'] = [f"{katisko}iss{a}"]
		all_forms['sg|ess'] = [f"{katiska}n{a}"]
		all_forms['pl|ess'] = [f"{katisko}in{a}"]
		all_forms['pl|gen|rare'] = [f"{katiska}in"]

	# "solakka"
	elif kotus_class == "14":
		solakk = word[:-1]
		solak = grad_weak(word, gradtype)[:-1]
		#
		all_forms['sg|gen'] = [f"{solak}{a}n"]
		all_forms['sg|par'] = [f"{solakk}{aa}"]
		all_forms['sg|ill'] = [f"{solakk}{aa}n"]
		all_forms['pl|gen'] = [f"{solak}{o}iden", f"{solak}{o}itten", f"{solakk}{o}jen"]
		all_forms['pl|par'] = [f"{solak}{o}it{a}", f"{solakk}{o}j{a}"]
		all_forms['pl|ill'] = [f"{solakk}{o}ihin", f"{solak}{o}ihin"]
		all_forms['pl|ine'] = [f"{solak}{o}iss{a}"]
		all_forms['sg|ess'] = [f"{solakk}{a}n{a}"]
		all_forms['pl|ess'] = [f"{solakk}{o}in{a}", f"{solak}{o}in{a}"]
		all_forms['pl|gen|rare'] = [f"{solakk}{a}in"]

	# "korkea"
	elif kotus_class == "15":
		korkea = word
		korke = word[:-1]
		#
		all_forms['sg|gen'] = [f"{korkea}n"]
		all_forms['sg|par'] = [f"{korkea}{a}", f"{korkea}t{a}"]
		all_forms['sg|ill'] = [f"{korkea}{a}n"]
		all_forms['pl|gen'] = [f"{korke}iden", f"{korke}itten"]
		all_forms['pl|par'] = [f"{korke}it{a}"]
		all_forms['pl|ill'] = [f"{korke}isiin", f"{korke}ihin"]
		all_forms['pl|ine'] = [f"{korke}iss{a}"]
		all_forms['sg|ess'] = [f"{korkea}n{a}"]
		all_forms['pl|ess'] = [f"{korke}in{a}"]
		all_forms['pl|gen|rare'] = [f"{korkea}in"]

	# "vanhempi"
	elif kotus_class == "16":
		vanhem = word[:-2]
		#
		all_forms['sg|gen'] = [f"{vanhem}pi"]
		all_forms['sg|gen'] = [f"{vanhem}m{a}n"]
		all_forms['sg|par'] = [f"{vanhem}p{aa}"]
		all_forms['sg|ill'] = [f"{vanhem}p{aa}n"]
		all_forms['pl|gen'] = [f"{vanhem}pien"]
		all_forms['pl|par'] = [f"{vanhem}pi{a}"]
		all_forms['pl|ill'] = [f"{vanhem}piin"]
		all_forms['pl|ine'] = [f"{vanhem}miss{a}"]
		all_forms['sg|ess'] = [f"{vanhem}p{a}n{a}"]
		all_forms['pl|ess'] = [f"{vanhem}pin{a}"]
		all_forms['pl|gen|rare'] = [f"{vanhem}p{a}in"]

	# "vapaa"
	elif kotus_class == "17":
		vapaa = word
		vapa = word[:-1]
		#
		all_forms['sg|gen'] = [f"{vapaa}n"]
		all_forms['sg|par'] = [f"{vapaa}t{a}"]
		all_forms['sg|ill'] = [f"{vapaa}seen"]
		all_forms['pl|gen'] = [f"{vapa}iden", f"{vapa}itten"]
		all_forms['pl|par'] = [f"{vapa}it{a}"]
		all_forms['pl|ill'] = [f"{vapa}isiin"]
		all_forms['pl|ine'] = [f"{vapa}iss{a}"]
		all_forms['sg|ess'] = [f"{vapaa}n{a}"]
		all_forms['pl|ess'] = [f"{vapa}in{a}"]
		all_forms['pl|ill|rare'] = [f"{vapa}ihin"]

	# "maa"
	elif kotus_class == "18":
		maa = word
		ma = word[:-1]
		han = f"h{vowel}n"
		#
		all_forms['sg|gen'] = [f"{maa}n"]
		all_forms['sg|par'] = [f"{maa}t{a}"]
		all_forms['sg|ill'] = [f"{maa}{han}"]
		all_forms['pl|gen'] = [f"{ma}iden", f"{ma}itten"]
		all_forms['pl|par'] = [f"{ma}it{a}"]
		all_forms['pl|ill'] = [f"{ma}ihin"]
		all_forms['pl|ine'] = [f"{ma}iss{a}"]
		all_forms['sg|ess'] = [f"{maa}n{a}"]
		all_forms['pl|ess'] = [f"{ma}in{a}"]

	# "leu"
	elif kotus_class == "18U":
		tau = word
		hun = f'h{vowel}n'
		#
		all_forms['sg|gen'] = [f"{tau}n"]
		all_forms['sg|par'] = [f"{tau}t{a}"]
		all_forms['sg|ill'] = [f"{tau}{hun}"]
		all_forms['pl|gen'] = [f"{tau}iden", f"{tau}itten", f"{tau}jen"]
		all_forms['pl|par'] = [f"{tau}it{a}", f"{tau}j{a}"]
		all_forms['pl|ill'] = [f"{tau}ihin"]
		all_forms['pl|ine'] = [f"{tau}iss{a}"]
		all_forms['sg|ess'] = [f"{tau}n{a}"]
		all_forms['pl|ess'] = [f"{tau}in{a}"]

	# "DNA"
	elif kotus_class == "18B":
		dna = word
		han = f"h{vowel}n"
		#
		all_forms['sg|nom'] = [f"{dna}"]
		all_forms['sg|gen'] = [f"{dna}:n"]
		all_forms['sg|par'] = [f"{dna}:t{a}"]
		all_forms['sg|ill'] = [f"{dna}:{han}"]
		all_forms['pl|gen'] = [f"{dna}:iden", f"{dna}:itten"]
		all_forms['pl|par'] = [f"{dna}:it{a}"]
		all_forms['pl|ill'] = [f"{dna}:ihin"]
		all_forms['pl|ine'] = [f"{dna}:iss{a}"]
		all_forms['sg|ess'] = [f"{dna}:n{a}"]
		all_forms['pl|ess'] = [f"{dna}:in{a}"]
		all_forms['@stem:clitics'] = [f"{dna}:"]

	# "suo"
	elif kotus_class == "19":
		suo = word
		so = word[:-2] + word[-1]
		hon = f"h{vowel}n"
		#
		all_forms['sg|gen'] = [f"{suo}n"]
		all_forms['sg|par'] = [f"{suo}t{a}"]
		all_forms['sg|ill'] = [f"{suo}{hon}"]
		all_forms['pl|gen'] = [f"{so}iden", f"{so}itten"]
		all_forms['pl|par'] = [f"{so}it{a}"]
		all_forms['pl|ill'] = [f"{so}ihin"]
		all_forms['pl|ine'] = [f"{so}iss{a}"]
		all_forms['sg|ess'] = [f"{suo}n{a}"]
		all_forms['pl|ess'] = [f"{so}in{a}"]

	# "filee"
	elif kotus_class == "20":
		patee = word
		pate = word[:-1]
		hen = f"h{vowel}n"
		#
		all_forms['sg|gen'] = [f"{patee}n"]
		all_forms['sg|par'] = [f"{patee}t{a}"]
		all_forms['sg|ill'] = [f"{patee}{hen}", f"{patee}seen"]
		all_forms['pl|gen'] = [f"{pate}iden", f"{pate}itten"]
		all_forms['pl|par'] = [f"{pate}it{a}"]
		all_forms['pl|ill'] = [f"{pate}ihin"]
		all_forms['pl|ine'] = [f"{pate}iss{a}"]
		all_forms['sg|ess'] = [f"{patee}n{a}"]
		all_forms['pl|ess'] = [f"{pate}in{a}"]

	# "rosé"
	elif kotus_class == "21":
		cowboy = word
		hyn = f"h{vowel}n"
		#
		all_forms['sg|gen'] = [f"{cowboy}n"]
		all_forms['sg|par'] = [f"{cowboy}t{a}"]
		all_forms['sg|ill'] = [f"{cowboy}{hyn}"]
		all_forms['pl|gen'] = [f"{cowboy}iden", f"{cowboy}itten"]
		all_forms['pl|par'] = [f"{cowboy}it{a}"]
		all_forms['pl|ill'] = [f"{cowboy}ihin"]
		all_forms['pl|ine'] = [f"{cowboy}iss{a}"]
		all_forms['sg|ess'] = [f"{cowboy}n{a}"]
		all_forms['pl|ess'] = [f"{cowboy}in{a}"]

	# "parfait"
	elif kotus_class == "22":
		parfait = word
		hen = f"h{vowel}n"
		#
		all_forms['sg|nom'] = [f"{parfait}"]
		all_forms['sg|gen'] = [f"{parfait}’n"]
		all_forms['sg|par'] = [f"{parfait}’t{a}"]
		all_forms['sg|ill'] = [f"{parfait}’{hen}"]
		all_forms['pl|gen'] = [f"{parfait}’iden", f"{parfait}’itten"]
		all_forms['pl|par'] = [f"{parfait}’it{a}"]
		all_forms['pl|ill'] = [f"{parfait}’ihin"]
		all_forms['pl|ine'] = [f"{parfait}’iss{a}"]
		all_forms['sg|ess'] = [f"{parfait}’n{a}"]
		all_forms['pl|ess'] = [f"{parfait}’in{a}"]

		# TODO: Add nonstandard inflections *here*!

	# "tiili"
	elif kotus_class == "23":
		loh = word[:-1]
		#
		all_forms['sg|gen'] = [f"{loh}en"]
		all_forms['sg|par'] = [f"{loh}t{a}"]
		all_forms['sg|ill'] = [f"{loh}een"]
		all_forms['pl|gen'] = [f"{loh}ien"]
		all_forms['pl|par'] = [f"{loh}i{a}"]
		all_forms['pl|ill'] = [f"{loh}iin"]
		all_forms['pl|ine'] = [f"{loh}iss{a}"]
		all_forms['sg|ess'] = [f"{loh}en{a}"]
		all_forms['pl|ess'] = [f"{loh}in{a}"]
		all_forms['pl|gen|nstd'] = [f"{loh}ten"]

	# TODO: Conflate 24, 32, 26 (+ 23)?

	# "uni"
	elif kotus_class == "24":
		un = word[:-1]
		#
		all_forms['sg|gen'] = [f"{un}en"]
		all_forms['sg|par'] = [f"{un}t{a}"]
		all_forms['sg|ill'] = [f"{un}een"]
		all_forms['pl|gen'] = [f"{un}ten", f"{un}ien"]
		all_forms['pl|par'] = [f"{un}i{a}"]
		all_forms['pl|ill'] = [f"{un}iin"]
		all_forms['pl|ine'] = [f"{un}iss{a}"]
		all_forms['sg|ess'] = [f"{un}en{a}"]
		all_forms['pl|ess'] = [f"{un}in{a}"]

	# "toimi"
	elif kotus_class == "25":
		toim = word[:-1]
		toin = word[:-2] + 'n'
		#
		all_forms['sg|gen'] = [f"{toim}en"]
		all_forms['sg|par'] = [f"{toin}t{a}", f"{toim}e{a}"]
		all_forms['sg|ill'] = [f"{toim}een"]
		all_forms['pl|gen'] = [f"{toin}ten", f"{toim}ien"]
		all_forms['pl|par'] = [f"{toim}i{a}"]
		all_forms['pl|ill'] = [f"{toim}iin"]
		all_forms['pl|ine'] = [f"{toim}iss{a}"]
		all_forms['sg|ess'] = [f"{toim}en{a}"]
		all_forms['pl|ess'] = [f"{toim}in{a}"]

		if word == 'liemi':
			all_forms['sg|par'] = [f"{toin}t{a}"]
			all_forms['sg|par|nstd'] = [f"{toim}e{a}"]

	# "pieni"
	elif kotus_class == "26":
		suur = word[:-1]
		#
		all_forms['sg|gen'] = [f"{suur}en"]
		all_forms['sg|par'] = [f"{suur}t{a}"]
		all_forms['sg|ill'] = [f"{suur}een"]
		all_forms['pl|gen'] = [f"{suur}ten", f"{suur}ien"]
		all_forms['pl|par'] = [f"{suur}i{a}"]
		all_forms['pl|ill'] = [f"{suur}iin"]
		all_forms['pl|ine'] = [f"{suur}iss{a}"]
		all_forms['sg|ess'] = [f"{suur}en{a}"]
		all_forms['pl|ess'] = [f"{suur}in{a}"]

	# "käsi"
	elif kotus_class == "27":
		uu = word[:-2]
		#
		all_forms['sg|gen'] = [f"{uu}den"]
		all_forms['sg|par'] = [f"{uu}tt{a}"]
		all_forms['sg|ill'] = [f"{uu}teen"]
		all_forms['pl|gen'] = [f"{uu}sien"]
		all_forms['pl|par'] = [f"{uu}si{a}"]
		all_forms['pl|ill'] = [f"{uu}siin"]
		all_forms['pl|ine'] = [f"{uu}siss{a}"]
		all_forms['sg|ess'] = [f"{uu}ten{a}"]
		all_forms['pl|ess'] = [f"{uu}sin{a}"]
		all_forms['pl|gen|rare'] = [f"{uu}tten"]

	# "kynsi"
	elif kotus_class == "28":
		kansi = word
		kann = word[:-2] + word[-3]
		kant = word[:-2] + "t"
		#
		all_forms['sg|gen'] = [f"{kann}en"]
		all_forms['sg|par'] = [f"{kant}t{a}"]
		all_forms['sg|ill'] = [f"{kant}een"]
		all_forms['pl|gen'] = [f"{kansi}en"]
		all_forms['pl|par'] = [f"{kansi}{a}"]
		all_forms['pl|ill'] = [f"{kansi}in"]
		all_forms['pl|ine'] = [f"{kansi}ss{a}"]
		all_forms['sg|ess'] = [f"{kant}en{a}"]
		all_forms['pl|ess'] = [f"{kansi}n{a}"]
		all_forms['pl|gen|nstd'] = [f"{kant}ten"]

	# "lapsi", "uksi"
	elif kotus_class == "29":
		laps = word[:-1]
		la = word[:-3]
		#
		all_forms['sg|gen'] = [f"{laps}en"]
		all_forms['sg|par'] = [f"{la}st{a}"]
		all_forms['sg|ill'] = [f"{laps}een"]
		all_forms['pl|gen'] = [f"{la}sten", f"{laps}ien"]
		all_forms['pl|par'] = [f"{laps}i{a}"]
		all_forms['pl|ill'] = [f"{laps}iin"]
		all_forms['pl|ine'] = [f"{laps}iss{a}"]
		all_forms['sg|ess'] = [f"{laps}en{a}"]
		all_forms['pl|ess'] = [f"{laps}in{a}"]

	# "veitsi"
	elif kotus_class == "30":
		vei = word[:-3]
		#
		all_forms['sg|gen'] = [f"{vei}tsen"]
		all_forms['sg|par'] = [f"{vei}st{a}"]
		all_forms['sg|ill'] = [f"{vei}tseen"]
		all_forms['pl|gen'] = [f"{vei}tsien"]
		all_forms['pl|par'] = [f"{vei}tsi{a}"]
		all_forms['pl|ill'] = [f"{vei}tsiin"]
		all_forms['pl|ine'] = [f"{vei}tsiss{a}"]
		all_forms['sg|ess'] = [f"{vei}tsen{a}"]
		all_forms['pl|ess'] = [f"{vei}tsin{a}"]
		all_forms['pl|gen|rare'] = [f"{vei}sten"]

	# "kaksi"
	elif kotus_class == "31":
		ka = word[:-3]
		#
		all_forms['sg|gen'] = [f"{ka}hden"]
		all_forms['sg|par'] = [f"{ka}ht{a}"]
		all_forms['sg|ill'] = [f"{ka}hteen"]
		all_forms['pl|gen'] = [f"{ka}ksien"]
		all_forms['pl|par'] = [f"{ka}ksi{a}"]
		all_forms['pl|ill'] = [f"{ka}ksiin"]
		all_forms['pl|ine'] = [f"{ka}ksiss{a}"]
		all_forms['sg|ess'] = [f"{ka}hten{a}"]
		all_forms['pl|ess'] = [f"{ka}ksin{a}"]

	# "kymmenen"
	elif kotus_class == "32" and word.endswith('kymmenen'):
		ilta = word[:-9]
		#
		all_forms['sg|nom'] = [f"{ilta}kymmenen"]
		all_forms['sg|gen'] = [f"{ilta}kymmenen"]
		all_forms['sg|par'] = [f"{ilta}kymmentä"]
		all_forms['sg|ill'] = [f"{ilta}kymmeneen"]
		all_forms['pl|gen'] = [f"{ilta}kymmenten", f"{ilta}kymmenien"]
		all_forms['pl|par'] = [f"{ilta}kymmeniä"]
		all_forms['pl|ill'] = [f"{ilta}kymmeniin"]
		all_forms['pl|ine'] = [f"{ilta}kymmenissä"]
		all_forms['sg|ess'] = [f"{ilta}kymmenenä"]
		all_forms['pl|ess'] = [f"{ilta}kymmeninä"]

	# "sisar"
	elif kotus_class == "32":
		ajatar = word[:-2] if word.endswith('kymmenen') else word
		ajattar = grad_strong(ajatar[:-1], gradtype) + word[-1]
		#
		all_forms['sg|nom'] = [f"{ajatar}"]
		all_forms['sg|gen'] = [f"{ajattar}en"]
		all_forms['sg|par'] = [f"{ajatar}t{a}"]
		all_forms['sg|ill'] = [f"{ajattar}een"]
		all_forms['pl|gen'] = [f"{ajatar}ten", f"{ajattar}ien"]
		all_forms['pl|par'] = [f"{ajattar}i{a}"]
		all_forms['pl|ill'] = [f"{ajattar}iin"]
		all_forms['pl|ine'] = [f"{ajattar}iss{a}"]
		all_forms['sg|ess'] = [f"{ajattar}en{a}"]
		all_forms['pl|ess'] = [f"{ajattar}in{a}"]

	# "kytkin"
	elif kotus_class == "33":
		eroti = word[:-1]
		erotti = grad_strong(eroti, gradtype)
		#
		all_forms['sg|nom'] = [f"{eroti}n"]
		all_forms['sg|gen'] = [f"{erotti}men"]
		all_forms['sg|par'] = [f"{eroti}nt{a}"]
		all_forms['sg|ill'] = [f"{erotti}meen"]
		all_forms['pl|gen'] = [f"{erotti}mien", f"{eroti}nten"]
		all_forms['pl|par'] = [f"{erotti}mi{a}"]
		all_forms['pl|ill'] = [f"{erotti}miin"]
		all_forms['pl|ine'] = [f"{erotti}miss{a}"]
		all_forms['sg|ess'] = [f"{erotti}men{a}"]
		all_forms['pl|ess'] = [f"{erotti}min{a}"]

	# "onneton", "alaston"
	elif kotus_class == "34":
		onneto = word[:-1]
		onnetto = grad_strong(onneto, gradtype)
		#
		all_forms['sg|nom'] = [f"{onneto}n"]
		all_forms['sg|gen'] = [f"{onnetto}m{a}n"]
		all_forms['sg|par'] = [f"{onneto}nt{a}"]
		all_forms['sg|ill'] = [f"{onnetto}m{aa}n"]
		all_forms['pl|gen'] = [f"{onnetto}mien", f"{onneto}nten"]
		all_forms['pl|par'] = [f"{onnetto}mi{a}"]
		all_forms['pl|ill'] = [f"{onnetto}miin"]
		all_forms['pl|ine'] = [f"{onnetto}miss{a}"]
		all_forms['sg|ess'] = [f"{onnetto}m{a}n{a}"]
		all_forms['pl|ess'] = [f"{onnetto}min{a}"]

		# "onnetonna"
		all_forms['sg|ess|dial'] = [f"{onneto}nn{a}"]

	# "vastaus"
	elif kotus_class == "39":
		vastau = word[:-1]
		#
		all_forms['sg|nom'] = [f"{vastau}s"]
		all_forms['sg|gen'] = [f"{vastau}ksen"]
		all_forms['sg|par'] = [f"{vastau}st{a}"]
		all_forms['sg|ill'] = [f"{vastau}kseen"]
		all_forms['pl|gen'] = [f"{vastau}sten", f"{vastau}ksien"]
		all_forms['pl|par'] = [f"{vastau}ksi{a}"]
		all_forms['pl|ill'] = [f"{vastau}ksiin"]
		all_forms['pl|ine'] = [f"{vastau}ksiss{a}"]
		all_forms['sg|ess'] = [f"{vastau}ksen{a}"]
		all_forms['pl|ess'] = [f"{vastau}ksin{a}"]

	# "kalleus"
	elif kotus_class == "40":
		kalleu = word[:-1]
		#
		all_forms['sg|nom'] = [f"{kalleu}s"]
		all_forms['sg|gen'] = [f"{kalleu}den"]
		all_forms['sg|par'] = [f"{kalleu}tt{a}"]
		all_forms['sg|ill'] = [f"{kalleu}teen"]
		all_forms['pl|gen'] = [f"{kalleu}ksien"]
		all_forms['pl|par'] = [f"{kalleu}ksi{a}"]
		all_forms['pl|ill'] = [f"{kalleu}ksiin"]
		all_forms['pl|ine'] = [f"{kalleu}ksiss{a}"]
		all_forms['sg|ess'] = [f"{kalleu}ten{a}"]
		all_forms['pl|ess'] = [f"{kalleu}ksin{a}"]

	# "vieras", "kevät"
	elif kotus_class == "41" or kotus_class == "44":
		rikas = word
		rika = word[:-1]
		rikka = grad_strong(rika, gradtype)
		rikkaa = rikka + vowel
		#
		all_forms['sg|nom'] = [f"{rikas}"]
		all_forms['sg|gen'] = [f"{rikkaa}n"]
		all_forms['sg|par'] = [f"{rikas}t{a}"]
		all_forms['sg|ill'] = [f"{rikkaa}seen"]
		all_forms['pl|gen'] = [f"{rikka}iden", f"{rikka}itten"]
		all_forms['pl|par'] = [f"{rikka}it{a}"]
		all_forms['pl|ill'] = [f"{rikka}isiin"]
		all_forms['pl|ine'] = [f"{rikka}iss{a}"]
		all_forms['sg|ess'] = [f"{rikkaa}n{a}"]
		all_forms['pl|ess'] = [f"{rikka}in{a}"]
		all_forms['pl|ill|rare'] = [f"{rikka}ihin"]

		all_forms['pl|ill|nstd'] = [f"{rikka}hiin"] if kotus_class == '41' else []
		all_forms['pl|gen|rare'] = [f"{rikas}ten"] if kotus_class == '41' else []

	# "mies"
	elif kotus_class == "42":
		mie = word[:-1]
		#
		all_forms['sg|gen'] = [f"{mie}hen"]
		all_forms['sg|par'] = [f"{mie}stä"]
		all_forms['sg|ill'] = [f"{mie}heen"]
		all_forms['pl|gen'] = [f"{mie}sten", f"{mie}hien"]
		all_forms['pl|par'] = [f"{mie}hiä"]
		all_forms['pl|ill'] = [f"{mie}hiin"]
		all_forms['pl|ine'] = [f"{mie}hissä"]
		all_forms['sg|ess'] = [f"{mie}hen{a}"]
		all_forms['pl|ess'] = [f"{mie}hin{a}"]

	# "ohut"
	elif kotus_class == "43":
		poiu = word[:-1]
		poiku = grad_strong(poiu, gradtype)
		#
		all_forms['sg|nom'] = [f"{poiu}t"]
		all_forms['sg|gen'] = [f"{poiku}en"]
		all_forms['sg|par'] = [f"{poiu}tt{a}"]
		all_forms['sg|ill'] = [f"{poiku}een"]
		all_forms['pl|gen'] = [f"{poiku}iden", f"{poiku}itten"]
		all_forms['pl|par'] = [f"{poiku}it{a}"]
		all_forms['pl|ill'] = [f"{poiku}isiin", f"{poiku}ihin"]
		all_forms['pl|ine'] = [f"{poiku}iss{a}"]
		all_forms['sg|ess'] = [f"{poiku}en{a}"]
		all_forms['pl|ess'] = [f"{poiku}in{a}"]

		# "olueeseen", "kevyeeseen"
		if re.fullmatch('.+(ut|yt)', word):
			all_forms['sg|ill|nstd'] = [f"{poiku}eeseen"]

	# "kahdeksas"
	elif kotus_class == "45":
		kahdeksa = word[:-1]
		#
		all_forms['sg|nom'] = [f"{kahdeksa}s"]
		all_forms['sg|gen'] = [f"{kahdeksa}nnen"]
		all_forms['sg|par'] = [f"{kahdeksa}tt{a}"]
		all_forms['sg|ill'] = [f"{kahdeksa}nteen"]
		all_forms['pl|gen'] = [f"{kahdeksa}nsien"]
		all_forms['pl|par'] = [f"{kahdeksa}nsi{a}"]
		all_forms['pl|ill'] = [f"{kahdeksa}nsiin"]
		all_forms['pl|ine'] = [f"{kahdeksa}nsiss{a}"]
		all_forms['sg|ess'] = [f"{kahdeksa}nten{a}"]
		all_forms['pl|ess'] = [f"{kahdeksa}nsin{a}"]

	# "tuhat"
	elif kotus_class == "46":
		tuha = word[:-1]
		#
		all_forms['sg|nom'] = [f"{tuha}t"]
		all_forms['sg|gen'] = [f"{tuha}nnen"]
		all_forms['sg|par'] = [f"{tuha}tt{a}"]
		all_forms['sg|ill'] = [f"{tuha}nteen"]
		all_forms['pl|gen'] = [f"{tuha}nsien"]
		all_forms['pl|par'] = [f"{tuha}nsi{a}"]
		all_forms['pl|ill'] = [f"{tuha}nsiin"]
		all_forms['pl|ine'] = [f"{tuha}nsiss{a}"]
		all_forms['sg|ess'] = [f"{tuha}nten{a}"]
		all_forms['pl|ess'] = [f"{tuha}nsin{a}"]
		all_forms['pl|gen|rare'] = [f"{tuha}nten"]

	# "kuollut"
	elif kotus_class == "47":
		kuollu = word[:-1]
		kuolle = word[:-2] + 'e'
		#
		all_forms['sg|gen'] = [f"{kuolle}en"]
		all_forms['sg|par'] = [f"{kuollu}tt{a}"]
		all_forms['sg|ill'] = [f"{kuolle}eseen"]
		all_forms['pl|gen'] = [f"{kuolle}iden", f"{kuolle}itten"]
		all_forms['pl|par'] = [f"{kuolle}it{a}"]
		all_forms['pl|ill'] = [f"{kuolle}isiin"]
		all_forms['pl|ine'] = [f"{kuolle}iss{a}"]
		all_forms['sg|ess'] = [f"{kuolle}en{a}"]
		all_forms['pl|ess'] = [f"{kuolle}in{a}"]

	# "hame", "moite"
	elif kotus_class == "48" or kotus_class == '49b':
		moite = word
		moitte = grad_strong(moite, gradtype)
		moittee = moitte + vowel
		#
		all_forms['sg|nom'] = [f"{moite}"]
		all_forms['sg|gen'] = [f"{moittee}n"]
		all_forms['sg|par'] = [f"{moite}tt{a}"]
		all_forms['sg|ill'] = [f"{moittee}seen"]
		all_forms['pl|gen'] = [f"{moitte}iden", f"{moitte}itten"]
		all_forms['pl|par'] = [f"{moitte}it{a}"]
		all_forms['pl|ill'] = [f"{moitte}isiin", f"{moitte}ihin"]
		all_forms['pl|ine'] = [f"{moitte}iss{a}"]
		all_forms['sg|ess'] = [f"{moittee}n{a}"]
		all_forms['pl|ess'] = [f"{moitte}in{a}"]
		all_forms['pl|par|nstd'] = [f"{moitte}hi{a}"]

	# "askel"
	elif kotus_class == "49":
		auer = word
		auter = grad_strong(word[:-1], gradtype) + word[-1]
		#
		all_forms['sg|nom'] = [f"{auer}"]
		all_forms['sg|gen'] = [f"{auter}en"]
		all_forms['sg|par'] = [f"{auer}t{a}"]
		all_forms['sg|ill'] = [f"{auter}eeseen"]
		all_forms['pl|gen'] = [f"{auer}ten", f"{auter}ien"]
		all_forms['pl|par'] = [f"{auter}i{a}"]
		all_forms['pl|ill'] = [f"{auter}iin"]
		all_forms['pl|ine'] = [f"{auter}iss{a}", f"{auter}eiss{a}"]
		all_forms['sg|ess'] = [f"{auter}en{a}"]
		all_forms['pl|ess'] = [f"{auter}ein{a}"]
		all_forms['sg|ill|rare'] = [f"{auter}een"]

	# "lämmin"
	elif kotus_class == '35':
		hapa = word[:-1]
		happa = grad_strong(hapa, gradtype)
		#
		all_forms['sg|nom'] = [f"{hapa}n"]
		all_forms['sg|gen'] = [f"{happa}m{a}n"]
		all_forms['sg|par'] = [f"{hapa}nt{a}"]
		all_forms['sg|ill'] = [f"{happa}m{aa}n"]
		all_forms['pl|gen'] = [f"{happa}mien"]
		all_forms['pl|par'] = [f"{happa}mi{a}"]
		all_forms['pl|ill'] = [f"{happa}miin"]
		all_forms['pl|ine'] = [f"{happa}miss{a}"]
		all_forms['sg|ess'] = [f"{happa}m{a}n{a}"]
		all_forms['pl|ess'] = [f"{happa}min{a}"]
		all_forms['sg|par|nstd'] = [f"{happa}m{aa}"]

	# "sisin"
	elif kotus_class == "36":
		vanhi = word[:-1]
		#
		all_forms['sg|nom'] = [f"{vanhi}n"]
		all_forms['sg|gen'] = [f"{vanhi}mm{a}n"]
		all_forms['sg|par'] = [f"{vanhi}nt{a}"]
		all_forms['sg|ill'] = [f"{vanhi}mp{aa}n"]
		all_forms['pl|gen'] = [f"{vanhi}mpien"]
		all_forms['pl|par'] = [f"{vanhi}mpi{a}"]
		all_forms['pl|ill'] = [f"{vanhi}mpiin"]
		all_forms['pl|ine'] = [f"{vanhi}mmiss{a}"]
		all_forms['sg|ess'] = [f"{vanhi}mp{a}n{a}"]
		all_forms['pl|ess'] = [f"{vanhi}mpin{a}"]
		all_forms['pl|gen|rare'] = [f"{vanhi}nten", f"{vanhi}mp{a}in"]
		all_forms['sg|par|nstd'] = [f"{vanhi}mp{aa}"]

	# "vasen"
	elif kotus_class == "37":
		vase = word[:-1]
		#
		all_forms['sg|nom'] = [f"{vase}n"]
		all_forms['sg|gen'] = [f"{vase}mman"]
		all_forms['sg|par'] = [f"{vase}nta"]
		all_forms['sg|ill'] = [f"{vase}mpaan"]
		all_forms['pl|gen'] = [f"{vase}mpien"]
		all_forms['pl|par'] = [f"{vase}mpia"]
		all_forms['pl|ill'] = [f"{vase}mpiin"]
		all_forms['pl|ine'] = [f"{vase}mmissa"]
		all_forms['sg|ess'] = [f"{vase}mpana"]
		all_forms['pl|ess'] = [f"{vase}mpina"]
		all_forms['sg|par|rare'] = [f"{vase}mpaa"]
		all_forms['pl|gen|rare'] = [f"{vase}nten", f"{vase}mpain"]

	# "nainen"
	elif kotus_class == '38' or kotus_class == '38-pl':
		nai = word[:-3]
		#
		all_forms['sg|nom'] = [f"{nai}nen"]
		all_forms['sg|gen'] = [f"{nai}sen"]
		all_forms['sg|par'] = [f"{nai}st{a}"]
		all_forms['sg|ill'] = [f"{nai}seen"]
		all_forms['pl|gen'] = [f"{nai}sten"]
		all_forms['pl|gen|rare'] = [f"{nai}sien"]
		all_forms['pl|par'] = [f"{nai}si{a}"]
		all_forms['pl|ill'] = [f"{nai}siin"]
		all_forms['pl|ine'] = [f"{nai}siss{a}"]
		all_forms['sg|ess'] = [f"{nai}sen{a}"]
		all_forms['pl|ess'] = [f"{nai}sin{a}"]

	# Kauniainen
	elif kotus_class == '38-pl':
		pass
		# TODO
		"""
		kauniai = word[:-3]
		all_forms = inflect_noun_pl(f'{kauniai}set', '38', '', harmony)
		all_forms = {f'sg|{tag}': forms for tag, forms in all_forms.items()}
		all_forms['@base'] = [word]
		all_forms['@stem:possessives:nom'] = [f'{kauniai}se']
		all_forms['@stem:possessives:gen'] = [f'{kauniai}ste', f'{kauniai}sie']
		all_forms['sg|nom'] = [word]
		all_forms['sg|acc'] = [f'{kauniai}nen', f'{kauniai}sen']
		del all_forms['sg|@stem:possessives:nom']
		del all_forms['sg|@base']
		return all_forms
		"""

	# (Miscellaneous symbols and Roman numerals)
	elif kotus_class == 'XX':
		x = word
		all_forms['sg|nom'] = [f"{x}"]
		all_forms['sg|gen'] = [f"{x}:n"]
		all_forms['sg|par'] = [f"{x}:{a}", f"{x}:{aa}", f"{x}:t{a}"]
		all_forms['sg|ill'] = [f"{x}:{aa}n", f"{x}:een", f"{x}:iin"]
		all_forms['pl|gen'] = [f"{x}:ien"]
		all_forms['pl|par'] = [f"{x}:i{a}", f"{x}:it{a}"]
		all_forms['pl|ill'] = [f"{x}:iin"]
		all_forms['pl|ine'] = [f"{x}:iss{a}"]
		all_forms['sg|ess'] = [f"{x}:n{a}"]
		all_forms['pl|ess'] = [f"{x}:in{a}"]
		all_forms['@stem:clitics'] = [f"{x}:"]

	# "1", "2"
	elif kotus_class == "31B":
		k = word
		#
		all_forms['sg|nom'] = [f"{k}"]
		all_forms['sg|gen'] = [f"{k}:n"]
		all_forms['sg|par'] = [f"{k}:t{a}"]
		all_forms['sg|ill'] = [f"{k}:een"]
		all_forms['pl|gen'] = [f"{k}:ien"]
		all_forms['pl|par'] = [f"{k}:i{a}"]
		all_forms['pl|ill'] = [f"{k}:iin"]
		all_forms['pl|ine'] = [f"{k}:iss{a}"]
		all_forms['sg|ess'] = [f"{k}:n{a}"]
		all_forms['pl|ess'] = [f"{k}:in{a}"]
		all_forms['@stem:clitics'] = [f"{k}:"]

	# "3", "4"
	elif kotus_class == '8B':
		x = word
		een = f"{vowel}{vowel}n"
		#
		all_forms['sg|nom'] = [f"{x}"]
		all_forms['sg|gen'] = [f"{x}:n"]
		all_forms['sg|par'] = [f"{x}:{a}"]
		all_forms['sg|ill'] = [f"{x}:{een}"]
		all_forms['pl|gen'] = [f"{x}:ien"]
		all_forms['pl|par'] = [f"{x}:i{a}"]
		all_forms['pl|ill'] = [f"{x}:iin"]
		all_forms['pl|ine'] = [f"{x}:iss{a}"]
		all_forms['sg|ess'] = [f"{x}:n{a}"]
		all_forms['pl|ess'] = [f"{x}:in{a}"]
		all_forms['@stem:clitics'] = [f"{x}:"]

	# "5", "6"
	elif kotus_class == '27B':
		x = word
		#
		all_forms['sg|nom'] = [f"{x}"]
		all_forms['sg|gen'] = [f"{x}:n"]
		all_forms['sg|par'] = [f"{x}:tt{a}", f"{x}:t{a}"]
		all_forms['sg|ill'] = [f"{x}:een"]
		all_forms['pl|gen'] = [f"{x}:ien"]
		all_forms['pl|par'] = [f"{x}:i{a}"]
		all_forms['pl|ill'] = [f"{x}:iin"]
		all_forms['pl|ine'] = [f"{x}:iss{a}"]
		all_forms['sg|ess'] = [f"{x}:n{a}"]
		all_forms['pl|ess'] = [f"{x}:in{a}"]
		all_forms['@stem:clitics'] = [f"{x}:"]

	# "7", "8", "9"
	elif kotus_class == '10B':
		x = word
		#
		all_forms['sg|nom'] = [f"{x}"]
		all_forms['sg|gen'] = [f"{x}:n"]
		all_forms['sg|par'] = [f"{x}:{aa}"]
		all_forms['sg|ill'] = [f"{x}:{aa}n"]
		all_forms['pl|gen'] = [f"{x}:ien"]
		all_forms['pl|par'] = [f"{x}:i{a}"]
		all_forms['pl|ill'] = [f"{x}:iin"]
		all_forms['pl|ine'] = [f"{x}:iss{a}"]
		all_forms['sg|ess'] = [f"{x}:n{a}"]
		all_forms['pl|ess'] = [f"{x}:in{a}"]
		all_forms['@stem:clitics'] = [f"{x}:"]

	else:
		print(f'Unknown class for noun "{word}": {kotus_class}')
		return {'@base': [word], '': [word]}

	# Derive remaining cases from existing ones

	for kaupa in [f[:-1] for f in all_forms['sg|gen']]:
		all_forms['sg|all'] += [f"{kaupa}lle"]
		all_forms['sg|ade'] += [f"{kaupa}ll{a}"]
		all_forms['sg|abl'] += [f"{kaupa}lt{a}"]
		all_forms['sg|ine'] += [f"{kaupa}ss{a}"]
		all_forms['sg|ela'] += [f"{kaupa}st{a}"]
		all_forms['sg|tra'] += [f"{kaupa}ksi"]
		all_forms['sg|abe'] += [f"{kaupa}tt{a}"]
		all_forms['pl|nom'] += [f"{kaupa}t"]

	for kaupoi in [f[:-3] for f in all_forms['pl|ine']]:
		all_forms['pl|all'] += [f"{kaupoi}lle"]
		all_forms['pl|ade'] += [f"{kaupoi}ll{a}"]
		all_forms['pl|abl'] += [f"{kaupoi}lt{a}"]
		all_forms['pl|ela'] += [f"{kaupoi}st{a}"]
		all_forms['pl|tra'] += [f"{kaupoi}ksi"]
		all_forms['pl|abe'] += [f"{kaupoi}tt{a}"]
		all_forms['pl|ins'] += [f"{kaupoi}n"]

	for kauppoi in [f[:-2] for f in all_forms['pl|ess']]:
		all_forms['pl|com'] += [f"{kauppoi}ne"]

	# Auxiliary forms
	poss_stem = all_forms['sg|ess'][0][:-2]
	all_forms['@stem:possessives'] = [poss_stem]
	all_forms['@stem:clitics'] = all_forms.get('@stem:clitics') or all_forms['sg|nom']
	all_forms['@base'] = [word]

	return clean(all_forms)


def inflect_verb(word, kotus_class, gradtype=None, harmony=None):

	harmony = harmony or determine_harmony(word)
	a, o, u, aa, oo, _ = HARMONY_MAPPING[harmony]

	all_forms = defaultdict(list)
	all_forms['@base'] = [word]
	all_forms['inf1'] = [word]

	# "olla"
	if word == "olla":          # 'olla'
		all_forms['pres|1sg'] = ["olen"]
		all_forms['pres|3sg'] = ["on"]
		all_forms['past|1sg'] = ["olin"]
		all_forms['past|3sg'] = ["oli"]
		all_forms['cond|3sg'] = ["olisi"]
		all_forms['poten|3sg'] = ["lienee"]
		all_forms['imper|3sg'] = ["olkoon"]
		all_forms['part_past'] = ["ollut"]
		all_forms['pass|past'] = ["oltiin"]
		all_forms['part_ma'] = ["olema"]
		all_forms['pass|pres'] = ["ollaan"]

	# "sanoa"
	elif kotus_class == "52":
		haukko = word[:-1]
		hauko = grad_weak(haukko, gradtype)
		haukkoo = haukko + word[-2]
		all_forms['pres|1sg'] = [f"{hauko}n"]
		all_forms['pres|3sg'] = [f"{haukkoo}"]
		all_forms['past|1sg'] = [f"{hauko}in"]
		all_forms['past|3sg'] = [f"{haukko}i"]
		all_forms['cond|3sg'] = [f"{haukko}isi"]
		all_forms['poten|3sg'] = [f"{haukko}nee"]
		all_forms['imper|3sg'] = [f"{haukko}k{oo}n"]
		all_forms['part_past'] = [f"{haukko}n{u}t"]
		all_forms['pass|past'] = [f"{hauko}ttiin"]
		all_forms['part_ma'] = [f"{haukko}m{a}"]
		all_forms['pass|pres'] = [f"{hauko}t{aa}n"]

	# "muistaa"
	elif kotus_class == "53":
		otta = word[:-1]
		ott = otta[:-1]
		ota = grad_weak(otta, gradtype)
		ot = ota[:-1]
		ote = ot + 'e'
		all_forms['pres|1sg'] = [f"{ota}n"]
		all_forms['pres|3sg'] = [f"{otta}{a}"]
		all_forms['past|1sg'] = [f"{ot}in"]
		all_forms['past|3sg'] = [f"{ott}i"]
		all_forms['cond|3sg'] = [f"{otta}isi"]
		all_forms['poten|3sg'] = [f"{otta}nee"]
		all_forms['imper|3sg'] = [f"{otta}k{oo}n"]
		all_forms['part_past'] = [f"{otta}n{u}t"]
		all_forms['pass|past'] = [f"{ote}ttiin"]
		all_forms['part_ma'] = [f"{otta}m{a}"]
		all_forms['pass|pres'] = [f"{ote}t{aa}n"]

	# "huutaa"
	elif kotus_class == "54":
		murta = word[:-1]
		murra = grad_weak(murta, gradtype)
		murre = murra[:-1] + 'e'
		murs = word[:-3] + 's'
		all_forms['pres|1sg'] = [f"{murra}n"]
		all_forms['pres|3sg'] = [f"{murta}{a}"]
		all_forms['past|1sg'] = [f"{murs}in"]
		all_forms['past|3sg'] = [f"{murs}i"]
		all_forms['cond|3sg'] = [f"{murta}isi"]
		all_forms['poten|3sg'] = [f"{murta}nee"]
		all_forms['imper|3sg'] = [f"{murta}k{oo}n"]
		all_forms['part_past'] = [f"{murta}n{u}t"]
		all_forms['pass|past'] = [f"{murre}ttiin"]
		all_forms['part_ma'] = [f"{murta}m{a}"]
		all_forms['pass|pres'] = [f"{murre}t{aa}n"]

	# "soutaa"
	elif kotus_class == "55":
		souta = word[:-1]
		souda = grad_weak(souta, gradtype)
		sout = souta[:-1]
		soude = souda[:-1] + 'e'
		soud = souda[:-1]
		sous = souda[:-2] + 's'
		all_forms['pres|1sg'] = [f"{souda}n"]
		all_forms['pres|3sg'] = [f"{souta}{a}"]
		all_forms['past|1sg'] = [f"{soud}in", f"{sous}in"]
		all_forms['past|3sg'] = [f"{sout}i", f"{sous}i"]
		all_forms['cond|3sg'] = [f"{souta}isi"]
		all_forms['poten|3sg'] = [f"{souta}nee"]
		all_forms['imper|3sg'] = [f"{souta}k{oo}n"]
		all_forms['part_past'] = [f"{souta}n{u}t"]
		all_forms['pass|past'] = [f"{soude}ttiin"]
		all_forms['part_ma'] = [f"{souta}m{a}"]
		all_forms['pass|pres'] = [f"{soude}t{aa}n"]

	# "kaivaa"
	elif kotus_class == "56":
		anta = word[:-1]
		anto = word[:-2] + o
		anna = grad_weak(anta, gradtype)
		anno = grad_weak(anto, gradtype)
		anne = anna[:-1] + 'e'
		all_forms['pres|1sg'] = [f"{anna}n"]
		all_forms['pres|3sg'] = [f"{anta}{a}"]
		all_forms['past|1sg'] = [f"{anno}in"]
		all_forms['past|3sg'] = [f"{anto}i"]
		all_forms['cond|3sg'] = [f"{anta}isi"]
		all_forms['poten|3sg'] = [f"{anta}nee"]
		all_forms['imper|3sg'] = [f"{anta}k{oo}n"]
		all_forms['part_past'] = [f"{anta}n{u}t"]
		all_forms['pass|past'] = [f"{anne}ttiin"]
		all_forms['part_ma'] = [f"{anta}m{a}"]
		all_forms['pass|pres'] = [f"{anne}t{aa}n"]

	# "saartaa"
	elif kotus_class == "57":
		saarta = word[:-1]
		saarto = word[:-2] + o
		saarra = grad_weak(saarta, gradtype)
		saarro = grad_weak(saarto, gradtype)
		saarre = saarra[:-1] + 'e'
		saars = word[:-3] + 's'
		all_forms['pres|1sg'] = [f"{saarra}n"]
		all_forms['pres|3sg'] = [f"{saarta}{a}"]
		all_forms['past|1sg'] = [f"{saarro}in", f"{saars}in"]
		all_forms['past|3sg'] = [f"{saarto}i", f"{saars}i"]
		all_forms['cond|3sg'] = [f"{saarta}isi"]
		all_forms['poten|3sg'] = [f"{saarta}nee"]
		all_forms['imper|3sg'] = [f"{saarta}k{oo}n"]
		all_forms['part_past'] = [f"{saarta}n{u}t"]
		all_forms['pass|past'] = [f"{saarre}ttiin"]
		all_forms['part_ma'] = [f"{saarta}m{a}"]
		all_forms['pass|pres'] = [f"{saarre}t{aa}n"]

	# "laskea"
	elif kotus_class == "58":
		luke = word[:-1]
		luki = word[:-2] + 'i'
		lue = grad_weak(luke, gradtype)
		lui = grad_weak(luki, gradtype)
		all_forms['pres|1sg'] = [f"{luke}{a}"]
		all_forms['pres|1sg'] = [f"{lue}n"]
		all_forms['pres|3sg'] = [f"{luke}e"]
		all_forms['past|1sg'] = [f"{lui}n"]
		all_forms['past|3sg'] = [f"{luki}"]
		all_forms['cond|3sg'] = [f"{luki}si"]
		all_forms['poten|3sg'] = [f"{luke}nee"]
		all_forms['imper|3sg'] = [f"{luke}k{oo}n"]
		all_forms['part_past'] = [f"{luke}n{u}t"]
		all_forms['pass|past'] = [f"{lue}ttiin"]
		all_forms['part_ma'] = [f"{luke}m{a}"]
		all_forms['pass|pres'] = [f"{lue}t{aa}n"]

	# "tuntea"
	elif kotus_class == "59":
		tunt = word[:-2]
		tunn = grad_weak(word[:-1], gradtype)[:-1]
		tuns = word[:-3] + 's'
		all_forms['pres|1sg'] = [f"{tunn}en"]
		all_forms['pres|3sg'] = [f"{tunt}ee"]
		all_forms['past|1sg'] = [f"{tuns}in"]
		all_forms['past|3sg'] = [f"{tuns}i"]
		all_forms['cond|3sg'] = [f"{tunt}isi"]
		all_forms['poten|3sg'] = [f"{tunt}enee"]
		all_forms['imper|3sg'] = [f"{tunt}ek{oo}n"]
		all_forms['part_past'] = [f"{tunt}en{u}t"]
		all_forms['pass|past'] = [f"{tunn}ettiin"]
		all_forms['part_ma'] = [f"{tunt}em{a}"]
		all_forms['pass|pres'] = [f"{tunn}et{aa}n"]

	# "lähteä"
	elif kotus_class == "60":
		pfx_ = word[:-6]
		all_forms['pres|1sg'] = [f"{pfx_}lähden"]
		all_forms['pres|3sg'] = [f"{pfx_}lähtee"]
		all_forms['past|1sg'] = [f"{pfx_}lähdin", f"{pfx_}läksin"]
		all_forms['past|3sg'] = [f"{pfx_}lähti", f"{pfx_}läksi"]
		all_forms['cond|3sg'] = [f"{pfx_}lähtisi"]
		all_forms['poten|3sg'] = [f"{pfx_}lähtenee"]
		all_forms['imper|3sg'] = [f"{pfx_}lähteköön"]
		all_forms['part_past'] = [f"{pfx_}lähtenyt"]
		all_forms['pass|past'] = [f"{pfx_}lähdettiin"]
		all_forms['part_ma'] = [f"{pfx_}lähtemä"]
		all_forms['pass|pres'] = [f"{pfx_}lähdetään"]

	# "sallia"
	elif kotus_class == "61":
		opp = word[:-2]
		op = grad_weak(word[:-1], gradtype)[:-1]
		all_forms['pres|1sg'] = [f"{op}in"]
		all_forms['pres|3sg'] = [f"{opp}ii"]
		all_forms['past|1sg'] = [f"{op}in"]
		all_forms['past|3sg'] = [f"{opp}i"]
		all_forms['cond|3sg'] = [f"{opp}isi"]
		all_forms['poten|3sg'] = [f"{opp}inee"]
		all_forms['imper|3sg'] = [f"{opp}ik{oo}n"]
		all_forms['part_past'] = [f"{opp}in{u}t"]
		all_forms['pass|past'] = [f"{op}ittiin"]
		all_forms['part_ma'] = [f"{opp}im{a}"]
		all_forms['pass|pres'] = [f"{op}it{aa}n"]

	# "voida"
	elif kotus_class == "62":
		vo = word[:-3]
		all_forms['pres|1sg'] = [f"{vo}in"]
		all_forms['pres|3sg'] = [f"{vo}i"]
		all_forms['past|1sg'] = [f"{vo}in"]
		all_forms['past|3sg'] = [f"{vo}i"]
		all_forms['cond|3sg'] = [f"{vo}isi"]
		all_forms['poten|3sg'] = [f"{vo}inee"]
		all_forms['imper|3sg'] = [f"{vo}ik{oo}n"]
		all_forms['part_past'] = [f"{vo}in{u}t"]
		all_forms['pass|past'] = [f"{vo}itiin"]
		all_forms['part_ma'] = [f"{vo}im{a}"]
		all_forms['pass|pres'] = [f"{vo}id{aa}n"]

	# "saada"
	elif kotus_class == "63":
		saa = word[:-2]
		sa = word[:-3]
		all_forms['pres|1sg'] = [f"{saa}n"]
		all_forms['pres|3sg'] = [f"{saa}"]
		all_forms['past|1sg'] = [f"{sa}in"]
		all_forms['past|3sg'] = [f"{sa}i"]
		all_forms['cond|3sg'] = [f"{sa}isi"]
		all_forms['poten|3sg'] = [f"{saa}nee"]
		all_forms['imper|3sg'] = [f"{saa}k{oo}n"]
		all_forms['part_past'] = [f"{saa}n{u}t"]
		all_forms['pass|past'] = [f"{saa}tiin"]
		all_forms['part_ma'] = [f"{saa}m{a}"]
		all_forms['pass|pres'] = [f"{saa}d{aa}n"]

	# "juoda"
	elif kotus_class == "64":
		juo = word[:-2]
		jo = word[:-4] + word[-3]
		all_forms['pres|1sg'] = [f"{juo}n"]
		all_forms['pres|3sg'] = [f"{juo}"]
		all_forms['past|1sg'] = [f"{jo}in"]
		all_forms['past|3sg'] = [f"{jo}i"]
		all_forms['cond|3sg'] = [f"{jo}isi"]
		all_forms['poten|3sg'] = [f"{juo}nee"]
		all_forms['imper|3sg'] = [f"{juo}k{oo}n"]
		all_forms['part_past'] = [f"{juo}n{u}t"]
		all_forms['pass|past'] = [f"{juo}tiin"]
		all_forms['part_ma'] = [f"{juo}m{a}"]
		all_forms['pass|pres'] = [f"{juo}d{aa}n"]

	# "käydä"
	elif kotus_class == "65":
		pfx_ = word[:-5]
		all_forms['pres|1sg'] = [f"{pfx_}käyn"]
		all_forms['pres|3sg'] = [f"{pfx_}käy"]
		all_forms['past|1sg'] = [f"{pfx_}kävin"]
		all_forms['past|3sg'] = [f"{pfx_}kävi"]
		all_forms['cond|3sg'] = [f"{pfx_}kävisi"]
		all_forms['poten|3sg'] = [f"{pfx_}käynee"]
		all_forms['imper|3sg'] = [f"{pfx_}käyköön"]
		all_forms['part_past'] = [f"{pfx_}käynyt"]
		all_forms['pass|past'] = [f"{pfx_}käytiin"]
		all_forms['part_ma'] = [f"{pfx_}käymä"]
		all_forms['pass|pres'] = [f"{pfx_}käydään"]

	# "seistä"
	elif kotus_class == "66" and word == 'seistä':
		all_forms['pres|1sg'] = ["seison"]
		all_forms['pres|3sg'] = ["seisoo"]
		all_forms['past|1sg'] = ["seisoin"]
		all_forms['past|3sg'] = ["seisoi"]
		all_forms['cond|3sg'] = ["seisoisi"]
		all_forms['poten|3sg'] = ["seissee"]
		all_forms['imper|3sg'] = ["seisköön"]
		all_forms['part_past'] = ["seissyt"]
		all_forms['pass|past'] = ["seistiin"]
		all_forms['part_ma'] = ["seisoma"]
		all_forms['pass|pres'] = ["seistään"]

	# "rohkaista"
	elif kotus_class == "66":
		vavi = word[:-3]
		vapi = grad_strong(vavi, gradtype)
		all_forms['pres|1sg'] = [f"{vapi}sen"]
		all_forms['pres|3sg'] = [f"{vapi}see"]
		all_forms['past|1sg'] = [f"{vapi}sin"]
		all_forms['past|3sg'] = [f"{vapi}si"]
		all_forms['cond|3sg'] = [f"{vapi}sisi"]
		all_forms['poten|3sg'] = [f"{vavi}ssee"]
		all_forms['imper|3sg'] = [f"{vavi}sk{oo}n"]
		all_forms['part_past'] = [f"{vavi}ss{u}t"]
		all_forms['pass|past'] = [f"{vavi}stiin"]
		all_forms['part_ma'] = [f"{vapi}sem{a}"]
		all_forms['pass|pres'] = [f"{vavi}st{aa}n"]

	# "tulla"
	elif kotus_class == "67":
		l = word[-2]
		ajate = word[:-3]
		ajatte = grad_strong(ajate, gradtype)
		all_forms['pres|1sg'] = [f"{ajatte}{l}en"]
		all_forms['pres|3sg'] = [f"{ajatte}{l}ee"]
		all_forms['past|1sg'] = [f"{ajatte}{l}in"]
		all_forms['past|3sg'] = [f"{ajatte}{l}i"]
		all_forms['cond|3sg'] = [f"{ajatte}{l}isi"]
		all_forms['poten|3sg'] = [f"{ajate}{l}{l}ee"]
		all_forms['imper|3sg'] = [f"{ajate}{l}k{oo}n"]
		all_forms['part_past'] = [f"{ajate}{l}{l}{u}t"]
		all_forms['pass|past'] = [f"{ajate}{l}tiin"]
		all_forms['part_ma'] = [f"{ajatte}{l}em{a}"]
		all_forms['pass|pres'] = [f"{ajate}{l}{l}{aa}n"]

	# "tupakoida"
	elif kotus_class == "68":
		tupako = word[:-3]
		all_forms['pres|1sg'] = [f"{tupako}in"]
		all_forms['pres|3sg'] = [f"{tupako}i"]
		all_forms['past|1sg'] = [f"{tupako}in"]
		all_forms['past|3sg'] = [f"{tupako}i"]
		all_forms['cond|3sg'] = [f"{tupako}isi"]
		all_forms['poten|3sg'] = [f"{tupako}inee"]
		all_forms['imper|3sg'] = [f"{tupako}ik{oo}n"]
		all_forms['part_past'] = [f"{tupako}in{u}t"]
		all_forms['pass|past'] = [f"{tupako}itiin"]
		all_forms['part_ma'] = [f"{tupako}im{a}"]
		all_forms['part_ma|rare'] = [f"{tupako}itsem{a}"]
		all_forms['pass|pres'] = [f"{tupako}id{aa}n"]

		all_forms['pres|1sg|rare'] = [f"{tupako}itsen"]
		all_forms['pres|3sg|rare'] = [f"{tupako}itsee"]
		all_forms['past|1sg|rare'] = [f"{tupako}itsin"]
		all_forms['past|3sg|rare'] = [f"{tupako}itsi"]
		all_forms['cond|3sg|rare'] = [f"{tupako}itsisi"]

	# "valita"
	elif kotus_class == "69":
		vali = word[:-2]
		all_forms['pres|1sg'] = [f"{vali}tsen"]
		all_forms['pres|3sg'] = [f"{vali}tsee"]
		all_forms['past|1sg'] = [f"{vali}tsin"]
		all_forms['past|3sg'] = [f"{vali}tsi"]
		all_forms['cond|3sg'] = [f"{vali}tsisi"]
		all_forms['poten|3sg'] = [f"{vali}nnee"]
		all_forms['imper|3sg'] = [f"{vali}tk{oo}n"]
		all_forms['part_past'] = [f"{vali}nn{u}t"]
		all_forms['pass|past'] = [f"{vali}ttiin"]
		all_forms['part_ma'] = [f"{vali}tsem{a}"]
		all_forms['pass|pres'] = [f"{vali}t{aa}n"]

	# "juosta"
	elif kotus_class == "70":
		juo = word[:-3]
		all_forms['pres|1sg'] = [f"{juo}ksen"]
		all_forms['pres|3sg'] = [f"{juo}ksee"]
		all_forms['past|1sg'] = [f"{juo}ksin"]
		all_forms['past|3sg'] = [f"{juo}ksi"]
		all_forms['cond|3sg'] = [f"{juo}ksisi"]
		all_forms['poten|3sg'] = [f"{juo}ssee"]
		all_forms['imper|3sg'] = [f"{juo}sk{oo}n"]
		all_forms['part_past'] = [f"{juo}ss{u}t"]
		all_forms['pass|past'] = [f"{juo}stiin"]
		all_forms['part_ma'] = [f"{juo}ksem{a}"]
		all_forms['pass|pres'] = [f"{juo}st{aa}n"]
		all_forms['poten|3sg|nstd'] = [f"{juo}ksenee"]

	# "nähdä"
	elif kotus_class == "71":
		te = word[:-3]
		all_forms['pres|1sg'] = [f"{te}en"]
		all_forms['pres|3sg'] = [f"{te}kee"]
		all_forms['past|1sg'] = [f"{te}in"]
		all_forms['past|3sg'] = [f"{te}ki"]
		all_forms['cond|3sg'] = [f"{te}kisi"]
		all_forms['poten|3sg'] = [f"{te}hnee"]
		all_forms['imper|3sg'] = [f"{te}hköön"]
		all_forms['part_past'] = [f"{te}hnyt"]
		all_forms['pass|past'] = [f"{te}htiin"]
		all_forms['part_ma'] = [f"{te}kemä"]
		all_forms['pass|pres'] = [f"{te}hdään"]

	# "vanheta"
	elif kotus_class == "72":
		valje = word[:-2]
		valke = grad_strong(valje, gradtype)
		all_forms['pres|1sg'] = [f"{valke}nen"]
		all_forms['pres|3sg'] = [f"{valke}nee"]
		all_forms['past|1sg'] = [f"{valke}nin"]
		all_forms['past|3sg'] = [f"{valke}ni"]
		all_forms['cond|3sg'] = [f"{valke}nisi"]
		all_forms['poten|3sg'] = [f"{valje}nnee"]
		all_forms['imper|3sg'] = [f"{valje}tk{oo}n"]
		all_forms['part_past'] = [f"{valje}nn{u}t"]
		all_forms['pass|past'] = [f"{valje}ttiin"]
		all_forms['part_ma'] = [f"{valke}nem{a}"]
		all_forms['pass|pres'] = [f"{valje}t{aa}n"]

	# "salata"
	elif kotus_class == "73":
		haka = word[:-2]
		hakka = grad_strong(haka, gradtype)
		all_forms['pres|1sg'] = [f"{hakka}{a}n"]
		all_forms['pres|3sg'] = [f"{hakka}{a}"]
		all_forms['past|1sg'] = [f"{hakka}sin"]
		all_forms['past|3sg'] = [f"{hakka}si"]
		all_forms['cond|3sg'] = [f"{hakka}isi"]
		all_forms['poten|3sg'] = [f"{haka}nnee"]
		all_forms['imper|3sg'] = [f"{haka}tk{oo}n"]
		all_forms['part_past'] = [f"{haka}nn{u}t"]
		all_forms['pass|past'] = [f"{haka}ttiin"]
		all_forms['part_ma'] = [f"{hakka}{a}m{a}"]
		all_forms['pass|pres'] = [f"{haka}t{aa}n"]

	# "katketa"
	elif kotus_class == "74":
		poike = word[:-2]
		poikke = grad_strong(poike, gradtype)
		all_forms['pres|1sg'] = [f"{poikke}{a}n"]
		all_forms['pres|3sg'] = [f"{poikke}{a}{a}"]
		all_forms['past|1sg'] = [f"{poikke}sin"]
		all_forms['past|3sg'] = [f"{poikke}si"]
		all_forms['cond|3sg'] = [f"{poikke}{a}isi"]
		all_forms['cond|3sg|rare'] = [f"{poikke}isi"]
		all_forms['poten|3sg'] = [f"{poike}nnee"]
		all_forms['imper|3sg'] = [f"{poike}tk{oo}n"]
		all_forms['part_past'] = [f"{poike}nn{u}t"]
		all_forms['pass|past'] = [f"{poike}ttiin"]
		all_forms['part_ma'] = [f"{poikke}{a}m{a}"]
		all_forms['pass|pres'] = [f"{poike}t{aa}n"]

	# "selvitä"
	elif kotus_class == "75":
		peito = word[:-2]
		peitto = grad_strong(peito, gradtype)
		all_forms['pres|1sg'] = [f"{peitto}{a}n"]
		all_forms['pres|3sg'] = [f"{peitto}{a}{a}"]
		all_forms['past|1sg'] = [f"{peitto}sin"]
		all_forms['past|3sg'] = [f"{peitto}si"]
		all_forms['cond|3sg'] = [f"{peitto}{a}isi"]
		all_forms['poten|3sg'] = [f"{peito}nnee"]
		all_forms['imper|3sg'] = [f"{peito}tk{oo}n"]
		all_forms['part_past'] = [f"{peito}nn{u}t"]
		all_forms['pass|past'] = [f"{peito}ttiin"]
		all_forms['part_ma'] = [f"{peitto}{a}m{a}"]
		all_forms['pass|pres'] = [f"{peito}t{aa}n"]

	# "taitaa"
	elif kotus_class == "76":
		taita = word[:-1]
		taida = word[:-3] + f'd{a}'
		tais = word[:-3] + 's'
		tain = word[:-3] + 'n'
		taide = word[:-3] + 'de'
		all_forms['pres|1sg'] = [f"{taida}n"]
		all_forms['pres|3sg'] = [f"{taita}{a}"]
		all_forms['past|1sg'] = [f"{tais}in"]
		all_forms['past|3sg'] = [f"{tais}i"]
		all_forms['cond|3sg'] = [f"{taita}isi"]
		all_forms['poten|3sg'] = [f"{taita}nee", f"{tain}nee"]
		all_forms['imper|3sg'] = [f"{taita}k{oo}n"]
		all_forms['part_past'] = [f"{tain}n{u}t", f"{taita}n{u}t"]
		all_forms['pass|past'] = [f"{taide}ttiin"]
		all_forms['part_ma'] = [f"{taita}m{a}"]
		all_forms['pass|pres'] = [f"{taide}t{aa}n"]

	# "halata" : "halajan"
	elif kotus_class == "77" and word in ['avata', 'halata', 'palata']:
		avaja = word[:-2] + f'j{a}'
		avaji = word[:-2] + f'ji'
		all_forms['pres|1sg|rare'] = [f"{avaja}n"]
		all_forms['pres|3sg|rare'] = [f"{avaja}{a}"]
		all_forms['past|1sg|rare'] = [f"{avaji}n"]
		all_forms['past|3sg|rare'] = [f"{avaji}"]
		all_forms['cond|3sg|rare'] = [f"{avaja}isi"]

	# "kumajaa" (vaill.)
	elif kotus_class == "77":
		kumaja = word[:-1]
		kumaj = word[:-2]
		all_forms['pres|3sg'] = [f"{kumaja}{a}"]
		all_forms['pres|3pl'] = [f"{kumaja}v{a}t"]
		all_forms['part_pres'] = [f"{kumaja}v{a}"]
		all_forms['past|3sg|rare'] = [f"{kumaj}i"]
		all_forms['past|3pl|rare'] = [f"{kumaj}iv{a}t"]
		all_forms['cond|3sg'] = [f"{kumaja}isi"]
		all_forms['cond|3pl'] = [f"{kumaja}isiv{a}t"]

	# "kaikaa" (vaill.)
	elif kotus_class == "78":
		kaika = word[:-1]
		all_forms['pres|3sg'] = [f"{kaika}{a}"]
		all_forms['pres|3pl'] = [f"{kaika}v{a}t"]
		all_forms['part_pres'] = [f"{kaika}v{a}"]
		all_forms['cond|3sg'] = [f"{kaika}isi"]
		all_forms['cond|3pl'] = [f"{kaika}isiv{a}t"]
		all_forms['inf1'] = [word]

	# "erkanee"
	elif kotus_class == "ERKANEE":
		erkan = word[:-2]
		all_forms['pres|1sg'] = [f"{erkan}en"]
		all_forms['pres|3sg'] = [f"{erkan}ee"]
		all_forms['past|1sg'] = [f"{erkan}in"]
		all_forms['past|3sg'] = [f"{erkan}i"]
		all_forms['cond|3sg'] = [f"{erkan}isi"]
		all_forms['part_ma'] = [f"{erkan}em{a}"]
		all_forms['inf1'] = []

	# "kutiaa" : "kutian" : "kutisin" : "kutiamaan"
	elif kotus_class == "KUTIAA":
		kutia = word[:-2] + f'{a}'
		kutisi = word[:-2] + f'si'
		all_forms['pres|1sg|rare'] = [f"{kutia}n"]
		all_forms['pres|3sg|rare'] = [f"{kutia}{a}"]
		all_forms['past|1sg|rare'] = [f"{kutisi}n"]
		all_forms['past|3sg|rare'] = [f"{kutisi}"]
		all_forms['cond|3sg|rare'] = [f"{kutia}isi"]
		all_forms['part_ma'] = [f"{kutia}m{a}"]
		all_forms['inf1'] = []

	elif kotus_class == 'EI':
		pfx = word[:-2]
		return {
			'1sg': [f'{pfx}en'],
			'2sg': [f'{pfx}et'],
			'3sg': [f'{pfx}ei'],
			'1pl': [f'{pfx}emme'],
			'2pl': [f'{pfx}ette'],
			'3pl': [f'{pfx}eivät'],
			'@base': [f'{pfx}ei'],
		}

	else:
		print(f'Unknown class for verb "{word}": {kotus_class}')
		return {'@base': [word], '': [word]}

	if kotus_class in ['77', '78']:
		return clean(all_forms)

	if all_forms.get('inf1'):
		[lukea] = all_forms['inf1']
		luke = lukea[:-1]
		luki = luke[:-1] + 'i' if luke.endswith('e') else luke
		all_forms['inf1|tra'] = [f'{lukea}kseen']
		all_forms['inf2|ins'] = [f'{luki}en']
		all_forms['inf2|ine'] = [f'{luki}ess{a}']
		all_forms['past|conneg|sg'] = all_forms['part_past']
		all_forms['past|conneg|pl'] = [val[:-2] + 'eet' for val in all_forms['part_past']]

	for style in {'', '|rare', '|nstd'}:
		for jaa in [f[:-1] for f in all_forms[f'pres|1sg{style}']]:
			all_forms[f'pres|2sg{style}'] += [f"{jaa}t"]
			all_forms[f'pres|1pl{style}'] += [f"{jaa}mme"]
			all_forms[f'pres|2pl{style}'] += [f"{jaa}tte"]
			all_forms[f'imper|2sg{style}'] += [f"{jaa}"]
			all_forms[f'pres|conneg{style}'] += [f"{jaa}"]
			all_forms[f'imper|2sg|conneg{style}'] += [f"{jaa}"]

		for jaoi in [f[:-1] for f in all_forms[f'past|1sg{style}']]:
			all_forms[f'past|2sg{style}'] += [f"{jaoi}t"]
			all_forms[f'past|1pl{style}'] += [f"{jaoi}mme"]
			all_forms[f'past|2pl{style}'] += [f"{jaoi}tte"]

		for jakak in [f[:-3] for f in all_forms[f'imper|3sg{style}']]:
			all_forms[f'imper|2pl{style}'] += [f"{jakak}{aa}"]
			all_forms[f'imper|3pl{style}'] += [f"{jakak}{oo}t"]
			all_forms[f'imper|1pl'] = [f"{jakak}{aa}mme"]
			all_forms[f'imper|2pl|rare'] = [f"{jakak}{aa}tte"]
			all_forms[f'imper|2pl|arch'] = [f"{jakak}{aa}t"]
			all_forms[f'imper|2pl|nstd'] = [f"{jakak}{aa}tten"]
			all_forms[f'imper|pl|conneg'] = [f"{jakak}{o}"]
			all_forms[f'imper|3sg|conneg'] = [f"{jakak}{o}"]

		for jaeta in [f[:-2] for f in all_forms[f'pass|pres{style}']]:
			all_forms[f'pass|pres{style}'] += [f"{jaeta}{a}n"]
			all_forms[f'pass|pres|conneg{style}'] += [f"{jaeta}"]

		for jaett in [f[:-3] for f in all_forms[f'pass|past{style}']]:
			a, o, u, _, _, _ = HARMONY_MAPPING[determine_harmony(jaett)]
			all_forms[f'pass|past{style}'] += [f"{jaett}iin"]
			all_forms[f'pass|cond{style}'] += [f"{jaett}{a}isiin"]
			all_forms[f'pass|poten{style}'] += [f"{jaett}{a}neen"]
			all_forms[f'pass|imper{style}'] += [f"{jaett}{a}k{oo}n"]
			all_forms[f'pass|past|conneg{style}'] += [f"{jaett}{u}"]
			all_forms[f'pass|cond|conneg{style}'] += [f"{jaett}{a}isi"]
			all_forms[f'pass|poten|conneg{style}'] += [f"{jaett}{a}ne"]
			all_forms[f'pass|imper|conneg{style}'] += [f"{jaett}{a}k{o}"]
			all_forms[f'pass|part_pres{style}'] += [f"{jaett}{a}v{a}"]
			all_forms[f'pass|part_past{style}'] += [f"{jaett}{u}"]
			all_forms[f'pass|part_past|sg|par{style}'] += [f"{jaett}{u}{a}"]
			all_forms[f'pass|inf2|ine{style}'] = [f"{jaett}{a}ess{a}"]
			all_forms[f'pass|inf3|ins{style}'] += [f"{jaett}{a}m{a}n"]

		for jaka in [f[:-2] for f in all_forms[f'part_ma{style}']]:
			a, o, _, aa, _, _ = HARMONY_MAPPING[determine_harmony(jaka)]
			all_forms[f'part_pres{style}'] += [f"{jaka}v{a}"]
			all_forms[f'part_maton{style}'] += [f"{jaka}m{a}t{o}n"]
			all_forms[f'pres|3pl{style}'] += [f"{jaka}v{a}t"]
			all_forms[f'inf3{style}|ine'] = [f"{jaka}m{a}ss{a}"]
			all_forms[f'inf3{style}|ela'] = [f"{jaka}m{a}st{a}"]
			all_forms[f'inf3{style}|ill'] = [f"{jaka}m{aa}n"]
			all_forms[f'inf3{style}|ade'] = [f"{jaka}m{a}ll{a}"]
			all_forms[f'inf3{style}|abe'] = [f"{jaka}m{a}tt{a}"]
			all_forms[f'inf3{style}|ins'] = [f"{jaka}m{a}n"]
			all_forms[f'inf4{style}'] = [f"{jaka}minen"]
			all_forms[f'inf5{style}'] = [f"{jaka}m{a}isill{aa}n"]

		for jakoi in [f for f in all_forms[f'past|3sg{style}']]:
			a, _, _, _, _, _ = HARMONY_MAPPING[determine_harmony(jakoi)]
			all_forms[f'past|3pl{style}'] += [f"{jakoi}v{a}t"]

		for jakaisi in [f for f in all_forms[f'cond|3sg{style}']]:
			a, _, _, _, _, _ = HARMONY_MAPPING[determine_harmony(jakaisi)]
			all_forms[f'cond|1sg{style}'] += [f"{jakaisi}n"]
			all_forms[f'cond|2sg{style}'] += [f"{jakaisi}t"]
			all_forms[f'cond|3sg{style}'] += [f"{jakaisi}"]
			all_forms[f'cond|1pl{style}'] += [f"{jakaisi}mme"]
			all_forms[f'cond|2pl{style}'] += [f"{jakaisi}tte"]
			all_forms[f'cond|3pl{style}'] += [f"{jakaisi}v{a}t"]
			all_forms[f'cond|conneg{style}'] += [f"{jakaisi}"]

		for jakane in [f[:-1] for f in all_forms[f'poten|3sg{style}']]:
			a, _, _, _, _, _ = HARMONY_MAPPING[determine_harmony(jakane)]
			all_forms[f'poten|1sg{style}'] += [f"{jakane}n"]
			all_forms[f'poten|2sg{style}'] += [f"{jakane}t"]
			all_forms[f'poten|3sg{style}'] += [f"{jakane}e"]
			all_forms[f'poten|1pl{style}'] += [f"{jakane}mme"]
			all_forms[f'poten|2pl{style}'] += [f"{jakane}tte"]
			all_forms[f'poten|3pl{style}'] += [f"{jakane}v{a}t"]
			all_forms[f'poten|conneg{style}'] += [f"{jakane}"]

	# Irregular forms of "olla" that cannot be derived from other forms
	if word == 'olla':
		all_forms['pres|3pl'] = ['ovat']
		all_forms['pres|3sg|poet'] = ['ompi']
		all_forms['poten|3sg|poet'] = ['lie']

	# Verb type "erkanee" does not actually have this participle
	if kotus_class == 'ERKANEE':
		all_forms['part_ma'] = []

	all_forms['deriv_agent'] = derive_agent_noun(all_forms)
	all_forms['deriv_action'] = derive_action_noun(all_forms)

	return clean(all_forms)


def inflect_noun_pl(word, kotus_class, gradtype=None, harmony=None, vowel=None):

	if not kotus_class:
		return {'': [word], '@base': [word]}

	singular = plural2singular(word, kotus_class, gradtype)
	inflections = inflect_noun(singular, kotus_class, gradtype, harmony, vowel)
	[sg_essive] = inflections.pop('sg|ess')
	inflections = {key[3:]: val for key, val in inflections.items() if key.startswith('pl|')}
	inflections['@stem:possessives:nom'] = [sg_essive[:-2]]
	inflections['@stem:possessives'] = []
	inflections['@base'] = inflections['nom']
	return inflections


def inflect_adjective(word, kotus_class, gradtype=None, harmony=None, vowel=None, info=''):
	inflections = inflect_noun(word, kotus_class, gradtype, harmony, vowel)
	if 'non-comparable' not in info:
		inflections.update(get_comparison(word, inflections, kotus_class))
	if '+poss' not in info:
		inflections['@stem:possessives'] = []
	inflections['@stem:clitics'] = []
	return inflections


def inflect_adposition(word, info=''):

	if info == 'no-poss':
		return {'@base': [word], '': [word]}

	# tähden => tähte|ni, -si, -nsä
	if word == 'tähden':
		return {'@base': [word], '': [word], '@stem:possessives': ['tähte']}
	if word == 'nähden':
		return {'@base': [word], '': [word], '@stem:possessives': ['nähte']}

	# eteen => etee|ni, -si, -nsä
	if re.fullmatch('.+n', word):
		etee = word[:-1]
		return {'@base': [word], '': [word], '@stem:possessives': [etee]}

	# vuoksi => vuokse|ni, -si, -nsa
	if re.fullmatch('.+ksi', word):
		vuoks = word[:-1]
		vuokse = f'{vuoks}e'
		return {'@base': [word], '': [word], '@stem:possessives': [vuokse]}

	return {'@base': [word], '': [word],  '@stem:possessives': [word]}


def inflect_adverb(word, info):

	info = info or ''

	# Adverb w/ possessive suffix
	if re.fullmatch('.+(an|än|en)', word) and '+poss' in info:
		hajalla = word[:-2]
		inflections = {'@stem:possessives': [hajalla]}
	elif re.fullmatch('.+(h[aeiou]nsa|h[äeiöy]nsä)', word) and '+poss' in info:
		haltioihi = word[:-3]
		inflections = {'@stem:possessives': [haltioihi]}
	elif '+poss' in info:
		inflections = {'@stem:possessives': [word]}

	elif word.endswith('isesti'):
		ilois = word[:-4]
		inflections = {'': [f'{ilois}esti'], 'comparative': [f'{ilois}emmin'], 'superlative': [f'{ilois}immin']}
	elif word.endswith('iisti'):
		kaun = word[:-5]
		inflections = {'': [f'{kaun}iisti'], 'comparative': [f'{kaun}iimmin'], 'superlative': [f'{kaun}eimmin', f'{kaun}eiten']}
	elif re.fullmatch('(eä|ea|aa|ää)sti', word):
		surkea = word[:-3]
		surke = word[:-4]
		inflections = {'': [f'{surkea}sti'], 'comparative': [f'{surkea}mmin'], 'superlative': [f'{surke}immin', f'{surke}iten']}
	else:
		inflections = copy.deepcopy(ADVERB_INFLECTIONS.get(word)) or {'': [word]}

	inflections['@base'] = [word]
	return inflections


def inflect(word, pos, kotus_class=None, gradation=None, harmony=None, vowel=None, info=''):

	if not pos:
		return {}

	kotus_class = kotus_class or ''
	gradation = gradation or ''
	info = info or ''

	# TODO: Add patching function to adjust inflections of individual words

	if '|' in kotus_class:
		class1, class2 = kotus_class.split('|')
		style = 'dial' if '‡' in class2 else 'nstd' if '†' in class2 else ''
		inflections1 = inflect(word, pos, class1, gradation)
		inflections2 = inflect(word, pos, class2, gradation)
		return merge_inflections(inflections1, inflections2, secondary_tag=style)

	if '|' in gradation:
		grad1, grad2 = gradation.split('|')
		style = 'dial' if '‡' in grad2 else 'nstd' if '†' in grad2 else ''
		inflections1 = inflect(word, pos, kotus_class, grad1)
		inflections2 = inflect(word, pos, kotus_class, grad2)
		return merge_inflections(inflections1, inflections2, secondary_tag=style)

	kotus_class = kotus_class.replace('†', '').replace('‡', '')
	gradation = gradation.replace('†', '').replace('‡', '')

	if info == '#':
		return {'': [word], '@base': [word]}

	elif pos == 'noun':
		return inflect_noun(word, kotus_class, gradation, harmony, vowel)
	elif pos == 'noun-pl':
		return inflect_noun_pl(word, kotus_class, gradation, harmony, vowel)
	elif pos == 'proper':
		return inflect_noun(word, kotus_class, gradation, harmony, vowel)
	elif pos == 'proper-pl':
		return inflect_noun_pl(word, kotus_class, gradation, harmony, vowel)
	elif kotus_class == 'EI':
		return inflect_verb(word, kotus_class, gradation, harmony)
	elif pos == 'verb':
		return inflect_verb(word, kotus_class, gradation, harmony)
	elif pos == 'adjective':
		return inflect_adjective(word, kotus_class, gradation, harmony, vowel, info)
	elif pos == 'adverb':
		return inflect_adverb(word, info)
	elif pos == 'adposition':
		return inflect_adposition(word, info)
	elif pos == 'ordinal':
		return inflect_noun(word, kotus_class, gradation, harmony, vowel)
	elif pos == 'numeral':
		return inflect_noun(word, kotus_class, gradation, harmony, vowel)
	elif pos == 'pronoun':
		return inflect_noun(word, kotus_class, gradation, harmony, vowel)
	elif pos == 'pronoun-pl':
		return inflect_noun_pl(word, kotus_class, gradation, harmony, vowel)
	elif pos == 'noun|adjective':
		return inflect_noun(word, kotus_class, gradation, harmony, vowel)
	elif pos == 'participle':
		return inflect_noun(word, kotus_class, gradation, harmony, vowel)
	else:
		'???'

	return {'': [word], '@base': [word]}
