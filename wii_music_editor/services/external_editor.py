import os

from PySide6.QtCore import QThread, Signal

from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.utils.osUtils import choose_from_os
from wii_music_editor.utils.shell import give_permission, run_shell


class ExternalEditor(QThread):
    done = Signal()

    def run(self):
        os.mkdir(rom_folder.messagePath/'message.d')
        path = rom_folder.messagePath/'message.d'/'new_music_message.txt'
        with open(path, 'wb') as file:
            file.writelines(rom_folder.text.textlines)
        give_permission(path)
        print(path)
        text_editor = choose_from_os([["notepad"], ["open", "-e"], ["gedit"]])
        run_shell(text_editor + [path])
        self.done.emit()
