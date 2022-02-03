#Imports
import os
import sys
import platform
import subprocess
import pathlib
import tempfile
import pretty_midi
from shutil import copyfile, rmtree
from math import floor, ceil
import mido
from configparser import ConfigParser
import stat as stats
import wave
import audioop

from PyQt5.QtCore import QCoreApplication

#Classes
class SongClass:
	def __init__(self,SongType,Name,MemOrder,DefaultStyle="nope",MemOffset = -1):
		self.SongType = SongType
		self.Name = Name
		self.MemOrder = MemOrder
		self.DefaultStyle = DefaultStyle
		self.MemOffset = MemOffset
		if(self.MemOffset == -1): self.MemOffset = 0x025a0440+0xBC*self.MemOrder
			
class StyleClass:
	def __init__(self,StyleType,Name,MemOffset,StyleId,DefaultStyle):
		self.StyleType = StyleType
		self.Name = Name
		self.MemOffset = MemOffset
		self.StyleId = StyleId
		self.DefaultStyle = DefaultStyle

class InstrumentClass:
	def __init__(self,Name,Number,InMenu,NumberOfSounds=[]):
		self.Name = Name
		self.Number = Number
		self.InMenu = InMenu
		self.NumberOfSounds = NumberOfSounds

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

class SongTypeValue:
	Regular = 0
	Menu = 1
	Maestro = 2
	Handbell = 3

class StyleTypeValue:
	Global = 0
	SongSpecific = 1
	QuickJam = 2
	Menu = 3

class LoadedFile:
	def __init__(self,path,type):
		self.path = path
		self.type = type

def RetranslateSongNames():
	_translate = QCoreApplication.translate
	global Songs
	global Styles
	global Instruments
	global extraSounds

	Songs = [
	SongClass(SongTypeValue.Regular,_translate("Editor",'A Little Night Music'),6,"21"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'American Patrol'),11,"03"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Animal Crossing'),48,"1B"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Animal Crossing -- K.K. Blues'),26,"23"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Bridal Chorus'),1,"08"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Carmen'),3,"0F"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Chariots of Fire'),35,"13"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Daydream Believer'),33,"00"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Do-Re-Mi'),9,"01"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Every Breath You Take'),34,"12"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'F-Zero -- Mute City Theme'),49,"01"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Frère Jacques'),22,"04"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'From Santurtzi to Bilbao'),27,"20"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'From the New World'),16,"02"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Happy Birthday to You'),8,"1E"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'I\'ll Be There'),40,"16"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'I\'ve Never Been to Me'),44,"18"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Jingle Bell Rock'),41,"00"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'La Bamba'),17,"0A"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'La Cucaracha'),29,"1F"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Little Hans'),25,"04"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Long, Long Ago'),19,"08"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Material Girl'),38,"15"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Minuet in G Major'),7,"1C"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'My Grandfather\'s Clock'),15,"05"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'O Christmas Tree'),24,"10"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Ode to Joy'),0,"02"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Oh, My Darling Clementine'),14,"0D"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Over the Waves'),30,"11"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Please Mr. Postman'),37,"09"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Sakura Sakura'),31,"06"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Scarborough Fair'),18,"0E"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'September'),36,"14"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Sukiyaki'),32,"0A"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Super Mario Bros.'),45,"2C"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Sur le pont d\'Avignon'),21,"09"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Swan Lake'),2,"07"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'The Blue Danube'),5,"22"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'The Entertainer'),10,"1D"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'The Flea Waltz'),23,"03"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'The Legend of Zelda'),46,"19"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'The Loco-Motion'),39,"05"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Troika'),28,"07"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Turkey in the Straw'),12,"06"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Twinkle, Twinkle, Little Star'),20,"0B"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Wake Me Up Before You Go-Go'),42,"17"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Wii Music'),4,"24"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Wii Sports'),47,"1A"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Woman'),43,"17"),
	SongClass(SongTypeValue.Regular,_translate("Editor",'Yankee Doodle'),13,"0C"),
	SongClass(SongTypeValue.Maestro,_translate("Editor",'Twinkle, Twinkle, Little Star (Mii Maestro)'),2,MemOffset=0x25a3e1c),
	SongClass(SongTypeValue.Maestro,_translate("Editor",'Carmen (Mii Maestro)'),0,MemOffset=0x25a3d80),
	SongClass(SongTypeValue.Maestro,_translate("Editor",'The Four Seasons -- Spring (Mii Maestro)'),4,MemOffset=0x25a3f54),
	SongClass(SongTypeValue.Maestro,_translate("Editor",'Ode to Joy (Mii Maestro)'),3,MemOffset=0x25a3ff0),
	SongClass(SongTypeValue.Maestro,_translate("Editor",'The Legend of Zelda (Mii Maestro)'),1,MemOffset=0x25a3eb8),
	SongClass(SongTypeValue.Handbell,_translate("Editor",'O Christmas Tree (Handbell Harmony)'),0,MemOffset=0x2566D5A),
	SongClass(SongTypeValue.Handbell,_translate("Editor",'Hum, Hum, Hum (Handbell Harmony)'),2,MemOffset=0x2566E0A),
	SongClass(SongTypeValue.Handbell,_translate("Editor",'My Grandfather\'s Clock (Handbell Harmony)'),3,MemOffset=0x2566E62),
	SongClass(SongTypeValue.Handbell,_translate("Editor",'Do-Re-Mi (Handbell Harmony)'),1,MemOffset=0x2566DB2),
	SongClass(SongTypeValue.Handbell,_translate("Editor",'Sukiyaki (Handbell Harmony)'),4,MemOffset=0x2566EBA),
	SongClass(SongTypeValue.Menu,_translate("Editor",'Menu Song'),-1,MemOffset=[0x259ACB0,0x259ACD4,0x259ACF8,0x259AD1C,0x259AD40])]

	noneInstrument = 67
	Styles = [
	StyleClass(StyleTypeValue.Global,_translate("Editor",'Jazz'),0x0659A65C,'00',[28,2,0,16,42,45]),
	StyleClass(StyleTypeValue.Global,_translate("Editor",'Rock'),0x0659A680,'01',[14,14,36,15,41,47]),
	StyleClass(StyleTypeValue.Global,_translate("Editor",'Latin'),0x0659A6A4,'02',[27,28,1,15,43,46]),
	StyleClass(StyleTypeValue.Global,_translate("Editor",'March'),0x0659A6C8,'03',[27,27,27,31,59,58]),
	StyleClass(StyleTypeValue.Global,_translate("Editor",'Electronic'),0x659A6EC,'04',[2,22,8,23,62,50]),
	StyleClass(StyleTypeValue.Global,_translate("Editor",'Pop'),0x659A710,'05',[0,2,13,15,40,47]),
	StyleClass(StyleTypeValue.Global,_translate("Editor",'Japanese'),0x659A734,'06',[29,noneInstrument,noneInstrument,20,56,51]),
	StyleClass(StyleTypeValue.Global,_translate("Editor",'Tango'),0x659A758,'07',[25,0,32,16,58,52]),
	StyleClass(StyleTypeValue.Global,_translate("Editor",'Classical'),0x659A77C,'08',[25,25,6,26,noneInstrument,noneInstrument]),
	StyleClass(StyleTypeValue.Global,_translate("Editor",'Hawaiian'),0x659A7A0,'09',[17,17,17,16,46,45]),
	StyleClass(StyleTypeValue.Global,_translate("Editor",'Reggae'),0x659A7C4,'0A',[3,3,0,15,64,noneInstrument]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'A Little Night Music'),0x659AB00,'21',[29,25,6,26,noneInstrument,noneInstrument]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Animal Crossing'),0x659AA28,'1B',[32,18,13,13,46,45]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Animal Crossing K.K. Blues'),0x659AB48,'23',[33,28,13,16,42,53]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Carmen'),0x659A878,'0F',[35,32,13,16,59,46]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Chariots of Fire'),0x659A908,'13',[0,13,6,7,58,46]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Every Breath You Take'),0x659A8E4,'12',[33,0,22,15,40,47]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'From Santurtzi to Bilbao'),0x659AADc,'20',[3,3,3,3,50,47]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Happy Birthday to You'),0x659AA94,'1E',[27,28,0,16,42,45]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'I\'ll Be There'),0x659A974,'16',[38,38,39,39,44,50]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'I\'ve Never Been to Me'),0x659A9Bc,'18',[0,0,13,15,40,46]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'La Cucaracha'),0x659AAB8,'1F',[29,1,13,15,48,54]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Material Girl'),0x659A950,'15',[36,14,22,23,60,47]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Minuet in G Major'),0x659AA4c,'1C',[29,30,0,6,noneInstrument,noneInstrument]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'O-Christmas Tree'),0x659A89c,'10',[5,5,5,5,51,noneInstrument]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Oh My Darling Clementine'),0x659A830,'0D',[36,36,9,36,58,52]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Over The Waves'),0x659A8C0,'11',[32,30,6,16,53,47]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Scarborough Fair'),0x659A854,'0E',[34,34,13,16,59,47]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'September'),0x659A92c,'14',[27,28,8,23,40,50]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Super Mario Bros'),0x659AC8c,'2C',[37,37,37,37,noneInstrument,noneInstrument]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'The Blue Danube'),0x659AB24,'22',[30,25,4,31,58,52]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'The Entertainer'),0x659AA70,'1D',[0,6,0,16,42,46]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'The Legend of Zelda'),0x659A9E0,'19',[27,25,21,31,58,59]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Twinkle Twinkle Little Star'),0x659A7E8,'0B',[0,1,13,16,51,52]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Wii Sports'),0x659AA04,'1A',[29,0,13,15,60,47]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Wii Music'),0x659AB6c,'24',[25,28,0,15,40,50]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Woman'),0x659A998,'17',[28,27,13,15,40,49]),
	StyleClass(StyleTypeValue.SongSpecific,_translate("Editor",'Yankee Doodle'),0x659A80C,'0C',[33,24,18,16,49,46]),
	StyleClass(StyleTypeValue.QuickJam,_translate("Editor",'A Capella'),0x659AC20,'29',[38,38,39,39,66,50]),
	StyleClass(StyleTypeValue.QuickJam,_translate("Editor",'Acoustic'),0x659AB90,'38',[25,25,13,13,52,50]), #
	StyleClass(StyleTypeValue.QuickJam,_translate("Editor",'African Electronic'),0x659AB93,'3C',[25,25,13,13,52,50]), #
	StyleClass(StyleTypeValue.QuickJam,_translate("Editor",'Animals!'),0x659AC68,'2B',[11,11,10,31,59,49]),
	StyleClass(StyleTypeValue.QuickJam,_translate("Editor",'Calypso'),0x659AC44,'2A',[3,3,3,3,noneInstrument,noneInstrument]),
	StyleClass(StyleTypeValue.QuickJam,_translate("Editor",'Exotic'),0x659ABFC,'28',[19,19,4,19,55,noneInstrument]),
	StyleClass(StyleTypeValue.QuickJam,_translate("Editor",'Flamenco'),0x659AB90,'25',[25,25,13,13,52,50]), #
	StyleClass(StyleTypeValue.QuickJam,_translate("Editor",'Galactic'),0x659ADD0,'35',[25,25,13,13,52,50]), #
	StyleClass(StyleTypeValue.QuickJam,_translate("Editor",'Handbell'),0x659AB93,'43',[25,25,13,13,52,50]), #
	StyleClass(StyleTypeValue.QuickJam,_translate("Editor",'Karate'),0x659ABB4,'26',[14,14,14,15,41,63]),
	StyleClass(StyleTypeValue.QuickJam,_translate("Editor",'Orchestral'),0x659AD64,'32',[29,27,25,7,58,noneInstrument]),
	StyleClass(StyleTypeValue.QuickJam,_translate("Editor",'Parade'),0x659ABD8,'27',[27,30,27,31,65,57]),
	StyleClass(StyleTypeValue.QuickJam,_translate("Editor",'Rap'),0x659ADF4,'36',[12,noneInstrument,8,23,62,61]),
	StyleClass(StyleTypeValue.QuickJam,_translate("Editor",'Samba'),0x659AE18,'37',[29,1,13,15,65,48]),
	StyleClass(StyleTypeValue.Menu,_translate("Editor",'Menu Style Main'),0x659ACB0,'2D',[25,28,0,15,40,40]),
	StyleClass(StyleTypeValue.Menu,_translate("Editor",'Menu Style Electronic'),0x659ACD4,'2E',[2,22,0,23,62,40]),
	StyleClass(StyleTypeValue.Menu,_translate("Editor",'Menu Style Japanese'),0x659ACF8,'2F',[29,20,0,20,56,40]),
	StyleClass(StyleTypeValue.Menu,_translate("Editor",'Menu Style March'),0x659AD1C,'30',[30,27,0,31,58,40]),
	StyleClass(StyleTypeValue.Menu,_translate("Editor",'Menu Style A Capella'),0x659AD40,'31',[38,39,0,39,66,40])]

	Instruments = [
	InstrumentClass(_translate("Editor",'Piano'),0,True,["C2","G2","D3","A3","E4","B4","F#5","D6","F6"]),
	InstrumentClass(_translate("Editor",'Marimba'),1,False,["G3","D4","A4","E5","B5","F#6"]),
	InstrumentClass(_translate("Editor",'Vibraphone'),2,False,["F#3","C#4","G#4","D#5","A#5","F6"]),
	InstrumentClass(_translate("Editor",'Steel Drum'),3,False,["F#2","A#3","F#4","G4","E4","??(26)","C4"]),
	InstrumentClass(_translate("Editor",'Dulcimer'),4,False,["F3","C#4","G4","C5","A6","D6"]),
	InstrumentClass(_translate("Editor",'Handbell'),5,False,["G4","G4 (Variation)","G4 (Variation 2)","C7"]),
	InstrumentClass(_translate("Editor",'Harpsichord'),6,False,["G2","C4","C5","C6"]),
	InstrumentClass(_translate("Editor",'Timpani'),7,False,["F3","F3 (Variation)","F3 (Variation 2)"]),
	InstrumentClass(_translate("Editor",'Galactic Piano'),8,False,["G2","D3","A3","E4","B4","F#5"]),
	InstrumentClass(_translate("Editor",'Toy Piano'),9,False,["B4","D6"]),
	InstrumentClass(_translate("Editor",'Dog'),10,False,["Howl","??(54)","??(55)","??(54)","D5","G5","C#6"]),
	InstrumentClass(_translate("Editor",'Cat'),11,False,["G3","C#4","G4","C#5","G5","C#6"]),
	InstrumentClass(_translate("Editor",'Rapper'),12,False,["??"]*62),
	InstrumentClass(_translate("Editor",'Guitar'),13,False,["G#2","E3","B3","F#4","D5","??(133)"]),
	InstrumentClass(_translate("Editor",'Electric Guitar'),14,False,["A2","D3","B3","G4","E5","A5"]),
	InstrumentClass(_translate("Editor",'Electric Bass'),15,True,["G1","D2","G2","C3","G#3"]),
	InstrumentClass(_translate("Editor",'Double Bass'),16,False,["F1","G#1","G#2","G#3"]),
	InstrumentClass(_translate("Editor",'Ukulele'),17,False,["B3","F#4","C#5","G#5"]),
	InstrumentClass(_translate("Editor",'Banjo'),18,False,["A#2","F3","C4","G4","D5","A5"]),
	InstrumentClass(_translate("Editor",'Sitar'),19,False,["C3","G3","C4","G4"]),
	InstrumentClass(_translate("Editor",'Shamisen'),20,True,["D3","A3","D4","A4"]),
	InstrumentClass(_translate("Editor",'Harp'),21,False,["C3","C4","E5","B5","G6"]),
	InstrumentClass(_translate("Editor",'Galactic Guitar'),22,False,["F2","C3","F3","C4","F4","C5","F5"]),
	InstrumentClass(_translate("Editor",'Galactic Bass'),23,True,["A1","C2","F2","A2","C3"]),
	InstrumentClass(_translate("Editor",'Jaw Harp'),24,False,["??(184)","??(185)","??(186)","??(187)"]),
	InstrumentClass(_translate("Editor",'Violin'),25,True,["C4","A4","E5","B5","F#6"]),
	InstrumentClass(_translate("Editor",'Cello'),26,False,["A2","D3","A3","E4","B4"]),
	InstrumentClass(_translate("Editor",'Trumpet'),27,True,["F#2","G#3","A3","D4","G4","C5","F5","Bb5","G6"]),
	InstrumentClass(_translate("Editor",'Saxophone'),28,True,["F2","B2","F3","E4","Bb4","E5","Bb5","E6"]),
	InstrumentClass(_translate("Editor",'Flute'),29,True,["D4","G4","C5","G5","D6","G6","D7"]),
	InstrumentClass(_translate("Editor",'Clairenet'),30,True,["Bb2","F3","C4","F4","C5","F5","C6"]),
	InstrumentClass(_translate("Editor",'Tuba'),31,False,["??(229)","Eb2","Bb2","A3"]),
	InstrumentClass(_translate("Editor",'Accordion'),32,False,["B2","C4"]),
	InstrumentClass(_translate("Editor",'Harmonica'),33,False,["B4","A3","E4","D5","B5","A6"]),
	InstrumentClass(_translate("Editor",'Bagpipe'),34,False,["C4","F#4","C5","F#5"]),
	InstrumentClass(_translate("Editor",'Recorder'),35,False,["G6"]),
	InstrumentClass(_translate("Editor",'Galactic horn'),36,False,["G2","C4","C5"]),
	InstrumentClass(_translate("Editor",'Nes'),37,False,["Mario Jump","C3","F3","Bb3","G4","C5","C6"]),
	InstrumentClass(_translate("Editor",'Singer'),38,True,["C4 (Wii)","G4 (Wii)","C5 (Wii)","G5 (Wii)","C4 (Do)","F#4 (Do)","D5 (Do)","F#5 (Do)","C4 (Ba)","G4 (Ba)","C5 (Ba)","G5 (Ba)"]),
	InstrumentClass(_translate("Editor",'Bass Singer'),39,True,["D3 (Wii)","G3 (Wii)","C4 (Wii)","G4 (Wii)","C3 (Do)","G3 (Do)","C4 (Do)","G4 (Do)","D3 (Ba)","A3 (Ba)","D4 (Ba)","G4 (Ba)"]),
	InstrumentClass(_translate("Editor",'Basic Drums'),40,True),
	InstrumentClass(_translate("Editor",'Rock Drums'),41,False),
	InstrumentClass(_translate("Editor",'Jazz Drums'),42,False),
	InstrumentClass(_translate("Editor",'Latin Drums'),43,False),
	InstrumentClass(_translate("Editor",'Ballad Drums'),44,False),
	InstrumentClass(_translate("Editor",'Congas'),45,False),
	InstrumentClass(_translate("Editor",'Maracas'),46,False),
	InstrumentClass(_translate("Editor",'Tambourine'),47,False),
	InstrumentClass(_translate("Editor",'Cuica'),48,False),
	InstrumentClass(_translate("Editor",'Cowbell'),49,False),
	InstrumentClass(_translate("Editor",'Clap'),50,False),
	InstrumentClass(_translate("Editor",'Bells'),51,False),
	InstrumentClass(_translate("Editor",'Castanets'),52,False),
	InstrumentClass(_translate("Editor",'Guiro'),53,False),
	InstrumentClass(_translate("Editor",'Timpales'),54,False),
	InstrumentClass(_translate("Editor",'Djembe'),55,False),
	InstrumentClass(_translate("Editor",'Taiko Drum'),56,True),
	InstrumentClass(_translate("Editor",'Cheerleader'),57,False),
	InstrumentClass(_translate("Editor",'Snare Drum'),58,True),
	InstrumentClass(_translate("Editor",'Bass Drum'),59,False),
	InstrumentClass(_translate("Editor",'Galactic Drums'),60,False),
	InstrumentClass(_translate("Editor",'Galactic Congas'),61,False),
	InstrumentClass(_translate("Editor",'DJ Turntables'),62,True),
	InstrumentClass(_translate("Editor",'Black Belt'),63,False),
	InstrumentClass(_translate("Editor",'Reggae Drums'),64,False),
	InstrumentClass(_translate("Editor",'Whistle'),65,False),
	InstrumentClass(_translate("Editor",'Beatbox'),66,True),
	InstrumentClass(_translate("Editor",'None'),-1,False)]

	extraSounds = [
	SoundClass(_translate("Editor","Basic Drum"),[297,300]),
	SoundClass(_translate("Editor","Rock Drums"),[302,306]),
	SoundClass(_translate("Editor","Jazz Drums"),[307,311]),
	SoundClass(_translate("Editor","Latin Drums"),[312,315]),
	SoundClass(_translate("Editor","Ballad Drums"),[316,319]),
	SoundClass(_translate("Editor","Cymbal for Basic, Jazz, Latin, Reggae, and Ballad Drums"),301),
	SoundClass(_translate("Editor","Bass for Basic, Latin, and Ballad Drums"),296),
	SoundClass(_translate("Editor","Congas"),[320,324]),
	SoundClass(_translate("Editor","Maracas"),[325,330],[430,_translate("Editor","Female Variant")]),
	SoundClass(_translate("Editor","Tambourine"),[331,335]),
	SoundClass(_translate("Editor","Cuica"),[336,340]),
	SoundClass(_translate("Editor","Cowbell"),[341,343]),
	SoundClass(_translate("Editor","Hand Clap"),[344,346]),
	SoundClass(_translate("Editor","Bells"),[347,349]),
	SoundClass(_translate("Editor","Castanets"),[350,353],[431,_translate("Editor","Male Variant")]),
	SoundClass(_translate("Editor","Guiro"),[354,358]),
	SoundClass(_translate("Editor","Timbales"),[359,362]),
	SoundClass(_translate("Editor","Djembe"),[363,367]),
	SoundClass(_translate("Editor","Taiko Drums"),[368,370],[432,_translate("Editor","Female Varient")]),
	SoundClass(_translate("Editor","Cheerleader"),[371,376,_translate("Editor","Female")],[424,429,_translate("Editor","Male")]),
	SoundClass(_translate("Editor","Snare Drum"),[377,380]),
	SoundClass(_translate("Editor","Bass Drum"),[381,383]),
	SoundClass(_translate("Editor","Galactic Drums"),[384,388]),
	SoundClass(_translate("Editor","Galactic Congas"),[389,393]),
	SoundClass(_translate("Editor","DJ Turntables"),[280,295]),
	SoundClass(_translate("Editor","Black Belt"),[394,399,_translate("Editor","Male")],[418,423,_translate("Editor","Female")]),
	SoundClass(_translate("Editor","Reggae Drums"),[400,404]),
	SoundClass(_translate("Editor","Whistle"),[405,408]),
	SoundClass(_translate("Editor","Beat Boxer"),[409,414]),
	SoundClass(_translate("Editor","Drum Mode"),[433,444])]

RetranslateSongNames()

class LoadType:
	Rom = 0
	Brsar = 1
	Carc = 2
	Dol = 3
	Midi = 4
	Gct = 5
	RomFile = 6

class RecordType:
	Song = "song"
	Style = "style"
	TextSong = "textsong"
	TextStyle = "textstyle"
	DefaultStyle = "defaultstyle"
	RemoveSong = "removesong"
	MainDol = "maindol"

#Functions

#Get File
def GetBrsarPath():
	if(os.path.isdir(file.path)):
		return file.path+"/files/Sound/MusicStatic/rp_Music_sound.brsar"
	else:
		return file.path

def GetMessagePath():
	if(os.path.isdir(file.path)):
		return file.path+"/files/"+BasedOnRegion(romLanguage)+"/Message"
	else:
		return os.path.dirname(file.path)

def GetGeckoPath():
	if(os.path.isdir(file.path)):
		return file.path+"/GeckoCodes.ini"
	else:
		return file.path

def GetMainDolPath():
	if(os.path.isdir(file.path)):
		return file.path+"/sys/main.dol"
	else:
		return file.path

def GivePermission(file):
	if(currentSystem != "Windows"):
		try:
			os.chmod(file,os.stat(file).st_mode | stats.S_IEXEC)
		except:
			tryed = 0

#Other
def Run(command):
	try:
		if(type(command) != str): GivePermission(command[0])
		if(currentSystem == "Windows"):
			CREATE_NO_WINDOW = 0x08000000
			subprocess.run(command,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=CREATE_NO_WINDOW)
		else:
			subprocess.run(command,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
	except Exception as e:
		ShowError("Could not execute command:","Command: "+str(command)+"\nError: "+str(e))

def DecodeTxt():
	path = GetMessagePath()
	if(not os.path.isfile(GetMessagePath()+'/message.d/new_music_message.txt')):
		try:
			if(os.path.isdir(path+"/message.d")): rmtree(path+"/message.d")
			Run([HelperPath()+'/Wiimms/wszst','extract',path+'/message.carc'])
			os.remove(path+"/message.d/wszst-setup.txt")
			Run([HelperPath()+'/Wiimms/wbmgt','decode',path+'/message.d/new_music_message.bmg'])
			os.remove(path+"/message.d/new_music_message.bmg")
		except Exception as e:
			ShowError("Could not decode text file",str(e))

def EncodeTxt():
	path = GetMessagePath()
	try:
		Run([HelperPath()+'/Wiimms/wbmgt','encode',path+'/message.d/new_music_message.txt'])
		os.remove(path+"/message.d/new_music_message.txt")
		if(not os.path.exists(path+"/message.carc.backup")): copyfile(path+"/message.carc",path+"/message.carc.backup")
		os.remove(path+"/message.carc")
		Run([HelperPath()+'/Wiimms/wszst','create',path+'/message.d','--dest',path+'/message.carc'])
		rmtree(path+'/message.d')
	except Exception as e:
		ShowError("Could not encode text file",str(e))

def GetRegion():
	for i in range(len(regionNames)):
		if(os.path.isdir(file.path+"/files/"+regionNames[i][0]+"/Message")):
			return i
	ShowError("Could not determine region","Using fallback region: "+BasedOnRegion(regionFullNames))
	return regionSelected

def GetDefaultStyle(SongID,default):
	style = Songs[SongID].DefaultStyle

	if(not default and os.path.exists(GetGeckoPath())):
		file = open(GetGeckoPath())
		textlines = file.readlines()
		file.close()
		for i in range(len(textlines)):
			if(textlines[i] == "$"+Songs[SongID].Name+" Default Style Patch [WiiMusicEditor]\n"):
				style = textlines[i+1][15:17:1]

	for i in range(len(Styles)):
		if(Styles[i].StyleId == style):
			return i

	return -1
			

#Main Functions
def AddPatch(PatchName,PatchInfo):
	if(type(PatchName) == str):
		PatchName = [PatchName]
		PatchInfo = [PatchInfo]

	for patchNum in range(len(PatchName)):
		if(os.path.exists(GetGeckoPath())):
			codes = open(GetGeckoPath(),'r')
			lineText = codes.readlines()
			codes.close()
			geckoExists = -1
			songExists = -1
			geckoEnabled = -1
			songEnabled = -1
			for num in range(len(lineText)):
				if(lineText[num].rstrip() == '[Gecko]'):
					geckoExists = num
				if(lineText[num].rstrip() == '$'+PatchName[patchNum]+' [WiiMusicEditor]'):
					songExists = num

			if(geckoExists == -1):
				lineText.insert(0,'[Gecko]\n'+'$'+PatchName[patchNum]+' [WiiMusicEditor]\n'+PatchInfo[patchNum])
			elif(songExists == -1):
				lineText.insert(geckoExists+1,'$'+PatchName[patchNum]+' [WiiMusicEditor]\n'+PatchInfo[patchNum])
			else:
				while True:
					if(len(lineText) <= songExists+1):
						break
					elif(not lineText[songExists+1][0].isnumeric() and (lineText[songExists+1][0] != 'f')):
						break
					else:
						lineText.pop(songExists+1)
				lineText.insert(songExists+1,PatchInfo[patchNum])
			
			for num in range(len(lineText)):
				if(lineText[num].rstrip() == '[Gecko_Enabled]'):
					geckoEnabled = num
				if(lineText[num].rstrip() == '$'+PatchName[patchNum]):
					songEnabled = num

			if(geckoEnabled == -1):
				lineText.insert(len(lineText),'[Gecko_Enabled]\n'+'$'+PatchName[patchNum]+'\n')
			elif(songEnabled == -1):
				lineText.insert(geckoEnabled+1,'$'+PatchName[patchNum]+'\n')
			
			codes = open(GetGeckoPath(),'w')
			codes.writelines(lineText)
			codes.close()
		else:
			codes = open(GetGeckoPath(),'w')
			codes.write('[Gecko]\n')
			codes.write('$'+PatchName[patchNum]+' [WiiMusicEditor]\n')
			codes.write(PatchInfo[patchNum])
			codes.write('[Gecko_Enabled]\n')
			codes.write('$'+PatchName[patchNum]+'\n')
			codes.close()

	#Copy Code to Dolphin
	if(LoadSetting("Settings","CopyCodes",True)):
		dir = GetDolphinSave()
		if(os.path.isdir(dir)):
			if(os.path.isfile(dir+"/GameSettings/"+BasedOnRegion(gameIds)+".ini")):
				if(not os.path.isfile(dir+"/GameSettings/"+BasedOnRegion(gameIds)+".backup.ini")):
					copyfile(dir+"/GameSettings/"+BasedOnRegion(gameIds)+".ini",dir+"/GameSettings/"+BasedOnRegion(gameIds)+".backup.ini")
				os.remove(dir+"/GameSettings/"+BasedOnRegion(gameIds)+".ini")
			copyfile(GetGeckoPath(),dir+"/GameSettings/"+BasedOnRegion(gameIds)+".ini")

def ChangeName(SongToChange,newText):
	txtPath = GetMessagePath()
	if(type(newText) != str):
		if(Songs[SongToChange].SongType == SongTypeValue.Regular):
			TextOffset = ['c8','190','12c']
		elif(Songs[SongToChange].SongType == SongTypeValue.Maestro):
			TextOffset = ['fa','1c2','15e']
		elif(Songs[SongToChange].SongType == SongTypeValue.Handbell):
			TextOffset = ['ff','1c7','163']
		textFromTxt[0][SongToChange] = newText[0]
		textFromTxt[1][SongToChange] = newText[1]
		textFromTxt[2][SongToChange] = newText[2]
	else: TextOffset = ['b200']
	DecodeTxt()
	for typeNum in range(3):
		message = open(txtPath+'/message.d/new_music_message.txt','rb')
		textlines = message.readlines()
		message.close()
		if(type(newText) != str):
			numberToChange = Songs[SongToChange].MemOrder
			if(Songs[SongToChange].SongType == SongTypeValue.Maestro):
				array = [0,4,2,3,1]
				numberToChange = array[numberToChange]
			elif(Songs[SongToChange].SongType == SongTypeValue.Handbell):
				array = [0,2,3,1,4]
				numberToChange = array[numberToChange]
		else:
			array = [3,1,4,2,7,10,11,9,8,6,5]
			numberToChange = array[SongToChange]

		offset = format(int(TextOffset[typeNum],16)+numberToChange,'x').lower()
		if(type(newText) != str):
			offset = ' ' * (4-len(offset))+offset+'00 @'
		else:
			offset = ' ' * (4-len(offset))+offset+' @'
		textlines = FixMessageFile(textlines)
		for num in range(len(textlines)):
			if offset in str(textlines[num]):
				while bytes('@','utf-8') not in textlines[num+1]:
					textlines.pop(num+1)

				if(type(newText) == str):
					text = repr(newText).strip("'").replace(r"\'","'").strip("\"")
				else:
					text = repr(newText[typeNum]).strip("'").replace(r"\'","'").strip("\"")
				textlines[num] = bytes(offset+str(textlines[num])[10:24:1]+text+'\r\n','utf-8')
				break
		message = open(txtPath+'/message.d/new_music_message.txt','wb')
		message.writelines(textlines)
		message.close()
		if(type(newText) == str): break
	EncodeTxt()

def CreateGct(path,geckopath=-1):
	if(geckopath == -1): geckopath = GetGeckoPath()
	patches = open(geckopath)
	textlines = patches.readlines()
	patches.close()
	codes = '00D0C0DE00D0C0DE'
	for text in textlines:
		if(text[0].isalpha() or text[0].isnumeric()):
			codes = codes + text.replace(' ','').strip()
	codes = codes+'F000000000000000'
	patch = open(path,'wb')
	patch.write(bytes.fromhex(codes))
	patch.close()

def BasedOnRegion(array):
	global regionSelected
	return array[regionSelected]

def SizeIncreaseBrsar(file,sizeDifference,startoffset):
	groupTableOffset = dataPath(file,inO,grO)
	file.seek(groupTableOffset)
	numberOfGroups = int.from_bytes(file.read(4),"big")

	for i in range(numberOfGroups-1):
		offset = dataPath(file,inO,grO,0x8*(i+1))+0x10
		if(offset > startoffset):
			file.seek(offset)
			size = file.read(4)
			file.seek(offset)
			file.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
			offset += 8
			file.seek(offset)
			size = file.read(4)
			file.seek(offset)
			file.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big')) 

def ReplaceSong(positionNum,replacementArray,BrseqOrdering,BrseqInfoArray,BrseqLengthArray):
	if(not os.path.exists(GetBrsarPath()+".backup")): copyfile(GetBrsarPath(),GetBrsarPath()+".backup")
	BrsarPath = GetBrsarPath()
	BrseqInfo = []
	BrseqLength = []
	for i in range(len(BrseqOrdering)):
		BrseqInfo.append(BrseqInfoArray[BrseqOrdering[i]])
		BrseqLength.append(BrseqLengthArray[BrseqOrdering[i]])
	sizeDifference = 0
	brsar = open(BrsarPath, "rb")
	positionOffset = dataPath(brsar,inO,grO,0x8*(positionNum+1))+0x10
	listOffset = BrsarGetList(brsar,positionOffset)
	replacementArray.append(getData(brsar,dataPath(brsar,inO,grO,8*(positionNum+1))+0x28))
	brsar.seek(positionOffset)
	currentSpot = int.from_bytes(brsar.read(4),'big')
	if(listOffset != -1):
		posOffset = []
		lenOffset = []
		data = []
		for num in range(len(replacementArray)-1):
			brsar.seek(listOffset+24*replacementArray[num])
			posOffset.append(brsar.read(4))
			lenOffset.append(brsar.read(4))
		brsar.seek(0)
		data.append(brsar.read(currentSpot+int.from_bytes(posOffset[0],'big')))
		for num in range(len(replacementArray)-2):
			brsar.seek(currentSpot+int.from_bytes(posOffset[num],'big')+int.from_bytes(lenOffset[num],'big'))
			data.append(brsar.read(int.from_bytes(posOffset[num+1],'big')-int.from_bytes(posOffset[num],'big')-int.from_bytes(lenOffset[num],'big')))
		brsar.seek(currentSpot+int.from_bytes(posOffset[len(posOffset)-1],'big')+int.from_bytes(lenOffset[len(lenOffset)-1],'big'))
		data.append(brsar.read())
		brsar.close()
		for num in range(len(replacementArray)-1):	
			if(num == 0):
				infoToWrite = data[num]+BrseqInfo[num]
			else:
				infoToWrite = infoToWrite+data[num]+BrseqInfo[num]
		infoToWrite = infoToWrite+data[len(replacementArray)-1]
		brsar = open(BrsarPath, "wb")
		brsar.write(infoToWrite)
		brsar.close()
		brsar = open(BrsarPath, "r+b")
		for num in range(replacementArray[0],replacementArray[len(replacementArray)-1]):
			if(sizeDifference != 0):
				brsar.seek(listOffset+24*num)
				size = brsar.read(4)
				brsar.seek(listOffset+24*num)
				brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
			if (num in replacementArray):
				brsar.seek(listOffset+4+24*num)
				sizeDifference += BrseqLength[replacementArray.index(num)]-int.from_bytes(brsar.read(4),"big")
				brsar.seek(listOffset+4+24*num)
				brsar.write(BrseqLength[replacementArray.index(num)].to_bytes(4, 'big'))
		
		SizeIncreaseBrsar(brsar,sizeDifference,positionOffset)

		for offset in [8,positionOffset+4]:
			brsar.seek(offset)
			size = brsar.read(4)
			brsar.seek(offset)
			brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
	else:
		data = []
		brsar.seek(0)
		data.append(brsar.read(currentSpot))
		brsar.seek(positionOffset+4)
		brsar.seek(currentSpot+int.from_bytes(brsar.read(4),'big'))
		data.append(brsar.read())
		brsar.close()
		brsar = open(BrsarPath, "wb")
		brsar.write(data[0]+BrseqInfo+data[1])
		brsar.close()
		brsar = open(BrsarPath, "r+b")
		brsar.seek(positionOffset+4)
		sizeDifference = BrseqLength-int.from_bytes(brsar.read(4),"big")

		SizeIncreaseBrsar(brsar,sizeDifference,positionOffset)

		for offset in [8,positionOffset+4]:
			brsar.seek(offset)
			size = brsar.read(4)
			brsar.seek(offset)
			brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
	brsar.close()

def ConvertWav(wavPath,loopstart=-1,loopend=-1):
	with tempfile.TemporaryDirectory() as directory:
		if(LoadSetting("Settings","ResampleSounds",True)):
			s_read = wave.open(wavPath, 'r')
			framerate = s_read.getframerate()

			if(framerate != 16000 and s_read.getnchannels() != 1):
				wavPath = directory+"converted.wav"
				s_write = wave.open(wavPath, 'w')
				s_write.setparams((1, 2, 16000, 0, 'NONE', 'Uncompressed'))
				data = s_read.readframes(s_read.getnframes())
				if(framerate != 16000):
					data = audioop.ratecv(data, 2, s_read.getnchannels(), framerate, 16000, None)
					if(loopstart != -1):
						loopstart *= 16000/framerate
						loopend *= 16000/framerate
				if(s_read.getnchannels() != 1): data = audioop.tomono(data[0], 2, 1, 0)
				s_write.writeframes(data)
				s_write.close()
			s_read.close()
			
		cmd = [HelperPath()+"/SoundConverter/rwavconvert",wavPath,directory+"converted.rwav"]
		if(loopstart != -1):
			cmd.append(str(round(loopstart)))
			cmd.append(str(round(loopend)))
		Run(cmd)
		file = open(directory+"converted.rwav","rb")
		rwavInfo = file.read()
		file.close()
		rwavSize = os.stat(directory+"converted.rwav").st_size

	return rwavInfo, rwavSize

def ReplaceWave(startOffset,replaceNumber,rwavInfo,rwavSize):
	if(not os.path.exists(GetBrsarPath()+".backup")): copyfile(GetBrsarPath(),GetBrsarPath()+".backup")
	sizeDifference = 0
	brsar = open(GetBrsarPath(), "r+b")
	brsar.seek(startOffset)
	rwarSpot = int.from_bytes(brsar.read(4),'big')
	brsar.seek(rwarSpot+0x18)
	dataSection = rwarSpot+int.from_bytes(brsar.read(4),'big')
	brsar.seek(rwarSpot+0x10)
	table = rwarSpot+int.from_bytes(brsar.read(4),'big')
	brsar.seek(table+8)
	numberOfRwavs = int.from_bytes(brsar.read(4),'big')
	if(numberOfRwavs == len(replaceNumber)): replaceNumber = -1
	if(replaceNumber == -1):
		for i in range(numberOfRwavs):
			brsar.seek(table+0x10+0xC*i)
			tempdataSpot = int.from_bytes(brsar.read(4),'big')
			if(i == 0): dataSpot = tempdataSpot
			dataSize = int.from_bytes(brsar.read(4),'big')
			brsar.seek(table+0x10+0xC*i)
			offset = int.from_bytes(brsar.read(4),'big')
			brsar.seek(table+0x10+0xC*i)
			brsar.write((offset+sizeDifference).to_bytes(4, 'big'))
			brsar.seek(table+0x10+0xC*i)
			brsar.write((tempdataSpot+sizeDifference).to_bytes(4, 'big'))
			sizeDifference += rwavSize-dataSize
			brsar.seek(table+0x10+0xC*i+4)
			brsar.write(rwavSize.to_bytes(4, 'big'))
		brsar.seek(0)
		data1 = brsar.read(dataSection+dataSpot)
		brsar.seek(dataSection+dataSpot+rwavSize*numberOfRwavs-sizeDifference)
		data2 = brsar.read()
		brsar.seek(0)
		brsar.write(data1+rwavInfo*numberOfRwavs+data2)
		brsar.truncate()
	else:
		for i in replaceNumber:
			brsar.seek(table+0x10+0xC*i)
			dataSpot = int.from_bytes(brsar.read(4),'big')
			dataSize = int.from_bytes(brsar.read(4),'big')
			sizeDifference += rwavSize-dataSize
			brsar.seek(table+0x10+0xC*i+4)
			brsar.write(rwavSize.to_bytes(4, 'big'))
			brsar.seek(0)
			data1 = brsar.read(dataSection+dataSpot)
			brsar.seek(dataSection+dataSpot+dataSize)
			data2 = brsar.read()
			brsar.seek(0)
			brsar.write(data1+rwavInfo+data2)
			brsar.truncate()
			for j in range(i+1,numberOfRwavs):
				brsar.seek(table+0x10+0xC*j)
				offset = int.from_bytes(brsar.read(4),'big')
				brsar.seek(table+0x10+0xC*j)
				brsar.write((offset+rwavSize-dataSize).to_bytes(4, 'big'))
			
	for offset in [8,startOffset+4,rwarSpot+8]:
		brsar.seek(offset)
		size = brsar.read(4)
		brsar.seek(offset)
		brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
	for offset in rseqList:
		if(offset > startOffset):
			brsar.seek(offset)
			size = brsar.read(4)
			brsar.seek(offset)
			brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
	brsar.close()

def PlayRwav(startOffset,replaceNumber):
	if(os.path.isdir(SavePath()+"/tmp")):
		try:
			rmtree(SavePath()+"/tmp")
		except Exception:
			tried = True
	
	if(not os.path.isdir(SavePath()+"/tmp")): os.mkdir(SavePath()+"/tmp")
	brsar = open(GetBrsarPath(), "r+b")
	brsar.seek(startOffset)
	rwarSpot = int.from_bytes(brsar.read(4),'big')
	brsar.seek(rwarSpot+0x18)
	dataSection = rwarSpot+int.from_bytes(brsar.read(4),'big')
	brsar.seek(rwarSpot+0x10)
	table = rwarSpot+int.from_bytes(brsar.read(4),'big')
	for i in replaceNumber:
		brsar.seek(table+0x10+0xC*i)
		dataSpot = int.from_bytes(brsar.read(4),'big')
		dataSize = int.from_bytes(brsar.read(4),'big')
		brsar.seek(dataSection+dataSpot)
		wav = open(SavePath()+"/tmp/sound"+str(i)+".rwav","wb")
		wav.write(brsar.read(dataSize))
		wav.close()
	brsar.close()
	try:
		args = [HelperPath()+"/SoundConverter/vgmstream","-o","?f.wav"]
		for i in replaceNumber:
			args.append(SavePath()+"/tmp/sound"+str(i)+".rwav")
		if(currentSystem == "Mac"):
			command = "vgmstream-cli"
			for i in range(3,len(args)): command += ' "'+args[i]+'"'
			subprocess.run(command,shell=True)
		else: Run(args)
	except Exception as e:
		error = ""
		if(currentSystem == "Mac"): error = "Install vgmstream using 'brew install vgmstream'\n"
		error += str(e)
		ShowError("Could not play audio",error)

def NormalizeMidi(midiPath,savePath,defaultTempo):
	mid = mido.MidiFile(midiPath)
	for track in mid.tracks:
		for num,msg in enumerate(track):
			try:
				if(not msg.is_meta and msg.channel != 0):
					track[num] = msg.copy(channel=0)
			except Exception:
				tried = True
	mid.save(savePath)
	midi_data = pretty_midi.PrettyMIDI(savePath)
	newMidi = pretty_midi.PrettyMIDI(initial_tempo=defaultTempo,resolution=2000)
	i = 0
	for instrument in midi_data.instruments:
		newInstrument = pretty_midi.Instrument(program=instrument.program,is_drum=instrument.is_drum,name="Track"+str(i))
		i += 1
		for note in instrument.notes:
			newInstrument.notes.append(pretty_midi.Note(
			velocity=note.velocity, pitch=note.pitch, start=note.start, end=note.end))
		newMidi.instruments.append(newInstrument)
	newMidi.write(savePath)
	mid = mido.MidiFile(savePath)
	mid.tracks[1] = mido.merge_tracks([mid.tracks[0],mid.tracks[1]])
	mid.tracks.remove(mid.tracks[0])
	for track in mid.tracks:
		for i in range(len(track)):
			if(track[i].type == "note_on" and track[i].velocity == 0):
				track[i] = mido.Message("note_off",note=track[i].note,velocity=track[i].velocity,time=track[i].time,channel=track[i].channel)
	mid.save(savePath)

def LoadMidi(midiPath,defaultTempo = -1):
	with tempfile.TemporaryDirectory() as directory:
		prefix = pathlib.Path(midiPath).suffix
		if(prefix == '.mid'): prefix = '.midi'
		if(defaultTempo == -1):
			copyfile(midiPath,directory+'/z'+prefix)
		else:
			NormalizeMidi(midiPath,directory+'/z'+prefix,defaultTempo)

		if(os.path.isfile(directory+'/z.rseq')):
			Run([HelperPath()+'/SequenceCmd/GotaSequenceCmd','assemble',directory+'/z.rseq'])
		if(os.path.isfile(directory+'/z.brseq')):
			Run([HelperPath()+'/SequenceCmd/GotaSequenceCmd','to_midi',directory+'/z.brseq'])
		else:
			Run([HelperPath()+'/SequenceCmd/GotaSequenceCmd','from_midi',directory+'/z.midi'])

		mid = mido.MidiFile(directory+"/z.midi")		
		Tempo = 0
		TimeSignature = 4
		for msg in mid.tracks[0]:
			if(msg.type == 'set_tempo'):
				Tempo = floor(mido.tempo2bpm(msg.tempo))
			elif(msg.type == 'time_signature'):
				TimeSignature = msg.numerator
		Length = ceil(mid.length*Tempo/60)
		Tempo = Tempo
		Brseq = open(directory+"/z.brseq","rb")
		Brseq.seek(0)
		info = Brseq.read()
		Brseq.close()
		fileLength = os.stat(directory+"/z.brseq").st_size
	return [info,fileLength,Tempo,Length,TimeSignature]

def GetSongNames():
	global textFromTxt
	textFromTxt = [[],[],[],[]]
	DecodeTxt()
	message = open(GetMessagePath()+'/message.d/new_music_message.txt','rb')
	textlines = message.readlines()
	message.close()
	rmtree(GetMessagePath()+'/message.d')
	for i in range(3):
		for SongToChange in range(len(Songs)-1):
			TextOffset = ['c8','190','12c']
			numberToChange = Songs[SongToChange].MemOrder
			if(Songs[SongToChange].SongType == SongTypeValue.Maestro):
				TextOffset = ['fa','1c2','15e']
				array = [0,4,2,3,1]
				numberToChange = array[numberToChange]
			elif(Songs[SongToChange].SongType == SongTypeValue.Handbell):
				TextOffset = ['ff','1c7','163']
				array = [0,2,3,1,4]
				numberToChange = array[numberToChange]
			offset = format(int(TextOffset[i],16)+numberToChange,'x').lower()
			offset = ' ' * (4-len(offset))+offset+'00 @'
			for num in range(len(textlines)):
				if offset in str(textlines[num]):
					textToAdd = (textlines[num][22:len(textlines[num])-2:1]).decode("utf-8")
					for number in range(num+1,len(textlines)):
						if bytes('@','utf-8') in textlines[number]: break
						textToAdd = textToAdd[0:len(textToAdd)-2:1]+"\n"+(textlines[number][3:len(textlines[number])-2:1]).decode("utf-8")
					textFromTxt[i].append(textToAdd)
					break
	TextOffset = "b200"
	array = [3,1,4,2,7,10,11,9,8,6,5]
	for i in range(11):
		numberToChange = array[i]
		offset = format(int(TextOffset,16)+numberToChange,'x').lower()
		offset = ' ' * (4-len(offset))+offset+' @'
		for num in range(len(textlines)):
			if offset in str(textlines[num]):
				textToAdd = (textlines[num][22:len(textlines[num])-2:1]).decode("utf-8")
				for number in range(num+1,len(textlines)):
					if bytes('@','utf-8') in textlines[number]: break
					textToAdd = textToAdd[0:len(textToAdd)-2:1]+"\n"+(textlines[number][3:len(textlines[number])-2:1]).decode("utf-8")
				textFromTxt[3].append(textToAdd)
				break

def GetStyles():
	global loadedStyles
	for i in range(len(Styles)):
		loadedStyles[i] = Styles[i].DefaultStyle
	if(os.path.exists(GetGeckoPath())):
		file = open(GetGeckoPath())
		textlines = file.readlines()
		file.close()
		for i in range(len(textlines)):
			if("Style Patch [WiiMusicEditor]" in textlines[i] and "Default Style Patch [WiiMusicEditor]" not in textlines[i]):
				for j in range(len(Styles)):
					if(Styles[j].Name == textlines[i][1:len(textlines[i])-30:1]):
						loadedStyles[j] = [
						min(int(textlines[i+2][6:8:1],16),len(Instruments)-1),
						min(int(textlines[i+2][15:17:1],16),len(Instruments)-1),
						min(int(textlines[i+3][6:8:1],16),len(Instruments)-1),
						min(int(textlines[i+3][15:17:1],16),len(Instruments)-1),
						min(int(textlines[i+4][6:8:1],16),len(Instruments)-1),
						min(int(textlines[i+4][15:17:1],16),len(Instruments)-1)]
						break

def PatchBrsar(SongSelected,BrseqInfo,BrseqLength,Tempo,Length,TimeSignature):
	if(LoadSetting("Setting","RapperFix",True)):
		AddPatch('Rapper Crash Fix',BasedOnRegion([
			'043B0BBB 881C0090\n043B0BBF 7C090000\n043B0BC3 4081FFBC\n043B0BC7 881C00D6\n',
			'043B0CCF 881C0090\n043B0CD3 7C090000\n043B0BC3 4081FFBC\n043B0CD7 881C00D6\n',
			'043AE47F 881C0090\n043AE483 7C090000\n043AE487 4081FFBC\n043AE48B 881C00D6\n',
			'0429CE7B 881C0090\n0429CE7F 7C090000\n0429CE83 4081FFBC\n0429CE87 881C00D6\n']))
	if(Songs[SongSelected].SongType != SongTypeValue.Menu):
		Tempo = format(Tempo,"x")
		Length = format(Length,"x")
		LengthCode = '0'+format(Songs[SongSelected].MemOffset+BasedOnRegion(gctRegionOffsets)+6,'x').lower()+' '+'0'*(8-len(Length))+Length+'\n'
		TempoCode = '0'+format(Songs[SongSelected].MemOffset+BasedOnRegion(gctRegionOffsets)+10,'x').lower()+' '+'0'*(8-len(Tempo))+Tempo+'\n'
		TimeCode = '0'+format(Songs[SongSelected].MemOffset+BasedOnRegion(gctRegionOffsets),'x').lower()+' 00000'+str(TimeSignature)+'00\n'
	if(Songs[SongSelected].SongType == SongTypeValue.Regular):
		ReplaceSong(2,[Songs[SongSelected].MemOrder*2,Songs[SongSelected].MemOrder*2+1],[0,1],BrseqInfo,BrseqLength)
		AddPatch(Songs[SongSelected].Name+' Song Patch',LengthCode+TempoCode+TimeCode)
		if(Songs[SongSelected].Name == 'Do-Re-Mi'):
			ReplaceSong(3,[18,19,113,155,156,157,158,159,160,161,162],[0,1,0,0,0,0,0,0,0,0,0],BrseqInfo,BrseqLength)
			ReplaceSong(19,[18,19,113],[0,1,0],BrseqInfo,BrseqLength)
	elif(Songs[SongSelected].SongType == SongTypeValue.Menu):
		ReplaceSong(34,[0,1,2,3,4,5,6],[0,1,1,1,1,1,1],BrseqInfo,BrseqLength)
	elif(Songs[SongSelected].SongType == SongTypeValue.Maestro):
		ReplaceSong(21,[Songs[SongSelected].MemOrder+2],[0],BrseqInfo,BrseqLength)
		AddPatch(Songs[SongSelected].Name+' Song Patch',LengthCode+TempoCode+TimeCode)
	elif(Songs[SongSelected].SongType == SongTypeValue.Handbell):
		ReplaceSong(23,[Songs[SongSelected].MemOrder*5+2,Songs[SongSelected].MemOrder*5+3,Songs[SongSelected].MemOrder*5+4,Songs[SongSelected].MemOrder*5+5,Songs[SongSelected].MemOrder*5+6],[0,0,0,0,0],BrseqInfo,BrseqLength)
		LengthCode = '0'+format(Songs[SongSelected].MemOffset+BasedOnRegion(gctRegionOffsets),'x').lower()+' '+'0'*(8-len(Length))+Length+'\n'
		LengthCode2 = '0'+format(Songs[SongSelected].MemOffset+BasedOnRegion(gctRegionOffsets)+4,'x').lower()+' '+'0'*(8-len(Length))+Length+'\n'
		MeasureCode = '0'+format(Songs[SongSelected].MemOffset+BasedOnRegion(gctRegionOffsets)+24,'x').lower()+' '+'00000000\n'
		AddPatch(Songs[SongSelected].Name+' Song Patch',LengthCode+LengthCode2+MeasureCode)

def BrsarGetList(file,positionOffset):
	return getData(file,inO)+0x10+getData(file,positionOffset+0x14)+getData(file,positionOffset+0x18)*8

def GetTableOffset(file,num):
	return dataPath(file,inO,grO,0x8*(num+1))

def printh(num): print(format(num,"x"))

def BrseqAddingName(text):
	brsar = open(GetBrsarPath(),"r+b")
	sizeDifference = 4*len(text)
	for i in range(len(text)):
		text[i] = text[i].encode("utf-8")
		if(i != len(text)-1): text[i] += bytes(1)
		sizeDifference += len(text[i])

	offset = dataPath(brsar,syO,0x0C)-1
	brsar.seek(offset)
	extra = 0
	while(int.from_bytes(brsar.read(1),"big") == 0):
		extra += 1
		brsar.seek(offset-extra)
	positionOffset = offset+1
	text[len(text)-1] += bytes(4-((sizeDifference-extra) % 4)-1)
	sizeDifference += 4-((sizeDifference-extra) % 4)-1

	number = getData(brsar,dataPath(brsar,syO,0x8))
	brsar.seek(dataPath(brsar,syO,0x8))
	brsar.write((number+len(text)).to_bytes(4, 'big'))

	#Other Name Offsets
	for i in range(number):
		offset = dataPath(brsar,syO,0x8)+4*(i+1)
		brsar.seek(offset)
		size = brsar.read(4)
		brsar.seek(offset)
		brsar.write((int.from_bytes(size,"big")+4*len(text)).to_bytes(4, 'big'))

	#group table 335A8 33500
	for i in range(getData(brsar,dataPath(brsar,inO,grO))):
		offset = dataPath(brsar,inO,grO,(i+1)*8)
		for j in [0x10,0x18]:
			brsar.seek(offset+j)
			size = brsar.read(4)
			brsar.seek(offset+j)
			brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))

	#file length, size of info, offset to file
	for offset in [0x8,0x14,0x18,0x20,dataPathPoint(brsar,syO,0x4),dataPathPoint(brsar,syO,0x0C),dataPathPoint(brsar,syO,0x10),dataPathPoint(brsar,syO,0x14),dataPathPoint(brsar,syO,0x18)]:
		brsar.seek(offset)
		size = brsar.read(4)
		brsar.seek(offset)
		brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
	
	data1Point = dataPath(brsar,syO,0x08)+4*(number+1)
	data2Point = positionOffset-data1Point
	brsar.seek(0)
	dataToWrite = brsar.read(data1Point)
	for i in range(len(text)):
		dataToWrite += positionOffset.to_bytes(4,"big")
		positionOffset += len(text[i])
	dataToWrite += brsar.read(data2Point-extra+1)
	brsar.seek(data1Point+data2Point)
	for i in text:
		dataToWrite += i
	dataToWrite += brsar.read()
	brsar.close()
	brsar = open(GetBrsarPath(),"wb")
	brsar.write(dataToWrite)
	brsar.close()
	return number

def BrseqAddingSounddata(nameNumber,collectNumber):
	slotsToAdd = 2
	brsar = open(GetBrsarPath(),"r+b")
	number = getData(brsar,dataPath(brsar,inO,sdO))
	sizeDifference = 0x54*slotsToAdd
	brsar.seek(dataPath(brsar,inO,sdO))
	brsar.write((number+slotsToAdd).to_bytes(4, 'big'))

	#Sound Data list 17A30
	for i in range(number):
		offset = dataPath(brsar,inO,sdO)+(i+1)*8
		suboffset = dataPath(brsar,inO,sdO,(i+1)*8)
		for j in [suboffset+0x10,suboffset+0x1C,offset]:
			brsar.seek(j)
			size = brsar.read(4)
			brsar.seek(j)
			brsar.write((int.from_bytes(size,"big")+0x8*slotsToAdd).to_bytes(4, 'big'))

	#Soundbank, Player Info
	for offsettype in [sbO,piO]:
		for i in range(getData(brsar,dataPath(brsar,inO,offsettype))):
			offset = dataPath(brsar,inO,offsettype)+(i+1)*8
			brsar.seek(offset)
			size = brsar.read(4)
			brsar.seek(offset)
			brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))

	#2DAFC - Collection
	for i in range(getData(brsar,dataPath(brsar,inO,ctO))):
		offset = dataPath(brsar,inO,ctO,(i+1)*8,0x18)
		for j in range(getData(brsar,offset)):
			brsar.seek(offset+(j+1)*8)
			size = brsar.read(4)
			brsar.seek(offset+(j+1)*8)
			brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
		offset = dataPath(brsar,inO,ctO,(i+1)*8)+0x18
		brsar.seek(offset)
		size = brsar.read(4)
		brsar.seek(offset)
		brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
		offset = dataPath(brsar,inO,ctO)+(i+1)*8
		brsar.seek(offset)
		size = brsar.read(4)
		brsar.seek(offset)
		brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))

	#group table 335A8 33500
	for i in range(getData(brsar,dataPath(brsar,inO,grO))):
		offset = dataPath(brsar,inO,grO,(i+1)*8)
		for j in [0x10,0x18,0x24]:
			brsar.seek(offset+j)
			size = brsar.read(4)
			brsar.seek(offset+j)
			brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
		for j in range(getData(brsar,offset+0x28)):
			brsar.seek(offset+0x30+j*8)
			size = brsar.read(4)
			brsar.seek(offset+0x30+j*8)
			brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
		offset = dataPath(brsar,inO,grO)+(i+1)*8
		brsar.seek(offset)
		size = brsar.read(4)
		brsar.seek(offset)
		brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))

	#file length, size of info, offset to file
	for offset in [0x8,0x1C,0x20,dataPathPoint(brsar,inO,0x4),dataPathPoint(brsar,inO,0x14),dataPathPoint(brsar,inO,0x1C),dataPathPoint(brsar,inO,0x24),dataPathPoint(brsar,inO,0x2C),dataPathPoint(brsar,inO,0x34),dataPathPoint(brsar,inO,scO,0x2)]:
		brsar.seek(offset)
		size = brsar.read(4)
		brsar.seek(offset)
		brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))

	#Add New Offsets
	#sounddata = 01B7+i 38+i 0000000301000000 (start + 0x40) 64780100010001010000 (start + 0x2C) 0000000000000000000000000000000000300000000 (0000C00F song/000000FF score) 7800000000000000000000000180000000
	soundDataOffset = dataPath(brsar,inO,sdO,number*8)+0x4C-8*slotsToAdd
	soundDataOffsetTable = dataPath(brsar,inO,sdO)+number*8+4
	lastOffset = getData(brsar,soundDataOffsetTable-4)

	brsar.seek(0)
	dataToWrite = brsar.read(soundDataOffsetTable)
	for i in range(slotsToAdd):
		dataToWrite += (0x01000000).to_bytes(4,"big")+(lastOffset+0x4C*(i+1)).to_bytes(4,"big")
	dataToWrite += brsar.read(soundDataOffset-soundDataOffsetTable)
	for i in range(slotsToAdd):
		dataToWrite += (nameNumber+i).to_bytes(4,"big")+(collectNumber+i).to_bytes(4,"big")+(0x301000000).to_bytes(8,"big")+(lastOffset+0x4C*(i+1)+0x40).to_bytes(4,"big")+(0x6478010001010000).to_bytes(8,"big")+(lastOffset+0x4C*(i+1)+0x2C).to_bytes(4,"big")+(0x3000000000000).to_bytes(22,"big")
		if(i % 2 == 0): dataToWrite += (0xC00F).to_bytes(2,"big")
		else: dataToWrite += (0x00FF).to_bytes(2,"big")
		dataToWrite += (0x7800000000000000000000000180000000000000).to_bytes(20,"big")
	dataToWrite += brsar.read()
	brsar.close()
	brsar = open(GetBrsarPath(),"wb")
	brsar.write(dataToWrite)
	brsar.close()

	return number

def BrseqAddingCollection(group,sizes):
	slotsToAdd = 2
	brsar = open(GetBrsarPath(),"r+b")
	positionNum = getData(brsar,dataPath(brsar,inO,ctO))
	sizeDifference = 0x38*slotsToAdd
	brsar.seek(dataPath(brsar,inO,ctO))
	brsar.write((positionNum+slotsToAdd).to_bytes(4, 'big'))
	positionOffset = dataPath(brsar,inO,grO)
	pos = getData(brsar,dataPathPoint(brsar,inO,grO))+0x10
	
	#collectionshift
	for i in range(positionNum):
		offset = dataPath(brsar,inO,ctO,(i+1)*8,0x18)
		for j in range(getData(brsar,offset)):
			brsar.seek(offset+(j+1)*8)
			size = brsar.read(4)
			brsar.seek(offset+(j+1)*8)
			brsar.write((int.from_bytes(size,"big")+8*slotsToAdd).to_bytes(4, 'big'))
		offset = dataPath(brsar,inO,ctO,(i+1)*8)+0x18
		brsar.seek(offset)
		size = brsar.read(4)
		brsar.seek(offset)
		brsar.write((int.from_bytes(size,"big")+8*slotsToAdd).to_bytes(4, 'big'))
		offset = dataPath(brsar,inO,ctO)+(i+1)*8
		brsar.seek(offset)
		size = brsar.read(4)
		brsar.seek(offset)
		brsar.write((int.from_bytes(size,"big")+8*slotsToAdd).to_bytes(4, 'big'))

	#group table 335A8 33500
	for i in range(getData(brsar,dataPath(brsar,inO,grO))):
		offset = dataPath(brsar,inO,grO,(i+1)*8)
		for j in [0x10,0x18,0x24]:
			brsar.seek(offset+j)
			size = brsar.read(4)
			brsar.seek(offset+j)
			brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
		for j in range(getData(brsar,offset+0x28)):
			brsar.seek(offset+0x30+j*8)
			size = brsar.read(4)
			brsar.seek(offset+0x30+j*8)
			brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
		offset = dataPath(brsar,inO,grO)+(i+1)*8
		brsar.seek(offset)
		size = brsar.read(4)
		brsar.seek(offset)
		brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))

	#file length, size of info, offset to file
	for offset in [0x8,0x1C,0x20,dataPathPoint(brsar,inO,0x4),dataPathPoint(brsar,inO,0x2C),dataPathPoint(brsar,inO,0x34)]:
		brsar.seek(offset)
		size = brsar.read(4)
		brsar.seek(offset)
		brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))

	#collection index group: randomlengthnumber(4bytes) FFFFFFFF(8bytes) 01000000(12bytes) postitionoffset+0x1C(4bytes) 0301000000(8bytes) postitionoffset+0x38(4bytes) 01000000(4bytes) postitionoffset+0x40(4bytes) 01000000(4bytes) postitionoffset+0x48(4bytes) 02(4bytes) 63+number(4bytes) 03(4bytes) 63+number(4bytes) 13(4bytes) 63+number(4bytes)
	data1Point = dataPath(brsar,inO,ctO)+8*positionNum+4
	brsar.seek(0)
	dataToWrite = brsar.read(data1Point)
	for i in range(slotsToAdd):
		dataToWrite += (0x01000000).to_bytes(4,"big")+(pos+i*0x30).to_bytes(4,"big")
	dataToWrite += brsar.read(positionOffset-data1Point)
	for i in range(slotsToAdd):
		dataToWrite += sizes[i].to_bytes(4,"big")+(0xFFFFFFFF).to_bytes(8,"big")+(0x01000000).to_bytes(12,"big")+(pos+i*0x30+0x1C).to_bytes(4,"big")
		#the collection pos entry could maybe reperesent putting the song in different tables for space saving purposes
		dataToWrite += (0x0101000000).to_bytes(8,"big")+(pos+i*0x30+0x28).to_bytes(4,"big")+(0x02).to_bytes(4,"big")+(group+i).to_bytes(4,"big")
	dataToWrite += brsar.read()
	brsar.close()
	brsar = open(GetBrsarPath(),"wb")
	brsar.write(dataToWrite)
	brsar.close()
	return positionNum

def BrseqAddingTable(positionNum):
	slotsToAdd = 2
	brsar = open(GetBrsarPath(),"r+b")
	positionOffset = GetTableOffset(brsar,positionNum)+0x10
	listOffset = BrsarGetList(brsar,positionOffset)
	brsar.seek(positionOffset+0x18)
	num = int.from_bytes(brsar.read(4),"big")
	brsar.seek(positionOffset+0x18)
	#number of tracks
	brsar.write((num+slotsToAdd).to_bytes(4,"big"))

	brsar.seek(listOffset+24*(num-1))
	amount = int.from_bytes(brsar.read(4),"big")+int.from_bytes(brsar.read(4),"big")
	brsar.seek(listOffset+24*(num-1)-4)
	number = int.from_bytes(brsar.read(4),"big")+slotsToAdd
	lastTableOffset = getData(brsar,listOffset-8)+8*slotsToAdd

	sizeDifference = 0x20*slotsToAdd

	numberOfGroups = getData(brsar,dataPath(brsar,inO,grO))
	
	#for every group entry after the changed group
	for i in range(numberOfGroups):
		offset = dataPath(brsar,inO,grO,0x8*(i+1))
		if(i > positionNum):
			location = dataPathPoint(brsar,inO,grO,0x8*(i+1))
			brsar.seek(location)
			size = brsar.read(4)
			brsar.seek(location)
			brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))

		#offset to rseq, offset to rwar, offset to subsection 2
		offsetList = [0x10,0x18]
		if(i > positionNum): offsetList.append(0x24)
		for j in offsetList:
			brsar.seek(offset+j)
			size = brsar.read(4)
			brsar.seek(offset+j)
			brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))

		#offsets in the big table
		if(i >= positionNum):
			numbers = getData(brsar,offset+0x28)
			if(i == positionNum): numbers -= slotsToAdd
			for j in range(numbers):
				offsetToChoose = sizeDifference
				if(i == positionNum): offsetToChoose = 8*slotsToAdd
				newOffset = getData(brsar,offset+0x30+8*j)+offsetToChoose
				brsar.seek(offset+0x30+8*j)
				#printh(offset)
				brsar.write(newOffset.to_bytes(4,"big"))
	
	#total, info size, file offset, sound count table, info size
	for offset in [0x8,0x1C,0x20,dataPathPoint(brsar,inO,0x34),dataPathPoint(brsar,inO,0x4)]:
		brsar.seek(offset)
		size = brsar.read(4)
		brsar.seek(offset)
		brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))

	#add expanding parts
	brsar.seek(0)
	data1 = brsar.read(listOffset-4)
	data2 = brsar.read(24*num)
	data3 = brsar.read()
	brsar.close()
	brsar = open(GetBrsarPath(),"wb")
	dataToWrite = data1
	for i in range(slotsToAdd):
		dataToWrite += b"\01\00\00\00"+(lastTableOffset+0x18*(i+1)).to_bytes(4,"big")
	dataToWrite += data2
	for i in range(slotsToAdd):
		dataToWrite += (number+i).to_bytes(4,"big")+amount.to_bytes(4,"big")+bytes(16)
	dataToWrite += data3
	brsar.write(dataToWrite)
	brsar.close()

	return num

def BrseqAddingDol(number,midiInfo,brseqNumber):
	#59C520
	dol = open(GetMainDolPath(),"r+b")
	sizeDifference = 0xBC
	positionOffset = 0x59C520+0xBC*50#0x005AB200

	if(False):
		#offset
		for i in range(18):
			dol.seek(4*i)
			size = int.from_bytes(dol.read(4),"big")
			if(size > 0x59C56E):
				dol.seek(4*i)
				dol.write((size+sizeDifference).to_bytes(4,"big"))

		#size
		dol.seek(0xC0)
		size = int.from_bytes(dol.read(4),"big")
		dol.seek(0xC0)
		dol.write((size+sizeDifference).to_bytes(4,"big"))

	#stuff: number + something
	dol.seek(0)
	data = dol.read(positionOffset)

	data += (number+0xC8).to_bytes(4,"big")

	mem = 0x805211CC+0x32*50

	data += mem.to_bytes(4,"big")
	data += (mem-0x15E9).to_bytes(4,"big")
	data += (mem-0x15D8).to_bytes(4,"big")
	data += (mem+0x10).to_bytes(4,"big")
	data += (mem+0x22).to_bytes(4,"big")
	data += (mem-0x15C9).to_bytes(4,"big")
	data += (mem-0x15BB).to_bytes(4,"big")

	data += midiInfo[4].to_bytes(1,"big")+bytes(3)
	data += midiInfo[2].to_bytes(4,"big")
	data += midiInfo[3].to_bytes(4,"big")
	data += (0xC0).to_bytes(4,"big") #?
	data += (0x00010000).to_bytes(4,"big")
	data += int("3F 37 4B C7 3F 5D F3 B6 3F 80 00 00 3F 93 33 33 3F A6 66 66".replace(" ",""),16).to_bytes(0x14,"big") #?
	data += bytes(4)
	data += brseqNumber.to_bytes(4,"big")
	data += (brseqNumber+1).to_bytes(4,"big")
	data += (0x00010102).to_bytes(4,"big") #?
	data += (0x01010000).to_bytes(4,"big")
	data += int("00 00 00 08 00 00 00 1C 00 00 00 2C 00 00 00 3C 00 00 00 50 00 00 00 60".replace(" ",""),16).to_bytes(0x18,"big") #?
	data += (0x03E7).to_bytes(4,"big")
	data += int("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 01 00 00 00 02 00 00 00 00 00 00 00 02 00 00 00 02 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 08 FF FF FF FF 00 00 00 74".replace(" ",""),16).to_bytes(0x44,"big") #?

	dol.seek(positionOffset+0xBC)
	data += dol.read()
	dol.close()

	dol = open(GetMainDolPath(),"wb")
	dol.write(data)
	dol.close()

def dataPath(file,*argv):
	file.seek(argv[0])
	root = int.from_bytes(file.read(4),"big")
	file.seek(root+argv[1])
	if(len(argv) > 2):
		for i in range(2,len(argv)):
			file.seek(root+argv[i]+8+int.from_bytes(file.read(4),"big"))
	return root+int.from_bytes(file.read(4),"big")+8

def dataPathPoint(file,*argv):
	file.seek(argv[0])
	root = int.from_bytes(file.read(4),"big")
	file.seek(root+argv[1])
	if(len(argv) > 2):
		for i in range(2,len(argv)):
			file.seek(root+argv[i]+8+int.from_bytes(file.read(4),"big"))
	return file.tell()

def FixMessageFile(textlines):
	nameIndex = romLanguageNumber[regionSelected]+(4+max(regionSelected-1,0))*(regionSelected > 1)
	for num in range(len(textlines)):
		if(textlines[num] == b'  b200 @015f /\r\n'):
			textlines[num] = b'  b200 @015f [/,4b] = '+["Default","Par défaut","Predeterm.","Standard","Normale","オリジナル","오리지널"][nameIndex].encode("utf-8")+b'\r\n'
			textlines[num+1] = b'  b201 @0160 [/,4b] = '+["Rock","Rock","Rock","Rock","Rock","ロック","록"][nameIndex].encode("utf-8")+b'\r\n'
			textlines[num+2] = b'  b202 @0161 [/,4b] = '+["March","Marche","Marcha","Marsch","Marcia","マーチ","행진곡"][nameIndex].encode("utf-8")+b'\r\n'
			textlines[num+3] = b'  b203 @0162 [/,4b] = '+["Jazz","Jazz","Jazz","Jazz","Jazz","ジャズ","재즈"][nameIndex].encode("utf-8")+b'\r\n'
			textlines[num+4] = b'  b204 @0163 [/,4b] = '+["Latin","Latino","Latino","Latin","Latino","ラテン","라틴 음악"][nameIndex].encode("utf-8")+b'\r\n'
			textlines[num+5] = b'  b205 @0164 [/,4b] = '+["Reggae","Reggae","Reggae","Reggae","Reggae","レゲエ","레게"][nameIndex].encode("utf-8")+b'\r\n'
			textlines[num+6] = b'  b206 @0165 [/,4b] = '+["Hawaiian","Hawaïen","Hawaiano","Hawaii","Hawaiano","ハワイ風","하와이 음악"][nameIndex].encode("utf-8")+b'\r\n'
			textlines[num+7] = b'  b207 @0166 [/,4b] = '+["Electronic","Électronique","Electrónico","Elektronik","Elettronico","ダウンビート","전자 음악"][nameIndex].encode("utf-8")+b'\r\n'
			textlines[num+8] = b'  b208 @0167 [/,4b] = '+["Classical","Classique","Clásico","Klassisch","Classico","室内楽","실내악"][nameIndex].encode("utf-8")+b'\r\n'
			textlines[num+9] = b'  b209 @0168 [/,4b] = '+["Tango","Tango","Tango","Tango","Tango","タンゴ","탱고"][nameIndex].encode("utf-8")+b'\r\n'
			textlines[num+10] = b'  b20a @0169 [/,4b] = '+["Pop","Pop","Pop","Pop","Pop","ポップス","팝"][nameIndex].encode("utf-8")+b'\r\n'
			textlines[num+11] = b'  b20b @016a [/,4b] = '+["Japanese","Japonais","Japonés","Japanisch","Giapponese","和風","일본 음악"][nameIndex].encode("utf-8")+b'\r\n'
			break
	return textlines

def PatchMainDol(dolPath="",geckoPath=""):
	if(dolPath == ""):
		dolPath = GetMainDolPath()
		if(not os.path.exists(dolPath+".backup")): copyfile(dolPath,dolPath+".backup")
		
	if(geckoPath == ""): geckoPath = GetGeckoPath()

	gct = False
	if(pathlib.Path(geckoPath).suffix != ".gct"):
		CreateGct(SavePath()+"/"+BasedOnRegion(gameIds)+".gct",geckoPath)
		geckoPath = SavePath()+"/"+BasedOnRegion(gameIds)+".gct"
		gct = True
	Run([HelperPath()+'/Wiimms/wstrt','patch',dolPath,'--add-section',geckoPath,'--force'])
	if(gct): os.remove(geckoPath)

def GetFileType():
	if(os.path.isdir(file.path)): return LoadType.Rom
	else:
		extension = pathlib.Path(file.path).suffix
		if(extension == ".brsar"): return LoadType.Brsar
		elif(extension == ".carc"): return LoadType.Carc
		elif(extension == ".midi" or extension == ".mid" or extension == ".brseq" or extension == ".rseq"): return LoadType.Midi
		elif(extension == ".dol"): return LoadType.Dol
		elif(extension == ".gct" or extension == ".ini"): return LoadType.Gct
		elif(extension == ".wbfs" or extension == ".iso"): return LoadType.RomFile

def PrepareFile():
	global file
	global regionSelected
	file.type = GetFileType()
	if(file.type == LoadType.RomFile): ConvertRom()
	if(file.type == LoadType.Rom): regionSelected = GetRegion()
	if(file.type == LoadType.Rom or file.type == LoadType.Carc): GetSongNames()

def ConvertRom():
	try:
		Run([HelperPath()+'/Wiimms/wit','cp','--fst',file.path,os.path.dirname(file.path)+"/"+os.path.splitext(os.path.basename(file.path))[0]])
		if(os.path.isdir(os.path.dirname(file.path).replace('\\','/')+'/'+os.path.splitext(os.path.basename(file.path))[0]+'/DATA')):
			file.path = os.path.dirname(file.path).replace('\\','/')+'/'+os.path.splitext(os.path.basename(file.path))[0]+'/DATA'
		else:
			file.path = os.path.dirname(file.path).replace('\\','/')+'/'+os.path.splitext(os.path.basename(file.path))[0]
		file.type = LoadType.Rom
	except Exception as e:
		ShowError("Could not extract rom",str(e))

def LoadSetting(section,key,default):
	ini = ConfigParser()
	ini.read(SavePath()+'/settings.ini')
	if(ini.has_option(section, key)):
		if(type(default) == str):
			return ini[section][key]
		else:
			if(ini[section][key] == "True"): return True
			elif(ini[section][key] == "False"): return False
			return int(ini[section][key])
	else:
		return default

def SaveSetting(section,key,value):
	ini = ConfigParser()
	ini.read(SavePath()+'/settings.ini')
	if(not ini.has_section(section)):
		ini.add_section(section)
	ini.set(section,key,str(value))
	with open(SavePath()+'/settings.ini', 'w') as inifile:
		ini.write(inifile)

def SaveRecording(action,name,values,remove=False):
	if(file.type == LoadType.Rom):
		if(type(values[0]) != list):
			values = [values]
		section = action+"-"+str(name)
		ini = ConfigParser()
		ini.read(file.path+"/Changes.ini")
		if(ini.has_section(section)): ini.remove_section(section)
		if(not remove):
			ini.add_section(section)
			for value in values:
				ini.set(section,value[0],str(value[1]))
		with open(file.path+"/Changes.ini", 'w') as inifile:
			ini.write(inifile)

def GetDolphinSave():
	if(os.path.isdir(dolphinSavePath)): return dolphinSavePath
	if(os.path.exists(os.path.dirname(dolphinPath)+"/portable.txt") and currentSystem == "Windows"): return os.path.dirname(dolphinPath)+"/User"
	return ChooseFromOS([os.path.expanduser('~/Documents/Dolphin Emulator'),os.path.expanduser('~/Library/Application Support/Dolphin'),os.path.expanduser('~/.local/share/dolphin-emu')])
		
#OS Specific
def ChooseFromOS(array):
	if(currentSystem == "Windows"): return array[0]
	elif(currentSystem == "Mac"): return array[1]
	else: return array[2]

def SavePath():
	path = ChooseFromOS([os.path.expanduser('~/AppData/Local/WiiMusicEditorPlus'),os.path.expanduser('~/Library/Application Support/WiiMusicEditorPlus'),os.path.expanduser('~/.local/share/WiiMusicEditorPlus')])
	if(not os.path.isdir(path)): os.mkdir(path)
	return path

def HelperPath():
	if getattr(sys, 'frozen', False):
		return sys._MEIPASS+"/Helper"
	else:
		return ProgramPath+"/crossplatformhelpers/"+currentSystem+"/Helper"

def TranslationPath():
	if getattr(sys, 'frozen', False):
		return sys._MEIPASS+"/translations"
	else:
		return ProgramPath+"/translations/translations"

def getData(file,point):
	file.seek(point)
	return int.from_bytes(file.read(4),"big")

#Brsar Helper
syO = 0x10
inO = 0x18
sdO = 0x0C
sbO = 0x14
piO = 0x1C
ctO = 0x24
grO = 0x2C
scO = 0x34


#Other Constants
textFromTxt = []
loadedStyles = [[]]*len(Styles)
rseqList = [0x3364C,0x336B8,0x33744,0x343F0,0x343F8,0x359FC,0x35A04,0x35A68,0x35A70,0x35AD4,0x35ADC,0x35B40,0x35B48,0x35BCC,0x35BD4,0x35C38,0x35C40,0x35CA4,0x35CAC,0x35D30,0x35D38,0x35DBC,0x35DC4,0x35E28,0x35E30,0x35EB4,0x35EBC,0x35F20,0x35F28,0x35F8C,0x35F94,0x36018,0x36020,0x36064,0x3606C,0x360D0,0x360D8,0x3705C,0x37064,0x370E8,0x370F0,0x371F4,0x371FC,0x37340,0x37348,0x376CC,0x376D4,0x37738,0x37740,0x3374C,0x37784,0x3778C,0x379D0,0x379D8,0x37ABC,0x37AC4,0x37B48,0x37B50,0x37BB4,0x37BBC,0x37C20,0x37C28,0x37C8C,0x37C94,0x37D18,0x37D20,0x37D64,0x37D6C,0x37E70,0x37E78,0x37EBC,0x37EC4,0x37F48,0x37F50]
rseqInfoList = [0x8,0x1C,0x20]
languageList = ["en","fr","sp","ge","it","jp","kr"]
regionNames = [["US","FU","SU"],["EN","FR","SP","GE","IT"],["JP"],["KR"]]
regionFullNames = ["US","Europe","Japan","Korea"]
gameIds = ["R64E01","R64P01","R64J01","R64K01"]
savePathIds = ["52363445","52363450","5236344a","5236344b"]
gctRegionOffsets = [0,0x200,-0x35F0,-0x428E8]
gctRegionOffsetsStyles = [0,0x200,-0x3420,-0x25320]
currentSystem = platform.system()
if(currentSystem == "Darwin"): currentSystem = "Mac"
firstStart = not os.path.isfile(SavePath()+"/settings.ini")

romLanguage = []
romLanguageNumber = [LoadSetting("Settings","RomLanguage",0)]*4
for i in range(4):
	try:
		if(romLanguageNumber[i] >= len(regionNames[i])):
			romLanguageNumber[i] = 0
		romLanguage.append(regionNames[i][romLanguageNumber[i]])
	except Exception as e:
		SaveSetting("Settings","RomLanguage",0)
		romLanguageNumber[i] = 0
		romLanguage.append(regionNames[i][0])

if getattr(sys, 'frozen', False):
	if(sys.platform == "darwin"):
		ProgramPath = os.path.dirname(pathlib.PosixPath(os.path.dirname(sys.executable)).parent.parent)
		FullPath = os.path.dirname(pathlib.PosixPath(os.path.dirname(sys.executable)).parent)
	else:
		ProgramPath = os.path.dirname(sys.executable)
		FullPath = sys.executable
else:
	ProgramPath = os.path.dirname(os.path.abspath(__file__))
	FullPath = "NULL"

#Variables
unsafeMode = LoadSetting("Settings","UnsafeMode",False)
regionSelected = LoadSetting("Settings","DefaultRegion",0)
dolphinPath = LoadSetting("Paths","Dolphin","")
if(currentSystem == "Linux" and not os.path.isfile(dolphinPath)):
	try:
		temp = subprocess.check_output("whereis dolphin-emu",shell=True).decode()
		if(os.path.exists(temp[13:len(temp)-1:1])):
			dolphinPath = temp[13:len(temp)-1:1]
			SaveSetting("Paths","Dolphin",dolphinPath)
	except:
		dolphinPath = ""
dolphinSavePath = LoadSetting("Paths","DolphinSave","")
file = LoadedFile(LoadSetting("Paths","CurrentLoadedFile",""),None)
if(not os.path.exists(file.path)): file.path = ""
from errorhandler import ShowError

version = "1.0.0"