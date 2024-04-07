import json
import urllib.request

from wii_music_editor.utils.logger import is_debug


def GetVersionNumber(version: str) -> int:
    version = version.replace("dev", "").split(".")
    version_number = 0
    for i in range(len(version)):
        version_number += int(version[i]) * (100 ** (3 - i))
    return version_number


def GetLatestVersion() -> str:
    req = urllib.request.Request(f"https://pypi.org/pypi/wii-music-editor/json")
    with urllib.request.urlopen(req, timeout=1) as response:
        contents = response.read()
        data = json.loads(contents)
        latest_pypi_version = data["info"]["version"]
        return latest_pypi_version


def CheckForUpdate(local_version: str = "", latest_version: str = "") -> bool:
    return not is_debug() and GetVersionNumber(local_version) < GetVersionNumber(latest_version)
