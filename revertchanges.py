from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from revertchanges_ui import Ui_Dialog
from os import path
from shutil import copyfile
from editor import GetBrsarPath, GetGeckoPath, GetMainDolPath, GetMessagePath
from success import SuccessWindow

class RevertChangesWindow(QDialog,Ui_Dialog):
    def __init__(self):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.setupUi(self)

        self.SelectButton.clicked.connect(lambda: self.SelectAll(True))
        self.DeselectButton.clicked.connect(lambda: self.SelectAll(False))
        self.PatchButton.clicked.connect(self.Revert)

        self.show()
        self.exec()

    def SelectAll(self,select):
        self.Songs.setChecked(select)
        self.Styles.setChecked(select)
        self.Text.setChecked(select)
        self.MainDol.setChecked(select)
        
    def Revert(self):
        if(self.Songs.isChecked()):
            if(path.isfile(GetGeckoPath())):
                codes = open(GetGeckoPath())
                textlines = codes.readlines()
                codes.close()
                linenum = 0
                while linenum < len(textlines):
                    if('Song' in textlines[linenum]):
                        textlines.pop(linenum)
                        while(len(textlines) > linenum) and (textlines[linenum][0].isnumeric() or textlines[linenum][0].isalpha()):
                            textlines.pop(linenum)
                    else:
                        linenum = linenum+1					
                codes = open(GetGeckoPath(),'w')
                codes.writelines(textlines)
                codes.close()
            if(path.isfile(GetBrsarPath()+".backup")):
                copyfile(GetBrsarPath()+".backup",GetBrsarPath())
        if(self.Text.isChecked()):
            if(path.isfile(GetMessagePath()+"/message.carc.backup")):
                copyfile(GetMessagePath()+"/message.carc.backup",GetMessagePath()+"/message.carc")
        if(self.Styles.isChecked()):
            if(path.isfile(GetGeckoPath())):
                codes = open(GetGeckoPath())
                textlines = codes.readlines()
                codes.close()
                linenum = 0
                while linenum < len(textlines):
                    if('Style' in textlines[linenum]):
                        textlines.pop(linenum)
                        while(len(textlines) > linenum) and (textlines[linenum][0].isnumeric() or textlines[linenum][0].isalpha()):
                            textlines.pop(linenum)
                    else:
                        linenum = linenum+1
                codes = open(GetGeckoPath(),'w')
                codes.writelines(textlines)
                codes.close()
        if(self.MainDol.isChecked()):
            if(path.isfile(GetMainDolPath()+".backup")):
                copyfile(GetMainDolPath()+".backup",GetMainDolPath())
        self.close()
        SuccessWindow("Files Reverted!")