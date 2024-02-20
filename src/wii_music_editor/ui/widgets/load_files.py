import os
from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.utils.osUtils import choose_from_os
from wii_music_editor.utils.save import save_setting, load_setting
from wii_music_editor.ui.widgets.translate import tr


def save_file_directory(directory: str):
    if Path(directory).is_dir():
        paths.lastLoaded = Path(directory[0:len(directory) - len(os.path.basename(directory)) - 1:1])
    else:
        paths.lastLoaded = Path(os.path.dirname(directory))
    save_setting("Paths", "LastLoadedDir", str(paths.lastLoaded))


def select_dolphin_path():
    file = QFileDialog()
    file.setFileMode(QFileDialog.FileMode.ExistingFiles)
    file.setNameFilter(choose_from_os(["Dolphin (Dolphin.exe)", "Dolphin (Dolphin.app)", "Dolphin (dolphin-emu)"]))
    if paths.dolphin is not None:
        file.setDirectory(str(paths.dolphin))
    else:
        file.setDirectory(str(paths.program))
    if file.exec():
        paths.dolphin = Path(file.selectedFiles()[0])
        save_setting("Paths", "Dolphin", file.selectedFiles()[0])
        return True
    return False


def select_rom_path(dialog_filter: str):
    try:
        file = QFileDialog()
        if dialog_filter == "":
            file.setFileMode(QFileDialog.FileMode.Directory)
        else:
            file.setFileMode(QFileDialog.FileMode.ExistingFile)
        file.setNameFilter(dialog_filter)
        file.setDirectory(str(paths.lastLoadedDir))
        if file.exec():
            path = file.selectedFiles()[0]
            if os.path.isdir(path):
                if not os.path.exists(path + "/files") or not os.path.exists(path + "/sys"):
                    path = path + "/DATA"
                if not os.path.exists(path + "/files") or not os.path.exists(path + "/sys"):
                    ShowError(
                        tr("Error", "Not a valid Wii Music folder"),
                        tr("Error", "Files and sys folder not found"),
                    )
                    return False
            save_file_directory(file.selectedFiles()[0])
            save_setting("Paths", "CurrentLoadedFile", path)
            rom_folder.load(path)
            if rom_folder.loaded:
                return True
    except Exception as e:
        print(e)

    return False


def save_file(dialog_filter: str, save_id: str):
    file = QFileDialog()
    file.setFileMode(QFileDialog.FileMode.AnyFile)
    file.setNameFilter(dialog_filter)
    file.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
    file.setDirectory(load_setting("Paths", f"load_{save_id}", paths.lastLoadedDir))
    if file.exec():
        save_setting("Paths", f"load_{save_id}", str(Path(file.selectedFiles()[0]).parent))
        return file.selectedFiles()[0]
    return ""


def get_file_path(dialog_filter: str, save_id: str) -> str:
    try:
        file = QFileDialog()
        file.setFileMode(QFileDialog.FileMode.ExistingFile)
        file.setNameFilter(dialog_filter)
        file.setDirectory(load_setting("Paths", f"load_{save_id}", paths.lastLoadedDir))
        if file.exec():
            save_setting("Paths", f"load_{save_id}", str(Path(file.selectedFiles()[0]).parent))
            return file.selectedFiles()[0]
    except Exception as e:
        print(e)

    return ""
