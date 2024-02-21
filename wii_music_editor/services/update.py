import os
from pathlib import Path
from shutil import rmtree
from zipfile import ZipFile

import requests
from PySide6.QtCore import QThread, Signal

from wii_music_editor.utils.osUtils import currentSystem
from wii_music_editor.utils.save import load_setting, savePath
from wii_music_editor.utils.shell import run_shell


class UpdateProgress:
    def update(self, op_code, cur_count, max_count=None, message=''):
        if op_code > 10:
            UpdateThread.progress.emit(cur_count / max_count * 100)


class DownloadUpdate(QThread):
    progress = Signal(int)
    done = Signal()
    version = "null"

    def run(self):
        file = open(f"{savePath}/downloaded.zip", "wb")
        with requests.get(
                f"https://github.com/BenjaminHalko/WiiMusicEditorPlus/releases/download/{self.version}/WiiMusicEditorPlus-{currentSystem}.zip",
                stream=True) as response:
            total = int(response.headers['content-length'])
            downloaded = 0
            for i in response.iter_content(1024):
                downloaded += len(i)
                file.write(i)
                UpdateThread.progress.emit(downloaded / total * 100)

        file.close()

        if currentSystem == "Linux":
            if Path(f"{savePath}/WiiMusicEditorPlus").exists():
                os.remove(f"{savePath}/WiiMusicEditorPlus")
            zip_file = ZipFile(f"{savePath}/downloaded.zip")
            zip_file.extractall(savePath)
            zip_file.close()
        elif currentSystem == "Mac":
            if Path(f"{savePath}/WiiMusicEditorPlus.app").exists():
                rmtree(f"{savePath}/WiiMusicEditorPlus.app")
            zip_file = ZipFile(f"{savePath}/downloaded.zip")
            for file in zip_file.infolist():
                zip_file.extract(file, savePath)
                run_shell(["chmod", "u+x", f"{savePath}/{file.filename}"])
            zip_file.close()

        if currentSystem != "Windows":
            os.remove(f"{savePath}/downloaded.zip")
        UpdateThread.done.emit()


def CheckForUpdate():
    try:
        tag = GetReleaseTag()
        if tag != version:
            return tag
        else:
            return "null"
    except (ConnectionError, requests.Timeout):
        return "null"


def GetReleaseTag():
    data = requests.get("https://api.github.com/repos/BenjaminHalko/WiiMusicEditorPlus/releases").json()
    i = 0
    try:
        if not load_setting("Settings", "Beta", False):
            while data[i]["prerelease"]:
                i += 1
        else:
            looking = True
            i = -1
            while looking:
                i += 1
                for j in data[i]["assets"]:
                    if j["name"] == f"WiiMusicEditorPlus-{currentSystem}.zip":
                        looking = False
                        break
    except Exception as e:
        i = 0
        print("Error getting release tag:", e)
    return data[i]["tag_name"]


UpdateThread = DownloadUpdate()
