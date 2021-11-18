import os
import pathlib
from shutil import copyfile, rmtree
import subprocess
import sys
import zipfile
import tempfile

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow

from main_window_ui import Ui_MainWindow 

import editor
from editor import ChangeName, GetBrsarPath, GetDefaultStyle, GetGeckoPath, GetMainDolPath, PatchMainDol, CreateGct, DecodeTxt, EncodeTxt, FixMessageFile, Run, GetMessagePath, GivePermission, BasedOnRegion, SaveSetting, LoadSetting, PrepareFile, LoadMidi, PatchBrsar, GetStyles, AddPatch, ChooseFromOS, Instruments, gctRegionOffsets, Songs, Styles, ProgramPath, currentSystem, gameIds, StyleTypeValue, SongTypeValue, LoadType
from update import UpdateWindow, CheckForUpdate
from errorhandler import ShowError
from settings import SettingsWindow
from riivolution import RiivolutionWindow
from success import SuccessWindow
from packrom import PackRomWindow

_translate = QtCore.QCoreApplication.translate
defaultStyle = ""

brseqInfo = 0
brseqLength = 0
lastExtraFileDirectory = LoadSetting("Paths","LastExtraLoadedPath","")
lastFileDirectory = LoadSetting("Paths","LastLoadedPath","")

def AllowType(type):
    return (editor.file.type == LoadType.Rom or editor.file.type == type)

def LoadMainFile(filter):
    global lastFileDirectory
    file = QtWidgets.QFileDialog()
    if(filter == ""): file.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
    else: file.setFileMode(QtWidgets.QFileDialog.AnyFile)
    file.setNameFilter(filter)
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
        

#Load Places
class TAB:
    MainMenu = 0
    SongEditor = 1
    StyleEditor = 2
    TextEditor = 3
    DefaultStyleEditor = 4

#Main Window
class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        global defaultStyle
        super().__init__(parent)
        self.setupUi(self)
        defaultStyle=self.styleSheet()
        self.externalEditorOpen = False
        self.fromSongEditor = -1

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
        self.MP_DefaultStyle_Button.clicked.connect(self.LoadDefaultStyleEditor)
        self.MP_GeckocodeConvert_Button.clicked.connect(self.ConvertGeckocode)
        self.MP_MainDolPatch_Button.clicked.connect(self.PatchMainDolWithGeckoCode)
        self.MP_Riivolution_Button.clicked.connect(self.CreateRiivolutionPatch)

        self.MP_PackRom_Button.clicked.connect(self.PackRom)
        self.MP_ExportFiles_Button.clicked.connect(self.ExportFiles)
        self.MP_ImportFiles_Button.clicked.connect(self.ImportFiles)

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
        self.SE_OpenStyleEditor.clicked.connect(self.Button_SE_OpenStyleEditor)
        self.SE_OpenDefaultStyleEditor.clicked.connect(self.Button_SE_OpenDefaultStyleEditor)

        #Style Editor Buttons
        self.StE_Back_Button.clicked.connect(self.GotoMainMenu)
        self.StE_PartSelector.currentIndexChanged.connect(self.Button_StE_PartSelector)
        self.StE_InstrumentList.itemSelectionChanged.connect(self.List_StE_InstrumentList)
        self.StE_StyleList.itemSelectionChanged.connect(self.List_StE_StyleList)
        self.StE_ResetStyle.clicked.connect(self.Button_StE_ResetStyle)
        self.StE_Patch.clicked.connect(self.Button_StE_Patch)
        self.StE_ChangeStyleName.textEdited.connect(self.StE_Patchable)

        #Text Editor Buttons
        self.TE_Back_Button.clicked.connect(self.GotoMainMenu)
        self.TE_Patch.clicked.connect(self.Button_TE_Patch)
        self.TE_OpenExternal.clicked.connect(self.Button_TE_ExternalEditor)

        #Default Style Editor
        self.DS_Back_Button.clicked.connect(self.GotoMainMenu)
        self.DS_Patch.clicked.connect(self.Button_DS_Patch)
        self.DS_Songs.itemSelectionChanged.connect(self.List_DS_SongList)
        self.DS_Styles.itemSelectionChanged.connect(self.List_DS_StyleList)
        self.DS_Reset.clicked.connect(self.Button_DS_Reset)

    #Lists
    def LoadSongs(self,widgetID,types=[],lockSongs=False):
        widgetID.clear()
        for i in range(len(Songs)):
            if(types == [] or Songs[i].SongType in types):
                item = QtWidgets.QListWidgetItem()
                text = Songs[i].Name
                if(AllowType(LoadType.Carc) and len(editor.textFromTxt[0]) > i) and (Songs[i].SongType != SongTypeValue.Regular or editor.textFromTxt[0][i] != Songs[i].Name) and (Songs[i].SongType != SongTypeValue.Maestro or editor.textFromTxt[0][i] != Songs[i].Name[0:len(Songs[i].Name)-14:1]) and (Songs[i].SongType != SongTypeValue.Handbell or editor.textFromTxt[0][i] != Songs[i].Name[0:len(Songs[i].Name)-19:1]) and (Songs[i].SongType != SongTypeValue.Menu):
                    text = editor.textFromTxt[0][i]
                    if(Songs[i].SongType == SongTypeValue.Maestro): text = text+" (Mii Maestro)"
                    if(Songs[i].SongType == SongTypeValue.Handbell): text = text+" (Handbell Harmony)"
                item.setText(_translate("MainWindow", text))
                if(lockSongs and i != self.fromSongEditor): item.setFlags(QtCore.Qt.ItemIsSelectable)
                widgetID.addItem(item)
        if(lockSongs): widgetID.setCurrentRow(self.fromSongEditor)

    def LoadStyles(self,widgetID,lockSongs=False):
        widgetID.clear()
        for i in range(len(Styles)):
            item = QtWidgets.QListWidgetItem()
            extraText = ""
            if(AllowType(LoadType.Gct) and editor.loadedStyles[i] != Styles[i].DefaultStyle): extraText = " ~[Replaced]~" 
            item.setText(_translate("MainWindow", Styles[i].Name+extraText))
            if(lockSongs and i != self.fromSongEditor): item.setFlags(QtCore.Qt.ItemIsSelectable)
            widgetID.addItem(item)
        if(lockSongs): widgetID.setCurrentRow(self.fromSongEditor)

    def LoadInstruments(self,widgetID,percussion,menu):
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

    def LoadExtraFile(self,filter):
        global lastExtraFileDirectory
        file = QtWidgets.QFileDialog() 
        file.setFileMode(QtWidgets.QFileDialog.AnyFile)
        file.setNameFilter(filter)
        file.setViewMode(QtWidgets.QFileDialog.Detail)
        file.setDirectory(lastExtraFileDirectory)
        if file.exec_() and os.path.isfile(file.selectedFiles()[0]):
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
            if(pathlib.Path(editor.file.path).suffix != ".ini"): editor.file.path = editor.file.path+".ini"
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
        if(self.fromSongEditor != -1):    
            self.MainWidget.setCurrentIndex(TAB.SongEditor)       
            self.fromSongEditor = -1
        else:
            self.MainWidget.setCurrentIndex(TAB.MainMenu)

    def LoadSongEditor(self):
        if(editor.file.type == LoadType.Rom or editor.file.type == LoadType.Brsar or editor.file.type == LoadType.Carc):
            self.MainWidget.setCurrentIndex(TAB.SongEditor)
            self.extraFile = ""
            self.LoadSongs(self.SE_SongToChange)
            self.SE_Midi.setEnabled(False)
            self.SE_Midi.setCheckable(False)
            self.SE_ChangeSongText.setEnabled(False)
            self.SE_Patch.setEnabled(False)
            self.SE_StyleLabel.setEnabled(False)
            self.SE_StyleText.setEnabled(False)
            self.SE_OpenDefaultStyleEditor.setEnabled(False)
            self.SE_OpenStyleEditor.setEnabled(False)
            self.SE_Midi_File_Label.setText(_translate("MainWindow","Load a Midi-Type file"))
            if(not AllowType(LoadType.Brsar)): self.SE_SongToChange.removeItemWidget(self.SE_SongToChange.takeItem(len(Songs)-1))
        else:
            ShowError("Unable to load song editor","Must load Wii Music Rom, Brsar, or Message File")

    def LoadStyleEditor(self):
        if(editor.file.type == LoadType.Rom or editor.file.type == LoadType.Gct or editor.file.type == LoadType.Carc):
            self.MainWidget.setCurrentIndex(TAB.StyleEditor)
            GetStyles()
            self.LoadStyles(self.StE_StyleList,self.fromSongEditor != -1)
            self.LoadInstruments(self.StE_InstrumentList,False,False)
            self.StE_Instruments.setEnabled(False)
            self.StE_ChangeStyleName.setEnabled(False)
            self.StE_ChangeStyleName_Label.setEnabled(False)
            self.StE_ResetStyle.setEnabled(False)
            self.StE_Patch.setEnabled(False)
            self.styleSelected = []
            if(self.fromSongEditor != -1): self.List_StE_StyleList()
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
            textlines = FixMessageFile(textlines)
            if(textlines != originalTextlines): file.writelines(textlines)
            file.close()
            file = open(GetMessagePath()+"/message.d/new_music_message.txt","rb")
            self.TE_Text.setPlainText(_translate("MainWindow",file.read().decode("utf-8")))
            file.close()
            self.MainWidget.setCurrentIndex(TAB.TextEditor)
        else:
            ShowError("Unable to load text editor","Must load Wii Music Rom or Message File")

    def LoadDefaultStyleEditor(self):
        if(AllowType(LoadType.Gct)):
            self.MainWidget.setCurrentIndex(TAB.DefaultStyleEditor)
            GetStyles()
            self.LoadSongs(self.DS_Songs,[SongTypeValue.Regular],self.fromSongEditor != -1)
            self.LoadStyles(self.DS_Styles)
            self.DS_StyleBox.setEnabled(False)
            self.DS_Patch.setEnabled(False)
            if(self.fromSongEditor != -1): self.List_DS_SongList()
        else:
            error = ShowError("Unable to load default style editor","Must load Wii Music Rom or Geckocode",True)
            if(error.clicked):
                if(self.CreateGeckoCode()): self.LoadDefaultStyleEditor()
            
    def ConvertGeckocode(self):
        if(AllowType(LoadType.Gct)):
            file = QFileDialog()
            file.setFileMode(QFileDialog.AnyFile)
            file.setAcceptMode(QFileDialog.AcceptSave)
            file.setNameFilter("Geckocodes (*.gct)")
            file.setDirectory(lastFileDirectory)
            if(file.exec()):
                path = file.selectedFiles()[0]
                if(pathlib.Path(path).suffix != ".gct"): file = file+".gct"
                CreateGct(path)
                SuccessWindow("Creation Complete!")
        else:
            ShowError("Unable to create .gct file","Must load Wii Music Rom or Geckocode")

    def PatchMainDolWithGeckoCode(self):
        if(editor.file.type == LoadType.Rom):
            file = QFileDialog()
            file.setFileMode(QFileDialog.AnyFile)
            file.setNameFilter("Geckocodes (*.ini *.gct)")
            file.setDirectory(os.path.dirname(GetGeckoPath()))
            if(file.exec()):
                PatchMainDol(geckoPath=file.selectedFiles()[0])
                SuccessWindow("Main.dol Patched!")
        elif(editor.file.type == LoadType.Gct or editor.file.type == LoadType.Dol):
            file = QFileDialog()
            file.setFileMode(QFileDialog.AnyFile)
            if(editor.file.type == LoadType.Midi):
                file.setNameFilter("Geckocodes (*.ini *.gct)")
            else:
                file.setNameFilter("Main.dol (*.dol)")
            file.setDirectory(lastExtraFileDirectory)
            if(file.exec()):
                if(editor.file.type == LoadType.Midi):
                    PatchMainDol(geckoPath=file.selectedFiles()[0])
                else:
                    PatchMainDol(dolPath=file.selectedFiles()[0])
                SuccessWindow("Main.dol Patched!")
        else:
            ShowError("Unable to patch Main.dol","Must load Wii Music Rom, Main.dol, or Geckocode")

    def CreateRiivolutionPatch(self):
        if(editor.file.type == LoadType.Rom):
            RiivolutionWindow()
        else:
            ShowError("Unable to create Riivolution patch","Must load Wii Music Rom")

    def RevertChanges(self):
        if(editor.file.type == LoadType.Rom):
            if(os.path.isfile(GetBrsarPath()+".backup")): copyfile(GetBrsarPath()+".backup",GetBrsarPath())
            if(os.path.isfile(GetMessagePath()+"/message.carc.backup")): copyfile(GetMessagePath()+"/message.carc.backup",GetMessagePath()+"/message.carc")
            if(os.path.isfile(GetMainDolPath()+".backup")): copyfile(GetMainDolPath()+".backup",GetMainDolPath())

    def PackRom(self):
        PackRomWindow()

    def ImportFiles(self):
        file = QFileDialog()
        file.setFileMode(QFileDialog.AnyFile)
        file.setNameFilter("""All supported files (*.zip *.brsar *.carc *.dol *.ini)
        Zipfile (*.zip)
        Sound Archive (*.brsar)
        Text File (*.carc)
        Main.dol (*.dol)
        Geckocodes (*.ini)""")
        file.setDirectory(lastFileDirectory)
        if(file.exec()):
            try:
                path = file.selectedFiles()[0]
                if(pathlib.Path(path).suffix == "zip"):
                    os.mkdir(ProgramPath+"/tmp")
                    zipfile.ZipFile(path, 'r').extractall(ProgramPath+"/tmp")
                    files = os.listdir(ProgramPath+"/tmp")
                else:
                    files = [path]
                for newfile in files:
                    if(pathlib.Path(newfile).suffix == ".brsar"): copyfile(newfile,GetBrsarPath())
                    elif(pathlib.Path(newfile).suffix == ".carc"): copyfile(newfile,GetMessagePath()+"/message.carc")
                    elif(pathlib.Path(newfile).suffix == ".dol"): copyfile(newfile,GetMainDolPath())
                    elif(pathlib.Path(newfile).suffix == ".ini"): copyfile(newfile,GetGeckoPath())
                if(pathlib.Path(path).suffix == "zip"):
                    rmtree(ProgramPath+"/tmp")
                SuccessWindow("Files Successfully Imported!")                
            except Exception as e:
                ShowError("Unable to import files",str(e))


    def ExportFiles(self):
        file = QFileDialog()
        file.setFileMode(QFileDialog.AnyFile)
        file.setAcceptMode(QFileDialog.AcceptSave)
        file.setNameFilter("Zipfile (*.zip)")
        file.setDirectory(lastFileDirectory)
        if(file.exec()):
            try:
                path = file.selectedFiles()[0]
                if(pathlib.Path(path).suffix != ".zip"): path = path+".zip"
                zipObj = zipfile.ZipFile(path, 'w')
                zipObj.write(GetBrsarPath(),'rp_Music_sound.brsar')
                zipObj.write(GetMessagePath()+"/message.carc","message.carc")
                zipObj.write(GetMainDolPath(),"main.dol")
                zipObj.write(GetGeckoPath(),"Geckocodes.ini")
                zipObj.close()
                SuccessWindow("Files Exported")
            except Exception as e:
                ShowError("Files not Exported",str(e))

    

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
                cmd = [editor.dolphinPath,'-e',editor.file.path+'/sys/main.dol']
                if(not menu): cmd.insert(1,"-b")
                env = os.environ
                env["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.dirname(editor.dolphinPath)+'/QtPlugins/platforms/'
                GivePermission(editor.dolphinPath)
                subprocess.Popen(cmd,env=env)
            except Exception as e:
                ShowError("Unable to launch Dolphin","Check the Dolphin path in the settings\n"+str(e))

    #############Menu Bar Buttons
    def MenuBar_Load_Settings(self):
        SettingsWindow(self)

    def MenuBar_Load_Rom(self):
        if(LoadMainFile("""All supported files (*.wbfs *.iso *.brsar *.carc *.dol *midi *.mid *.brseq *.rseq *.ini)
        Wii Music Rom (*.wbfs *.iso)
        Sound Archive (*.brsar)
        Text File (*.carc)
        Main.dol (*.dol)
        Midi-Type File (*.midi *.mid *.brseq *.rseq)
        Geckocode (*.ini)""")):
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
        if(self.SE_Midi.isEnabled() and (self.SE_Midi.isChecked() or Songs[self.SE_SongToChange.currentRow()].SongType == SongTypeValue.Menu)):
            if(self.extraFile == ""): allow = False
        elif(Songs[self.SE_SongToChange.currentRow()].SongType != SongTypeValue.Menu):
            if(self.SE_ChangeSongText_Name_Input.text() == editor.textFromTxt[0][self.SE_SongToChange.currentRow()] and
                self.SE_ChangeSongText_Desc_Input.toPlainText() == editor.textFromTxt[1][self.SE_SongToChange.currentRow()] and
                self.SE_ChangeSongText_Genre_Input.text() == editor.textFromTxt[2][self.SE_SongToChange.currentRow()]): allow = False
        self.SE_Patch.setEnabled(allow)

    def Button_SE_SongToChange(self):
        global brseqInfo
        global brseqLength
        if(self.LoadExtraFile("Midi-Type File (*.midi *.mid *.brseq *.rseq)")):
            midiInfo = LoadMidi(self.extraFile)
            if(midiInfo[0] != False):
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
            if(Songs[self.SE_SongToChange.currentRow()].SongType != SongTypeValue.Menu):
                self.SE_ChangeSongText.setEnabled(True)
                self.SE_ChangeSongText_Name_Input.setText(_translate("MainWindow", editor.textFromTxt[0][self.SE_SongToChange.currentRow()]))
                self.SE_ChangeSongText_Desc_Input.setPlainText(_translate("MainWindow", editor.textFromTxt[1][self.SE_SongToChange.currentRow()]))
                self.SE_ChangeSongText_Genre_Input.setText(_translate("MainWindow", editor.textFromTxt[2][self.SE_SongToChange.currentRow()]))
            else:
                self.SE_ChangeSongText.setEnabled(False)
                self.SE_ChangeSongText_Name_Input.setText(_translate("MainWindow", ""))
                self.SE_ChangeSongText_Desc_Input.setPlainText(_translate("MainWindow", ""))
                self.SE_ChangeSongText_Genre_Input.setText(_translate("MainWindow", ""))
                self.SE_Midi.setCheckable(False)
                self.SE_Midi.setEnabled(True)
        if(AllowType(LoadType.Brsar)):
            self.SE_StyleLabel.setEnabled(Songs[self.SE_SongToChange.currentRow()].SongType == SongTypeValue.Regular)
            self.SE_StyleText.setEnabled(Songs[self.SE_SongToChange.currentRow()].SongType == SongTypeValue.Regular)
            self.SE_OpenDefaultStyleEditor.setEnabled(Songs[self.SE_SongToChange.currentRow()].SongType == SongTypeValue.Regular)
            self.SE_OpenStyleEditor.setEnabled(Songs[self.SE_SongToChange.currentRow()].SongType == SongTypeValue.Regular)
            if(Songs[self.SE_SongToChange.currentRow()].SongType != SongTypeValue.Regular): self.SE_StyleText.setText(_translate("MainWindow",""))
            else: self.SE_StyleText.setText(_translate("MainWindow",Styles[GetDefaultStyle(self.SE_SongToChange.currentRow(),False)].Name))
        self.SE_Patchable()

    def Button_SE_Patch(self):
        if(self.SE_Midi.isEnabled() and self.SE_Midi.isChecked()):
            PatchBrsar(self.SE_SongToChange.currentRow(),brseqInfo,brseqLength,self.SE_Midi_Tempo_Input.value(),
            self.SE_Midi_Length_Input.value(),3+self.SE_Midi_TimeSignature_4.isChecked())
        
        if(AllowType(LoadType.Carc)):
            ChangeName(self.SE_SongToChange.currentRow(),[self.SE_ChangeSongText_Name_Input.text(),self.SE_ChangeSongText_Desc_Input.toPlainText(),self.SE_ChangeSongText_Genre_Input.text()])
            text = Songs[self.SE_SongToChange.currentRow()].Name
            if(len(editor.textFromTxt[0]) > self.SE_SongToChange.currentRow()) and AllowType(LoadType.Carc) and (Songs[self.SE_SongToChange.currentRow()].SongType != SongTypeValue.Regular or editor.textFromTxt[0][self.SE_SongToChange.currentRow()] != Songs[self.SE_SongToChange.currentRow()].Name) and (Songs[self.SE_SongToChange.currentRow()].SongType != SongTypeValue.Maestro or editor.textFromTxt[0][self.SE_SongToChange.currentRow()] != Songs[self.SE_SongToChange.currentRow()].Name[0:len(Songs[self.SE_SongToChange.currentRow()].Name)-14:1]) and (Songs[self.SE_SongToChange.currentRow()].SongType != SongTypeValue.Handbell or editor.textFromTxt[0][self.SE_SongToChange.currentRow()] != Songs[self.SE_SongToChange.currentRow()].Name[0:len(Songs[self.SE_SongToChange.currentRow()].Name)-19:1]) and (Songs[self.SE_SongToChange.currentRow()].SongType != SongTypeValue.Menu):
                text = editor.textFromTxt[0][self.SE_SongToChange.currentRow()]
                if(Songs[self.SE_SongToChange.currentRow()].SongType == SongTypeValue.Maestro): text = text+" (Mii Maestro)"
                if(Songs[self.SE_SongToChange.currentRow()].SongType == SongTypeValue.Handbell): text = text+" (Handbell Harmony)"
            self.SE_SongToChange.item(self.SE_SongToChange.currentRow()).setText(_translate("MainWindow", text))
            editor.textFromTxt[0][self.SE_SongToChange.currentRow()] = self.SE_ChangeSongText_Name_Input.text()
            editor.textFromTxt[1][self.SE_SongToChange.currentRow()] = self.SE_ChangeSongText_Desc_Input.toPlainText()
            editor.textFromTxt[2][self.SE_SongToChange.currentRow()] = self.SE_ChangeSongText_Genre_Input.text()
        self.SE_Patch.setEnabled(False)

    def Button_SE_OpenStyleEditor(self):
        self.fromSongEditor = GetDefaultStyle(self.SE_SongToChange.currentRow(),False)
        self.MainWidget.setCurrentIndex(TAB.StyleEditor)
        self.LoadStyleEditor()

    def Button_SE_OpenDefaultStyleEditor(self):
        self.fromSongEditor = self.SE_SongToChange.currentRow()
        self.MainWidget.setCurrentIndex(TAB.DefaultStyleEditor)
        self.LoadDefaultStyleEditor()

    #############Style Editor Buttons
    def StE_Patchable(self):
        self.StE_Patch.setEnabled((self.styleSelected != editor.loadedStyles[self.StE_StyleList.currentRow()]) or (self.StE_ChangeStyleName.isEnabled() and self.StE_ChangeStyleName.text() != editor.textFromTxt[3][self.StE_StyleList.currentRow()]))

    def Button_StE_PartSelector(self):
        self.StE_InstrumentList.setCurrentRow(-1)
        self.LoadInstruments(self.StE_InstrumentList,(self.StE_PartSelector.currentIndex() == 4 or self.StE_PartSelector.currentIndex() == 5),Styles[self.StE_StyleList.currentRow()].StyleType == StyleTypeValue.Menu)
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
            self.StE_Patchable()
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
        self.LoadInstruments(self.StE_InstrumentList,(self.StE_PartSelector.currentIndex() == 4 or self.StE_PartSelector.currentIndex() == 5),Styles[self.StE_StyleList.currentRow()].StyleType == StyleTypeValue.Menu)
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
        self.StE_Patchable()
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
        self.StE_Patch.setEnabled(False)
        if(self.styleSelected != editor.loadedStyles[self.StE_StyleList.currentRow()]):
            editor.loadedStyles[self.StE_StyleList.currentRow()] = self.styleSelected.copy()
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

        if(self.StE_ChangeStyleName.isEnabled() and self.StE_ChangeStyleName.text() != editor.textFromTxt[3][self.StE_StyleList.currentRow()]):
            ChangeName(self.StE_StyleList.currentRow(),self.StE_ChangeStyleName.text())
            editor.textFromTxt[3][self.StE_StyleList.currentRow()] = self.StE_ChangeStyleName.text()

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

    #############Default Style Editor
    def Button_DS_Patch(self):
        AddPatch(Songs[self.DS_Songs.currentRow()].Name+' Default Style Patch','0'+format(Songs[self.DS_Songs.currentRow()].MemOffset+BasedOnRegion(gctRegionOffsets)+42,'x')+' 000000'+Styles[self.DS_Styles.currentRow()].StyleId+'\n')
        self.DS_Patch.setEnabled(False)
        if(self.fromSongEditor != -1): self.SE_StyleText.setText(_translate("MainWindow",Styles[self.DS_Styles.currentRow()].Name))

    def List_DS_SongList(self):
        self.DS_StyleBox.setEnabled(True)
        self.DS_Styles.setCurrentRow(GetDefaultStyle(self.DS_Songs.currentRow(),False))
    
    def List_DS_StyleList(self):
        self.DS_Patch.setEnabled(self.DS_Styles.currentRow() != GetDefaultStyle(self.DS_Songs.currentRow(),False))
        self.DS_Reset.setEnabled(self.DS_Styles.currentRow() != GetDefaultStyle(self.DS_Songs.currentRow(),True))

    def Button_DS_Reset(self):
        self.DS_Styles.setCurrentRow(GetDefaultStyle(self.DS_Songs.currentRow(),True))
        self.DS_Reset.setEnabled(False)

class ExternalEditor(QtCore.QThread):
    done = QtCore.pyqtSignal()
    def run(self):
        GivePermission(GetMessagePath()+'/message.d/new_music_message.txt')
        Run(ChooseFromOS(["notepad","open -e","gedit"])+' "'+GetMessagePath()+'/message.d/new_music_message.txt"')
        self.done.emit()

if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon(ProgramPath+"/Helper/Extra/icon.png"))
    win = Window()
    win.show()
    if(editor.file.path == "" and LoadSetting("Paths","CurrentLoadedFile","") != ""): ShowError("Could not load file","One or more errors have occurred")
    if(LoadSetting("Settings","AutoUpdate",True)):
        version = CheckForUpdate()
        if(version != "null"): UpdateWindow(win,version)
    sys.exit(app.exec())