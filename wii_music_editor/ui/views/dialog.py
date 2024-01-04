from os import path, mkdir, remove
from shutil import copyfile, move, copytree
from wii_music_editor_plus.utils.editor import GetBrsarPath, GetGeckoPath, GetMainDolPath, GetMessagePath, GetSongNames, LoadSetting, SavePath, ProgramPath
import wii_music_editor_plus.utils.editor as editor
from wii_music_editor_plus.utils.editor import RecordType, LoadSetting, RecordType, GetMainDolPath, Songs, LoadMidi, PatchBrsar, Styles, AddPatch, ChangeName, BasedOnRegion, gctRegionOffsets, Instruments, PatchMainDol, gctRegionOffsetsStyles, HelperPath, Run, romLanguage, gameIds
from configparser import ConfigParser
from wii_music_editor_plus.ui.views.error_handler.error_handler import ShowError
from psutil import disk_partitions
from pathlib import Path
from requests import get
from zipfile import ZipFile

from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal, Qt

from revertchanges_ui import Ui_Revert
from confirm_ui import Ui_Confirm
from importchanges_ui import Ui_Import
from wii_music_editor_plus.ui.views.pack_rom.pack_rom_ui import Ui_Packrom
from riivolution_ui import Ui_Riivolution
from success_ui import Ui_Success

class SuccessWindow(QDialog,Ui_Success):
    def __init__(self,message):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.setupUi(self)
        self.CompleteTitle.setText(message)
        self.CompleteClose.clicked.connect(self.close)
        self.show()
        self.exec()

class RevertChangesWindow(QDialog,Ui_Revert):
    def __init__(self):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.setupUi(self)

        self.SelectButton.clicked.connect(lambda: self.SelectAll(True))
        self.DeselectButton.clicked.connect(lambda: self.SelectAll(False))
        self.PatchButton.clicked.connect(self.Revert)

        self.show()
        self.exec()

    def SelectAll(self,select):
        self.Songs.setChecked(select)
        self.Styles.setChecked(select)
        self.Text.setChecked(select)
        self.MainDol.setChecked(select)
        
    def Revert(self):
        sections = []
        if(path.isfile(editor.file.path+"/Changes.ini") and LoadSetting("Settings","RemoveChangesFromChangesINI",True)):
            ini = ConfigParser()
            ini.read(editor.file.path+"/Changes.ini")
            sections = ini.sections()

        if(self.Songs.isChecked()):
            try:
                if(path.isfile(GetGeckoPath())):
                    codes = open(GetGeckoPath())
                    textlines = codes.readlines()
                    codes.close()
                    linenum = 0
                    while linenum < len(textlines):
                        if('Song' in textlines[linenum]):
                            textlines.pop(linenum)
                            while(len(textlines) > linenum) and (textlines[linenum][0].isnumeric() or textlines[linenum][0].isalpha()):
                                textlines.pop(linenum)
                        else:
                            linenum = linenum+1					
                    codes = open(GetGeckoPath(),'w')
                    codes.writelines(textlines)
                    codes.close()
                copyfile(GetBrsarPath()+".backup",GetBrsarPath())
                for section in sections:
                    if(RecordType.Song in section): ini.remove_section(section)
            except Exception as e:
                ShowError(self.tr("Could not revert songs"),str(e),self)
        if(self.Text.isChecked()):
            try:
                copyfile(GetMessagePath()+"/message.carc.backup",GetMessagePath()+"/message.carc")
                if(path.isfile(GetMessagePath()+'/message.d/new_music_message.txt')): remove(GetMessagePath()+'/message.d/new_music_message.txt')
                GetSongNames()
                for section in sections:
                    if(RecordType.TextSong in section or RecordType.TextStyle in section): ini.remove_section(section)
            except Exception as e:
                ShowError(self.tr("Could not revert message file"),str(e),self)
        if(self.Styles.isChecked()):
            try:
                codes = open(GetGeckoPath())
                textlines = codes.readlines()
                codes.close()
                linenum = 0
                while linenum < len(textlines):
                    if('Style' in textlines[linenum]):
                        textlines.pop(linenum)
                        while(len(textlines) > linenum) and (textlines[linenum][0].isnumeric() or textlines[linenum][0].isalpha()):
                            textlines.pop(linenum)
                    else:
                        linenum = linenum+1
                codes = open(GetGeckoPath(),'w')
                codes.writelines(textlines)
                codes.close()
                for section in sections:
                    if(RecordType.Style in section or RecordType.DefaultStyle in section): ini.remove_section(section)
            except Exception as e:
                ShowError(self.tr("Could not revert styles"),str(e),self)
        if(self.MainDol.isChecked()):
            try:
                copyfile(GetMainDolPath()+".backup",GetMainDolPath())
                for section in sections:
                    if(RecordType.RemoveSong in section or RecordType.MainDol in section): ini.remove_section(section)
            except Exception as e:
                ShowError(self.tr("Could not revert main.dol"),str(e),self)
        if(path.isfile(editor.file.path+"/Changes.ini") and LoadSetting("Settings","RemoveChangesFromChangesINI",True)):
            with open(editor.file.path+"/Changes.ini", 'w') as inifile:
                ini.write(inifile)
        self.close()
        SuccessWindow(self.tr("Files Reverted!"))

class ConfirmWindow(QDialog,Ui_Confirm):
    def __init__(self,message):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.setupUi(self)
        self.clicked = False

        self.text.setText(self.tr(message))
        self.noButton.clicked.connect(self.close)
        self.yesButton.clicked.connect(self.Ok)

        self.show()
        self.exec()

    def Ok(self):
        self.clicked = True
        self.close()

def ConfirmDialog(message):
    win = ConfirmWindow(message)
    return win.clicked

class Import(QThread):
    progress = pyqtSignal(int,int)
    done = pyqtSignal()
    error = pyqtSignal(str,str)
    recordfile = "null"

    def run(self):
        ini = ConfigParser()
        ini.read(self.recordfile)
        sections = ini.sections()
        self.waiting = False
        for section in sections:
            try:
                self.progress.emit(sections.index(section),len(sections))
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
                    patchInfo = '0'+format(Styles[int(name)].MemOffset+BasedOnRegion(gctRegionOffsetsStyles),"x")+" 00000018\n"
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
                elif(action == RecordType.RemoveSong):
                    file = open(GetMainDolPath(), "r+b")
                    for song in ini.get(section,"songs").split(","):
                        file.seek(0x59C574+0xBC*Songs[int(song.replace("[","").replace("]",""))].MemOrder)
                        file.write(bytes.fromhex('ffffffffffff'))
                    file.close()
                elif(action == RecordType.DefaultStyle):
                    AddPatch(Songs[int(name)].Name+' Default Style Patch','0'+format(Songs[int(name)].MemOffset+BasedOnRegion(gctRegionOffsets)+42,'x')+' 000000'+Styles[int(ini.get(section,"style"))].StyleId+'\n')
            except Exception as e:
                self.error.emit(self.tr("Could not import change")+" "+section,str(e))
                self.waiting = True
                while self.waiting: w = 0
        self.done.emit()

class ImportChangesWindow(QDialog,Ui_Import):
    def __init__(self,file):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.setupUi(self)
        self.file = file

        self.importthread = Import()
        self.importthread.progress.connect(self.reportProgress)
        self.importthread.done.connect(self.finish)
        self.importthread.error.connect(self.error)
        self.importthread.recordfile = file
        self.importthread.start()

        self.show()
        self.exec()

    def finish(self):
        self.Progress.setValue(100)
        self.Label.setText(self.tr("Finished Importing Changes"))

    def reportProgress(self,value,total):
        self.Progress.setValue((value-1)/total*100)
        self.Label.setText(self.tr("Importing Change {} out of {}".format(value,total)))

    def error(self,error,message):
        ShowError(error,message,self)
        self.importthread.waiting = False

class PackRomWindow(QDialog,Ui_Packrom):
    def __init__(self):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.setupUi(self)
        self.CreateRom.clicked.connect(self.MakeRom)
        self.show()
        self.exec()

    def MakeRom(self):
        file = QFileDialog()
        file.setFileMode(QFileDialog.AnyFile)
        file.setAcceptMode(QFileDialog.AcceptSave)
        if(self.RomTypeWbfs.isChecked()): file.setNameFilter(self.tr("Wii Backup File System")+" (*.wbfs)")
        else: file.setNameFilter("iso (*.iso)")
        if(file.exec()):
            try:
                filePath = file.selectedFiles()[0]
                if(self.RomTypeWbfs.isChecked()): fileType = ".wbfs"
                else: fileType = ".iso"
                if(path.exists(filePath)): remove(filePath)
                if(Path(filePath).suffix != fileType): filePath = filePath+fileType
                args = [HelperPath()+'/Wiimms/wit','cp',editor.file.path,filePath]
                if(self.RomTypeWbfs.isChecked()): args.append('--wbfs')
                if(self.PatchMainDolCheckbox.isChecked()):
                    copyfile(GetMainDolPath(),GetMainDolPath()+".tmp")
                    PatchMainDol()
                Run(args)
                if(self.PatchMainDolCheckbox.isChecked()):
                    remove(GetMainDolPath())
                    move(GetMainDolPath()+".tmp",GetMainDolPath())
                self.close()
                SuccessWindow(self.tr("Rom Successfuly Packed!"))
            except Exception as e:
                self.close()
                ShowError(self.tr("Could not pack rom"),str(e))

class RiivolutionWindow(QDialog,Ui_Riivolution):
    def __init__(self):
        super().__init__(None)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.disks = disk_partitions()

        for disk in self.disks:
            self.SDSelector.addItem(disk.device)

        self.ModName.setText(path.basename(editor.file.path[0:len(editor.file.path)-len(path.basename(editor.file.path))-1:1]))
        self.UpdateName()
        self.ModName.textEdited.connect(self.UpdateName)
        self.Patch.clicked.connect(self.CreatePatch)

        self.show()
        self.exec()

    def UpdateName(self):
        if(path.basename(editor.file.path).lower() == "data"):
            name = editor.file.path[0:len(editor.file.path)-len(path.basename(editor.file.path[0:len(editor.file.path)-5:1]))-5:1]+self.ModName.text()
        else:
            name = editor.file.path[0:len(editor.file.path)-len(path.basename(editor.file.path)):1]+self.ModName.text()
        extra = ""
        num = 1
        while(path.exists(name+extra)):
            num += 1
            extra = " ("+str(num)+")"
        self.SaveLabel.setText(name+extra)

    def CreatePatch(self):
        ModPath = self.SaveLabel.text()
        ModName = self.ModName.text()

        mkdir(ModPath)
        mkdir(ModPath+'/Riivolution')
        if(self.GeckocodeOptions.currentIndex() == 1):
            mkdir(ModPath+'/Riivolution/codes')
            copyfile(HelperPath()+'/Extra/codehandler.bin',ModPath+'/Riivolution/codes/codehandler.bin')
        mkdir(ModPath+'/'+ModName.replace(' ',''))
        copyfile(GetBrsarPath(),ModPath+'/'+ModName.replace(' ','')+'/rp_Music_sound.brsar')
        copyfile(GetMessagePath()+'/message.carc',ModPath+'/'+ModName.replace(' ','')+'/message.carc')
        copyfile(GetMainDolPath(),ModPath+'/'+ModName.replace(' ','')+'/main.dol')
        if(self.GeckocodeOptions.currentIndex() == 1): editor.CreateGct(ModPath+'/Riivolution/codes/'+editor.BasedOnRegion(gameIds)+'.gct')
        elif(self.GeckocodeOptions.currentIndex() == 0): PatchMainDol(dolPath=ModPath+'/'+ModName.replace(' ','')+'/main.dol')
        linestowrite = [
        '<wiidisc version="1" root="">\n',
        '  <id game="R64" />\n',
        '  <options>\n',
        '    <section name="'+ModName+'">\n',
        '      <option name="Load Mod">\n',
        '        <choice name="Enabled">\n',
        '          <patch id="TheMod" />\n',
        '        </choice>\n',
        '      </option>\n',
        '    </section>\n',
        '  </options>\n',
        '  <patch id="TheMod">\n',
        '    <file disc="/Sound/MusicStatic/rp_Music_sound.brsar" external="/'+ModName.replace(' ','')+'/rp_Music_sound.brsar" offset="" />\n',
        '    <file disc="/'+editor.BasedOnRegion(romLanguage)+'/Message/message.carc" external="/'+ModName.replace(' ','')+'/message.carc" offset="" />\n',
        '    <file disc="main.dol" external="/'+ModName.replace(' ','')+'/main.dol" offset="" />\n',
        '  </patch>\n',
        '</wiidisc>\n']
        if(self.GeckocodeOptions.currentIndex() == 1):
            linestowrite.insert(15,'    <memory valuefile="codes/'+editor.BasedOnRegion(gameIds)+'.gct" offset="0x800028B8" />\n')
            linestowrite.insert(16,'    <memory valuefile="codes/codehandler.bin" offset="0x80001800" />\n')
            linestowrite.insert(17,'    <memory value="8000" offset="0x00001CDE" />\n')
            linestowrite.insert(18,'    <memory value="28B8" offset="0x00001CE2" />\n')
            linestowrite.insert(19,'    <memory value="8000" offset="0x00001F5A" />\n')
            linestowrite.insert(20,'    <memory value="28B8" offset="0x00001F5E" />\n')
        xml = open(ModPath+'/Riivolution/'+ModName.replace(' ','')+'.xml','w')
        xml.writelines(linestowrite)
        xml.close()
        if(self.SDSelector.currentIndex() != 0):
            mpoint = self.disks[self.SDSelector.currentIndex()-1].mountpoint
            copytree(ModPath+'/Riivolution',mpoint+'Riivolution')
            copytree(ModPath+'/'+ModName.replace(' ',''),mpoint+ModName.replace(' ',''))
        self.Patch.setEnabled(False)
        SuccessWindow(self.tr("Creation Complete!"))
        self.close()

class DownloadSongThread(QThread):
    progress = pyqtSignal(str)
    done = pyqtSignal()

    def run(self):
        file = open(SavePath()+"/downloaded.zip", "wb")
        file.write(get("https://github.com/BenjaminHalko/Pre-Made-Songs-for-Wii-Music/archive/refs/heads/main.zip").content)
        file.close()
        zip = ZipFile(SavePath()+"/downloaded.zip")
        for zip_info in zip.infolist():
            if zip_info.filename[-1] == '/':
                continue
            zip_info.filename = zip_info.filename.replace("Pre-Made-Songs-for-Wii-Music-main/","")
            zip.extract(zip_info,ProgramPath+"/Pre-Made Songs for Wii Music")
        zip.close()
        remove(SavePath()+"/downloaded.zip")
        self.done.emit()