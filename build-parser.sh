#!/bin/sh

# Generate required files
python3 -m scripts.lexc.generate-numerals
python3 -m scripts.lexc.generate-ordinals
python3 -m scripts.lexc.collect-prefixes
python3 -m scripts.inflection.generate-adverbs

# Generate Lexc file
python3 -m scripts.lexc.generate-main-lexc

# Compile LexC file
python3 -m scripts.compile.compile-parser
python3 -m scripts.compile.compile-generator
