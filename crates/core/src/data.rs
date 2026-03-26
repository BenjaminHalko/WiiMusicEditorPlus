use crate::types::{Instrument, Song, SongType, Style, StyleInstruments, StyleType};

pub const SONG_LIST: &[Song] = &[
    Song {
        name: "A Little Night Music",
        song_type: SongType::Regular,
        mem_order: 6,
        default_style: 33,
    },
    Song {
        name: "American Patrol",
        song_type: SongType::Regular,
        mem_order: 11,
        default_style: 3,
    },
    Song {
        name: "Animal Crossing",
        song_type: SongType::Regular,
        mem_order: 48,
        default_style: 27,
    },
    Song {
        name: "Animal Crossing -- K.K. Blues",
        song_type: SongType::Regular,
        mem_order: 26,
        default_style: 35,
    },
    Song {
        name: "Bridal Chorus",
        song_type: SongType::Regular,
        mem_order: 1,
        default_style: 8,
    },
    Song {
        name: "Carmen",
        song_type: SongType::Regular,
        mem_order: 3,
        default_style: 15,
    },
    Song {
        name: "Chariots of Fire",
        song_type: SongType::Regular,
        mem_order: 35,
        default_style: 19,
    },
    Song {
        name: "Daydream Believer",
        song_type: SongType::Regular,
        mem_order: 33,
        default_style: 0,
    },
    Song {
        name: "Do-Re-Mi",
        song_type: SongType::Regular,
        mem_order: 9,
        default_style: 1,
    },
    Song {
        name: "Every Breath You Take",
        song_type: SongType::Regular,
        mem_order: 34,
        default_style: 18,
    },
    Song {
        name: "F-Zero -- Mute City Theme",
        song_type: SongType::Regular,
        mem_order: 49,
        default_style: 1,
    },
    Song {
        name: "Frère Jacques",
        song_type: SongType::Regular,
        mem_order: 22,
        default_style: 4,
    },
    Song {
        name: "From Santurtzi to Bilbao",
        song_type: SongType::Regular,
        mem_order: 27,
        default_style: 32,
    },
    Song {
        name: "From the New World",
        song_type: SongType::Regular,
        mem_order: 16,
        default_style: 2,
    },
    Song {
        name: "Happy Birthday to You",
        song_type: SongType::Regular,
        mem_order: 8,
        default_style: 30,
    },
    Song {
        name: "I'll Be There",
        song_type: SongType::Regular,
        mem_order: 40,
        default_style: 22,
    },
    Song {
        name: "I've Never Been to Me",
        song_type: SongType::Regular,
        mem_order: 44,
        default_style: 24,
    },
    Song {
        name: "Jingle Bell Rock",
        song_type: SongType::Regular,
        mem_order: 41,
        default_style: 0,
    },
    Song {
        name: "La Bamba",
        song_type: SongType::Regular,
        mem_order: 17,
        default_style: 10,
    },
    Song {
        name: "La Cucaracha",
        song_type: SongType::Regular,
        mem_order: 29,
        default_style: 31,
    },
    Song {
        name: "Little Hans",
        song_type: SongType::Regular,
        mem_order: 25,
        default_style: 4,
    },
    Song {
        name: "Long, Long Ago",
        song_type: SongType::Regular,
        mem_order: 19,
        default_style: 8,
    },
    Song {
        name: "Material Girl",
        song_type: SongType::Regular,
        mem_order: 38,
        default_style: 21,
    },
    Song {
        name: "Minuet in G Major",
        song_type: SongType::Regular,
        mem_order: 7,
        default_style: 28,
    },
    Song {
        name: "My Grandfather's Clock",
        song_type: SongType::Regular,
        mem_order: 15,
        default_style: 5,
    },
    Song {
        name: "O Christmas Tree",
        song_type: SongType::Regular,
        mem_order: 24,
        default_style: 16,
    },
    Song {
        name: "Ode to Joy",
        song_type: SongType::Regular,
        mem_order: 0,
        default_style: 2,
    },
    Song {
        name: "Oh, My Darling Clementine",
        song_type: SongType::Regular,
        mem_order: 14,
        default_style: 13,
    },
    Song {
        name: "Over the Waves",
        song_type: SongType::Regular,
        mem_order: 30,
        default_style: 17,
    },
    Song {
        name: "Please Mr. Postman",
        song_type: SongType::Regular,
        mem_order: 37,
        default_style: 9,
    },
    Song {
        name: "Sakura Sakura",
        song_type: SongType::Regular,
        mem_order: 31,
        default_style: 6,
    },
    Song {
        name: "Scarborough Fair",
        song_type: SongType::Regular,
        mem_order: 18,
        default_style: 14,
    },
    Song {
        name: "September",
        song_type: SongType::Regular,
        mem_order: 36,
        default_style: 20,
    },
    Song {
        name: "Sukiyaki",
        song_type: SongType::Regular,
        mem_order: 32,
        default_style: 10,
    },
    Song {
        name: "Super Mario Bros.",
        song_type: SongType::Regular,
        mem_order: 45,
        default_style: 44,
    },
    Song {
        name: "Sur le pont d'Avignon",
        song_type: SongType::Regular,
        mem_order: 21,
        default_style: 9,
    },
    Song {
        name: "Swan Lake",
        song_type: SongType::Regular,
        mem_order: 2,
        default_style: 7,
    },
    Song {
        name: "The Blue Danube",
        song_type: SongType::Regular,
        mem_order: 5,
        default_style: 34,
    },
    Song {
        name: "The Entertainer",
        song_type: SongType::Regular,
        mem_order: 10,
        default_style: 29,
    },
    Song {
        name: "The Flea Waltz",
        song_type: SongType::Regular,
        mem_order: 23,
        default_style: 3,
    },
    Song {
        name: "The Legend of Zelda",
        song_type: SongType::Regular,
        mem_order: 46,
        default_style: 25,
    },
    Song {
        name: "The Loco-Motion",
        song_type: SongType::Regular,
        mem_order: 39,
        default_style: 5,
    },
    Song {
        name: "Troika",
        song_type: SongType::Regular,
        mem_order: 28,
        default_style: 7,
    },
    Song {
        name: "Turkey in the Straw",
        song_type: SongType::Regular,
        mem_order: 12,
        default_style: 6,
    },
    Song {
        name: "Twinkle, Twinkle, Little Star",
        song_type: SongType::Regular,
        mem_order: 20,
        default_style: 11,
    },
    Song {
        name: "Wake Me Up Before You Go-Go",
        song_type: SongType::Regular,
        mem_order: 42,
        default_style: 23,
    },
    Song {
        name: "Wii Music",
        song_type: SongType::Regular,
        mem_order: 4,
        default_style: 36,
    },
    Song {
        name: "Wii Sports",
        song_type: SongType::Regular,
        mem_order: 47,
        default_style: 26,
    },
    Song {
        name: "Woman",
        song_type: SongType::Regular,
        mem_order: 43,
        default_style: 23,
    },
    Song {
        name: "Yankee Doodle",
        song_type: SongType::Regular,
        mem_order: 13,
        default_style: 12,
    },
    Song {
        name: "Twinkle, Twinkle, Little Star (Mii Maestro)",
        song_type: SongType::Maestro,
        mem_order: 2,
        default_style: 0,
    },
    Song {
        name: "Carmen (Mii Maestro)",
        song_type: SongType::Maestro,
        mem_order: 0,
        default_style: 0,
    },
    Song {
        name: "The Four Seasons -- Spring (Mii Maestro)",
        song_type: SongType::Maestro,
        mem_order: 4,
        default_style: 0,
    },
    Song {
        name: "Ode to Joy (Mii Maestro)",
        song_type: SongType::Maestro,
        mem_order: 3,
        default_style: 0,
    },
    Song {
        name: "The Legend of Zelda (Mii Maestro)",
        song_type: SongType::Maestro,
        mem_order: 1,
        default_style: 0,
    },
    Song {
        name: "O Christmas Tree (Handbell Harmony)",
        song_type: SongType::Handbell,
        mem_order: 0,
        default_style: 0,
    },
    Song {
        name: "Hum, Hum, Hum (Handbell Harmony)",
        song_type: SongType::Handbell,
        mem_order: 2,
        default_style: 0,
    },
    Song {
        name: "My Grandfather's Clock (Handbell Harmony)",
        song_type: SongType::Handbell,
        mem_order: 3,
        default_style: 0,
    },
    Song {
        name: "Do-Re-Mi (Handbell Harmony)",
        song_type: SongType::Handbell,
        mem_order: 1,
        default_style: 0,
    },
    Song {
        name: "Sukiyaki (Handbell Harmony)",
        song_type: SongType::Handbell,
        mem_order: 4,
        default_style: 0,
    },
    Song {
        name: "Menu Song",
        song_type: SongType::Menu,
        mem_order: 0,
        default_style: 0,
    },
];

pub const STYLE_LIST: &[Style] = &[
    Style {
        name: "Jazz",
        style_type: StyleType::Global,
        instruments: StyleInstruments([28, 2, 0, 16, 42, 45]),
    },
    Style {
        name: "Rock",
        style_type: StyleType::Global,
        instruments: StyleInstruments([14, 14, 36, 15, 41, 47]),
    },
    Style {
        name: "Latin",
        style_type: StyleType::Global,
        instruments: StyleInstruments([27, 28, 1, 15, 43, 46]),
    },
    Style {
        name: "March",
        style_type: StyleType::Global,
        instruments: StyleInstruments([27, 27, 27, 31, 59, 58]),
    },
    Style {
        name: "Electronic",
        style_type: StyleType::Global,
        instruments: StyleInstruments([2, 22, 8, 23, 62, 50]),
    },
    Style {
        name: "Pop",
        style_type: StyleType::Global,
        instruments: StyleInstruments([0, 2, 13, 15, 40, 47]),
    },
    Style {
        name: "Japanese",
        style_type: StyleType::Global,
        instruments: StyleInstruments([29, 67, 67, 20, 56, 51]),
    },
    Style {
        name: "Tango",
        style_type: StyleType::Global,
        instruments: StyleInstruments([25, 0, 32, 16, 58, 52]),
    },
    Style {
        name: "Classical",
        style_type: StyleType::Global,
        instruments: StyleInstruments([25, 25, 6, 26, 67, 67]),
    },
    Style {
        name: "Hawaiian",
        style_type: StyleType::Global,
        instruments: StyleInstruments([17, 17, 17, 16, 46, 45]),
    },
    Style {
        name: "Reggae",
        style_type: StyleType::Global,
        instruments: StyleInstruments([3, 3, 0, 15, 64, 67]),
    },
    Style {
        name: "A Cappella",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([38, 38, 39, 39, 66, 50]),
    },
    Style {
        name: "Acoustic",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([38, 18, 13, 13, 45, 46]),
    },
    Style {
        name: "African",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([1, 1, 1, 1, 55, 45]),
    },
    Style {
        name: "Animals!",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([11, 11, 16, 31, 59, 49]),
    },
    Style {
        name: "Ballad",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([28, 0, 0, 15, 44, 45]),
    },
    Style {
        name: "Calypso",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([3, 3, 3, 3, 67, 67]),
    },
    Style {
        name: "Celtic",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([34, 34, 13, 16, 59, 47]),
    },
    Style {
        name: "Country",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([33, 24, 18, 16, 49, 46]),
    },
    Style {
        name: "Eurobeat",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([36, 14, 22, 23, 60, 47]),
    },
    Style {
        name: "European",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([30, 25, 4, 31, 58, 52]),
    },
    Style {
        name: "Exotic",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([19, 19, 4, 19, 55, 67]),
    },
    Style {
        name: "Flamenco",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([25, 25, 13, 13, 52, 50]),
    },
    Style {
        name: "Folk",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([35, 32, 13, 16, 59, 46]),
    },
    Style {
        name: "French Bistro",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([32, 30, 6, 16, 53, 47]),
    },
    Style {
        name: "Funk",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([27, 28, 22, 15, 40, 50]),
    },
    Style {
        name: "Galactic",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([36, 22, 8, 23, 60, 61]),
    },
    Style {
        name: "Handbells",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([5, 5, 5, 5, 51, 67]),
    },
    Style {
        name: "Karate",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([14, 14, 14, 15, 41, 63]),
    },
    Style {
        name: "NES-Style",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([37, 37, 37, 37, 67, 67]),
    },
    Style {
        name: "Orchestral",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([29, 27, 25, 7, 58, 67]),
    },
    Style {
        name: "Parade",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([27, 30, 27, 31, 65, 57]),
    },
    Style {
        name: "Rap",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([12, 67, 8, 23, 62, 61]),
    },
    Style {
        name: "Salsa",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([27, 1, 13, 15, 45, 54]),
    },
    Style {
        name: "Samba",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([29, 1, 13, 15, 65, 48]),
    },
    Style {
        name: "Soul",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([27, 28, 8, 23, 40, 50]),
    },
    Style {
        name: "Soundtrack",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([0, 13, 6, 7, 58, 46]),
    },
    Style {
        name: "Toy",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([36, 36, 9, 36, 58, 52]),
    },
    Style {
        name: "Woodwind",
        style_type: StyleType::QuickJam,
        instruments: StyleInstruments([29, 30, 0, 6, 67, 67]),
    },
    Style {
        name: "A Little Night Music",
        style_type: StyleType::SongSpecific,
        instruments: StyleInstruments([29, 25, 6, 26, 67, 67]),
    },
    Style {
        name: "Animal Crossing",
        style_type: StyleType::SongSpecific,
        instruments: StyleInstruments([32, 18, 13, 13, 46, 45]),
    },
    Style {
        name: "Animal Crossing K.K. Blues",
        style_type: StyleType::SongSpecific,
        instruments: StyleInstruments([33, 28, 13, 16, 42, 53]),
    },
    Style {
        name: "Every Breath You Take",
        style_type: StyleType::SongSpecific,
        instruments: StyleInstruments([33, 0, 22, 15, 40, 47]),
    },
    Style {
        name: "From Santurtzi to Bilbao",
        style_type: StyleType::SongSpecific,
        instruments: StyleInstruments([3, 3, 3, 3, 50, 47]),
    },
    Style {
        name: "Happy Birthday to You",
        style_type: StyleType::SongSpecific,
        instruments: StyleInstruments([27, 28, 0, 16, 42, 45]),
    },
    Style {
        name: "I'll Be There",
        style_type: StyleType::SongSpecific,
        instruments: StyleInstruments([38, 38, 39, 39, 44, 50]),
    },
    Style {
        name: "I've Never Been to Me",
        style_type: StyleType::SongSpecific,
        instruments: StyleInstruments([0, 0, 13, 15, 40, 46]),
    },
    Style {
        name: "La Cucaracha",
        style_type: StyleType::SongSpecific,
        instruments: StyleInstruments([29, 1, 13, 15, 48, 54]),
    },
    Style {
        name: "O-Christmas Tree",
        style_type: StyleType::SongSpecific,
        instruments: StyleInstruments([5, 5, 5, 5, 51, 67]),
    },
    Style {
        name: "The Entertainer",
        style_type: StyleType::SongSpecific,
        instruments: StyleInstruments([0, 6, 0, 16, 42, 46]),
    },
    Style {
        name: "The Legend of Zelda",
        style_type: StyleType::SongSpecific,
        instruments: StyleInstruments([27, 25, 21, 31, 58, 59]),
    },
    Style {
        name: "Twinkle Twinkle Little Star",
        style_type: StyleType::SongSpecific,
        instruments: StyleInstruments([0, 1, 13, 16, 51, 52]),
    },
    Style {
        name: "Wii Sports",
        style_type: StyleType::SongSpecific,
        instruments: StyleInstruments([29, 0, 13, 15, 60, 47]),
    },
    Style {
        name: "Wii Music",
        style_type: StyleType::SongSpecific,
        instruments: StyleInstruments([25, 28, 0, 15, 40, 50]),
    },
    Style {
        name: "Woman",
        style_type: StyleType::SongSpecific,
        instruments: StyleInstruments([28, 27, 13, 15, 40, 49]),
    },
    Style {
        name: "Menu Style Main",
        style_type: StyleType::Menu,
        instruments: StyleInstruments([25, 28, 0, 15, 40, 40]),
    },
    Style {
        name: "Menu Style Electronic",
        style_type: StyleType::Menu,
        instruments: StyleInstruments([2, 22, 0, 23, 62, 40]),
    },
    Style {
        name: "Menu Style Japanese",
        style_type: StyleType::Menu,
        instruments: StyleInstruments([29, 20, 0, 20, 56, 40]),
    },
    Style {
        name: "Menu Style March",
        style_type: StyleType::Menu,
        instruments: StyleInstruments([30, 27, 0, 31, 58, 40]),
    },
    Style {
        name: "Menu Style A Capella",
        style_type: StyleType::Menu,
        instruments: StyleInstruments([38, 39, 0, 39, 66, 40]),
    },
    Style {
        name: "Unused 1",
        style_type: StyleType::Unused,
        instruments: StyleInstruments([28, 29, 28, 31, 67, 67]),
    },
    Style {
        name: "Unused 2",
        style_type: StyleType::Unused,
        instruments: StyleInstruments([31, 27, 29, 29, 67, 67]),
    },
    Style {
        name: "Unused 3",
        style_type: StyleType::Unused,
        instruments: StyleInstruments([8, 8, 8, 8, 67, 67]),
    },
    Style {
        name: "Unused 4",
        style_type: StyleType::Unused,
        instruments: StyleInstruments([1, 1, 1, 1, 62, 54]),
    },
    Style {
        name: "Unused 5",
        style_type: StyleType::Unused,
        instruments: StyleInstruments([26, 0, 29, 16, 67, 67]),
    },
    Style {
        name: "Unused 6",
        style_type: StyleType::Unused,
        instruments: StyleInstruments([26, 0, 29, 16, 67, 67]),
    },
    Style {
        name: "Unused 7",
        style_type: StyleType::Unused,
        instruments: StyleInstruments([26, 26, 31, 26, 67, 67]),
    },
];

pub const INSTRUMENT_LIST: &[Instrument] = &[
    Instrument {
        name: "Piano",
        number: 0,
        in_menu: true,
    },
    Instrument {
        name: "Marimba",
        number: 1,
        in_menu: false,
    },
    Instrument {
        name: "Vibraphone",
        number: 2,
        in_menu: false,
    },
    Instrument {
        name: "Steel Drum",
        number: 3,
        in_menu: false,
    },
    Instrument {
        name: "Dulcimer",
        number: 4,
        in_menu: false,
    },
    Instrument {
        name: "Handbell",
        number: 5,
        in_menu: false,
    },
    Instrument {
        name: "Harpsichord",
        number: 6,
        in_menu: false,
    },
    Instrument {
        name: "Timpani",
        number: 7,
        in_menu: false,
    },
    Instrument {
        name: "Galactic Piano",
        number: 8,
        in_menu: false,
    },
    Instrument {
        name: "Toy Piano",
        number: 9,
        in_menu: false,
    },
    Instrument {
        name: "Dog",
        number: 10,
        in_menu: false,
    },
    Instrument {
        name: "Cat",
        number: 11,
        in_menu: false,
    },
    Instrument {
        name: "Rapper",
        number: 12,
        in_menu: false,
    },
    Instrument {
        name: "Guitar",
        number: 13,
        in_menu: false,
    },
    Instrument {
        name: "Electric Guitar",
        number: 14,
        in_menu: false,
    },
    Instrument {
        name: "Electric Bass",
        number: 15,
        in_menu: true,
    },
    Instrument {
        name: "Double Bass",
        number: 16,
        in_menu: false,
    },
    Instrument {
        name: "Ukulele",
        number: 17,
        in_menu: false,
    },
    Instrument {
        name: "Banjo",
        number: 18,
        in_menu: false,
    },
    Instrument {
        name: "Sitar",
        number: 19,
        in_menu: false,
    },
    Instrument {
        name: "Shamisen",
        number: 20,
        in_menu: true,
    },
    Instrument {
        name: "Harp",
        number: 21,
        in_menu: false,
    },
    Instrument {
        name: "Galactic Guitar",
        number: 22,
        in_menu: false,
    },
    Instrument {
        name: "Galactic Bass",
        number: 23,
        in_menu: true,
    },
    Instrument {
        name: "Jaw Harp",
        number: 24,
        in_menu: false,
    },
    Instrument {
        name: "Violin",
        number: 25,
        in_menu: true,
    },
    Instrument {
        name: "Cello",
        number: 26,
        in_menu: false,
    },
    Instrument {
        name: "Trumpet",
        number: 27,
        in_menu: true,
    },
    Instrument {
        name: "Saxophone",
        number: 28,
        in_menu: true,
    },
    Instrument {
        name: "Flute",
        number: 29,
        in_menu: true,
    },
    Instrument {
        name: "Clairenet",
        number: 30,
        in_menu: true,
    },
    Instrument {
        name: "Tuba",
        number: 31,
        in_menu: false,
    },
    Instrument {
        name: "Accordion",
        number: 32,
        in_menu: false,
    },
    Instrument {
        name: "Harmonica",
        number: 33,
        in_menu: false,
    },
    Instrument {
        name: "Bagpipe",
        number: 34,
        in_menu: false,
    },
    Instrument {
        name: "Recorder",
        number: 35,
        in_menu: false,
    },
    Instrument {
        name: "Galactic horn",
        number: 36,
        in_menu: false,
    },
    Instrument {
        name: "Nes",
        number: 37,
        in_menu: false,
    },
    Instrument {
        name: "Singer",
        number: 38,
        in_menu: true,
    },
    Instrument {
        name: "Bass Singer",
        number: 39,
        in_menu: true,
    },
    Instrument {
        name: "Basic Drums",
        number: 40,
        in_menu: true,
    },
    Instrument {
        name: "Rock Drums",
        number: 41,
        in_menu: false,
    },
    Instrument {
        name: "Jazz Drums",
        number: 42,
        in_menu: false,
    },
    Instrument {
        name: "Latin Drums",
        number: 43,
        in_menu: false,
    },
    Instrument {
        name: "Ballad Drums",
        number: 44,
        in_menu: false,
    },
    Instrument {
        name: "Congas",
        number: 45,
        in_menu: false,
    },
    Instrument {
        name: "Maracas",
        number: 46,
        in_menu: false,
    },
    Instrument {
        name: "Tambourine",
        number: 47,
        in_menu: false,
    },
    Instrument {
        name: "Cuica",
        number: 48,
        in_menu: false,
    },
    Instrument {
        name: "Cowbell",
        number: 49,
        in_menu: false,
    },
    Instrument {
        name: "Clap",
        number: 50,
        in_menu: false,
    },
    Instrument {
        name: "Bells",
        number: 51,
        in_menu: false,
    },
    Instrument {
        name: "Castanets",
        number: 52,
        in_menu: false,
    },
    Instrument {
        name: "Guiro",
        number: 53,
        in_menu: false,
    },
    Instrument {
        name: "Timpales",
        number: 54,
        in_menu: false,
    },
    Instrument {
        name: "Djembe",
        number: 55,
        in_menu: false,
    },
    Instrument {
        name: "Taiko Drum",
        number: 56,
        in_menu: true,
    },
    Instrument {
        name: "Cheerleader",
        number: 57,
        in_menu: false,
    },
    Instrument {
        name: "Snare Drum",
        number: 58,
        in_menu: true,
    },
    Instrument {
        name: "Bass Drum",
        number: 59,
        in_menu: false,
    },
    Instrument {
        name: "Galactic Drums",
        number: 60,
        in_menu: false,
    },
    Instrument {
        name: "Galactic Congas",
        number: 61,
        in_menu: false,
    },
    Instrument {
        name: "DJ Turntables",
        number: 62,
        in_menu: true,
    },
    Instrument {
        name: "Black Belt",
        number: 63,
        in_menu: false,
    },
    Instrument {
        name: "Reggae Drums",
        number: 64,
        in_menu: false,
    },
    Instrument {
        name: "Whistle",
        number: 65,
        in_menu: false,
    },
    Instrument {
        name: "Beatbox",
        number: 66,
        in_menu: true,
    },
    Instrument {
        name: "None",
        number: 67,
        in_menu: false,
    },
];

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn song_list_count() {
        assert_eq!(SONG_LIST.len(), 61);
    }

    #[test]
    fn style_list_count() {
        assert_eq!(STYLE_LIST.len(), 67);
    }

    #[test]
    fn instrument_list_count() {
        assert_eq!(INSTRUMENT_LIST.len(), 68);
    }

    fn assert_unique_mem_orders(song_type: SongType, label: &str) {
        let mut mem_orders: Vec<u8> = SONG_LIST
            .iter()
            .filter(|song| song.song_type == song_type)
            .map(|song| song.mem_order)
            .collect();
        mem_orders.sort_unstable();
        let original_len = mem_orders.len();
        mem_orders.dedup();
        assert_eq!(
            mem_orders.len(),
            original_len,
            "Duplicate mem_order in {label} songs"
        );
    }

    #[test]
    fn mem_orders_unique_per_type() {
        assert_unique_mem_orders(SongType::Regular, "Regular");
        assert_unique_mem_orders(SongType::Maestro, "Maestro");
        assert_unique_mem_orders(SongType::Handbell, "Handbell");
    }

    #[test]
    fn default_styles_valid() {
        for song in SONG_LIST {
            assert!(
                (song.default_style as usize) < STYLE_LIST.len(),
                "Song '{}' has invalid default_style {}",
                song.name,
                song.default_style
            );
        }
    }

    #[test]
    fn sentinel_instrument_exists() {
        assert_eq!(INSTRUMENT_LIST.len(), 68);
        assert_eq!(INSTRUMENT_LIST[67].name, "None");
        assert_eq!(INSTRUMENT_LIST[67].number, 67);
        assert!(!INSTRUMENT_LIST[67].in_menu);
    }
}
