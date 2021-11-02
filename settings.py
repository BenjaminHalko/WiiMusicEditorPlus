from os import path
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets
from settings_ui import Ui_Settings
import editor
from editor import SaveSetting, LoadSetting
from errorhandler import ShowError
from update import UpdateWindow

_translate = QCoreApplication.translate

class SettingsWindow(QDialog,Ui_Settings):
    def __init__(self,otherWindow):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.setupUi(self)
        self.otherWindow = otherWindow

        self.RegionBox.setCurrentIndex(editor.regionSelected)
        self.RegionBox.currentIndexChanged.connect(self.RegionChange)

        self.SwitchBeta.clicked.connect(self.Button_SwitchBeta)
        if(LoadSetting("Settings","Beta",False)): self.SwitchBeta.setText(_translate("MainWindow","Switch to Main"))

        self.ConnectCheckmark(self.CheckForUpdates,"AutoUpdate",True)
        self.ConnectCheckmark(self.RapperFix,"RapperFix",True)
        self.ConnectCheckmark(self.UnsafeMode,"UnsafeMode",False)
        self.ConnectCheckmark(self.SongScoreCheckbox,"SongScore",False)
        self.ConnectCheckmark(self.Dolphon_Geckocodes,"CopyCodes",True)

        self.DolphinPath_Browse.clicked.connect(self.GetDolphin)
        self.DolphinSave_Browse.clicked.connect(self.GetDolphinSave)
        self.DolphinSave_Default.clicked.connect(self.DefaultDolphinSave)

        if(editor.dolphinPath != ""): self.DolphinPath_Label.setText(_translate("MainWindow",editor.dolphinPath))
        if(editor.dolphinSavePath != ""): self.DolphinSave_Label.setText(_translate("MainWindow",editor.dolphinSavePath))

        self.show()
        self.exec()
    
    def Button_SwitchBeta(self):
        UpdateWindow(self.otherWindow,-1)

    def ConnectCheckmark(self,checkmarkId,setting,default):
        checkmarkId.setCheckState(LoadSetting("Settings",setting,default)*2)
        checkmarkId.stateChanged.connect(lambda: self.Checkmark(checkmarkId,setting))
    
    def Checkmark(self,checkmark,setting):
        SaveSetting("Settings",setting,(checkmark.checkState() == 2))
        if(setting == "UnsafeMode"): editor.unsafeMode = (checkmark.checkState() == 2)

    def RegionChange(self):
        editor.regionSelected = self.RegionBox.currentIndex()
        SaveSetting("Settings","DefaultRegion",editor.regionSelected)

    def GetDolphin(self):
        file = QtWidgets.QFileDialog() 
        file.setFileMode(QtWidgets.QFileDialog.AnyFile)
        file.setNameFilter("Dolphin (Dolphin.exe)")
        file.setViewMode(QtWidgets.QFileDialog.Detail)
        if file.exec_():
            editor.dolphinPath = file.selectedFiles()[0]
            self.DolphinPath_Label.setText(_translate("MainWindow",file.selectedFiles()[0]))
            SaveSetting("Paths","Dolphin",file.selectedFiles()[0])

    def DefaultDolphinSave(self):
        self.DolphinSave_Label.setText(_translate("MainWindow","Default Path"))
        SaveSetting("Paths","DolphinSave","")

    def GetDolphinSave(self):
        file = QtWidgets.QFileDialog() 
        file.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        file.setViewMode(QtWidgets.QFileDialog.Detail)
        if file.exec_():
            if(path.isdir(file.selectedFiles()[0]+"/Wii") and path.isdir(file.selectedFiles()[0]+"/GameSettings")):
                editor.dolphinSavePath = file.selectedFiles()[0]
                self.DolphinSave_Label.setText(_translate("MainWindow",file.selectedFiles()[0]))
                SaveSetting("Paths","DolphinSave",file.selectedFiles()[0])
            else:
                self.hide()
                ShowError("Not a Dolphin Save Directory","Wii and GameSettings folder not found")
                self.show()
