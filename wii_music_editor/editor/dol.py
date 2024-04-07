from pathlib import Path

from wii_music_editor.data.songs import SongClass, SongType, song_list
from wii_music_editor.data.styles import style_list, StyleInstruments


class MainDol:
    __songSegmentRegularOffset = 0x59C520
    __songSegmentMaestroOffset = 0x5A00EC
    __songSegmentHandBellOffset = 0x5A0AEC
    __songSegmentMenuOffset = 0x596DAC
    __songSegmentSize = 0xBC
    songSegmentTimeSignature = 0x20
    songSegmentLength = 0x24
    songSegmentTempo = 0x28
    songSegmentDefaultStyle = 0x48

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
    __defaultStyleCodeBegin = 0x3d4acc
    __defaultStyleCodeEnd = 0x3d4b64

    mainDolPath: Path
    data: bytearray

    def __init__(self, path: Path):
        self.mainDolPath = path
        with open(self.mainDolPath, "rb") as file:
            self.data = bytearray(file.read())
        self.__remove_style_execution()

    def read(self, offset: int, length: int = 4) -> int:
        return int.from_bytes(self.data[offset:offset + length], "big")

    def write(self, data: int, offset: int, length: int = 4):
        self.data[offset:offset + length] = data.to_bytes(length, "big")

    def save(self):
        with open(self.mainDolPath, "wb") as file:
            file.write(self.data)

    def __set_style(self, data: int, offset: int):
        if data == 67:
            data = 0xffffffff
        self.write(data, offset)

    def __get_style(self, offset: int) -> int:
        data = self.read(offset)
        if data == 0xffffffff:
            data = 67
        return data

    def set_style(self, index: int, style: StyleInstruments):
        offset = self.__styleSegmentOffset + index * self.__styleSegmentSize
        self.__set_style(style.melody, offset + self.__styleSegmentMelody)
        self.__set_style(style.harmony, offset + self.__styleSegmentHarmony)
        self.__set_style(style.chord, offset + self.__styleSegmentChord)
        self.__set_style(style.bass, offset + self.__styleSegmentBass)
        self.__set_style(style.perc1, offset + self.__styleSegmentPerc1)
        self.__set_style(style.perc2, offset + self.__styleSegmentPerc2)

    def get_style(self, index: int) -> StyleInstruments:
        offset = self.__styleSegmentOffset + index * self.__styleSegmentSize
        return StyleInstruments(
            self.__get_style(offset + self.__styleSegmentMelody),
            self.__get_style(offset + self.__styleSegmentHarmony),
            self.__get_style(offset + self.__styleSegmentChord),
            self.__get_style(offset + self.__styleSegmentBass),
            self.__get_style(offset + self.__styleSegmentPerc1),
            self.__get_style(offset + self.__styleSegmentPerc2)
        )

    def __remove_code(self, min_offset: int, max_offset: int) -> bool:
        replaced = False
        for i in range(min_offset, max_offset, 4):
            if self.data[i] >= 0x90:
                self.data[i:i + 4] = b'\x38\x11\x00\x00'
                replaced = True
        return replaced

    def __remove_style_execution(self):
        if self.__remove_code(self.__styleCodeBegin, self.__styleCodeEnd):
            for style in style_list:
                self.set_style(style.style_id, style.style)

        if self.__remove_code(self.__defaultStyleCodeBegin, self.__defaultStyleCodeEnd):
            for song in song_list:
                if song.default_style != -1:
                    self.write_song_info(song, song.default_style, self.songSegmentDefaultStyle)

    def __get_song_offset(self, song: SongClass) -> int:
        song_offset = self.__songSegmentRegularOffset
        if song.song_type == SongType.Maestro:
            song_offset = self.__songSegmentMaestroOffset
        elif song.song_type == SongType.Hand_Bell:
            song_offset = self.__songSegmentHandBellOffset
        elif song.song_type == SongType.Menu:
            song_offset = self.__songSegmentMenuOffset
        song_offset += song.mem_order * self.__songSegmentSize
        return song_offset

    def write_song_info(self, song: SongClass, data: int, offset: int, length: int = 4):
        offset += self.__get_song_offset(song)
        self.write(data, offset, length)

    def read_song_info(self, song: SongClass, offset: int, length: int = 4) -> int:
        offset += self.__get_song_offset(song)
        return self.read(offset, length)
