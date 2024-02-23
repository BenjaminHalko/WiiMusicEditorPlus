from PySide6.QtWidgets import QDialog, QApplication
from PySide6.QtCore import Qt

from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.ui.windows.first_setup_ui import Ui_FirstSetup
from wii_music_editor.ui.widgets.load_files import select_rom_path, select_dolphin_path
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.utils.save import save_setting
from wii_music_editor.ui.widgets.translate import tr


class FirstSetupWindow(QDialog, Ui_FirstSetup):

    def __init__(self, app: QApplication):
        super().__init__(None)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        self.app = app

        self.BackButton.setEnabled(False)
        self.BackButton.clicked.connect(self.Back)
        self.NextButton.clicked.connect(self.Next)
        # self.RomLanguageBox.currentIndexChanged.connect(self.RomLanguageSelect)
        # self.RegionBox.currentIndexChanged.connect(self.RegionChange)

        self.RomPath_File.clicked.connect(lambda: self.LoadMainFile("Wii Music Rom (*.wbfs *.iso)"))
        self.RomPath_Folder.clicked.connect(lambda: self.LoadMainFile(""))

        self.DolphinPath_Browse.clicked.connect(self.GetDolphin)

        if paths.dolphin != "":
            self.DolphinPath_Label.setText(str(paths.dolphin))

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

    def RomLanguageChange(self):
        self.RomLanguageBox.blockSignals(True)
        self.RomLanguageBox.clear()
        rom_language_list = [
            tr("Language", "English"),
            tr("Language", "French"),
            tr("Language", "Spanish"),
            tr("Language", "Germen"),
            tr("Language", "Italian"),
            tr("Language", "Japanese"),
            tr("Language", "Korean")
        ]
        if self.RegionBox.currentIndex() > 1:
            self.RomLanguageBox.addItem(rom_language_list[3 + self.RegionBox.currentIndex()])
        else:
            for i in range(3 + 2 * self.RegionBox.currentIndex()):
                self.RomLanguageBox.addItem(rom_language_list[i])
        self.RomLanguageBox.setCurrentIndex(romLanguageNumber[self.RegionBox.currentIndex()])
        self.RomLanguageBox.blockSignals(False)

    def RomLanguageSelect(self):
        save_setting("Settings", "RomLanguage", self.RomLanguageBox.currentIndex())
        region.romLanguageNumber = [self.RomLanguageBox.currentIndex()] * 4
        for i in range(4):
            if region.romLanguageNumber[i] >= len(regionNames[i]):
                region.romLanguageNumber[i] = 0
            region.romLanguage[i] = regionNames[i][region.romLanguageNumber[i]]

    def LoadMainFile(self, dialog_filter):
        if select_rom_path(dialog_filter):
            self.RomPath_Label.setText(str(rom_folder.folderPath))

    def GetDolphin(self):
        if select_dolphin_path():
            self.DolphinPath_Label.setText(str(paths.dolphin))
