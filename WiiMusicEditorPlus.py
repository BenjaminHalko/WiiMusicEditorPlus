import os
import subprocess
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QMainWindow

from main_window_ui import Ui_MainWindow 

import editor
from editor import ChangeName, Instruments, ProgramPath, Songs, StyleTypeValue, Styles, currentSystem, SongTypeValue, LoadType, SaveSetting, LoadSetting, PrepareFile, LoadMidi, PatchBrsar, GetStyles, AddPatch
from update import UpdateWindow, CheckForUpdate
from errorhandler import ShowError
from settings import SettingsWindow



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
    return (editor.file.type == LoadType.Rom or editor.file.type == type)

def LoadMainFile(filter):
    global extraFile
    global lastFileDirectory
    file = QtWidgets.QFileDialog()
    if(filter == ""): file.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
    else: file.setFileMode(QtWidgets.QFileDialog.AnyFile)
    file.setNameFilter(filter)
    file.setViewMode(QtWidgets.QFileDialog.Detail)
    file.setDirectory(lastFileDirectory)
    if file.exec_():
        path = file.selectedFiles()[0]
        if(filter == "" and (not os.path.exists(path+"/files") or not os.path.exists(path+"/sys"))): path = path+"/DATA"
        if(filter == "" and (not os.path.exists(path+"/files") or not os.path.exists(path+"/sys"))):
            ShowError("Not a valid Wii Music folder","Files and sys folder not found")
            return False
        editor.file.path = path
        if(filter == ""): lastFileDirectory = editor.file.path[0:len(editor.file.path)-len(os.path.basename(editor.file.path))-1:1]
        else: lastFileDirectory = os.path.dirname(editor.file.path)
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

#Lists
def LoadSongs(widgetID):
    widgetID.clear()
    for i in range(len(Songs)):
        item = QtWidgets.QListWidgetItem()
        extraText = ""
        if(AllowType(LoadType.Carc) and len(editor.textFromTxt[0]) > i) and (Songs[i].SongType != SongTypeValue.Regular or editor.textFromTxt[0][i] != Songs[i].Name) and (Songs[i].SongType != SongTypeValue.Maestro or editor.textFromTxt[0][i] != Songs[i].Name[0:len(Songs[i].Name)-14:1]) and (Songs[i].SongType != SongTypeValue.Handbell or editor.textFromTxt[0][i] != Songs[i].Name[0:len(Songs[i].Name)-19:1]) and (Songs[i].SongType != SongTypeValue.Menu): extraText = " ("+editor.textFromTxt[0][i]+")"
        item.setText(_translate("MainWindow", Songs[i].Name)+extraText)
        widgetID.addItem(item)

def LoadStyles(widgetID):
    widgetID.clear()
    for i in range(len(Styles)):
        item = QtWidgets.QListWidgetItem()
        extraText = ""
        if(AllowType(LoadType.Gct) and editor.loadedStyles[i] != Styles[i].DefaultStyle): extraText = " [Replaced]" 
        item.setText(_translate("MainWindow", Styles[i].Name+extraText))
        widgetID.addItem(item)

def LoadInstruments(widgetID,percussion,menu):
    widgetID.clear()
    if(menu and editor.unsafeMode): menu = False
    if(editor.unsafeMode or percussion == -1): array = range(0,len(Instruments)-1)
    if(percussion == False): array = range(0,40)
    elif(percussion == True ): array = range(40,len(Instruments)-1)
    for i in array:
        item = QtWidgets.QListWidgetItem()
        item.setText(_translate("MainWindow", Instruments[i].Name))
        if(menu and not Instruments[i].InMenu): item.setFlags(QtCore.Qt.ItemIsSelectable)
        widgetID.addItem(item)
    item = QtWidgets.QListWidgetItem()
    item.setText(_translate("MainWindow", Instruments[len(Instruments)-1].Name))
    if(menu): item.setFlags(QtCore.Qt.ItemIsSelectable)
    widgetID.addItem(item)

#Load Places
class TAB:
    MainMenu = 0
    SongEditor = 1
    StyleEditor = 2

#Main Window
class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        global defaultStyle
        super().__init__(parent)
        self.setupUi(self)
        defaultStyle=self.styleSheet()

        if(editor.file.path != ""):
            if(editor.file.type == LoadType.Rom): self.MP_LoadedFile_Label.setText(_translate("MainWindow",'Currently Loaded Folder:'))
            self.MP_LoadedFile_Path.setText(_translate("MainWindow",editor.file.path))
        self.menuBar().setNativeMenuBar(False)

        #Menu Bar Buttons
        self.MB_LoadFile.triggered.connect(self.MenuBar_Load_Rom)
        self.MB_LoadFolder.triggered.connect(self.MenuBar_Load_RomFolder)
        self.MB_Settings.triggered.connect(self.MenuBar_Load_Settings)
        self.MB_Updates.triggered.connect(self.MenuBar_CheckForUpdates)
        self.MB_Dolphin.triggered.connect(lambda: self.LoadDolphin(False))
        self.MB_DolphinMenu.triggered.connect(lambda: self.LoadDolphin(True))

        #Main Menu Buttons
        self.MP_SongEditor_Button.clicked.connect(self.LoadSongEditor)
        self.MP_StyleEditor_Button.clicked.connect(self.LoadStyleEditor)

        #Song Editor Buttons    
        self.SE_Midi_File_Button.clicked.connect(self.Button_SE_SongToChange)
        self.SE_Midi_TimeSignature_4.toggled.connect(self.Button_SE_Midi_TimeSignature)
        self.SE_Midi_Length_Measures.toggled.connect(self.Button_SE_Midi_Length)
        self.SE_SongToChange.itemSelectionChanged.connect(self.List_SE_SongToChange)
        self.SE_Midi_Tempo_Input.textChanged.connect(lambda: UnError(self.SE_Midi_Tempo_Input))
        self.SE_Midi_Length_Input.textChanged.connect(lambda: UnError(self.SE_Midi_Length_Input))
        self.SE_Patch.clicked.connect(self.Button_SE_Patch)
        self.SE_Back_Button.clicked.connect(self.GotoMainMenu)

        #Style Editor Buttons
        self.StE_Back_Button.clicked.connect(self.GotoMainMenu)
        self.StE_PartSelector.currentIndexChanged.connect(self.Button_StE_PartSelector)
        self.StE_InstrumentList.itemSelectionChanged.connect(self.List_StE_InstrumentList)
        self.StE_StyleList.itemSelectionChanged.connect(self.List_StE_StyleList)
        self.StE_ResetStyle.clicked.connect(self.Button_StE_ResetStyle)
        self.StE_Patch.clicked.connect(self.Button_StE_Patch)

    def GotoMainMenu(self):
        self.MainWidget.setCurrentIndex(TAB.MainMenu)

    def LoadSongEditor(self):
        if(editor.file.type == LoadType.Rom or editor.file.type == LoadType.Brsar or editor.file.type == LoadType.Carc):
            self.MainWidget.setCurrentIndex(TAB.SongEditor)
            LoadSongs(self.SE_SongToChange)
            self.SE_Midi.setEnabled(editor.file.type != LoadType.Carc)
            self.SE_Midi.setCheckable(editor.file.type == LoadType.Rom)
            self.SE_ChangeSongText.setEnabled(editor.file.type != LoadType.Brsar)
        else:
            ShowError("Unable to load song editor","Must load Wii Music Rom, Brsar, or Message File")

    def LoadStyleEditor(self):
        self.MainWidget.setCurrentIndex(TAB.StyleEditor)
        GetStyles()
        LoadStyles(self.StE_StyleList)
        LoadInstruments(self.StE_InstrumentList,False,False)
        self.StE_Instruments.setEnabled(False)
        self.StE_ChangeStyleName.setEnabled(False)
        self.StE_ChangeStyleName_Label.setEnabled(False)
        self.StE_ResetStyle.setEnabled(False)
        self.StE_Patch.setEnabled(False)
        self.styleSelected = []
        
    def MenuBar_CheckForUpdates(self):
        updater = UpdateWindow(self,False)

    def LoadDolphin(self,menu):
        if(editor.file.type != LoadType.Rom):
            ShowError("Unable to launch Dolphin","Loaded file must be a complete rom")
        elif(editor.dolphinPath == ""):
            ShowError("Unable to launch Dolphin","Dolphin path not specified\nGo to settings to add a Dolphin path")
        else:
            try:
                if(menu): loadMenu = ""
                else: loadMenu = "-b "
                subprocess.Popen('"'+editor.dolphinPath+'" '+loadMenu+'-e "'+editor.file.path+'/sys/main.dol"')
            except:
                ShowError("Unable to launch Dolphin","Check the Dolphin path in the settings")

    #Menu Bar Buttons
    def MenuBar_Load_Settings():
        SettingsWindow()

    def MenuBar_Load_Rom(self):
        if(LoadMainFile("""All supported files (*.wbfs *.iso *.brsar *.carc *.dol *midi *.mid *.brseq *.rseq *.gct *.txt)
        Wii Music Rom (*.wbfs *.iso)
        Sound Archive (*.brsar)
        Text File (*.carc)
        Main.dol (*.dol)
        Midi-Type File (*.midi *.mid *.brseq *.rseq)
        Geckocode (*.gct *.txt)""")):
            PrepareFile()
            SaveSetting("Paths","CurrentLoadedFile",editor.file.path)
            self.MP_LoadedFile_Path.setText(_translate("MainWindow", editor.file.path))
            self.MP_LoadedFile_Label.setText(_translate("MainWindow",'Currently Loaded File:'))

    def MenuBar_Load_RomFolder(self):
        LoadMainFile("")
        PrepareFile()
        SaveSetting("Paths","CurrentLoadedFile",editor.file.path)
        self.MP_LoadedFile_Path.setText(_translate("MainWindow", editor.file.path))
        self.MP_LoadedFile_Label.setText(_translate("MainWindow",'Currently Loaded Folder:'))   

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
        if(editor.file.type == LoadType.Carc or editor.file.type == LoadType.Rom):
            self.SE_ChangeSongText_Name_Input.setText(_translate("MainWindow", editor.textFromTxt[0][self.SE_SongToChange.currentRow()]))
            self.SE_ChangeSongText_Desc_Input.setPlainText(_translate("MainWindow", editor.textFromTxt[1][self.SE_SongToChange.currentRow()]))
            self.SE_ChangeSongText_Genre_Input.setText(_translate("MainWindow", editor.textFromTxt[2][self.SE_SongToChange.currentRow()]))

    def Button_SE_Patch(self):
        allow = True
        if(self.SE_Midi.isEnabled() and self.SE_Midi.isChecked()): #Replace Song
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
                PatchBrsar(self.SE_SongToChange.currentRow(),brseqInfo,brseqLength,int(self.SE_Midi_Tempo_Input.text()),
                int(self.SE_Midi_Length_Input.text()),3+self.SE_Midi_TimeSignature_4.isChecked())
        
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

    #Style Editor Buttons
    def Button_StE_PartSelector(self):
        self.StE_InstrumentList.setCurrentRow(-1)
        LoadInstruments(self.StE_InstrumentList,(self.StE_PartSelector.currentIndex() == 4 or self.StE_PartSelector.currentIndex() == 5),Styles[self.StE_StyleList.currentRow()].StyleType == StyleTypeValue.Menu)
        if(editor.unsafeMode): toHighlight = editor.loadedStyles[self.StE_StyleList.currentRow()][self.StE_PartSelector.currentIndex()]
        elif(self.StE_PartSelector.currentIndex() == 4 or self.StE_PartSelector.currentIndex() == 5):
            toHighlight = editor.loadedStyles[self.StE_StyleList.currentRow()][self.StE_PartSelector.currentIndex()]-40
        else:
            toHighlight = editor.loadedStyles[self.StE_StyleList.currentRow()][self.StE_PartSelector.currentIndex()]
            if(toHighlight == len(Instruments)-1): toHighlight = 40
        self.StE_InstrumentList.setCurrentRow(toHighlight)

    def List_StE_InstrumentList(self):
        if(self.StE_InstrumentList.currentRow() != -1):
            if(editor.unsafeMode): songSelected = self.StE_InstrumentList.currentRow()
            elif(self.StE_PartSelector.currentIndex() == 4 or self.StE_PartSelector.currentIndex() == 5):
                songSelected = self.StE_InstrumentList.currentRow()+40
            else:
                songSelected = self.StE_InstrumentList.currentRow()
                if(songSelected == 40): songSelected = len(Instruments)-1
            self.styleSelected[self.StE_PartSelector.currentIndex()] = songSelected
            self.StE_Patch.setEnabled(self.styleSelected != editor.loadedStyles[self.StE_StyleList.currentRow()])
            if(self.StE_PartSelector.currentIndex() == 0): self.StE_Part_Melody_Instrument.setText(_translate("MainWindow",Instruments[songSelected].Name))
            elif(self.StE_PartSelector.currentIndex() == 1): self.StE_Part_Harmony_Instrument.setText(_translate("MainWindow",Instruments[songSelected].Name))
            elif(self.StE_PartSelector.currentIndex() == 2): self.StE_Part_Chords_Instrument.setText(_translate("MainWindow",Instruments[songSelected].Name))
            elif(self.StE_PartSelector.currentIndex() == 3): self.StE_Part_Bass_Instrument.setText(_translate("MainWindow",Instruments[songSelected].Name))
            elif(self.StE_PartSelector.currentIndex() == 4): self.StE_Part_Percussion1_Instrument.setText(_translate("MainWindow",Instruments[songSelected].Name))
            elif(self.StE_PartSelector.currentIndex() == 5): self.StE_Part_Percussion2_Instrument.setText(_translate("MainWindow",Instruments[songSelected].Name))
            self.StE_ResetStyle.setEnabled(self.styleSelected != Styles[self.StE_StyleList.currentRow()].DefaultStyle)
    
    def List_StE_StyleList(self):
        self.StE_Instruments.setEnabled(True)
        self.StE_Patch.setEnabled(False)
        if(AllowType(LoadType.Carc) and (Styles[self.StE_StyleList.currentRow()].StyleType == StyleTypeValue.Global)):
            self.StE_ChangeStyleName.setEnabled(True)
            self.StE_ChangeStyleName_Label.setEnabled(True)
            self.StE_ChangeStyleName.setText(_translate("MainWindow",editor.textFromTxt[3][self.StE_StyleList.currentRow()]))
        else:
            self.StE_ChangeStyleName.setEnabled(False)
            self.StE_ChangeStyleName_Label.setEnabled(False)
            self.StE_ChangeStyleName.setText(_translate("MainWindow",""))
        self.styleSelected = editor.loadedStyles[self.StE_StyleList.currentRow()].copy()
        self.StE_InstrumentList.setCurrentRow(-1)
        LoadInstruments(self.StE_InstrumentList,(self.StE_PartSelector.currentIndex() == 4 or self.StE_PartSelector.currentIndex() == 5),Styles[self.StE_StyleList.currentRow()].StyleType == StyleTypeValue.Menu)
        if(editor.unsafeMode): toHighlight = editor.loadedStyles[self.StE_StyleList.currentRow()][self.StE_PartSelector.currentIndex()]
        elif(self.StE_PartSelector.currentIndex() == 4 or self.StE_PartSelector.currentIndex() == 5):
            toHighlight = editor.loadedStyles[self.StE_StyleList.currentRow()][self.StE_PartSelector.currentIndex()]-40
        else:
            toHighlight = editor.loadedStyles[self.StE_StyleList.currentRow()][self.StE_PartSelector.currentIndex()]
            if(toHighlight == len(Instruments)-1): toHighlight = 40
        self.StE_ResetStyle.setEnabled(self.styleSelected != Styles[self.StE_StyleList.currentRow()].DefaultStyle)
        self.StE_InstrumentList.setCurrentRow(toHighlight)
        self.StE_Part_Melody_Instrument.setText(_translate("MainWindow",Instruments[editor.loadedStyles[self.StE_StyleList.currentRow()][0]].Name))
        self.StE_Part_Harmony_Instrument.setText(_translate("MainWindow",Instruments[editor.loadedStyles[self.StE_StyleList.currentRow()][1]].Name))
        self.StE_Part_Chords_Instrument.setText(_translate("MainWindow",Instruments[editor.loadedStyles[self.StE_StyleList.currentRow()][2]].Name))
        self.StE_Part_Bass_Instrument.setText(_translate("MainWindow",Instruments[editor.loadedStyles[self.StE_StyleList.currentRow()][3]].Name))
        self.StE_Part_Percussion1_Instrument.setText(_translate("MainWindow",Instruments[editor.loadedStyles[self.StE_StyleList.currentRow()][4]].Name))
        self.StE_Part_Percussion2_Instrument.setText(_translate("MainWindow",Instruments[editor.loadedStyles[self.StE_StyleList.currentRow()][5]].Name))

    def Button_StE_ResetStyle(self):
        self.styleSelected = Styles[self.StE_StyleList.currentRow()].DefaultStyle.copy()
        self.StE_ResetStyle.setEnabled(False)
        self.StE_Patch.setEnabled((self.styleSelected != editor.loadedStyles[self.StE_StyleList.currentRow()]))
        self.StE_Part_Melody_Instrument.setText(_translate("MainWindow",Instruments[self.styleSelected[0]].Name))
        self.StE_Part_Harmony_Instrument.setText(_translate("MainWindow",Instruments[self.styleSelected[1]].Name))
        self.StE_Part_Chords_Instrument.setText(_translate("MainWindow",Instruments[self.styleSelected[2]].Name))
        self.StE_Part_Bass_Instrument.setText(_translate("MainWindow",Instruments[self.styleSelected[3]].Name))
        self.StE_Part_Percussion1_Instrument.setText(_translate("MainWindow",Instruments[self.styleSelected[4]].Name))
        self.StE_Part_Percussion2_Instrument.setText(_translate("MainWindow",Instruments[self.styleSelected[5]].Name))
        if(editor.unsafeMode): toHighlight = self.styleSelected[self.StE_PartSelector.currentIndex()]
        elif(self.StE_PartSelector.currentIndex() == 4 or self.StE_PartSelector.currentIndex() == 5):
            toHighlight = self.styleSelected[self.StE_PartSelector.currentIndex()]-40
        else:
            toHighlight = self.styleSelected[self.StE_PartSelector.currentIndex()]
            if(toHighlight == len(Instruments)-1): toHighlight = 40
        self.StE_InstrumentList.setCurrentRow(toHighlight)

    def Button_StE_Patch(self):
        if(self.StE_Instruments.isEnabled()):
            patchInfo = Styles[self.StE_StyleList.currentRow()].MemOffset+" 00000018"
            for i in range(3):
                if(self.styleSelected[i*2] == len(Instruments)-1): num1 = "ffffffff"
                else: num1 = format(self.styleSelected[i*2],"x")
                if(self.styleSelected[i*2+1] == len(Instruments)-1): num2 = "ffffffff"
                else: num2 = format(self.styleSelected[i*2+1],"x")
                patchInfo = patchInfo+"\n"+"0"*(8-len(num1))+num1+" "+"0"*(8-len(num2))+num2

            AddPatch(Styles[self.StE_StyleList.currentRow()].Name,patchInfo)

if __name__ == "__main__":
    app = QApplication([])
    win = Window()
    win.show()
    if(editor.file.path == "" and LoadSetting("Paths","CurrentLoadedFile","") != ""): ShowError("Could not load file","One or more errors have occurred")
    if(LoadSetting("Settings","AutoUpdate",True)):
        version = CheckForUpdate()
        if(version != "null"): updater = UpdateWindow(win,version)
    app.exec()