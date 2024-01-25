import sys
from os import remove
from shutil import copyfile
from subprocess import Popen

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from wii_music_editor.services.update import CheckForUpdate, UpdateThread
from wii_music_editor.ui.windows.update_ui import Ui_Update
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.utils.osUtils import currentSystem, SystemType
from wii_music_editor.utils.shell import give_permission


class UpdateWindow(QDialog, Ui_Update):
    def __init__(self, parent, check):
        super().__init__(None)
        self.parent = parent
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        self.switchBranch = False
        if not check:
            check = CheckForUpdate()
            if check == "null":
                self.MainWidget.setCurrentIndex(2)

        self.version = check
        self.NewUpdate_Update.clicked.connect(self.start_update)
        self.NewUpdate_Cancel.clicked.connect(self.close)
        self.NoUpdate_Button.clicked.connect(self.close)

        self.show()
        self.exec()

    def start_update(self):
        self.MainWidget.setCurrentIndex(1)
        UpdateThread.version = self.version
        UpdateThread.progress.connect(self.reportProgress)
        UpdateThread.done.connect(self.restart)
        UpdateThread.start()

    def reportProgress(self, value):
        self.Update_Progress.setValue(value)

    def restart(self):
        updateExt = ".sh"
        if currentSystem == SystemType.Windows:
            updateExt = ".bat"
        if (paths.save/f"update{updateExt}").exists():
            remove(paths.save/f"update{updateExt}")
        copyfile(paths.include/"update"/f"update{updateExt}", paths.save/"update"/f"update{updateExt}")

        if currentSystem == SystemType.Windows:
            Popen([paths.save / "update.bat", paths.full])
        else:
            give_permission(paths.save / "update.sh")
            if currentSystem == SystemType.Linux:
                give_permission(paths.save / "WiiMusicEditorPlus")
            Popen([paths.save / "update.sh", paths.full])
        self.close()
        self.parent.close()
        sys.exit(0)
