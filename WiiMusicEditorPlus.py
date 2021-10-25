import os
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from main_window_ui import Ui_MainWindow
import logging

import editor
from editor import ChangeName, ProgramPath, Songs, Styles, currentSystem, SongTypeValue, LoadType, PrepareFile, SaveSetting, LoadSetting, LoadMidi, PatchBrsar
from update import UpdateWindow, CheckForUpdate

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
logger.name = "logger"
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
#fh = logging.FileHandler('log.txt')
#fh.setFormatter(formatter)
logger.addHandler(handler)
#logger.addHandler(fh)

logger.info("Program Started in "+ProgramPath)
logger.info("OS: "+currentSystem)

_translate = QtCore.QCoreApplication.translate
defaultStyle = ""

extraFile = ""
brseqInfo = 0
brseqLength = 0
lastExtraFileDirectory = LoadSetting("Paths","LastExtraLoadedPath","")
lastFileDirectory = LoadSetting("Paths","LastLoadedPath","")

def Error(widget):
    widget.setProperty("error", "true")
    widget.style().polish(widget)
    widget.update()

def UnError(widget):
    widget.setProperty("error", "false")
    widget.style().polish(widget)
    widget.update()

def AllowType(type):
    return (editor.loadedType == LoadType.Rom or editor.loadedType == type)

def LoadMainFile(filter):
    global extraFile
    global lastFileDirectory
    file = QtWidgets.QFileDialog() 
    file.setFileMode(QtWidgets.QFileDialog.AnyFile)
    file.setNameFilter(filter)
    file.setViewMode(QtWidgets.QFileDialog.Detail)
    file.setDirectory(lastFileDirectory)
    if file.exec_():
        editor.loadedFile = file.selectedFiles()[0]
        lastFileDirectory = os.path.dirname(extraFile)
        SaveSetting("Paths","LastLoadedPath",lastFileDirectory)
        return True
    return False

def LoadExtraFile(filter):
    global extraFile
    global lastExtraFileDirectory
    file = QtWidgets.QFileDialog() 
    file.setFileMode(QtWidgets.QFileDialog.AnyFile)
    file.setNameFilter(filter)
    file.setViewMode(QtWidgets.QFileDialog.Detail)
    file.setDirectory(lastExtraFileDirectory)
    if file.exec_():
        extraFile = file.selectedFiles()[0]
        lastExtraFileDirectory = os.path.dirname(extraFile)
        SaveSetting("Paths","LastExtraLoadedPath",lastExtraFileDirectory)
        return True
    return False

def LoadSongs(widgetID):
    for i in range(len(Songs)):
        item = QtWidgets.QListWidgetItem()
        extraText = ""
        if(len(editor.textFromTxt[0]) > i) and AllowType(LoadType.Carc) and (Songs[i].SongType != SongTypeValue.Regular or editor.textFromTxt[0][i] != Songs[i].Name) and (Songs[i].SongType != SongTypeValue.Maestro or editor.textFromTxt[0][i] != Songs[i].Name[0:len(Songs[i].Name)-14:1]) and (Songs[i].SongType != SongTypeValue.Handbell or editor.textFromTxt[0][i] != Songs[i].Name[0:len(Songs[i].Name)-19:1]) and (Songs[i].SongType != SongTypeValue.Menu): extraText = " ("+editor.textFromTxt[0][i]+")"
        item.setText(_translate("MainWindow", Songs[i].Name)+extraText)
        widgetID.addItem(item)

def LoadStyles(widgetID):
    for i in range(len(Styles)):
        item = QtWidgets.QListWidgetItem()
        item.setText(_translate("MainWindow", Styles[i].Name))
        widgetID.addItem(item)

#Menu Bar Buttons
def MenuBar_Load_Rom(self):
    if(LoadMainFile("""All supported files (*.wbfs *.iso *.brsar *.carc *.dol *midi *.mid *.brseq *.rseq *.gct *.txt)
    Wii Music Rom (*.wbfs *.iso)
    Sound Archive (*.brsar)
    Text File (*.carc)
    Main.dol (*.dol)
    Midi-Type File (*.midi *.mid *.brseq *.rseq)
    Geckocode (*.gct *.txt)""")):
        PrepareFile()
        self.MP_LoadedFile_Path.setText(_translate("MainWindow", editor.loadedFile))

#Song Editor Buttons

def Button_SE_SongToChange(self):
    global brseqInfo
    global brseqLength
    if(LoadExtraFile("Midi-Type File (*.midi *.mid *.brseq *.rseq)")):
        midiInfo = LoadMidi(extraFile)
        UnError(self.SE_Midi_File_Label)
        self.SE_Midi_File_Label.setText(_translate("MainWindow", os.path.basename(extraFile)))
        if(midiInfo[2] != 0): self.SE_Midi_Tempo_Input.setText(_translate("MainWindow", str(midiInfo[2])))
        self.SE_Midi_TimeSignature_3.setAutoExclusive(False)
        self.SE_Midi_TimeSignature_4.setAutoExclusive(False)
        self.SE_Midi_TimeSignature_3.setChecked(midiInfo[4] == 3)
        self.SE_Midi_TimeSignature_4.setChecked(midiInfo[4] != 3)
        self.SE_Midi_TimeSignature_3.setAutoExclusive(True)
        self.SE_Midi_TimeSignature_4.setAutoExclusive(True)
        if(self.SE_Midi_Length_Measures.isChecked()):
            self.SE_Midi_Length_Measures.setAutoExclusive(False)
            self.SE_Midi_Length_Beats.setAutoExclusive(False)
            self.SE_Midi_Length_Measures.setChecked(False)
            self.SE_Midi_Length_Beats.setChecked(True)
            self.SE_Midi_Length_Measures.setAutoExclusive(True)
            self.SE_Midi_Length_Beats.setAutoExclusive(True)
        self.SE_Midi_Length_Input.setText(_translate("MainWindow", str(midiInfo[3])))
        brseqInfo = [midiInfo[0],midiInfo[0]]
        brseqLength = [midiInfo[1],midiInfo[1]]
        
def Button_SE_Midi_TimeSignature(self):
    if(self.SE_Midi_Length_Input.text() != "" and  self.SE_Midi_Length_Measures.isChecked()):
        self.SE_Midi_Length_Input.setText(_translate("MainWindow", str(round(int(self.SE_Midi_Length_Input.text())/(3+self.SE_Midi_TimeSignature_4.isChecked())*(4-self.SE_Midi_TimeSignature_4.isChecked())))))

def Button_SE_Midi_Length(self):
    if(self.SE_Midi_Length_Input.text() != ""):
        if(self.SE_Midi_Length_Measures.isChecked()): self.SE_Midi_Length_Input.setText(_translate("MainWindow", str(round(int(self.SE_Midi_Length_Input.text())/(3+self.SE_Midi_TimeSignature_4.isChecked())))))
        else: self.SE_Midi_Length_Input.setText(_translate("MainWindow", str(round(int(self.SE_Midi_Length_Input.text())*(3+self.SE_Midi_TimeSignature_4.isChecked())))))

def List_SE_SongToChange(self):
    UnError(self.SE_SongToChange)
    if(editor.loadedType == LoadType.Carc or editor.loadedType == LoadType.Rom):
        self.SE_ChangeSongText_Name_Input.setText(_translate("MainWindow", editor.textFromTxt[0][self.SE_SongToChange.currentRow()]))
        self.SE_ChangeSongText_Desc_Input.setPlainText(_translate("MainWindow", editor.textFromTxt[1][self.SE_SongToChange.currentRow()]))
        self.SE_ChangeSongText_Genre_Input.setText(_translate("MainWindow", editor.textFromTxt[2][self.SE_SongToChange.currentRow()]))

def Button_SE_Patch(self):
    allow = True
    if(AllowType(LoadType.Brsar) and self.SE_Midi.isChecked()): #Replace Song
        #Check for Error
        if(self.SE_Midi_Tempo_Input.text() == ""):
            allow = False
            Error(self.SE_Midi_Tempo_Input)
        if(self.SE_Midi_Length_Input.text() == ""):
            allow = False
            Error(self.SE_Midi_Length_Input)
        if(extraFile == ""):
            allow = False
            Error(self.SE_Midi_File_Label)
        if(self.SE_SongToChange.currentRow() == -1):
            allow = False
            Error(self.SE_SongToChange)

        if(allow):
            PatchBrsar(self.SE_SongToChange.currentRow(),brseqInfo,brseqLength,self.SE_Midi_Tempo_Input.text(),
            self.SE_Midi_Length_Input.text(),3+self.SE_Midi_TimeSignature_4.isChecked())
    
    if(AllowType(LoadType.Carc)):
        if(self.SE_SongToChange.currentRow() == -1):
            allow = False
            Error(self.SE_SongToChange)
        elif(self.SE_ChangeSongText_Name_Input.text() != editor.textFromTxt[0][self.SE_SongToChange.currentRow()] or
            self.SE_ChangeSongText_Desc_Input.toPlainText() != editor.textFromTxt[1][self.SE_SongToChange.currentRow()] or
            self.SE_ChangeSongText_Genre_Input.text() != editor.textFromTxt[2][self.SE_SongToChange.currentRow()]) and (allow):
                ChangeName(self.SE_SongToChange.currentRow(),[self.SE_ChangeSongText_Name_Input.text(),self.SE_ChangeSongText_Desc_Input.toPlainText(),self.SE_ChangeSongText_Genre_Input.text()])
                extraText = ""
                if(len(editor.textFromTxt[0]) > self.SE_SongToChange.currentRow()) and AllowType(LoadType.Carc) and (Songs[self.SE_SongToChange.currentRow()].SongType != SongTypeValue.Regular or editor.textFromTxt[0][self.SE_SongToChange.currentRow()] != Songs[self.SE_SongToChange.currentRow()].Name) and (Songs[self.SE_SongToChange.currentRow()].SongType != SongTypeValue.Maestro or editor.textFromTxt[0][self.SE_SongToChange.currentRow()] != Songs[self.SE_SongToChange.currentRow()].Name[0:len(Songs[self.SE_SongToChange.currentRow()].Name)-14:1]) and (Songs[self.SE_SongToChange.currentRow()].SongType != SongTypeValue.Handbell or editor.textFromTxt[0][self.SE_SongToChange.currentRow()] != Songs[self.SE_SongToChange.currentRow()].Name[0:len(Songs[self.SE_SongToChange.currentRow()].Name)-19:1]) and (Songs[self.SE_SongToChange.currentRow()].SongType != SongTypeValue.Menu): extraText = " ("+editor.textFromTxt[0][self.SE_SongToChange.currentRow()]+")"
                self.SE_SongToChange.item(self.SE_SongToChange.currentRow()).setText(_translate("MainWindow", Songs[self.SE_SongToChange.currentRow()].Name)+extraText)

#Load Places
class TAB:
    MainMenu = 0
    SongEditor = 1
    StyleEditor = 2

def GotoMainMenu(self):
    self.MainWidget.setCurrentIndex(TAB.MainMenu)

def LoadSongEditor(self):
    self.MainWidget.setCurrentIndex(TAB.SongEditor)
    PrepareFile()
    LoadSongs(self.SE_SongToChange)

def MenuBar_CheckForUpdates(self):
    updater = UpdateWindow(self,False)

#Main Window
class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        global defaultStyle
        super().__init__(parent)
        self.setupUi(self)
        defaultStyle=self.styleSheet()

        #Menu Bar Buttons
        self.MB_LoadFile.triggered.connect(lambda: MenuBar_Load_Rom(self))
        self.MB_CheckForUpdates.triggered.connect(lambda: MenuBar_CheckForUpdates(self))

        #Main Menu Buttons
        self.MP_SongEditor_Button.clicked.connect(lambda: LoadSongEditor(self))

        #Song Editor Buttons    
        self.SE_Midi_File_Button.clicked.connect(lambda: Button_SE_SongToChange(self))
        self.SE_Midi_TimeSignature_4.toggled.connect(lambda: Button_SE_Midi_TimeSignature(self))
        self.SE_Midi_Length_Measures.toggled.connect(lambda: Button_SE_Midi_Length(self))
        self.SE_SongToChange.itemSelectionChanged.connect(lambda: List_SE_SongToChange(self))
        self.SE_Midi_Tempo_Input.textChanged.connect(lambda: UnError(self.SE_Midi_Tempo_Input))
        self.SE_Midi_Length_Input.textChanged.connect(lambda: UnError(self.SE_Midi_Length_Input))
        self.SE_Patch.clicked.connect(lambda: Button_SE_Patch(self))
        self.SE_Back_Button.clicked.connect(lambda: GotoMainMenu(self))

if __name__ == "__main__":
    app = QApplication([])
    win = Window()
    win.show()
    #version = CheckForUpdate()
    #if(version != "null"): updater = UpdateWindow(win,version)
    sys.exit(app.exec())