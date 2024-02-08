import os
from pathlib import Path
from shutil import rmtree, copyfile

from wii_music_editor.data.songs import songList, SongType, SongClass
from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.utils.shell import run_shell


class TextClass:
    __regular_offsets = [0xc8, 0x190, 0x12c]
    __maestro_offsets = [0xfa, 0x1c2, 0x15e]
    __hand_bell_offsets = [0xff, 0x1c7, 0x163]
    __style_offset = 0xb200
    __maestro_order = [0, 4, 2, 3, 1]
    __hand_bell_order = [0, 2, 3, 1, 4]
    __style_order = [3, 1, 4, 2, 7, 10, 11, 9, 8, 6, 5]
    __filename: Path

    songs: list[str]
    descriptions: list[str]
    genres: list[str]
    styles: list[str]
    textlines: list[bytes]

    def __init__(self, file: Path):
        self.songs = []
        self.descriptions = []
        self.genres = []
        self.styles = []
        self.__filepath = file

        # Read the text file
        self.decode()

        # Set song names, descriptions, and genres
        for i, text_type in enumerate([self.songs, self.descriptions, self.genres]):
            for song in songList:
                offsets, index = self.__get_song_offset(song)
                offset_str = format(offsets[i]+index, 'x').lower()
                offset_str = ' ' * (4 - len(offset_str)) + offset_str + '00 @'
                text_type.append(self.__text_at_offset(offset_str))

        # Get the styles
        for i, index in enumerate(self.__style_order):
            offset_str = format(self.__style_offset + index, 'x').lower()
            offset_str = ' ' * (4 - len(offset_str)) + offset_str + ' @'
            self.styles.append(self.__text_at_offset(offset_str))

    def __get_song_offset(self, song: SongClass) -> (list[int], int):
        offset = self.__regular_offsets
        index = song.MemOrder
        if song.SongType == SongType.Maestro:
            offset = self.__maestro_offsets
            index = self.__maestro_order[index]
        elif song.SongType == SongType.Hand_Bell:
            offset = self.__hand_bell_offsets
            index = self.__hand_bell_order[index]
        return offset, index

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

    def change_name(self, item_index: int, new_text: list[str]):
        isSong = len(new_text) == 3
        offsets = [self.__style_offset]
        index = self.__style_order[item_index]
        if isSong:
            offsets, index = self.__get_song_offset(songList[item_index])

        for i in range(len(offsets)):
            offset = format(offsets[i]+index, 'x').lower()
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

        os.mkdir(self.__filepath/'message.d')
        with open(self.__filepath/'message.d'/'new_music_message.txt', 'wb') as message:
            message.writelines(self.textlines)

        self.encode()

    def decode(self):
        try:
            if (self.__filepath / "message.d").is_dir():
                rmtree(self.__filepath / "message.d")
            run_shell([paths.include / 'wiimms' / 'wszst', 'extract', self.__filepath / 'message.carc'])
            os.remove(self.__filepath/"message.d"/"wszst-setup.txt")
            run_shell([paths.include/'wiimms'/'wbmgt', 'decode',
                       self.__filepath/'message.d'/'new_music_message.bmg'])
            os.remove(self.__filepath/'message.d'/'new_music_message.bmg')
            with open(self.__filepath/'message.d'/'new_music_message.txt', 'rb') as message:
                self.textlines = message.readlines()
            rmtree(self.__filepath/'message.d')
        except Exception as e:
            ShowError("Could not decode text file", str(e))

    def encode(self):
        try:
            run_shell([paths.include/'wiimms'/'wbmgt', 'encode',
                       self.__filepath/'message.d'/'new_music_message.txt'])
            os.remove(self.__filepath/"message.d"/"new_music_message.txt")
            if not (self.__filepath/"message.carc.backup").exists():
                copyfile(self.__filepath/"message.carc", self.__filepath/"message.carc.backup")
            os.remove(self.__filepath/"message.carc")
            run_shell([paths.include/'wiimms'/'wszst', 'create', self.__filepath/'message.d',
                       '--dest', self.__filepath/'message.carc'])
            rmtree(self.__filepath/'message.d')
        except Exception as e:
            ShowError("Could not encode text file", str(e))

def FixMessageFile(textlines):
    nameIndex = romLanguageNumber[regionSelected] + (4 + max(regionSelected - 1, 0)) * (regionSelected > 1)
    for num in range(len(textlines)):
        if textlines[num] == b'  b200 @015f /\r\n':
            textlines[num] = b'  b200 @015f [/,4b] = ' + \
                             ["Default", "Par défaut", "Predeterm.", "Standard", "Normale", "オリジナル", "오리지널"][
                                 nameIndex].encode("utf-8") + b'\r\n'
            textlines[num + 1] = b'  b201 @0160 [/,4b] = ' + ["Rock", "Rock", "Rock", "Rock", "Rock", "ロック", "록"][
                nameIndex].encode("utf-8") + b'\r\n'
            textlines[num + 2] = b'  b202 @0161 [/,4b] = ' + \
                                 ["March", "Marche", "Marcha", "Marsch", "Marcia", "マーチ", "행진곡"][nameIndex].encode(
                                     "utf-8") + b'\r\n'
            textlines[num + 3] = b'  b203 @0162 [/,4b] = ' + ["Jazz", "Jazz", "Jazz", "Jazz", "Jazz", "ジャズ", "재즈"][
                nameIndex].encode("utf-8") + b'\r\n'
            textlines[num + 4] = b'  b204 @0163 [/,4b] = ' + \
                                 ["Latin", "Latino", "Latino", "Latin", "Latino", "ラテン", "라틴 음악"][nameIndex].encode(
                                     "utf-8") + b'\r\n'
            textlines[num + 5] = b'  b205 @0164 [/,4b] = ' + \
                                 ["Reggae", "Reggae", "Reggae", "Reggae", "Reggae", "レゲエ", "레게"][nameIndex].encode(
                                     "utf-8") + b'\r\n'
            textlines[num + 6] = b'  b206 @0165 [/,4b] = ' + \
                                 ["Hawaiian", "Hawaïen", "Hawaiano", "Hawaii", "Hawaiano", "ハワイ風", "하와이 음악"][
                                     nameIndex].encode("utf-8") + b'\r\n'
            textlines[num + 7] = b'  b207 @0166 [/,4b] = ' + \
                                 ["Electronic", "Électronique", "Electrónico", "Elektronik", "Elettronico",
                                  "ダウンビート", "전자 음악"][nameIndex].encode("utf-8") + b'\r\n'
            textlines[num + 8] = b'  b208 @0167 [/,4b] = ' + \
                                 ["Classical", "Classique", "Clásico", "Klassisch", "Classico", "室内楽", "실내악"][
                                     nameIndex].encode("utf-8") + b'\r\n'
            textlines[num + 9] = b'  b209 @0168 [/,4b] = ' + \
                                 ["Tango", "Tango", "Tango", "Tango", "Tango", "タンゴ", "탱고"][nameIndex].encode(
                                     "utf-8") + b'\r\n'
            textlines[num + 10] = b'  b20a @0169 [/,4b] = ' + ["Pop", "Pop", "Pop", "Pop", "Pop", "ポップス", "팝"][
                nameIndex].encode("utf-8") + b'\r\n'
            textlines[num + 11] = b'  b20b @016a [/,4b] = ' + \
                                  ["Japanese", "Japonais", "Japonés", "Japanisch", "Giapponese", "和風", "일본 음악"][
                                      nameIndex].encode("utf-8") + b'\r\n'
            break
    return textlines