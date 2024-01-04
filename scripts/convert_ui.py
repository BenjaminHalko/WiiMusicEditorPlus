import os
from pathlib import Path
from PyQt6.uic import pyuic


def convert():
    root_dir = (Path(__file__).parent / "..").resolve()
    files = os.listdir(root_dir / "ui")
    for file in files:
        print(f'Converting {file}')
        file_name = Path(file).stem
        pyuic.generate(
            root_dir / 'ui' / file, root_dir / 'wii_music_editor' / 'ui' / 'views' / file_name / f'{file_name}_ui.py',
            execute=True, indent=4, max_workers=1)
