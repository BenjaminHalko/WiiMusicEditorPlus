from shutil import rmtree

from wii_music_editor.data.instruments import instrumentList
from wii_music_editor.data.region import regionNames, regionFullNames
from wii_music_editor.data.songs import songList, SongTypeValue
from wii_music_editor.data.styles import styleList
from wii_music_editor.editor.message import DecodeTxt
from wii_music_editor.editor.rom import ConvertRom
from wii_music_editor.ui.views.error_handler.error_handler import ShowError
from wii_music_editor.utils import paths
from wii_music_editor.editor.region import regionSelected, BasedOnRegion


class LoadType:
    Rom = 0
    Brsar = 1
    Message = 2
    Dol = 3
    Midi = 4
    Gct = 5
    RomFile = 6

class RecordType:
    Song = "song"
    Style = "style"
    TextSong = "textsong"
    TextStyle = "textstyle"
    DefaultStyle = "defaultstyle"
    RemoveSong = "removesong"
    MainDol = "maindol"


loadedStyles = [[]] * len(styleList)
loadedText = ""
loadedRegion = 0
loadedCodes = []
loadedFileType = 0


def SaveRecording(action, name, values, remove=False):
    if (file.type == LoadType.Rom):
        if (type(values[0]) != list):
            values = [values]
        section = action + "-" + str(name)
        ini = ConfigParser()
        ini.read(file.path + "/Changes.ini")
        if (ini.has_section(section)): ini.remove_section(section)
        if (not remove):
            ini.add_section(section)
            for value in values:
                ini.set(section, value[0], str(value[1]))
        with open(file.path + "/Changes.ini", 'w') as inifile:
            ini.write(inifile)


def GetStyles():
    global loadedStyles
    loadedStyles = [[]] * len(styleList)
    for i in range(len(styleList)):
        loadedStyles[i] = styleList[i].DefaultStyle

        for j in range(len(loadedCodes)):
            if ("Style Patch [WiiMusicEditor]" in loadedCodes[i] and "Default Style Patch [WiiMusicEditor]" not in
                    loadedCodes[i]):
                for j in range(len(styleList)):
                    if styleList[j].Name == loadedCodes[i][1:len(loadedCodes[i]) - 30:1]:
                        loadedStyles[j] = [
                            min(int(loadedCodes[i + 2][6:8:1], 16), len(instrumentList) - 1),
                            min(int(loadedCodes[i + 2][15:17:1], 16), len(instrumentList) - 1),
                            min(int(loadedCodes[i + 3][6:8:1], 16), len(instrumentList) - 1),
                            min(int(loadedCodes[i + 3][15:17:1], 16), len(instrumentList) - 1),
                            min(int(loadedCodes[i + 4][6:8:1], 16), len(instrumentList) - 1),
                            min(int(loadedCodes[i + 4][15:17:1], 16), len(instrumentList) - 1)]
                        break


def GetRegion():
    global loadedRegion
    for i in range(len(regionNames)):
        if (paths.romPath / "files" / regionNames[i][0] / "Message").is_dir():
            loadedRegion = i
            return
    ShowError("Could not determine region", f"Using fallback region: {BasedOnRegion(regionFullNames)}")
    loadedRegion = regionSelected


def GetGecko():
    global loadedCodes

    loadedCodes = []
    if paths.geckoPath.exists():
        with open(str(paths.geckoPath)) as file:
            loadedCodes = file.readlines()


def GetText():
    global loadedText

    loadedText = [[], [], [], []]
    DecodeTxt()
    with open(f'{paths.messagePath}/message.d/new_music_message.txt', 'rb') as message:
        textlines = message.readlines()

    rmtree(f'{paths.messagePath}/message.d')
    for i in range(3):
        for SongToChange in range(len(songList) - 1):
            text_offset = ['c8', '190', '12c']
            number_to_change = songList[SongToChange].MemOrder
            if songList[SongToChange].SongType == SongTypeValue.Maestro:
                text_offset = ['fa', '1c2', '15e']
                array = [0, 4, 2, 3, 1]
                number_to_change = array[number_to_change]
            elif songList[SongToChange].SongType == SongTypeValue.Hand_Bell:
                text_offset = ['ff', '1c7', '163']
                array = [0, 2, 3, 1, 4]
                number_to_change = array[number_to_change]
            offset = format(int(text_offset[i], 16) + number_to_change, 'x').lower()
            offset = ' ' * (4 - len(offset)) + offset + '00 @'
            for num in range(len(textlines)):
                if offset in str(textlines[num]):
                    text_to_add = (loadedCodes[num][22:len(loadedCodes[num]) - 2:1]).decode("utf-8")
                    for number in range(num + 1, len(loadedCodes)):
                        if bytes('@', 'utf-8') in loadedCodes[number]: break
                        text_to_add = text_to_add[0:len(text_to_add) - 2:1] + "\n" + (
                            loadedCodes[number][3:len(loadedCodes[number]) - 2:1]).decode("utf-8")
                    loadedText[i].append(text_to_add)
                    break
    text_offset = "b200"
    array = [3, 1, 4, 2, 7, 10, 11, 9, 8, 6, 5]
    for i in range(11):
        number_to_change = array[i]
        offset = format(int(text_offset, 16) + number_to_change, 'x').lower()
        offset = ' ' * (4 - len(offset)) + offset + ' @'
        for num in range(len(textlines)):
            if offset in str(textlines[num]):
                text_to_add = (loadedCodes[num][22:len(textlines[num]) - 2:1]).decode("utf-8")
                for number in range(num + 1, len(loadedCodes)):
                    if bytes('@', 'utf-8') in loadedCodes[number]: break
                    text_to_add = text_to_add[0:len(text_to_add) - 2:1] + "\n" + (
                        loadedCodes[number][3:len(loadedCodes[number]) - 2:1]).decode("utf-8")
                loadedText[3].append(text_to_add)
                break


def GetDefaultStyle(song_id, default):
    style = songList[song_id].DefaultStyle

    if not default and paths.geckoPath.exists():
        for i in range(len(loadedCodes)):
            if loadedCodes[i] == "$" + songList[song_id].Name + " Default Style Patch [WiiMusicEditor]\n":
                style = loadedCodes[i + 1][15:17:1]

    for i in range(len(styleList)):
        if styleList[i].StyleId == style:
            return i

    return -1


def GetFileType():
    if paths.loadedFilePath.is_dir():
        return LoadType.Rom

    extension = paths.loadedFilePath.suffix
    if extension == ".brsar":
        return LoadType.Brsar
    elif extension == ".carc":
        return LoadType.Message
    elif extension == ".midi" or extension == ".mid" or extension == ".brseq" or extension == ".rseq":
        return LoadType.Midi
    elif extension == ".dol":
        return LoadType.Dol
    elif extension == ".gct" or extension == ".ini":
        return LoadType.Gct

    return LoadType.RomFile


def PrepareFile():
    global loadedFileType
    loadedFileType = GetFileType()
    if loadedFileType == LoadType.RomFile:
        ConvertRom()
    if loadedFileType == LoadType.Rom:
        GetRegion()
    if loadedFileType == LoadType.Rom or loadedFileType == LoadType.Message:
        # TODO
        # GetSongNames()
        print("?")
