import logging
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog
from wii_music_editor.ui.windows.error_handler_ui import Ui_Error


class ShowError(QDialog, Ui_Error):
    def __init__(self, error, message, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setupUi(self)
        self.ErrorTitle.setText(error)
        self.ErrorMessage.setText(message)
        self.ErrorClose.clicked.connect(self.close)
        self.show()
        self.exec()
