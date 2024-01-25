import os
from pathlib import Path
from shutil import rmtree, copyfile

from wii_music_editor.data.songs import songList, SongTypeValue
from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.utils.paths import paths
from wii_music_editor.utils.shell import run_shell


def DecodeTxt():
    try:
        if (paths.messagePath / "message.d").is_dir():
            rmtree(f"{paths.messagePath}/message.d")
        run_shell([str(paths.includePath / 'wiimms' / 'wszst'), 'extract', str(paths.messagePath / 'message.carc')])
        os.remove(f"{paths.messagePath}/message.d/wszst-setup.txt")
        run_shell([str(paths.includePath / 'wiimms' / 'wbmgt'), 'decode',
                   str(paths.messagePath / 'message.d' / 'new_music_message.bmg')])
        os.remove(f"{paths.messagePath}/message.d/new_music_message.bmg")
    except Exception as e:
        ShowError("Could not decode text file", str(e))


def EncodeTxt():
    try:
        run_shell([str(paths.includePath / 'wiimms' / 'wbmgt'), 'encode',
                   str(paths.messagePath / 'message.d' / 'new_music_message.txt')])
        os.remove(f"{paths.messagePath}/message.d/new_music_message.txt")
        if not Path(paths.messagePath / "message.carc.backup").exists():
            copyfile(f"{paths.messagePath}/message.carc", f"{paths.messagePath}/message.carc.backup")
        os.remove(f"{paths.messagePath}/message.carc")
        run_shell([str(paths.includePath / 'wiimms' / 'wszst'), 'create', str(paths.messagePath / 'message.d'),
                   '--dest', str(paths.messagePath / 'message.carc')])
        rmtree(f'{paths.messagePath}/message.d')
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


def ChangeName(song_number, new_text):
    song_to_change = songList[song_number]
    text_offset = []
    if type(new_text) is not str:
        if song_to_change.SongType == SongTypeValue.Regular:
            text_offset = ['c8', '190', '12c']
        elif song_to_change.SongType == SongTypeValue.Maestro:
            text_offset = ['fa', '1c2', '15e']
        elif song_to_change == SongTypeValue.Hand_Bell:
            text_offset = ['ff', '1c7', '163']
        textFromTxt[0][song_number] = new_text[0]
        textFromTxt[1][song_number] = new_text[1]
        textFromTxt[2][song_number] = new_text[2]
    else:
        text_offset = ['b200']
    DecodeTxt()

    # Write the new text to the file
    for typeNum in range(3):
        with open(f'{paths.messagePath}/message.d/new_music_message.txt', 'rb') as message:
            textlines = message.readlines()

        if type(new_text) is not str:
            number_to_change = song_to_change.MemOrder
            if song_to_change.SongType == SongTypeValue.Maestro:
                array = [0, 4, 2, 3, 1]
                number_to_change = array[number_to_change]
            elif song_to_change.SongType == SongTypeValue.Hand_Bell:
                array = [0, 2, 3, 1, 4]
                number_to_change = array[number_to_change]
        else:
            array = [3, 1, 4, 2, 7, 10, 11, 9, 8, 6, 5]
            number_to_change = array[song_number]

        offset = format(int(text_offset[typeNum], 16) + number_to_change, 'x').lower()
        if type(new_text) is not str:
            offset = ' ' * (4 - len(offset)) + offset + '00 @'
        else:
            offset = ' ' * (4 - len(offset)) + offset + ' @'
        textlines = FixMessageFile(textlines)
        for num in range(len(textlines)):
            if offset in str(textlines[num]):
                while bytes('@', 'utf-8') not in textlines[num + 1]:
                    textlines.pop(num + 1)

                if type(new_text) is str:
                    text = repr(new_text).strip("'").replace(r"\'", "'").strip("\"")
                else:
                    text = repr(new_text[typeNum]).strip("'").replace(r"\'", "'").strip("\"")
                textlines[num] = bytes(offset + str(textlines[num])[10:24:1] + text + '\r\n', 'utf-8')
                break

        with open(f'{paths.messagePath}/message.d/new_music_message.txt', 'rb') as message:
            message.writelines(textlines)

        if type(new_text) is str:
            break

    EncodeTxt()
