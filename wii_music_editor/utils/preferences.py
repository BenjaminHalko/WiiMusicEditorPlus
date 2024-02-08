class Preferences:
    unsafe_mode: bool
    separate_tracks: bool
    normalize_midi: bool
    rapper_crash_fix: bool

    def __init__(self):
        self.separate_tracks = False
        self.unsafe_mode = False
        self.normalize_midi = False
        self.rapper_crash_fix = True


preferences = Preferences()
