import os
from pathlib import Path

from wii_music_editor.editor import loaded_file
from wii_music_editor.editor.gecko import CreateGct
from wii_music_editor.ui.views.error_handler.error_handler import ShowError
from wii_music_editor.utils import paths
from wii_music_editor.utils.save import save_setting
from wii_music_editor.utils.shell import run_shell


def ConvertRom():
    print("Converting Rom")
    try:
        folder_path = os.path.splitext(str(paths.loadedFilePath))[0]
        run_shell([str(paths.includePath / 'Wiimms' / 'wit'), 'cp', '--fst', str(paths.loadedFilePath), folder_path])

        if (Path(folder_path) / 'DATA').is_dir():
            paths.loadedFilePath = Path(folder_path) / 'DATA'
        else:
            paths.loadedFilePath = Path(folder_path)
        save_setting("Paths", "CurrentLoadedFile", str(paths.loadedFilePath))
        paths.setLoadedFilePath()
        loaded_file.loadedFileType = loaded_file.LoadType.Rom
    except Exception as e:
        ShowError("Could not extract rom", str(e))
