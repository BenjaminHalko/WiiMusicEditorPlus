import os
import sys

from PySide6.QtGui import QIcon, QFontDatabase
from PySide6.QtWidgets import QApplication

from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.ui.first_setup import FirstSetupWindow
from wii_music_editor.ui.main_window import MainWindow
from wii_music_editor.ui.update import CheckForUpdate, UpdateWindow
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.utils.save import savePath, load_setting
from wii_music_editor.ui.widgets.translate import changeLanguage, tr


def startApplication():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(paths.includeAll/"icon"/"icon.png")))
    QFontDatabase.addApplicationFont(str(paths.includeAll/"fonts"/"contb.ttf"))
    QFontDatabase.addApplicationFont(str(paths.includeAll/"fonts"/"contm.ttf"))
    changeLanguage(app)
    return app


def startMainWindow():
    win = MainWindow()
    win.show()
    rom_folder_path = load_setting("Paths", "CurrentLoadedFile", "")
    if rom_folder_path != "":
        try:
            rom_folder.load(rom_folder_path)
            if rom_folder.loaded:
                win.MP_LoadedFile_Path.setText(str(rom_folder.folderPath))
            else:
                win.MP_LoadedFile_Path.setText("Error Loading File")
        except Exception as e:
            ShowError(tr("Error", "Could not load file"), tr("Error", "One or more errors have occurred"))
            print("Error loading file:", e)
    if load_setting("Settings", "AutoUpdate", True):
        try:
            version = CheckForUpdate()
            if version != "null":
                UpdateWindow(win, version)
        except Exception as e:
            print("Could Not Update:", e)
    win.SE_SeparateSongPatching()


def main():
    app = startApplication()

    # First Setup
    if not os.path.isfile(f"{savePath}/settings.ini"):
        FirstSetupWindow(app)

    # Main Window
    startMainWindow()
    app.exec()


if __name__ == "__main__":
    main()
