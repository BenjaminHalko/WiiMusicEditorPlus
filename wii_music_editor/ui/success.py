from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from wii_music_editor.ui.windows.success_ui import Ui_Success


class SuccessWindow(QDialog, Ui_Success):
    def __init__(self, message):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setupUi(self)
        self.CompleteTitle.setText(message)
        self.CompleteClose.clicked.connect(self.close)
        self.show()
        self.exec()
