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
