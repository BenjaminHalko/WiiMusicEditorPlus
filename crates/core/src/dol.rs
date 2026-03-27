use crate::{
    data::{SONG_LIST, STYLE_LIST},
    types::{InstrumentId, Song, SongType, StyleInstruments},
};

/// Beginning of the regular song data segment.
const SONG_REGULAR_OFFSET: u32 = 0x0059_C520;
/// Beginning of the maestro song data segment.
const SONG_MAESTRO_OFFSET: u32 = 0x005A_00EC;
/// Beginning of the handbell song data segment.
const SONG_HANDBELL_OFFSET: u32 = 0x005A_0AEC;
/// Beginning of the menu song data segment.
const SONG_MENU_OFFSET: u32 = 0x0059_6DAC;
/// Size of each song segment entry.
const SONG_SEGMENT_SIZE: u32 = 0xBC;
/// Relative offset to song time signature inside a song segment.
pub const SONG_SEGMENT_TIME_SIGNATURE: u32 = 0x20;
/// Relative offset to song length inside a song segment.
pub const SONG_SEGMENT_LENGTH: u32 = 0x24;
/// Relative offset to song tempo inside a song segment.
pub const SONG_SEGMENT_TEMPO: u32 = 0x28;
/// Relative offset to song default style inside a song segment.
pub const SONG_SEGMENT_DEFAULT_STYLE: u32 = 0x48;

/// Beginning of the style data segment.
const STYLE_SEGMENT_OFFSET: u32 = 0x0059_6758;
/// Size of each style segment entry.
const STYLE_SEGMENT_SIZE: u32 = 0x24;
/// Relative offset to style melody instrument.
const STYLE_SEGMENT_MELODY: u32 = 0x04;
/// Relative offset to style harmony instrument.
const STYLE_SEGMENT_HARMONY: u32 = 0x08;
/// Relative offset to style chord instrument.
const STYLE_SEGMENT_CHORD: u32 = 0x0C;
/// Relative offset to style bass instrument.
const STYLE_SEGMENT_BASS: u32 = 0x10;
/// Relative offset to style percussion 1 instrument.
const STYLE_SEGMENT_PERC1: u32 = 0x14;
/// Relative offset to style percussion 2 instrument.
const STYLE_SEGMENT_PERC2: u32 = 0x18;

/// Start of style execution code that must be neutralized.
const STYLE_CODE_BEGIN: u32 = 0x0036_F9A4;
/// End of style execution code that must be neutralized.
const STYLE_CODE_END: u32 = 0x0037_01CC;
/// Start of default-style execution code that must be neutralized.
const DEFAULT_STYLE_CODE_BEGIN: u32 = 0x003D_4ACC;
/// End of default-style execution code that must be neutralized.
const DEFAULT_STYLE_CODE_END: u32 = 0x003D_4B64;

/// PowerPC `li r0, 0` used for style execution patching.
const STYLE_EXECUTION_PATCH: u32 = 0x3811_0000;
/// DOL encoding for "no instrument".
const NO_INSTRUMENT_SENTINEL: u32 = 0xFFFF_FFFF;

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct MainDol {
    data: Vec<u8>,
}

impl MainDol {
    #[must_use]
    pub fn parse(data: Vec<u8>) -> Self {
        Self { data }
    }

    #[must_use]
    pub fn as_bytes(&self) -> &[u8] {
        &self.data
    }

    #[must_use]
    pub fn read_u32(&self, offset: usize) -> u32 {
        let Some(end) = offset.checked_add(0x04) else {
            panic!("Offset overflow reading u32 at {offset:#X}");
        };
        assert!(
            end <= self.data.len(),
            "Out-of-bounds read_u32 at {offset:#X} (len {:#X})",
            self.data.len()
        );

        let mut bytes = [0_u8; 0x04];
        bytes.copy_from_slice(&self.data[offset..end]);
        u32::from_be_bytes(bytes)
    }

    pub fn write_u32(&mut self, offset: usize, value: u32) {
        let Some(end) = offset.checked_add(0x04) else {
            panic!("Offset overflow writing u32 at {offset:#X}");
        };
        assert!(
            end <= self.data.len(),
            "Out-of-bounds write_u32 at {offset:#X} (len {:#X})",
            self.data.len()
        );

        self.data[offset..end].copy_from_slice(&value.to_be_bytes());
    }

    #[must_use]
    pub fn read_song_info(&self, song: &Song, segment: u8) -> u32 {
        let offset = Self::song_offset(song) + usize::from(segment);
        self.read_u32(offset)
    }

    pub fn write_song_info(&mut self, song: &Song, segment: u8, value: u32) {
        let offset = Self::song_offset(song) + usize::from(segment);
        self.write_u32(offset, value);
    }

    #[must_use]
    pub fn read_style_instruments(&self, style_index: usize) -> StyleInstruments {
        let offset = Self::style_offset(style_index);
        StyleInstruments([
            self.read_style_slot(offset + usize_from_u32(STYLE_SEGMENT_MELODY)),
            self.read_style_slot(offset + usize_from_u32(STYLE_SEGMENT_HARMONY)),
            self.read_style_slot(offset + usize_from_u32(STYLE_SEGMENT_CHORD)),
            self.read_style_slot(offset + usize_from_u32(STYLE_SEGMENT_BASS)),
            self.read_style_slot(offset + usize_from_u32(STYLE_SEGMENT_PERC1)),
            self.read_style_slot(offset + usize_from_u32(STYLE_SEGMENT_PERC2)),
        ])
    }

    pub fn write_style_instruments(&mut self, style_index: usize, instruments: &StyleInstruments) {
        let offset = Self::style_offset(style_index);
        self.write_style_slot(
            offset + usize_from_u32(STYLE_SEGMENT_MELODY),
            InstrumentId(instruments[0]),
        );
        self.write_style_slot(
            offset + usize_from_u32(STYLE_SEGMENT_HARMONY),
            InstrumentId(instruments[1]),
        );
        self.write_style_slot(
            offset + usize_from_u32(STYLE_SEGMENT_CHORD),
            InstrumentId(instruments[2]),
        );
        self.write_style_slot(
            offset + usize_from_u32(STYLE_SEGMENT_BASS),
            InstrumentId(instruments[3]),
        );
        self.write_style_slot(
            offset + usize_from_u32(STYLE_SEGMENT_PERC1),
            InstrumentId(instruments[4]),
        );
        self.write_style_slot(
            offset + usize_from_u32(STYLE_SEGMENT_PERC2),
            InstrumentId(instruments[5]),
        );
    }

    pub fn remove_style_execution(&mut self) {
        if self.remove_code(STYLE_CODE_BEGIN, STYLE_CODE_END) {
            for (index, style) in STYLE_LIST.iter().enumerate() {
                self.write_style_instruments(index, &style.instruments);
            }
        }

        if self.remove_code(DEFAULT_STYLE_CODE_BEGIN, DEFAULT_STYLE_CODE_END) {
            for song in SONG_LIST {
                if song.default_style != u8::MAX {
                    self.write_song_info(
                        song,
                        SONG_SEGMENT_DEFAULT_STYLE as u8,
                        u32::from(song.default_style),
                    );
                }
            }
        }
    }

    fn style_offset(style_index: usize) -> usize {
        usize_from_u32(STYLE_SEGMENT_OFFSET) + style_index * usize_from_u32(STYLE_SEGMENT_SIZE)
    }

    fn song_offset(song: &Song) -> usize {
        let base_offset = match song.song_type {
            SongType::Regular => SONG_REGULAR_OFFSET,
            SongType::Maestro => SONG_MAESTRO_OFFSET,
            SongType::Handbell => SONG_HANDBELL_OFFSET,
            SongType::Menu => SONG_MENU_OFFSET,
        };

        usize_from_u32(base_offset)
            + usize::from(song.mem_order) * usize_from_u32(SONG_SEGMENT_SIZE)
    }

    #[must_use]
    fn remove_code(&mut self, min_offset: u32, max_offset: u32) -> bool {
        let mut replaced = false;
        let patch_bytes = STYLE_EXECUTION_PATCH.to_be_bytes();
        let scan_end = usize_from_u32(max_offset).min(self.data.len().saturating_sub(0x03));
        let scan_begin = usize_from_u32(min_offset);

        if scan_begin >= scan_end {
            return false;
        }

        for offset in (scan_begin..scan_end).step_by(0x04) {
            if self.data[offset] >= 0x90 {
                self.data[offset..offset + 0x04].copy_from_slice(&patch_bytes);
                replaced = true;
            }
        }

        replaced
    }

    #[must_use]
    fn read_style_slot(&self, offset: usize) -> u8 {
        let raw = self.read_u32(offset);
        let instrument = InstrumentId::from_dol_u32(raw);
        instrument.0
    }

    fn write_style_slot(&mut self, offset: usize, instrument: InstrumentId) {
        let value = if instrument.0 == 67 {
            NO_INSTRUMENT_SENTINEL
        } else {
            instrument.to_dol_u32()
        };
        self.write_u32(offset, value);
    }
}

const fn usize_from_u32(value: u32) -> usize {
    value as usize
}

#[cfg(test)]
mod tests {
    use super::*;

    fn base_test_dol() -> MainDol {
        MainDol::parse(vec![0_u8; usize_from_u32(SONG_HANDBELL_OFFSET) + 0x2000])
    }

    #[test]
    fn test_sentinel_write_read() {
        let id = InstrumentId(67);
        assert_eq!(id.to_dol_u32(), 0xFFFF_FFFF);
        assert_eq!(InstrumentId::from_dol_u32(0xFFFF_FFFF).0, 67);
    }

    #[test]
    fn test_offset_constants_are_hex() {
        assert_eq!(SONG_REGULAR_OFFSET, 0x0059_C520);
        assert_eq!(SONG_MAESTRO_OFFSET, 0x005A_00EC);
        assert_eq!(SONG_HANDBELL_OFFSET, 0x005A_0AEC);
        assert_eq!(SONG_MENU_OFFSET, 0x0059_6DAC);
        assert_eq!(SONG_SEGMENT_SIZE, 0xBC);
        assert_eq!(SONG_SEGMENT_TIME_SIGNATURE, 0x20);
        assert_eq!(SONG_SEGMENT_LENGTH, 0x24);
        assert_eq!(SONG_SEGMENT_TEMPO, 0x28);
        assert_eq!(SONG_SEGMENT_DEFAULT_STYLE, 0x48);
        assert_eq!(STYLE_SEGMENT_OFFSET, 0x0059_6758);
        assert_eq!(STYLE_SEGMENT_SIZE, 0x24);
        assert_eq!(STYLE_SEGMENT_MELODY, 0x04);
        assert_eq!(STYLE_SEGMENT_HARMONY, 0x08);
        assert_eq!(STYLE_SEGMENT_CHORD, 0x0C);
        assert_eq!(STYLE_SEGMENT_BASS, 0x10);
        assert_eq!(STYLE_SEGMENT_PERC1, 0x14);
        assert_eq!(STYLE_SEGMENT_PERC2, 0x18);
        assert_eq!(STYLE_CODE_BEGIN, 0x0036_F9A4);
        assert_eq!(STYLE_CODE_END, 0x0037_01CC);
        assert_eq!(DEFAULT_STYLE_CODE_BEGIN, 0x003D_4ACC);
        assert_eq!(DEFAULT_STYLE_CODE_END, 0x003D_4B64);
    }

    #[test]
    fn test_read_write_song_info_round_trip() {
        let mut dol = base_test_dol();
        let song = &SONG_LIST[0];
        dol.write_song_info(song, SONG_SEGMENT_TEMPO as u8, 0x1122_3344);
        assert_eq!(
            dol.read_song_info(song, SONG_SEGMENT_TEMPO as u8),
            0x1122_3344
        );
    }

    #[test]
    fn test_read_write_style_instruments_round_trip() {
        let mut dol = base_test_dol();
        let style = StyleInstruments([0x01, 0x02, 67, 0x04, 0x05, 0x06]);
        dol.write_style_instruments(0, &style);
        assert_eq!(dol.read_style_instruments(0), style);
        assert_eq!(
            dol.read_u32(
                usize_from_u32(STYLE_SEGMENT_OFFSET) + usize_from_u32(STYLE_SEGMENT_CHORD)
            ),
            0xFFFF_FFFF
        );
    }
}
