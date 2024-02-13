from pathlib import Path

from wii_music_editor.data.styles import styleList, StyleInstruments


class MainDolOffsets:
    songSegmentRegularOffset = 0x59C520
    songSegmentMaestroOffset = 0x5A00EC
    songSegmentHandBellOffset = 0x5A0AEC
    songSegmentMenuOffset = 0x596DAC
    songSegmentSize = 0xBC
    songSegmentTimeSignature = 0x20
    songSegmentLength = 0x24
    songSegmentTempo = 0x28


class MainDol:
    __styleSegmentOffset = 0x596758
    __styleSegmentSize = 0x24
    __styleSegmentMelody = 0x04
    __styleSegmentHarmony = 0x08
    __styleSegmentChord = 0x0C
    __styleSegmentBass = 0x10
    __styleSegmentPerc1 = 0x14
    __styleSegmentPerc2 = 0x18

    __styleCodeBegin = 0x36F9A4
    __styleCodeEnd = 0x3701CC

    mainDolPath: Path
    data: bytearray

    def __init__(self, path: Path):
        self.mainDolPath = path
        with open(self.mainDolPath, "rb") as file:
            self.data = bytearray(file.read())

    def read(self, offset: int, length: int = 4) -> int:
        return int.from_bytes(self.data[offset:offset + length], "big")

    def write(self, data: int, offset: int, length: int = 4):
        self.data[offset:offset + length] = data.to_bytes(length, "big")

    def save(self):
        with open(self.mainDolPath, "wb") as file:
            file.write(self.data)

    def set_style(self, index: int, style: StyleInstruments):
        offset = self.__styleSegmentOffset + index * self.__styleSegmentSize
        self.write(style.melody, offset + self.__styleSegmentMelody)
        self.write(style.harmony, offset + self.__styleSegmentHarmony)
        self.write(style.chord, offset + self.__styleSegmentChord)
        self.write(style.bass, offset + self.__styleSegmentBass)
        self.write(style.perc1, offset + self.__styleSegmentPerc1)
        self.write(style.perc2, offset + self.__styleSegmentPerc2)

    def get_style(self, index: int) -> StyleInstruments:
        offset = self.__styleSegmentOffset + index * self.__styleSegmentSize
        return StyleInstruments(
            self.read(offset + self.__styleSegmentMelody),
            self.read(offset + self.__styleSegmentHarmony),
            self.read(offset + self.__styleSegmentChord),
            self.read(offset + self.__styleSegmentBass),
            self.read(offset + self.__styleSegmentPerc1),
            self.read(offset + self.__styleSegmentPerc2)
        )

    def remove_style_execution(self):
        replaced = False

        # Removes the style execution code
        for i in range(self.__styleCodeBegin, self.__styleCodeEnd, 4):
            if self.data[i] != 0x38:
                self.data[i:i + 4] = b'\x38\x00\x00\x00'
                replaced = True

        if replaced:
            for style in styleList:
                self.set_style(style.style_id, style.style)
