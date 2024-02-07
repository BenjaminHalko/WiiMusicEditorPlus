from enum import Enum
from shutil import rmtree

from wii_music_editor.data.instruments import instrumentList
from wii_music_editor.data.region import regionNames, regionFullNames
from wii_music_editor.data.songs import songList
from wii_music_editor.data.styles import styleList
from wii_music_editor.editor.message import TextClass
from wii_music_editor.editor.rom import ConvertRom
from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.editor.region import regionSelected, BasedOnRegion


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
        if not paths.loadedFile.is_dir():
            ConvertRom()
        self.GetRegion()
        self.text = TextClass(paths.message)


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
