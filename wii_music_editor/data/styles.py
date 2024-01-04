from wii_music_Style.utils.translate import tr


class StyleClass:
    def __init__(self, style_type, name, mem_offset, style_id, default_style):
        self.StyleType = style_type
        self.Name = name
        self.MemOffset = mem_offset
        self.StyleId = style_id
        self.DefaultStyle = default_style


class StyleTypeValue:
    Global = 0
    SongSpecific = 1
    QuickJam = 2
    Menu = 3


def get_styles():
    none_instrument = 67
    return [
        StyleClass(StyleTypeValue.Global, tr("Style", 'Jazz'),
                   0x0659A65C, '00', [28, 2, 0, 16, 42, 45]),
        StyleClass(StyleTypeValue.Global, tr("Style", 'Rock'),
                   0x0659A680, '01', [14, 14, 36, 15, 41, 47]),
        StyleClass(StyleTypeValue.Global, tr("Style", 'Latin'),
                   0x0659A6A4, '02', [27, 28, 1, 15, 43, 46]),
        StyleClass(StyleTypeValue.Global, tr("Style", 'March'),
                   0x0659A6C8, '03', [27, 27, 27, 31, 59, 58]),
        StyleClass(StyleTypeValue.Global, tr("Style", 'Electronic'),
                   0x659A6EC, '04', [2, 22, 8, 23, 62, 50]),
        StyleClass(StyleTypeValue.Global, tr("Style", 'Pop'),
                   0x659A710, '05', [0, 2, 13, 15, 40, 47]),
        StyleClass(StyleTypeValue.Global, tr("Style", 'Japanese'),
                   0x659A734, '06', [29, none_instrument, none_instrument, 20, 56, 51]),
        StyleClass(StyleTypeValue.Global, tr("Style", 'Tango'),
                   0x659A758, '07', [25, 0, 32, 16, 58, 52]),
        StyleClass(StyleTypeValue.Global, tr("Style", 'Classical'),
                   0x659A77C, '08', [25, 25, 6, 26, none_instrument, none_instrument]),
        StyleClass(StyleTypeValue.Global, tr("Style", 'Hawaiian'),
                   0x659A7A0, '09', [17, 17, 17, 16, 46, 45]),
        StyleClass(StyleTypeValue.Global, tr("Style", 'Reggae'),
                   0x659A7C4, '0A', [3, 3, 0, 15, 64, none_instrument]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'A Little Night Music'),
                   0x659AB00, '21', [29, 25, 6, 26, none_instrument, none_instrument]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Animal Crossing'),
                   0x659AA28, '1B', [32, 18, 13, 13, 46, 45]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Animal Crossing K.K. Blues'),
                   0x659AB48, '23', [33, 28, 13, 16, 42, 53]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Carmen'),
                   0x659A878, '0F', [35, 32, 13, 16, 59, 46]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Chariots of Fire'),
                   0x659A908, '13', [0, 13, 6, 7, 58, 46]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Every Breath You Take'),
                   0x659A8E4, '12', [33, 0, 22, 15, 40, 47]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'From Santurtzi to Bilbao'),
                   0x659AADc, '20', [3, 3, 3, 3, 50, 47]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Happy Birthday to You'),
                   0x659AA94, '1E', [27, 28, 0, 16, 42, 45]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'I\'ll Be There'),
                   0x659A974, '16', [38, 38, 39, 39, 44, 50]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'I\'ve Never Been to Me'),
                   0x659A9Bc, '18', [0, 0, 13, 15, 40, 46]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'La Cucaracha'),
                   0x659AAB8, '1F', [29, 1, 13, 15, 48, 54]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Material Girl'),
                   0x659A950, '15', [36, 14, 22, 23, 60, 47]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Minuet in G Major'),
                   0x659AA4c, '1C', [29, 30, 0, 6, none_instrument, none_instrument]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'O-Christmas Tree'),
                   0x659A89c, '10', [5, 5, 5, 5, 51, none_instrument]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Oh My Darling Clementine'),
                   0x659A830, '0D', [36, 36, 9, 36, 58, 52]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Over The Waves'),
                   0x659A8C0, '11', [32, 30, 6, 16, 53, 47]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Scarborough Fair'),
                   0x659A854, '0E', [34, 34, 13, 16, 59, 47]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'September'),
                   0x659A92c, '14', [27, 28, 8, 23, 40, 50]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Super Mario Bros'),
                   0x659AC8c, '2C', [37, 37, 37, 37, none_instrument, none_instrument]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'The Blue Danube'),
                   0x659AB24, '22', [30, 25, 4, 31, 58, 52]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'The Entertainer'),
                   0x659AA70, '1D', [0, 6, 0, 16, 42, 46]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'The Legend of Zelda'),
                   0x659A9E0, '19', [27, 25, 21, 31, 58, 59]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Twinkle Twinkle Little Star'),
                   0x659A7E8, '0B', [0, 1, 13, 16, 51, 52]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Wii Sports'),
                   0x659AA04, '1A', [29, 0, 13, 15, 60, 47]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Wii Music'),
                   0x659AB6c, '24', [25, 28, 0, 15, 40, 50]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Woman'),
                   0x659A998, '17', [28, 27, 13, 15, 40, 49]),
        StyleClass(StyleTypeValue.SongSpecific, tr("Style", 'Yankee Doodle'),
                   0x659A80C, '0C', [33, 24, 18, 16, 49, 46]),
        StyleClass(StyleTypeValue.QuickJam, tr("Style", 'A Capella'),
                   0x659AC20, '29', [38, 38, 39, 39, 66, 50]),
        StyleClass(StyleTypeValue.QuickJam, tr("Style", 'Acoustic'),
                   0x659AB90, '38', [25, 25, 13, 13, 52, 50]),  #
        StyleClass(StyleTypeValue.QuickJam, tr("Style", 'African Electronic'),
                   0x659AB93, '3C', [25, 25, 13, 13, 52, 50]),  #
        StyleClass(StyleTypeValue.QuickJam, tr("Style", 'Animals!'),
                   0x659AC68, '2B', [11, 11, 10, 31, 59, 49]),
        StyleClass(StyleTypeValue.QuickJam, tr("Style", 'Calypso'),
                   0x659AC44, '2A', [3, 3, 3, 3, none_instrument, none_instrument]),
        StyleClass(StyleTypeValue.QuickJam, tr("Style", 'Exotic'),
                   0x659ABFC, '28', [19, 19, 4, 19, 55, none_instrument]),
        StyleClass(StyleTypeValue.QuickJam, tr("Style", 'Flamenco'),
                   0x659AB90, '25', [25, 25, 13, 13, 52, 50]),  #
        StyleClass(StyleTypeValue.QuickJam, tr("Style", 'Galactic'),
                   0x659ADD0, '35', [25, 25, 13, 13, 52, 50]),  #
        StyleClass(StyleTypeValue.QuickJam, tr("Style", 'Handbell'),
                   0x659AB93, '43', [25, 25, 13, 13, 52, 50]),  #
        StyleClass(StyleTypeValue.QuickJam, tr("Style", 'Karate'),
                   0x659ABB4, '26', [14, 14, 14, 15, 41, 63]),
        StyleClass(StyleTypeValue.QuickJam, tr("Style", 'Orchestral'),
                   0x659AD64, '32', [29, 27, 25, 7, 58, none_instrument]),
        StyleClass(StyleTypeValue.QuickJam, tr("Style", 'Parade'),
                   0x659ABD8, '27', [27, 30, 27, 31, 65, 57]),
        StyleClass(StyleTypeValue.QuickJam, tr("Style", 'Rap'),
                   0x659ADF4, '36', [12, none_instrument, 8, 23, 62, 61]),
        StyleClass(StyleTypeValue.QuickJam, tr("Style", 'Samba'),
                   0x659AE18, '37', [29, 1, 13, 15, 65, 48]),
        StyleClass(StyleTypeValue.Menu, tr("Style", 'Menu Style Main'),
                   0x659ACB0, '2D', [25, 28, 0, 15, 40, 40]),
        StyleClass(StyleTypeValue.Menu, tr("Style", 'Menu Style Electronic'),
                   0x659ACD4, '2E', [2, 22, 0, 23, 62, 40]),
        StyleClass(StyleTypeValue.Menu, tr("Style", 'Menu Style Japanese'),
                   0x659ACF8, '2F', [29, 20, 0, 20, 56, 40]),
        StyleClass(StyleTypeValue.Menu, tr("Style", 'Menu Style March'),
                   0x659AD1C, '30', [30, 27, 0, 31, 58, 40]),
        StyleClass(StyleTypeValue.Menu, tr("Style", 'Menu Style A Capella'),
                   0x659AD40, '31', [38, 39, 0, 39, 66, 40])
    ]


styleList = get_styles()
