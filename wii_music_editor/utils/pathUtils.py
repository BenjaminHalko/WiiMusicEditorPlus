import os
from pathlib import Path, PosixPath
import subprocess
import sys

from wii_music_editor.utils.osUtils import currentSystem, choose_from_os, SystemType
from wii_music_editor.utils.save import save_setting, load_setting, savePath


class Paths:
    save: Path = None
    program: Path = None
    full: Path = None
    include: Path = None
    includeAll: Path = None
    module: Path = None
    translation: Path = None
    lastLoadedDir: Path = None
    lastLoadedSubDir: Path = None

    dolphin: Path = None
    dolphinSave: Path = None

    def __init__(self):
        # System
        self.save = Path(savePath)
        if getattr(sys, 'frozen', False):
            if currentSystem == SystemType.Mac:
                self.program = PosixPath(sys.executable).parent.parent.parent.parent
                self.full = PosixPath(sys.executable).parent.parent.parent
                self.include = self.full / "Contents" / "Resources" / "app" / "include"
                self.includeAll = self.include
            else:
                self.program = Path(sys.executable).parent
                self.full = Path(sys.executable)
                self.include = Path(sys._MEIPASS) / "include"
                print(self.include)
                self.includeAll = self.include
            self.translation = Path(sys._MEIPASS) / "translations"
        else:
            self.program = Path(__file__).parent.parent.parent
            self.include = self.program / "include" / currentSystem.name.lower()
            self.includeAll = self.program / "include" / "all"
            self.translation = self.program / "translations" / "translations"

        # Dolphin
        tempDolphinPath = load_setting("Paths", "Dolphin", "")
        self.dolphin = Path(tempDolphinPath) if tempDolphinPath != "" else None
        if currentSystem == SystemType.Linux and self.dolphin is None:
            temp = subprocess.check_output("whereis dolphin-emu", shell=True).decode()
            if os.path.exists(temp[13:len(temp) - 1:1]):
                self.dolphin = Path(temp[13:len(temp) - 1:1])
                save_setting("Paths", "Dolphin", str(self.dolphin))

        # Dolphin Save Path
        self.setDolphinSavePath(load_setting("Paths", "DolphinSave", ""))

        # Last Loaded Path
        self.lastLoaded = Path(load_setting("Paths", "LastLoadedDir", str(self.program)))
        self.lastLoadedSubDir = Path(load_setting("Paths", "LastLoadedSubDir", str(self.program)))

    def setDolphinSavePath(self, dolphin_save_path: str):
        if os.path.isdir(dolphin_save_path):
            self.dolphinSave = Path(dolphin_save_path)
        elif self.dolphin is not None and (self.dolphin.parent / "portable.txt").exists() and currentSystem == "Windows":
            self.dolphinSave = self.dolphin.parent / "User"
        else:
            self.dolphinSave = Path(choose_from_os([
                os.path.expanduser('~/Documents/Dolphin Emulator'),
                os.path.expanduser('~/Library/Application Support/Dolphin'),
                os.path.expanduser('~/.local/share/dolphin-emu')
            ]))


paths = Paths()
