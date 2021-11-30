from editor import LoadSetting, RecordType, LoadMidi, PatchBrsar, Styles, AddPatch, ChangeName, BasedOnRegion, gctRegionOffsets, Instruments, PatchMainDol
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication
from importchanges_ui import Ui_Dialog
from configparser import ConfigParser
from errorhandler import ShowError

class Import(QThread):
    progress = pyqtSignal(int,int)
    done = pyqtSignal()
    recordfile = "null"

    def run(self):
        ini = ConfigParser()
        ini.read(self.recordfile)
        sections = ini.sections()
        i = 0
        for section in sections:
            i += 1
            self.progress.emit(i,len(sections))
            action,name = section.split("-")
            if(action == RecordType.Song):
                brseqInfo = [0,0]
                brseqLength = [0,0]
                if(LoadSetting("Settings","NormalizeMidi",False)):
                    midiInfo = LoadMidi(ini.get(section,"midisong"),int(ini.get(section,"tempo")))
                else:
                    midiInfo = LoadMidi(ini.get(section,"midisong"))
                brseqInfo[0] = midiInfo[0]
                brseqLength[0] = midiInfo[1]

                if(ini.get(section,"midiscore") != ""):
                    if(LoadSetting("Settings","NormalizeMidi",False)):
                        midiInfo = LoadMidi(ini.get(section,"midiscore"),int(ini.get(section,"tempo")))
                    else:
                        midiInfo = LoadMidi(ini.get(section,"midiscore"))
                brseqInfo[1] = midiInfo[0]
                brseqLength[1] = midiInfo[1]
                
                PatchBrsar(int(name),brseqInfo,brseqLength,int(ini.get(section,"tempo")),int(ini.get(section,"length")),int(ini.get(section,"timesignature")))
            elif(action == RecordType.Style):
                patchInfo = '0'+format(Styles[int(name)].MemOffset+BasedOnRegion(gctRegionOffsets),"x")+" 00000018\n"
                for i in range(3):
                    if(int(ini.get(section,str(i*2))) == len(Instruments)-1): num1 = "ffffffff"
                    else: num1 = format(int(ini.get(section,str(i*2))),"x")
                    if(int(ini.get(section,str(i*2+1))) == len(Instruments)-1): num2 = "ffffffff"
                    else: num2 = format(int(ini.get(section,str(i*2+1))),"x")
                    patchInfo = patchInfo+"0"*(8-len(num1))+num1+" "+"0"*(8-len(num2))+num2+"\n"
                AddPatch(Styles[int(name)].Name+" Style Patch",patchInfo)
            elif(action == RecordType.TextSong):
                ChangeName(int(name),[ini.get(section,"name"),ini.get(section,"desc"),ini.get(section,"genre")])
            elif(action == RecordType.TextStyle):
                ChangeName(int(name),ini.get(section,"name"))
            elif(action == RecordType.MainDol):
                PatchMainDol(geckoPath=ini.get(section,"geckopath"))
        self.done.emit()

class ImportChangesWindow(QDialog,Ui_Dialog):
    def __init__(self,file):
        super().__init__(None)
        self.setupUi(self)
        self.file = file

        thread = Import()
        thread.progress.connect(self.reportProgress)
        thread.done.connect(self.close)
        thread.recordfile = file
        thread.start()

        self.show()
        self.exec()

    def reportProgress(self,value,total):
        self.Progress.setValue(value/total*100)
        self.Label.setText(QCoreApplication.translate("Import change "+str(value)+" out of "+str(total)))