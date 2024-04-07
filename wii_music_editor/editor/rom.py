import os
from pathlib import Path

from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.utils.save import save_setting
from wii_music_editor.utils.shell import run_shell


def ConvertRom(rom_path: Path) -> Path or None:
    folder_path = Path(os.path.splitext(str(rom_path))[0])
    run_shell([paths.include / 'wiimms' / 'wit', 'cp', '--fst', rom_path, folder_path])

    if (folder_path / 'DATA').is_dir():
        folder_path = folder_path / 'DATA'
    save_setting("Paths", "CurrentLoadedFile", str(folder_path))
    return folder_path
