import logging
import os
import subprocess
import stat

from wii_music_editor.utils.osUtils import currentSystem, SystemType


def give_permission(file: str):
    if currentSystem != SystemType.Windows:
        try:
            os.chmod(file, os.stat(file).st_mode | stat.S_IEXEC)
        except Exception as e:
            print("Error giving permission to file:", file, "\nError:", e)


def run_shell(command: list[str] or str, logging_level: int = logging.INFO):
    try:
        if type(command) is not str:
            give_permission(command[0])
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with process.stdout:
            try:
                for line in iter(process.stdout.readline, b''):
                    logging.log(logging_level, line.decode().strip())
            except subprocess.CalledProcessError as e:
                logging.error(f"{e}")
        process.wait()
    except Exception as e:
        logging.error(f"Error running shell command: {command}\nError: {e}")
