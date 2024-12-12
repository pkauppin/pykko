#! /usr/bin/env python3

import sys
import hfst
from datetime import datetime
from scripts.constants import ALPHA_UPPER, TAB, PARSER_FST_PATH, POS_TAGS


def lexc2fst(filename):

	time1 = datetime.now()

	print('—' * 64)
	print('Compiling parser FST:')

	print(f'Compiling LexC "{filename}"...')
	fst = hfst.compile_lexc_file(filename, verbosity=0, output=sys.stdout)

	print('Composing (1)...')
	# Enable substituting uppercase letters with lowercase equivalents in input
	# NB! Do not allow everywhere in input – guesser will go haywire
	enable_lowercase = hfst.regex(
		' ,, '.join(f'"{c}" -> [ "{c}" | "{c.lower()}"::1.0 ] || .#. _' for c in ALPHA_UPPER)
	)
	fst = hfst.compose([fst, enable_lowercase])

	print('Inverting...')
	fst.invert()

	print('Composing (2)...')
	# Enable capitalization of initial letter
	optional_initial_capitals = hfst.regex(
		' ,, '.join(f'"{c}" -> [ "{c}" | "{c.lower()}"::1.0 ] || .#. _' for c in ALPHA_UPPER)
	)
	fst = hfst.compose([optional_initial_capitals, fst])

	print('Normalizing...')
	replace_special1 = hfst.regex(f' ,, '.join(f'"{TAB}" "^{pos}" "{TAB}" -> "\t{pos}\t"' for pos in POS_TAGS))
	replace_special2 = hfst.regex(f'"{TAB}" -> "\t"')
	normalize_apostrophes = hfst.regex('"\'" -> "’"')
	fst = hfst.compose([normalize_apostrophes, fst, replace_special1, replace_special2])

	print('Optimizing...')
	fst.minimize()
	fst.convert(hfst.ImplementationType.HFST_OLW_TYPE)

	print('Done.')
	time2 = datetime.now()
	print('Time taken:', time2 - time1)

	return fst


def main():
	fst = lexc2fst('fi.lexc')
	output_stream = hfst.HfstOutputStream(filename=PARSER_FST_PATH, type=hfst.ImplementationType.HFST_OLW_TYPE)
	output_stream.write(fst)
	output_stream.close()


if __name__ == '__main__':
	main()
