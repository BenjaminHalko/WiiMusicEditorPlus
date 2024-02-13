from os import path, mkdir
from shutil import copyfile, copytree

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog
from psutil import disk_partitions

from wii_music_editor.data.region import game_ids
from wii_music_editor.editor.dol import PatchMainDol
from wii_music_editor.editor.gecko import CreateGct
from wii_music_editor.editor.region import BasedOnRegion
from wii_music_editor.ui.success import SuccessWindow
from wii_music_editor.ui.windows.riivolution_ui import Ui_Riivolution
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.ui.widgets.translate import tr


class RiivolutionWindow(QDialog, Ui_Riivolution):
    def __init__(self):
        super().__init__(None)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.disks = disk_partitions()

        for disk in self.disks:
            self.SDSelector.addItem(disk.device)

        self.ModName.setText(
            path.basename(paths.loadedFile[0:len(paths.loadedFile) - len(path.basename(paths.loadedFile)) - 1:1]))
        self.UpdateName()
        self.ModName.textEdited.connect(self.UpdateName)
        self.Patch.clicked.connect(self.CreatePatch)

        self.show()
        self.exec()

    def UpdateName(self):
        if path.basename(paths.loadedFile).lower() == "data":
            name = (paths.loadedFile[
                    0:len(paths.loadedFile) - len(path.basename(paths.loadedFile[0:len(paths.loadedFile) - 5:1])) - 5:1]
                    + self.ModName.text())
        else:
            name = paths.loadedFile[
                   0:len(paths.loadedFile) - len(path.basename(paths.loadedFile)):1] + self.ModName.text()
        extra = ""
        num = 1
        while path.exists(name + extra):
            num += 1
            extra = f" ({num})"
        self.SaveLabel.setText(name + extra)

    def CreatePatch(self):
        mod_path = self.SaveLabel.text()
        mod_name = self.ModName.text()
        mod_name_xml = mod_name.replace(' ', '')

        mkdir(mod_path)
        mkdir(mod_path + '/Riivolution')
        if self.GeckocodeOptions.currentIndex() == 1:
            mkdir(mod_path + '/Riivolution/codes')
            copyfile(f'{paths.includeAllPath}/gecko/codehandler.bin', mod_path + '/Riivolution/codes/codehandler.bin')
        mkdir(mod_path + '/' + mod_name_xml)
        copyfile(paths.brsar, mod_path + '/' + mod_name_xml + '/rp_Music_sound.brsar')
        copyfile(paths.message / 'message.carc', mod_path + '/' + mod_name_xml + '/message.carc')
        copyfile(paths.mainDol, mod_path + '/' + mod_name_xml + '/main.dol')
        if self.GeckocodeOptions.currentIndex() == 1:
            CreateGct(mod_path + '/Riivolution/codes/' + BasedOnRegion(game_ids) + '.gct')
        elif self.GeckocodeOptions.currentIndex() == 0:
            PatchMainDol(dol_path=mod_path + '/' + mod_name_xml + '/main.dol')
        lines_to_write = f'''
<wiidisc version="1" root="">
    <id game="R64" />
    <options>
        <section name="{mod_name}">
            <option name="Load Mod">
                <choice name="Enabled">
                    <patch id="TheMod" />
                </choice>
            </option>
        </section>
    </options>
    <patch id="TheMod">
        <file disc="/Sound/MusicStatic/rp_Music_sound.brsar" external="/{mod_name_xml}/rp_Music_sound.brsar" offset=""/>
        <file disc="/{BasedOnRegion(game_ids)}/Message/message.carc" external="/{mod_name_xml}/message.carc" offset=""/>
        <file disc="main.dol" external="/{mod_name_xml}/main.dol" offset="" />
    </patch>
</wiidisc>'''
        lines_to_write = lines_to_write.splitlines()
        if self.GeckocodeOptions.currentIndex() == 1:
            lines_to_write.insert(15,
                f'    <memory valuefile="codes/{BasedOnRegion(game_ids)}.gct" offset="0x800028B8" />\n')
            lines_to_write.insert(16, '    <memory valuefile="codes/codehandler.bin" offset="0x80001800" />\n')
            lines_to_write.insert(17, '    <memory value="8000" offset="0x00001CDE" />\n')
            lines_to_write.insert(18, '    <memory value="28B8" offset="0x00001CE2" />\n')
            lines_to_write.insert(19, '    <memory value="8000" offset="0x00001F5A" />\n')
            lines_to_write.insert(20, '    <memory value="28B8" offset="0x00001F5E" />\n')
        with open(f"{mod_path}/Riivolution/{mod_name_xml}.xml", 'w') as xml:
            xml.writelines(lines_to_write)
        if self.SDSelector.currentIndex() != 0:
            mpoint = self.disks[self.SDSelector.currentIndex() - 1].mountpoint
            copytree(mod_path + '/Riivolution', mpoint + 'Riivolution')
            copytree(mod_path + '/' + mod_name_xml, mpoint + mod_name.replace(' ', ''))
        self.Patch.setEnabled(False)
        SuccessWindow(tr("Riivolution", "Creation Complete!"))
        self.close()
