from wii_music_editor import AddPatch
from wii_music_editor import BasedOnRegion
from wii_music_editor.utils.save import load_setting


#Brsar Helper
    syO = 0x10
    inO = 0x18
    sdO = 0x0C
    sbO = 0x14
    piO = 0x1C
    ctO = 0x24
    grO = 0x2C
    scO = 0x34

rseqList = [0x3364C,0x336B8,0x33744,0x343F0,0x343F8,0x359FC,0x35A04,0x35A68,0x35A70,0x35AD4,0x35ADC,0x35B40,0x35B48,0x35BCC,0x35BD4,0x35C38,0x35C40,0x35CA4,0x35CAC,0x35D30,0x35D38,0x35DBC,0x35DC4,0x35E28,0x35E30,0x35EB4,0x35EBC,0x35F20,0x35F28,0x35F8C,0x35F94,0x36018,0x36020,0x36064,0x3606C,0x360D0,0x360D8,0x3705C,0x37064,0x370E8,0x370F0,0x371F4,0x371FC,0x37340,0x37348,0x376CC,0x376D4,0x37738,0x37740,0x3374C,0x37784,0x3778C,0x379D0,0x379D8,0x37ABC,0x37AC4,0x37B48,0x37B50,0x37BB4,0x37BBC,0x37C20,0x37C28,0x37C8C,0x37C94,0x37D18,0x37D20,0x37D64,0x37D6C,0x37E70,0x37E78,0x37EBC,0x37EC4,0x37F48,0x37F50]
rseqInfoList = [0x8,0x1C,0x20]


def getData(file,point):
	file.seek(point)
	return int.from_bytes(file.read(4),"big")


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
		if(offset > startoffset):
			file.seek(offset)
			size = file.read(4)
			file.seek(offset)
			file.write((int.from_bytes(size,"big")+sizeDifference).to_bytes(4, 'big')


def PatchBrsar(SongSelected, BrseqInfo, BrseqLength, Tempo, Length, TimeSignature):
    if (load_setting("Setting", "RapperFix", True)):
        AddPatch('Rapper Crash Fix', BasedOnRegion([
            '043b0bc0 60000000\n043b0bec 4e800020\n',
            '043B0CCF 881C0090\n043B0CD3 7C090000\n043B0BC3 4081FFBC\n043B0CD7 881C00D6\n',
            '043AE47F 881C0090\n043AE483 7C090000\n043AE487 4081FFBC\n043AE48B 881C00D6\n',
            '0429CE7B 881C0090\n0429CE7F 7C090000\n0429CE83 4081FFBC\n0429CE87 881C00D6\n']))
    if (Songs[SongSelected].SongType != SongTypeValue.Menu):
        Tempo = format(Tempo, "x")
        Length = format(Length, "x")
        LengthCode = '0' + format(Songs[SongSelected].MemOffset + BasedOnRegion(gctRegionOffsets) + 6,
                                  'x').lower() + ' ' + '0' * (8 - len(Length)) + Length + '\n'
        TempoCode = '0' + format(Songs[SongSelected].MemOffset + BasedOnRegion(gctRegionOffsets) + 10,
                                 'x').lower() + ' ' + '0' * (8 - len(Tempo)) + Tempo + '\n'
        TimeCode = '0' + format(Songs[SongSelected].MemOffset + BasedOnRegion(gctRegionOffsets),
                                'x').lower() + ' 00000' + str(TimeSignature) + '00\n'
    if (Songs[SongSelected].SongType == SongTypeValue.Regular):
        ReplaceSong(2, [Songs[SongSelected].MemOrder * 2, Songs[SongSelected].MemOrder * 2 + 1], [0, 1], BrseqInfo,
                    BrseqLength)
        AddPatch(Songs[SongSelected].Name + ' Song Patch', LengthCode + TempoCode + TimeCode)
        if (Songs[SongSelected].Name == 'Do-Re-Mi'):
            ReplaceSong(3, [18, 19, 113, 155, 156, 157, 158, 159, 160, 161, 162], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        BrseqInfo, BrseqLength)
            ReplaceSong(19, [18, 19, 113], [0, 1, 0], BrseqInfo, BrseqLength)
    elif (Songs[SongSelected].SongType == SongTypeValue.Menu):
        ReplaceSong(34, [0, 1, 2, 3, 4, 5, 6], [0, 1, 1, 1, 1, 1, 1], BrseqInfo, BrseqLength)
    elif (Songs[SongSelected].SongType == SongTypeValue.Maestro):
        ReplaceSong(21, [Songs[SongSelected].MemOrder + 2], [0], BrseqInfo, BrseqLength)
        AddPatch(Songs[SongSelected].Name + ' Song Patch', LengthCode + TempoCode + TimeCode)
    elif (Songs[SongSelected].SongType == SongTypeValue.Handbell):
        ReplaceSong(23, [Songs[SongSelected].MemOrder * 5 + 2, Songs[SongSelected].MemOrder * 5 + 3,
                         Songs[SongSelected].MemOrder * 5 + 4, Songs[SongSelected].MemOrder * 5 + 5,
                         Songs[SongSelected].MemOrder * 5 + 6], [0, 0, 0, 0, 0], BrseqInfo, BrseqLength)
        LengthCode = '0' + format(Songs[SongSelected].MemOffset + BasedOnRegion(gctRegionOffsets),
                                  'x').lower() + ' ' + '0' * (8 - len(Length)) + Length + '\n'
        LengthCode2 = '0' + format(Songs[SongSelected].MemOffset + BasedOnRegion(gctRegionOffsets) + 4,
                                   'x').lower() + ' ' + '0' * (8 - len(Length)) + Length + '\n'
        MeasureCode = '0' + format(Songs[SongSelected].MemOffset + BasedOnRegion(gctRegionOffsets) + 24,
                                   'x').lower() + ' ' + '00000000\n'
        AddPatch(Songs[SongSelected].Name + ' Song Patch', LengthCode + LengthCode2 + MeasureCode)

def ReplaceWave(startOffset, replaceNumber, rwavInfo, rwavSize):
    if (not os.path.exists(GetBrsarPath() + ".backup")): copyfile(GetBrsarPath(), GetBrsarPath() + ".backup")
    sizeDifference = 0
    brsar = open(GetBrsarPath(), "r+b")
    brsar.seek(startOffset)
    rwarSpot = int.from_bytes(brsar.read(4), 'big')
    brsar.seek(rwarSpot + 0x18)
    dataSection = rwarSpot + int.from_bytes(brsar.read(4), 'big')
    brsar.seek(rwarSpot + 0x10)
    table = rwarSpot + int.from_bytes(brsar.read(4), 'big')
    brsar.seek(table + 8)
    numberOfRwavs = int.from_bytes(brsar.read(4), 'big')
    if (numberOfRwavs == len(replaceNumber)): replaceNumber = -1
    if (replaceNumber == -1):
        for i in range(numberOfRwavs):
            brsar.seek(table + 0x10 + 0xC * i)
            tempdataSpot = int.from_bytes(brsar.read(4), 'big')
            if (i == 0): dataSpot = tempdataSpot
            dataSize = int.from_bytes(brsar.read(4), 'big')
            brsar.seek(table + 0x10 + 0xC * i)
            offset = int.from_bytes(brsar.read(4), 'big')
            brsar.seek(table + 0x10 + 0xC * i)
            brsar.write((offset + sizeDifference).to_bytes(4, 'big'))
            brsar.seek(table + 0x10 + 0xC * i)
            brsar.write((tempdataSpot + sizeDifference).to_bytes(4, 'big'))
            sizeDifference += rwavSize - dataSize
            brsar.seek(table + 0x10 + 0xC * i + 4)
            brsar.write(rwavSize.to_bytes(4, 'big'))
        brsar.seek(0)
        data1 = brsar.read(dataSection + dataSpot)
        brsar.seek(dataSection + dataSpot + rwavSize * numberOfRwavs - sizeDifference)
        data2 = brsar.read()
        brsar.seek(0)
        brsar.write(data1 + rwavInfo * numberOfRwavs + data2)
        brsar.truncate()
    else:
        for i in replaceNumber:
            brsar.seek(table + 0x10 + 0xC * i)
            dataSpot = int.from_bytes(brsar.read(4), 'big')
            dataSize = int.from_bytes(brsar.read(4), 'big')
            sizeDifference += rwavSize - dataSize
            brsar.seek(table + 0x10 + 0xC * i + 4)
            brsar.write(rwavSize.to_bytes(4, 'big'))
            brsar.seek(0)
            data1 = brsar.read(dataSection + dataSpot)
            brsar.seek(dataSection + dataSpot + dataSize)
            data2 = brsar.read()
            brsar.seek(0)
            brsar.write(data1 + rwavInfo + data2)
            brsar.truncate()
            for j in range(i + 1, numberOfRwavs):
                brsar.seek(table + 0x10 + 0xC * j)
                offset = int.from_bytes(brsar.read(4), 'big')
                brsar.seek(table + 0x10 + 0xC * j)
                brsar.write((offset + rwavSize - dataSize).to_bytes(4, 'big'))

    for offset in [8, startOffset + 4, rwarSpot + 8]:
        brsar.seek(offset)
        size = brsar.read(4)
        brsar.seek(offset)
        brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))
    for offset in rseqList:
        if (offset > startOffset):
            brsar.seek(offset)
            size = brsar.read(4)
            brsar.seek(offset)
            brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))
    brsar.close()


def BrsarGetList(file, positionOffset):
    return getData(file, inO) + 0x10 + getData(file, positionOffset + 0x14) + getData(file, positionOffset + 0x18) * 8


def GetTableOffset(file, num):
    return dataPath(file, inO, grO, 0x8 * (num + 1))


def printh(num): print(format(num, "x"))


def BrseqAddingName(text):
    brsar = open(GetBrsarPath(), "r+b")
    sizeDifference = 4 * len(text)
    for i in range(len(text)):
        text[i] = text[i].encode("utf-8")
        if (i != len(text) - 1): text[i] += bytes(1)
        sizeDifference += len(text[i])

    offset = dataPath(brsar, syO, 0x0C) - 1
    brsar.seek(offset)
    extra = 0
    while (int.from_bytes(brsar.read(1), "big") == 0):
        extra += 1
        brsar.seek(offset - extra)
    positionOffset = offset + 1
    text[len(text) - 1] += bytes(4 - ((sizeDifference - extra) % 4) - 1)
    sizeDifference += 4 - ((sizeDifference - extra) % 4) - 1

    number = getData(brsar, dataPath(brsar, syO, 0x8))
    brsar.seek(dataPath(brsar, syO, 0x8))
    brsar.write((number + len(text)).to_bytes(4, 'big'))

    # Other Name Offsets
    for i in range(number):
        offset = dataPath(brsar, syO, 0x8) + 4 * (i + 1)
        brsar.seek(offset)
        size = brsar.read(4)
        brsar.seek(offset)
        brsar.write((int.from_bytes(size, "big") + 4 * len(text)).to_bytes(4, 'big'))

    # group table 335A8 33500
    for i in range(getData(brsar, dataPath(brsar, inO, grO))):
        offset = dataPath(brsar, inO, grO, (i + 1) * 8)
        for j in [0x10, 0x18]:
            brsar.seek(offset + j)
            size = brsar.read(4)
            brsar.seek(offset + j)
            brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))

    # file length, size of info, offset to file
    for offset in [0x8, 0x14, 0x18, 0x20, dataPathPoint(brsar, syO, 0x4), dataPathPoint(brsar, syO, 0x0C),
                   dataPathPoint(brsar, syO, 0x10), dataPathPoint(brsar, syO, 0x14), dataPathPoint(brsar, syO, 0x18)]:
        brsar.seek(offset)
        size = brsar.read(4)
        brsar.seek(offset)
        brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))

    data1Point = dataPath(brsar, syO, 0x08) + 4 * (number + 1)
    data2Point = positionOffset - data1Point
    brsar.seek(0)
    dataToWrite = brsar.read(data1Point)
    for i in range(len(text)):
        dataToWrite += positionOffset.to_bytes(4, "big")
        positionOffset += len(text[i])
    dataToWrite += brsar.read(data2Point - extra + 1)
    brsar.seek(data1Point + data2Point)
    for i in text:
        dataToWrite += i
    dataToWrite += brsar.read()
    brsar.close()
    brsar = open(GetBrsarPath(), "wb")
    brsar.write(dataToWrite)
    brsar.close()
    return number


def BrseqAddingSounddata(nameNumber, collectNumber):
    slotsToAdd = 2
    brsar = open(GetBrsarPath(), "r+b")
    number = getData(brsar, dataPath(brsar, inO, sdO))
    sizeDifference = 0x54 * slotsToAdd
    brsar.seek(dataPath(brsar, inO, sdO))
    brsar.write((number + slotsToAdd).to_bytes(4, 'big'))

    # Sound Data list 17A30
    for i in range(number):
        offset = dataPath(brsar, inO, sdO) + (i + 1) * 8
        suboffset = dataPath(brsar, inO, sdO, (i + 1) * 8)
        for j in [suboffset + 0x10, suboffset + 0x1C, offset]:
            brsar.seek(j)
            size = brsar.read(4)
            brsar.seek(j)
            brsar.write((int.from_bytes(size, "big") + 0x8 * slotsToAdd).to_bytes(4, 'big'))

    # Soundbank, Player Info
    for offsettype in [sbO, piO]:
        for i in range(getData(brsar, dataPath(brsar, inO, offsettype))):
            offset = dataPath(brsar, inO, offsettype) + (i + 1) * 8
            brsar.seek(offset)
            size = brsar.read(4)
            brsar.seek(offset)
            brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))

    # 2DAFC - Collection
    for i in range(getData(brsar, dataPath(brsar, inO, ctO))):
        offset = dataPath(brsar, inO, ctO, (i + 1) * 8, 0x18)
        for j in range(getData(brsar, offset)):
            brsar.seek(offset + (j + 1) * 8)
            size = brsar.read(4)
            brsar.seek(offset + (j + 1) * 8)
            brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))
        offset = dataPath(brsar, inO, ctO, (i + 1) * 8) + 0x18
        brsar.seek(offset)
        size = brsar.read(4)
        brsar.seek(offset)
        brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))
        offset = dataPath(brsar, inO, ctO) + (i + 1) * 8
        brsar.seek(offset)
        size = brsar.read(4)
        brsar.seek(offset)
        brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))

    # group table 335A8 33500
    for i in range(getData(brsar, dataPath(brsar, inO, grO))):
        offset = dataPath(brsar, inO, grO, (i + 1) * 8)
        for j in [0x10, 0x18, 0x24]:
            brsar.seek(offset + j)
            size = brsar.read(4)
            brsar.seek(offset + j)
            brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))
        for j in range(getData(brsar, offset + 0x28)):
            brsar.seek(offset + 0x30 + j * 8)
            size = brsar.read(4)
            brsar.seek(offset + 0x30 + j * 8)
            brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))
        offset = dataPath(brsar, inO, grO) + (i + 1) * 8
        brsar.seek(offset)
        size = brsar.read(4)
        brsar.seek(offset)
        brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))

    # file length, size of info, offset to file
    for offset in [0x8, 0x1C, 0x20, dataPathPoint(brsar, inO, 0x4), dataPathPoint(brsar, inO, 0x14),
                   dataPathPoint(brsar, inO, 0x1C), dataPathPoint(brsar, inO, 0x24), dataPathPoint(brsar, inO, 0x2C),
                   dataPathPoint(brsar, inO, 0x34), dataPathPoint(brsar, inO, scO, 0x2)]:
        brsar.seek(offset)
        size = brsar.read(4)
        brsar.seek(offset)
        brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))

    # Add New Offsets
    # sounddata = 01B7+i 38+i 0000000301000000 (start + 0x40) 64780100010001010000 (start + 0x2C) 0000000000000000000000000000000000300000000 (0000C00F song/000000FF score) 7800000000000000000000000180000000
    soundDataOffset = dataPath(brsar, inO, sdO, number * 8) + 0x4C - 8 * slotsToAdd
    soundDataOffsetTable = dataPath(brsar, inO, sdO) + number * 8 + 4
    lastOffset = getData(brsar, soundDataOffsetTable - 4)

    brsar.seek(0)
    dataToWrite = brsar.read(soundDataOffsetTable)
    for i in range(slotsToAdd):
        dataToWrite += (0x01000000).to_bytes(4, "big") + (lastOffset + 0x4C * (i + 1)).to_bytes(4, "big")
    dataToWrite += brsar.read(soundDataOffset - soundDataOffsetTable)
    for i in range(slotsToAdd):
        dataToWrite += (nameNumber + i).to_bytes(4, "big") + (collectNumber + i).to_bytes(4, "big") + (
            0x301000000).to_bytes(8, "big") + (lastOffset + 0x4C * (i + 1) + 0x40).to_bytes(4, "big") + (
                           0x6478010001010000).to_bytes(8, "big") + (lastOffset + 0x4C * (i + 1) + 0x2C).to_bytes(4,
                                                                                                                  "big") + (
                           0x3000000000000).to_bytes(22, "big")
        if (i % 2 == 0):
            dataToWrite += (0xC00F).to_bytes(2, "big")
        else:
            dataToWrite += (0x00FF).to_bytes(2, "big")
        dataToWrite += (0x7800000000000000000000000180000000000000).to_bytes(20, "big")
    dataToWrite += brsar.read()
    brsar.close()
    brsar = open(GetBrsarPath(), "wb")
    brsar.write(dataToWrite)
    brsar.close()

    return number


def BrseqAddingCollection(group, sizes):
    slotsToAdd = 2
    brsar = open(GetBrsarPath(), "r+b")
    positionNum = getData(brsar, dataPath(brsar, inO, ctO))
    sizeDifference = 0x38 * slotsToAdd
    brsar.seek(dataPath(brsar, inO, ctO))
    brsar.write((positionNum + slotsToAdd).to_bytes(4, 'big'))
    positionOffset = dataPath(brsar, inO, grO)
    pos = getData(brsar, dataPathPoint(brsar, inO, grO)) + 0x10

    # collectionshift
    for i in range(positionNum):
        offset = dataPath(brsar, inO, ctO, (i + 1) * 8, 0x18)
        for j in range(getData(brsar, offset)):
            brsar.seek(offset + (j + 1) * 8)
            size = brsar.read(4)
            brsar.seek(offset + (j + 1) * 8)
            brsar.write((int.from_bytes(size, "big") + 8 * slotsToAdd).to_bytes(4, 'big'))
        offset = dataPath(brsar, inO, ctO, (i + 1) * 8) + 0x18
        brsar.seek(offset)
        size = brsar.read(4)
        brsar.seek(offset)
        brsar.write((int.from_bytes(size, "big") + 8 * slotsToAdd).to_bytes(4, 'big'))
        offset = dataPath(brsar, inO, ctO) + (i + 1) * 8
        brsar.seek(offset)
        size = brsar.read(4)
        brsar.seek(offset)
        brsar.write((int.from_bytes(size, "big") + 8 * slotsToAdd).to_bytes(4, 'big'))

    # group table 335A8 33500
    for i in range(getData(brsar, dataPath(brsar, inO, grO))):
        offset = dataPath(brsar, inO, grO, (i + 1) * 8)
        for j in [0x10, 0x18, 0x24]:
            brsar.seek(offset + j)
            size = brsar.read(4)
            brsar.seek(offset + j)
            brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))
        for j in range(getData(brsar, offset + 0x28)):
            brsar.seek(offset + 0x30 + j * 8)
            size = brsar.read(4)
            brsar.seek(offset + 0x30 + j * 8)
            brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))
        offset = dataPath(brsar, inO, grO) + (i + 1) * 8
        brsar.seek(offset)
        size = brsar.read(4)
        brsar.seek(offset)
        brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))

    # file length, size of info, offset to file
    for offset in [0x8, 0x1C, 0x20, dataPathPoint(brsar, inO, 0x4), dataPathPoint(brsar, inO, 0x2C),
                   dataPathPoint(brsar, inO, 0x34)]:
        brsar.seek(offset)
        size = brsar.read(4)
        brsar.seek(offset)
        brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))

    # collection index group: randomlengthnumber(4bytes) FFFFFFFF(8bytes) 01000000(12bytes) postitionoffset+0x1C(4bytes) 0301000000(8bytes) postitionoffset+0x38(4bytes) 01000000(4bytes) postitionoffset+0x40(4bytes) 01000000(4bytes) postitionoffset+0x48(4bytes) 02(4bytes) 63+number(4bytes) 03(4bytes) 63+number(4bytes) 13(4bytes) 63+number(4bytes)
    data1Point = dataPath(brsar, inO, ctO) + 8 * positionNum + 4
    brsar.seek(0)
    dataToWrite = brsar.read(data1Point)
    for i in range(slotsToAdd):
        dataToWrite += (0x01000000).to_bytes(4, "big") + (pos + i * 0x30).to_bytes(4, "big")
    dataToWrite += brsar.read(positionOffset - data1Point)
    for i in range(slotsToAdd):
        dataToWrite += sizes[i].to_bytes(4, "big") + (0xFFFFFFFF).to_bytes(8, "big") + (0x01000000).to_bytes(12,
                                                                                                             "big") + (
                                   pos + i * 0x30 + 0x1C).to_bytes(4, "big")
        # the collection pos entry could maybe reperesent putting the song in different tables for space saving purposes
        dataToWrite += (0x0101000000).to_bytes(8, "big") + (pos + i * 0x30 + 0x28).to_bytes(4, "big") + (0x02).to_bytes(
            4, "big") + (group + i).to_bytes(4, "big")
    dataToWrite += brsar.read()
    brsar.close()
    brsar = open(GetBrsarPath(), "wb")
    brsar.write(dataToWrite)
    brsar.close()
    return positionNum


def BrseqAddingTable(positionNum):
    slotsToAdd = 2
    brsar = open(GetBrsarPath(), "r+b")
    positionOffset = GetTableOffset(brsar, positionNum) + 0x10
    listOffset = BrsarGetList(brsar, positionOffset)
    brsar.seek(positionOffset + 0x18)
    num = int.from_bytes(brsar.read(4), "big")
    brsar.seek(positionOffset + 0x18)
    # number of tracks
    brsar.write((num + slotsToAdd).to_bytes(4, "big"))

    brsar.seek(listOffset + 24 * (num - 1))
    amount = int.from_bytes(brsar.read(4), "big") + int.from_bytes(brsar.read(4), "big")
    brsar.seek(listOffset + 24 * (num - 1) - 4)
    number = int.from_bytes(brsar.read(4), "big") + slotsToAdd
    lastTableOffset = getData(brsar, listOffset - 8) + 8 * slotsToAdd

    sizeDifference = 0x20 * slotsToAdd

    numberOfGroups = getData(brsar, dataPath(brsar, inO, grO))

    # for every group entry after the changed group
    for i in range(numberOfGroups):
        offset = dataPath(brsar, inO, grO, 0x8 * (i + 1))
        if (i > positionNum):
            location = dataPathPoint(brsar, inO, grO, 0x8 * (i + 1))
            brsar.seek(location)
            size = brsar.read(4)
            brsar.seek(location)
            brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))

        # offset to rseq, offset to rwar, offset to subsection 2
        offsetList = [0x10, 0x18]
        if (i > positionNum): offsetList.append(0x24)
        for j in offsetList:
            brsar.seek(offset + j)
            size = brsar.read(4)
            brsar.seek(offset + j)
            brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))

        # offsets in the big table
        if (i >= positionNum):
            numbers = getData(brsar, offset + 0x28)
            if (i == positionNum): numbers -= slotsToAdd
            for j in range(numbers):
                offsetToChoose = sizeDifference
                if (i == positionNum): offsetToChoose = 8 * slotsToAdd
                newOffset = getData(brsar, offset + 0x30 + 8 * j) + offsetToChoose
                brsar.seek(offset + 0x30 + 8 * j)
                # printh(offset)
                brsar.write(newOffset.to_bytes(4, "big"))

    # total, info size, file offset, sound count table, info size
    for offset in [0x8, 0x1C, 0x20, dataPathPoint(brsar, inO, 0x34), dataPathPoint(brsar, inO, 0x4)]:
        brsar.seek(offset)
        size = brsar.read(4)
        brsar.seek(offset)
        brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))

    # add expanding parts
    brsar.seek(0)
    data1 = brsar.read(listOffset - 4)
    data2 = brsar.read(24 * num)
    data3 = brsar.read()
    brsar.close()
    brsar = open(GetBrsarPath(), "wb")
    dataToWrite = data1
    for i in range(slotsToAdd):
        dataToWrite += b"\01\00\00\00" + (lastTableOffset + 0x18 * (i + 1)).to_bytes(4, "big")
    dataToWrite += data2
    for i in range(slotsToAdd):
        dataToWrite += (number + i).to_bytes(4, "big") + amount.to_bytes(4, "big") + bytes(16)
    dataToWrite += data3
    brsar.write(dataToWrite)
    brsar.close()

    return num


def BrseqAddingDol(number, midiInfo, brseqNumber):
    # 59C520
    dol = open(GetMainDolPath(), "r+b")
    sizeDifference = 0xBC
    positionOffset = 0x59C520 + 0xBC * 50  # 0x005AB200

    if (False):
        # offset
        for i in range(18):
            dol.seek(4 * i)
            size = int.from_bytes(dol.read(4), "big")
            if (size > 0x59C56E):
                dol.seek(4 * i)
                dol.write((size + sizeDifference).to_bytes(4, "big"))

        # size
        dol.seek(0xC0)
        size = int.from_bytes(dol.read(4), "big")
        dol.seek(0xC0)
        dol.write((size + sizeDifference).to_bytes(4, "big"))

    # stuff: number + something
    dol.seek(0)
    data = dol.read(positionOffset)

    data += (number + 0xC8).to_bytes(4, "big")

    mem = 0x805211CC + 0x32 * 50

    data += mem.to_bytes(4, "big")
    data += (mem - 0x15E9).to_bytes(4, "big")
    data += (mem - 0x15D8).to_bytes(4, "big")
    data += (mem + 0x10).to_bytes(4, "big")
    data += (mem + 0x22).to_bytes(4, "big")
    data += (mem - 0x15C9).to_bytes(4, "big")
    data += (mem - 0x15BB).to_bytes(4, "big")

    data += midiInfo[4].to_bytes(1, "big") + bytes(3)
    data += midiInfo[2].to_bytes(4, "big")
    data += midiInfo[3].to_bytes(4, "big")
    data += (0xC0).to_bytes(4, "big")  # ?
    data += (0x00010000).to_bytes(4, "big")
    data += int("3F 37 4B C7 3F 5D F3 B6 3F 80 00 00 3F 93 33 33 3F A6 66 66".replace(" ", ""), 16).to_bytes(0x14,
                                                                                                             "big")  # ?
    data += bytes(4)
    data += brseqNumber.to_bytes(4, "big")
    data += (brseqNumber + 1).to_bytes(4, "big")
    data += (0x00010102).to_bytes(4, "big")  # ?
    data += (0x01010000).to_bytes(4, "big")
    data += int("00 00 00 08 00 00 00 1C 00 00 00 2C 00 00 00 3C 00 00 00 50 00 00 00 60".replace(" ", ""),
                16).to_bytes(0x18, "big")  # ?
    data += (0x03E7).to_bytes(4, "big")
    data += int(
        "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 01 00 00 00 02 00 00 00 00 00 00 00 02 00 00 00 02 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 08 FF FF FF FF 00 00 00 74".replace(
            " ", ""), 16).to_bytes(0x44, "big")  # ?

    dol.seek(positionOffset + 0xBC)
    data += dol.read()
    dol.close()

    dol = open(GetMainDolPath(), "wb")
    dol.write(data)
    dol.close()


def dataPath(file, *argv):
    file.seek(argv[0])
    root = int.from_bytes(file.read(4), "big")
    file.seek(root + argv[1])
    if (len(argv) > 2):
        for i in range(2, len(argv)):
            file.seek(root + argv[i] + 8 + int.from_bytes(file.read(4), "big"))
    return root + int.from_bytes(file.read(4), "big") + 8


def dataPathPoint(file, *argv):
    file.seek(argv[0])
    root = int.from_bytes(file.read(4), "big")
    file.seek(root + argv[1])
    if (len(argv) > 2):
        for i in range(2, len(argv)):
            file.seek(root + argv[i] + 8 + int.from_bytes(file.read(4), "big"))
    return file.tell()


def ReplaceSong(positionNum, replacementArray, BrseqOrdering, BrseqInfoArray, BrseqLengthArray):
    if (not os.path.exists(GetBrsarPath() + ".backup")): copyfile(GetBrsarPath(), GetBrsarPath() + ".backup")
    BrsarPath = GetBrsarPath()
    BrseqInfo = []
    BrseqLength = []
    for i in range(len(BrseqOrdering)):
        BrseqInfo.append(BrseqInfoArray[BrseqOrdering[i]])
        BrseqLength.append(BrseqLengthArray[BrseqOrdering[i]])
    sizeDifference = 0
    brsar = open(BrsarPath, "rb")
    positionOffset = dataPath(brsar, inO, grO, 0x8 * (positionNum + 1)) + 0x10
    listOffset = BrsarGetList(brsar, positionOffset)
    replacementArray.append(getData(brsar, dataPath(brsar, inO, grO, 8 * (positionNum + 1)) + 0x28))
    brsar.seek(positionOffset)
    currentSpot = int.from_bytes(brsar.read(4), 'big')
    if (listOffset != -1):
        posOffset = []
        lenOffset = []
        data = []
        for num in range(len(replacementArray) - 1):
            brsar.seek(listOffset + 24 * replacementArray[num])
            posOffset.append(brsar.read(4))
            lenOffset.append(brsar.read(4))
        brsar.seek(0)
        data.append(brsar.read(currentSpot + int.from_bytes(posOffset[0], 'big')))
        for num in range(len(replacementArray) - 2):
            brsar.seek(currentSpot + int.from_bytes(posOffset[num], 'big') + int.from_bytes(lenOffset[num], 'big'))
            data.append(brsar.read(
                int.from_bytes(posOffset[num + 1], 'big') - int.from_bytes(posOffset[num], 'big') - int.from_bytes(
                    lenOffset[num], 'big')))
        brsar.seek(currentSpot + int.from_bytes(posOffset[len(posOffset) - 1], 'big') + int.from_bytes(
            lenOffset[len(lenOffset) - 1], 'big'))
        data.append(brsar.read())
        brsar.close()
        for num in range(len(replacementArray) - 1):
            if (num == 0):
                infoToWrite = data[num] + BrseqInfo[num]
            else:
                infoToWrite = infoToWrite + data[num] + BrseqInfo[num]
        infoToWrite = infoToWrite + data[len(replacementArray) - 1]
        brsar = open(BrsarPath, "wb")
        brsar.write(infoToWrite)
        brsar.close()
        brsar = open(BrsarPath, "r+b")
        for num in range(replacementArray[0], replacementArray[len(replacementArray) - 1]):
            if (sizeDifference != 0):
                brsar.seek(listOffset + 24 * num)
                size = brsar.read(4)
                brsar.seek(listOffset + 24 * num)
                brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))
            if (num in replacementArray):
                brsar.seek(listOffset + 4 + 24 * num)
                sizeDifference += BrseqLength[replacementArray.index(num)] - int.from_bytes(brsar.read(4), "big")
                brsar.seek(listOffset + 4 + 24 * num)
                brsar.write(BrseqLength[replacementArray.index(num)].to_bytes(4, 'big'))

        SizeIncreaseBrsar(brsar, sizeDifference, positionOffset)

        for offset in [8, positionOffset + 4]:
            brsar.seek(offset)
            size = brsar.read(4)
            brsar.seek(offset)
            brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))
    else:
        data = []
        brsar.seek(0)
        data.append(brsar.read(currentSpot))
        brsar.seek(positionOffset + 4)
        brsar.seek(currentSpot + int.from_bytes(brsar.read(4), 'big'))
        data.append(brsar.read())
        brsar.close()
        brsar = open(BrsarPath, "wb")
        brsar.write(data[0] + BrseqInfo + data[1])
        brsar.close()
        brsar = open(BrsarPath, "r+b")
        brsar.seek(positionOffset + 4)
        sizeDifference = BrseqLength - int.from_bytes(brsar.read(4), "big")

        SizeIncreaseBrsar(brsar, sizeDifference, positionOffset)

        for offset in [8, positionOffset + 4]:
            brsar.seek(offset)
            size = brsar.read(4)
            brsar.seek(offset)
            brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))
    brsar.close()