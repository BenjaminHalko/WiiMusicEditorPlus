from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QDialog
from success_ui import Ui_Dialog

class SuccessWindow(QDialog,Ui_Dialog):
    def __init__(self,message):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.setupUi(self)
        self.CompleteTitle.setText(QCoreApplication.translate("MainWindow",message))
        self.CompleteClose.clicked.connect(self.close)
        self.show()
        self.exec()