import os
from pathlib import Path

from wii_music_editor.editor import openData
from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.utils.save import save_setting
from wii_music_editor.utils.shell import run_shell


def ConvertRom():
    print("Converting Rom")
    try:
        folder_path = os.path.splitext(str(paths.loadedFile))[0]
        run_shell([str(paths.includePath / 'Wiimms' / 'wit'), 'cp', '--fst', str(paths.loadedFile), folder_path])

        if (Path(folder_path) / 'DATA').is_dir():
            paths.loadedFile = Path(folder_path) / 'DATA'
        else:
            paths.loadedFile = Path(folder_path)
        save_setting("Paths", "CurrentLoadedFile", str(paths.loadedFile))
        paths.setLoadedFilePath()
        loaded_file.loadedType = loaded_file.LoadType.Rom
    except Exception as e:
        ShowError("Could not extract rom", str(e))
