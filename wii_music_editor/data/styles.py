from enum import Enum


class StyleNames:
    default = ("Default", "Par défaut", "Predeterm.", "Standard", "Normale", "オリジナル", "오리지널")
    rock = ("Rock", "Rock", "Rock", "Rock", "Rock", "ロック", "록")
    march = ("March", "Marche", "Marcha", "Marsch", "Marcia", "マーチ", "행진곡")
    jazz = ("Jazz", "Jazz", "Jazz", "Jazz", "Jazz", "ジャズ", "재즈")
    latin = ("Latin", "Latino", "Latino", "Latin", "Latino", "ラテン", "라틴 음악")
    reggae = ("Reggae", "Reggae", "Reggae", "Reggae", "Reggae", "レゲエ", "레게")
    hawaiian = ("Hawaiian", "Hawaïen", "Hawaiano", "Hawaii", "Hawaiano", "ハワイ風", "하와이 음악")
    electronic = ("Electronic", "Électronique", "Electrónico", "Elektronik", "Elettronico", "ダウンビート", "전자 음악")
    classical = ("Classical", "Classique", "Clásico", "Klassisch", "Classico", "室内楽", "실내악")
    tango = ("Tango", "Tango", "Tango", "Tango", "Tango", "タンゴ", "탱고")
    pop = ("Pop", "Pop", "Pop", "Pop", "Pop", "ポップス", "팝")
    japanese = ("Japanese", "Japonais", "Japonés", "Japanisch", "Giapponese", "和風", "일본 음악")


class StyleType(Enum):
    Global = 0
    QuickJam = 1
    SongSpecific = 2
    Menu = 3
    Unused = 4


class StyleInstruments:
    melody: int
    harmony: int
    chord: int
    bass: int
    perc1: int
    perc2: int

    def __init__(self, melody: int, harmony: int, chord: int, bass: int, perc1: int, perc2: int):
        self.melody = melody
        self.harmony = harmony
        self.chord = chord
        self.bass = bass
        self.perc1 = perc1
        self.perc2 = perc2

    def __eq__(self, other) -> bool:
        return (
                self.melody == other.melody and
                self.harmony == other.harmony and
                self.chord == other.chord and
                self.bass == other.bass and
                self.perc1 == other.perc1 and
                self.perc2 == other.perc2
        )

    def __setitem__(self, key, value):
        if key == 0:
            self.melody = value
        elif key == 1:
            self.harmony = value
        elif key == 2:
            self.chord = value
        elif key == 3:
            self.bass = value
        elif key == 4:
            self.perc1 = value
        elif key == 5:
            self.perc2 = value
        else:
            raise IndexError("Index out of range")

    def __getitem__(self, item):
        if item == 0:
            return self.melody
        elif item == 1:
            return self.harmony
        elif item == 2:
            return self.chord
        elif item == 3:
            return self.bass
        elif item == 4:
            return self.perc1
        elif item == 5:
            return self.perc2
        else:
            raise IndexError("Index out of range")

    def copy(self) -> 'StyleInstruments':
        return StyleInstruments(self.melody, self.harmony, self.chord, self.bass, self.perc1, self.perc2)


class Style:
    __total_styles = 0
    total_style_types = [0] * len(StyleType)
    style_type: StyleType
    name: str
    style_id: int
    style: StyleInstruments
    list_order: int

    def __init__(self, style_type: StyleType, name, style_id: int,
                 melody: int, harmony: int, chord: int, bass: int, perc1: int, perc2: int):
        self.style_type = style_type
        self.name = name
        self.style_id = style_id
        self.style = StyleInstruments(melody, harmony, chord, bass, perc1, perc2)
        self.list_order = Style.__total_styles
        Style.__total_styles += 1
        Style.total_style_types[style_type.value] += 1


def get_style_by_id(style_id: int) -> Style:
    for style in style_list:
        if style.style_id == style_id:
            return style
    print(f"Style {style_id} not found")
    return style_list[0]


# STYLES START AT MEMORY ADDRESS 0x8059A658
style_list = [
    Style(StyleType.Global, 'Jazz', 0x0,
          0x1C, 0x02, 0x00, 0x10, 0x2A, 0x2D),
    Style(StyleType.Global, 'Rock', 0x1,
          0x0E, 0x0E, 0x24, 0x0F, 0x29, 0x2F),
    Style(StyleType.Global, 'Latin', 0x2,
          0x1B, 0x1C, 0x01, 0x0F, 0x2B, 0x2E),
    Style(StyleType.Global, 'March', 0x3,
          0x1B, 0x1B, 0x1B, 0x1F, 0x3B, 0x3A),
    Style(StyleType.Global, 'Electronic', 0x4,
          0x02, 0x16, 0x08, 0x17, 0x3E, 0x32),
    Style(StyleType.Global, 'Pop', 0x5,
          0x00, 0x02, 0x0D, 0x0F, 0x28, 0x2F),
    Style(StyleType.Global, 'Japanese', 0x6,
          0x1D, 0x43, 0x43, 0x14, 0x38, 0x33),
    Style(StyleType.Global, 'Tango', 0x7,
          0x19, 0x00, 0x20, 0x10, 0x3A, 0x34),
    Style(StyleType.Global, 'Classical', 0x8,
          0x19, 0x19, 0x06, 0x1A, 0x43, 0x43),
    Style(StyleType.Global, 'Hawaiian', 0x9,
          0x11, 0x11, 0x11, 0x10, 0x2E, 0x2D),
    Style(StyleType.Global, 'Reggae', 0xa,
          0x03, 0x03, 0x00, 0x0F, 0x40, 0x43),
    Style(StyleType.QuickJam, 'A Cappella', 0x29,
          0x26, 0x26, 0x27, 0x27, 0x42, 0x32),
    Style(StyleType.QuickJam, 'Acoustic', 0x38,
          0x26, 0x12, 0x0D, 0x0D, 0x2D, 0x2E),
    Style(StyleType.QuickJam, 'African', 0x34,
          0x01, 0x01, 0x01, 0x01, 0x37, 0x2D),
    Style(StyleType.QuickJam, 'Animals!', 0x2b,
          0x0B, 0x0B, 0x10, 0x1F, 0x3B, 0x31),
    Style(StyleType.QuickJam, 'Ballad', 0x33,
          0x1C, 0x00, 0x00, 0x0F, 0x2C, 0x2D),
    Style(StyleType.QuickJam, 'Calypso', 0x2a,
          0x03, 0x03, 0x03, 0x03, 0x43, 0x43),
    Style(StyleType.QuickJam, 'Celtic', 0x0e,
          0x22, 0x22, 0x0D, 0x10, 0x3B, 0x2F),
    Style(StyleType.QuickJam, 'Country', 0x0c,
          0x21, 0x18, 0x12, 0x10, 0x31, 0x2E),
    Style(StyleType.QuickJam, 'Eurobeat', 0x15,
          0x24, 0x0E, 0x16, 0x17, 0x3C, 0x2F),
    Style(StyleType.QuickJam, 'European', 0x22,
          0x1E, 0x19, 0x04, 0x1F, 0x3A, 0x34),
    Style(StyleType.QuickJam, 'Exotic', 0x28,
          0x13, 0x13, 0x04, 0x13, 0x37, 0x43),
    Style(StyleType.QuickJam, 'Flamenco', 0x25,
          0x19, 0x19, 0x0D, 0x0D, 0x34, 0x32),
    Style(StyleType.QuickJam, 'Folk', 0x0f,
          0x23, 0x20, 0x0D, 0x10, 0x3B, 0x2E),
    Style(StyleType.QuickJam, 'French Bistro', 0x11,
          0x20, 0x1E, 0x06, 0x10, 0x35, 0x2F),
    Style(StyleType.QuickJam, 'Funk', 0x44,
          0x1B, 0x1C, 0x16, 0x0F, 0x28, 0x32),
    Style(StyleType.QuickJam, 'Galactic', 0x35,
          0x24, 0x16, 0x08, 0x17, 0x3C, 0x3D),
    Style(StyleType.QuickJam, 'Handbells', 0x43,
          0x05, 0x05, 0x05, 0x05, 0x33, 0x43),
    Style(StyleType.QuickJam, 'Karate', 0x26,
          0x0E, 0x0E, 0x0E, 0x0F, 0x29, 0x3F),
    Style(StyleType.QuickJam, 'NES-Style', 0x2c,
          0x25, 0x25, 0x25, 0x25, 0x43, 0x43),
    Style(StyleType.QuickJam, 'Orchestral', 0x32,
          0x1D, 0x1B, 0x19, 0x07, 0x3A, 0x43),
    Style(StyleType.QuickJam, 'Parade', 0x27,
          0x1B, 0x1E, 0x1B, 0x1F, 0x41, 0x39),
    Style(StyleType.QuickJam, 'Rap', 0x36,
          0x0C, 0x43, 0x08, 0x17, 0x3E, 0x3D),
    Style(StyleType.QuickJam, 'Salsa', 0x42,
          0x1B, 0x01, 0x0D, 0x0F, 0x2D, 0x36),
    Style(StyleType.QuickJam, 'Samba', 0x37,
          0x1D, 0x01, 0x0D, 0x0F, 0x41, 0x30),
    Style(StyleType.QuickJam, 'Soul', 0x14,
          0x1B, 0x1C, 0x08, 0x17, 0x28, 0x32),
    Style(StyleType.QuickJam, 'Soundtrack', 0x13,
          0x00, 0x0D, 0x06, 0x07, 0x3A, 0x2E),
    Style(StyleType.QuickJam, 'Toy', 0x0d,
          0x24, 0x24, 0x09, 0x24, 0x3A, 0x34),
    Style(StyleType.QuickJam, 'Woodwind', 0x1c,
          0x1D, 0x1E, 0x00, 0x06, 0x43, 0x43),
    Style(StyleType.SongSpecific, 'A Little Night Music', 0x21,
          0x1D, 0x19, 0x06, 0x1A, 0x43, 0x43),
    Style(StyleType.SongSpecific, 'Animal Crossing', 0x1b,
          0x20, 0x12, 0x0D, 0x0D, 0x2E, 0x2D),
    Style(StyleType.SongSpecific, 'Animal Crossing K.K. Blues', 0x23,
          0x21, 0x1C, 0x0D, 0x10, 0x2A, 0x35),
    Style(StyleType.SongSpecific, 'Every Breath You Take', 0x12,
          0x21, 0x00, 0x16, 0x0F, 0x28, 0x2F),
    Style(StyleType.SongSpecific, 'From Santurtzi to Bilbao', 0x20,
          0x03, 0x03, 0x03, 0x03, 0x32, 0x2F),
    Style(StyleType.SongSpecific, 'Happy Birthday to You', 0x1e,
          0x1B, 0x1C, 0x00, 0x10, 0x2A, 0x2D),
    Style(StyleType.SongSpecific, 'I\'ll Be There', 0x16,
          0x26, 0x26, 0x27, 0x27, 0x2C, 0x32),
    Style(StyleType.SongSpecific, 'I\'ve Never Been to Me', 0x18,
          0x00, 0x00, 0x0D, 0x0F, 0x28, 0x2E),
    Style(StyleType.SongSpecific, 'La Cucaracha', 0x1f,
          0x1D, 0x01, 0x0D, 0x0F, 0x30, 0x36),
    Style(StyleType.SongSpecific, 'O-Christmas Tree', 0x10,
          0x05, 0x05, 0x05, 0x05, 0x33, 0x43),
    Style(StyleType.SongSpecific, 'The Entertainer', 0x1d,
          0x00, 0x06, 0x00, 0x10, 0x2A, 0x2E),
    Style(StyleType.SongSpecific, 'The Legend of Zelda', 0x19,
          0x1B, 0x19, 0x15, 0x1F, 0x3A, 0x3B),
    Style(StyleType.SongSpecific, 'Twinkle Twinkle Little Star', 0xb,
          0x00, 0x01, 0x0D, 0x10, 0x33, 0x34),
    Style(StyleType.SongSpecific, 'Wii Sports', 0x1a,
          0x1D, 0x00, 0x0D, 0x0F, 0x3C, 0x2F),
    Style(StyleType.SongSpecific, 'Wii Music', 0x24,
          0x19, 0x1C, 0x00, 0x0F, 0x28, 0x32),
    Style(StyleType.SongSpecific, 'Woman', 0x17,
          0x1C, 0x1B, 0x0D, 0x0F, 0x28, 0x31),
    Style(StyleType.Menu, 'Menu Style Main', 0x2d,
          0x19, 0x1C, 0x00, 0x0F, 0x28, 0x28),
    Style(StyleType.Menu, 'Menu Style Electronic', 0x2e,
          0x02, 0x16, 0x00, 0x17, 0x3E, 0x28),
    Style(StyleType.Menu, 'Menu Style Japanese', 0x2f,
          0x1D, 0x14, 0x00, 0x14, 0x38, 0x28),
    Style(StyleType.Menu, 'Menu Style March', 0x30,
          0x1E, 0x1B, 0x00, 0x1F, 0x3A, 0x28),
    Style(StyleType.Menu, 'Menu Style A Capella', 0x31,
          0x26, 0x27, 0x00, 0x27, 0x42, 0x28),
    Style(StyleType.Unused, "Unused 1", 0x39,
          0x1C, 0x1D, 0x1C, 0x1F, 0x43, 0x43),
    Style(StyleType.Unused, "Unused 2", 0x3a,
          0x1F, 0x1B, 0x1D, 0x1D, 0x43, 0x43),
    Style(StyleType.Unused, "Unused 3", 0x3b,
          0x08, 0x08, 0x08, 0x08, 0x43, 0x43),
    Style(StyleType.Unused, "Unused 4", 0x3c,
          0x01, 0x01, 0x01, 0x01, 0x3E, 0x36),
    Style(StyleType.Unused, "Unused 5", 0x3d,
          0x1A, 0x00, 0x1D, 0x10, 0x43, 0x43),
    Style(StyleType.Unused, "Unused 6", 0x3e,
          0x1A, 0x00, 0x1D, 0x10, 0x43, 0x43),
    Style(StyleType.Unused, "Unused 7", 0x3f,
          0x1A, 0x1A, 0x1F, 0x1A, 0x43, 0x43),
    Style(StyleType.Unused, "Unused 8", 0x40,
          0x08, 0x08, 0x08, 0x08, 0x43, 0x43),
    Style(StyleType.Unused, "Unused 9", 0x41,
          0x01, 0x01, 0x01, 0x01, 0x3E, 0x36)
]
