from os import chmod, path, remove, stat
from shutil import rmtree
from editor import LoadSetting, FullPath, currentSystem, ChooseFromOS, Run, version, SavePath, GivePermission
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from update_ui import Ui_Update
from subprocess import Popen
from requests import get, ConnectionError, Timeout
from zipfile import ZipFile
import stat as stats
from sys import exit as sys_exit

class Progress():
    def update(self, op_code, cur_count, max_count=None, message=''):
        if(op_code > 10): UpdateThread.progress.emit(cur_count/max_count*100)

class Download(QThread):
    progress = pyqtSignal(int)
    done = pyqtSignal()
    version = "null"

    def run(self):
        file = open(SavePath()+"/downloaded.zip", "wb")
        with get("https://github.com/BenjaminHalko/WiiMusicEditorPlus/releases/download/"+self.version+"/WiiMusicEditorPlus-"+currentSystem+".zip",stream=True) as response:
            total =  int(response.headers['content-length'])
            downloaded = 0
            for i in response.iter_content(1024):
                downloaded+=len(i)
                file.write(i)
                UpdateThread.progress.emit(downloaded/total*100)

        file.close()

        if(currentSystem != "Mac"):
            zip = ZipFile(SavePath()+"/downloaded.zip")
            zip.extractall(SavePath())
            zip.close()
        else:
            Run(["unzip","-d",SavePath(),SavePath()+"/downloaded.zip"])

        remove(SavePath()+"/downloaded.zip")
        UpdateThread.done.emit()

class UpdateWindow(QDialog,Ui_Update):
    def __init__(self,otherWindow,check):
        global UpdateThread
        super().__init__(None)
        self.otherWindow = otherWindow
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)

        self.switchBranch = False
        if(check == False):
            check = CheckForUpdate()
            if(check == "null"):
                self.MainWidget.setCurrentIndex(2)

        self.version = check
        self.NewUpdate_Update.clicked.connect(self.startupdate)
        self.NewUpdate_Cancel.clicked.connect(self.close)
        self.NoUpdate_Button.clicked.connect(self.close)

        self.show()
        self.exec()
        
    def startupdate(self):
        global UpdateThread
        self.MainWidget.setCurrentIndex(1)
        UpdateThread = Download()
        UpdateThread.version = self.version
        UpdateThread.progress.connect(self.reportProgress)
        UpdateThread.done.connect(self.restart)
        UpdateThread.start()

    def reportProgress(self,value):
        self.Update_Progress.setValue(value)

    def restart(self):
        updateExt = ".sh"
        if(currentSystem == "Windows"): updateExt = ".bat"
        if(path.exists(SavePath()+"/"+currentSystem+updateExt)): remove(SavePath()+"/"+currentSystem+updateExt)
        file = open(SavePath()+"/"+currentSystem+updateExt,"wb")
        file.write(get("https://github.com/BenjaminHalko/WiiMusicEditorPlus/raw/main/Update/"+currentSystem+updateExt).content)
        file.close()

        if(currentSystem == "Windows"):
            Popen([SavePath()+"/Windows.bat",FullPath])
        else:
            GivePermission(SavePath()+"/"+currentSystem+".sh")
            GivePermission(SavePath()+'/WiiMusicEditorPlus'+ChooseFromOS([".exe",".app",""]))
            Popen([SavePath()+"/"+currentSystem+".sh",FullPath])
        self.close()
        if(self.otherWindow != list):
            self.otherWindow.close()
        else:
            for window in self.otherWindow:
                window.close()
        sys_exit()

def CheckForUpdate():
    try:
        tag = GetReleaseTag()
        if(tag != version): return tag
        else: return "null"
    except (ConnectionError, Timeout):
        return "null"
        
def GetReleaseTag():
    data = get("https://api.github.com/repos/BenjaminHalko/WiiMusicEditorPlus/releases").json()
    i = 0
    try:
        if(not LoadSetting("Settings","Beta",False)):
            while (data[i]["prerelease"]): i += 1
    except:
        i = 0
    return data[i]["tag_name"]