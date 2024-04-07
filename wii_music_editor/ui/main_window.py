import os
from pathlib import Path
from shutil import copyfile, rmtree
import zipfile
import webbrowser

from PySide6.QtWidgets import QMainWindow, QComboBox

from wii_music_editor.data.region import RegionType
from wii_music_editor.editor.rom import ConvertRom
from wii_music_editor.ui.settings import SettingsWindow
from wii_music_editor.ui.update import UpdateWindow
from wii_music_editor.ui.warning import show_warning
from wii_music_editor.ui.widgets.verify_rom import verify_rom_folder
from wii_music_editor.utils.logger import is_debug
from wii_music_editor.utils.update import CheckForUpdate, GetLatestVersion

from wii_music_editor.data.instruments import instrument_list
from wii_music_editor.data.songs import SongType, song_list
from wii_music_editor.data.styles import get_style_by_id, style_list, StyleType, StyleInstruments
from wii_music_editor.editor.editor import replace_song, replace_song_text, replace_style, replace_style_text, \
    get_original_song, replace_default_style
from wii_music_editor.editor.midi import Midi
from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.services.discord import discord_presence, DiscordState
from wii_music_editor.services.external_editor import ExternalEditor
from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.ui.pack_rom import PackRomWindow
from wii_music_editor.ui.revert_changes import RevertChangesWindow
from wii_music_editor.ui.riivolution import RiivolutionWindow
from wii_music_editor.ui.widgets.dolphin import LoadDolphin, CopySaveFileToDolphin
from wii_music_editor.ui.widgets.load_files import get_file_path, select_rom_path
from wii_music_editor.ui.widgets.populate_list_widget import populate_song_list, populate_style_list, \
    populate_instrument_list, get_style_list_index, set_style_list_index
from wii_music_editor.ui.widgets.translate import tr
from wii_music_editor.ui.windows.main_window_ui import Ui_MainWindow
from wii_music_editor.utils.preferences import preferences
from wii_music_editor.utils.save import load_setting, save_setting
from wii_music_editor.utils.version import GetCurrentVersion


# Load Places
class TAB:
    MainMenu = 0
    SongEditor = 1
    StyleEditor = 2
    TextEditor = 3
    DefaultStyleEditor = 4
    RemoveSongEditor = 5
    SoundEditor = 6


# Main Window
class MainWindow(QMainWindow, Ui_MainWindow):
    externalEditorOpen: bool
    textEditor: ExternalEditor
    fromSongEditor: int

    __SE_midiScore: Midi or None
    __SE_midiSong: Midi or None

    __StE_styleSelected: StyleInstruments

    def __init__(self):
        super().__init__(None)
        self.setupUi(self)
        self.externalEditorOpen = False
        self.fromSongEditor = -1

        # Load folder
        rom_folder_path = load_setting("Paths", "CurrentLoadedFile", "")
        if rom_folder_path != "":
            rom_folder.load(Path(rom_folder_path))
            self.LoadRomInfo()
            if not rom_folder.loaded:
                ShowError("Error", "Unable to load rom folder")

        # Menu Bar Buttons
        self.menuBar().setNativeMenuBar(False)
        self.MB_LoadFile.triggered.connect(self.MenuBar_Load_Rom)
        self.MB_LoadFolder.triggered.connect(self.MenuBar_Load_RomFolder)
        self.MB_Settings.triggered.connect(self.MenuBar_Load_Settings)
        self.MB_Updates.triggered.connect(self.MenuBar_CheckForUpdates)
        self.MB_Dolphin.triggered.connect(lambda: LoadDolphin(False))
        self.MB_DolphinMenu.triggered.connect(lambda: LoadDolphin(True))
        self.MB_DownloadSongs.triggered.connect(lambda: webbrowser.open(
                "https://github.com/BenjaminHalko/Pre-Made-Songs-for-Wii-Music/archive/refs/heads/main.zip"))
        self.MB_SaveFile.triggered.connect(CopySaveFileToDolphin)
        self.MB_Help.triggered.connect(lambda: webbrowser.open(
            "https://github.com/BenjaminHalko/WiiMusicEditorPlus/wiki"))
        self.MB_Donate.triggered.connect(lambda: webbrowser.open("https://ko-fi.com/benjaminhalko"))
        self.MB_Discord.triggered.connect(lambda: webbrowser.open("https://discord.gg/NC3wYAeCDs"))

        # Main Menu Buttons
        self.MP_SongEditor_Button.clicked.connect(self.LoadSongEditor)
        self.MP_StyleEditor_Button.clicked.connect(self.LoadStyleEditor)

        self.MP_EditText_Button.clicked.connect(self.LoadTextEditor)
        self.MP_DefaultStyle_Button.clicked.connect(self.LoadDefaultStyleEditor)
        self.MP_RemoveSong_Button.clicked.connect(self.LoadRemoveSongEditor)

        self.MP_Riivolution_Button.clicked.connect(lambda: RiivolutionWindow())
        self.MP_PackRom_Button.clicked.connect(lambda: PackRomWindow())

        self.MP_RevertChanges_Button.clicked.connect(lambda: RevertChangesWindow())
        self.MP_ImportFiles_Button.clicked.connect(self.ImportFiles)
        self.MP_ExportFiles_Button.clicked.connect(self.ExportFiles)
        self.MP_ImportChanges_Button.clicked.connect(self.ImportChanges)

        # Song Editor Buttons
        self.SE_Midi_File_Score_Button.clicked.connect(self.Button_SE_SongToChange)
        self.SE_Midi_File_Song_Button.clicked.connect(lambda: self.Button_SE_SongToChange(True))
        self.SE_Midi_TimeSignature_4.toggled.connect(self.Button_SE_Midi_TimeSignature)
        self.SE_Midi_Length_Measures.toggled.connect(self.Button_SE_Midi_Length)
        self.SE_SongToChange.itemSelectionChanged.connect(self.List_SE_SongToChange)
        self.SE_Midi_Tempo_Input.valueChanged.connect(self.SE_Patchable)
        self.SE_Midi_Length_Input.valueChanged.connect(self.SE_Patchable)
        self.SE_Midi_File_Replace_Song.toggled.connect(self.SE_Patchable)
        self.SE_Patch.clicked.connect(self.Button_SE_Patch)
        self.SE_Back_Button.clicked.connect(self.GotoMainMenu)
        self.SE_ChangeSongText_Name_Input.textEdited.connect(self.SE_Patchable)
        self.SE_ChangeSongText_Desc_Input.textChanged.connect(self.SE_Patchable)
        self.SE_ChangeSongText_Genre_Input.textEdited.connect(self.SE_Patchable)
        self.SE_Midi.toggled.connect(self.SE_Patchable)
        self.SE_OpenStyleEditor.clicked.connect(self.Button_SE_OpenStyleEditor)
        self.SE_OpenDefaultStyleEditor.clicked.connect(self.Button_SE_OpenDefaultStyleEditor)
        self.SE_ResetButton.clicked.connect(self.Button_SE_ResetSong)

        # Style Editor Buttons
        self.StE_Back_Button.clicked.connect(self.GotoMainMenu)
        self.StE_PartSelector.currentIndexChanged.connect(self.Button_StE_PartSelector)
        self.StE_InstrumentList.itemSelectionChanged.connect(self.List_StE_InstrumentList)
        self.StE_StyleList.itemSelectionChanged.connect(self.List_StE_StyleList)
        self.StE_ResetStyle.clicked.connect(self.Button_StE_ResetStyle)
        self.StE_Patch.clicked.connect(self.Button_StE_Patch)
        self.StE_ChangeStyleName.textEdited.connect(self.StE_Patchable)

        # Text Editor Buttons
        self.TE_Back_Button.clicked.connect(self.GotoMainMenu)
        self.TE_Patch.clicked.connect(self.Button_TE_Patch)
        self.TE_OpenExternal.clicked.connect(self.Button_TE_ExternalEditor)
        self.TE_Text.textChanged.connect(self.TE_Text_Editor)

        # Default Style Editor
        self.DS_Back_Button.clicked.connect(self.GotoMainMenu)
        self.DS_Patch.clicked.connect(self.Button_DS_Patch)
        self.DS_Songs.itemSelectionChanged.connect(self.List_DS_SongList)
        self.DS_Styles.itemSelectionChanged.connect(self.List_DS_StyleList)
        self.DS_Reset.clicked.connect(self.Button_DS_Reset)

        # Remove Song Editor
        self.RS_Back_Button.clicked.connect(self.GotoMainMenu)
        self.RS_RemoveCustomSongs.clicked.connect(self.Button_RS_RemoveCustomSongs)
        self.RS_Deselect_Button.clicked.connect(self.Button_RS_DeselectAll)
        self.RS_Patch.clicked.connect(self.Button_RS_Purge)

        # Show Main Window
        self.show()

        # Check for updates
        try:
            local_version = GetCurrentVersion()
            if is_debug():
                self.setWindowTitle(f"Wii Music Editor Plus - Debug Build")
            else:
                self.setWindowTitle(f"Wii Music Editor Plus - v{local_version}")
            if preferences.auto_update:
                latest_version = GetLatestVersion()
                if CheckForUpdate(local_version, latest_version):
                    UpdateWindow(self, local_version, latest_version)
        except Exception as e:
            print("Could Not Update:", e)

        # Verify Rom Folder
        verify_rom_folder()

    def LoadRomInfo(self):
        if rom_folder.loaded:
            self.MP_LoadedFile_Path.setText(str(rom_folder.folderPath))
            regionNames = [
                tr("region", "US"),
                tr("region", "Europe"),
                tr("region", "Japan"),
                tr("region", "Korea"),
            ]
            self.MP_Rom_Region.setText(regionNames[rom_folder.region])
            languages = [
                tr("language", "English"),
                tr("language", "French"),
                tr("language", "Spanish"),
                tr("language", "German"),
                tr("language", "Italian"),
                tr("language", "Japanese"),
                tr("language", "Korean"),
            ]
            self.MP_Language.clear()
            if rom_folder.region == RegionType.US:
                self.MP_Language.addItems(languages[:3])
                self.MP_Language.setCurrentIndex(min(preferences.rom_language, 2))
            elif rom_folder.region == RegionType.Europe:
                self.MP_Language.addItems(languages[:5])
                self.MP_Language.setCurrentIndex(min(preferences.rom_language, 4))
            elif rom_folder.region == RegionType.Japan:
                self.MP_Language.addItem(languages[5])
            elif rom_folder.region == RegionType.Korea:
                self.MP_Language.addItem(languages[6])
            self.MP_Language.currentIndexChanged.connect(self.SetLangauge)
            self.MP_Language.setEnabled(True)

            if rom_folder.region != RegionType.US:
                show_warning("Only US rom is supported in the beta version currently."
                             "\nSupport for other regions will be added in the future.", "us_only")

        else:
            self.MP_LoadedFile_Path.setText(tr("error", "Error Loading File"))
            self.MP_Rom_Region.setText("")
            self.MP_Language.clear()
            self.MP_Language.setEnabled(False)

    def SetLangauge(self):
        if preferences.rom_language != self.MP_Language.currentIndex():
            preferences.rom_language = self.MP_Language.currentIndex()
            save_setting("preferences", "rom_language", self.MP_Language.currentIndex())
            rom_folder.load_text()

    def GotoMainMenu(self):
        if self.fromSongEditor != -1:
            self.MainWidget.setCurrentIndex(TAB.SongEditor)
            self.fromSongEditor = -1
        else:
            self.MainWidget.setCurrentIndex(TAB.MainMenu)
            discord_presence.update(DiscordState.ModdingWiiMusic)

    def LoadSongEditor(self):
        self.MainWidget.setCurrentIndex(TAB.SongEditor)
        populate_song_list(self.SE_SongToChange)
        self.SE_Midi.setEnabled(False)
        self.SE_Midi.setCheckable(False)
        self.SE_ChangeSongText.setEnabled(False)
        self.SE_Patch.setEnabled(False)
        self.SE_StyleBox.setEnabled(False)
        self.SE_OpenDefaultStyleEditor.setEnabled(False)
        self.SE_OpenStyleEditor.setEnabled(False)
        self.SE_ResetButton.setEnabled(False)
        self.SE_Midi_File_Score_Label.setText(tr("main", "Load a Midi-Type file"))
        self.SE_Midi_File_Song_Label.setText(tr("main", "Load a Midi-Type file"))
        self.__SE_midiScore = None
        self.__SE_midiSong = None
        discord_presence.update(DiscordState.EditingSongs)

    def LoadStyleEditor(self):
        self.MainWidget.setCurrentIndex(TAB.StyleEditor)
        populate_style_list(self.StE_StyleList, self.fromSongEditor)
        populate_instrument_list(self.StE_InstrumentList)
        self.StE_Instruments.setEnabled(False)
        self.StE_ChangeStyleName.setEnabled(False)
        self.StE_ChangeStyleName_Label.setEnabled(False)
        self.StE_ResetStyle.setEnabled(False)
        self.StE_Patch.setEnabled(False)
        discord_presence.update(DiscordState.EditingStyles)
        if self.fromSongEditor != -1:
            set_style_list_index(self.StE_StyleList, self.fromSongEditor)
            self.List_StE_StyleList()

    def LoadTextEditor(self):
        self.TE_Text.setPlainText(rom_folder.text.to_text())
        self.MainWidget.setCurrentIndex(TAB.TextEditor)
        self.TE_Patch.setEnabled(False)
        discord_presence.update(DiscordState.EditingText)

    def LoadDefaultStyleEditor(self):
        self.MainWidget.setCurrentIndex(TAB.DefaultStyleEditor)
        populate_song_list(self.DS_Songs, [SongType.Regular], self.fromSongEditor)
        populate_style_list(self.DS_Styles)
        self.DS_StyleBox.setEnabled(False)
        self.DS_Patch.setEnabled(False)
        if self.fromSongEditor != -1:
            self.DS_Songs.setCurrentRow(self.fromSongEditor)
            self.List_DS_SongList()
        discord_presence.update(DiscordState.EditingDefaultStyles)

    def LoadRemoveSongEditor(self):
        if (AllowType(LoadType.Dol)):
            self.MainWidget.setCurrentIndex(TAB.RemoveSongEditor)
            self.LoadSongs(self.RS_Songs, [SongType.Regular])
            self.RS_RemoveCustomSongs.setEnabled(editor.file.type == LoadType.Rom)
            if (self.fromSongEditor != -1): self.List_DS_SongList()
            self.discord_presence(5)
        else:
            ShowError(self.tr("Unable to remove songs"), self.tr("Must load Wii Music Rom or Main.dol"))

    def ImportFiles(self):
        if (editor.file.type == LoadType.Rom):
            file = QFileDialog()
            file.setFileMode(QFileDialog.ExistingFile)
            file.setNameFilter(f"""{self.tr("All supported files")} (*.zip *.brsar *.carc *.dol *.ini)
            Zip File (*.zip)
            {self.tr("Sound Archive")} (*.brsar)
            {self.tr("Text File")} (*.carc)
            Main.dol (*.dol)
            Geckocodes (*.ini)""")
            file.setDirectory(lastFileDirectory)
            if (file.exec()):
                try:
                    path = file.selectedFiles()[0]
                    if (pathlib.Path(path).suffix == "zip"):
                        os.mkdir(SavePath() + "/tmp")
                        zipfile.ZipFile(path, 'r').extractall(SavePath() + "/tmp")
                        files = os.listdir(SavePath() + "/tmp")
                    else:
                        files = [path]
                    for newfile in files:
                        if (pathlib.Path(newfile).suffix == ".brsar"):
                            if (not os.path.isfile(GetBrsarPath() + ".backup")): copyfile(GetBrsarPath(),
                                                                                          GetBrsarPath() + ".backup")
                            copyfile(newfile, GetBrsarPath())
                        elif (pathlib.Path(newfile).suffix == ".carc"):
                            if (not os.path.isfile(GetMessagePath() + "/message.carc.backup")): copyfile(
                                GetMessagePath() + "/message.carc", GetMessagePath() + "/message.carc.backup")
                            copyfile(newfile, GetMessagePath() + "/message.carc")
                            if (os.path.isfile(GetMessagePath() + '/message.d/new_music_message.txt')): os.remove(
                                GetMessagePath() + '/message.d/new_music_message.txt')
                            GetSongNames()
                        elif (pathlib.Path(newfile).suffix == ".dol"):
                            if (not os.path.isfile(GetMainDolPath() + ".backup")): copyfile(GetMainDolPath(),
                                                                                            GetMainDolPath() + ".backup")
                            copyfile(newfile, GetMainDolPath())
                        elif (pathlib.Path(newfile).suffix == ".ini"):
                            copyfile(newfile, GetGeckoPath())
                    if (pathlib.Path(path).suffix == "zip"):
                        rmtree(SavePath() + "/tmp")
                    SuccessWindow(self.tr("Files Successfully Imported!"))
                except Exception as e:
                    ShowError(self.tr("Unable to import files"), str(e))
        else:
            ShowError(self.tr("Unable to import files"), self.tr("Must load Wii Music Rom"))

    def ExportFiles(self):
        if (editor.file.type == LoadType.Rom):
            file = QFileDialog()
            file.setFileMode(QFileDialog.AnyFile)
            file.setAcceptMode(QFileDialog.AcceptSave)
            file.setNameFilter("Zipfile (*.zip)")
            file.setDirectory(lastFileDirectory)
            if (file.exec()):
                try:
                    path = file.selectedFiles()[0]
                    if (pathlib.Path(path).suffix != ".zip"): path = path + ".zip"
                    zipObj = zipfile.ZipFile(path, 'w')
                    zipObj.write(GetBrsarPath(), 'rp_Music_sound.brsar')
                    zipObj.write(GetMessagePath() + "/message.carc", "message.carc")
                    zipObj.write(GetMainDolPath(), "main.dol")
                    zipObj.write(GetGeckoPath(), "Geckocodes.ini")
                    zipObj.close()
                    SuccessWindow(self.tr("Files Exported"))
                except Exception as e:
                    ShowError(self.tr("Files not Exported"), str(e))
        else:
            ShowError(self.tr("Unable to export files"), self.tr("Must load Wii Music Rom"))

    def ImportChanges(self):
        if (editor.file.type == LoadType.Rom):
            file = QFileDialog()
            file.setFileMode(QFileDialog.ExistingFile)
            file.setNameFilter(self.tr("Rom Change File") + " (*.ini)")
            file.setDirectory(lastFileDirectory)
            if (file.exec()):
                self.discord_presence(10)
                ImportChangesWindow(file.selectedFiles()[0])
        else:
            ShowError(self.tr("Unable to import changes"), self.tr("Must load Wii Music Rom"))

    # Menu Bar
    def MenuBar_CheckForUpdates(self):
        UpdateWindow(self)

    # Menu Bar Buttons
    def MenuBar_Load_Settings(self):
        using_discord = preferences.using_discord
        discord_state = discord_presence.state
        discord_presence.update(DiscordState.Settings)
        SettingsWindow()
        if preferences.using_discord != using_discord:
            if preferences.using_discord:
                discord_presence.connect()
            else:
                discord_presence.disconnect()
        discord_presence.update(discord_state)

    def MenuBar_Load_Rom(self):
        if select_rom_path("Wii Music Rom (*.wbfs *.iso)"):
            self.LoadRomInfo()
            self.GotoMainMenu()

    def MenuBar_Load_RomFolder(self):
        if select_rom_path(""):
            self.LoadRomInfo()
            self.GotoMainMenu()

    # Song Editor Buttons
    def SE_Patchable(self):
        allow = True
        songIndex = self.SE_SongToChange.currentRow()
        song = song_list[songIndex]
        if self.SE_Midi.isEnabled() and (self.SE_Midi.isChecked() or song.song_type == SongType.Menu):
            if (self.__SE_midiScore is None or
                    (self.__SE_midiSong is None
                        and self.SE_Midi_File_Replace_Song.isChecked()
                        and preferences.separate_tracks
                        and song.song_type != SongType.Maestro)):
                allow = False
        elif song.song_type != SongType.Menu:
            if (self.SE_ChangeSongText_Name_Input.text() == rom_folder.text.songs[songIndex]
                    and self.SE_ChangeSongText_Desc_Input.toPlainText() == rom_folder.text.descriptions[songIndex]
                    and self.SE_ChangeSongText_Genre_Input.text() == rom_folder.text.genres[songIndex]):
                allow = False
        self.SE_Patch.setEnabled(allow)

    def Button_SE_SongToChange(self, song: bool = False):
        try:
            midiPath = get_file_path(f"{tr('file', 'Midi-Type File')} (*.midi *.mid *.brseq *.rseq)",
                                     "midi")
            if midiPath != "":
                midi = Midi(Path(midiPath))
                if song:
                    self.SE_Midi_File_Song_Label.setText(os.path.basename(midiPath))
                    self.__SE_midiSong = midi
                else:
                    self.SE_Midi_File_Score_Label.setText(os.path.basename(midiPath))
                    self.SE_Midi_TimeSignature_3.setAutoExclusive(False)
                    self.SE_Midi_TimeSignature_4.setAutoExclusive(False)
                    self.SE_Midi_TimeSignature_3.setChecked(midi.time_signature == 3)
                    self.SE_Midi_TimeSignature_4.setChecked(midi.time_signature != 3)
                    self.SE_Midi_TimeSignature_3.setAutoExclusive(True)
                    self.SE_Midi_TimeSignature_4.setAutoExclusive(True)
                    if self.SE_Midi_Length_Measures.isChecked():
                        self.SE_Midi_Length_Measures.setAutoExclusive(False)
                        self.SE_Midi_Length_Beats.setAutoExclusive(False)
                        self.SE_Midi_Length_Measures.setChecked(False)
                        self.SE_Midi_Length_Beats.setChecked(True)
                        self.SE_Midi_Length_Measures.setAutoExclusive(True)
                        self.SE_Midi_Length_Beats.setAutoExclusive(True)
                    self.SE_Midi_Tempo_Input.setValue(midi.tempo)
                    self.SE_Midi_Length_Input.setValue(midi.length)
                self.__SE_midiScore = midi
                self.SE_Patchable()
        except Exception as e:
            ShowError("Error", str(e))

    def Button_SE_Midi_TimeSignature(self):
        if self.SE_Midi_Length_Measures.isChecked():
            length = int(self.SE_Midi_Length_Input.text())
            time_is_4 = self.SE_Midi_TimeSignature_4.isChecked()
            self.SE_Midi_Length_Input.setValue(round(length) / (3 + time_is_4) * (4 - time_is_4))

    def Button_SE_Midi_Length(self):
        length = int(self.SE_Midi_Length_Input.text())
        time = 3 + self.SE_Midi_TimeSignature_4.isChecked()
        if self.SE_Midi_Length_Measures.isChecked():
            self.SE_Midi_Length_Input.setValue(round(length) / time)
        else:
            self.SE_Midi_Length_Input.setValue(round(length) * time)

    def SE_SeparateSongPatching(self):
        if preferences.separate_tracks:
            self.SE_Midi_File_Song_Button.show()
            self.SE_Midi_File_Song_Title.show()
            self.SE_Midi_File_Song_Label.show()
            self.SE_Midi_File_Score_Title.show()
            self.SE_Midi_File_Replace_Song.show()
            enabled = (not self.SE_Midi.isEnabled() or song_list[
                self.SE_SongToChange.currentRow()].song_type != SongType.Maestro)
            self.SE_Midi_File_Song_Button.setEnabled(enabled)
            self.SE_Midi_File_Song_Title.setEnabled(enabled)
            self.SE_Midi_File_Song_Label.setEnabled(enabled)
            self.SE_Midi_File_Replace_Song.setEnabled(enabled)
        else:
            self.SE_Midi_File_Song_Button.hide()
            self.SE_Midi_File_Song_Title.hide()
            self.SE_Midi_File_Song_Label.hide()
            self.SE_Midi_File_Score_Title.hide()
            self.SE_Midi_File_Replace_Song.hide()

    def List_SE_SongToChange(self):
        try:
            songIndex = self.SE_SongToChange.currentRow()
            song = song_list[songIndex]
            self.SE_Midi.setCheckable(True)
            self.SE_Midi.setEnabled(True)
            if song.song_type != SongType.Menu:
                self.SE_ChangeSongText.setEnabled(True)
                self.SE_ChangeSongText_Name_Input.setText(rom_folder.text.songs[songIndex])
                self.SE_ChangeSongText_Desc_Input.setText(rom_folder.text.descriptions[songIndex])
                self.SE_ChangeSongText_Genre_Input.setText(rom_folder.text.genres[songIndex])
            else:
                self.SE_ChangeSongText.setEnabled(False)
                self.SE_ChangeSongText_Name_Input.setText("")
                self.SE_ChangeSongText_Desc_Input.setText("")
                self.SE_ChangeSongText_Genre_Input.setText("")
                self.SE_Midi.setCheckable(False)
                self.SE_Midi.setEnabled(True)
            self.SE_ResetButton.setEnabled(True)
            self.SE_SeparateSongPatching()
            self.SE_StyleBox.setEnabled(song.song_type == SongType.Regular)
            self.SE_OpenDefaultStyleEditor.setEnabled(song.song_type == SongType.Regular)
            self.SE_OpenStyleEditor.setEnabled(song.song_type == SongType.Regular)
            if song.song_type != SongType.Regular:
                self.SE_StyleText.setText("")
            else:
                self.SE_StyleText.setText(get_style_by_id(rom_folder.default_styles[songIndex]).name)
            self.SE_Patchable()
        except Exception as e:
            ShowError("Error", str(e))

    def Button_SE_Patch(self):
        songIndex = self.SE_SongToChange.currentRow()
        song = song_list[songIndex]
        if self.SE_Midi.isEnabled() and (self.SE_Midi.isChecked() or song.song_type == SongType.Menu):
            self.__SE_midiScore.tempo = self.SE_Midi_Tempo_Input.value()
            self.__SE_midiScore.length = self.SE_Midi_Length_Input.value()
            self.__SE_midiScore.time_signature = 3 + self.SE_Midi_TimeSignature_4.isChecked()
            if self.SE_Midi_Length_Measures.isChecked():
                self.__SE_midiScore.length *= 3 + self.SE_Midi_TimeSignature_4.isChecked()

            if (not self.SE_Midi_File_Replace_Song.isChecked() or
                    not preferences.separate_tracks or not self.SE_Midi_File_Replace_Song.isEnabled()):
                self.__SE_midiSong = self.__SE_midiScore

            # Patch Brsar
            replace_song(song, self.__SE_midiScore, self.__SE_midiSong)

        # Patch Text
        if song.song_type != SongType.Menu:
            name = self.SE_ChangeSongText_Name_Input.text()
            desc = self.SE_ChangeSongText_Desc_Input.toPlainText()
            genre = self.SE_ChangeSongText_Genre_Input.text()
            replace_song_text(song, name, desc, genre)
            if song.song_type == SongType.Maestro:
                name += f' ({tr("main", "Mii Maestro")})'
            if song.song_type == SongType.Maestro:
                name += f' ({tr("main", "Handbell Harmony")})'
            self.SE_SongToChange.item(self.SE_SongToChange.currentRow()).setText(name)

        self.SE_Patch.setEnabled(False)

    def Button_SE_OpenStyleEditor(self):
        self.fromSongEditor = get_style_by_id(rom_folder.default_styles[self.SE_SongToChange.currentRow()]).list_order
        self.MainWidget.setCurrentIndex(TAB.StyleEditor)
        self.LoadStyleEditor()

    def Button_SE_OpenDefaultStyleEditor(self):
        self.fromSongEditor = self.SE_SongToChange.currentRow()
        self.MainWidget.setCurrentIndex(TAB.DefaultStyleEditor)
        self.LoadDefaultStyleEditor()

    def Button_SE_ResetSong(self):
        index = self.SE_SongToChange.currentRow()
        (self.__SE_midiScore, self.__SE_midiSong, name, desc,
         genre, length, tempo, time) = get_original_song(song_list[index])
        self.SE_ChangeSongText_Name_Input.setText(name)
        self.SE_ChangeSongText_Desc_Input.setText(desc)
        self.SE_ChangeSongText_Genre_Input.setText(genre)
        self.SE_Midi_Length_Beats.setChecked(True)
        self.SE_Midi_Tempo_Input.setValue(tempo)
        self.SE_Midi_Length_Input.setValue(length)
        self.SE_Midi_TimeSignature_3.setChecked(time == 3)
        self.SE_Midi_File_Score_Label.setText(tr("main", "Default"))
        self.SE_Midi_File_Song_Label.setText(tr("main", "Default"))
        pass

    # Style Editor Buttons
    def StE_Patchable(self):
        styleIndex = get_style_list_index(self.StE_StyleList)
        self.StE_Patch.setEnabled((self.__StE_styleSelected != rom_folder.styles[styleIndex])
                                  or (self.StE_ChangeStyleName.isEnabled()
                                      and self.StE_ChangeStyleName.text() != rom_folder.text.styles[styleIndex]))

    def Button_StE_PartSelector(self):
        self.StE_InstrumentList.setCurrentRow(-1)
        style = style_list[get_style_list_index(self.StE_StyleList)]
        partIndex = self.StE_PartSelector.currentIndex()
        partIsPercussion = partIndex == 4 or partIndex == 5
        populate_instrument_list(self.StE_InstrumentList, partIsPercussion, style.style_type == StyleType.Menu)
        self.StE_SetIndex()

    def StE_SetIndex(self):
        partIndex = self.StE_PartSelector.currentIndex()
        partIsPercussion = partIndex == 4 or partIndex == 5
        if preferences.unsafe_mode:
            toHighlight = self.__StE_styleSelected[partIndex]
        elif partIsPercussion:
            toHighlight = self.__StE_styleSelected[partIndex] - 40
        else:
            toHighlight = self.__StE_styleSelected[partIndex]
            if toHighlight == len(instrument_list) - 1:
                toHighlight = 40
        self.StE_InstrumentList.setCurrentRow(toHighlight)

    def List_StE_InstrumentList(self):
        styleIndex = get_style_list_index(self.StE_StyleList)
        partIndex = self.StE_PartSelector.currentIndex()
        instrumentIndex = self.StE_InstrumentList.currentRow()
        partIsPercussion = partIndex == 4 or partIndex == 5
        if self.StE_InstrumentList.currentRow() != -1:
            if not preferences.unsafe_mode:
                if partIsPercussion:
                    instrumentIndex += 40
                else:
                    if instrumentIndex == 40:
                        instrumentIndex = len(instrument_list) - 1
            self.__StE_styleSelected[partIndex] = instrumentIndex
            self.StE_Patchable()
            if partIndex == 0:
                self.StE_Part_Melody_Instrument.setText(instrument_list[instrumentIndex].name)
            elif partIndex == 1:
                self.StE_Part_Harmony_Instrument.setText(instrument_list[instrumentIndex].name)
            elif partIndex == 2:
                self.StE_Part_Chords_Instrument.setText(instrument_list[instrumentIndex].name)
            elif partIndex == 3:
                self.StE_Part_Bass_Instrument.setText(instrument_list[instrumentIndex].name)
            elif partIndex == 4:
                self.StE_Part_Percussion1_Instrument.setText(instrument_list[instrumentIndex].name)
            elif partIndex == 5:
                self.StE_Part_Percussion2_Instrument.setText(instrument_list[instrumentIndex].name)
            self.StE_ResetStyle.setEnabled(self.__StE_styleSelected != style_list[styleIndex].style)

    def List_StE_StyleList(self):
        styleIndex = get_style_list_index(self.StE_StyleList)
        style = style_list[styleIndex]
        self.StE_Instruments.setEnabled(True)
        self.StE_Patch.setEnabled(False)
        if style.style_type == StyleType.Global or style.style_type == StyleType.QuickJam:
            self.StE_ChangeStyleName.setEnabled(True)
            self.StE_ChangeStyleName_Label.setEnabled(True)
            self.StE_ChangeStyleName.setText(rom_folder.text.styles[styleIndex])
        else:
            self.StE_ChangeStyleName.setEnabled(False)
            self.StE_ChangeStyleName_Label.setEnabled(False)
            self.StE_ChangeStyleName.setText("")
        self.__StE_styleSelected = rom_folder.styles[styleIndex].copy()
        self.StE_InstrumentList.setCurrentRow(-1)
        self.Button_StE_PartSelector()
        self.StE_ResetStyle.setEnabled(self.__StE_styleSelected != style.style)
        default_style = rom_folder.styles[styleIndex]
        self.StE_Part_Melody_Instrument.setText(instrument_list[default_style.melody].name)
        self.StE_Part_Harmony_Instrument.setText(instrument_list[default_style.harmony].name)
        self.StE_Part_Chords_Instrument.setText(instrument_list[default_style.chord].name)
        self.StE_Part_Bass_Instrument.setText(instrument_list[default_style.bass].name)
        self.StE_Part_Percussion1_Instrument.setText(instrument_list[default_style.perc1].name)
        self.StE_Part_Percussion2_Instrument.setText(instrument_list[default_style.perc2].name)

    def Button_StE_ResetStyle(self):
        self.__StE_styleSelected = style_list[get_style_list_index(self.StE_StyleList)].style.copy()
        self.StE_ResetStyle.setEnabled(False)
        self.StE_Patchable()
        self.StE_Part_Melody_Instrument.setText(instrument_list[self.__StE_styleSelected.melody].name)
        self.StE_Part_Harmony_Instrument.setText(instrument_list[self.__StE_styleSelected.harmony].name)
        self.StE_Part_Chords_Instrument.setText(instrument_list[self.__StE_styleSelected.chord].name)
        self.StE_Part_Bass_Instrument.setText(instrument_list[self.__StE_styleSelected.bass].name)
        self.StE_Part_Percussion1_Instrument.setText(instrument_list[self.__StE_styleSelected.perc1].name)
        self.StE_Part_Percussion2_Instrument.setText(instrument_list[self.__StE_styleSelected.perc2].name)
        self.StE_SetIndex()

    def Button_StE_Patch(self):
        self.StE_Patch.setEnabled(False)
        styleIndex = get_style_list_index(self.StE_StyleList)
        if self.__StE_styleSelected != rom_folder.styles[styleIndex]:
            replace_style(style_list[styleIndex], self.__StE_styleSelected)

        if (self.StE_ChangeStyleName.isEnabled()
                and self.StE_ChangeStyleName.text() != rom_folder.text.styles[styleIndex]):
            replace_style_text(style_list[styleIndex], self.StE_ChangeStyleName.text())

        if style_list[styleIndex].style == self.__StE_styleSelected:
            self.StE_StyleList.item(self.StE_StyleList.currentRow()).setText(
                rom_folder.text.styles[style_list[styleIndex].style_id])
        else:
            self.StE_StyleList.item(self.StE_StyleList.currentRow()).setText(
                f"{rom_folder.text.styles[style_list[styleIndex].style_id]} ~[{tr('main', 'Replaced')}]~")

    # Text Editor
    def Button_TE_Patch(self):
        rom_folder.text.textlines = [text.encode('utf-8') for text in self.TE_Text.toPlainText().split("\n")]
        rom_folder.text.encode()
        self.MainWidget.setCurrentIndex(TAB.MainMenu)
        self.TE_Patch.setEnabled(False)

    def Button_TE_ExternalEditor(self):
        self.externalEditorOpen = True
        self.TE_Patch.setEnabled(False)
        self.TE_Text.setEnabled(False)
        self.TE_Back_Button.setEnabled(False)
        self.TE_OpenExternal.setEnabled(False)
        self.textEditor = ExternalEditor()
        self.textEditor.done.connect(self.TE_FinishEditor)
        self.textEditor.start()

    def TE_Text_Editor(self):
        self.TE_Text.setEnabled(True)

    def TE_FinishEditor(self):
        try:
            rom_folder.text.read()
        except Exception as e:
            print("error", str(e))
        self.TE_Text.setPlainText(rom_folder.text.to_text())
        self.TE_Patch.setEnabled(True)
        self.TE_Text.setEnabled(True)
        self.TE_Back_Button.setEnabled(True)
        self.TE_OpenExternal.setEnabled(True)
        self.textEditor.deleteLater()

    # Default Style Editor
    def Button_DS_Patch(self):
        song = song_list[self.DS_Songs.currentRow()]
        style = style_list[get_style_list_index(self.DS_Styles)]
        replace_default_style(song, style)
        self.DS_Patch.setEnabled(False)
        if self.fromSongEditor != -1:
            self.SE_StyleText.setText(style.name)

    def List_DS_SongList(self):
        self.DS_StyleBox.setEnabled(True)
        set_style_list_index(self.DS_Styles,
                             get_style_by_id(rom_folder.default_styles[self.DS_Songs.currentRow()]).list_order)

    def List_DS_StyleList(self):
        song = song_list[self.DS_Songs.currentRow()]
        style = style_list[get_style_list_index(self.DS_Styles)]
        self.DS_Patch.setEnabled(style.style_id != rom_folder.default_styles[song.list_order])
        self.DS_Reset.setEnabled(style.style_id != song.default_style)

    def Button_DS_Reset(self):
        set_style_list_index(self.DS_Styles, get_style_by_id(
            song_list[self.DS_Songs.currentRow()].default_style).list_order)
        self.DS_Reset.setEnabled(False)

    # Remove Songs
    def Button_RS_RemoveCustomSongs(self):
        file = open(GetGeckoPath())
        textlines = file.readlines()
        file.close()
        for i in range(self.RS_Songs.count()):
            self.RS_Songs.item(i).setSelected(True)

        for text in textlines:
            if ("Song Patch [WiiMusicEditor]"):
                name = text[1:len(text) - 29:1]
                for i in range(self.RS_Songs.count()):
                    if (Songs[i].Name == name):
                        self.RS_Songs.item(i).setSelected(False)

    def Button_RS_DeselectAll(self):
        for i in range(self.RS_Songs.count()):
            self.RS_Songs.item(i).setSelected(False)

    def Button_RS_Purge(self):
        try:
            removesongs = []
            file = open(GetMainDolPath(), "r+b")
            for i in range(self.RS_Songs.count()):
                if (self.RS_Songs.item(i).isSelected()):
                    file.seek(0x59C574 + 0xBC * Songs[i].MemOrder)
                    file.write(bytes.fromhex('ffffffffffff'))
                    removesongs.append(i)
            file.close()
            SaveRecording(RecordType.RemoveSong, "null", ["songs", removesongs])
            SuccessWindow(self.tr("Songs Successfully Destroyed!!!"))
        except Exception as e:
            ShowError(self.tr("Could not remove songs"), str(e))
