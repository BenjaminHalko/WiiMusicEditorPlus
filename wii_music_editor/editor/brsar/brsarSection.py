class BrsarSection:
    _referenceValueOffset = 0x04
    _referenceSize = 0x08

    parent: 'BrsarSection'
    offset: int
    infoSectionOffset: int
    fileSectionOffset: int

    def __init__(self, parent: 'BrsarSection', offset: int):
        print(type(self), hex(offset))
        self.parent = parent
        self.offset = offset

    def getParentData(self, value: str):
        if hasattr(self, value):
            return getattr(self, value)
        else:
            return self.parent.getParentData(value)

    def readBytes(self, offset: int, length: int = 4):
        offset += self.offset
        data = self.getParentData("data")
        return int.from_bytes(data[offset:offset + length], "big")

    def sectionReference(self, offset: int):
        infoSectionOffset = self.getParentData("infoSectionOffset")
        return self.readBytes(offset + self._referenceValueOffset) + infoSectionOffset + 0x08
