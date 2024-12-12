#! /usr/bin/env python3

import sys
import hfst
from datetime import datetime
from scripts.constants import GENERATOR_FST_PATH, STYLE_TAGS


def collect_style_tags(filename):
	style_tags = set()
	with open(filename, 'r') as file:
		for line in file:
			line = line.strip()
			if line.startswith('LEXICON Root'):
				break
			if line.startswith('⟨'):
				style_tags.add(line)
	return style_tags


def lexc2fst(filename):

	style_tags = collect_style_tags(filename)

	time1 = datetime.now()

	print('—' * 64)
	print('Compiling generator FST:')

	print(f'Compiling LexC "{filename}"...')
	fst = hfst.compile_lexc_file(filename, verbosity=0, output=sys.stdout)
	fst.minimize()

	# Remove word style tags
	for tag in style_tags:
		fst.substitute(tag, hfst.EPSILON, input=True, output=True)

	fst.minimize()
	fst.convert(hfst.ImplementationType.HFST_OLW_TYPE)

	print('Done.')
	time2 = datetime.now()
	print('Time taken:', time2 - time1)

	return fst


def main():
	fst = lexc2fst('fi.lexc')
	output_stream = hfst.HfstOutputStream(filename=GENERATOR_FST_PATH, type=hfst.ImplementationType.HFST_OLW_TYPE)
	output_stream.write(fst)
	output_stream.close()


if __name__ == '__main__':
	main()
