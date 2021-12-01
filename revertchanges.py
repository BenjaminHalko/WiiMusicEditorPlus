from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from revertchanges_ui import Ui_Dialog
from os import path
from shutil import copyfile
from editor import GetBrsarPath, GetGeckoPath, GetMainDolPath, GetMessagePath, GetSongNames
from success import SuccessWindow
from errorhandler import ShowError
import editor
from editor import RecordType
from configparser import ConfigParser

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
        sections = []
        if(path.isfile(editor.file.path+"/Changes.ini")):
            ini = ConfigParser()
            ini.read(editor.file.path+"/Changes.ini")
            sections = ini.sections()

        if(self.Songs.isChecked()):
            try:
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
                copyfile(GetBrsarPath()+".backup",GetBrsarPath())
                for section in sections:
                    if(RecordType.Song in section): ini.remove_section(section)
            except Exception as e:
                ShowError("Could not revert songs",str(e))
        if(self.Text.isChecked()):
            try:
                copyfile(GetMessagePath()+"/message.carc.backup",GetMessagePath()+"/message.carc")
                GetSongNames()
                for section in sections:
                    if(RecordType.TextSong in section or RecordType.TextStyle in section): ini.remove_section(section)
            except Exception as e:
                ShowError("Could not revert message file",str(e))
        if(self.Styles.isChecked()):
            try:
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
                for section in sections:
                    if(RecordType.Style in section or RecordType.DefaultStyle in section): ini.remove_section(section)
            except Exception as e:
                ShowError("Could not revert styles",str(e))
        if(self.MainDol.isChecked()):
            try:
                copyfile(GetMainDolPath()+".backup",GetMainDolPath())
                for section in sections:
                    if(RecordType.RemoveSong in section or RecordType.MainDol in section): ini.remove_section(section)
            except Exception as e:
                ShowError("Could not revert main.dol",str(e))
        if(path.isfile(editor.file.path+"/Changes.ini")):
            with open(editor.file.path+"/Changes.ini", 'w') as inifile:
                ini.write(inifile)
        self.close()
        SuccessWindow("Files Reverted!")