from PyQt6.QtCore import QThread, pyqtSignal

from wii_music_editor.utils import paths
from wii_music_editor.utils.osUtils import choose_from_os
from wii_music_editor.utils.shell import give_permission, run_shell


class ExternalEditor(QThread):
    done = pyqtSignal()

    def run(self):
        give_permission(f'{paths.messagePath}/message.d/new_music_message.txt')
        run_shell(f'{choose_from_os(["notepad", "open -e", "gedit"])} "${paths.messagePath}/message.d/new_music_message.txt"')
        self.done.emit()