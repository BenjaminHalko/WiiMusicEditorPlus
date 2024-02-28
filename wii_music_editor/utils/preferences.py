from wii_music_editor.data.region import LanguageType
from wii_music_editor.utils.save import load_setting, save_setting


class Preferences:
    unsafe_mode: bool
    separate_tracks: bool
    normalize_midi: bool
    rapper_crash_fix: bool
    rom_language: int
    ui_language: int
    auto_update: bool
    using_discord: bool

    def __init__(self):
        self.__load("unsafe_mode", False)
        self.__load("separate_tracks", False)
        self.__load("normalize_midi", False)
        self.__load("rapper_crash_fix", True)
        self.__load("rom_language", LanguageType.English)
        self.__load("ui_language", LanguageType.English)
        self.__load("auto_update", True)
        self.__load("using_discord", True)

    def __load(self, setting: str, default: int or bool):
        setattr(self, setting, load_setting("preferences", setting, default))

    def __setitem__(self, key, value):
        setattr(self, key, value)
        save_setting("preferences", key, value)
        print("saved")


preferences = Preferences()
