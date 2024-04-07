import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget, QApplication

from wii_music_editor.ui.widgets.translate import tr
from wii_music_editor.ui.windows.update_ui import Ui_Update
from wii_music_editor.utils.update import CheckForUpdate, GetLatestVersion
from wii_music_editor.utils.version import GetCurrentVersion


class UpdateWindow(QDialog, Ui_Update):
    def __init__(self, parent: QWidget, local_version: str = "", latest_version: str = ""):
        super().__init__(None)
        self.parent = parent
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        if local_version == "":
            local_version = GetCurrentVersion()
            latest_version = GetLatestVersion()
            if not CheckForUpdate(local_version, latest_version):
                self.MainWidget.setCurrentIndex(1)

        self.NewUpdate_CurrentVersion.setText(local_version)
        self.NewUpdate_NewVersion.setText(latest_version)
        self.NewUpdate_Copy.clicked.connect(self.copyToClipboard)
        self.NewUpdate_Update.clicked.connect(self.update)
        self.NewUpdate_Cancel.clicked.connect(self.close)
        self.NoUpdate_Button.clicked.connect(self.close)

        self.show()
        self.exec()

    def copyToClipboard(self):
        self.NewUpdate_Copy.setText(tr("Update", "Copied"))
        QApplication.clipboard().setText("pip install wii-music-editor -U")

    def update(self):
        self.close()
        self.parent.close()
        sys.exit(0)
