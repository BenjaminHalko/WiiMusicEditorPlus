import os
from pathlib import Path, PosixPath
import subprocess
import sys
from wii_music_editor.utils.helper.osUtils import currentSystem, choose_from_os
from wii_music_editor.utils.helper.save import save_setting, load_setting


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
        helperPath = os.path.join(fullPath, "Contents", "Resources", "app", "Helper")
        resPath = os.path.join(fullPath, "Contents", "Resources", "app", "res")
    else:
        programPath = os.path.dirname(sys.executable)
        fullPath = sys.executable
        helperPath = Path(sys._MEIPASS) / "Helper"
        modulePath = Path(sys._MEIPASS) / "wii_music_editor"
    translationPath = Path(sys._MEIPASS) / "translations"
else:
    programPath = Path(__file__).parent.parent.parent.parent
    fullPath = "NULL"
    helperPath = programPath / "crossplatformhelpers" / currentSystem / "Helper"
    translationPath = programPath / "translations" / "translations"
    modulePath = programPath / "wii_music_editor"

# Save
savePath = choose_from_os([
        os.path.expanduser('~/AppData/Local/WiiMusicEditorPlus'),
        os.path.expanduser('~/Library/Application Support/WiiMusicEditorPlus'),
        os.path.expanduser('~/.local/share/WiiMusicEditorPlus')
    ])
if not os.path.isdir(savePath):
    os.mkdir(savePath)

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
romPath = load_setting("Paths", "CurrentLoadedFile", "")

# Last Loaded Path
print(programPath)
lastLoadedPath = load_setting("Paths", "LastLoadedPath", programPath)
