import os
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import Qt, QLocale, QTranslator
from firstsetup_ui import Ui_FirstSetup
from editor import SaveSetting, TranslationPath, PrepareFile, GetSongNames, ChooseFromOS, languageList, regionNames, ProgramPath, currentSystem, LoadType
import editor
from errorhandler import ShowError
from subprocess import check_output

class FirstSetupWindow(QDialog,Ui_FirstSetup):
    def __init__(self,app,translator):
        super().__init__(None)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)

        self.app = app
        self.translator = translator

        self.BackButton.setEnabled(False)
        self.BackButton.clicked.connect(self.Back)
        self.NextButton.clicked.connect(self.Next)
        self.LanguageBox.currentIndexChanged.connect(self.LanguageChange)
        self.RomLanguageBox.currentIndexChanged.connect(self.RomLanguageSelect)
        self.RegionBox.currentIndexChanged.connect(self.RegionChange)

        self.RomPath_File.clicked.connect(lambda: self.LoadMainFile("Wii Music Rom (*.wbfs *.iso)"))
        self.RomPath_Folder.clicked.connect(lambda: self.LoadMainFile(""))

        self.Dolphon_Geckocodes.stateChanged.connect(lambda: self.Checkmark(self.Dolphon_Geckocodes,"CopyCodes"))
        self.DolphinEnableCheats.stateChanged.connect(lambda: self.Checkmark(self.DolphinEnableCheats,"DolphinEnableCheats"))
        self.DolphinPath_Browse.clicked.connect(self.GetDolphin)

        if(currentSystem == "Linux"):
            temp = check_output("whereis dolphin-emu",shell=True).decode()
            if(os.path.exists(temp[13:len(temp)-1:1])):
                self.DolphinPath_Label.setText(editor.dolphinPath)

        self.RomLanguageChange()

        self.show()
        self.exec()
        
    def Back(self):
        self.MainWidget.setCurrentIndex(self.MainWidget.currentIndex()-1)
        if(self.MainWidget.currentIndex() == 0): self.BackButton.setEnabled(False)

    def Next(self):
        if(self.MainWidget.currentIndex() == self.MainWidget.count()-1):
            self.close()
        else:
            self.MainWidget.setCurrentIndex(self.MainWidget.currentIndex()+1)
            self.BackButton.setEnabled(True)
    
    def LanguageChange(self):
        SaveSetting("Settings","Language",self.LanguageBox.currentIndex())
        self.app.removeTranslator(self.translator)
        if(self.LanguageBox.currentIndex() != 0):
            translator = QTranslator()
            translator.load(QLocale(),TranslationPath()+f"/{languageList[self.LanguageBox.currentIndex()]}.qm")
            self.app.installTranslator(translator)
        self.retranslateUi(self)
        editor.RetranslateSongNames()
        self.RomLanguageChange()

    def RegionChange(self):
        editor.regionSelected = self.RegionBox.currentIndex()
        SaveSetting("Settings","DefaultRegion",self.RegionBox.currentIndex())
        self.RomLanguageChange()

    def RomLanguageChange(self):
        self.RomLanguageBox.blockSignals(True)
        self.RomLanguageBox.clear()
        romLanguageList = [self.tr("English"),self.tr("French"),self.tr("Spanish"),self.tr("Germen"),self.tr("Italian"),self.tr("Japanese"),self.tr("Korean")]
        if(self.RegionBox.currentIndex() > 1):
            self.RomLanguageBox.addItem(romLanguageList[3+self.RegionBox.currentIndex()])
        else:
            for i in range(3+2*self.RegionBox.currentIndex()):
                self.RomLanguageBox.addItem(romLanguageList[i])
        self.RomLanguageBox.setCurrentIndex(editor.romLanguageNumber[self.RegionBox.currentIndex()])
        self.RomLanguageBox.blockSignals(False)

    def RomLanguageSelect(self):
        SaveSetting("Settings","RomLanguage",self.RomLanguageBox.currentIndex())
        editor.romLanguageNumber = [self.RomLanguageBox.currentIndex()]*4
        for i in range(4):
            if(editor.romLanguageNumber[i] >= len(regionNames[i])):
                editor.romLanguageNumber[i] = 0
            editor.romLanguage[i] = regionNames[i][editor.romLanguageNumber[i]]
        if(editor.file.type == LoadType.Rom): GetSongNames()

    def LoadMainFile(self,filter):
        global lastFileDirectory
        file = QFileDialog()
        if(filter == ""): file.setFileMode(QFileDialog.DirectoryOnly)
        else: file.setFileMode(QFileDialog.ExistingFile)
        file.setNameFilter(filter)
        file.setDirectory(ProgramPath)
        if file.exec_():
            path = file.selectedFiles()[0]
            if(os.path.isdir(path)):
                if(not os.path.exists(path+"/files") or not os.path.exists(path+"/sys")): path = path+"/DATA"
                if(not os.path.exists(path+"/files") or not os.path.exists(path+"/sys")):
                    ShowError(self.tr("Not a valid Wii Music folder"),self.tr("Files and sys folder not found"),self)
                    return False
            editor.file.path = path
            if(os.path.isdir(path)): lastFileDirectory = editor.file.path[0:len(editor.file.path)-len(os.path.basename(editor.file.path))-1:1]
            else: lastFileDirectory = os.path.dirname(editor.file.path)
            SaveSetting("Paths","LastLoadedPath",lastFileDirectory)
            PrepareFile()
            SaveSetting("Paths","CurrentLoadedFile",editor.file.path)
            self.RomPath_Label.setText(editor.file.path)
    
    def Checkmark(self,checkmark,setting):
        SaveSetting("Settings",setting,(checkmark.checkState() == 2))

    def GetDolphin(self):
        file = QFileDialog() 
        file.setFileMode(QFileDialog.ExistingFile)
        file.setNameFilter(ChooseFromOS(["Dolphin (Dolphin.exe)","Dolphin (Dolphin.app)","Dolphin (dolphin-emu)"]))
        if file.exec_():
            editor.dolphinPath = file.selectedFiles()[0]
            self.DolphinPath_Label.setText(file.selectedFiles()[0])
            SaveSetting("Paths","Dolphin",file.selectedFiles()[0])