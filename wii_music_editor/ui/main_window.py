import os
from pathlib import Path
from shutil import copyfile, copytree, rmtree
import subprocess
import zipfile
import webbrowser
import wave

from PySide6.QtWidgets import QMainWindow

from wii_music_editor.data.songs import SongType, songList
from wii_music_editor.data.styles import styleList, get_style_by_id
from wii_music_editor.editor.midi import Midi

from wii_music_editor.editor.rom_folder import RomFolder
from wii_music_editor.services.discord import DiscordUpdate, DiscordState
from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.ui.widgets.dolphin import LoadDolphin
from wii_music_editor.ui.widgets.load_files import get_file_path
from wii_music_editor.ui.widgets.populate_list_widget import populate_song_list, populate_style_list, \
    populate_instrument_list
from wii_music_editor.ui.windows.main_window_ui import Ui_MainWindow
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.utils.preferences import preferences
from wii_music_editor.utils.save import load_setting
from wii_music_editor.utils.translate import tr


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
    rom_folder: RomFolder
    externalEditorOpen: bool
    fromSongEditor: int

    __SE_midiScore: Midi or None
    __SE_midiSong: Midi or None

    __StE_styleSelected: list[int]

    def __init__(self, rom_folder: RomFolder):
        super().__init__(None)
        self.setupUi(self)
        self.externalEditorOpen = False
        self.fromSongEditor = -1
        self.rom_folder = rom_folder

        # Menu Bar Buttons
        self.menuBar().setNativeMenuBar(False)
        self.MB_LoadFile.triggered.connect(self.MenuBar_Load_Rom)
        self.MB_LoadFolder.triggered.connect(self.MenuBar_Load_RomFolder)
        self.MB_Settings.triggered.connect(self.MenuBar_Load_Settings)
        self.MB_Updates.triggered.connect(self.MenuBar_CheckForUpdates)
        self.MB_Dolphin.triggered.connect(lambda: LoadDolphin(False))
        self.MB_DolphinMenu.triggered.connect(lambda: LoadDolphin(True))
        self.MB_DownloadSongs.triggered.connect(self.DownloadSongs)
        self.MB_SaveFile.triggered.connect(self.MenuBar_Save_File)
        self.MB_Help.triggered.connect(
            lambda: webbrowser.open("https://github.com/BenjaminHalko/WiiMusicEditorPlus/wiki"))
        self.MB_Donate.triggered.connect(lambda: webbrowser.open("https://ko-fi.com/benjaminhalko"))
        self.MB_Discord.triggered.connect(lambda: webbrowser.open("https://discord.gg/NC3wYAeCDs"))

        # Main Menu Buttons
        self.MP_SongEditor_Button.clicked.connect(self.LoadSongEditor)
        self.MP_StyleEditor_Button.clicked.connect(self.LoadStyleEditor)
        self.MP_EditText_Button.clicked.connect(self.LoadTextEditor)
        self.MP_DefaultStyle_Button.clicked.connect(self.LoadDefaultStyleEditor)
        self.MP_ReplaceSound_Button.clicked.connect(self.LoadSoundEditor)
        self.MP_RemoveSong_Button.clicked.connect(self.LoadRemoveSongEditor)
        self.MP_GeckocodeConvert_Button.clicked.connect(self.ConvertGeckocode)
        self.MP_MainDolPatch_Button.clicked.connect(self.PatchMainDolWithGeckoCode)
        self.MP_Riivolution_Button.clicked.connect(self.CreateRiivolutionPatch)

        self.MP_RevertChanges_Button.clicked.connect(self.RevertChanges)
        self.MP_PackRom_Button.clicked.connect(self.PackRom)
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

        # Sound Editor
        self.SOE_Back_Button.clicked.connect(self.GotoMainMenu)
        self.SOE_Sounds.itemSelectionChanged.connect(self.List_SOE_Sounds)
        self.SOE_SelectAll.clicked.connect(self.Button_SOE_SelectAll)
        self.SOE_SoundType.itemPressed.connect(self.SOE_Patchable)
        self.SOE_File_Browse.clicked.connect(self.Button_SOE_Browse)
        self.SOE_Patch.clicked.connect(self.Button_SOE_Patch)
        self.SOE_PlayAudio.clicked.connect(self.Button_SOE_PlayAudio)
        self.SOE_LoopSeconds.toggled.connect(self.Button_SOE_SwitchType)

    def GotoMainMenu(self):
        if self.fromSongEditor != -1:
            self.MainWidget.setCurrentIndex(TAB.SongEditor)
            self.fromSongEditor = -1
        else:
            self.MainWidget.setCurrentIndex(TAB.MainMenu)
            DiscordUpdate(DiscordState.ModdingWiiMusic)

    def LoadSongEditor(self):
        self.MainWidget.setCurrentIndex(TAB.SongEditor)
        populate_song_list(self.rom_folder, self.SE_SongToChange)
        self.SE_Midi.setEnabled(False)
        self.SE_Midi.setCheckable(False)
        self.SE_ChangeSongText.setEnabled(False)
        self.SE_Patch.setEnabled(False)
        self.SE_StyleLabel.setEnabled(False)
        self.SE_StyleText.setEnabled(False)
        self.SE_OpenDefaultStyleEditor.setEnabled(False)
        self.SE_OpenStyleEditor.setEnabled(False)
        self.SE_Midi_File_Score_Label.setText(tr("main", "Load a Midi-Type file"))
        self.SE_Midi_File_Song_Label.setText(tr("main", "Load a Midi-Type file"))
        self.__SE_midiScore = None
        self.__SE_midiSong = None
        DiscordUpdate(DiscordState.EditingSongs)

    def LoadStyleEditor(self):
        self.MainWidget.setCurrentIndex(TAB.StyleEditor)
        populate_style_list(self.rom_folder, self.StE_StyleList, self.fromSongEditor)
        populate_instrument_list(self.StE_InstrumentList)
        self.StE_Instruments.setEnabled(False)
        self.StE_ChangeStyleName.setEnabled(False)
        self.StE_ChangeStyleName_Label.setEnabled(False)
        self.StE_ResetStyle.setEnabled(False)
        self.StE_Patch.setEnabled(False)
        self.__StE_styleSelected = []
        DiscordUpdate(DiscordState.EditingStyles)

    def LoadTextEditor(self):
        if (AllowType(LoadType.Carc)):
            DecodeTxt()
            file = open(GetMessagePath() + "/message.d/new_music_message.txt", "r+b")
            textlines = file.readlines()
            originalTextlines = textlines.copy()
            textlines = FixMessageFile(textlines)
            if (textlines != originalTextlines): file.writelines(textlines)
            file.close()
            file = open(GetMessagePath() + "/message.d/new_music_message.txt", "rb")
            self.TE_Text.setPlainText(file.read().decode("utf-8"))
            file.close()
            self.MainWidget.setCurrentIndex(TAB.TextEditor)
            self.DiscordUpdate(3)
        else:
            ShowError(self.tr("Unable to load text editor"), self.tr("Must load Wii Music Rom or Message File"))

    def LoadDefaultStyleEditor(self):
        if (AllowType(LoadType.Gct)):
            self.MainWidget.setCurrentIndex(TAB.DefaultStyleEditor)
            GetStyles()
            self.LoadSongs(self.DS_Songs, [SongType.Regular], self.fromSongEditor != -1)
            self.LoadStyles(self.DS_Styles)
            self.DS_StyleBox.setEnabled(False)
            self.DS_Patch.setEnabled(False)
            if (self.fromSongEditor != -1): self.List_DS_SongList()
            self.DiscordUpdate(4)
        else:
            error = ShowError(self.tr("Unable to load default style editor"),
                              self.tr("Must load Wii Music Rom or Geckocode"), geckocode=True)
            if (error.clicked):
                if (self.CreateGeckoCode()): self.LoadDefaultStyleEditor()

    def LoadRemoveSongEditor(self):
        if (AllowType(LoadType.Dol)):
            self.MainWidget.setCurrentIndex(TAB.RemoveSongEditor)
            self.LoadSongs(self.RS_Songs, [SongType.Regular])
            self.RS_RemoveCustomSongs.setEnabled(editor.file.type == LoadType.Rom)
            if (self.fromSongEditor != -1): self.List_DS_SongList()
            self.DiscordUpdate(5)
        else:
            ShowError(self.tr("Unable to remove songs"), self.tr("Must load Wii Music Rom or Main.dol"))

    def LoadSoundEditor(self):
        if (AllowType(LoadType.Brsar)):
            self.MainWidget.setCurrentIndex(TAB.SoundEditor)
            self.SOE_Sounds.clear()
            for i in range(40):
                item = QtWidgets.QListWidgetItem()
                item.setText(Instruments[i].Name)
                self.SOE_Sounds.addItem(item)
            for sound in extraSounds:
                item = QtWidgets.QListWidgetItem()
                item.setText(sound.Name)
                self.SOE_Sounds.addItem(item)
            item = QtWidgets.QListWidgetItem()
            item.setText("Sebastion Tute")
            self.SOE_Sounds.addItem(item)
            self.extraFile = ""
            self.SOE_Patch.setEnabled(False)
            self.SOE_SoundTypeBox.setEnabled(False)
            self.SOE_File_Label.setText(self.tr("Load a Wav-Type File"))
            self.SOE_Loop.setEnabled(False)
            self.SOE_Loop.setCheckable(False)
            self.DiscordUpdate(6)
        else:
            ShowError(self.tr("Unable to load sound editor"), self.tr("Must load Wii Music Rom or Brsar"))

    def ConvertGeckocode(self):
        if (AllowType(LoadType.Gct)):
            file = QFileDialog()
            file.setFileMode(QFileDialog.AnyFile)
            file.setAcceptMode(QFileDialog.AcceptSave)
            file.setNameFilter("Geckocodes (*.gct)")
            file.setDirectory(lastFileDirectory)
            if (file.exec()):
                path = file.selectedFiles()[0]
                if (pathlib.Path(path).suffix != ".gct"): file = file + ".gct"
                CreateGct(path)
                SuccessWindow(self.tr("Creation Complete!"))
        else:
            ShowError(self.tr("Unable to create .gct file"), self.tr("Must load Wii Music Rom or Geckocode"))

    def PatchMainDolWithGeckoCode(self):
        if (editor.file.type == LoadType.Rom):
            file = QFileDialog()
            file.setFileMode(QFileDialog.ExistingFile)
            file.setNameFilter("Geckocodes (*.ini *.gct)")
            file.setDirectory(os.path.dirname(GetGeckoPath()))
            if (file.exec()):
                PatchMainDol(geckoPath=file.selectedFiles()[0])
                SaveRecording(RecordType.MainDol, "null", ["geckopath", str(file.selectedFiles()[0])])
                SuccessWindow(self.tr("Main.dol Patched!"))
        elif (editor.file.type == LoadType.Gct or editor.file.type == LoadType.Dol):
            file = QFileDialog()
            file.setFileMode(QFileDialog.ExistingFile)
            if (editor.file.type == LoadType.Midi):
                file.setNameFilter("Geckocodes (*.ini *.gct)")
            else:
                file.setNameFilter("Main.dol (*.dol)")
            file.setDirectory(lastExtraFileDirectory)
            if (file.exec()):
                if (editor.file.type == LoadType.Midi):
                    PatchMainDol(geckoPath=file.selectedFiles()[0])
                else:
                    PatchMainDol(dolPath=file.selectedFiles()[0])
                SuccessWindow(self.tr("Main.dol Patched!"))
        else:
            ShowError(self.tr("Unable to patch Main.dol"), self.tr("Must load Wii Music Rom, Main.dol, or Geckocode"))

    def CreateRiivolutionPatch(self):
        if (editor.file.type == LoadType.Rom):
            self.DiscordUpdate(7)
            RiivolutionWindow()
            self.DiscordUpdate(0)
        else:
            ShowError(self.tr("Unable to create Riivolution patch"), self.tr("Must load Wii Music Rom"))

    def RevertChanges(self):
        if (editor.file.type == LoadType.Rom):
            self.DiscordUpdate(8)
            RevertChangesWindow()
            self.DiscordUpdate(0)
        else:
            ShowError(self.tr("Unable to revert changes"), self.tr("Must load Wii Music Rom"))

    def PackRom(self):
        if (editor.file.type == LoadType.Rom):
            self.DiscordUpdate(9)
            PackRomWindow()
            self.DiscordUpdate(0)
        else:
            ShowError(self.tr("Unable to pack rom"), self.tr("Must load Wii Music Rom"))

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
                self.DiscordUpdate(10)
                ImportChangesWindow(file.selectedFiles()[0])
        else:
            ShowError(self.tr("Unable to import changes"), self.tr("Must load Wii Music Rom"))

    # Menu Bar

    def MenuBar_CheckForUpdates(self):
        UpdateWindow(self, False)

    #############Menu Bar Buttons
    def MenuBar_Load_Settings(self):
        self.DiscordUpdate(-1)
        SettingsWindow(self, app, translator)
        if ((self.discord != False) != load_setting("Settings", "Discord", True)):
            if (self.discord == False):
                self.DiscordPresenceConnect()
            else:
                try:
                    self.discord.close()
                    self.discord = False
                except Exception:
                    self.discord = False
        self.DiscordUpdate(self.MainWidget.currentIndex())

    def MenuBar_Load_Rom(self):
        if (self.LoadMainFile(f"""{self.tr("All supported files")} (*.wbfs *.iso *.brsar *.carc *.dol *.ini)
        Wii Music Rom (*.wbfs *.iso)
        {self.tr("Sound Archive")} (*.brsar)
        {self.tr("Text File")} (*.carc)
        Main.dol (*.dol)
        Geckocode (*.ini)""")):
            PrepareFile()
            SaveSetting("Paths", "CurrentLoadedFile", editor.file.path)
            self.MP_LoadedFile_Path.setText(editor.file.path)
            self.MP_LoadedFile_Label.setText(self.tr('Currently Loaded File:'))
            self.GotoMainMenu()

    def MenuBar_Load_RomFolder(self):
        if (self.LoadMainFile("")):
            PrepareFile()
            SaveSetting("Paths", "CurrentLoadedFile", editor.file.path)
            self.MP_LoadedFile_Path.setText(editor.file.path)
            self.MP_LoadedFile_Label.setText(self.tr('Currently Loaded Folder:'))

    def MenuBar_Save_File(self):
        try:
            if (ConfirmDialog(self.tr("Are you sure you want to overwrite your save file?"))):
                rmtree(GetDolphinSave() + "/Wii/title/00010000/" + BasedOnRegion(savePathIds) + "/data")
                copytree(HelperPath() + "/WiiMusicSave",
                         GetDolphinSave() + "/Wii/title/00010000/" + BasedOnRegion(savePathIds) + "/data")
                SuccessWindow(self.tr("Save file copied!"))
        except Exception as e:
            ShowError(self.tr("Unable to copy save file"), str(e))

    def DownloadSongs(self):
        self.importthread = DownloadSongThread()
        self.importthread.done.connect(
            lambda: SuccessWindow(self.tr("Songs Saved to: Program Path") + "/Pre-Made Songs for Wii Music"))
        self.importthread.start()

    # Song Editor Buttons
    def SE_Patchable(self):
        allow = True
        songIndex = self.SE_SongToChange.currentRow()
        song = songList[songIndex]
        if self.SE_Midi.isEnabled() and (self.SE_Midi.isChecked() or song.SongType == SongType.Menu):
            if (self.__SE_midiScore is None or
                    (self.__SE_midiSong is None
                        and self.SE_Midi_File_Replace_Song.isChecked()
                        and preferences.separate_tracks
                        and song.SongType != SongType.Maestro)):
                allow = False
        elif song.SongType != SongType.Menu:
            if (self.SE_ChangeSongText_Name_Input.text() == self.rom_folder.text.songs[songIndex]
                    and self.SE_ChangeSongText_Desc_Input.toPlainText() == self.rom_folder.text.descriptions[songIndex]
                    and self.SE_ChangeSongText_Genre_Input.text() == self.rom_folder.text.genres[songIndex]):
                allow = False
        self.SE_Patch.setEnabled(allow)

    def Button_SE_SongToChange(self, song: bool = False):
        try:
            midiPath = get_file_path(f"{tr('file', 'Midi-Type File')} (*.midi *.mid *.brseq *.rseq)")
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
            enabled = (not self.SE_Midi.isEnabled() or songList[
                self.SE_SongToChange.currentRow()].SongType != SongType.Maestro)
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
            song = songList[songIndex]
            self.SE_Midi.setCheckable(True)
            self.SE_Midi.setEnabled(True)
            if song.SongType != SongType.Menu:
                self.SE_ChangeSongText.setEnabled(True)
                self.SE_ChangeSongText_Name_Input.setText(self.rom_folder.text.songs[songIndex])
                self.SE_ChangeSongText_Desc_Input.setText(self.rom_folder.text.descriptions[songIndex])
                self.SE_ChangeSongText_Genre_Input.setText(self.rom_folder.text.genres[songIndex])
            else:
                self.SE_ChangeSongText.setEnabled(False)
                self.SE_ChangeSongText_Name_Input.setText("")
                self.SE_ChangeSongText_Desc_Input.setText("")
                self.SE_ChangeSongText_Genre_Input.setText("")
                self.SE_Midi.setCheckable(False)
                self.SE_Midi.setEnabled(True)
            self.SE_SeparateSongPatching()
            self.SE_StyleLabel.setEnabled(song.SongType == SongType.Regular)
            self.SE_StyleText.setEnabled(song.SongType == SongType.Regular)
            self.SE_OpenDefaultStyleEditor.setEnabled(song.SongType == SongType.Regular)
            self.SE_OpenStyleEditor.setEnabled(song == SongType.Regular)
            if song.SongType != SongType.Regular:
                self.SE_StyleText.setText("")
            else:
                self.SE_StyleText.setText(get_style_by_id(song.DefaultStyle).Name)
            self.SE_Patchable()
        except Exception as e:
            ShowError("Error", str(e))

    def Button_SE_Patch(self):
        try:
            songIndex = self.SE_SongToChange.currentRow()
            song = songList[songIndex]
            if self.SE_Midi.isEnabled() and (self.SE_Midi.isChecked() or song.SongType == SongType.Menu):
                self.__SE_midiScore.tempo = self.SE_Midi_Tempo_Input.value()
                self.__SE_midiScore.length = self.SE_Midi_Length_Input.value()
                self.__SE_midiScore.time_signature = 3 + self.SE_Midi_TimeSignature_4.isChecked()
                if self.SE_Midi_Length_Measures.isChecked():
                    self.__SE_midiScore.length *= 3 + self.SE_Midi_TimeSignature_4.isChecked()

                if (not self.SE_Midi_File_Replace_Song.isChecked() or
                        not preferences.separate_tracks or not self.SE_Midi_File_Replace_Song.isEnabled()):
                    self.__SE_midiSong = self.__SE_midiScore


                # Patch Brsar
                PatchBrsar(self.SE_SongToChange.currentRow(), tmpInfo, tmpLength, self.SE_Midi_Tempo_Input.value(),
                           length, 3 + self.SE_Midi_TimeSignature_4.isChecked())
                SaveRecording(RecordType.Song, self.SE_SongToChange.currentRow(), [
                    ["midisong", tmpPath[0]],
                    ["midiscore", tmpPath[1]],
                    ["tempo", self.SE_Midi_Tempo_Input.value()],
                    ["length", length],
                    ["timesignature", 3 + self.SE_Midi_TimeSignature_4.isChecked()]])

            if (AllowType(LoadType.Carc) and (
                    Songs[self.SE_SongToChange.currentRow()].SongType != SongType.Menu)) and not (
            (self.SE_ChangeSongText_Name_Input.text() == editor.textFromTxt[0][self.SE_SongToChange.currentRow()] and
             self.SE_ChangeSongText_Desc_Input.toPlainText() == editor.textFromTxt[1][
                 self.SE_SongToChange.currentRow()] and
             self.SE_ChangeSongText_Genre_Input.text() == editor.textFromTxt[2][self.SE_SongToChange.currentRow()])):
                ChangeName(self.SE_SongToChange.currentRow(),
                           [self.SE_ChangeSongText_Name_Input.text(), self.SE_ChangeSongText_Desc_Input.toPlainText(),
                            self.SE_ChangeSongText_Genre_Input.text()])
                text = Songs[self.SE_SongToChange.currentRow()].Name
                if (len(editor.textFromTxt[0]) > self.SE_SongToChange.currentRow()) and AllowType(LoadType.Carc) and (
                        Songs[self.SE_SongToChange.currentRow()].SongType != SongType.Regular or
                        editor.textFromTxt[0][self.SE_SongToChange.currentRow()] != Songs[
                            self.SE_SongToChange.currentRow()].Name) and (
                        Songs[self.SE_SongToChange.currentRow()].SongType != SongType.Maestro or
                        editor.textFromTxt[0][self.SE_SongToChange.currentRow()] != Songs[
                                                                                        self.SE_SongToChange.currentRow()].Name[
                                                                                    0:len(Songs[
                                                                                              self.SE_SongToChange.currentRow()].Name) - 14:1]) and (
                        Songs[self.SE_SongToChange.currentRow()].SongType != SongType.Handbell or
                        editor.textFromTxt[0][self.SE_SongToChange.currentRow()] != Songs[
                                                                                        self.SE_SongToChange.currentRow()].Name[
                                                                                    0:len(Songs[
                                                                                              self.SE_SongToChange.currentRow()].Name) - 19:1]) and (
                        Songs[self.SE_SongToChange.currentRow()].SongType != SongType.Menu):
                    text = editor.textFromTxt[0][self.SE_SongToChange.currentRow()]
                    if (Songs[
                        self.SE_SongToChange.currentRow()].SongType == SongType.Maestro): text = text + " (" + self.tr(
                        "Mii Maestro") + ")"
                    if (Songs[
                        self.SE_SongToChange.currentRow()].SongType == SongType.Handbell): text = text + " (" + self.tr(
                        "Handbell Harmony") + ")"
                self.SE_SongToChange.item(self.SE_SongToChange.currentRow()).setText(text)
                editor.textFromTxt[0][self.SE_SongToChange.currentRow()] = self.SE_ChangeSongText_Name_Input.text()
                editor.textFromTxt[1][
                    self.SE_SongToChange.currentRow()] = self.SE_ChangeSongText_Desc_Input.toPlainText()
                editor.textFromTxt[2][self.SE_SongToChange.currentRow()] = self.SE_ChangeSongText_Genre_Input.text()
                SaveRecording(RecordType.TextSong, self.SE_SongToChange.currentRow(), [
                    ["name", self.SE_ChangeSongText_Name_Input.text()],
                    ["desc", self.SE_ChangeSongText_Desc_Input.toPlainText()],
                    ["genre", self.SE_ChangeSongText_Genre_Input.text()]])
            self.SE_Patch.setEnabled(False)
        except Exception as e:
            ShowError(tr("error", "Could not patch songs"), str(e))

    def Button_SE_OpenStyleEditor(self):
        self.fromSongEditor = songList[self.SE_SongToChange.currentRow()].DefaultStyle
        self.MainWidget.setCurrentIndex(TAB.StyleEditor)
        self.LoadStyleEditor()

    def Button_SE_OpenDefaultStyleEditor(self):
        self.fromSongEditor = self.SE_SongToChange.currentRow()
        self.MainWidget.setCurrentIndex(TAB.DefaultStyleEditor)
        self.LoadDefaultStyleEditor()

    # Style Editor Buttons
    def StE_Patchable(self):
        self.StE_Patch.setEnabled((self.styleSelected != editor.loadedStyles[self.StE_StyleList.currentRow()]) or (
                    self.StE_ChangeStyleName.isEnabled() and self.StE_ChangeStyleName.text() != editor.textFromTxt[3][
                self.StE_StyleList.currentRow()]))

    def Button_StE_PartSelector(self):
        self.StE_InstrumentList.setCurrentRow(-1)
        self.LoadInstruments(self.StE_InstrumentList,
                             (self.StE_PartSelector.currentIndex() == 4 or self.StE_PartSelector.currentIndex() == 5),
                             Styles[self.StE_StyleList.currentRow()].StyleType == StyleTypeValue.Menu)
        if (editor.unsafeMode):
            toHighlight = self.styleSelected[self.StE_PartSelector.currentIndex()]
        elif (self.StE_PartSelector.currentIndex() == 4 or self.StE_PartSelector.currentIndex() == 5):
            toHighlight = self.styleSelected[self.StE_PartSelector.currentIndex()] - 40
        else:
            toHighlight = self.styleSelected[self.StE_PartSelector.currentIndex()]
            if (toHighlight == len(Instruments) - 1): toHighlight = 40
        self.StE_InstrumentList.setCurrentRow(toHighlight)

    def List_StE_InstrumentList(self):
        if (self.StE_InstrumentList.currentRow() != -1):
            if (editor.unsafeMode):
                songSelected = self.StE_InstrumentList.currentRow()
            elif (self.StE_PartSelector.currentIndex() == 4 or self.StE_PartSelector.currentIndex() == 5):
                songSelected = self.StE_InstrumentList.currentRow() + 40
            else:
                songSelected = self.StE_InstrumentList.currentRow()
                if (songSelected == 40): songSelected = len(Instruments) - 1
            self.styleSelected[self.StE_PartSelector.currentIndex()] = songSelected
            self.StE_Patchable()
            if (self.StE_PartSelector.currentIndex() == 0):
                self.StE_Part_Melody_Instrument.setText(Instruments[songSelected].Name)
            elif (self.StE_PartSelector.currentIndex() == 1):
                self.StE_Part_Harmony_Instrument.setText(Instruments[songSelected].Name)
            elif (self.StE_PartSelector.currentIndex() == 2):
                self.StE_Part_Chords_Instrument.setText(Instruments[songSelected].Name)
            elif (self.StE_PartSelector.currentIndex() == 3):
                self.StE_Part_Bass_Instrument.setText(Instruments[songSelected].Name)
            elif (self.StE_PartSelector.currentIndex() == 4):
                self.StE_Part_Percussion1_Instrument.setText(Instruments[songSelected].Name)
            elif (self.StE_PartSelector.currentIndex() == 5):
                self.StE_Part_Percussion2_Instrument.setText(Instruments[songSelected].Name)
            self.StE_ResetStyle.setEnabled(self.styleSelected != Styles[self.StE_StyleList.currentRow()].DefaultStyle)

    def List_StE_StyleList(self):
        self.StE_Instruments.setEnabled(True)
        self.StE_Patch.setEnabled(False)
        if (AllowType(LoadType.Carc) and (Styles[self.StE_StyleList.currentRow()].StyleType == StyleTypeValue.Global)):
            self.StE_ChangeStyleName.setEnabled(True)
            self.StE_ChangeStyleName_Label.setEnabled(True)
            self.StE_ChangeStyleName.setText(editor.textFromTxt[3][self.StE_StyleList.currentRow()])
        else:
            self.StE_ChangeStyleName.setEnabled(False)
            self.StE_ChangeStyleName_Label.setEnabled(False)
            self.StE_ChangeStyleName.setText("")
        self.styleSelected = editor.loadedStyles[self.StE_StyleList.currentRow()].copy()
        self.StE_InstrumentList.setCurrentRow(-1)
        self.LoadInstruments(self.StE_InstrumentList,
                             (self.StE_PartSelector.currentIndex() == 4 or self.StE_PartSelector.currentIndex() == 5),
                             Styles[self.StE_StyleList.currentRow()].StyleType == StyleTypeValue.Menu)
        if (editor.unsafeMode):
            toHighlight = editor.loadedStyles[self.StE_StyleList.currentRow()][self.StE_PartSelector.currentIndex()]
        elif (self.StE_PartSelector.currentIndex() == 4 or self.StE_PartSelector.currentIndex() == 5):
            toHighlight = editor.loadedStyles[self.StE_StyleList.currentRow()][
                              self.StE_PartSelector.currentIndex()] - 40
        else:
            toHighlight = editor.loadedStyles[self.StE_StyleList.currentRow()][self.StE_PartSelector.currentIndex()]
            if (toHighlight == len(Instruments) - 1): toHighlight = 40
        self.StE_ResetStyle.setEnabled(self.styleSelected != Styles[self.StE_StyleList.currentRow()].DefaultStyle)
        self.StE_InstrumentList.setCurrentRow(toHighlight)
        self.StE_Part_Melody_Instrument.setText(
            Instruments[editor.loadedStyles[self.StE_StyleList.currentRow()][0]].Name)
        self.StE_Part_Harmony_Instrument.setText(
            Instruments[editor.loadedStyles[self.StE_StyleList.currentRow()][1]].Name)
        self.StE_Part_Chords_Instrument.setText(
            Instruments[editor.loadedStyles[self.StE_StyleList.currentRow()][2]].Name)
        self.StE_Part_Bass_Instrument.setText(Instruments[editor.loadedStyles[self.StE_StyleList.currentRow()][3]].Name)
        self.StE_Part_Percussion1_Instrument.setText(
            Instruments[editor.loadedStyles[self.StE_StyleList.currentRow()][4]].Name)
        self.StE_Part_Percussion2_Instrument.setText(
            Instruments[editor.loadedStyles[self.StE_StyleList.currentRow()][5]].Name)

    def Button_StE_ResetStyle(self):
        self.styleSelected = Styles[self.StE_StyleList.currentRow()].DefaultStyle.copy()
        self.StE_ResetStyle.setEnabled(False)
        self.StE_Patchable()
        self.StE_Part_Melody_Instrument.setText(Instruments[self.styleSelected[0]].Name)
        self.StE_Part_Harmony_Instrument.setText(Instruments[self.styleSelected[1]].Name)
        self.StE_Part_Chords_Instrument.setText(Instruments[self.styleSelected[2]].Name)
        self.StE_Part_Bass_Instrument.setText(Instruments[self.styleSelected[3]].Name)
        self.StE_Part_Percussion1_Instrument.setText(Instruments[self.styleSelected[4]].Name)
        self.StE_Part_Percussion2_Instrument.setText(Instruments[self.styleSelected[5]].Name)
        if (editor.unsafeMode):
            toHighlight = self.styleSelected[self.StE_PartSelector.currentIndex()]
        elif (self.StE_PartSelector.currentIndex() == 4 or self.StE_PartSelector.currentIndex() == 5):
            toHighlight = self.styleSelected[self.StE_PartSelector.currentIndex()] - 40
        else:
            toHighlight = self.styleSelected[self.StE_PartSelector.currentIndex()]
            if (toHighlight == len(Instruments) - 1): toHighlight = 40
        self.StE_InstrumentList.setCurrentRow(toHighlight)

    def Button_StE_Patch(self):
        self.StE_Patch.setEnabled(False)
        if (self.styleSelected != editor.loadedStyles[self.StE_StyleList.currentRow()]):
            editor.loadedStyles[self.StE_StyleList.currentRow()] = self.styleSelected.copy()
            if (Styles[self.StE_StyleList.currentRow()].DefaultStyle == self.styleSelected):
                self.StE_StyleList.item(self.StE_StyleList.currentRow()).setText(
                    Styles[self.StE_StyleList.currentRow()].Name)
            else:
                self.StE_StyleList.item(self.StE_StyleList.currentRow()).setText(
                    Styles[self.StE_StyleList.currentRow()].Name + " ~[" + self.tr("Replaced") + "]~")
                patchInfo = '0' + format(
                    Styles[self.StE_StyleList.currentRow()].MemOffset + BasedOnRegion(gctRegionOffsetsStyles),
                    "x") + " 00000018\n"
                for i in range(3):
                    if (self.styleSelected[i * 2] == len(Instruments) - 1):
                        num1 = "ffffffff"
                    else:
                        num1 = format(self.styleSelected[i * 2], "x")
                    if (self.styleSelected[i * 2 + 1] == len(Instruments) - 1):
                        num2 = "ffffffff"
                    else:
                        num2 = format(self.styleSelected[i * 2 + 1], "x")
                    patchInfo = patchInfo + "0" * (8 - len(num1)) + num1 + " " + "0" * (8 - len(num2)) + num2 + "\n"

                AddPatch(Styles[self.StE_StyleList.currentRow()].Name + " Style Patch", patchInfo)
            SaveRecording(RecordType.Style, self.StE_StyleList.currentRow(), [
                ["0", self.styleSelected[0]],
                ["1", self.styleSelected[1]],
                ["2", self.styleSelected[2]],
                ["3", self.styleSelected[3]],
                ["4", self.styleSelected[4]],
                ["5", self.styleSelected[5]]],
                          Styles[self.StE_StyleList.currentRow()].DefaultStyle == self.styleSelected)

        if (self.StE_ChangeStyleName.isEnabled() and self.StE_ChangeStyleName.text() != editor.textFromTxt[3][
            self.StE_StyleList.currentRow()]):
            ChangeName(self.StE_StyleList.currentRow(), self.StE_ChangeStyleName.text())
            editor.textFromTxt[3][self.StE_StyleList.currentRow()] = self.StE_ChangeStyleName.text()
            SaveRecording(RecordType.TextStyle, self.StE_StyleList.currentRow(),
                          ["name", self.StE_ChangeStyleName.text()])

    #############Text Editor
    def Button_TE_Patch(self):
        file = open(GetMessagePath() + "/message.d/new_music_message.txt", "wb")
        file.write(self.TE_Text.toPlainText().encode("utf-8"))
        file.close()
        EncodeTxt()
        self.MainWidget.setCurrentIndex(0)

    def Button_TE_ExternalEditor(self):
        self.externalEditorOpen = True
        self.TE_Patch.setEnabled(False)
        self.TE_Text.setEnabled(False)
        self.TE_Back_Button.setEnabled(False)
        self.TE_OpenExternal.setEnabled(False)
        self.edit = ExternalEditor()
        self.edit.done.connect(self.TE_FinishEditor)
        self.edit.start()

    def TE_FinishEditor(self):
        file = open(GetMessagePath() + "/message.d/new_music_message.txt", "r+b")
        self.TE_Text.setPlainText(file.read().decode("utf-8"))
        file.close()
        self.TE_Patch.setEnabled(True)
        self.TE_Text.setEnabled(True)
        self.TE_Back_Button.setEnabled(True)
        self.TE_OpenExternal.setEnabled(True)
        self.edit.deleteLater()

    #############Default Style Editor
    def Button_DS_Patch(self):
        AddPatch(Songs[self.DS_Songs.currentRow()].Name + ' Default Style Patch',
                 '0' + format(Songs[self.DS_Songs.currentRow()].MemOffset + BasedOnRegion(gctRegionOffsets) + 42,
                              'x') + ' 000000' + Styles[self.DS_Styles.currentRow()].StyleId + '\n')
        self.DS_Patch.setEnabled(False)
        if (self.fromSongEditor != -1): self.SE_StyleText.setText(Styles[self.DS_Styles.currentRow()].Name)
        SaveRecording(RecordType.DefaultStyle, self.DS_Songs.currentRow(), ["style", self.DS_Styles.currentRow()],
                      self.DS_Styles.currentRow() == GetDefaultStyle(self.DS_Songs.currentRow(), True))

    def List_DS_SongList(self):
        self.DS_StyleBox.setEnabled(True)
        self.DS_Styles.setCurrentRow(GetDefaultStyle(self.DS_Songs.currentRow(), False))

    def List_DS_StyleList(self):
        self.DS_Patch.setEnabled(self.DS_Styles.currentRow() != GetDefaultStyle(self.DS_Songs.currentRow(), False))
        self.DS_Reset.setEnabled(self.DS_Styles.currentRow() != GetDefaultStyle(self.DS_Songs.currentRow(), True))

    def Button_DS_Reset(self):
        self.DS_Styles.setCurrentRow(GetDefaultStyle(self.DS_Songs.currentRow(), True))
        self.DS_Reset.setEnabled(False)

    #############Remove Songs
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

    #############Sound Editor
    def SOE_Patchable(self):
        self.SOE_Patch.setEnabled(self.extraFile != "" and len(self.SOE_SoundType.selectedItems()) != 0)
        self.SOE_PlayAudio.setEnabled(len(self.SOE_SoundType.selectedItems()) != 0)

    def Button_SOE_PlayAudio(self):
        selected = []
        offset = 0
        index = 0x33654
        if (self.SOE_Sounds.currentRow() == 40 + len(extraSounds)):
            index = 0x37B50
        elif (self.SOE_Sounds.currentRow() < 40):
            for i in range(self.SOE_Sounds.currentRow()):
                offset += len(Instruments[i].NumberOfSounds)

        if (self.SOE_Sounds.currentRow() == 40 + len(extraSounds)) or (self.SOE_Sounds.currentRow() < 40):
            for i in range(self.SOE_SoundType.count()):
                if (self.SOE_SoundType.item(i).isSelected()): selected.append(i + offset)
        else:
            for i in range(self.SOE_SoundType.count()):
                if (self.SOE_SoundType.item(i).isSelected()): selected.append(
                    extraSounds[self.SOE_Sounds.currentRow() - 40].typeValues[i])
        PlayRwav(index, selected)
        if (len(selected) > 1):
            playlist = open(SavePath() + "/tmp/playlist.m3u", "w")
            for i in selected:
                if (currentSystem == "Windows"):
                    playlist.write(SavePath().replace("/", "\\") + "\\tmp\\sound" + str(i) + ".rwav.wav\n")
                else:
                    playlist.write(SavePath() + "/tmp/sound" + str(i) + ".rwav.wav\n")
            playlist.close()
            subprocess.Popen(ChooseFromOS(["", "open ", "xdg-open "]) + '"' + SavePath() + '/tmp/playlist.m3u"',
                             shell=True)
        else:
            subprocess.Popen(ChooseFromOS(["", "open ", "xdg-open "]) + '"' + SavePath() + "/tmp/sound" + str(
                selected[0]) + '.rwav.wav"', shell=True)

    def Button_SOE_SwitchType(self):
        wav = wave.open(self.extraFile, "r")
        if (self.SOE_LoopSeconds.isChecked()):
            self.SOE_LoopStart.setDecimals(3)
            self.SOE_LoopEnd.setDecimals(3)
            self.SOE_LoopStart.setValue(self.SOE_LoopStart.value() / wav.getframerate())
            self.SOE_LoopEnd.setValue(self.SOE_LoopEnd.value() / wav.getframerate())
            self.SOE_LoopStart.setMaximum(1000000)
            self.SOE_LoopEnd.setMaximum(1000000)
        else:
            self.SOE_LoopStart.setValue(self.SOE_LoopStart.value() * wav.getframerate())
            self.SOE_LoopEnd.setValue(self.SOE_LoopEnd.value() * wav.getframerate())
            self.SOE_LoopStart.setMaximum(1000000000)
            self.SOE_LoopEnd.setMaximum(1000000000)
            self.SOE_LoopStart.setDecimals(0)
            self.SOE_LoopEnd.setDecimals(0)

    def List_SOE_Sounds(self):
        self.SOE_PlayAudio.setEnabled(False)
        self.SOE_SoundTypeBox.setEnabled(True)
        self.SOE_SoundType.clear()
        if (self.SOE_Sounds.currentRow() == 40 + len(extraSounds)):
            for i in range(142):
                item = QtWidgets.QListWidgetItem()
                item.setText(str(i))
                self.SOE_SoundType.addItem(item)
        elif (self.SOE_Sounds.currentRow() < 40):
            for i in Instruments[self.SOE_Sounds.currentRow()].NumberOfSounds:
                item = QtWidgets.QListWidgetItem()
                item.setText(i)
                self.SOE_SoundType.addItem(item)
        else:
            for i in extraSounds[self.SOE_Sounds.currentRow() - 40].typeNames:
                item = QtWidgets.QListWidgetItem()
                item.setText(i)
                self.SOE_SoundType.addItem(item)

    def Button_SOE_SelectAll(self):
        for i in range(self.SOE_SoundType.count()):
            self.SOE_SoundType.item(i).setSelected(True)
        self.SOE_Patchable()

    def Button_SOE_Browse(self):
        if (self.LoadExtraFile(self.tr("Wav Files") + " (*.wav *.rwav)")):
            self.SOE_Patchable()
            self.SOE_File_Label.setText(os.path.basename(self.extraFile))
            if (pathlib.Path(self.extraFile).suffix == ".wav"):
                self.SOE_Loop.setEnabled(True)
                wav = wave.open(self.extraFile, "r")
                samples = wav.getnframes()
                if (self.SOE_LoopSeconds.isChecked()): samples /= wav.getframerate()
                self.SOE_LoopStart.setValue(0)
                self.SOE_LoopEnd.setValue(samples)
                self.SOE_Loop.setCheckable(True)
            else:
                self.SOE_Loop.setEnabled(False)
                self.SOE_Loop.setCheckable(False)

    def Button_SOE_Patch(self):
        if (pathlib.Path(self.extraFile).suffix == ".wav"):
            if (self.SOE_Loop.isEnabled() and self.SOE_Loop.isChecked()):
                modify = 1
                wav = wave.open(self.extraFile, "r")
                if (self.SOE_LoopSeconds): modify = wav.getframerate()
                rwavInfo, rwavSize = ConvertWav(self.extraFile,
                                                min(self.SOE_LoopStart.value() * modify, wav.getnframes()),
                                                min(self.SOE_LoopEnd.value() * modify, wav.getnframes()))
            else:
                rwavInfo, rwavSize = ConvertWav(self.extraFile)
        else:
            file = open(self.extraFile, "rb")
            rwavInfo = file.read()
            file.close()
            rwavSize = os.stat(self.extraFile).st_size
        index = 0x33654
        selected = []
        offset = 0
        if (self.SOE_Sounds.currentRow() == 40 + len(extraSounds)):
            index = 0x37B50
        elif (self.SOE_Sounds.currentRow() < 40):
            for i in range(self.SOE_Sounds.currentRow()):
                offset += len(Instruments[i].NumberOfSounds)

        if (self.SOE_Sounds.currentRow() == 40 + len(extraSounds)) or (self.SOE_Sounds.currentRow() < 40):
            for i in range(self.SOE_SoundType.count()):
                if (self.SOE_SoundType.item(i).isSelected()): selected.append(i + offset)
        else:
            for i in range(self.SOE_SoundType.count()):
                if (self.SOE_SoundType.item(i).isSelected()): selected.append(
                    extraSounds[self.SOE_Sounds.currentRow() - 40].typeValues[i])

        ReplaceWave(index, selected, rwavInfo, rwavSize)
        self.SOE_Patch.setEnabled(False)


