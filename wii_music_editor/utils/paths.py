import os
from pathlib import Path, PosixPath
import subprocess
import sys

from wii_music_editor.utils.osUtils import currentSystem, choose_from_os
from wii_music_editor.utils.region import BasedOnRegion, romLanguage
from wii_music_editor.utils.save import save_setting, load_setting


def setLoadedFilePath(loaded_file_path):
    global romPath, mainDolPath, brsarPath, messagePath, geckoPath

    romPath = None
    mainDolPath = None
    brsarPath = None
    messagePath = None
    geckoPath = None

    if os.path.isdir(loaded_file_path):
        romPath = loaded_file_path
        mainDolPath = Path(loaded_file_path)/"sys"/"main.dol"
        brsarPath = Path(loaded_file_path)/"files"/"Sound"/"MusicStatic"/"rp_Music_sound.brsar"
        messagePath = Path(loaded_file_path)/"files"/BasedOnRegion(romLanguage)/"Message"
        geckoPath = Path(loaded_file_path)/"GeckoCodes.ini"
    else:
        # TODO: Add support for loading from a non folder
        temp = 0


def setDolphinSavePath(dolphin_save_path):
    global dolphinSavePath, dolphinPath
    if os.path.isdir(dolphin_save_path):
        dolphinSavePath = dolphin_save_path
    elif (os.path.exists(os.path.join(os.path.dirname(dolphinPath), "portable.txt"))
          and currentSystem == "Windows"):
        dolphinSavePath = os.path.join(os.path.dirname(dolphinPath), "portable.txt")
    else:
        dolphinSavePath = choose_from_os([
            os.path.expanduser('~/Documents/Dolphin Emulator'),
            os.path.expanduser('~/Library/Application Support/Dolphin'),
            os.path.expanduser('~/.local/share/dolphin-emu')
        ])


# System
if getattr(sys, 'frozen', False):
    if currentSystem == "Mac":
        programPath = os.path.dirname(
            PosixPath(os.path.dirname(sys.executable)).parent.parent.parent)
        fullPath = os.path.dirname(PosixPath(os.path.dirname(sys.executable)).parent.parent)
        includePath = os.path.join(fullPath, "Contents", "Resources", "app", "include")
        includeAllPath = includePath
        resPath = os.path.join(fullPath, "Contents", "Resources", "app", "res")
    else:
        programPath = os.path.dirname(sys.executable)
        fullPath = sys.executable
        includePath = Path(sys._MEIPASS) / "include"
        includeAllPath = includePath
        modulePath = Path(sys._MEIPASS) / "wii_music_editor"
    translationPath = Path(sys._MEIPASS) / "translations"
else:
    programPath = Path(__file__).parent.parent.parent.parent
    fullPath = "NULL"
    includePath = programPath / "include" / currentSystem
    includeAllPath = programPath / "include" / "all"
    translationPath = programPath / "translations" / "translations"
    modulePath = programPath / "wii_music_editor"



# Dolphin
dolphinPath = load_setting("Paths", "Dolphin", "")
if currentSystem == "Linux" and not os.path.isfile(dolphinPath):
    temp = subprocess.check_output("whereis dolphin-emu", shell=True).decode()
    if os.path.exists(temp[13:len(temp) - 1:1]):
        dolphinPath = temp[13:len(temp) - 1:1]
        save_setting("Paths", "Dolphin", dolphinPath)

# Dolphin Save Path
dolphinSavePath = None
setDolphinSavePath(load_setting("Paths", "DolphinSave", ""))

# Loaded Rom
romPath = None
mainDolPath = None
brsarPath = None
messagePath = None
geckoPath = None
setLoadedFilePath(load_setting("Paths", "CurrentLoadedFile", ""))

# Last Loaded Path
lastLoadedPath = load_setting("Paths", "LastLoadedPath", programPath)
