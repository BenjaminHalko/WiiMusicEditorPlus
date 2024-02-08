from wii_music_editor.utils.translate import tr


class InstrumentClass:
    def __init__(self, Name, Number, InMenu, NumberOfSounds=[]):
        self.Name = Name
        self.Number = Number
        self.InMenu = InMenu
        self.NumberOfSounds = NumberOfSounds


def get_instruments():
    return [
        InstrumentClass(tr("Editor", 'Piano'), 0, True,
                        ["C2", "G2", "D3", "A3", "E4", "B4", "F#5", "D6", "F6"]),
        InstrumentClass(tr("Editor", 'Marimba'), 1, False,
                        ["G3", "D4", "A4", "E5", "B5", "F#6"]),
        InstrumentClass(tr("Editor", 'Vibraphone'), 2, False,
                        ["F#3", "C#4", "G#4", "D#5", "A#5", "F6"]),
        InstrumentClass(tr("Editor", 'Steel Drum'), 3, False,
                        ["F#2", "A#3", "F#4", "G4", "E4", "??(26)", "C4"]),
        InstrumentClass(tr("Editor", 'Dulcimer'), 4, False,
                        ["F3", "C#4", "G4", "C5", "A6", "D6"]),
        InstrumentClass(tr("Editor", 'Handbell'), 5, False,
                        ["G4", "G4 (Variation)", "G4 (Variation 2)", "C7"]),
        InstrumentClass(tr("Editor", 'Harpsichord'), 6, False,
                        ["G2", "C4", "C5", "C6"]),
        InstrumentClass(tr("Editor", 'Timpani'), 7, False, ["F3", "F3 (Variation)", "F3 (Variation 2)"]),
        InstrumentClass(tr("Editor", 'Galactic Piano'), 8, False, ["G2", "D3", "A3", "E4", "B4", "F#5"]),
        InstrumentClass(tr("Editor", 'Toy Piano'), 9, False, ["B4", "D6"]),
        InstrumentClass(tr("Editor", 'Dog'), 10, False,
                        ["Howl", "??(54)", "??(55)", "??(54)", "D5", "G5", "C#6"]),
        InstrumentClass(tr("Editor", 'Cat'), 11, False, ["G3", "C#4", "G4", "C#5", "G5", "C#6"]),
        InstrumentClass(tr("Editor", 'Rapper'), 12, False, ["??"] * 62),
        InstrumentClass(tr("Editor", 'Guitar'), 13, False, ["G#2", "E3", "B3", "F#4", "D5", "??(133)"]),
        InstrumentClass(tr("Editor", 'Electric Guitar'), 14, False, ["A2", "D3", "B3", "G4", "E5", "A5"]),
        InstrumentClass(tr("Editor", 'Electric Bass'), 15, True, ["G1", "D2", "G2", "C3", "G#3"]),
        InstrumentClass(tr("Editor", 'Double Bass'), 16, False, ["F1", "G#1", "G#2", "G#3"]),
        InstrumentClass(tr("Editor", 'Ukulele'), 17, False, ["B3", "F#4", "C#5", "G#5"]),
        InstrumentClass(tr("Editor", 'Banjo'), 18, False, ["A#2", "F3", "C4", "G4", "D5", "A5"]),
        InstrumentClass(tr("Editor", 'Sitar'), 19, False, ["C3", "G3", "C4", "G4"]),
        InstrumentClass(tr("Editor", 'Shamisen'), 20, True, ["D3", "A3", "D4", "A4"]),
        InstrumentClass(tr("Editor", 'Harp'), 21, False, ["C3", "C4", "E5", "B5", "G6"]),
        InstrumentClass(tr("Editor", 'Galactic Guitar'), 22, False, ["F2", "C3", "F3", "C4", "F4", "C5", "F5"]),
        InstrumentClass(tr("Editor", 'Galactic Bass'), 23, True, ["A1", "C2", "F2", "A2", "C3"]),
        InstrumentClass(tr("Editor", 'Jaw Harp'), 24, False, ["??(184)", "??(185)", "??(186)", "??(187)"]),
        InstrumentClass(tr("Editor", 'Violin'), 25, True, ["C4", "A4", "E5", "B5", "F#6"]),
        InstrumentClass(tr("Editor", 'Cello'), 26, False, ["A2", "D3", "A3", "E4", "B4"]),
        InstrumentClass(tr("Editor", 'Trumpet'), 27, True,
                        ["F#2", "G#3", "A3", "D4", "G4", "C5", "F5", "Bb5", "G6"]),
        InstrumentClass(tr("Editor", 'Saxophone'), 28, True,
                        ["F2", "B2", "F3", "E4", "Bb4", "E5", "Bb5", "E6"]),
        InstrumentClass(tr("Editor", 'Flute'), 29, True, ["D4", "G4", "C5", "G5", "D6", "G6", "D7"]),
        InstrumentClass(tr("Editor", 'Clairenet'), 30, True, ["Bb2", "F3", "C4", "F4", "C5", "F5", "C6"]),
        InstrumentClass(tr("Editor", 'Tuba'), 31, False, ["??(229)", "Eb2", "Bb2", "A3"]),
        InstrumentClass(tr("Editor", 'Accordion'), 32, False, ["B2", "C4"]),
        InstrumentClass(tr("Editor", 'Harmonica'), 33, False, ["B4", "A3", "E4", "D5", "B5", "A6"]),
        InstrumentClass(tr("Editor", 'Bagpipe'), 34, False, ["C4", "F#4", "C5", "F#5"]),
        InstrumentClass(tr("Editor", 'Recorder'), 35, False, ["G6"]),
        InstrumentClass(tr("Editor", 'Galactic horn'), 36, False, ["G2", "C4", "C5"]),
        InstrumentClass(tr("Editor", 'Nes'), 37, False, ["Mario Jump", "C3", "F3", "Bb3", "G4", "C5", "C6"]),
        InstrumentClass(tr("Editor", 'Singer'), 38, True,
                        ["C4 (Wii)", "G4 (Wii)", "C5 (Wii)", "G5 (Wii)", "C4 (Do)", "F#4 (Do)", "D5 (Do)", "F#5 (Do)",
                         "C4 (Ba)", "G4 (Ba)", "C5 (Ba)", "G5 (Ba)"]),
        InstrumentClass(tr("Editor", 'Bass Singer'), 39, True,
                        ["D3 (Wii)", "G3 (Wii)", "C4 (Wii)", "G4 (Wii)", "C3 (Do)", "G3 (Do)", "C4 (Do)", "G4 (Do)",
                         "D3 (Ba)", "A3 (Ba)", "D4 (Ba)", "G4 (Ba)"]),
        InstrumentClass(tr("Editor", 'Basic Drums'), 40, True),
        InstrumentClass(tr("Editor", 'Rock Drums'), 41, False),
        InstrumentClass(tr("Editor", 'Jazz Drums'), 42, False),
        InstrumentClass(tr("Editor", 'Latin Drums'), 43, False),
        InstrumentClass(tr("Editor", 'Ballad Drums'), 44, False),
        InstrumentClass(tr("Editor", 'Congas'), 45, False),
        InstrumentClass(tr("Editor", 'Maracas'), 46, False),
        InstrumentClass(tr("Editor", 'Tambourine'), 47, False),
        InstrumentClass(tr("Editor", 'Cuica'), 48, False),
        InstrumentClass(tr("Editor", 'Cowbell'), 49, False),
        InstrumentClass(tr("Editor", 'Clap'), 50, False),
        InstrumentClass(tr("Editor", 'Bells'), 51, False),
        InstrumentClass(tr("Editor", 'Castanets'), 52, False),
        InstrumentClass(tr("Editor", 'Guiro'), 53, False),
        InstrumentClass(tr("Editor", 'Timpales'), 54, False),
        InstrumentClass(tr("Editor", 'Djembe'), 55, False),
        InstrumentClass(tr("Editor", 'Taiko Drum'), 56, True),
        InstrumentClass(tr("Editor", 'Cheerleader'), 57, False),
        InstrumentClass(tr("Editor", 'Snare Drum'), 58, True),
        InstrumentClass(tr("Editor", 'Bass Drum'), 59, False),
        InstrumentClass(tr("Editor", 'Galactic Drums'), 60, False),
        InstrumentClass(tr("Editor", 'Galactic Congas'), 61, False),
        InstrumentClass(tr("Editor", 'DJ Turntables'), 62, True),
        InstrumentClass(tr("Editor", 'Black Belt'), 63, False),
        InstrumentClass(tr("Editor", 'Reggae Drums'), 64, False),
        InstrumentClass(tr("Editor", 'Whistle'), 65, False),
        InstrumentClass(tr("Editor", 'Beatbox'), 66, True),
        InstrumentClass(tr("Editor", 'None'), -1, False)]


instrumentList = get_instruments()