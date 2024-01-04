from wii_music_Song.utils.translate import tr


class SongClass:
    def __init__(self, song_type, name, mem_order, default_style="nope", mem_offset=-1):
        self.SongType = song_type
        self.Name = name
        self.MemOrder = mem_order
        self.DefaultStyle = default_style
        self.mem_offset = mem_offset
        if self.mem_offset == -1:
            self.mem_offset = 0x025a0440 + 0xBC * self.MemOrder


class SongTypeValue:
    Regular = 0
    Menu = 1
    Maestro = 2
    Hand_Bell = 3


def get_songs():
    return [
        SongClass(SongTypeValue.Regular, tr("Song", 'A Little Night Music'), 
                  6, "21"),
        SongClass(SongTypeValue.Regular, tr("Song", 'American Patrol'), 
                  11, "03"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Animal Crossing'), 
                  48, "1B"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Animal Crossing -- K.K. Blues'), 
                  26, "23"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Bridal Chorus'), 
                  1, "08"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Carmen'), 
                  3, "0F"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Chariots of Fire'), 
                  35, "13"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Daydream Believer'), 
                  33, "00"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Do-Re-Mi'), 
                  9, "01"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Every Breath You Take'), 
                  34, "12"),
        SongClass(SongTypeValue.Regular, tr("Song", 'F-Zero -- Mute City Theme'), 
                  49, "01"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Frère Jacques'), 
                  22, "04"),
        SongClass(SongTypeValue.Regular, tr("Song", 'From Santurtzi to Bilbao'), 
                  27, "20"),
        SongClass(SongTypeValue.Regular, tr("Song", 'From the New World'), 
                  16, "02"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Happy Birthday to You'), 
                  8, "1E"),
        SongClass(SongTypeValue.Regular, tr("Song", 'I\'ll Be There'), 
                  40, "16"),
        SongClass(SongTypeValue.Regular, tr("Song", 'I\'ve Never Been to Me'), 
                  44, "18"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Jingle Bell Rock'), 
                  41, "00"),
        SongClass(SongTypeValue.Regular, tr("Song", 'La Bamba'), 
                  17, "0A"),
        SongClass(SongTypeValue.Regular, tr("Song", 'La Cucaracha'), 
                  29, "1F"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Little Hans'), 
                  25, "04"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Long, Long Ago'), 
                  19, "08"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Material Girl'), 
                  38, "15"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Minuet in G Major'), 
                  7, "1C"),
        SongClass(SongTypeValue.Regular, tr("Song", 'My Grandfather\'s Clock'), 
                  15, "05"),
        SongClass(SongTypeValue.Regular, tr("Song", 'O Christmas Tree'), 
                  24, "10"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Ode to Joy'), 
                  0, "02"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Oh, My Darling Clementine'), 
                  14, "0D"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Over the Waves'), 
                  30, "11"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Please Mr. Postman'), 
                  37, "09"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Sakura Sakura'), 
                  31, "06"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Scarborough Fair'), 
                  18, "0E"),
        SongClass(SongTypeValue.Regular, tr("Song", 'September'), 
                  36, "14"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Sukiyaki'), 
                  32, "0A"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Super Mario Bros.'), 
                  45, "2C"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Sur le pont d\'Avignon'), 
                  21, "09"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Swan Lake'), 
                  2, "07"),
        SongClass(SongTypeValue.Regular, tr("Song", 'The Blue Danube'), 
                  5, "22"),
        SongClass(SongTypeValue.Regular, tr("Song", 'The Entertainer'), 
                  10, "1D"),
        SongClass(SongTypeValue.Regular, tr("Song", 'The Flea Waltz'), 
                  23, "03"),
        SongClass(SongTypeValue.Regular, tr("Song", 'The Legend of Zelda'), 
                  46, "19"),
        SongClass(SongTypeValue.Regular, tr("Song", 'The Loco-Motion'), 
                  39, "05"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Troika'), 
                  28, "07"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Turkey in the Straw'), 
                  12, "06"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Twinkle, Twinkle, Little Star'), 
                  20, "0B"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Wake Me Up Before You Go-Go'), 
                  42, "17"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Wii Music'), 
                  4, "24"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Wii Sports'), 
                  47, "1A"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Woman'), 
                  43, "17"),
        SongClass(SongTypeValue.Regular, tr("Song", 'Yankee Doodle'), 
                  13, "0C"),
        SongClass(SongTypeValue.Maestro, tr("Song", 'Twinkle, Twinkle, Little Star (Mii Maestro)'), 
                  2, mem_offset=0x25a3e1c),
        SongClass(SongTypeValue.Maestro, tr("Song", 'Carmen (Mii Maestro)'), 
                  0, mem_offset=0x25a3d80),
        SongClass(SongTypeValue.Maestro, tr("Song", 'The Four Seasons -- Spring (Mii Maestro)'), 
                  4, mem_offset=0x25a3f54),
        SongClass(SongTypeValue.Maestro, tr("Song", 'Ode to Joy (Mii Maestro)'), 
                  3, mem_offset=0x25a3ff0),
        SongClass(SongTypeValue.Maestro, tr("Song", 'The Legend of Zelda (Mii Maestro)'), 
                  1, mem_offset=0x25a3eb8),
        SongClass(SongTypeValue.Hand_Bell, tr("Song", 'O Christmas Tree (Handbell Harmony)'), 
                  0, mem_offset=0x2566D5A),
        SongClass(SongTypeValue.Hand_Bell, tr("Song", 'Hum, Hum, Hum (Handbell Harmony)'), 
                  2, mem_offset=0x2566E0A),
        SongClass(SongTypeValue.Hand_Bell, tr("Song", 'My Grandfather\'s Clock (Handbell Harmony)'), 
                  3, mem_offset=0x2566E62),
        SongClass(SongTypeValue.Hand_Bell, tr("Song", 'Do-Re-Mi (Handbell Harmony)'), 
                  1, mem_offset=0x2566DB2),
        SongClass(SongTypeValue.Hand_Bell, tr("Song", 'Sukiyaki (Handbell Harmony)'), 
                  4, mem_offset=0x2566EBA),
        SongClass(SongTypeValue.Menu, tr("Song", 'Menu Song'), 
                  -1, mem_offset=[0x259ACB0, 0x259ACD4, 0x259ACF8, 0x259AD1C, 0x259AD40])
    ]


songList = get_songs()
