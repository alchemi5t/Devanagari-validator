import sublime
import sublime_plugin
import re

consonants=["ॿ","ॾ","ॼ","ॻ","क","ख","ग","घ","ङ","च","छ","ज","झ","ञ","ट","ठ","ड","ढ","ण","त","थ","द","ध","न","प","फ","ब","भ","म","य","र","ऱ","ल","ळ","व","श","ष","स","ह"]
vowels=["ॷ","ॶ","ॵ","ॴ","ॳ","ॲ","अ","आ","इ","ई","उ","ऊ","ऋ","ऍ","ऎ","ए","ऐ","ऑ","ऒ","ओ","औ","ॠ"]
matras=["ा","ि","ी","ु","ू","ृ","ॅ","ॆ","े","ै","ॉ","ॊ","ो","ौ","ऻ","ऺ","ॄ","ॆ","ॏ","ॗ","ॖ"]
vowelMod=["ँ","ं","ः"]
halant=["्"]
nukta=["़"]

def character_class(characters):
    return '[' + ''.join(characters) + ']'

Charset=character_class(consonants+vowels+matras+vowelMod+halant+nukta)
C=character_class(consonants)
N=character_class(nukta)
H=character_class(halant)
D=character_class(vowelMod)
M=character_class(matras)
V=character_class(vowels)

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

class DetectInvalidDevangariListener(sublime_plugin.EventListener):
    settings = sublime.load_settings("Detect Invalid Devangari.sublime-settings")

    def on_load_async(self, view):
        # print(self.settings.get("run_on_load", False))
        if self.settings.get("run_on_load", False):
            view.run_command('detect_invalid_devangari')

    def on_post_save_async(self, view):
        # print(self.settings.get("run_on_load", False))
        if self.settings.get("run_on_save", False):
            view.run_command('detect_invalid_devangari')

class DetectInvalidDevangariCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        valid_regions = [
            region
            for region in self.view.find_all(r'{Charset}+'.format(Charset=Charset))
            if re.match(reg, self.view.substr(region))
        ]
        if valid_regions:
            self.view.add_regions('valid', valid_regions, 'valid')
