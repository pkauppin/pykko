# Finnish Morphological Parser (WIP)

Pykko is an experimental finite-state morphological parser for Finnish. Personal recreational project.

## Requirements
- Python3 (3.7 or greater)
- C++ compiler
- [HFST for Python](https://pypi.org/project/hfst/) (3.15 or greater)

## Compiling

Generate the LexC file and compile it into an FST:

```
$ ./build-parser.sh
```

## Parsing

**Tokenized text**:

The transducer accepts tokenized input (one token per line):

```
$ echo "Tämä
on
esimerkkilause
." | python3 -m tools.parse | python3 -m tools.normalize
```

**Untokenized text**:

You can also use the tentative tokenizer to tokenize the input text:

```
$ echo "Tämä on esimerkki." | python3 -m tools.tokenizer | python3 -m tools.parse | python3 -m tools.normalize
```

or

```
$ echo "Tämä on esimerkki." | ./parse-text.sh
```

## Sources

The core lexicon on nouns, adjectives, verbs etc. together with the inflectional information is primarily based on the 2022
version of [Nykysuomen sanalista](https://www.kotus.fi/aineistot/sana-aineistot/nykysuomen_sanalista)
by the Institute for the Languages of Finland (CC BY 4.0).

## License & Copyright

This project is licensed under the MIT License.

Copyright © 2024 Pekka Kauppinen.
