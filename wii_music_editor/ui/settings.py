from os import path
from PySide6.QtCore import Qt, QLocale, QTranslator
from PySide6.QtWidgets import QDialog
from PySide6 import QtWidgets
from wii_music_editor.ui import Ui_Settings
import editor
from editor import SaveSetting, load_setting, ChooseFromOS, languageList, TranslationPath, regionNames, GetSongNames, \
    LoadType
from errorhandler import ShowError
from update import UpdateWindow, CheckForUpdate


class SettingsWindow(QDialog, Ui_Settings):
    def __init__(self, otherWindow, app, translator):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setupUi(self)
        self.otherWindow = otherWindow
        self.app = app
        self.translator = translator

        self.RegionBox.setCurrentIndex(load_setting("Settings", "DefaultRegion", 0))
        self.RegionBox.currentIndexChanged.connect(self.RegionChange)
        self.LanguageBox.setCurrentIndex(load_setting("Settings", "Language", 0))
        self.LanguageBox.currentIndexChanged.connect(self.LanguageChange)
        self.RomLanguageBox.setCurrentIndex(editor.romLanguageNumber[load_setting("Settings", "DefaultRegion", 0)])
        self.RomLanguageBox.currentIndexChanged.connect(self.RomLanguageSelect)

        self.SwitchBeta.clicked.connect(self.Button_SwitchBeta)
        if (load_setting("Settings", "Beta", False)): self.SwitchBeta.setText(self.tr("Switch to Main"))

        self.ConnectCheckmark(self.CheckForUpdates, "AutoUpdate", True)
        self.ConnectCheckmark(self.RapperFix, "RapperFix", True)
        self.ConnectCheckmark(self.UnsafeMode, "UnsafeMode", False)
        self.ConnectCheckmark(self.SongScoreCheckbox, "SongScore", False)
        self.ConnectCheckmark(self.Dolphon_Geckocodes, "CopyCodes", True)
        self.ConnectCheckmark(self.SongScoreCheckbox, "LoadSongSeparately", False)
        self.ConnectCheckmark(self.DolphinEnableCheats, "DolphinEnableCheats", True)
        self.ConnectCheckmark(self.Normalize, "NormalizeMidi", False)
        self.ConnectCheckmark(self.RevertChanges, "RemoveChangesFromChangesINI", True)
        self.ConnectCheckmark(self.Discord, "Discord", True)

        self.DolphinPath_Browse.clicked.connect(self.GetDolphin)
        self.DolphinSave_Browse.clicked.connect(self.GetDolphinSave)
        self.DolphinSave_Default.clicked.connect(self.DefaultDolphinSave)

        self.RomLanguageChange()

        if (editor.dolphinPath != ""): self.DolphinPath_Label.setText(editor.dolphinPath)
        if (editor.dolphinSavePath != ""): self.DolphinSave_Label.setText(editor.dolphinSavePath)

        self.show()
        self.exec()

    def Button_SwitchBeta(self):
        SaveSetting("Settings", "Beta", not load_setting("Settings", "Beta", False))
        if (load_setting("Settings", "Beta", False)):
            self.SwitchBeta.setText(self.tr("Switch to Main"))
        else:
            self.SwitchBeta.setText(self.tr("Switch to Beta"))
        version = CheckForUpdate()
        if (version != "null"): UpdateWindow([self.otherWindow, self], version)

    def ConnectCheckmark(self, checkmarkId, setting, default):
        checkmarkId.setCheckState(load_setting("Settings", setting, default) * 2)
        checkmarkId.stateChanged.connect(lambda: self.Checkmark(checkmarkId, setting))

    def Checkmark(self, checkmark, setting):
        SaveSetting("Settings", setting, (checkmark.checkState() == 2))
        if (setting == "UnsafeMode"): editor.unsafeMode = (checkmark.checkState() == 2)
        if (setting == "LoadSongSeparately"): self.otherWindow.SE_SeparateSongPatching()

    def RegionChange(self):
        if (editor.file.type != LoadType.Rom):
            editor.regionSelected = self.RegionBox.currentIndex()
        SaveSetting("Settings", "DefaultRegion", self.RegionBox.currentIndex())
        self.RomLanguageChange()

    def RomLanguageChange(self):
        self.RomLanguageBox.blockSignals(True)
        self.RomLanguageBox.clear()
        romLanguageList = [self.tr("English"), self.tr("French"), self.tr("Spanish"), self.tr("Germen"),
                           self.tr("Italian"), self.tr("Japanese"), self.tr("Korean")]
        if (self.RegionBox.currentIndex() > 1):
            self.RomLanguageBox.addItem(romLanguageList[3 + self.RegionBox.currentIndex()])
        else:
            for i in range(3 + 2 * self.RegionBox.currentIndex()):
                self.RomLanguageBox.addItem(romLanguageList[i])
        self.RomLanguageBox.setCurrentIndex(editor.romLanguageNumber[self.RegionBox.currentIndex()])
        self.RomLanguageBox.blockSignals(False)

    def RomLanguageSelect(self):
        SaveSetting("Settings", "RomLanguage", self.RomLanguageBox.currentIndex())
        editor.romLanguageNumber = [self.RomLanguageBox.currentIndex()] * 4
        for i in range(4):
            if (editor.romLanguageNumber[i] >= len(regionNames[i])):
                editor.romLanguageNumber[i] = 0
            editor.romLanguage[i] = regionNames[i][editor.romLanguageNumber[i]]
        if (editor.file.type == LoadType.Rom): GetSongNames()

    def LanguageChange(self):
        SaveSetting("Settings", "Language", self.LanguageBox.currentIndex())
        self.app.removeTranslator(self.translator)
        if (self.LanguageBox.currentIndex() != 0):
            translator = QTranslator()
            translator.load(QLocale(), TranslationPath() + f"/{languageList[self.LanguageBox.currentIndex()]}.qm")
            self.app.installTranslator(translator)
        self.retranslateUi(self)
        self.otherWindow.retranslateUi(self.otherWindow)
        editor.RetranslateSongNames()
        self.RomLanguageChange()

    def GetDolphin(self):
        file = QtWidgets.QFileDialog()
        file.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        file.setNameFilter(ChooseFromOS(["Dolphin (Dolphin.exe)", "Dolphin (Dolphin.app)", "Dolphin (dolphin-emu)"]))
        if file.exec_():
            editor.dolphinPath = file.selectedFiles()[0]
            self.DolphinPath_Label.setText(file.selectedFiles()[0])
            SaveSetting("Paths", "Dolphin", file.selectedFiles()[0])

    def DefaultDolphinSave(self):
        self.DolphinSave_Label.setText(self.tr("Default Path"))
        SaveSetting("Paths", "DolphinSave", "")

    def GetDolphinSave(self):
        file = QtWidgets.QFileDialog()
        file.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        if file.exec_():
            if (path.isdir(file.selectedFiles()[0] + "/Wii") and path.isdir(file.selectedFiles()[0] + "/GameSettings")):
                editor.dolphinSavePath = file.selectedFiles()[0]
                self.DolphinSave_Label.setText(file.selectedFiles()[0])
                SaveSetting("Paths", "DolphinSave", file.selectedFiles()[0])
            else:
                self.hide()
                ShowError(self.tr("Not a Dolphin Save Directory"), self.tr("Wii and GameSettings folder not found"))
                self.show()