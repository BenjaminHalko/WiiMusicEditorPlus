import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog
from wii_music_editor.ui.windows.error_handler_ui import Ui_Error


class ShowError(QDialog, Ui_Error):
    def __init__(self, error, message, parent=None, gecko_code=False):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setupUi(self)
        if not gecko_code:
            self.ErrorTitle.setText(error)
            self.ErrorMessage.setText(message)
            self.ErrorClose.clicked.connect(self.close)
        else:
            self.clicked = False
            self.ErrorTitle_GC.setText(error)
            self.ErrorMessage_GC.setText(message)
            self.ErrorClose_GC.clicked.connect(self.close)
            self.ErrorCreate_GC.clicked.connect(self.GeckoCodeCreate)
            self.MainWidget.setCurrentIndex(1)
        logging.error(f"{error}: {message}")
        self.show()
        self.exec()

    def GeckoCodeCreate(self):
        self.clicked = True
        self.close()
