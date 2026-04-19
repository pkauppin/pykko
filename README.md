# Finnish Morphological Parser (WIP)

Pykko is an experimental finite-state morphological parser for Finnish. Personal recreational project.

Check out the nifty [PyPykko](https://pypi.org/project/pypykko/) wrapper (with extra goodies) by [@thfr](https://pypi.org/user/thfr/) on PyPi.

## Requirements
- 3.12 >= Python >= 3.8
- C++ compiler
- [HFST for Python](https://pypi.org/project/hfst/) >= 3.15

## Compiling

Generate the LexC file and compile into a parser and a generator:

```
$ ./build-parser.sh
```

## Parsing text on command line

The transducer accepts tokenized input (one token per line).
You can tokenize the input and normalize the transducer output as follows:

```
$ echo "Tämä on esimerkki." | python3 -m tools.tokenizer | python3 -m tools.parse | python3 -m tools.normalize
```

or simply

```
$ echo "Tämä on esimerkki." | ./parse-text.sh
```

## Examples

(Yours truly highly recommends using PyPykko for better user experience.)

### Analyzing individual wordforms

```py
>>> from pykko.tools.utils import analyze

>>> for _ in analyze('kallistakaan'): _
...
('kallistakaan', 'Lexicon', 'kallis', 'adjective', '', '', '+sg+par+kaan', 0.0)
('kallistakaan', 'Lexicon', 'kallistaa', 'verb', '', '', '+imper+2sg+conneg+kaan', 0.0)
('kallistakaan', 'Lexicon', 'kallistaa', 'verb', '', '', '+pres+conneg+kaan', 0.0)

>>> for _ in analyze('viinissä'): _
...
('viinissä', 'Lexicon', 'viini', 'noun', '1', '', '+sg+ine', 0.0)
('viinissä', 'Lexicon', 'viini', 'noun', '2', '', '+pl+ine', 0.0)

>>> for _ in analyze('viinessä'): _
...
('viinessä', 'Lexicon', 'viini', 'noun', '2', '', '+sg+ine', 0.0)

>>> for _ in analyze('ABC-possukaloja'): _
...
('ABC-possukaloja', 'Lexicon|Hyp+Pfx', 'ABC-possu|kala', 'noun', '', '', '+pl+par', 4.0)

>>> for _ in analyze('xxxisaatioista'): _
...
'xxxisaatioista', 'Guesser|Any', 'xxxisaatio', 'noun', '', '', '+pl+ela', 10.0)
```

### Generating individual wordforms

```py
>>> from pykko.tools.generate import generate_wordform

>>> generate_wordform('laatikko', pos='noun', morphtags='+pl+gen')
{'laatikoiden', 'laatikoitten', 'laatikkojen'}

>>> generate_wordform('tavata', pos='verb', morphtags='+pres+1sg', homonym="1")
{'tapaan'}

>>> generate_wordform('tavata', pos='verb', morphtags='+pres+1sg', homonym="2")
{'tavaan'}

>>> generate_wordform('tavata', pos='verb', morphtags='+pres+1sg')
{'tapaan', 'tavaan'}
```

### Generating all basic wordforms

```py
>>> from pykko.tools.generate import generate_forms
>>> for _ in generate_forms('tulla'): _
... 
'tulkoot'
'tultakoon'
'tullevat'
'tulkaamme'
'tulisimme'
'tullessa'
'tulit'
'tulette'
'tulee'
'tulemasta'
…

>>> for _ in generate_forms('tavata', homonym='1'): _
... 
'tapaamassa'
'tapasin'
'tapaavat'
'tapasivat'
'tapasi'
'tavanne'
'tapaisivat'
'tavattu'
'tapasimme'
'tapaatte'
…
```

### Generating inflectional paradigms

```py
>>> from pykko.tools.generate import generate_inflection_paradigm
>>> from pprint import pprint
>>> pprint(generate_inflection_paradigm('saapua', pos='verb'))
{'+cond+1pl': ['saapuisimme'],
 '+cond+1sg': ['saapuisin'],
 '+cond+2pl': ['saapuisitte'],
 '+cond+2sg': ['saapuisit'],
 '+cond+3pl': ['saapuisivat'],
 '+cond+3sg': ['saapuisi'],
 '+cond+conneg': ['saapuisi'],
 '+imper+1pl': ['saapukaamme'],
 '+imper+2pl': ['saapukaa'],
 '+imper+2sg': ['saavu'],
 '+imper+2sg+conneg': ['saavu'],
 '+imper+3pl': ['saapukoot'],
 '+imper+3sg': ['saapukoon'],
 '+imper+3sg+conneg': ['saapuko'],
 '+imper+pl+conneg': ['saapuko'],
 '+inf1': ['saapua'],
…
```

## Sources

The core lexicon on nouns, adjectives, verbs etc. together with the inflectional information is primarily based on the 2022
version of [Nykysuomen sanalista](https://www.kotus.fi/aineistot/sana-aineistot/nykysuomen_sanalista)
by the Institute for the Languages of Finland (CC BY 4.0).

## License & Copyright

This project is licensed under the MIT License.

Copyright © 2026 Pekka Kauppinen.
