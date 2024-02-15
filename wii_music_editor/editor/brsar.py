from pathlib import Path


class BrsarGroup:
    """
    Each group in a brsar file holds a list of songs.
    Different groups are used for different types of songs.
    """
    Regular = 2
    Maestro = 21
    Handbell = 23
    Menu = 34


class __BrsarSection:
    """
    This class is a parent class for all the sections in a brsar file.
    A list of all the sections in a brsar file can be found at:
    https://wiki.tockdom.com/wiki/BRSAR_(File_Format).
    :param parent: The `parent` attribute is the parent section of the section.
    :param offset: The `offset` attribute is the offset of the section from the start of the file.
    """
    _referenceValueOffset = 0x04
    _referenceSize = 0x08

    root: 'Brsar'
    parent: '__BrsarSection'
    offset: int

    def __init__(self, parent: '__BrsarSection', offset: int):
        self.parent = parent
        self.root = parent.root
        self.offset = offset

    def read_bytes(self, offset: int) -> int:
        """
        :param offset: The offset from the start of the section.
        :return: The integer value of the bytes at the given offset.
        """
        length = 4
        offset += self.offset
        return int.from_bytes(self.root.data[offset:offset + length], "big")

    def section_reference(self, offset: int) -> int:
        """
        This function returns the offset to another section.
        The documentation for a data reference can be found at:
        https://wiki.tockdom.com/wiki/BRSAR_(File_Format)#Data_References.
        :param offset: The offset from the start of the current section.
        :return:
        """
        section_offset = self.read_bytes(offset + self._referenceValueOffset)
        return section_offset + self.root.infoSectionOffset + 0x08

    def increment_value(self, value: str, increment: int) -> None:
        """
        :param value: The name of the attribute to update.
        :param increment: The amount to increment the attribute by.
        """
        length = 4
        offset = getattr(self, f"_{value}") + self.offset
        val = getattr(self, value) + increment
        setattr(self, value, val)
        self.root.data[offset:offset + length] = val.to_bytes(length, "big")


class Brsar(__BrsarSection):
    """
    This class is a representation of a brsar file.
    A list of all the sections in a brsar file can be found at https://wiki.tockdom.com/wiki/BRSAR_(File_Format).
    :param path: The path to a brsar file.
    """
    _fileLength = 0x08
    _infoSectionOffset = 0x18
    _infoSectionSize = 0x1C
    _fileSectionOffset = 0x20
    _fileSectionSize = 0x24

    fileLength: int
    infoSectionOffset: int
    infoSectionSize: int
    fileSectionOffset: int
    fileSectionSize: int

    brsarPath: Path
    data: bytearray
    infoSection: 'InfoSection'
    fileSection: 'FileSection'

    def __init__(self, path: Path):
        self.root = self
        super().__init__(self, 0)
        # Read the file
        self.brsarPath = path
        with open(self.brsarPath, "rb") as file:
            self.data = bytearray(file.read())
        # Read the header
        self.fileLength = self.read_bytes(self._fileLength)
        self.infoSectionOffset = self.read_bytes(self._infoSectionOffset)
        self.infoSectionSize = self.read_bytes(self._infoSectionSize)
        self.fileSectionOffset = self.read_bytes(self._fileSectionOffset)
        self.fileSectionSize = self.read_bytes(self._fileSectionSize)
        # Create the sections
        self.infoSection = InfoSection(self, self.infoSectionOffset)
        self.fileSection = FileSection(self, self.fileSectionOffset)

    def replace_song(self, song: bytearray, group_index: int, item_index: int):
        """
        This function replaces a song in the brsar file.
        :param song: The bytes of the new song.
        :param item_index: The index of the song inside the item table.
        :param group_index: The index of the group inside the group table.
        :return:
        """
        songGroup = self.infoSection.groupDataTable.entries[group_index]
        itemGroup = songGroup.itemTable.entries[item_index]
        rseqOffset = songGroup.rseqOffset + itemGroup.rseqOffset
        incrementAmount = len(song) - itemGroup.rseqSize

        # Replace song data
        self.data = self.data[:rseqOffset]+song+self.data[rseqOffset+itemGroup.rseqSize:]

        # Update Group Table
        songGroup.increment_value('rseqSize', incrementAmount)
        songGroup.increment_value('rwarOffset', incrementAmount)
        itemGroup.increment_value('rseqSize', incrementAmount)
        for item in songGroup.itemTable.entries[item_index+1:]:
            item.increment_value('rseqOffset', incrementAmount)

        # Update other group tables
        for group in self.infoSection.groupDataTable.entries[group_index+1:]:
            group.increment_value('rseqOffset', incrementAmount)
            group.increment_value('rwarOffset', incrementAmount)

        # Update Section Size
        self.increment_value('fileLength', incrementAmount)

    def get_song(self, group_index: int, item_index: int) -> bytearray:
        """
        This function returns the bytes of a song in the brsar file.
        :param group_index: The index of the group inside the group table.
        :param item_index: The index of the song inside the item table.
        :return: The bytes of the song.
        """
        songGroup = self.infoSection.groupDataTable.entries[group_index]
        itemGroup = songGroup.itemTable.entries[item_index]
        rseqOffset = songGroup.rseqOffset + itemGroup.rseqOffset
        return self.data[rseqOffset:rseqOffset+itemGroup.rseqSize]

    def save(self):
        with open(self.brsarPath, "wb") as file:
            file.write(self.data)


class InfoSection(__BrsarSection):
    """
    This class is a representation of the info section in a brsar file.
    https://wiki.tockdom.com/wiki/BRSAR_(File_Format)#INFO
    :param parent: A reference to the brsar header.
    :param offset: The `offset` attribute is the offset of the section from the start of the file.
    """
    _groupTable = 0x28

    parent: Brsar
    groupDataTable: 'GroupDataTable'

    def __init__(self, parent: Brsar, offset: int):
        super().__init__(parent, offset)
        groupDataTableOffset = self.section_reference(self._groupTable)
        self.groupDataTable = GroupDataTable(self, groupDataTableOffset)


class FileSection(__BrsarSection):
    """
    This class is a representation of the file section in a brsar file.
    https://wiki.tockdom.com/wiki/BRSAR_(File_Format)#FILE
    :param parent: A reference to the brsar header.
    :param offset: The offset from the start of the file.
    """
    _sectionSize = 0x04

    parent: Brsar
    sectionSize: int

    def __init__(self, parent: Brsar, offset: int):
        super().__init__(parent, offset)
        self.sectionSize = self.read_bytes(self._sectionSize)


class GroupDataTable(__BrsarSection):
    """
    This class is a representation of the group data table in a brsar file.
    This holds a list of all the groups in the file.
    https://wiki.tockdom.com/wiki/BRSAR_(File_Format)#Group_Table
    :param parent: A reference to the info section.
    :param offset: The offset from the start of the file.
    """
    __numEntries = 0x00
    __entries = 0x04

    parent: InfoSection
    entries: list['GroupDataEntry']

    def __init__(self, parent: InfoSection, offset: int):
        super().__init__(parent, offset)
        numEntries = self.read_bytes(self.__numEntries)
        self.entries = [
            GroupDataEntry(self, self.section_reference(self.__entries + i * self._referenceSize))
            for i in range(numEntries)
        ]


class GroupDataEntry(__BrsarSection):
    """
    This class is a representation of a group data entry in a brsar file.
    Each group data entry holds a reference to a list of items, and the offset and size of the group.
    Each rseqOffset is releative to the file section offset.
    https://wiki.tockdom.com/wiki/BRSAR_(File_Format)#Group_Data_Entry
    :param parent: A reference to the group data table.
    :param offset: The offset from the start of the file.
    """
    _rseqOffset = 0x10
    _rseqSize = 0x14
    _rwarOffset = 0x18
    _groupItemEntry = 0x20

    parent: GroupDataTable
    itemTable: 'GroupItemTable'

    def __init__(self, parent: GroupDataTable, offset: int):
        super().__init__(parent, offset)
        self.rseqOffset = self.read_bytes(self._rseqOffset)
        self.rseqSize = self.read_bytes(self._rseqSize)
        self.rwarOffset = self.read_bytes(self._rwarOffset)
        self.itemTable = GroupItemTable(self, self.section_reference(self._groupItemEntry))


class GroupItemTable(__BrsarSection):
    """
    This class is a representation of the group item table in a brsar file.
    This holds a list of all the items in the group.
    https://wiki.tockdom.com/wiki/BRSAR_(File_Format)#Group_Item_Reference_Table
    :param parent: A reference to the group data entry.
    :param offset: The offset from the start of the file.
    """
    __numEntries = 0x00
    __entries = 0x04

    parent: GroupDataEntry
    entries: list['GroupItemEntry']

    def __init__(self, parent: GroupDataEntry, offset: int):
        super().__init__(parent, offset)
        numEntries = self.read_bytes(self.__numEntries)
        self.entries = [
            GroupItemEntry(self, self.section_reference(self.__entries + i * self._referenceSize))
            for i in range(numEntries)
        ]


class GroupItemEntry(__BrsarSection):
    """
    This class is a representation of a group item entry in a brsar file.
    Each group item entry holds the offset and size of a rseq in the file section.
    Each rseqOffset is relative to the group offset.
    https://wiki.tockdom.com/wiki/BRSAR_(File_Format)#Group_Item_Info_Entry
    """
    _rseqOffset = 0x04
    _rseqSize = 0x08

    parent: GroupItemTable
    rseqOffset: int
    rseqSize: int

    def __init__(self, parent: GroupItemTable, offset: int):
        super().__init__(parent, offset)
        self.rseqOffset = self.read_bytes(self._rseqOffset)
        self.rseqSize = self.read_bytes(self._rseqSize)
    