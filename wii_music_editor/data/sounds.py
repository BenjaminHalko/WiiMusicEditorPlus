class SoundClass:
	def __init__(self,Name,*args):
		self.Name = Name
		self.typeNames = []
		self.typeValues = []
		for arg in args:
			if(type(arg) == int):
				self.typeNames.append(str(arg))
				self.typeValues.append(arg)
			elif(type(arg[1]) == str):
				self.typeNames.append(arg[1])
				self.typeValues.append(arg[0])
			else:
				for i in range(arg[0],arg[1]):
					if(len(arg) == 3): self.typeNames.append(str(i)+" ("+arg[2]+")")
					else: self.typeNames.append(str(i))
					self.typeValues.append(i)



def get_sounds():
    [
        SoundClass(_translate("Editor", "Basic Drum"), [297, 300]),
        SoundClass(_translate("Editor", "Rock Drums"), [302, 306]),
        SoundClass(_translate("Editor", "Jazz Drums"), [307, 311]),
        SoundClass(_translate("Editor", "Latin Drums"), [312, 315]),
        SoundClass(_translate("Editor", "Ballad Drums"), [316, 319]),
        SoundClass(_translate("Editor", "Cymbal for Basic, Jazz, Latin, Reggae, and Ballad Drums"), 301),
        SoundClass(_translate("Editor", "Bass for Basic, Latin, and Ballad Drums"), 296),
        SoundClass(_translate("Editor", "Congas"), [320, 324]),
        SoundClass(_translate("Editor", "Maracas"), [325, 330], [430, _translate("Editor", "Female Variant")]),
        SoundClass(_translate("Editor", "Tambourine"), [331, 335]),
        SoundClass(_translate("Editor", "Cuica"), [336, 340]),
        SoundClass(_translate("Editor", "Cowbell"), [341, 343]),
        SoundClass(_translate("Editor", "Hand Clap"), [344, 346]),
        SoundClass(_translate("Editor", "Bells"), [347, 349]),
        SoundClass(_translate("Editor", "Castanets"), [350, 353], [431, _translate("Editor", "Male Variant")]),
        SoundClass(_translate("Editor", "Guiro"), [354, 358]),
        SoundClass(_translate("Editor", "Timbales"), [359, 362]),
        SoundClass(_translate("Editor", "Djembe"), [363, 367]),
        SoundClass(_translate("Editor", "Taiko Drums"), [368, 370], [432, _translate("Editor", "Female Varient")]),
        SoundClass(_translate("Editor", "Cheerleader"), [371, 376, _translate("Editor", "Female")],
                   [424, 429, _translate("Editor", "Male")]),
        SoundClass(_translate("Editor", "Snare Drum"), [377, 380]),
        SoundClass(_translate("Editor", "Bass Drum"), [381, 383]),
        SoundClass(_translate("Editor", "Galactic Drums"), [384, 388]),
        SoundClass(_translate("Editor", "Galactic Congas"), [389, 393]),
        SoundClass(_translate("Editor", "DJ Turntables"), [280, 295]),
        SoundClass(_translate("Editor", "Black Belt"), [394, 399, _translate("Editor", "Male")],
                   [418, 423, _translate("Editor", "Female")]),
        SoundClass(_translate("Editor", "Reggae Drums"), [400, 404]),
        SoundClass(_translate("Editor", "Whistle"), [405, 408]),
        SoundClass(_translate("Editor", "Beat Boxer"), [409, 414]),
        SoundClass(_translate("Editor", "Drum Mode"), [433, 444])]