import sublime
import sublime_plugin
import re



consonants=["ॿ","ॾ","ॼ","ॻ","क","ख","ग","घ","ङ","च","छ","ज","झ","ञ","ट","ठ","ड","ढ","ण","त","थ","द","ध","न","प","फ","ब","भ","म","य","र","ऱ","ल","ळ","व","श","ष","स","ह"]
vowels=["ॷ","ॶ","ॵ","ॴ","ॳ","ॲ","अ","आ","इ","ई","उ","ऊ","ऋ","ऍ","ऎ","ए","ऐ","ऑ","ऒ","ओ","औ","ॠ"]
matras=["ा","ि","ी","ु","ू","ृ","ॅ","ॆ","े","ै","ॉ","ॊ","ो","ौ","ऻ","ऺ","ॄ","ॆ","ॏ","ॗ","ॖ"]
vowelMod=["ँ","ं","ः"]
halant=["्"]
nukta=["़"]
Charset='[^'+''.join(consonants+vowels+matras+vowelMod+halant+nukta)+']'
C='['+''.join(consonants)+']'
N='['+''.join(nukta)+']'
H='['+''.join(halant)+']'
D='['+''.join(vowelMod)+']'
M='['+''.join(matras)+']'
V='['+''.join(vowels)+']'
# reg=r'^((((('+C+')('+N+')?('+H+'))?(('+C+')('+N+')?('+H+'))?(('+C+')('+N+')?('+H+')))?(('+C+')('+N+')?)('+M+')?('+D+')?|('+V+')('+D+')?))+((('+C+')('+N+')?('+H+'))?(('+C+')('+N+')?('+H+'))?(('+C+')('+N+')?('+H+')))?$'
reg = r'''
(?x)
(
    (
        (({C}{N}?{H})?({C}{N}?{H})?({C}{N}?{H}))?
        ({C}{N}?){M}?{D}?
    )
    |{V}{D}?
)+
(
    ({C}{N}?{H})?
    ({C}{N}?{H})?
    ({C}{N}?{H})
)?
$
'''.format(C=C, N=N, H=H, D=D, V=V, M=M)




class isbetter(sublime_plugin.EventListener):

	def dothings(self, view):
		content = view.substr(sublime.Region(0, view.size()))
		words = re.split("\n|।| |"+Charset,content)
		valid_words=[]
		valid_words = [ word for word in words if re.match(reg, word) and word not in valid_words ]
		view.erase_regions('invalid')
		for idx,i in enumerate(valid_words):
			valid_words[idx]=r''+valid_words[idx]+r''
		regexf=" |".join(valid_words)
		regions = view.find_all(regexf)
		if regions:
			view.add_regions('valid', regions, 'valid')


	def on_load_async(self, view):
		try:
			self.dothings(view)
		except:
			print("broke")
	def on_post_save_async(self, view):
		try:
			self.dothings(view)
		except:
			print("broke")






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
