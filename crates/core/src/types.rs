use std::ops::{Index, IndexMut};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum SongType {
    Regular,
    Maestro,
    Handbell,
    Menu,
}

// Lookup tables mapping mem_order → effective BMG index for Maestro/Handbell songs.
const MAESTRO_ORDER: [u8; 5] = [0, 4, 2, 3, 1];
const HANDBELL_ORDER: [u8; 5] = [0, 2, 3, 1, 4];

#[derive(Clone, Debug, PartialEq)]
pub struct Song {
    pub name: &'static str,
    pub song_type: SongType,
    pub mem_order: u8,
}

impl Song {
    const fn bmg_id(&self, regular: u32, maestro: u32, handbell: u32) -> u32 {
        let mem = self.mem_order as u32;
        match self.song_type {
            SongType::Regular => (regular + mem) << 8,
            SongType::Maestro => (maestro + MAESTRO_ORDER[self.mem_order as usize] as u32) << 8,
            SongType::Handbell => (handbell + HANDBELL_ORDER[self.mem_order as usize] as u32) << 8,
            SongType::Menu => 0,
        }
    }

    /// BMG entry ID for this song's name in `message.carc`. `0` = no entry (Menu).
    #[must_use]
    pub const fn bmg_name_id(&self) -> u32 {
        self.bmg_id(0xC8, 0xFA, 0xFF)
    }

    /// BMG entry ID for this song's description. `0` = no entry (Menu).
    #[must_use]
    pub const fn bmg_desc_id(&self) -> u32 {
        self.bmg_id(0x190, 0x1C2, 0x1C7)
    }

    /// BMG entry ID for this song's genre. `0` = no entry (Menu).
    #[must_use]
    pub const fn bmg_genre_id(&self) -> u32 {
        self.bmg_id(0x12C, 0x15E, 0x163)
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum StyleType {
    Global,
    QuickJam,
    SongSpecific,
    Menu,
    Unused,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct StyleInstruments(pub [u8; 6]);

impl Index<usize> for StyleInstruments {
    type Output = u8;

    fn index(&self, index: usize) -> &Self::Output {
        &self.0[index]
    }
}

impl IndexMut<usize> for StyleInstruments {
    fn index_mut(&mut self, index: usize) -> &mut Self::Output {
        &mut self.0[index]
    }
}

#[derive(Clone, Debug, PartialEq)]
pub struct Style {
    pub name: &'static str,
    pub style_type: StyleType,
    pub instruments: StyleInstruments,
}

#[derive(Clone, Debug, PartialEq)]
pub struct Instrument {
    pub name: &'static str,
    pub number: u8,
    pub in_menu: bool,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Region {
    US,
    EU,
    JP,
    KR,
}

impl Region {
    #[must_use]
    pub fn game_id_prefix(&self) -> &'static str {
        match self {
            Self::US => "R64E",
            Self::EU => "R64P",
            Self::JP => "R64J",
            Self::KR => "R64K",
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Language {
    English,
    French,
    Spanish,
    German,
    Italian,
    Japanese,
    Korean,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct InstrumentId(pub u8);

impl InstrumentId {
    #[must_use]
    pub fn to_dol_u32(self) -> u32 {
        if self.0 == 67 {
            0xFFFF_FFFF
        } else {
            u32::from(self.0)
        }
    }

    #[must_use]
    pub fn from_dol_u32(val: u32) -> Self {
        if val == 0xFFFF_FFFF {
            Self(67)
        } else {
            Self(val as u8)
        }
    }
}

#[derive(Debug, thiserror::Error)]
pub enum WmError {
    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),
    #[error("Parse error in {file} at offset {offset:#x}: {message}")]
    Parse {
        file: String,
        offset: usize,
        message: String,
    },
    #[error("Checksum mismatch: expected {expected}, got {actual}")]
    ChecksumMismatch { expected: String, actual: String },
    #[error("Region not supported: {0}")]
    UnsupportedRegion(String),
    #[error("Invalid instrument index: {0}")]
    InvalidInstrument(u8),
    #[error("BRSAR error: {0}")]
    Brsar(#[from] brsar::BrsarError),
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_instrument_sentinel() {
        assert_eq!(InstrumentId(67).to_dol_u32(), 0xFFFF_FFFF);
        assert_eq!(InstrumentId::from_dol_u32(0xFFFF_FFFF).0, 67);
    }

    #[test]
    fn test_instrument_normal() {
        assert_eq!(InstrumentId(5).to_dol_u32(), 5);
    }

    #[test]
    fn test_region_game_id() {
        assert_eq!(Region::US.game_id_prefix(), "R64E");
    }
}
