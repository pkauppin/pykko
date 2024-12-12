- Morphological tags are displayed in the same order as the corresponding morphemes in a given word form.
- Features that are redundant or occur in complementary distribution have been eliminated:
  - For simple verb forms, only indicative mood has past and present tenses, while other moods only have present tense. Therefore, for indicative mood, only tense is indicated while for other moods, only the mood is explicitly indicated
  - Active voice and indicative mood are assumed for verbs unless stated otherwise.
- Pronouns etc. that are only used adverbially in different cases are not also analyzed as pronouns – the forms are treated as adverbs only (example?)
- For the sake of reducing clutter, the accusative case is only marked separately for personal pronouns and the pronoun _kuka_.

**PARTS OF SPEECH**
- `verb` verb
- `noun` common noun
- `noun-pl` common noun (plurale tantum)
- `numeral` cardinal number
- `ordinal` ordinal adjective/number
- `adjective` adjective
- `adverb` adverb
- `adposition` adposition
- `pronoun` pronoun (singular)
- `pronoun-pl` pronoun (plural)
- `interjection` interjection
- `proper` proper noun (singular)
- `proper-pl` proper noun (plural)
- `conjunction` conjunction

Compound tags:
- `conjunction+verb` e.g. _ettei_
- `adverb+verb` e.g. _miksei_

**PERSON & VOICE**
- `+1sg` active first person singular (_menen_)
- `+2sg` active second person singular (_menet_)
- `+3sg` active third person singular (_menee_)
- `+1pl` active first person plural (_menemme_)
- `+2pl` active second person plural (_menette_)
- `+3pl` active third person plural (_menevät_)
- `+pass` passive voice (_mennään_)

**TENSE & MOOD**
- `+pres` present indicative (_menee_)
- `+past` past indicative (_meni_)
- `+cond` present conditional (_menisi_)
- `+imper` present imperative (_mene_, _menköön_)
- `+poten` present potential (_mennee_)

**PARTICIPLES & INFINITIVES**
- `+part_pres` present active participle (_menevä_)
- `+part_past` past active participle (_mennyt_)
- `+pass+part_pres` present passive participle (_mentävä_)
- `+pass+part_past` past passive participle (_menty_)
- `+inf1` 1st infinitive (_mennä_, _mennä-_) – general base form of verbs
- `+inf2` 2nd infinitive (_menne-_)
- `+inf3` 3rd infinitive (_meneminen_)
- `+inf4` 4th infinitive (_meneminen_)
- `+inf5` 5th infinitive (_menemäisillään_)
- `part_ma` agent participle (_menemä_)
- `part_maton` negative participle (_menemätätön_)

**NUMBER**
- `+sg` singular
- `+pl` plural

**CASE**
- `+nom` nominative case (_talo_, _kuka_)
- `+gen` genitive case (_talon_, _kenen_)
- `+par` partitive case  (_taloa_, _ketä_)
- `+ill` illative case (_taloon_, _keneen_)
- `+ine` inessive case (_talossa_, _kenessä_)
- `+ela` elative case (_talosta_, _kenestä_)
- `+all` allative case (_talolle_, _kenelle_)
- `+ade` adessive case (_talolla_, _kenellä_)
- `+abl` ablative case (_talolta_, _keneltä_)
- `+ess` essive case (_talona_, _kenenä_)
- `+tra` translative case  (_taloksi_, _keneksi_)
- `+abe` abessive case (_talotta_, _kenettä_)
- `+ins` instructive case (_taloin_ — plural only)
- `+com` comitative case (_taloine-_ — plural only)
- `+acc` accusative case  (_kenet_ — certain pronouns only)

**COMPARISON**
- `+comparative` comparative degree (_suurempi_, _kauniimmin_)
- `+superlative` superlative degree (_suurin_, _kauneimmin_)

**POSSESSIVE SUFFIXES**
- `+poss1sg` first person singular (_taloni_)
- `+poss2sg` second person singular (_talosi_)
- `+poss1pl` first person plural (_talomme_)
- `+poss2pl` second person plural (_talonne_)
- `+poss3` third person singular and plural (_talonsa_)

**STYLE TAGS**
- `coll` colloquial
- `arch` dated/archaic
- `rare` rare
- `dial` dialectal
- `poet` poetic/literary
- `nstd` nonstandard
- `slang` slang
- `foreign` foreign word

> **NB!** The parser uses the character `’` <small>(U+2019 RIGHT SINGLE QUOTATION MARK)</small> as its default apostrophe. All apostrophes in the input are converted into this character in the lemma forms.
