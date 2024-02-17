from enum import Enum


class SongType(Enum):
    Regular = 0
    Menu = 1
    Maestro = 2
    Hand_Bell = 3


class SongClass:
    __totalSongs = 0
    song_type: SongType
    name: str
    mem_order: int
    default_style: int
    list_order: int

    def __init__(self, song_type: SongType, name: str, mem_order: int, default_style: int = -1):
        self.song_type = song_type
        self.name = name
        self.mem_order = mem_order
        self.default_style = default_style
        self.list_order = SongClass.__totalSongs
        SongClass.__totalSongs += 1


song_list = [
    SongClass(SongType.Regular, 'A Little Night Music', 0x06, 0x21),
    SongClass(SongType.Regular, 'American Patrol', 0x0B, 0x03),
    SongClass(SongType.Regular, 'Animal Crossing', 0x30, 0x1B),
    SongClass(SongType.Regular, 'Animal Crossing -- K.K. Blues', 0x1A, 0x23),
    SongClass(SongType.Regular, 'Bridal Chorus', 0x01, 0x08),
    SongClass(SongType.Regular, 'Carmen', 0x03, 0x0F),
    SongClass(SongType.Regular, 'Chariots of Fire', 0x23, 0x13),
    SongClass(SongType.Regular, 'Daydream Believer', 0x21, 0x00),
    SongClass(SongType.Regular, 'Do-Re-Mi', 0x09, 0x01),
    SongClass(SongType.Regular, 'Every Breath You Take', 0x22, 0x12),
    SongClass(SongType.Regular, 'F-Zero -- Mute City Theme', 0x31, 0x01),
    SongClass(SongType.Regular, 'Frère Jacques', 0x16, 0x04),
    SongClass(SongType.Regular, 'From Santurtzi to Bilbao', 0x1B, 0x20),
    SongClass(SongType.Regular, 'From the New World', 0x10, 0x02),
    SongClass(SongType.Regular, 'Happy Birthday to You', 0x08, 0x1E),
    SongClass(SongType.Regular, 'I\'ll Be There', 0x28, 0x16),
    SongClass(SongType.Regular, 'I\'ve Never Been to Me', 0x2C, 0x18),
    SongClass(SongType.Regular, 'Jingle Bell Rock', 0x29, 0x00),
    SongClass(SongType.Regular, 'La Bamba', 0x11, 0x0A),
    SongClass(SongType.Regular, 'La Cucaracha', 0x1D, 0x1F),
    SongClass(SongType.Regular, 'Little Hans', 0x19, 0x04),
    SongClass(SongType.Regular, 'Long, Long Ago', 0x13, 0x08),
    SongClass(SongType.Regular, 'Material Girl', 0x26, 0x15),
    SongClass(SongType.Regular, 'Minuet in G Major', 0x07, 0x1C),
    SongClass(SongType.Regular, 'My Grandfather\'s Clock', 0x0F, 0x05),
    SongClass(SongType.Regular, 'O Christmas Tree', 0x18, 0x10),
    SongClass(SongType.Regular, 'Ode to Joy', 0x00, 0x02),
    SongClass(SongType.Regular, 'Oh, My Darling Clementine', 0x0E, 0x0D),
    SongClass(SongType.Regular, 'Over the Waves', 0x1E, 0x11),
    SongClass(SongType.Regular, 'Please Mr. Postman', 0x25, 0x09),
    SongClass(SongType.Regular, 'Sakura Sakura', 0x1F, 0x06),
    SongClass(SongType.Regular, 'Scarborough Fair', 0x12, 0x0E),
    SongClass(SongType.Regular, 'September', 0x24, 0x14),
    SongClass(SongType.Regular, 'Sukiyaki', 0x20, 0x0A),
    SongClass(SongType.Regular, 'Super Mario Bros.', 0x2D, 0x2C),
    SongClass(SongType.Regular, 'Sur le pont d\'Avignon', 0x15, 0x09),
    SongClass(SongType.Regular, 'Swan Lake', 0x02, 0x07),
    SongClass(SongType.Regular, 'The Blue Danube', 0x05, 0x22),
    SongClass(SongType.Regular, 'The Entertainer', 0x0A, 0x1D),
    SongClass(SongType.Regular, 'The Flea Waltz', 0x17, 0x03),
    SongClass(SongType.Regular, 'The Legend of Zelda', 0x2E, 0x19),
    SongClass(SongType.Regular, 'The Loco-Motion', 0x27, 0x05),
    SongClass(SongType.Regular, 'Troika', 0x1C, 0x07),
    SongClass(SongType.Regular, 'Turkey in the Straw', 0x0C, 0x06),
    SongClass(SongType.Regular, 'Twinkle, Twinkle, Little Star', 0x14, 0x0B),
    SongClass(SongType.Regular, 'Wake Me Up Before You Go-Go', 0x2A, 0x17),
    SongClass(SongType.Regular, 'Wii Music', 0x04, 0x24),
    SongClass(SongType.Regular, 'Wii Sports', 0x2F, 0x1A),
    SongClass(SongType.Regular, 'Woman', 0x2B, 0x17),
    SongClass(SongType.Regular, 'Yankee Doodle', 0x0D, 0x0C),
    SongClass(SongType.Maestro, 'Twinkle, Twinkle, Little Star (Mii Maestro)', 0x02),
    SongClass(SongType.Maestro, 'Carmen (Mii Maestro)', 0x00),
    SongClass(SongType.Maestro, 'The Four Seasons -- Spring (Mii Maestro)', 0x04),
    SongClass(SongType.Maestro, 'Ode to Joy (Mii Maestro)', 0x03),
    SongClass(SongType.Maestro, 'The Legend of Zelda (Mii Maestro)', 0x01),
    SongClass(SongType.Hand_Bell, 'O Christmas Tree (Handbell Harmony)', 0x00),
    SongClass(SongType.Hand_Bell, 'Hum, Hum, Hum (Handbell Harmony)', 0x02),
    SongClass(SongType.Hand_Bell, 'My Grandfather\'s Clock (Handbell Harmony)', 0x03),
    SongClass(SongType.Hand_Bell, 'Do-Re-Mi (Handbell Harmony)', 0x01),
    SongClass(SongType.Hand_Bell, 'Sukiyaki (Handbell Harmony)', 0x04),
    SongClass(SongType.Menu, 'Menu Song', 0x00)
]


def get_song_by_id(song_id: int) -> SongClass:
    for song in song_list:
        if song.mem_order == song_id:
            return song
    print(f"Song with ID {song_id} not found")
    return song_list[0]
