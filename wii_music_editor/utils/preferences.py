class Preferences:
    unsafe_mode: bool
    separate_tracks: bool

    def __init__(self):
        self.separate_tracks = False
        self.unsafe_mode = False


preferences = Preferences()
