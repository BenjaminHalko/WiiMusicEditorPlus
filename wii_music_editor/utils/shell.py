import os
import subprocess
import stat

from wii_music_editor.ui.views.error_handler.error_handler import ShowError
from wii_music_editor.utils.osUtils import currentSystem


def give_permission(file):
    if currentSystem != "Windows":
        try:
            os.chmod(file, os.stat(file).st_mode | stat.S_IEXEC)
        except Exception as e:
            print("Error giving permission to file:", file, "\nError:", e)


def run_shell(command):
    try:
        if type(command) is str:
            give_permission(command[0])
        if currentSystem == "Windows":
            create_no_window = 0x08000000
            subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                           creationflags=create_no_window)
        else:
            subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        ShowError(f"Could not execute command:", f"Command: {command}\nError: {e}")
