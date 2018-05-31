# devanagari_invalid_grammar_detect
Sublime plugin to detect invalid devanagari word constructs.

It also highlights words with zero width characters.

Character set :-

		consonants=["ॿ","ॾ","ॼ","ॻ","क","ख","ग","घ","ङ","च","छ","ज","झ","ञ","ट","ठ","ड","ढ","ण","त","थ","द","ध","न","प","फ","ब","भ","म","य","र","ऱ","ल","ळ","व","श","ष","स","ह"]
		vowels=["ॷ","ॶ","ॵ","ॴ","ॳ","ॲ","अ","आ","इ","ई","उ","ऊ","ऋ","ऍ","ऎ","ए","ऐ","ऑ","ऒ","ओ","औ","ॠ"]
		matras=["ा","ि","ी","ु","ू","ृ","ॅ","ॆ","े","ै","ॉ","ॊ","ो","ौ","ऻ","ऺ","ॄ","ॆ","ॏ","ॗ","ॖ"]
		vowelMod=["ँ","ं","ः"]
		halant=["्"]
		nukta=["़"]




The rules are:-

		Rules
		1 Word ::= {Syllable} [Cons-Syllable]
		2 Syllable ::= Cons-Vowel-Syllable | Vowel-Syllable
		3 Vowel-Syllable ::= V [D]
		4 Cons-Vowel-Syllable ::= [Cons-Syllable] Full-Cons [M] [D]
		5 Cons-Syllable ::= [Pure-Cons] [Pure-Cons] Pure-Cons
		6 Pure-Cons ::= Full-Cons H
		7 Full-Cons ::= C [N]
		
	


Usage:

Highlights the incorrect words post save or on load
