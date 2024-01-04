import os
from PyQt6.QtWidgets import QFileDialog

from wii_music_editor.ui.views.error_handler.error_handler import ShowError
from wii_music_editor.utils.helper import paths
from wii_music_editor.utils.helper.osUtils import choose_from_os
from wii_music_editor.utils.helper.save import save_setting
from wii_music_editor.utils.translate import translator


def select_dolphin_path():
    file = QFileDialog()
    file.setFileMode(QFileDialog.FileMode.ExistingFiles)
    file.setNameFilter(choose_from_os(["Dolphin (Dolphin.exe)", "Dolphin (Dolphin.app)", "Dolphin (dolphin-emu)"]))
    if file.exec():
        paths.dolphinPath = file.selectedFiles()[0]
        save_setting("Paths", "Dolphin", file.selectedFiles()[0])
        return True
    return False


def select_rom_path(dialog_filter):
    file = QFileDialog()
    if dialog_filter == "":
        file.setFileMode(QFileDialog.FileMode.DirectoryOnly)
    else:
        file.setFileMode(QFileDialog.FileMode.ExistingFile)
    file.setNameFilter(dialog_filter)
    file.setDirectory(paths.programPath)
    if file.exec():
        path = file.selectedFiles()[0]
        if os.path.isdir(path):
            if not os.path.exists(path + "/files") or not os.path.exists(path + "/sys"):
                path = path + "/DATA"
            if not os.path.exists(path + "/files") or not os.path.exists(path + "/sys"):
                ShowError(translator("Not a valid Wii Music folder"), translator("Files and sys folder not found"))
                return False

        paths.romPath = path
        if os.path.isdir(path):
            paths.lastLoadedPath = paths.romPath[
                                   0:len(paths.romPath) - len(os.path.basename(paths.romPath)) - 1:1]
        else:
            paths.lastLoadedPath = os.path.dirname(paths.romPath)
        save_setting("Paths", "LastLoadedPath", paths.lastLoadedPath)
        # PrepareFile()
        save_setting("Paths", "CurrentLoadedFile", paths.romPath)
        return True
    return False
