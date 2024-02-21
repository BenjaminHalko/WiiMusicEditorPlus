from wii_music_editor.data.region import LanguageType


class Preferences:
    unsafe_mode: bool
    separate_tracks: bool
    normalize_midi: bool
    rapper_crash_fix: bool
    language: int
    auto_update: bool

    def __init__(self):
        self.separate_tracks = False
        self.unsafe_mode = False
        self.normalize_midi = False
        self.rapper_crash_fix = True
        self.language = LanguageType.English
        self.auto_update = True


preferences = Preferences()
