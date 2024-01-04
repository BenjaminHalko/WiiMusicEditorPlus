from os import path, mkdir
from shutil import copyfile

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog
from psutil import disk_partitions

from wii_music_editor.ui.views.riivolution.riivolution_ui import Ui_Riivolution
from wii_music_editor.utils import paths


class RiivolutionWindow(QDialog, Ui_Riivolution):
    def __init__(self):
        super().__init__(None)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.disks = disk_partitions()

        for disk in self.disks:
            self.SDSelector.addItem(disk.device)

        self.ModName.setText(
            path.basename(paths.loadedFilePath[0:len(paths.loadedFilePath) - len(path.basename(paths.loadedFilePath)) - 1:1]))
        self.UpdateName()
        self.ModName.textEdited.connect(self.UpdateName)
        self.Patch.clicked.connect(self.CreatePatch)

        self.show()
        self.exec()

    def UpdateName(self):
        if path.basename(paths.loadedFilePath).lower() == "data":
            name = (paths.loadedFilePath[
                    0:len(paths.loadedFilePath) - len(path.basename(paths.loadedFilePath[0:len(paths.loadedFilePath) - 5:1])) - 5:1]
                    + self.ModName.text())
        else:
            name = paths.loadedFilePath[0:len(paths.loadedFilePath) - len(path.basename(paths.loadedFilePath)):1] + self.ModName.text()
        extra = ""
        num = 1
        while path.exists(name + extra):
            num += 1
            extra = f" ({num})"
        self.SaveLabel.setText(name + extra)

    def CreatePatch(self):
        mod_path = self.SaveLabel.text()
        mod_name = self.ModName.text()

        mkdir(mod_path)
        mkdir(mod_path + '/Riivolution')
        if self.GeckocodeOptions.currentIndex() == 1:
            mkdir(mod_path + '/Riivolution/codes')
            copyfile(f'{paths.includeAllPath}/gecko/codehandler.bin', mod_path + '/Riivolution/codes/codehandler.bin')
        mkdir(mod_path + '/' + mod_name.replace(' ', ''))
        copyfile(GetBrsarPath(), mod_path + '/' + mod_name.replace(' ', '') + '/rp_Music_sound.brsar')
        copyfile(GetMessagePath() + '/message.carc', mod_path + '/' + mod_name.replace(' ', '') + '/message.carc')
        copyfile(GetMainDolPath(), mod_path + '/' + mod_name.replace(' ', '') + '/main.dol')
        if (self.GeckocodeOptions.currentIndex() == 1):
            editor.CreateGct(mod_path + '/Riivolution/codes/' + editor.BasedOnRegion(gameIds) + '.gct')
        elif (self.GeckocodeOptions.currentIndex() == 0):
            PatchMainDol(dolPath=mod_path + '/' + mod_name.replace(' ', '') + '/main.dol')
        linestowrite = [
            '<wiidisc version="1" root="">\n',
            '  <id game="R64" />\n',
            '  <options>\n',
            '    <section name="' + mod_name + '">\n',
            '      <option name="Load Mod">\n',
            '        <choice name="Enabled">\n',
            '          <patch id="TheMod" />\n',
            '        </choice>\n',
            '      </option>\n',
            '    </section>\n',
            '  </options>\n',
            '  <patch id="TheMod">\n',
            '    <file disc="/Sound/MusicStatic/rp_Music_sound.brsar" external="/' + mod_name.replace(' ',
                                                                                                     '') + '/rp_Music_sound.brsar" offset="" />\n',
            '    <file disc="/' + editor.BasedOnRegion(
                romLanguage) + '/Message/message.carc" external="/' + mod_name.replace(' ',
                                                                                      '') + '/message.carc" offset="" />\n',
            '    <file disc="main.dol" external="/' + mod_name.replace(' ', '') + '/main.dol" offset="" />\n',
            '  </patch>\n',
            '</wiidisc>\n']
        if (self.GeckocodeOptions.currentIndex() == 1):
            linestowrite.insert(15, '    <memory valuefile="codes/' + editor.BasedOnRegion(
                gameIds) + '.gct" offset="0x800028B8" />\n')
            linestowrite.insert(16, '    <memory valuefile="codes/codehandler.bin" offset="0x80001800" />\n')
            linestowrite.insert(17, '    <memory value="8000" offset="0x00001CDE" />\n')
            linestowrite.insert(18, '    <memory value="28B8" offset="0x00001CE2" />\n')
            linestowrite.insert(19, '    <memory value="8000" offset="0x00001F5A" />\n')
            linestowrite.insert(20, '    <memory value="28B8" offset="0x00001F5E" />\n')
        xml = open(mod_path + '/Riivolution/' + mod_name.replace(' ', '') + '.xml', 'w')
        xml.writelines(linestowrite)
        xml.close()
        if (self.SDSelector.currentIndex() != 0):
            mpoint = self.disks[self.SDSelector.currentIndex() - 1].mountpoint
            copytree(mod_path + '/Riivolution', mpoint + 'Riivolution')
            copytree(mod_path + '/' + mod_name.replace(' ', ''), mpoint + mod_name.replace(' ', ''))
        self.Patch.setEnabled(False)
        SuccessWindow(self.tr("Creation Complete!"))
        self.close()
