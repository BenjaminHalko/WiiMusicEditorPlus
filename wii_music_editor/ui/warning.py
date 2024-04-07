import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from wii_music_editor.ui.widgets.checkmark import Checkmark
from wii_music_editor.ui.windows.warning_ui import Ui_Warning
from wii_music_editor.utils.save import load_setting


def show_warning(message: str, error_id: str):
    if load_setting("warning", error_id, False):
        return
    logging.warning(message.replace("\n", " "))
    WarningWindow(message, error_id)


class WarningWindow(QDialog, Ui_Warning):
    def __init__(self, message: str, error_id: str):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setupUi(self)
        self.WarningText.setText(message)
        self.WarningClose.clicked.connect(self.close)
        Checkmark(self.WarningDisable, "warning", error_id)
        self.show()
        self.exec()
