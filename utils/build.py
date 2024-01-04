from os import path
import platform
from pathlib import Path
import PyInstaller.__main__


def build():
    system = platform.system()
    app_dir = Path(__file__).parent.parent

    args = [
        str(app_dir/'app.py'),
        '--noconfirm',
        '--add-data', f'{path.join("translations", "translations")}:translations',
        '--add-data', f'{path.join("crossplatformhelpers", system, "Helper")}:Helper',
        f'--icon={app_dir/"wii_music_editor"/"res"/"icon"/"icon.ico"}'
    ]

    if system != 'Mac':
        args.append('-w')

    if system == 'Linux':
        args.append('-F')

    PyInstaller.__main__.run(args)
