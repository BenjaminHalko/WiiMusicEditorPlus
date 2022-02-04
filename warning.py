from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from warning_ui import Ui_Warning

class ShowWarning(QDialog,Ui_Warning):
    def __init__(self,message,parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.setupUi(self)
        self.WarningText.setText(message)
        self.WarningClose.clicked.connect(self.close)
        self.show()
        self.exec()