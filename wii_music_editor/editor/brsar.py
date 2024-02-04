from pathlib import Path


class BrsarSection:
    _referenceValueOffset = 0x04
    _referenceSize = 0x08

    parent: 'BrsarSection'
    offset: int
    infoSectionOffset: int
    fileSectionOffset: int

    def __init__(self, parent: 'BrsarSection', offset: int):
        self.parent = parent
        self.offset = offset

    def rootSection(self):
        if self.parent is self:
            return self
        else:
            return self.parent.rootSection()

    def readBytes(self, offset: int):
        length = 4
        offset += self.offset
        rootSection = self.rootSection()
        return int.from_bytes(rootSection.data[offset:offset + length], "big")

    def updateValue(self, value: str, sizeDifference: int):
        length = 4
        offset = getattr(self, f"_{value}") + self.offset
        val = getattr(self, value) + sizeDifference
        setattr(self, value, val)
        rootSection = self.rootSection()
        rootSection.data[offset:offset + length] = val.to_bytes(length, "big")

    def sectionReference(self, offset: int):
        rootSection = self.rootSection()
        return self.readBytes(offset + self._referenceValueOffset) + rootSection.infoSectionOffset + 0x08


class Brsar(BrsarSection):
    _fileLength = 0x08
    _infoSectionOffset = 0x18
    _infoSectionSize = 0x1C
    _fileSectionOffset = 0x20
    _fileSectionSize = 0x24

    brsarPath: Path or str
    data: bytearray
    fileLength: int
    infoSectionOffset: int
    fileSectionOffset: int
    infoSectionSize: int
    fileSectionSize: int
    infoSection: 'InfoSection'
    fileSection: 'FileSection'

    def __init__(self, path: Path or str):
        super().__init__(self, 0)
        self.brsarPath = path
        with open(str(self.brsarPath)+".backup", "rb") as file:
            self.data = bytearray(file.read())
        self.fileLength = self.readBytes(self._fileLength)
        self.infoSectionOffset = self.readBytes(self._infoSectionOffset)
        self.fileSectionOffset = self.readBytes(self._fileSectionOffset)
        self.infoSectionSize = self.readBytes(self._infoSectionSize)
        self.fileSectionSize = self.readBytes(self._fileSectionSize)
        self.infoSection = InfoSection(self, self.infoSectionOffset)
        self.fileSection = FileSection(self, self.fileSectionOffset)

    def replaceSong(self, song: bytearray, index: int):
        songGroup = self.infoSection.groupTable.entries[index]
        sizeDifference = len(song) - songGroup.rseqSize

        # Replace song data
        self.data = self.data[:songGroup.rseqOffset]+song+self.data[songGroup.rseqOffset+songGroup.rseqSize:]

        # Update Group Table
        songGroup.updateValue('rseqSize', sizeDifference)
        for group in self.infoSection.groupTable.entries[index+1:]:
            group.updateValue('rseqOffset', sizeDifference)

        # Update Section Sizes
        self.updateValue('fileLength', sizeDifference)
        self.updateValue('fileSectionSize', sizeDifference)
        self.fileSection.updateValue('sectionSize', sizeDifference)

    def save(self):
        with open(self.brsarPath, "wb") as file:
            file.write(self.data)


class InfoSection(BrsarSection):
    # _sectionSize = 0x04
    # _soundDataTable = 0x08
    # _soundBankTable = 0x10
    # _playerInfoTable = 0x18
    _collectionTable = 0x20
    _groupTable = 0x28
    # _soundCount = 0x30

    parent: Brsar
    collectionTable: 'CollectionTable'
    groupTable: 'GroupTable'

    def __init__(self, parent: Brsar, offset: int):
        super().__init__(parent, offset)

        collectionTableOffset = self.sectionReference(self._collectionTable)
        groupTableOffset = self.sectionReference(self._groupTable)
        self.collectionTable = CollectionTable(self, collectionTableOffset)
        self.groupTable = GroupTable(self, groupTableOffset)


class FileSection(BrsarSection):
    _sectionSize = 0x04

    parent: Brsar
    sectionSize: int

    def __init__(self, parent: Brsar, offset: int):
        super().__init__(parent, offset)
        self.sectionSize = self.readBytes(self._sectionSize)


class CollectionTable(BrsarSection):
    _numEntries = 0x00
    _entries = 0x04

    parent: InfoSection
    entries: list['CollectionEntry']

    def __init__(self, parent: InfoSection, offset: int):
        super().__init__(parent, offset)
        numEntries = self.readBytes(self._numEntries)
        self.entries = [
            CollectionEntry(self, self.sectionReference(self._entries + i * self._referenceSize))
            for i in range(numEntries)
        ]


class CollectionEntry(BrsarSection):
    _audioLength = 0x00
    _audioData = 0x0C

    parent: CollectionTable
    audioLength: int
    audioData: int

    def __init__(self, parent: CollectionTable, offset: int):
        super().__init__(parent, offset)
        print(hex(offset))
        self.audioLength = self.readBytes(self._audioLength)
        self.audioData = self.readBytes(self._audioData)


class GroupTable(BrsarSection):
    _numEntries = 0x00
    _entries = 0x04

    parent: InfoSection
    entries: list['GroupDataEntry']

    def __init__(self, parent: InfoSection, offset: int):
        super().__init__(parent, offset)
        numEntries = self.readBytes(self._numEntries)
        self.entries = [
            GroupDataEntry(self, self.sectionReference(self._entries + i * self._referenceSize))
            for i in range(numEntries)
        ]


class GroupDataEntry(BrsarSection):
    _rseqOffset = 0x10
    _rseqSize = 0x14

    parent: GroupTable
    rseqOffset: int
    rseqSize: int

    def __init__(self, parent: GroupTable, offset: int):
        super().__init__(parent, offset)
        self.rseqOffset = self.readBytes(self._rseqOffset)
        self.rseqSize = self.readBytes(self._rseqSize)
    