from pathlib import Path
from shutil import copyfile, copytree

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog
from psutil import disk_partitions

from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.services.discord import discord_presence, DiscordState
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

        self.ModName.setText('New Mod')
        self.UpdateName()
        self.ModName.textEdited.connect(self.UpdateName)
        self.SDSelector.currentIndexChanged.connect(self.UpdateName)
        self.Patch.clicked.connect(self.CreatePatch)

        discord_presence.update(DiscordState.CreatingRiivolutionPatch)
        self.show()
        self.exec()
        discord_presence.update(DiscordState.ModdingWiiMusic)

    def UpdateName(self):
        if self.SDSelector.currentIndex() == 0:
            if rom_folder.folderPath.stem.lower() == "data":
                path = rom_folder.folderPath.parent.parent / self.ModName.text()
            else:
                path = rom_folder.folderPath.parent / self.ModName.text()
            self.SaveLabel.setText(str(path))
        else:
            self.SaveLabel.setText(self.SDSelector.currentText())

    def CreatePatch(self):
        mod_path = Path(self.SaveLabel.text())
        mod_name_full = self.ModName.text()
        mod_name = mod_name_full.replace(' ', '')

        (mod_path / 'Riivolution').mkdir(parents=True, exist_ok=True)
        (mod_path / mod_name).mkdir(parents=True, exist_ok=True)
        if self.SaveFile_Checkbox.isChecked():
            copytree(paths.includeAll / 'save', mod_path / mod_name / 'save')
        copyfile(rom_folder.mainDolPath, mod_path / mod_name / 'main.dol')
        copyfile(rom_folder.messagePath / 'message.carc', mod_path / mod_name / 'message.carc')
        copyfile(rom_folder.brsarPath, mod_path / mod_name / 'rp_Music_sound.brsar')
        message_region = rom_folder.messagePath.parent.stem
        lines_to_write = f'''
<wiidisc version="1" root="">
    <id game="R64" />
    <options>
        <section name="{mod_name_full}">
            <option name="Load Mod">
                <choice name="Enabled">
                    <patch id="TheMod" />
                </choice>
            </option>
        </section>
    </options>
    <patch id="TheMod">
        <file disc="/Sound/MusicStatic/rp_Music_sound.brsar" external="/{mod_name}/rp_Music_sound.brsar" offset=""/>
        <file disc="/{message_region}/Message/message.carc" external="/{mod_name}/message.carc" offset=""/>
        <file disc="main.dol" external="/{mod_name}/main.dol" offset="" />
    </patch>
</wiidisc>'''
        if self.SaveFile_Checkbox.isChecked():
            line_split = lines_to_write.splitlines()
            line_split.insert(-2, f'        <savegame external = "/{mod_name}/save" clone = "false" />')
            lines_to_write = '\n'.join(line_split)
        with open(f"{mod_path}/Riivolution/{mod_name}.xml", 'w') as xml:
            xml.writelines(lines_to_write)
        self.Patch.setEnabled(False)
        SuccessWindow(tr("Riivolution", "Creation Complete!"))
        self.close()
