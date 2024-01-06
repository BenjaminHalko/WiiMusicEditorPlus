import os
from pathlib import Path

from PyQt6.QtWidgets import QFileDialog, QWidget

from wii_music_editor.editor.loaded_file import PrepareFile
from wii_music_editor.ui.views.error_handler.error_handler import ShowError
from wii_music_editor.utils import paths
from wii_music_editor.utils.osUtils import choose_from_os
from wii_music_editor.utils.save import save_setting
from wii_music_editor.utils.translate import tr


def save_file_directory(directory):
    if Path(directory).is_dir():
        paths.lastLoadedPath = directory[0:len(directory) - len(os.path.basename(directory)) - 1:1]
    else:
        paths.lastLoadedPath = os.path.dirname(directory)
    save_setting("Paths", "LastLoadedPath", paths.lastLoadedPath)


def select_dolphin_path():
    file = QFileDialog()
    file.setFileMode(QFileDialog.FileMode.ExistingFiles)
    file.setNameFilter(choose_from_os(["Dolphin (Dolphin.exe)", "Dolphin (Dolphin.app)", "Dolphin (dolphin-emu)"]))
    if paths.dolphinPath != "":
        file.setDirectory(str(paths.dolphinPath))
    else:
        file.setDirectory(str(paths.programPath))
    if file.exec():
        paths.dolphinPath = file.selectedFiles()[0]
        save_setting("Paths", "Dolphin", file.selectedFiles()[0])
        return True
    return False


def select_rom_path(widget, dialog_filter):
    try:
        file = QFileDialog()
        if dialog_filter == "":
            file.setFileMode(QFileDialog.FileMode.Directory)
        else:
            file.setFileMode(QFileDialog.FileMode.ExistingFile)
        file.setNameFilter(dialog_filter)
        file.setDirectory(str(paths.lastLoadedPath))
        if file.exec():
            path = file.selectedFiles()[0]
            if os.path.isdir(path):
                if not os.path.exists(path + "/files") or not os.path.exists(path + "/sys"):
                    path = path + "/DATA"
                if not os.path.exists(path + "/files") or not os.path.exists(path + "/sys"):
                    ShowError(
                        tr("Error", "Not a valid Wii Music folder"),
                        tr("Error", "Files and sys folder not found"),
                        widget
                    )
                    return False

            paths.loadedFilePath = Path(path)
            save_file_directory(file.selectedFiles()[0])
            PrepareFile()
            save_setting("Paths", "CurrentLoadedFile", str(paths.loadedFilePath))
            return True
    except Exception as e:
        print(e)

    return False
