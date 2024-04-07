import importlib_metadata


def GetCurrentVersion() -> str:
    try:
        return str(importlib_metadata.version("wii_music_editor"))
    except importlib_metadata.PackageNotFoundError:
        pass
    return ""
