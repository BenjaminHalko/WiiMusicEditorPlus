class Preferences:
    unsafe_mode: bool
    separate_tracks: bool
    normalize_midi: bool
    rapper_crash_fix: bool
    copy_gecko_codes: bool

    def __init__(self):
        self.separate_tracks = False
        self.unsafe_mode = False
        self.normalize_midi = False
        self.rapper_crash_fix = True
        self.copy_gecko_codes = True


preferences = Preferences()
