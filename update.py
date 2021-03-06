from os import path, remove
from editor import HelperPath, LoadSetting, FullPath, currentSystem, ChooseFromOS, version, SavePath, GivePermission
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from update_ui import Ui_Update
from subprocess import Popen
from requests import get, ConnectionError, Timeout
from zipfile import ZipFile
from sys import exit as sys_exit
from shutil import copyfile, rmtree
from subprocess import call

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

        if(currentSystem == "Linux"):
            if(path.isfile(SavePath()+"/WiiMusicEditorPlus")): remove(SavePath()+"/WiiMusicEditorPlus")
            zip = ZipFile(SavePath()+"/downloaded.zip")
            zip.extractall(SavePath())
            zip.close()
        elif (currentSystem == "Mac"):
            if(path.isdir(SavePath()+"/WiiMusicEditorPlus.app")): rmtree(SavePath()+"/WiiMusicEditorPlus.app")
            zip = ZipFile(SavePath()+"/downloaded.zip")
            for file in zip.infolist():
                zip.extract(file, SavePath())
                call(["chmod","u+x",path.join(SavePath(), file.filename)])
            zip.close()

        if(currentSystem != "Windows"): remove(SavePath()+"/downloaded.zip")
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
        if(path.exists(SavePath()+"/update"+updateExt)): remove(SavePath()+"/update"+updateExt)
        copyfile(HelperPath()+"/Extra/update"+updateExt,SavePath()+"/update"+updateExt)

        if(currentSystem == "Windows"):
            Popen([SavePath()+"/update.bat",FullPath])
        else:
            GivePermission(SavePath()+"/update.sh")
            if(currentSystem == "Linux"): GivePermission(SavePath()+'/WiiMusicEditorPlus')
            Popen([SavePath()+"/update.sh",FullPath])
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
        else:
            looking = True
            i = -1
            while(looking):
                i += 1
                for j in data[i]["assets"]:
                    if(j["name"] == f"WiiMusicEditorPlus-{currentSystem}.zip"):
                        looking = False
                        break
    except:
        i = 0
    return data[i]["tag_name"]