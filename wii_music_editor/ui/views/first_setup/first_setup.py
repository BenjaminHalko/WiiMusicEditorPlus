from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt

from wii_music_editor.ui.views.first_setup.first_setup_ui import Ui_FirstSetup
from wii_music_editor.ui.widgets.loadFiles import select_rom_path, select_dolphin_path
import wii_music_editor.utils.paths as paths
from wii_music_editor.utils.save import save_setting
from wii_music_editor.utils.translate import changeLanguage


class FirstSetupWindow(QDialog, Ui_FirstSetup):
    def __init__(self, app):
        super().__init__(None)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        self.app = app

        self.BackButton.setEnabled(False)
        self.BackButton.clicked.connect(self.Back)
        self.NextButton.clicked.connect(self.Next)
        self.LanguageBox.currentIndexChanged.connect(self.LanguageChange)
        self.RomLanguageBox.currentIndexChanged.connect(self.RomLanguageSelect)
        self.RegionBox.currentIndexChanged.connect(self.RegionChange)

        self.RomPath_File.clicked.connect(lambda: self.LoadMainFile("Wii Music Rom (*.wbfs *.iso)"))
        self.RomPath_Folder.clicked.connect(lambda: self.LoadMainFile(""))

        self.Dolphon_Geckocodes.stateChanged.connect(lambda: self.Checkmark(self.Dolphon_Geckocodes, "CopyCodes"))
        self.DolphinEnableCheats.stateChanged.connect(
            lambda: self.Checkmark(self.DolphinEnableCheats, "DolphinEnableCheats"))
        self.DolphinPath_Browse.clicked.connect(self.GetDolphin)

        if paths.dolphinPath != "":
            self.DolphinPath_Label.setText(paths.dolphinPath)

        # self.RomLanguageChange()

        self.show()
        self.exec()

    def Back(self):
        self.MainWidget.setCurrentIndex(self.MainWidget.currentIndex() - 1)
        if self.MainWidget.currentIndex() == 0:
            self.BackButton.setEnabled(False)

    def Next(self):
        if self.MainWidget.currentIndex() == self.MainWidget.count() - 1:
            self.close()
        else:
            self.MainWidget.setCurrentIndex(self.MainWidget.currentIndex() + 1)
            self.BackButton.setEnabled(True)

    def LanguageChange(self):
        save_setting("Settings", "Language", self.LanguageBox.currentIndex())
        changeLanguage(self.app, self.LanguageBox.currentIndex())
        self.retranslateUi(self)
        # editor.RetranslateSongNames()
        self.RomLanguageChange()

    def RegionChange(self):
        # editor.regionSelected = self.RegionBox.currentIndex()
        save_setting("Settings", "DefaultRegion", self.RegionBox.currentIndex())
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
        save_setting("Settings", "RomLanguage", self.RomLanguageBox.currentIndex())
        editor.romLanguageNumber = [self.RomLanguageBox.currentIndex()] * 4
        for i in range(4):
            if (editor.romLanguageNumber[i] >= len(regionNames[i])):
                editor.romLanguageNumber[i] = 0
            editor.romLanguage[i] = regionNames[i][editor.romLanguageNumber[i]]
        if (editor.file.type == LoadType.Rom): GetSongNames()

    def LoadMainFile(self, dialog_filter):
        if select_rom_path(dialog_filter):
            self.RomPath_Label.setText(paths.loadedFilePath)

    def Checkmark(self, checkmark, setting):
        save_setting("Settings", setting, (checkmark.checkState() == 2))

    def GetDolphin(self):
        if select_dolphin_path():
            self.DolphinPath_Label.setText(paths.dolphinPath)
