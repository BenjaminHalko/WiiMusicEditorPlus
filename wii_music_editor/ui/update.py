import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget

from wii_music_editor.ui.windows.update_ui import Ui_Update
from wii_music_editor.utils.update import CheckForUpdate, UpdateEditor


class UpdateWindow(QDialog, Ui_Update):
    def __init__(self, parent: QWidget, check: bool = True):
        super().__init__(None)
        self.parent = parent
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        if not check:
            check = CheckForUpdate()
            if not check:
                self.MainWidget.setCurrentIndex(2)

        self.NewUpdate_Update.clicked.connect(self.update)
        self.NewUpdate_Cancel.clicked.connect(self.close)
        self.NoUpdate_Button.clicked.connect(self.close)

        self.show()
        self.exec()

    def update(self):
        if UpdateEditor():
            self.restart()

    def restart(self):
        self.close()
        self.parent.close()
        sys.exit(0)
