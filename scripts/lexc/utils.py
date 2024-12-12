import re
from scripts.utils import has_agreement, ADVERB_INFLECTIONS
from scripts.constants import TAB, EPSILON
from scripts.file_tools import read_tsv


class InflectionProperties:
	def __init__(self, infl_class=None, gradation=None, harmony=None, chroneme=None, info=None):
		self.infl_class = infl_class
		self.gradation = gradation
		self.harmony = harmony
		self.chroneme = chroneme
		self.info = info

	def __str__(self):
		return str((self.infl_class, self.gradation, self.harmony, self.chroneme))


NoneInfl = InflectionProperties()


def get_compound_parts(word: str, irregular=False):
	if irregular:
		return [], word
	if has_agreement(word):
		return [], word
	compound_parts = word.split('|')
	lemma = compound_parts.pop()
	return compound_parts, lemma


def get_lemma_head_strings(head: str, compound_parts: list):
	compound_parts.append(head)
	head1 = '|'.join(compound_parts)
	head2 = '0'.join(compound_parts)
	return head1, head2


def get_pos_sublexicon_name(pos: str, regex_name: str=None, lemma=None, info=None):

	info = info or ''

	if regex_name:
		regex_name = \
			'Cap' if regex_name == 'Cap' else \
			'Vä' if regex_name == 'Vä' else \
			'Va' if regex_name == 'Va' else \
			'Any'
		return f'GUESSER_{regex_name}_{pos}'.upper()

	if info == 'compound-only':
		return f'COMPOUND_ONLY'

	name = pos.upper()
	if len(lemma or '') < 2 and pos in ['noun', 'noun-pl']:
		name += '_NOPFX'
	elif 'non-compounding' in info:
		name += '_NOPFX'
	elif pos in ['noun', 'noun-pl'] and re.findall('foreign|abbr|unit|symbol', info):
		name += '_NOPFX'
	elif pos == 'adverb' and not ADVERB_INFLECTIONS.get(lemma):
		name += '_NOPFX'

	return name


def get_field_separators(pos, homonym=None, style=None, auxname=None):
	if auxname:
		return []
	return [
		TAB, f'^{pos}',
		TAB, homonym or '0',
		TAB, style or '0',
		TAB,
	]


def read_irregular():
	all_inflections = {}
	for row in read_tsv('special.tsv', directory='scripts/lexc'):

		wform, lemma, pos, style, tags = row
		key = lemma, pos, style

		tags = tags.strip('+').replace('+', '|')
		all_inflections[key] = inflections = all_inflections.get(key, {})
		inflections[tags] = inflections.get(tags, []) + [wform]

	return all_inflections


def escape_lexc_symbol(s, escape_zeros=False):

	"""
	Escape special LexC characters
	"""

	if s in [' ', '%', ':', ';', '!', '?', '<', '>', '"']:
		return '%' + s
	if escape_zeros and s == '0':
		return '%0'
	if s in ['', EPSILON, '@none']:
		return '0'
	return s


def escape_lexc_string(s, escape_zeros=False):

	"""
	Escape special LexC characters
	"""

	return ''.join(escape_lexc_symbol(x, escape_zeros) for x in s)