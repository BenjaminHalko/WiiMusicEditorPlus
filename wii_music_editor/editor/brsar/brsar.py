from pathlib import Path

from wii_music_editor.editor.brsar.brsarSection import BrsarSection
from wii_music_editor.utils.pathUtils import paths


class Brsar(BrsarSection):
    _fileLength = 0x08
    _infoSectionOffset = 0x18
    _infoSectionSize = 0x1C
    _fileSectionOffset = 0x20
    _fileSectionSize = 0x24

    data: bytearray
    infoSectionOffset: int
    fileSectionOffset: int
    infoSection: 'InfoSection'

    def __init__(self):
        super().__init__(self, 0)
        with open(paths.brsar, "rb") as file:
            self.data = bytearray(file.read())
        self.infoSectionOffset = self.readBytes(self._infoSectionOffset)
        self.fileSectionOffset = self.readBytes(self._fileSectionOffset)
        self.infoSection = InfoSection(self, self.infoSectionOffset)


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
        # self.groupTable = GroupTable(self, groupTableOffset)


class CollectionTable(BrsarSection):
    _numEntries = 0x00
    _entries = 0x04

    parent: InfoSection
    entries: list['CollectionEntry']

    def __init__(self, parent: InfoSection, offset: int):
        super().__init__(parent, offset)
        print(self._numEntries)
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

