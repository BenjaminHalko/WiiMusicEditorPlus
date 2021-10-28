from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from settings_ui import Ui_Settings
import editor
from editor import SaveSetting, LoadSetting

class SettingsWindow(QDialog,Ui_Settings):
    def __init__(self):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.setWindowModality(Qt.ApplicationModal)
        self.setupUi(self)

        self.RegionBox.setCurrentIndex(editor.regionSelected)
        self.RegionBox.currentIndexChanged.connect(self.RegionChange)

        self.show()
        self.exec()

    def RegionChange(self):
        editor.regionSelected = self.RegionBox.currentIndex()
        SaveSetting("Settings","DefaultRegion",editor.regionSelected)