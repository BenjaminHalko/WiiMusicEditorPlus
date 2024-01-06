from os import path, remove

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog

from wii_music_editor.services.update import CheckForUpdate, UpdateThread
from wii_music_editor.ui.views.update.update_ui import Ui_Update


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
        if (currentSystem == "Windows"): updateExt = ".bat"
        if (path.exists(SavePath() + "/update" + updateExt)): remove(SavePath() + "/update" + updateExt)
        copyfile(HelperPath() + "/Extra/update" + updateExt, SavePath() + "/update" + updateExt)

        if (currentSystem == "Windows"):
            Popen([SavePath() + "/update.bat", FullPath])
        else:
            GivePermission(SavePath() + "/update.sh")
            if (currentSystem == "Linux"): GivePermission(SavePath() + '/WiiMusicEditorPlus')
            Popen([SavePath() + "/update.sh", FullPath])
        self.close()
        self.parent.close()
        sys_exit()


