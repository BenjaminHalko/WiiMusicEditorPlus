from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog
from wii_music_editor.ui.views.warning.warning_ui import Ui_Warning


class ShowWarning(QDialog, Ui_Warning):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setupUi(self)
        self.WarningText.setText(message)
        self.WarningClose.clicked.connect(self.close)
        self.show()
        self.exec()
