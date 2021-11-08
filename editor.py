#Imports
import os
import sys
import platform
import subprocess
import pathlib
import tempfile
from shutil import copyfile, rmtree
from math import floor, ceil
import mido
from configparser import ConfigParser
from getpass import getuser
import stat as stats

#Classes
class SongClass:
	def __init__(self,SongType,Name,MemOrder,MemOffset = -1):
		self.SongType = SongType
		self.Name = Name
		self.MemOrder = MemOrder
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
	def __init__(self,Name,Number,InMenu,NumberOfSounds):
		self.Name = Name
		self.Number = Number
		self.InMenu = InMenu
		self.NumberOfSounds = NumberOfSounds

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

Songs = [
SongClass(SongTypeValue.Regular,'A Little Night Music',6),
SongClass(SongTypeValue.Regular,'American Patrol',11),
SongClass(SongTypeValue.Regular,'Animal Crossing',48),
SongClass(SongTypeValue.Regular,'Animal Crossing -- K.K. Blues',26),
SongClass(SongTypeValue.Regular,'Bridal Chorus',1),
SongClass(SongTypeValue.Regular,'Carmen',3),
SongClass(SongTypeValue.Regular,'Chariots of Fire',35),
SongClass(SongTypeValue.Regular,'Daydream Believer',33),
SongClass(SongTypeValue.Regular,'Do-Re-Mi',9),
SongClass(SongTypeValue.Regular,'Every Breath You Take',34),
SongClass(SongTypeValue.Regular,'F-Zero -- Mute City Theme',49),
SongClass(SongTypeValue.Regular,'Frère Jacques',22),
SongClass(SongTypeValue.Regular,'From Santurtzi to Bilbao',27),
SongClass(SongTypeValue.Regular,'From the New World',16),
SongClass(SongTypeValue.Regular,'Happy Birthday to You',8),
SongClass(SongTypeValue.Regular,'I\'ll Be There',40),
SongClass(SongTypeValue.Regular,'I\'ve Never Been to Me',44),
SongClass(SongTypeValue.Regular,'Jingle Bell Rock',41),
SongClass(SongTypeValue.Regular,'La Bamba',17),
SongClass(SongTypeValue.Regular,'La Cucaracha',29),
SongClass(SongTypeValue.Regular,'Little Hans',25),
SongClass(SongTypeValue.Regular,'Long, Long Ago',19),
SongClass(SongTypeValue.Regular,'Material Girl',38),
SongClass(SongTypeValue.Regular,'Minuet in G Major',7),
SongClass(SongTypeValue.Regular,'My Grandfather\'s Clock',15),
SongClass(SongTypeValue.Regular,'O Christmas Tree',24),
SongClass(SongTypeValue.Regular,'Ode to Joy',0),
SongClass(SongTypeValue.Regular,'Oh, My Darling Clementine',14),
SongClass(SongTypeValue.Regular,'Over the Waves',30),
SongClass(SongTypeValue.Regular,'Please Mr. Postman',37),
SongClass(SongTypeValue.Regular,'Sakura Sakura',31),
SongClass(SongTypeValue.Regular,'Scarborough Fair',18),
SongClass(SongTypeValue.Regular,'September',36),
SongClass(SongTypeValue.Regular,'Sukiyaki',32),
SongClass(SongTypeValue.Regular,'Super Mario Bros.',45),
SongClass(SongTypeValue.Regular,'Sur le pont d\'Avignon',21),
SongClass(SongTypeValue.Regular,'Swan Lake',2),
SongClass(SongTypeValue.Regular,'The Blue Danube',5),
SongClass(SongTypeValue.Regular,'The Entertainer',10),
SongClass(SongTypeValue.Regular,'The Flea Waltz',23),
SongClass(SongTypeValue.Regular,'The Legend of Zelda',46),
SongClass(SongTypeValue.Regular,'The Loco-Motion',39),
SongClass(SongTypeValue.Regular,'Troika',28),
SongClass(SongTypeValue.Regular,'Turkey in the Straw',12),
SongClass(SongTypeValue.Regular,'Twinkle, Twinkle, Little Star',20),
SongClass(SongTypeValue.Regular,'Wake Me Up Before You Go-Go',42),
SongClass(SongTypeValue.Regular,'Wii Music',4),
SongClass(SongTypeValue.Regular,'Wii Sports',47),
SongClass(SongTypeValue.Regular,'Woman',43),
SongClass(SongTypeValue.Regular,'Yankee Doodle',13),
SongClass(SongTypeValue.Maestro,'Twinkle, Twinkle, Little Star (Mii Maestro)',2,'025a3e1c'),
SongClass(SongTypeValue.Maestro,'Carmen (Mii Maestro)',0,'025a3d80'),
SongClass(SongTypeValue.Maestro,'The Four Seasons -- Spring (Mii Maestro)',4,'025a3f54'),
SongClass(SongTypeValue.Maestro,'Ode to Joy (Mii Maestro)',3,'025a3ff0'),
SongClass(SongTypeValue.Maestro,'The Legend of Zelda (Mii Maestro)',1,'025a3eb8'),
SongClass(SongTypeValue.Handbell,'O Christmas Tree (Handbell Harmony)',0,'02566D5A'),
SongClass(SongTypeValue.Handbell,'Hum, Hum, Hum (Handbell Harmony)',2,'02566E0A'),
SongClass(SongTypeValue.Handbell,'My Grandfather\'s Clock (Handbell Harmony)',3,'02566E62'),
SongClass(SongTypeValue.Handbell,'Do-Re-Mi (Handbell Harmony)',1,'02566DB2'),
SongClass(SongTypeValue.Handbell,'Sukiyaki (Handbell Harmony)',4,'02566EBA'),
SongClass(SongTypeValue.Menu,'Menu Song',-1,['0259ACB0','0259ACD4','0259ACF8','0259AD1C','0259AD40'])]

noneInstrument = 67
Styles = [
StyleClass(StyleTypeValue.Global,'Jazz','0659A65C','00',[28,2,0,16,42,45]),
StyleClass(StyleTypeValue.Global,'Rock','0659A680','01',[14,14,36,15,41,47]),
StyleClass(StyleTypeValue.Global,'Latin','0659A6A4','02',[27,28,1,15,43,46]),
StyleClass(StyleTypeValue.Global,'March','0659A6C8','03',[27,27,27,31,59,58]),
StyleClass(StyleTypeValue.Global,'Electronic','0659A6EC','04',[2,22,8,23,62,50]),
StyleClass(StyleTypeValue.Global,'Pop','0659A710','05',[0,2,13,15,40,47]),
StyleClass(StyleTypeValue.Global,'Japanese','0659A734','06',[29,noneInstrument,noneInstrument,20,56,51]),
StyleClass(StyleTypeValue.Global,'Tango','0659A758','07',[25,0,32,16,58,52]),
StyleClass(StyleTypeValue.Global,'Classical','0659A77C','08',[25,25,6,26,noneInstrument,noneInstrument]),
StyleClass(StyleTypeValue.Global,'Hawaiian','0659A7A0','09',[17,17,17,16,46,45]),
StyleClass(StyleTypeValue.Global,'Reggae','0659A7C4','0A',[3,3,0,15,64,noneInstrument]),
StyleClass(StyleTypeValue.SongSpecific,'A Little Night Music','0659AB00','21',[29,25,6,26,noneInstrument,noneInstrument]),
StyleClass(StyleTypeValue.SongSpecific,'Animal Crossing','0659AA28','1B',[32,18,13,13,46,45]),
StyleClass(StyleTypeValue.SongSpecific,'Animal Crossing K.K. Blues','0659AB48','23',[33,28,13,16,42,53]),
StyleClass(StyleTypeValue.SongSpecific,'Carmen','0659A878','0F',[35,32,13,16,59,46]),
StyleClass(StyleTypeValue.SongSpecific,'Chariots of Fire','0659A908','13',[0,13,6,7,58,46]),
StyleClass(StyleTypeValue.SongSpecific,'Every Breath You Take','0659A8E4','12',[33,0,22,15,40,47]),
StyleClass(StyleTypeValue.SongSpecific,'From Santurtzi to Bilbao','0659AADC','20',[3,3,3,3,50,47]),
StyleClass(StyleTypeValue.SongSpecific,'Happy Birthday to You','0659AA94','1E',[27,28,0,16,42,45]),
StyleClass(StyleTypeValue.SongSpecific,'I\'ll Be There','0659A974','16',[38,38,39,39,44,50]),
StyleClass(StyleTypeValue.SongSpecific,'I\'ve Never Been to Me','0659A9BC','18',[0,0,13,15,40,46]),
StyleClass(StyleTypeValue.SongSpecific,'La Cucaracha','0659AAB8','1F',[29,1,13,15,48,54]),
StyleClass(StyleTypeValue.SongSpecific,'Material Girl','0659A950','15',[36,14,22,23,60,47]),
StyleClass(StyleTypeValue.SongSpecific,'Minuet in G Major','0659AA4C','1C',[29,30,0,6,noneInstrument,noneInstrument]),
StyleClass(StyleTypeValue.SongSpecific,'O-Christmas Tree','0659A89C','10',[5,5,5,5,51,noneInstrument]),
StyleClass(StyleTypeValue.SongSpecific,'Oh My Darling Clementine','0659A830','0D',[36,36,9,36,58,52]),
StyleClass(StyleTypeValue.SongSpecific,'Over The Waves','0659A8C0','11',[32,30,6,16,53,47]),
StyleClass(StyleTypeValue.SongSpecific,'Scarborough Fair','0659A854','0E',[34,34,13,16,59,47]),
StyleClass(StyleTypeValue.SongSpecific,'September','0659A92C','14',[27,28,8,23,40,50]),
StyleClass(StyleTypeValue.SongSpecific,'Super Mario Bros','0659AC8C','2C',[37,37,37,37,noneInstrument,noneInstrument]),
StyleClass(StyleTypeValue.SongSpecific,'The Blue Danube','0659AB24','22',[30,25,4,31,58,52]),
StyleClass(StyleTypeValue.SongSpecific,'The Entertainer','0659AA70','1D',[0,6,0,16,42,46]),
StyleClass(StyleTypeValue.SongSpecific,'The Legend of Zelda','0659A9E0','19',[27,25,21,31,58,59]),
StyleClass(StyleTypeValue.SongSpecific,'Twinkle Twinkle Little Star','0659A7E8','0B',[0,1,13,16,51,52]),
StyleClass(StyleTypeValue.SongSpecific,'Wii Sports','0659AA04','1A',[29,0,13,15,60,47]),
StyleClass(StyleTypeValue.SongSpecific,'Wii Music','0659AB6C','24',[25,28,0,15,40,50]),
StyleClass(StyleTypeValue.SongSpecific,'Woman','0659A998','17',[28,27,13,15,40,49]),
StyleClass(StyleTypeValue.SongSpecific,'Yankee Doodle','0659A80C','0C',[33,24,18,16,49,46]),
StyleClass(StyleTypeValue.QuickJam,'A Capella','0659AC20','29',[38,38,39,39,66,50]),
StyleClass(StyleTypeValue.QuickJam,'Acoustic','0659AB90','38',[25,25,13,13,52,50]), #
StyleClass(StyleTypeValue.QuickJam,'African Electronic','0659AB93','3C',[25,25,13,13,52,50]), #
StyleClass(StyleTypeValue.QuickJam,'Animals!','0659AC68','2B',[11,11,10,31,59,49]),
StyleClass(StyleTypeValue.QuickJam,'Calypso','0659AC44','2A',[3,3,3,3,noneInstrument,noneInstrument]),
StyleClass(StyleTypeValue.QuickJam,'Exotic','0659ABFC','28',[19,19,4,19,55,noneInstrument]),
StyleClass(StyleTypeValue.QuickJam,'Flamenco','0659AB90','25',[25,25,13,13,52,50]), #
StyleClass(StyleTypeValue.QuickJam,'Galactic','0659ADD0','35',[25,25,13,13,52,50]), #
StyleClass(StyleTypeValue.QuickJam,'Handbell','0659AB93','43',[25,25,13,13,52,50]), #
StyleClass(StyleTypeValue.QuickJam,'Karate','0659ABB4','26',[14,14,14,15,41,63]),
StyleClass(StyleTypeValue.QuickJam,'Orchestral','0659AD64','32',[29,27,25,7,58,noneInstrument]),
StyleClass(StyleTypeValue.QuickJam,'Parade','0659ABD8','27',[27,30,27,31,65,57]),
StyleClass(StyleTypeValue.QuickJam,'Rap','0659ADF4','36',[12,noneInstrument,8,23,62,61]),
StyleClass(StyleTypeValue.QuickJam,'Samba','0659AE18','37',[29,1,13,15,65,48]),
StyleClass(StyleTypeValue.Menu,'Menu Style Main','0659ACB0','2D',[25,28,0,15,40,40]),
StyleClass(StyleTypeValue.Menu,'Menu Style Electronic','0659ACD4','2E',[2,22,0,23,62,40]),
StyleClass(StyleTypeValue.Menu,'Menu Style Japanese','0659ACF8','2F',[29,20,0,20,56,40]),
StyleClass(StyleTypeValue.Menu,'Menu Style March','0659AD1C','30',[30,27,0,31,58,40]),
StyleClass(StyleTypeValue.Menu,'Menu Style A Capella','0659AD40','31',[38,39,0,39,66,40])]

Instruments = [
InstrumentClass('Piano',0,True,["C2","G2","D3","A3","E4","B4","F#5","D6","F6"]),
InstrumentClass('Marimba',1,False,["G3","D4","A4","E5","B5","F#6"]),
InstrumentClass('Vibraphone',2,False,["F#3","C#4","G#4","D#5","A#5","F6"]),
InstrumentClass('Steel Drum',3,False,["F#2","A#3","F#4","G4","E4","??(26)","C4"]),
InstrumentClass('Dulcimer',4,False,["F3","C#4","G4","C5","A4","D6"]),
InstrumentClass('Handbell',5,False,["G4","G4 (Variation)","G4 (Variation 2)","C7"]),
InstrumentClass('Harpsichord',6,False,["G2","C4","C5","C6"]),
InstrumentClass('Timpani',7,False,["F3","F3 (Variation)","F3 (Variation 2)"]),
InstrumentClass('Galactic Piano',8,False,["G2","D3","A3","E4","B4","F#5"]),
InstrumentClass('Toy Piano',9,False,["B4","D6"]),
InstrumentClass('Dog',10,False,["Howl","??(54)","??(55)","??(54)","D5","G5","C#6"]),
InstrumentClass('Cat',11,False,["G3","C#4","G4","C#5","G5","C#6"]),
InstrumentClass('Rapper',12,False,["??"]*62),
InstrumentClass('Guitar',13,False,["G#2","E3","B3","F#4","D5","??(133)"]),
InstrumentClass('Electric Guitar',14,False,["A2","D3","B3","G4","E5","A5"]),
InstrumentClass('Electric Bass',15,True,["G1","D2","G2","C3","G#3"]),
InstrumentClass('Double Bass',16,False,["F1","G#1","G#2","G#3"]),
InstrumentClass('Ukulele',17,False,["B3","F#4","C#5","G#5"]),
InstrumentClass('Banjo',18,False,["A#2","F3","C4","G4","D5","A5"]),
InstrumentClass('Sitar',19,False,["C3","G3","C4","G4"]),
InstrumentClass('Shamisen',20,True,["D3","A3","D4","A4"]),
InstrumentClass('Harp',21,False,["C3","C4","E5","B5","G6"]),
InstrumentClass('Galactic Guitar',22,False,["F2","C3","F3","C4","F4","C5","F5"]),
InstrumentClass('Galactic Bass',23,True,["A1","C2","F2","A2","C3"]),
InstrumentClass('Jaw Harp',24,False,["??(184)","??(185)","??(186)","??(187)"]),
InstrumentClass('Violin',25,False,["C4","A4","E5","B5","F#6"]),
InstrumentClass('Cello',26,False,["A2","D3","A3","E4","B4"]),
InstrumentClass('Trumpet',27,True,["F#2","G#3","A3","D4","G4","C5","F5","Bb5","G6"]),
InstrumentClass('Saxophone',28,True,["F2","B2","F3","E4","Bb4","E5","Bb5","E6"]),
InstrumentClass('Flute',29,True,["D4","G4","C5","G5","D6","G6","D7"]),
InstrumentClass('Clairenet',30,True,["Bb2","F3","C4","F4","C5","F5","C6"]),
InstrumentClass('Tuba',31,False,["??(229)","Eb2","Bb2","A3"]),
InstrumentClass('Accordion',32,False,["B2","C4"]),
InstrumentClass('Harmonica',33,False,["B4","A3","E4","D5","B5","A6"]),
InstrumentClass('Bagpipe',34,False,["C4","F#4","C5","F#5"]),
InstrumentClass('Recorder',35,False,["G6"]),
InstrumentClass('Galactic horn',36,False,["G2","C4","C5"]),
InstrumentClass('Nes',37,False,["Mario Jump","C3","F3","Bb3","G4","C5","C6"]),
InstrumentClass('Singer',38,True,["C4 (Wii)","G4 (Wii)","C5 (Wii)","G5 (Wii)","C4 (Do)","F#4 (Do)","D5 (Do)","F#5 (Do)","C4 (Ba)","G4 (Ba)","C5 (Ba)","G5 (Ba)"]),
InstrumentClass('Bass Singer',39,True,["D3 (Wii)","G3 (Wii)","C4 (Wii)","G4 (Wii)","C3 (Do)","G3 (Do)","C4 (Do)","G4 (Do)","D3 (Ba)","A3 (Ba)","D4 (Ba)","G4 (Ba)"]),
InstrumentClass('Basic Drums',40,True,[]),
InstrumentClass('Rock Drums',41,False,[]),
InstrumentClass('Jazz Drums',42,False,[]),
InstrumentClass('Latin Drums',43,False,[]),
InstrumentClass('Ballad Drums',44,False,[]),
InstrumentClass('Congas',45,False,[]),
InstrumentClass('Maracas',46,False,[]),
InstrumentClass('Tambourine',47,False,[]),
InstrumentClass('Cuica',48,False,[]),
InstrumentClass('Cowbell',49,False,[]),
InstrumentClass('Clap',50,False,[]),
InstrumentClass('Bells',51,False,[]),
InstrumentClass('Castanets',52,False,[]),
InstrumentClass('Guiro',53,False,[]),
InstrumentClass('Timpales',54,False,[]),
InstrumentClass('Djembe',55,False,[]),
InstrumentClass('Taiko Drum',56,True,[]),
InstrumentClass('Cheerleader',57,False,[]),
InstrumentClass('Snare Drum',58,True,[]),
InstrumentClass('Bass Drum',59,False,[]),
InstrumentClass('Galactic Drums',60,False,[]),
InstrumentClass('Galactic Congas',61,False,[]),
InstrumentClass('DJ Turntables',62,True,[]),
InstrumentClass('Kung Fu Person',63,False,[]),
InstrumentClass('Reggae Drums',64,False,[]),
InstrumentClass('Whistle',65,False,[]),
InstrumentClass('Beatbox',66,True,[]),
InstrumentClass('None',-1,False,[])]

class LoadType:
	Rom = 0
	Brsar = 1
	Carc = 2
	Dol = 3
	Midi = 4
	Gct = 5
	RomFile = 6

#Functions

#Get File
def GetBrsarPath():
	if(os.path.isdir(file.path)):
		return file.path+"/files/Sound/MusicStatic/rp_Music_sound.brsar"
	else:
		return file.path

def GetMessagePath():
	if(os.path.isdir(file.path)):
		return file.path+"/files/"+BasedOnRegion(regionNames)+"/Message"
	else:
		return os.path.dirname(file.path)

def GetGeckoPath():
	if(os.path.isdir(file.path)):
		return file.path+"/GeckoCodes.ini"
	else:
		return file.path

def GivePermission(file):
	st = os.stat(file)
	os.chmod(file,st.st_mode | stats.S_IEXEC)

#Other
def Run(command):
	subprocess.run(command.replace("\\","/"))

def DecodeTxt():
	path = GetMessagePath()
	try:
		if(os.path.isdir(path+"/message.d")): rmtree(path+"/message.d")
		Run('"'+ProgramPath+'/Helper/Wiimms/wszst" extract "'+path+'/message.carc"')
		os.remove(path+"/message.d/wszst-setup.txt")
		Run('"'+ProgramPath+'/Helper/Wiimms/wbmgt" decode "'+path+'/message.d/new_music_message.bmg"')
		os.remove(path+"/message.d/new_music_message.bmg")
	except Exception as e:
		ShowError("Could not decode text file",str(e))

def EncodeTxt():
	path = GetMessagePath()
	try:
		Run('"'+ProgramPath+'/Helper/Wiimms/wbmgt" encode "'+path+'/message.d/new_music_message.txt"')
		os.remove(path+"/message.d/new_music_message.txt")
		os.remove(path+"/message.carc")
		Run('"'+ProgramPath+'/Helper/Wiimms/wszst" create "'+path+'/message.d" --dest "'+path+'/message.carc"')
		rmtree(path+'/message.d')
	except Exception as e:
		ShowError("Could not encode text file",str(e))

def GetRegion():
	for i in range(len(regionNames)):
		if(os.path.isdir(file.path+"/files/"+regionNames[i]+"/Message")):
			return i
	ShowError("Could not determine region","Using fallback region: "+BasedOnRegion(regionFullNames))
	return regionSelected

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
		for num in range(len(textlines)):
			if(textlines[num] == b'  b200 @015f /\r\n'):
				textlines[num] = b'  b200 @015f [/,4b] = Default\r\n'
				textlines[num+1] = b'  b201 @0160 [/,4b] = Rock\r\n'
				textlines[num+2] = b'  b202 @0161 [/,4b] = March\r\n'
				textlines[num+3] = b'  b203 @0162 [/,4b] = Jazz\r\n'
				textlines[num+4] = b'  b204 @0163 [/,4b] = Latin\r\n'
				textlines[num+5] = b'  b205 @0164 [/,4b] = Reggae\r\n'
				textlines[num+6] = b'  b206 @0165 [/,4b] = Hawaiian\r\n'
				textlines[num+7] = b'  b207 @0166 [/,4b] = Electronic\r\n'
				textlines[num+8] = b'  b208 @0167 [/,4b] = Classical\r\n'
				textlines[num+9] = b'  b209 @0168 [/,4b] = Tango\r\n'
				textlines[num+10] = b'  b20a @0169 [/,4b] = Pop\r\n'
				textlines[num+11] = b'  b20b @016a [/,4b] = Japanese\r\n'
				break
		for num in range(len(textlines)):
			if offset in str(textlines[num]):
				while bytes('@','utf-8') not in textlines[num+1]:
					textlines.pop(num+1)
				if(type(newText) == str):
					textlines[num] = bytes(offset+str(textlines[num])[10:24:1]+newText+'\r\n','utf-8')
				else:
					textlines[num] = bytes(offset+str(textlines[num])[10:24:1]+newText[typeNum]+'\r\n','utf-8')
				break
		message = open(txtPath+'/message.d/new_music_message.txt','wb')
		message.writelines(textlines)
		message.close()
		if(type(newText) == str): break
	EncodeTxt()

def CreateGct(path):
	patches = open(GetGeckoPath())
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

def ReplaceSong(positionOffset,listOffset,replacementArray,BrseqOrdering,BrseqInfoArray,BrseqLengthArray,BrsarPath):
	if(BrsarPath == -1): BrsarPath = GetBrsarPath()
	BrseqInfo = []
	BrseqLength = []
	for i in range(len(BrseqOrdering)):
		BrseqInfo.append(BrseqInfoArray[BrseqOrdering[i]])
		BrseqLength.append(BrseqLengthArray[BrseqOrdering[i]])
	sizeDifference = 0
	brsar = open(BrsarPath, "rb")
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
		for offset in rseqList:
			if(offset > positionOffset):
				brsar.seek(offset)
				size = brsar.read(4)
				brsar.seek(offset)
				brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
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
		for offset in rseqList:
			if(offset > positionOffset):
				brsar.seek(offset)
				size = brsar.read(4)
				brsar.seek(offset)
				brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
		for offset in [8,positionOffset+4]:
			brsar.seek(offset)
			size = brsar.read(4)
			brsar.seek(offset)
			brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
	brsar.close()

def ReplaceWave(startOffset,replaceNumber,rwavInfo,rwavSize,BrsarPath):
	sizeDifference = 0
	brsar = open(BrsarPath, "r+b")
	brsar.seek(startOffset)
	rwarSpot = int.from_bytes(brsar.read(4),'big')
	brsar.seek(rwarSpot+0x18)
	dataSection = rwarSpot+int.from_bytes(brsar.read(4),'big')
	brsar.seek(rwarSpot+0x10)
	table = rwarSpot+int.from_bytes(brsar.read(4),'big')
	brsar.seek(table+8)
	numberOfRwavs = int.from_bytes(brsar.read(4),'big')
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
		
	else:
		brsar.seek(table+0x10+0xC*replaceNumber)
		dataSpot = int.from_bytes(brsar.read(4),'big')
		dataSize = int.from_bytes(brsar.read(4),'big')
		sizeDifference = rwavSize-dataSize
		brsar.seek(table+0x10+0xC*replaceNumber+4)
		brsar.write(rwavSize.to_bytes(4, 'big'))
		for i in range(replaceNumber+1,numberOfRwavs):
			brsar.seek(table+0x10+0xC*i)
			offset = int.from_bytes(brsar.read(4),'big')
			brsar.seek(table+0x10+0xC*i)
			brsar.write((offset+sizeDifference).to_bytes(4, 'big'))
	for offset in [8,startOffset+4,rwarSpot+8]:
		brsar.seek(offset)
		size = brsar.read(4)
		brsar.seek(offset)
		brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
	for offset in rseqList:
		if(int(offset,16) > startOffset):
			brsar.seek(int(offset,16))
			size = brsar.read(4)
			brsar.seek(int(offset,16))
			brsar.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big'))
	brsar.seek(0)
	if(replaceNumber == -1):
		data1 = brsar.read(dataSection+dataSpot)
		brsar.seek(dataSection+dataSpot+rwavSize*numberOfRwavs-sizeDifference)
		data2 = brsar.read()
		brsar.close()
		brsar = open(BrsarPath, "wb")
		brsar.write(data1+rwavInfo*numberOfRwavs+data2)
	else:
		data1 = brsar.read(dataSection+dataSpot)
		brsar.seek(dataSection+dataSpot+dataSize)
		data2 = brsar.read()
		brsar.close()
		brsar = open(BrsarPath, "wb")
		brsar.write(data1+rwavInfo+data2)
	brsar.close()

def LoadMidi(midiPath):
	with tempfile.TemporaryDirectory() as directory:
		prefix = pathlib.Path(midiPath).suffix
		if(prefix == '.mid'): prefix = '.midi'
		copyfile(midiPath,directory+'/z'+prefix)
		if(os.path.isfile(directory+'/z.rseq')):
			Run('"'+ProgramPath+'/Helper/SequenceCmd/GotaSequenceCmd.exe" assemble "'+directory+'/z.rseq"')
		if(os.path.isfile(directory+'/z.brseq')):
			Run('"'+ProgramPath+'/Helper/SequenceCmd/GotaSequenceCmd.exe" to_midi "'+directory+'/z.brseq"')
		else:
			subprocess.run('"'+ProgramPath+'/Helper/SequenceCmd/GotaSequenceCmd.exe" from_midi "'+directory+'/z.midi"')

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



def PatchBrsar(SongSelected,BrseqInfo,BrseqLength,Tempo,Length,TimeSignature,BrsarPath=-1):
	Tempo = format(Tempo,"x")
	Length = format(Length,"x")
	LengthCode = '0'+format(Songs[SongSelected].MemOffset+BasedOnRegion(gctRegionOffsets)+6,'x').lower()+' '+'0'*(8-len(Length))+Length+'\n'
	TempoCode = '0'+format(Songs[SongSelected].MemOffset+BasedOnRegion(gctRegionOffsets)+10,'x').lower()+' '+'0'*(8-len(Tempo))+Tempo+'\n'
	TimeCode = '0'+format(Songs[SongSelected].MemOffset+BasedOnRegion(gctRegionOffsets),'x').lower()+' 00000'+str(TimeSignature)+'00\n'
	if(Songs[SongSelected].SongType == SongTypeValue.Regular):
		ReplaceSong(0x033744,0x033A84,[Songs[SongSelected].MemOrder*2,Songs[SongSelected].MemOrder*2+1,100],[0,1],BrseqInfo,BrseqLength,BrsarPath)
		AddPatch(Songs[SongSelected].Name+' Song Patch',LengthCode+TempoCode+TimeCode)
		if(Songs[SongSelected].Name == 'Do-Re-Mi'):
			ReplaceSong(0x0343F0,0x034988,[18,19,113,155,156,157,158,159,160,161,162,175],[0,1,0,0,0,0,0,0,0,0,0],BrseqInfo,BrseqLength,BrsarPath)
			ReplaceSong(0x0360D0,0x0364C8,[18,19,113,123],[0,1,0],BrseqInfo,BrseqLength,BrsarPath)
	elif(Songs[SongSelected].SongType == SongTypeValue.Menu):
		ReplaceSong(0x037D64,0x037DBC,[0,1,2,3,4,5,6,7],[0,1,1,1,1,1,1],BrseqInfo,BrseqLength,BrsarPath)
	elif(Songs[SongSelected].SongType == SongTypeValue.Maestro):
		ReplaceSong(0x0370E8,0x037140,[Songs[SongSelected].MemOrder+2,7],[0],BrseqInfo,BrseqLength,BrsarPath)
		AddPatch(Songs[SongSelected].Name+' Song Patch',LengthCode+TempoCode+TimeCode)
	elif(Songs[SongSelected].SongType == SongTypeValue.Handbell):
		ReplaceSong(0x037340,0x037438,[Songs[SongSelected].MemOrder*5+2,Songs[SongSelected].MemOrder*5+3,Songs[SongSelected].MemOrder*5+4,Songs[SongSelected].MemOrder*5+5,Songs[SongSelected].MemOrder*5+6,27],[0,0,0,0,0],BrseqInfo,BrseqLength,BrsarPath)
		LengthCode = '0'+format(Songs[SongSelected].MemOffset+BasedOnRegion(gctRegionOffsets),'x').lower()+' '+'0'*(8-len(Length))+Length+'\n'
		LengthCode2 = '0'+format(Songs[SongSelected].MemOffset+BasedOnRegion(gctRegionOffsets)+4,'x').lower()+' '+'0'*(8-len(Length))+Length+'\n'
		MeasureCode = '0'+format(Songs[SongSelected].MemOffset+BasedOnRegion(gctRegionOffsets)+24,'x').lower()+' '+'00000000\n'
		AddPatch(Songs[SongSelected].Name+' Song Patch',LengthCode+LengthCode2+MeasureCode)

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
		GivePermission(ProgramPath+'/Helper/Wiimms/wit')
		Run('\"'+ProgramPath+'/Helper/Wiimms/wit\" cp --fst \"'+file.path+'\" \"'+os.path.dirname(file.path)+"/"+os.path.splitext(os.path.basename(file.path))[0]+'\" \"'+file.path+'\" \"'+os.path.dirname(file.path)+"/"+os.path.splitext(os.path.basename(file.path))[0]+'\"')
		if(os.path.isdir(os.path.dirname(file.path).replace('\\','/')+'/'+os.path.splitext(os.path.basename(file.path))[0]+'/DATA')):
			file.path = os.path.dirname(file.path).replace('\\','/')+'/'+os.path.splitext(os.path.basename(file.path))[0]+'/DATA'
		else:
			file.path = os.path.dirname(file.path).replace('\\','/')+'/'+os.path.splitext(os.path.basename(file.path))[0]
		file.type = LoadType.Rom
	except Exception as e:
		ShowError("Could not extract rom",str(e))

def LoadSetting(section,key,default):
	ini = ConfigParser()
	ini.read(ProgramPath+'/settings.ini')
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
	ini.read(ProgramPath+'/settings.ini')
	if(not ini.has_section(section)):
		ini.add_section(section)
	ini.set(section,key,str(value))
	with open(ProgramPath+'/settings.ini', 'w') as inifile:
		ini.write(inifile)

def GetDolphinSave():
	if(os.path.isdir(dolphinSavePath)): return dolphinSavePath
	if(os.path.exists(os.path.dirname(dolphinSavePath)+"/portable.txt")): return os.path.dirname(dolphinSavePath)+"/User"
	return "C:/Users/"+getuser()+"/Documents/Dolphin Emulator"
		
#OS Specific
def ChooseFromOS(array):
	if(currentSystem == "Windows"): return array[0]
	elif(currentSystem == "Mac"): return array[1]
	else: return array[2]

#Constants
textFromTxt = []
loadedStyles = [[]]*len(Styles)
rseqList = [0x3364C,0x336B8,0x33744,0x343F0,0x343F8,0x359FC,0x35A04,0x35A68,0x35A70,0x35AD4,0x35ADC,0x35B40,0x35B48,0x35BCC,0x35BD4,0x35C38,0x35C40,0x35CA4,0x35CAC,0x35D30,0x35D38,0x35DBC,0x35DC4,0x35E28,0x35E30,0x35EB4,0x35EBC,0x35F20,0x35F28,0x35F8C,0x35F94,0x36018,0x36020,0x36064,0x3606C,0x360D0,0x360D8,0x3705C,0x37064,0x370E8,0x370F0,0x371F4,0x371FC,0x37340,0x37348,0x376CC,0x376D4,0x37738,0x37740,0x3374C,0x37784,0x3778C,0x379D0,0x379D8,0x37ABC,0x37AC4,0x37B48,0x37B50,0x37BB4,0x37BBC,0x37C20,0x37C28,0x37C8C,0x37C94,0x37D18,0x37D20,0x37D64,0x37D6C,0x37E70,0x37E78,0x37EBC,0x37EC4,0x37F48,0x37F50]
regionNames = ["US","EN","JP","KR"]
regionFullNames = ["US","Europe","Japan","Korea"]
gameIds = ["R64E01","R64P01","R64J01","R64K01"]
savePathIds = ["52363445","52363450","5236344a","5236344b"]
gctRegionOffsets = [0,0x200,-0x35F0,-0x428E8]
currentSystem = platform.system()
if(currentSystem == "Darwin"): currentSystem = "Mac"

if(sys.platform == "darwin"):
	import Cocoa
	ProgramPath = os.path.dirname(Cocoa.NSBundle.mainBundle().bundlePath())
elif getattr(sys, 'frozen', False): ProgramPath = os.path.dirname(sys.executable)
else: ProgramPath = os.path.dirname(os.path.abspath(__file__))

#Variables
unsafeMode = LoadSetting("Settings","UnsafeMode",False)
regionSelected = LoadSetting("Settings","DefaultRegion",0)
dolphinPath = LoadSetting("Paths","Dolphin","")
dolphinSavePath = LoadSetting("Paths","DolphinSave","")
file = LoadedFile(LoadSetting("Paths","CurrentLoadedFile",""),None)
if(not os.path.exists(file.path)): file.path = ""
if(file.path != ""):
	try:
		PrepareFile()
	except:
		file.path = ""
from errorhandler import ShowError