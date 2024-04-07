import logging
import os
from pathlib import Path
from shutil import rmtree

from wii_music_editor.data.songs import song_list, SongType, SongClass
from wii_music_editor.data.styles import StyleNames, Style, StyleType, style_list
from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.utils.preferences import preferences
from wii_music_editor.utils.shell import run_shell


class TextClass:
    __regular_offsets = [0xc8, 0x190, 0x12c]
    __maestro_offsets = [0xfa, 0x1c2, 0x15e]
    __hand_bell_offsets = [0xff, 0x1c7, 0x163]
    __style_offset = 0xb100
    __style_offset_custom_jam = 0xb200
    __maestro_order = [0, 4, 2, 3, 1]
    __hand_bell_order = [0, 2, 3, 1, 4]
    __style_order = [3, 1, 4, 2, 7, 10, 11, 9, 8, 6, 5]
    __filepath: Path
    __filename: str
    __folder: str
    __language: int

    songs: list[str]
    descriptions: list[str]
    genres: list[str]
    styles: list[str]
    textlines: list[bytes]

    def __init__(self, file: Path, filename: str = "message.carc"):
        self.__filepath = file
        self.__filename = filename
        self.__folder = str(Path(filename).with_suffix(".d"))
        self.__language = preferences.rom_language

        # Read the text file
        self.decode()
        self.read()

    def read(self):
        self.songs = []
        self.descriptions = []
        self.genres = []
        self.styles = []

        with open(self.__filepath / self.__folder / 'new_music_message.txt', 'rb') as message:
            self.textlines = message.readlines()
        rmtree(self.__filepath / self.__folder)
        self.fix_message_file()

        # Set song names, descriptions, and genres
        for i, text_type in enumerate([self.songs, self.descriptions, self.genres]):
            for song in song_list:
                offsets, index = self.__get_song_offset(song)
                offset_str = format(offsets[i] + index[i], 'x').lower()
                offset_str = ' ' * (4 - len(offset_str)) + offset_str + '00 @'
                text_type.append(self.__text_at_offset(offset_str))

        # Get the styles
        for style in style_list:
            if style.style_type == StyleType.Global or style.style_type == StyleType.QuickJam:
                offset_str = format(self.__style_offset + style.style_id, 'x').lower()
                offset_str = ' ' * (4 - len(offset_str)) + offset_str + ' @'
                self.styles.append(self.__text_at_offset(offset_str))

    def __get_song_offset(self, song: SongClass) -> (list[int], int):
        offset = self.__regular_offsets
        index = song.mem_order
        if song.song_type == SongType.Maestro:
            offset = self.__maestro_offsets
            index = self.__maestro_order[index]
        elif song.song_type == SongType.Hand_Bell:
            offset = self.__hand_bell_offsets
            index = self.__hand_bell_order[index]
        return offset, [index]*3

    def __text_at_offset(self, offset: str) -> str:
        for j, text in enumerate(self.textlines):
            if offset in text.decode("utf-8"):
                text_to_add = (text[22:len(text) - 2:1]).decode("utf-8")
                for text_line in self.textlines[j + 1:]:
                    if bytes('@', 'utf-8') in text_line:
                        break
                    text_to_add = f"{text_to_add[:len(text_to_add) - 2]}\n"
                    text_to_add += (text_line[3:len(text_line) - 2]).decode("utf-8")
                return text_to_add
        return ""

    def change_name(self, item: SongClass or Style, new_text: list[str], encode: bool = True):
        isSong = len(new_text) == 3
        if isSong:
            offsets, index = self.__get_song_offset(item)
            self.songs[item.list_order] = new_text[0]
            self.descriptions[item.list_order] = new_text[1]
            self.genres[item.list_order] = new_text[2]
        else:
            offsets = [self.__style_offset]
            index = [item.style_id]
            self.styles[item.list_order] = new_text[0]
            if item.style_type == StyleType.Global:
                offsets.append(self.__style_offset_custom_jam)
                index.append(self.__style_order[item.style_id])
                new_text.append(new_text[0])

        for i in range(len(offsets)):
            offset = format(offsets[i]+index[i], 'x').lower()
            offset = ' ' * (4 - len(offset)) + offset
            if isSong:
                offset += '00 @'
            else:
                offset += ' @'

            for j, text in enumerate(self.textlines):
                if offset in text.decode("utf-8"):
                    while bytes('@', 'utf-8') not in self.textlines[j + 1]:
                        self.textlines.pop(j + 1)
                    text_to_add = repr(new_text[i]).strip("'").replace(r"\'", "'").strip("\"")
                    self.textlines[j] = bytes(f"{offset}{text.decode('utf-8')[10:22]}{text_to_add}\r\n", 'utf-8')
                    break

        if encode:
            self.encode()

    def decode(self):
        try:
            if (self.__filepath / self.__folder).is_dir():
                rmtree(self.__filepath / self.__folder)
            run_shell([paths.include / 'wiimms' / 'wszst', 'extract', self.__filepath / self.__filename],
                      logging_level=logging.DEBUG)
            os.remove(self.__filepath/self.__folder/"wszst-setup.txt")
            run_shell([paths.include/'wiimms'/'wbmgt', 'decode',
                       self.__filepath/self.__folder/'new_music_message.bmg'], logging_level=logging.DEBUG)
            os.remove(self.__filepath/self.__folder/'new_music_message.bmg')
        except Exception as e:
            ShowError("Could not decode text file", str(e))

    def encode(self):
        try:
            os.mkdir(self.__filepath / self.__folder)
            with open(self.__filepath / self.__folder / 'new_music_message.txt', 'wb') as message:
                message.writelines(self.textlines)
            run_shell([paths.include/'wiimms'/'wbmgt', 'encode',
                       self.__filepath/self.__folder/'new_music_message.txt'], logging_level=logging.DEBUG)
            os.remove(self.__filepath/self.__folder/"new_music_message.txt")
            os.remove(self.__filepath/self.__filename)
            run_shell([paths.include/'wiimms'/'wszst', 'create', self.__filepath/self.__folder,
                       '--dest', self.__filepath/self.__filename], logging_level=logging.DEBUG)
            rmtree(self.__filepath/self.__folder)
        except Exception as e:
            ShowError("Could not encode text file", str(e))

    def to_text(self) -> str:
        return ''.join([text.decode('utf-8') for text in self.textlines])

    def fix_message_file(self):
        for num in range(len(self.textlines)):
            if self.textlines[num] == b'  b200 @015f /\r\n':
                self.textlines[num] = b'  b200 @015f [/,4b] = ' + StyleNames.default[self.__language].encode(
                    "utf-8") + b'\r\n'
                self.textlines[num + 1] = b'  b201 @0160 [/,4b] = ' + StyleNames.rock[self.__language].encode(
                    "utf-8") + b'\r\n'
                self.textlines[num + 2] = b'  b202 @0161 [/,4b] = ' + StyleNames.march[self.__language].encode(
                    "utf-8") + b'\r\n'
                self.textlines[num + 3] = b'  b203 @0162 [/,4b] = ' + StyleNames.jazz[self.__language].encode(
                    "utf-8") + b'\r\n'
                self.textlines[num + 4] = b'  b204 @0163 [/,4b] = ' + StyleNames.latin[self.__language].encode(
                    "utf-8") + b'\r\n'
                self.textlines[num + 5] = b'  b205 @0164 [/,4b] = ' + StyleNames.reggae[self.__language].encode(
                    "utf-8") + b'\r\n'
                self.textlines[num + 6] = b'  b206 @0165 [/,4b] = ' + StyleNames.hawaiian[self.__language].encode(
                    "utf-8") + b'\r\n'
                self.textlines[num + 7] = b'  b207 @0166 [/,4b] = ' + StyleNames.electronic[self.__language].encode(
                    "utf-8") + b'\r\n'
                self.textlines[num + 8] = b'  b208 @0167 [/,4b] = ' + StyleNames.classical[self.__language].encode(
                    "utf-8") + b'\r\n'
                self.textlines[num + 9] = b'  b209 @0168 [/,4b] = ' + StyleNames.tango[self.__language].encode(
                    "utf-8") + b'\r\n'
                self.textlines[num + 10] = b'  b20a @0169 [/,4b] = ' + StyleNames.pop[self.__language].encode(
                    "utf-8") + b'\r\n'
                self.textlines[num + 11] = b'  b20b @016a [/,4b] = ' + StyleNames.japanese[self.__language].encode(
                    "utf-8") + b'\r\n'
                break
