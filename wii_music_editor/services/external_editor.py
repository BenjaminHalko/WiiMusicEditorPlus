from PySide6.QtCore import QThread, pyqtSignal

from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.utils.osUtils import choose_from_os
from wii_music_editor.utils.shell import give_permission, run_shell


class ExternalEditor(QThread):
    done = pyqtSignal()

    def run(self):
        rom_folder.text.decode()
        give_permission(f'{rom_folder.messagePath}/message.d/new_music_message.txt')
        run_shell(f'{choose_from_os(["notepad", "open -e", "gedit"])} "${rom_folder.messagePath}/message.d/new_music_message.txt"')
        rom_folder.text.read()
        rom_folder.encode()
        self.done.emit()
