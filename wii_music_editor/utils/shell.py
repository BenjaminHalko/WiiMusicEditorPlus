import os
import subprocess
import stat

from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.utils.osUtils import currentSystem, SystemType


def give_permission(file: str):
    if currentSystem != SystemType.Windows:
        try:
            os.chmod(file, os.stat(file).st_mode | stat.S_IEXEC)
        except Exception as e:
            print("Error giving permission to file:", file, "\nError:", e)


def run_shell(command: list[str] or str):
    try:
        if type(command) is not str:
            give_permission(command[0])
        if currentSystem == SystemType.Windows:
            subprocess.run(command)
        else:
            subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        ShowError(f"Could not execute command:", f"Command: {command}\nError: {e}")
