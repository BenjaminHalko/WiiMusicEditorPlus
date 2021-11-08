import os
import subprocess
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow

from main_window_ui import Ui_MainWindow 

import editor
from editor import ChangeName, DecodeTxt, EncodeTxt, GetMessagePath, GivePermission, Instruments, currentSystem, ProgramPath, Songs, StyleTypeValue, Styles, gameIds, regionNames, SongTypeValue, LoadType, SaveSetting, LoadSetting, PrepareFile, LoadMidi, PatchBrsar, GetStyles, AddPatch, ChooseFromOS
from update import UpdateWindow, CheckForUpdate
from errorhandler import ShowError
from settings import SettingsWindow
from riivolution import RiivolutionWindow

_translate = QtCore.QCoreApplication.translate
defaultStyle = ""

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
        if(AllowType(LoadType.Gct) and editor.loadedStyles[i] != Styles[i].DefaultStyle): extraText = " ~[Replaced]~" 
        item.setText(_translate("MainWindow", Styles[i].Name+extraText))
        widgetID.addItem(item)

def LoadInstruments(widgetID,percussion,menu):
    widgetID.clear()
    if(percussion == False): array = range(0,40)
    elif(percussion == True ): array = range(40,len(Instruments)-1)
    normal = array
    if(editor.unsafeMode or percussion == -1): array = range(0,len(Instruments)-1)
    for i in array:
        item = QtWidgets.QListWidgetItem()
        item.setText(_translate("MainWindow", Instruments[i].Name))
        if(menu and not Instruments[i].InMenu):
            if(editor.unsafeMode): item.setForeground(QColor("#cf1800"))
            else: item.setFlags(QtCore.Qt.ItemIsSelectable)
        if(i not in normal): item.setForeground(QColor("#cf1800"))
        widgetID.addItem(item)
    item = QtWidgets.QListWidgetItem()
    item.setText(_translate("MainWindow", Instruments[len(Instruments)-1].Name))
    if(menu):
        if(editor.unsafeMode): item.setForeground(QColor("#cf1800"))
        else: item.setFlags(QtCore.Qt.ItemIsSelectable)
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
        self.externalEditorOpen = False

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
        self.MP_EditText_Button.clicked.connect(self.LoadTextEditor)
        self.MP_Riivolution_Button.clicked.connect(self.CreateRiivolutionPatch)

        #Song Editor Buttons    
        self.SE_Midi_File_Button.clicked.connect(self.Button_SE_SongToChange)
        self.SE_Midi_TimeSignature_4.toggled.connect(self.Button_SE_Midi_TimeSignature)
        self.SE_Midi_Length_Measures.toggled.connect(self.Button_SE_Midi_Length)
        self.SE_SongToChange.itemSelectionChanged.connect(self.List_SE_SongToChange)
        self.SE_Midi_Tempo_Input.valueChanged.connect(self.SE_Patchable)
        self.SE_Midi_Length_Input.valueChanged.connect(self.SE_Patchable)
        self.SE_Patch.clicked.connect(self.Button_SE_Patch)
        self.SE_Back_Button.clicked.connect(self.GotoMainMenu)
        self.SE_ChangeSongText_Name_Input.textEdited.connect(self.SE_Patchable)
        self.SE_ChangeSongText_Desc_Input.textChanged.connect(self.SE_Patchable)
        self.SE_ChangeSongText_Genre_Input.textEdited.connect(self.SE_Patchable)
        self.SE_Midi.toggled.connect(self.SE_Patchable)

        #Style Editor Buttons
        self.StE_Back_Button.clicked.connect(self.GotoMainMenu)
        self.StE_PartSelector.currentIndexChanged.connect(self.Button_StE_PartSelector)
        self.StE_InstrumentList.itemSelectionChanged.connect(self.List_StE_InstrumentList)
        self.StE_StyleList.itemSelectionChanged.connect(self.List_StE_StyleList)
        self.StE_ResetStyle.clicked.connect(self.Button_StE_ResetStyle)
        self.StE_Patch.clicked.connect(self.Button_StE_Patch)

        #Text Editor Buttons
        self.TE_Back_Button.clicked.connect(self.GotoMainMenu)
        self.TE_Patch.clicked.connect(self.Button_TE_Patch)
        self.TE_OpenExternal.clicked.connect(self.Button_TE_ExternalEditor)

    def LoadExtraFile(self,filter):
        global lastExtraFileDirectory
        file = QtWidgets.QFileDialog() 
        file.setFileMode(QtWidgets.QFileDialog.AnyFile)
        file.setNameFilter(filter)
        file.setViewMode(QtWidgets.QFileDialog.Detail)
        file.setDirectory(lastExtraFileDirectory)
        if file.exec_():
            self.extraFile = file.selectedFiles()[0]
            lastExtraFileDirectory = os.path.dirname(self.extraFile)
            SaveSetting("Paths","LastExtraLoadedPath",lastExtraFileDirectory)
            return True
        return False

    def CreateGeckoCode(self):
        global lastFileDirectory
        file = QtWidgets.QFileDialog() 
        file.setFileMode(QtWidgets.QFileDialog.AnyFile)
        file.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        file.setNameFilter("Geckocodes (*.ini)")
        file.setViewMode(QtWidgets.QFileDialog.Detail)
        file.setDirectory(lastFileDirectory)
        if file.exec_():
            editor.file.path = file.selectedFiles()[0]
            lastFileDirectory = os.path.dirname(editor.file.path)
            SaveSetting("Paths","LastLoadedPath",lastFileDirectory)
            openfile = open(editor.file.path,"w")
            openfile.write("")
            openfile.close()
            PrepareFile()
            SaveSetting("Paths","CurrentLoadedFile",editor.file.path)
            self.MP_LoadedFile_Path.setText(_translate("MainWindow", editor.file.path))
            self.MP_LoadedFile_Label.setText(_translate("MainWindow",'Currently Loaded File:'))
            return True
        return False

    #############Load Places

    def GotoMainMenu(self):
        self.MainWidget.setCurrentIndex(TAB.MainMenu)

    def LoadSongEditor(self):
        if(editor.file.type == LoadType.Rom or editor.file.type == LoadType.Brsar or editor.file.type == LoadType.Carc):
            self.MainWidget.setCurrentIndex(TAB.SongEditor)
            self.extraFile = ""
            LoadSongs(self.SE_SongToChange)
            self.SE_Midi.setEnabled(False)
            self.SE_Midi.setCheckable(False)
            self.SE_ChangeSongText.setEnabled(False)
            self.SE_Patch.setEnabled(False)
        else:
            ShowError("Unable to load song editor","Must load Wii Music Rom, Brsar, or Message File")

    def LoadStyleEditor(self):
        if(editor.file.type == LoadType.Rom or editor.file.type == LoadType.Gct or editor.file.type == LoadType.Carc):
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
        else:
            error = ShowError("Unable to load style editor","Must load Wii Music Rom, Message File, or Geckocode",True)
            if(error.clicked):
                if(self.CreateGeckoCode()): self.LoadStyleEditor()

    def LoadTextEditor(self):
        if(AllowType(LoadType.Carc)):
            DecodeTxt()
            file = open(GetMessagePath()+"/message.d/new_music_message.txt","r+b")
            textlines = file.readlines()
            originalTextlines = textlines.copy()
            for num in range(len(textlines)):
                if(textlines[num] == b'  b200 @015f /\r\n'):
                    textlines[num] = b'  b200 @015f [/,4b] = Default\r\n'
                    textlines[num+1] = b'  b201 @0160 [/,4b] = Rock\r\n'
                    textlines[num+2] = b'  b202 @0161 [/,4b] = March\r\n'
                    textlines[num+3] = b'  b203 @0162 [/,4b] = Jazz\r\n'
                    textlines[num+4] = b'  b204 @0163 [/,4b] = Latin\r\n'
                    textlines[num+5] = b'  b205 @0164 [/,4b] = Reggae\r\n'
                    textlines[num+6] = b'  b206 @0165 [/,4b] = Hawaiian\r\n'
                    textlines[num+7] = b'  b207 @0166 [/,4b] = Electronic\r\n'
                    textlines[num+8] = b'  b208 @0167 [/,4b] = Classical\r\n'
                    textlines[num+9] = b'  b209 @0168 [/,4b] = Tango\r\n'
                    textlines[num+10] = b'  b20a @0169 [/,4b] = Pop\r\n'
                    textlines[num+11] = b'  b20b @016a [/,4b] = Japanese\r\n'
                    break
            if(textlines != originalTextlines): file.writelines(textlines)
            file.close()
            file = open(GetMessagePath()+"/message.d/new_music_message.txt","rb")
            self.TE_Text.setPlainText(_translate("MainWindow",file.read().decode("utf-8")))
            file.close()
            self.MainWidget.setCurrentIndex(3)
        else:
            ShowError("Unable to load text editor","Must load Wii Music Rom or Message File")

    def CreateRiivolutionPatch(self):
        if(editor.file.type == LoadType.Rom):
            RiivolutionWindow()
        else:
            ShowError("Unable to create Riivolution patch","Must load Wii Music Rom")
    
    #############Menu Bar

    def MenuBar_CheckForUpdates(self):
        UpdateWindow(self,False)

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

    #############Menu Bar Buttons
    def MenuBar_Load_Settings(self):
        SettingsWindow(self)

    def MenuBar_Load_Rom(self):
        if(LoadMainFile("""All supported files (*.wbfs *.iso *.brsar *.carc *.dol *midi *.mid *.brseq *.rseq *.gct *.ini)
        Wii Music Rom (*.wbfs *.iso)
        Sound Archive (*.brsar)
        Text File (*.carc)
        Main.dol (*.dol)
        Midi-Type File (*.midi *.mid *.brseq *.rseq)
        Geckocode (*.gct *.ini)""")):
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

    #############Song Editor Buttons
    def SE_Patchable(self):
        allow = True
        if(self.SE_Midi.isEnabled() and self.SE_Midi.isChecked()):
            if(self.extraFile == ""): allow = False
        else:
            if(self.SE_ChangeSongText_Name_Input.text() == editor.textFromTxt[0][self.SE_SongToChange.currentRow()] and
                self.SE_ChangeSongText_Desc_Input.toPlainText() == editor.textFromTxt[1][self.SE_SongToChange.currentRow()] and
                self.SE_ChangeSongText_Genre_Input.text() == editor.textFromTxt[2][self.SE_SongToChange.currentRow()]): allow = False
        self.SE_Patch.setEnabled(allow)

    def Button_SE_SongToChange(self):
        global brseqInfo
        global brseqLength
        if(self.LoadExtraFile("Midi-Type File (*.midi *.mid *.brseq *.rseq)")):
            midiInfo = LoadMidi(self.extraFile)
            self.SE_Midi_File_Label.setText(_translate("MainWindow", os.path.basename(self.extraFile)))
            self.SE_Midi_Tempo_Input.setValue(midiInfo[2])
            self.SE_Midi_Length_Input.setValue(midiInfo[3])
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
            brseqInfo = [midiInfo[0],midiInfo[0]]
            brseqLength = [midiInfo[1],midiInfo[1]]
            self.SE_Patchable()
            
    def Button_SE_Midi_TimeSignature(self):
        if(self.SE_Midi_Length_Measures.isChecked()):
            self.SE_Midi_Length_Input.setValue(round(int(self.SE_Midi_Length_Input.text())/(3+self.SE_Midi_TimeSignature_4.isChecked())*(4-self.SE_Midi_TimeSignature_4.isChecked())))

    def Button_SE_Midi_Length(self):
        if(self.SE_Midi_Length_Measures.isChecked()): self.SE_Midi_Length_Input.setValue(round(int(self.SE_Midi_Length_Input.text())/(3+self.SE_Midi_TimeSignature_4.isChecked())))
        else: self.SE_Midi_Length_Input.setValue(round(int(self.SE_Midi_Length_Input.text())*(3+self.SE_Midi_TimeSignature_4.isChecked())))

    def List_SE_SongToChange(self):
        if(AllowType(LoadType.Brsar)):
            if(not self.SE_Midi.isCheckable()):
                self.SE_Midi.setCheckable(True)
                self.SE_Midi.setEnabled(True)
        if(AllowType(LoadType.Carc)):
            self.SE_ChangeSongText.setEnabled(True)
            self.SE_ChangeSongText_Name_Input.setText(_translate("MainWindow", editor.textFromTxt[0][self.SE_SongToChange.currentRow()]))
            self.SE_ChangeSongText_Desc_Input.setPlainText(_translate("MainWindow", editor.textFromTxt[1][self.SE_SongToChange.currentRow()]))
            self.SE_ChangeSongText_Genre_Input.setText(_translate("MainWindow", editor.textFromTxt[2][self.SE_SongToChange.currentRow()]))
        self.SE_Patchable() 

    def Button_SE_Patch(self):
        if(self.SE_Midi.isEnabled() and self.SE_Midi.isChecked()):
            PatchBrsar(self.SE_SongToChange.currentRow(),brseqInfo,brseqLength,self.SE_Midi_Tempo_Input.value(),
            self.SE_Midi_Length_Input.value(),3+self.SE_Midi_TimeSignature_4.isChecked())
        
        if(AllowType(LoadType.Carc)):
            ChangeName(self.SE_SongToChange.currentRow(),[self.SE_ChangeSongText_Name_Input.text(),self.SE_ChangeSongText_Desc_Input.toPlainText(),self.SE_ChangeSongText_Genre_Input.text()])
            extraText = ""
            if(len(editor.textFromTxt[0]) > self.SE_SongToChange.currentRow()) and AllowType(LoadType.Carc) and (Songs[self.SE_SongToChange.currentRow()].SongType != SongTypeValue.Regular or editor.textFromTxt[0][self.SE_SongToChange.currentRow()] != Songs[self.SE_SongToChange.currentRow()].Name) and (Songs[self.SE_SongToChange.currentRow()].SongType != SongTypeValue.Maestro or editor.textFromTxt[0][self.SE_SongToChange.currentRow()] != Songs[self.SE_SongToChange.currentRow()].Name[0:len(Songs[self.SE_SongToChange.currentRow()].Name)-14:1]) and (Songs[self.SE_SongToChange.currentRow()].SongType != SongTypeValue.Handbell or editor.textFromTxt[0][self.SE_SongToChange.currentRow()] != Songs[self.SE_SongToChange.currentRow()].Name[0:len(Songs[self.SE_SongToChange.currentRow()].Name)-19:1]) and (Songs[self.SE_SongToChange.currentRow()].SongType != SongTypeValue.Menu): extraText = " ("+editor.textFromTxt[0][self.SE_SongToChange.currentRow()]+")"
            self.SE_SongToChange.item(self.SE_SongToChange.currentRow()).setText(_translate("MainWindow", Songs[self.SE_SongToChange.currentRow()].Name)+extraText)
            editor.textFromTxt[0][self.SE_SongToChange.currentRow()] = self.SE_ChangeSongText_Name_Input.text()
            editor.textFromTxt[1][self.SE_SongToChange.currentRow()] = self.SE_ChangeSongText_Desc_Input.toPlainText()
            editor.textFromTxt[2][self.SE_SongToChange.currentRow()] = self.SE_ChangeSongText_Genre_Input.text()
        self.SE_Patch.setEnabled(False)

    #############Style Editor Buttons
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
            editor.loadedStyles[self.StE_StyleList.currentRow()] = self.styleSelected.copy()
            self.StE_Patch.setEnabled(False)
            if(Styles[self.StE_StyleList.currentRow()].DefaultStyle == self.styleSelected):
                self.StE_StyleList.item(self.StE_StyleList.currentRow()).setText(_translate("MainWindow",Styles[self.StE_StyleList.currentRow()].Name))
            else:
                self.StE_StyleList.item(self.StE_StyleList.currentRow()).setText(_translate("MainWindow",Styles[self.StE_StyleList.currentRow()].Name+" ~[Replaced]~"))
            patchInfo = Styles[self.StE_StyleList.currentRow()].MemOffset+" 00000018\n"
            for i in range(3):
                if(self.styleSelected[i*2] == len(Instruments)-1): num1 = "ffffffff"
                else: num1 = format(self.styleSelected[i*2],"x")
                if(self.styleSelected[i*2+1] == len(Instruments)-1): num2 = "ffffffff"
                else: num2 = format(self.styleSelected[i*2+1],"x")
                patchInfo = patchInfo+"0"*(8-len(num1))+num1+" "+"0"*(8-len(num2))+num2+"\n"

            AddPatch(Styles[self.StE_StyleList.currentRow()].Name+" Style Patch",patchInfo)

    #############Text Editor
    def Button_TE_Patch(self):
        file = open(GetMessagePath()+"/message.d/new_music_message.txt","wb")
        file.write(self.TE_Text.toPlainText().encode("utf-8"))
        file.close()
        EncodeTxt()
        self.MainWidget.setCurrentIndex(0)
    
    def Button_TE_ExternalEditor(self):
        self.externalEditorOpen = True
        self.TE_Patch.setEnabled(False)
        self.TE_Text.setEnabled(False)
        self.TE_Back_Button.setEnabled(False)
        self.TE_OpenExternal.setEnabled(False)
        self.edit = ExternalEditor()
        self.edit.done.connect(self.TE_FinishEditor)
        self.edit.start()

    def TE_FinishEditor(self):
        file = open(GetMessagePath()+"/message.d/new_music_message.txt","r+b")
        self.TE_Text.setPlainText(_translate("MainWindow",file.read().decode("utf-8")))
        file.close()
        self.TE_Patch.setEnabled(True)
        self.TE_Text.setEnabled(True)
        self.TE_Back_Button.setEnabled(True)
        self.TE_OpenExternal.setEnabled(True)
        self.edit.deleteLater()


class ExternalEditor(QtCore.QThread):
    done = QtCore.pyqtSignal()
    def run(self):
        GivePermission(GetMessagePath()+'/message.d/new_music_message.txt')
        subprocess.run(ChooseFromOS(["notepad","open -e","xdg-open"])+' "'+GetMessagePath()+'/message.d/new_music_message.txt"',shell=True)
        self.done.emit()

if __name__ == "__main__":
    app = QApplication([])
    win = Window()
    win.show()
    if(editor.file.path == "" and LoadSetting("Paths","CurrentLoadedFile","") != ""): ShowError("Could not load file","One or more errors have occurred")
    if(LoadSetting("Settings","AutoUpdate",True)):
        version = CheckForUpdate()
        if(version != "null"): updater = UpdateWindow(win,version)
    sys.exit(app.exec())