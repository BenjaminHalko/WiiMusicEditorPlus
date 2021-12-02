from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QDialog
from error_ui import Ui_Error

class ShowError(QDialog,Ui_Error):
    def __init__(self,error,message,parent=None,geckocode=False):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.setupUi(self)
        if(not geckocode):
            self.ErrorTitle.setText(QCoreApplication.translate("MainWindow",error))
            self.ErrorMessage.setText(QCoreApplication.translate("MainWindow",message))
            self.ErrorClose.clicked.connect(self.close)
        else:
            self.clicked = False
            self.ErrorTitle_GC.setText(QCoreApplication.translate("MainWindow",error))
            self.ErrorMessage_GC.setText(QCoreApplication.translate("MainWindow",message))
            self.ErrorClose_GC.clicked.connect(self.close)
            self.ErrorCreate_GC.clicked.connect(self.GeckoCodeCreate)
            self.MainWidget.setCurrentIndex(1)
        self.show()
        self.exec()

    def GeckoCodeCreate(self):
        self.clicked = True
        self.close()