import os
import sys

from PyQt6.QtGui import QIcon, QFontDatabase
from PyQt6.QtWidgets import QApplication

from wii_music_editor.ui.views.first_setup.first_setup import FirstSetupWindow
from wii_music_editor.utils.paths import modulePath
from wii_music_editor.utils.save import savePath
from wii_music_editor.utils.translate import changeLanguage


def startApplication():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(modulePath/"res"/"icon"/"icon.png")))
    QFontDatabase.addApplicationFont(str(modulePath/"fonts"/"contb.ttf"))
    QFontDatabase.addApplicationFont(str(modulePath/"fonts"/"contm.ttf"))
    changeLanguage(app)
    return app


def startMainWindow():
    win = Window()
    win.show()
    if (editor.file.path != ""):
        try:
            PrepareFile()
        except:
            editor.file.path = ""
    if (editor.file.path == "" and LoadSetting("Paths", "CurrentLoadedFile", "") != ""): ShowError(
        _translate("Window", "Could not load file"), _translate("Window", "One or more errors have occurred"))
    if (LoadSetting("Settings", "AutoUpdate", True)):
        try:
            version = CheckForUpdate()
            if (version != "null"): UpdateWindow(win, version)
        except:
            print("Could Not Update")
    win.SE_SeperateSongPatching()


def main():
    app = startApplication()

    # First Setup
    if not os.path.isfile(f"{savePath}/settings.ini") or True:
        FirstSetupWindow(app)
    app.exec()


if __name__ == "__main__":
    main()
