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






class LoadedFile:
	def __init__(self,path,type):
		self.path = path
		self.type = type


RetranslateSongNames()



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




#Other





			

#Main Functions






)

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
		if(load_setting("Settings","ResampleSounds",True)):
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










#Variables
unsafeMode = load_setting("Settings","UnsafeMode",False)

version = "1.0.3"