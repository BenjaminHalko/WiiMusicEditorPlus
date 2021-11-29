from riivolution_ui import Ui_Riivolution
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QCoreApplication
import editor
from os import path, mkdir
from shutil import copyfile, copytree
from editor import GetBrsarPath, GetMainDolPath, GetMessagePath, PatchMainDol, HelperPath, gameIds, regionNames
from psutil import disk_partitions
from success import SuccessWindow

class RiivolutionWindow(QDialog,Ui_Riivolution):
    def __init__(self):
        global UpdateThread
        super().__init__(None)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.disks = disk_partitions()

        for disk in self.disks:
            self.SDSelector.addItem(disk.device)

        self.ModName.setText(QCoreApplication.translate("MainWindow",path.basename(editor.file.path[0:len(editor.file.path)-len(path.basename(editor.file.path))-1:1])))
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
        self.SaveLabel.setText(QCoreApplication.translate("MainWindow",name+extra))

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
        '    <file disc="/'+editor.BasedOnRegion(regionNames)+'/Message/message.carc" external="/'+ModName.replace(' ','')+'/message.carc" offset="" />\n',
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
        SuccessWindow("Creation Complete!")
        self.close()