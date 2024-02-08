import os
import sys

from PySide6.QtGui import QIcon, QFontDatabase
from PySide6.QtWidgets import QApplication

from wii_music_editor.editor.rom_folder import RomFolder
from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.ui.first_setup import FirstSetupWindow
from wii_music_editor.ui.main_window import MainWindow
from wii_music_editor.ui.update import CheckForUpdate, UpdateWindow
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.utils.save import savePath, load_setting
from wii_music_editor.utils.translate import changeLanguage, tr


def startApplication():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(paths.includeAll/"icon"/"icon.png")))
    QFontDatabase.addApplicationFont(str(paths.includeAll/"fonts"/"contb.ttf"))
    QFontDatabase.addApplicationFont(str(paths.includeAll/"fonts"/"contm.ttf"))
    changeLanguage(app)
    return app


def startMainWindow(rom_folder: RomFolder):
    win = MainWindow(rom_folder)
    win.show()
    rom_folder_path = load_setting("Paths", "CurrentLoadedFile", "")
    if rom_folder_path != "":
        try:
            rom_folder.Load(rom_folder_path)
            if rom_folder.loaded:
                win.MP_LoadedFile_Path.setText(str(rom_folder.folderPath))
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

    # Load Folder
    rom_folder = RomFolder()
    # First Setup
    if not os.path.isfile(f"{savePath}/settings.ini"):
        FirstSetupWindow(app, rom_folder)

    # Main Window
    startMainWindow(rom_folder)
    app.exec()


if __name__ == "__main__":
    main()