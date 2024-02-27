import os
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.services.discord import discord_presence, DiscordState
from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.ui.widgets.load_files import save_file
from wii_music_editor.ui.widgets.translate import tr
from wii_music_editor.ui.windows.pack_rom_ui import Ui_Packrom
from wii_music_editor.ui.success import SuccessWindow
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.utils.shell import run_shell


class PackRomWindow(QDialog, Ui_Packrom):
    def __init__(self):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setupUi(self)
        self.CreateRom.clicked.connect(self.MakeRom)
        discord_presence.update(DiscordState.PackingRom)
        self.show()
        self.exec()
        discord_presence.update(DiscordState.ModdingWiiMusic)

    def MakeRom(self):
        if self.RomTypeWbfs.isChecked():
            save_filter = tr("file", "Wii Backup File System") + " (*.wbfs)"
        else:
            save_filter = "iso (*.iso)"
        save_path = save_file(save_filter, "pack_rom")
        if save_path != "":
            try:
                file_path = Path(save_path)
                if self.RomTypeWbfs.isChecked():
                    file_type = ".wbfs"
                else:
                    file_type = ".iso"
                if file_path.exists():
                    os.remove(file_path)
                file_path = file_path.with_suffix(file_type)
                args = [paths.include/'wiimms'/'wit', 'cp', rom_folder.folderPath, file_path]
                if self.RomTypeWbfs.isChecked():
                    args.append('--wbfs')
                run_shell(args)
                self.close()
                SuccessWindow(tr("rom", "Rom Successfuly Packed!"))
            except Exception as e:
                self.close()
                ShowError(tr("rom", "Could not pack rom."), str(e))
