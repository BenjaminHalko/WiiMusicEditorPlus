from os import path, mkdir
from editor import ProgramPath, GetBeta, GetPlatform
from shutil import copytree,move
from tempfile import TemporaryDirectory
from dirsync import sync
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QThread, pyqtSignal
from update_ui import Ui_Update
from subprocess import Popen
from requests import get, ConnectionError, Timeout
from zipfile import ZipFile

class Progress():
    def update(self, op_code, cur_count, max_count=None, message=''):
        if(op_code > 10): UpdateThread.progress.emit(cur_count/max_count*100)

class Download(QThread):
    progress = pyqtSignal(int)
    done = pyqtSignal()
    version = "null"

    def run(self):
        with TemporaryDirectory() as directory:
            directory = "D:\Benjaminz\\test"
            file = open(directory+"/downloaded.zip", "wb")
            with get("https://github.com/BenjaminHalko/WiiMusicEditorPlus/releases/download/"+self.version+"/WiiMusicEditorPlus-Windows.zip",stream=True) as response:
                total =  int(response.headers['content-length'])
                downloaded = 0
                for i in response.iter_content(1024):
                    downloaded+=len(i)
                    file.write(i)
                    UpdateThread.progress.emit(downloaded/total*100)

            file.close()

            zip = ZipFile(directory+"/downloaded.zip")
            zip.extractall(directory+"/downloaded")

            move(directory+"/downloaded/WiiMusicEditorPlus.exe",directory+"/downloaded/Helper/Update/NewProgram.exe")
            #sync(directory+"/downloaded",ProgramPath,"sync",purge=True,ignore=(r"settings.ini",r"Helper/Backup",r"WiiMusicEditorPlus.exe",r"Helper/Backup/Version.txt"),exclude=(r".git",))
        UpdateThread.done.emit()

class UpdateWindow(QDialog,Ui_Update):
    def __init__(self,otherWindow,check):
        global UpdateThread

        super().__init__(None)
        self.otherWindow = otherWindow
        self.setupUi(self)

        if(check == False):
            print("check")
            check = CheckForUpdate()
            if(check == "null"):
                self.MainWidget.setCurrentIndex(2)

        self.NewUpdate_Update.clicked.connect(lambda: self.startupdate(check))
        self.NewUpdate_Cancel.clicked.connect(self.closewindow)
        self.NoUpdate_Button.clicked.connect(self.closewindow)

        self.show()
        self.exec()
        
    def startupdate(self,version):
        global UpdateThread
        self.MainWidget.setCurrentIndex(1)
        UpdateThread = Download()
        UpdateThread.version = version
        UpdateThread.progress.connect(self.reportProgress)
        UpdateThread.done.connect(lambda: self.restart(version))
        UpdateThread.start()

    def reportProgress(self,value):
        self.Update_Progress.setValue(value)

    def restart(self,version):
        file = open(ProgramPath+"/Helper/Update/Version.txt","w")
        file.write(version)
        file.close()
        Popen(ProgramPath+'/Helper/Update/Update.bat')
        self.close()
        self.otherWindow.close()

    def closewindow(self):
        self.close()

def CheckForUpdate():
    if(path.isfile(ProgramPath+"/Helper/Update/Version.txt")):
        file = open(ProgramPath+"/Helper/Update/Version.txt")
        version = file.read()
        file.close()
        try:
            tag = GetReleaseTag()
            if(tag != version): return tag
            else: return "null"
        except (ConnectionError, Timeout):
            return "null"
    else:
        try:
            file = open(ProgramPath+"/Helper/Update/Version.txt","w")
            file.write(GetReleaseTag())
            file.close()
            return "null"
        except (ConnectionError, Timeout):
            return "null"
        
def GetReleaseTag():
    data = get("https://api.github.com/repos/BenjaminHalko/WiiMusicEditorPlus/releases").json()
    i = 0
    if(not GetBeta()):
        while (data[i]["prerelease"]): i += 1
    return data[i]["tag_name"]