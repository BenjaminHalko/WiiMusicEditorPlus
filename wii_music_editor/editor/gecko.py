import os
from shutil import copyfile

from wii_music_editor.data.region import getGameID
from wii_music_editor.utils import paths
from wii_music_editor.utils.save import load_setting


gctRegionOffsets = [0, 0x200, -0x35F0, -0x428E8]
gctRegionOffsetsStyles = [0, 0x200, -0x3420, -0x25320]


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


def AddPatch(patch_name, patch_info):
    if type(patch_name) is str:
        patch_name = [patch_name]
        patch_info = [patch_info]

    for patchNum in range(len(patch_name)):
        if paths.geckoPath.exists():
            with open(str(paths.geckoPath), 'r') as codes:
                line_text = codes.readlines()

            gecko_exists = -1
            song_exists = -1
            gecko_enabled = -1
            song_enabled = -1
            for num in range(len(line_text)):
                if line_text[num].rstrip() == '[Gecko]':
                    gecko_exists = num
                if line_text[num].rstrip() == f'${patch_name[patchNum]} [WiiMusicEditor]':
                    song_exists = num

            if gecko_exists == -1:
                line_text.insert(0, f'[Gecko]\n${patch_name[patchNum]} [WiiMusicEditor]\n{patch_info[patchNum]}')
            elif song_exists == -1:
                line_text.insert(gecko_exists + 1, f'${patch_name[patchNum]} [WiiMusicEditor]\n{patch_info[patchNum]}')
            else:
                while True:
                    if len(line_text) <= song_exists + 1:
                        break
                    elif not line_text[song_exists + 1][0].isnumeric() and (line_text[song_exists + 1][0] != 'f'):
                        break
                    else:
                        line_text.pop(song_exists + 1)
                line_text.insert(song_exists + 1, patch_info[patchNum])

            for num in range(len(line_text)):
                if line_text[num].rstrip() == '[Gecko_Enabled]':
                    gecko_enabled = num
                if line_text[num].rstrip() == f'${patch_name[patchNum]}':
                    song_enabled = num

            if gecko_enabled == -1:
                line_text.insert(len(line_text), f'[Gecko_Enabled]\n${patch_name[patchNum]}\n')
            elif song_enabled == -1:
                line_text.insert(gecko_enabled + 1, f'${patch_name[patchNum]}\n')

            with open(str(paths.geckoPath), 'w') as codes:
                codes.writelines(line_text)
        else:
            with open(str(paths.geckoPath), 'w') as codes:
                codes.write('[Gecko]\n')
                codes.write('$' + patch_name[patchNum] + ' [WiiMusicEditor]\n')
                codes.write(patch_info[patchNum])
                codes.write('[Gecko_Enabled]\n')
                codes.write('$' + patch_name[patchNum] + '\n')

    # Copy Code to Dolphin
    if load_setting("Settings", "CopyCodes", True):
        game_id = getGameID()
        if paths.dolphinSavePath.is_dir():
            if (paths.dolphinPath/"GameSettings"/game_id + ".ini").is_file():
                if not (paths.dolphinPath/"GameSettings"/game_id + ".backup.ini").is_file():
                    copyfile(str(paths.dolphinPath/"GameSettings"/game_id + ".ini"),
                             str(paths.dolphinPath/"GameSettings"/game_id + ".backup.ini"))
                os.remove(str(paths.dolphinPath/"GameSettings"/game_id + ".ini"))
            copyfile(paths.geckoPath, str(paths.dolphinPath/"GameSettings"/game_id + ".ini"))


