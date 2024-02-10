import os
from shutil import copyfile

from wii_music_editor.data.region import game_ids
from wii_music_editor.editor.region import BasedOnRegion
from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.utils.preferences import preferences
from wii_music_editor.utils.save import load_setting


gctRegionOffsets = [0, 0x200, -0x35F0, -0x428E8]
gctRegionOffsetsStyles = [0, 0x200, -0x3420, -0x25320]
rapperPatches = [
    '043b0bc0 60000000\n043b0bec 4e800020\n',
    '043B0CCF 881C0090\n043B0CD3 7C090000\n043B0BC3 4081FFBC\n043B0CD7 881C00D6\n',
    '043AE47F 881C0090\n043AE483 7C090000\n043AE487 4081FFBC\n043AE48B 881C00D6\n',
    '0429CE7B 881C0090\n0429CE7F 7C090000\n0429CE83 4081FFBC\n0429CE87 881C00D6\n'
]


class Patch:
    name: str
    info: str

    def __init__(self, name: str, info: str):
        self.name = name
        self.info = info


def CreateGct(path, gecko_path=""):
    if gecko_path == "":
        gecko_path = paths.geckoPath

    with open(gecko_path) as patches:
        textlines = patches.readlines()

    codes = '00D0C0DE00D0C0DE'
    for text in textlines:
        if text[0].isalpha() or text[0].isnumeric():
            codes = codes + text.replace(' ', '').strip()
    codes = codes + 'F000000000000000'

    with open(path, 'wb') as patch:
        patch.write(bytes.fromhex(codes))


def AddPatch(patches: list[Patch]):
    for patch in patches:
        if paths.geckoPath.exists():
            with open(str(rom_folder.geckoPath), 'r') as codes:
                line_text = codes.readlines()

            gecko_exists = -1
            song_exists = -1
            gecko_enabled = -1
            song_enabled = -1
            for num in range(len(line_text)):
                if line_text[num].rstrip() == '[Gecko]':
                    gecko_exists = num
                if line_text[num].rstrip() == f'${patch.name} [WiiMusicEditor]':
                    song_exists = num

            if gecko_exists == -1:
                line_text.insert(0, f'[Gecko]\n${patch.name} [WiiMusicEditor]\n{patch.info}')
            elif song_exists == -1:
                line_text.insert(gecko_exists + 1, f'${patch.name} [WiiMusicEditor]\n{patch.info}')
            else:
                while True:
                    if len(line_text) <= song_exists + 1:
                        break
                    elif not line_text[song_exists + 1][0].isnumeric() and (line_text[song_exists + 1][0] != 'f'):
                        break
                    else:
                        line_text.pop(song_exists + 1)
                line_text.insert(song_exists + 1, patch.info)

            for num in range(len(line_text)):
                if line_text[num].rstrip() == '[Gecko_Enabled]':
                    gecko_enabled = num
                if line_text[num].rstrip() == f'${patch.name}':
                    song_enabled = num

            if gecko_enabled == -1:
                line_text.insert(len(line_text), f'[Gecko_Enabled]\n${patch.name}\n')
            elif song_enabled == -1:
                line_text.insert(gecko_enabled + 1, f'${patch.name}\n')

            with open(str(rom_folder.geckoPath), 'w') as codes:
                codes.writelines(line_text)
        else:
            with open(str(rom_folder.geckoPath), 'w') as codes:
                codes.write('[Gecko]\n')
                codes.write('$' + patch.name + ' [WiiMusicEditor]\n')
                codes.write(patch.info)
                codes.write('[Gecko_Enabled]\n')
                codes.write('$' + patch.name + '\n')

    # Copy Code to Dolphin
    if preferences.copy_gecko_codes:
        game_id = BasedOnRegion(game_ids)
        if paths.dolphinSavePath.is_dir():
            if (paths.dolphinPath/"GameSettings"/game_id + ".ini").is_file():
                if not (paths.dolphinPath/"GameSettings"/game_id + ".backup.ini").is_file():
                    copyfile(str(paths.dolphinPath/"GameSettings"/game_id + ".ini"),
                             str(paths.dolphinPath/"GameSettings"/game_id + ".backup.ini"))
                os.remove(str(paths.dolphinPath/"GameSettings"/game_id + ".ini"))
            copyfile(rom_folder.geckoPath, str(paths.dolphinPath/"GameSettings"/game_id + ".ini"))


