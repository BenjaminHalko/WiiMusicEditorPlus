from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from wii_music_editor.ui.windows.confirm_ui import Ui_Confirm


class ConfirmWindow(QDialog, Ui_Confirm):
    def __init__(self, message):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setupUi(self)
        self.clicked = False

        self.text.setText(message)
        self.noButton.clicked.connect(self.close)
        self.yesButton.clicked.connect(self.Ok)

        self.show()
        self.exec()

    def Ok(self):
        self.clicked = True
        self.close()


def ConfirmDialog(message):
    win = ConfirmWindow(message)
    return win.clicked
