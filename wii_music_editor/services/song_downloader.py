from os import remove
from zipfile import ZipFile

import requests
from PyQt6.QtCore import QThread, pyqtSignal

from wii_music_editor.utils.paths import paths
from wii_music_editor.utils.save import savePath


class DownloadSongThread(QThread):
    progress = pyqtSignal(str)
    done = pyqtSignal()

    def run(self):
        file = open(f"{savePath}/downloaded.zip", "wb")
        file.write(
            requests.get("https://github.com/BenjaminHalko/Pre-Made-Songs-for-Wii-Music/archive/refs/heads/main.zip")
            .content)
        file.close()
        zip_file = ZipFile(f"{savePath}/downloaded.zip")
        for zip_info in zip_file.infolist():
            if zip_info.filename[-1] == '/':
                continue
            zip_info.filename = zip_info.filename.replace("Pre-Made-Songs-for-Wii-Music-main/", "")
            zip_file.extract(zip_info, f"{paths.programPath}/Pre-Made Songs for Wii Music")
        zip_file.close()
        remove(f"{savePath}/downloaded.zip")
        self.done.emit()
