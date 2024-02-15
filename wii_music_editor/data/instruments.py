from wii_music_editor.ui.widgets.translate import tr


class InstrumentClass:
    def __init__(self, name, number, in_menu):
        self.name = name
        self.number = number
        self.in_menu = in_menu


instrumentList = [
    InstrumentClass('Piano', 0, True),
    InstrumentClass('Marimba', 1, False),
    InstrumentClass('Vibraphone', 2, False),
    InstrumentClass('Steel Drum', 3, False),
    InstrumentClass('Dulcimer', 4, False),
    InstrumentClass('Handbell', 5, False),
    InstrumentClass('Harpsichord', 6, False),
    InstrumentClass('Timpani', 7, False),
    InstrumentClass('Galactic Piano', 8, False),
    InstrumentClass('Toy Piano', 9, False),
    InstrumentClass('Dog', 10, False),
    InstrumentClass('Cat', 11, False),
    InstrumentClass('Rapper', 12, False),
    InstrumentClass('Guitar', 13, False),
    InstrumentClass('Electric Guitar', 14, False),
    InstrumentClass('Electric Bass', 15, True),
    InstrumentClass('Double Bass', 16, False),
    InstrumentClass('Ukulele', 17, False),
    InstrumentClass('Banjo', 18, False),
    InstrumentClass('Sitar', 19, False),
    InstrumentClass('Shamisen', 20, True),
    InstrumentClass('Harp', 21, False),
    InstrumentClass('Galactic Guitar', 22, False),
    InstrumentClass('Galactic Bass', 23, True),
    InstrumentClass('Jaw Harp', 24, False),
    InstrumentClass('Violin', 25, True),
    InstrumentClass('Cello', 26, False),
    InstrumentClass('Trumpet', 27, True),
    InstrumentClass('Saxophone', 28, True),
    InstrumentClass('Flute', 29, True),
    InstrumentClass('Clairenet', 30, True),
    InstrumentClass('Tuba', 31, False),
    InstrumentClass('Accordion', 32, False),
    InstrumentClass('Harmonica', 33, False),
    InstrumentClass('Bagpipe', 34, False),
    InstrumentClass('Recorder', 35, False),
    InstrumentClass('Galactic horn', 36, False),
    InstrumentClass('Nes', 37, False),
    InstrumentClass('Singer', 38, True),
    InstrumentClass('Bass Singer', 39, True),
    InstrumentClass('Basic Drums', 40, True),
    InstrumentClass('Rock Drums', 41, False),
    InstrumentClass('Jazz Drums', 42, False),
    InstrumentClass('Latin Drums', 43, False),
    InstrumentClass('Ballad Drums', 44, False),
    InstrumentClass('Congas', 45, False),
    InstrumentClass('Maracas', 46, False),
    InstrumentClass('Tambourine', 47, False),
    InstrumentClass('Cuica', 48, False),
    InstrumentClass('Cowbell', 49, False),
    InstrumentClass('Clap', 50, False),
    InstrumentClass('Bells', 51, False),
    InstrumentClass('Castanets', 52, False),
    InstrumentClass('Guiro', 53, False),
    InstrumentClass('Timpales', 54, False),
    InstrumentClass('Djembe', 55, False),
    InstrumentClass('Taiko Drum', 56, True),
    InstrumentClass('Cheerleader', 57, False),
    InstrumentClass('Snare Drum', 58, True),
    InstrumentClass('Bass Drum', 59, False),
    InstrumentClass('Galactic Drums', 60, False),
    InstrumentClass('Galactic Congas', 61, False),
    InstrumentClass('DJ Turntables', 62, True),
    InstrumentClass('Black Belt', 63, False),
    InstrumentClass('Reggae Drums', 64, False),
    InstrumentClass('Whistle', 65, False),
    InstrumentClass('Beatbox', 66, True),
    InstrumentClass('None', -1, False)
]
