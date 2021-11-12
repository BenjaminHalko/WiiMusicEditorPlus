from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog
from monoframework_ui import Ui_GetMonoFramework
from requests import get
from editor import ProgramPath, Run, currentSystem
from os import remove
from sys import exit as sys_exit

UpdateThread = "null"

class GetMonoFramework(QDialog,Ui_GetMonoFramework):
    def __init__(self,otherWindow):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.setWindowModality(Qt.ApplicationModal)
        self.setupUi(self)
        self.otherWindow = otherWindow

        if(currentSystem != "Mac"): self.MainWidget.setCurrentIndex(3)

        self.DownloadButton.clicked.connect(self.GetMono)
        self.linuxButton.clicked.connect(self.close)
        self.MacDone.clicked.connect(self.CleanUp)

        self.show()
        self.exec()
    
    def GetMono(self):
        global UpdateThread
        self.MainWidget.setCurrentIndex(1)
        UpdateThread = Download()
        UpdateThread.progress.connect(self.reportProgress)
        UpdateThread.done.connect(self.Install)
        UpdateThread.start()

    def reportProgress(self,value):
        self.MonoProgress.setValue(value)

    def Install(self):
        self.MainWidget.setCurrentIndex(2)
        Run('open "'+ProgramPath+'/MonoInstaller.pkg"')

    def CleanUp(self):
        remove(ProgramPath+'/MonoInstaller.pkg')
        Run('open "'+ProgramPath+'/WiiMusicEditorPlus"')
        self.close()
        self.otherWindow.close()
        sys_exit()

class Progress():
    def update(self, op_code, cur_count, max_count=None, message=''):
        if(op_code > 10): UpdateThread.progress.emit(cur_count/max_count*100)

class Download(QThread):
    progress = pyqtSignal(int)
    done = pyqtSignal()
    version = "null"

    def run(self):
        file = open(ProgramPath+"/MonoInstaller.pkg", "wb")
        with get("https://download.mono-project.com/archive/6.12.0/macos-10-universal/MonoFramework-MDK-6.12.0.122.macos10.xamarin.universal.pkg",stream=True) as response:
            total =  int(response.headers['content-length'])
            downloaded = 0
            for i in response.iter_content(1024):
                downloaded+=len(i)
                file.write(i)
                UpdateThread.progress.emit(downloaded/total*100)

        file.close()
        UpdateThread.done.emit()