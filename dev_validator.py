import sublime
import sublime_plugin
import re

class isbetter(sublime_plugin.EventListener):

	invalid_words_set = u'|'.join([
		'\u200b',  
		'\u200c',  
		'\u200d',   
		'\u2060',   
		'\u2061', 
		'\u2062', 
		'\u2063',
		'\u2064',
		'\u2065',  
		'\u2066',  
		'\u2067',  
		'\u2068', 
		'\u2069',
		'\u206a',   
		'\u206b',
		'\u206c',
		'\u206d', 
		'\u206e',  
		'\u206f',  
		'\ufeff',   
	])






	def dothings(self, view):

		consonants=["ॿ","ॾ","ॼ","ॻ","क","ख","ग","घ","ङ","च","छ","ज","झ","ञ","ट","ठ","ड","ढ","ण","त","थ","द","ध","न","प","फ","ब","भ","म","य","र","ऱ","ल","ळ","व","श","ष","स","ह"]
		vowels=["ॷ","ॶ","ॵ","ॴ","ॳ","ॲ","अ","आ","इ","ई","उ","ऊ","ऋ","ऍ","ऎ","ए","ऐ","ऑ","ऒ","ओ","औ","ॠ"]
		matras=["ा","ि","ी","ु","ू","ृ","ॅ","ॆ","े","ै","ॉ","ॊ","ो","ौ","ऻ","ऺ","ॄ","ॆ","ॏ","ॗ","ॖ"]
		vowelMod=["ँ","ं","ः"]
		halant=["्"]
		nukta=["़"]

		C='['+''.join(consonants)+']'
		N='['+''.join(nukta)+']'
		H='['+''.join(halant)+']'
		D='['+''.join(vowelMod)+']'
		M='['+''.join(matras)+']'
		V='['+''.join(vowels)+']'
		reg=r'((((('+C+')('+N+')?('+H+'))?(('+C+')('+N+')?('+H+'))?(('+C+')('+N+')?('+H+')))?(('+C+')('+N+')?)('+M+')?('+D+')?|('+V+')('+D+')?))+((('+C+')('+N+')?('+H+'))?(('+C+')('+N+')?('+H+'))?(('+C+')('+N+')?('+H+')))?$'
		content = view.substr(sublime.Region(0, view.size()))
		# input_text=ip_file.read()
		words = re.split("\n| ",content)
		for idx,word in enumerate(words):
			if len(word)==0:
				del words[idx]
		# print(words)
		# a=words
		# for word in words:
			# a.append(word.split(",")[0])
		# words = a
		valid_words=[]
		# i_n=0
		print(words)
		for word in words:
			if(re.match(reg,word)):
				print(word)
				valid_words.append(word)

		# self.invalid_words_set=u'|'.join(temp)
		view.erase_regions('invalid')
		for idx,i in enumerate(valid_words):
			valid_words[idx]=r''+valid_words[idx]+r''
		# print("$|".join(valid_words))
		regexf="|".join(valid_words)
		regexf+=""
		print(regexf)
		regions = view.find_all(regexf)
		if regions:
			view.add_regions('zero-width', regions, 'invalid')


	def on_load_async(self, view):
		try:
			self.dothings(view)
		except e:
			print(e)
	def on_post_save_async(self, view):

		self.dothings(view)


# print(re.match(reg,'ॿिघ'))



# 	Rules
# 1 Word ::= {Syllable} [Cons-Syllable]
# 2 Syllable ::= Cons-Vowel-Syllable | Vowel-Syllable
# 3 Vowel-Syllable ::= V [D]
# 4 Cons-Vowel-Syllable ::= [Cons-Syllable] Full-Cons [M] [D]
# 5 Cons-Syllable ::= [Pure-Cons] [Pure-Cons] Pure-Cons
# 6 Pure-Cons ::= Full-Cons H
# 7 Full-Cons ::= C [N]
# 
# 
# 
# Full-Cons=(C)(N)?
# Pure-Cons=(C)(N)?(H)
# Cons-Syllable =((C)(N)?(H))?((C)(N)?(H))?((C)(N)?(H))
# Cons-Vowel-Syllable=(((C)(N)?(H))?((C)(N)?(H))?((C)(N)?(H)))?((C)(N)?)(M)?(D)?
# Vowel-Syllable=(V)(D)?
# Syllable=[(((C)(N)?(H))?((C)(N)?(H))?((C)(N)?(H)))?((C)(N)?)(M)?(D)?|(V)(D)?]
# Word=([(((C)(N)?(H))?((C)(N)?(H))?((C)(N)?(H)))?((C)(N)?)(M)?(D)?|(V)(D)?])+(((C)(N)?(H))?((C)(N)?(H))?((C)(N)?(H)))?
