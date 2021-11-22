from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QFileDialog
from packrom_ui import Ui_Dialog
import editor
from editor import GetMainDolPath, PatchMainDol, HelperPath, Run
from errorhandler import ShowError
from success import SuccessWindow
from pathlib import Path
from shutil import copyfile, move
from os import remove, path

class PackRomWindow(QDialog,Ui_Dialog):
    def __init__(self):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.setupUi(self)
        self.CreateRom.clicked.connect(self.MakeRom)
        self.show()
        self.exec()

    def MakeRom(self):
        file = QFileDialog()
        file.setFileMode(QFileDialog.AnyFile)
        file.setAcceptMode(QFileDialog.AcceptSave)
        if(self.RomTypeWbfs.isChecked()): file.setNameFilter("Wii Backup File System (*.wbfs)")
        else: file.setNameFilter("iso (*.iso)")
        if(file.exec()):
            try:
                filePath = file.selectedFiles()[0]
                if(self.RomTypeWbfs.isChecked()): fileType = ".wbfs"
                else: fileType = ".iso"
                if(path.exists(filePath)): remove(filePath)
                if(Path(filePath).suffix != fileType): filePath = filePath+fileType
                args = [HelperPath()+'/Wiimms/wit','cp',editor.file.path,filePath]
                if(self.RomTypeWbfs.isChecked()): args.append('--wbfs')
                if(self.PatchMainDolCheckbox.isChecked()):
                    copyfile(GetMainDolPath(),GetMainDolPath()+".tmp")
                    PatchMainDol()
                Run(args)
                if(self.PatchMainDolCheckbox.isChecked()):
                    remove(GetMainDolPath())
                    move(GetMainDolPath()+".tmp",GetMainDolPath())
                self.close()
                SuccessWindow("Rom Successfuly Packed!")      
            except Exception as e:
                self.close()
                ShowError("Could not pack rom",str(e))