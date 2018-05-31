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
		# content = view.substr(sublime.Region(0, view.size()))
		# view.erase_regions('zero-width')
		# view.run_command("select_all")
		# print(content)
		# # view.run_command("insert", {"characters": content})
		# regions = view.find_all(self.invalid_words_set)

		# print(len(regions))
		# # print(type(regions))
		# print(regions)
		# if regions:
		#     view.add_regions('zero-width', regions, 'invalid')
		consonants=["ॿ","ॾ","ॼ","ॻ","क","ख","ग","घ","ङ","च","छ","ज","झ","ञ","ट","ठ","ड","ढ","ण","त","थ","द","ध","न","प","फ","ब","भ","म","य","र","ऱ","ल","ळ","व","श","ष","स","ह"]
		vowels=["ॷ","ॶ","ॵ","ॴ","ॳ","ॲ","अ","आ","इ","ई","उ","ऊ","ऋ","ऍ","ऎ","ए","ऐ","ऑ","ऒ","ओ","औ","ॠ"]
		matras=["ा","ि","ी","ु","ू","ृ","ॅ","ॆ","े","ै","ॉ","ॊ","ो","ौ","ऻ","ऺ","ॄ","ॆ","ॏ","ॗ","ॖ"]
		vowelMod=["ँ","ं","ः"]
		halant=["्"]
		nukta=["़"]

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
		for word in words:
			# i_n+=1
			chars = [i for i in word]
			new_char=[]
			i=0
			# rule 7 Full-Cons ::= C [N]
			for char in chars:
				if not i<len(chars):
					break
				if chars[i] in consonants:
					new_char.append("Full-Cons")
					if (i<len(chars)-1) and (chars[i+1] in nukta):
						i+=1
				else:
					new_char.append(chars[i])
				i+=1
			# print(new_char)
			chars=new_char
			new_char=[]
			i=0
			# rule 6 Pure-Cons ::= Full-Cons H
			for char in chars:
				if not i<len(chars):
					break
				if (i<len(chars)-1) and (chars[i]=="Full-Cons") and (chars[i+1] in halant):
					new_char.append("Pure-Cons")
					i+=2
				else:
					new_char.append(chars[i])
					i+=1
			# print(new_char)
			chars=new_char
			new_char=[]
			i=0
			# rule 5 Cons-Syllable ::= [Pure-Cons] [Pure-Cons] Pure-Cons
			for char in chars:
				if not i<len(chars):
					break
				if chars[i]=="Pure-Cons":
					i+=1
					if (i<len(chars)) and chars[i]=="Pure-Cons":
						i+=1
						if (i<len(chars)) and chars[i]=="Pure-Cons":
							i+=1
					new_char.append("Cons-Syllable")
				else:
					new_char.append(chars[i])
					i+=1
			# print(new_char)
			chars=new_char
			new_char=[]
			i=0
			# rule 4 Cons-Vowel-Syllable ::= [Cons-Syllable] Full-Cons [M] [D]
			for char in chars:

				if not i<len(chars):
					break
				if (i<len(chars)-3) and (chars[i] == "Cons-Syllable") and (chars[i+1] == "Full-Cons") and (chars[i+2] in matras) and (chars[i+3] in vowelMod):
					i+=4
					new_char.append("Cons-Vowel-Syllable")

				elif (i<len(chars)-2) and (chars[i] == "Cons-Syllable") and (chars[i+1] == "Full-Cons") and (chars[i+2] in matras):
					i+=3
					new_char.append("Cons-Vowel-Syllable")

				elif (i<len(chars)-2) and (chars[i] == "Cons-Syllable") and (chars[i+1] == "Full-Cons") and (chars[i+2] in vowelMod):
					i+=3
					new_char.append("Cons-Vowel-Syllable")

				elif (i<len(chars)-1) and (chars[i] == "Cons-Syllable") and (chars[i+1] == "Full-Cons"):
					i+=2
					new_char.append("Cons-Vowel-Syllable")

				elif (i<len(chars)-2) and (chars[i] == "Full-Cons") and (chars[i+1] in matras) and (chars[i+2] in vowelMod):
					i+=3
					new_char.append("Cons-Vowel-Syllable")

				elif (i<len(chars)-1) and (chars[i] == "Full-Cons") and (chars[i+1] in matras):
					i+=2
					new_char.append("Cons-Vowel-Syllable")

				elif (i<len(chars)-1) and (chars[i] == "Full-Cons") and (chars[i+1] in vowelMod):
					i+=2
					new_char.append("Cons-Vowel-Syllable")

				elif (chars[i] == "Full-Cons"):
					i+=1
					new_char.append("Cons-Vowel-Syllable")

				else:
					new_char.append(chars[i])
					i+=1
			# print(new_char)
			chars=new_char
			new_char=[]
			i=0
			# rule 3 Vowel-Syllable ::= V [D]
			for char in chars:
				if not i<len(chars):
					break
				if chars[i] in vowels:
					i+=1
					if (i<len(chars)) and (chars[i] in vowelMod):
						i+=1
					new_char.append("Vowel-Syllable")
				else:
					new_char.append(chars[i])
					i+=1
			# print(new_char)
			chars=new_char
			new_char=[]
			i=0
			# rule 2 Syllable ::= Cons-Vowel-Syllable | Vowel-Syllable
			for char in chars:
				if not i<len(chars):
					break
				if (chars[i] == "Cons-Vowel-Syllable") or (chars[i] == "Vowel-Syllable"):
					new_char.append("Syllable")
				else:
					new_char.append(chars[i])
				i+=1
			# print(new_char)
			chars=new_char
			new_char=[]
			ans=True
			i=0
			# rule 1 Word ::= {Syllable} [Cons-Syllable]
			if chars[-1] == "Cons-Syllable":
				del(chars[-1])
			if len(chars)==0:
				ans=False
			for i in chars:
				if not i=="Syllable":
					ans=False
					break

			valid_words.append(ans)
			# print(i_n)
			# print(new_char)
		# print(valid_words)
		temp = []
		for x,y in zip(words,valid_words):
			if(y==False):
				temp.append(str(x) )
		print(temp)
		self.invalid_words_set=u'|'.join(temp)
		view.erase_regions('invalid')
		regions = view.find_all(self.invalid_words_set)
		if regions:
			view.add_regions('zero-width', regions, 'invalid')
		# with open("validated.txt","w") as f:
		# 	f.write("\n".join(temp))

		"""
		Rules
		1 Word ::= {Syllable} [Cons-Syllable]
		2 Syllable ::= Cons-Vowel-Syllable | Vowel-Syllable
		3 Vowel-Syllable ::= V [D]
		4 Cons-Vowel-Syllable ::= [Cons-Syllable] Full-Cons [M] [D]
		5 Cons-Syllable ::= [Pure-Cons] [Pure-Cons] Pure-Cons
		6 Pure-Cons ::= Full-Cons H
		7 Full-Cons ::= C [N]

		"""


	def on_load_async(self, view):
		try:
			self.dothings(view)
		except:
			print('broke')
	def on_post_save_async(self, view):
		try:
			self.dothings(view)
		except:
			print('broke')