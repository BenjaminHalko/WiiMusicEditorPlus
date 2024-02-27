from PySide6.QtCore import Qt, QLocale, QTranslator
from PySide6.QtWidgets import QDialog
from wii_music_editor.ui.widgets.checkmark import Checkmark
from wii_music_editor.ui.widgets.load_files import select_dolphin_path, select_dolphin_save_path
from wii_music_editor.ui.widgets.translate import tr
from wii_music_editor.ui.windows.settings_ui import Ui_Settings
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.utils.preferences import preferences
from wii_music_editor.utils.save import save_setting


class SettingsWindow(QDialog, Ui_Settings):
    __checkUpdate: Checkmark
    __rapperFix: Checkmark
    __unsafeMode: Checkmark
    __songScore: Checkmark
    __normalize: Checkmark
    __discord: Checkmark

    def __init__(self):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setupUi(self)

        # self.LanguageBox.setCurrentIndex(load_setting("Settings", "Language", 0))
        # self.LanguageBox.currentIndexChanged.connect(self.LanguageChange)
        # self.RomLanguageBox.setCurrentIndex(editor.romLanguageNumber[load_setting("Settings", "DefaultRegion", 0)])
        # self.RomLanguageBox.currentIndexChanged.connect(self.RomLanguageSelect)

        self.__checkUpdate = Checkmark(self.CheckForUpdates, "preferences", "auto_update", preferences)
        self.__rapperFix = Checkmark(self.RapperFix, "preferences", "rapper_crash_fix", preferences)
        self.__unsafeMode = Checkmark(self.UnsafeMode, "preferences", "unsafe_mode", preferences)
        self.__songScore = Checkmark(self.SongScoreCheckbox, "preferences", "separate_tracks", preferences)
        self.__normalize = Checkmark(self.Normalize, "preferences", "normalize_midi", preferences)
        self.__discord = Checkmark(self.Discord, "preferences", "using_discord", preferences)

        self.DolphinPath_Browse.clicked.connect(self.get_dolphin)
        self.DolphinSave_Browse.clicked.connect(self.get_dolphin_save)
        self.DolphinSave_Default.clicked.connect(self.default_dolphin_save)

        # self.rom_langauge_change()

        if paths.dolphin is not None:
            self.DolphinPath_Label.setText(str(paths.dolphin))
        if paths.dolphinSave is not None:
            self.DolphinSave_Label.setText(str(paths.dolphinSave))

        self.show()
        self.exec()

    def rom_langauge_change(self):
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

    def langauge_change(self):
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

    def get_dolphin(self):
        changed = select_dolphin_path()
        if changed:
            self.DolphinPath_Label.setText(str(paths.dolphin))

    def default_dolphin_save(self):
        self.DolphinSave_Label.setText(tr("settings", "Default Path"))
        save_setting("Paths", "DolphinSave", "")
        paths.setDolphinSavePath("")

    def get_dolphin_save(self):
        changed = select_dolphin_save_path()
        if changed:
            self.DolphinPath_Label.setText(str(paths.dolphin))
