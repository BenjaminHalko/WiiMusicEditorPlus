use std::fs;
use std::path::{Path, PathBuf};

use midly::{MetaMessage, Smf, Timing, TrackEventKind};

use brsar::{Brsar, Rseq};

use crate::{
    data::STYLE_LIST,
    dol::{
        MainDol, SONG_SEGMENT_DEFAULT_STYLE, SONG_SEGMENT_LENGTH, SONG_SEGMENT_TEMPO,
        SONG_SEGMENT_TIME_SIGNATURE,
    },
    message,
    rom_folder::RomFolder,
    types::{Song, SongType, Style, StyleInstruments, WmError},
};

pub const BRSAR_GROUP_REGULAR: usize = 0x02;
pub const BRSAR_GROUP_MAESTRO: usize = 0x15;
pub const BRSAR_GROUP_HANDBELL: usize = 0x17;
pub const BRSAR_GROUP_MENU: usize = 0x22;

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SongData {
    pub length: u32,
    pub tempo: u32,
    pub time_signature: u32,
    pub name: String,
    pub description: String,
    pub genre: String,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum SequenceKind {
    Song,
    Score,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct BrsarTarget {
    pub group: usize,
    pub item: usize,
    pub sequence: SequenceKind,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct SongMetadata {
    pub length: u32,
    pub tempo: Option<u32>,
    pub time_signature: Option<u32>,
}

impl SongMetadata {
    /// Parses song metadata from raw bytes, auto-detecting MIDI (`MThd`) or BRSEQ (`RSEQ`) by magic.
    ///
    /// `tempo` is `None` when no tempo event is present. `time_signature` is `None` when absent or
    /// when the input is a BRSEQ (RSEQ has no time-signature concept).
    ///
    /// # Errors
    /// Returns `WmError::Parse` if the data is not valid MIDI or BRSEQ, or the magic is unrecognized.
    pub fn from_bytes(data: &[u8]) -> Result<Self, WmError> {
        if data.starts_with(b"MThd") {
            Self::parse_midi(data)
        } else if data.starts_with(b"RSEQ") {
            Self::parse_rseq(data)
        } else {
            Err(WmError::Parse {
                file: "score".to_string(),
                offset: 0x00,
                message: "unrecognized format: expected MIDI (MThd) or BRSEQ (RSEQ)".to_string(),
            })
        }
    }

    fn parse_midi(data: &[u8]) -> Result<Self, WmError> {
        let smf = Smf::parse(data).map_err(|error| WmError::Parse {
            file: "score".to_string(),
            offset: 0x00,
            message: error.to_string(),
        })?;

        let ticks_per_beat = match smf.header.timing {
            Timing::Metrical(value) => u16::from(value),
            Timing::Timecode(_, _) => 0x01,
        };

        let mut max_ticks: u64 = 0x00;
        let mut tempo_microseconds_per_beat: Option<u32> = None;
        let mut time_signature_numerator: Option<u8> = None;

        for track in &smf.tracks {
            let mut running_ticks: u64 = 0x00;
            for event in track {
                running_ticks += u64::from(event.delta.as_int());
                if let TrackEventKind::Meta(meta) = event.kind {
                    if tempo_microseconds_per_beat.is_none()
                        && let MetaMessage::Tempo(tempo) = meta
                    {
                        tempo_microseconds_per_beat = Some(tempo.as_int());
                    }
                    if time_signature_numerator.is_none()
                        && let MetaMessage::TimeSignature(numerator, _, _, _) = meta
                    {
                        time_signature_numerator = Some(numerator);
                    }
                }
            }
            max_ticks = max_ticks.max(running_ticks);
        }

        let tempo = tempo_microseconds_per_beat.map(|micros| {
            if micros == 0x00 {
                0x78
            } else {
                0x03_93_87_00_u32 / micros
            }
        });

        let length = if ticks_per_beat == 0x00 {
            u32::try_from(max_ticks).unwrap_or(u32::MAX)
        } else {
            let max_beats = max_ticks / u64::from(ticks_per_beat);
            u32::try_from(max_beats).unwrap_or(u32::MAX)
        };

        Ok(Self {
            length,
            tempo,
            time_signature: time_signature_numerator.map(u32::from),
        })
    }

    fn parse_rseq(data: &[u8]) -> Result<Self, WmError> {
        let rseq = Rseq::from_bytes(data).map_err(|error| WmError::Parse {
            file: "score".to_string(),
            offset: 0x00,
            message: error.to_string(),
        })?;
        let midi = rseq.to_midi().map_err(|error| WmError::Parse {
            file: "score".to_string(),
            offset: 0x00,
            message: error.to_string(),
        })?;
        Self::parse_midi(&midi)
    }
}

/// Replaces the active song and score data for a song.
///
/// # Errors
/// Returns `WmError::Io` if the BRSAR or DOL updates fail.
pub fn replace_song(
    rom_folder: &mut RomFolder,
    song: &Song,
    score_brseq: &[u8],
    song_brseq: &[u8],
    metadata: SongMetadata,
) -> Result<(), WmError> {
    let mut brsar = Brsar::parse(rom_folder.brsar.clone())?;
    let backup_brsar = load_backup_brsar(rom_folder)?;

    for target in brsar_targets(song) {
        let requested = match target.sequence {
            SequenceKind::Song => song_brseq,
            SequenceKind::Score => score_brseq,
        };

        let replacement = if requested.is_empty() {
            backup_brsar.get_song_in_group(target.group, target.item)?
        } else {
            requested.to_vec()
        };

        brsar.replace_song_in_group(target.group, target.item, &replacement)?;
    }
    rom_folder.brsar = brsar.as_bytes().to_vec();

    if song.song_type != SongType::Menu {
        let mut main_dol = MainDol::parse(rom_folder.main_dol.clone());
        main_dol.write_song_info(song, SONG_SEGMENT_LENGTH as u8, metadata.length);
        main_dol.write_song_info(
            song,
            SONG_SEGMENT_TEMPO as u8,
            metadata.tempo.unwrap_or(0x78),
        );
        main_dol.write_song_info(
            song,
            SONG_SEGMENT_TIME_SIGNATURE as u8,
            metadata.time_signature.unwrap_or(0x04),
        );
        rom_folder.main_dol = main_dol.as_bytes().to_vec();
    }

    Ok(())
}

/// Replaces the instrument data for a style.
///
/// # Errors
/// Returns `WmError::InvalidStyle` if the style cannot be resolved, or
/// `WmError::Io` if the DOL update fails.
pub fn replace_style(
    rom_folder: &mut RomFolder,
    style: &Style,
    instruments: &StyleInstruments,
) -> Result<(), WmError> {
    let style_index = resolve_style_index(style)?;
    let mut main_dol = MainDol::parse(rom_folder.main_dol.clone());
    main_dol.write_style_instruments(style_index, instruments);
    rom_folder.main_dol = main_dol.as_bytes().to_vec();
    Ok(())
}

/// Replaces a song's default style assignment.
///
/// # Errors
/// Returns `WmError::InvalidStyle` if the style cannot be resolved, or
/// `WmError::Io` if the DOL update fails.
pub fn replace_default_style(
    rom_folder: &mut RomFolder,
    song: &Song,
    style: &Style,
) -> Result<(), WmError> {
    let style_index = resolve_style_index(style)?;
    let mut main_dol = MainDol::parse(rom_folder.main_dol.clone());
    main_dol.write_song_info(song, SONG_SEGMENT_DEFAULT_STYLE as u8, style_index as u32);
    rom_folder.main_dol = main_dol.as_bytes().to_vec();
    Ok(())
}

/// Replaces a song's name, description, and genre in `message.carc`.
///
/// # Errors
/// Returns `WmError::Io` if the CARC cannot be read or written, or
/// `WmError::Parse` if no `message.carc` is found in the ROM folder.
pub fn replace_song_text(
    rom_folder: &RomFolder,
    song: &Song,
    name: &str,
    description: &str,
    genre: &str,
) -> Result<(), WmError> {
    if song.bmg_name_id() == 0 {
        return Ok(());
    }

    let carc_path = message::find_message_carc(&rom_folder.text_dir)?;
    let carc_bytes = fs::read(&carc_path)?;
    let mut msgs = carc::WiiMessages::from_bytes(&carc_bytes)
        .map_err(|e| WmError::Io(std::io::Error::other(e.to_string())))?;

    let mut changed = false;

    for (id, text) in [
        (song.bmg_name_id(), name),
        (song.bmg_desc_id(), description),
        (song.bmg_genre_id(), genre),
    ] {
        if id == 0 {
            continue;
        }
        if let Some(idx) = msgs.entries().iter().position(|e| e.id == id)
            && msgs.entries()[idx].text != text
        {
            msgs.set_text(idx, text)
                .map_err(|e| WmError::Io(std::io::Error::other(e.to_string())))?;
            changed = true;
        }
    }

    if changed {
        fs::write(
            &carc_path,
            msgs.to_bytes()
                .map_err(|e| WmError::Io(std::io::Error::other(e.to_string())))?,
        )?;
    }

    Ok(())
}

/// Reads the backed-up song data and text for a song.
///
/// # Errors
/// Returns `WmError::Io` if the backup DOL or text files cannot be read.
pub fn get_original_song(rom_folder: &RomFolder, song: &Song) -> Result<SongData, WmError> {
    let backup_dol_bytes = fs::read(rom_folder.dol_backup_path())?;
    let backup_dol = MainDol::parse(backup_dol_bytes);
    let text = read_song_text_from_backup(rom_folder, song)?;

    Ok(SongData {
        length: backup_dol.read_song_info(song, SONG_SEGMENT_LENGTH as u8),
        tempo: backup_dol.read_song_info(song, SONG_SEGMENT_TEMPO as u8),
        time_signature: backup_dol.read_song_info(song, SONG_SEGMENT_TIME_SIGNATURE as u8),
        name: text.name,
        description: text.description,
        genre: text.genre,
    })
}

#[must_use]
pub fn brsar_targets(song: &Song) -> Vec<BrsarTarget> {
    let mem_order = usize::from(song.mem_order);

    match song.song_type {
        SongType::Regular => vec![
            BrsarTarget {
                group: BRSAR_GROUP_REGULAR,
                item: mem_order * 0x02,
                sequence: SequenceKind::Song,
            },
            BrsarTarget {
                group: BRSAR_GROUP_REGULAR,
                item: mem_order * 0x02 + 0x01,
                sequence: SequenceKind::Score,
            },
        ],
        SongType::Maestro => vec![BrsarTarget {
            group: BRSAR_GROUP_MAESTRO,
            item: mem_order + 0x02,
            sequence: SequenceKind::Song,
        }],
        SongType::Handbell => (0x02..=0x06)
            .map(|offset| BrsarTarget {
                group: BRSAR_GROUP_HANDBELL,
                item: mem_order * 0x05 + offset,
                sequence: SequenceKind::Song,
            })
            .collect(),
        SongType::Menu => {
            let mut targets = vec![BrsarTarget {
                group: BRSAR_GROUP_MENU,
                item: 0x00,
                sequence: SequenceKind::Song,
            }];
            targets.extend((0x01..=0x06).map(|item| BrsarTarget {
                group: BRSAR_GROUP_MENU,
                item,
                sequence: SequenceKind::Score,
            }));
            targets
        }
    }
}

/// Restores a style's instruments from the backup DOL.
///
/// # Errors
/// Returns `WmError::Parse` if the style cannot be resolved.
pub fn reset_style(rom_folder: &mut RomFolder, style: &Style) -> Result<(), WmError> {
    let style_index = resolve_style_index(style)?;
    let mut main_dol = MainDol::parse(rom_folder.main_dol.clone());
    main_dol.write_style_instruments(style_index, &STYLE_LIST[style_index].instruments);
    rom_folder.main_dol = main_dol.as_bytes().to_vec();
    Ok(())
}

fn resolve_style_index(style: &Style) -> Result<usize, WmError> {
    STYLE_LIST
        .iter()
        .position(|candidate| {
            candidate.name == style.name
                && candidate.style_type == style.style_type
                && candidate.instruments == style.instruments
        })
        .ok_or_else(|| WmError::Parse {
            file: "data".to_string(),
            offset: 0,
            message: format!("could not resolve style '{}'", style.name),
        })
}

fn load_backup_brsar(rom_folder: &RomFolder) -> Result<Brsar, WmError> {
    let backup_bytes = fs::read(rom_folder.brsar_backup_path())?;
    Ok(Brsar::parse(backup_bytes)?)
}

fn read_song_text_from_backup(rom_folder: &RomFolder, song: &Song) -> Result<SongData, WmError> {
    read_song_text_impl(rom_folder, song, true)
}

fn read_song_text_impl(
    rom_folder: &RomFolder,
    song: &Song,
    from_backup: bool,
) -> Result<SongData, WmError> {
    let path = locate_message_text_file(&rom_folder.text_dir, from_backup)?;
    let entries = message::parse_text_file(&path)?;
    let name = entries
        .iter()
        .find(|entry| entry.text == song.name)
        .map_or_else(|| song.name.to_string(), |entry| entry.text.clone());

    Ok(SongData {
        length: 0x00,
        tempo: 0x00,
        time_signature: 0x00,
        name,
        description: String::new(),
        genre: String::new(),
    })
}

fn locate_message_text_file(text_dir: &Path, from_backup: bool) -> Result<PathBuf, WmError> {
    let mut candidates = Vec::new();
    for region in fs::read_dir(text_dir)? {
        let region_path = region?.path();
        let normal = region_path.join("Message/message.d/new_music_message.txt");
        let backup = region_path.join("Message/message.d/new_music_message.txt.backup");

        if from_backup {
            if backup.is_file() {
                candidates.push(backup);
            }
        } else if normal.is_file() {
            candidates.push(normal);
        }
    }

    candidates.into_iter().next().ok_or_else(|| WmError::Parse {
        file: text_dir.display().to_string(),
        offset: 0x00,
        message: "message text file was not found".to_string(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn editor_item_indices_regular_match_python() {
        let song = Song {
            name: "Regular",
            song_type: SongType::Regular,
            mem_order: 0x03,
        };
        let targets = brsar_targets(&song);
        assert_eq!(
            targets,
            vec![
                BrsarTarget {
                    group: BRSAR_GROUP_REGULAR,
                    item: 0x06,
                    sequence: SequenceKind::Song,
                },
                BrsarTarget {
                    group: BRSAR_GROUP_REGULAR,
                    item: 0x07,
                    sequence: SequenceKind::Score,
                },
            ]
        );
    }

    #[test]
    fn editor_item_indices_maestro_match_python() {
        let song = Song {
            name: "Maestro",
            song_type: SongType::Maestro,
            mem_order: 0x04,
        };
        let targets = brsar_targets(&song);
        assert_eq!(
            targets,
            vec![BrsarTarget {
                group: BRSAR_GROUP_MAESTRO,
                item: 0x06,
                sequence: SequenceKind::Song,
            }]
        );
    }

    #[test]
    fn editor_item_indices_handbell_match_python() {
        let song = Song {
            name: "Handbell",
            song_type: SongType::Handbell,
            mem_order: 0x02,
        };
        let targets = brsar_targets(&song);
        assert_eq!(
            targets,
            vec![
                BrsarTarget {
                    group: BRSAR_GROUP_HANDBELL,
                    item: 0x0C,
                    sequence: SequenceKind::Song,
                },
                BrsarTarget {
                    group: BRSAR_GROUP_HANDBELL,
                    item: 0x0D,
                    sequence: SequenceKind::Song,
                },
                BrsarTarget {
                    group: BRSAR_GROUP_HANDBELL,
                    item: 0x0E,
                    sequence: SequenceKind::Song,
                },
                BrsarTarget {
                    group: BRSAR_GROUP_HANDBELL,
                    item: 0x0F,
                    sequence: SequenceKind::Song,
                },
                BrsarTarget {
                    group: BRSAR_GROUP_HANDBELL,
                    item: 0x10,
                    sequence: SequenceKind::Song,
                },
            ]
        );
    }

    #[test]
    fn editor_item_indices_menu_match_python() {
        let song = Song {
            name: "Menu",
            song_type: SongType::Menu,
            mem_order: 0x00,
        };
        let targets = brsar_targets(&song);
        assert_eq!(
            targets,
            vec![
                BrsarTarget {
                    group: BRSAR_GROUP_MENU,
                    item: 0x00,
                    sequence: SequenceKind::Song,
                },
                BrsarTarget {
                    group: BRSAR_GROUP_MENU,
                    item: 0x01,
                    sequence: SequenceKind::Score,
                },
                BrsarTarget {
                    group: BRSAR_GROUP_MENU,
                    item: 0x02,
                    sequence: SequenceKind::Score,
                },
                BrsarTarget {
                    group: BRSAR_GROUP_MENU,
                    item: 0x03,
                    sequence: SequenceKind::Score,
                },
                BrsarTarget {
                    group: BRSAR_GROUP_MENU,
                    item: 0x04,
                    sequence: SequenceKind::Score,
                },
                BrsarTarget {
                    group: BRSAR_GROUP_MENU,
                    item: 0x05,
                    sequence: SequenceKind::Score,
                },
                BrsarTarget {
                    group: BRSAR_GROUP_MENU,
                    item: 0x06,
                    sequence: SequenceKind::Score,
                },
            ]
        );
    }
}
