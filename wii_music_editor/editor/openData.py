from enum import Enum
from shutil import rmtree

from wii_music_editor.data.instruments import instrumentList
from wii_music_editor.data.region import regionNames, regionFullNames
from wii_music_editor.data.songs import songList, SongType
from wii_music_editor.data.styles import styleList
from wii_music_editor.editor.message import DecodeTxt, TextClass
from wii_music_editor.editor.rom import ConvertRom
from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.editor.region import regionSelected, BasedOnRegion


class LoadType(Enum):
    Rom = 0
    Brsar = 1
    Message = 2
    Dol = 3
    Midi = 4
    Gct = 5
    RomFile = 6


class RecordType(Enum):
    Song = "song"
    Style = "style"
    TextSong = "textsong"
    TextStyle = "textstyle"
    DefaultStyle = "defaultstyle"
    RemoveSong = "removesong"
    MainDol = "maindol"


class OpenData:
    styles = [[]] * len(styleList)
    text: TextClass
    region = 0
    codes = []
    type: LoadType

    def GetRegion(self):
        for i in range(len(regionNames)):
            if (paths.rom / "files" / regionNames[i][0] / "Message").is_dir():
                self.region = i
                return
        ShowError("Could not determine region", f"Using fallback region: {BasedOnRegion(regionFullNames)}")
        self.region = regionSelected

    def GetStyles(self):
        self.styles = [[]] * len(styleList)
        for i in range(len(styleList)):
            self.styles[i] = styleList[i].DefaultStyle

            for j in range(len(self.codes)):
                if ("Style Patch [WiiMusicEditor]" in self.codes[
                    i] and "Default Style Patch [WiiMusicEditor]" not in
                        self.codes[i]):
                    for j in range(len(styleList)):
                        if styleList[j].Name == self.codes[i][1:len(self.codes[i]) - 30:1]:
                            self.styles[j] = [
                                min(int(self.codes[i + 2][6:8:1], 16), len(instrumentList) - 1),
                                min(int(self.codes[i + 2][15:17:1], 16), len(instrumentList) - 1),
                                min(int(self.codes[i + 3][6:8:1], 16), len(instrumentList) - 1),
                                min(int(self.codes[i + 3][15:17:1], 16), len(instrumentList) - 1),
                                min(int(self.codes[i + 4][6:8:1], 16), len(instrumentList) - 1),
                                min(int(self.codes[i + 4][15:17:1], 16), len(instrumentList) - 1)]
                            break

    def GetGecko(self):
        self.codes = []
        if paths.geckoPath.exists():
            with open(str(paths.geckoPath)) as file:
                self.codes = file.readlines()

    def GetText(self):
        self.text = TextClass()
        DecodeTxt()
        with open(f'{paths.messagePath}/message.d/new_music_message.txt', 'rb') as message:
            textlines = message.readlines()

        rmtree(f'{paths.messagePath}/message.d')
        for i in range(3):
            for SongToChange in range(len(songList) - 1):
                text_offset = ['c8', '190', '12c']
                number_to_change = songList[SongToChange].MemOrder
                if songList[SongToChange].SongType == SongType.Maestro:
                    text_offset = ['fa', '1c2', '15e']
                    array = [0, 4, 2, 3, 1]
                    number_to_change = array[number_to_change]
                elif songList[SongToChange].SongType == SongType.Hand_Bell:
                    text_offset = ['ff', '1c7', '163']
                    array = [0, 2, 3, 1, 4]
                    number_to_change = array[number_to_change]
                offset = format(int(text_offset[i], 16) + number_to_change, 'x').lower()
                offset = ' ' * (4 - len(offset)) + offset + '00 @'
                for num in range(len(textlines)):
                    if offset in str(textlines[num]):
                        text_to_add = (self.codes[num][22:len(self.codes[num]) - 2:1]).decode("utf-8")
                        for number in range(num + 1, len(self.codes)):
                            if bytes('@', 'utf-8') in self.codes[number]:
                                break
                            text_to_add = text_to_add[0:len(text_to_add) - 2:1] + "\n" + (
                                self.codes[number][3:len(self.codes[number]) - 2:1]).decode("utf-8")
                        self.text[i].append(text_to_add)
                        break
        text_offset = "b200"
        array = [3, 1, 4, 2, 7, 10, 11, 9, 8, 6, 5]
        for i in range(11):
            number_to_change = array[i]
            offset = format(int(text_offset, 16) + number_to_change, 'x').lower()
            offset = ' ' * (4 - len(offset)) + offset + ' @'
            for num in range(len(textlines)):
                if offset in str(textlines[num]):
                    text_to_add = (self.codes[num][22:len(textlines[num]) - 2:1]).decode("utf-8")
                    for number in range(num + 1, len(self.codes)):
                        if bytes('@', 'utf-8') in self.codes[number]:
                            break
                        text_to_add = text_to_add[0:len(text_to_add) - 2:1] + "\n" + (
                            self.codes[number][3:len(self.codes[number]) - 2:1]).decode("utf-8")
                    self.text[3].append(text_to_add)
                    break

    def GetDefaultStyle(self, song_id, default):
        style = songList[song_id].DefaultStyle

        if not default and paths.geckoPath.exists():
            for i in range(len(self.codes)):
                if self.codes[i] == "$" + songList[song_id].Name + " Default Style Patch [WiiMusicEditor]\n":
                    style = self.codes[i + 1][15:17:1]

        for i in range(len(styleList)):
            if styleList[i].StyleId == style:
                return i

        return -1

    def PrepareFile(self):
        # Set file type
        if paths.loadedFile.is_dir():
            self.type = LoadType.Rom
        else:
            extension = paths.loadedFile.suffix
            if extension == ".brsar":
                self.type = LoadType.Brsar
            elif extension == ".carc":
                self.type = LoadType.Message
            elif extension == ".midi" or extension == ".mid" or extension == ".brseq" or extension == ".rseq":
                self.type = LoadType.Midi
            elif extension == ".dol":
                self.type = LoadType.Dol
            elif extension == ".gct" or extension == ".ini":
                self.type = LoadType.Gct
            else:
                self.type = LoadType.RomFile

        # Load file
        if self.type == LoadType.RomFile:
            ConvertRom()
        if self.type == LoadType.Rom:
            self.GetRegion()
        if self.type == LoadType.Rom or self.type == LoadType.Message:
            # TODO
            # GetSongNames()
            print("?")


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


openData = OpenData()
