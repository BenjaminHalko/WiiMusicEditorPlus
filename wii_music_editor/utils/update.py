from pypi_latest import PypiLatest

from wii_music_editor.version import version_info


def CheckForUpdate() -> bool:
    try:
        return PypiLatest("wii-music-editor", version_info).check_latest()
    except Exception as e:
        print("Could Not Check For Update:", e)
        return False


def UpdateEditor() -> bool:
    try:
        PypiLatest("wii-music-editor", version_info).upgrade()
        return True
    except Exception as e:
        print("Could Not Update:", e)
    return False
