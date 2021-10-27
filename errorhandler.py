from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QDialog
from error_ui import Ui_Error

class ShowError(QDialog,Ui_Error):
    def __init__(self,error,message):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.setWindowModality(Qt.ApplicationModal)
        self.setupUi(self)
        self.ErrorTitle.setText(QCoreApplication.translate("MainWindow",error))
        self.ErrorMessage.setText(QCoreApplication.translate("MainWindow",message))
        self.ErrorClose.clicked.connect(self.close)
        self.show()
        self.exec()