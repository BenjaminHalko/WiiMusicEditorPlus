use std::io::Write;
use std::path::Path;

use midly::num::u7;
use midly::{Format, MidiMessage, Smf, TrackEventKind};
use tempfile::{Builder, NamedTempFile};

use crate::types::WmError;

/// Loads a MIDI file and fixes common compatibility issues:
/// merges multiple tracks into one, remaps all channels to 0,
/// and converts `NoteOn(vel=0)` events to explicit `NoteOff`.
/// The original file is never modified — output is a temporary file.
///
/// # Errors
/// Returns [`WmError`] if the MIDI file cannot be read, parsed, or written.
pub fn prepare_midi(input: &Path) -> Result<NamedTempFile, WmError> {
    let bytes = std::fs::read(input)?;
    let mut smf = Smf::parse(&bytes).map_err(|e| WmError::Parse {
        file: input.to_string_lossy().into_owned(),
        offset: 0x0,
        message: e.to_string(),
    })?;

    let mut merged_track = Vec::new();
    for track in smf.tracks.drain(..) {
        merged_track.extend(track);
    }

    for event in &mut merged_track {
        if let TrackEventKind::Midi { channel, message } = &mut event.kind {
            *channel = 0.into();
            if let MidiMessage::NoteOn { key, vel } = message
                && u8::from(*vel) == 0x00
            {
                let k = *key;
                *message = MidiMessage::NoteOff {
                    key: k,
                    vel: u7::from(0),
                };
            }
        }
    }

    smf.header.format = Format::SingleTrack;
    smf.tracks = vec![merged_track];

    let mut out = Builder::new().suffix(".mid").tempfile()?;
    smf.write_std(out.as_file_mut())
        .map_err(|e| WmError::Parse {
            file: input.to_string_lossy().into_owned(),
            offset: 0x0,
            message: e.to_string(),
        })?;
    out.as_file_mut().flush()?;
    Ok(out)
}

/// Runs the MIDI through [`prepare_midi`] first to fix compatibility issues,
/// then converts to a Wii Music BRSEQ sequence file.
/// The original MIDI is never modified.
///
/// # Errors
/// Returns [`WmError`] if preparation, conversion, or file I/O fails.
pub fn convert_to_sequence(midi: &Path, output: &Path) -> Result<(), WmError> {
    let prepared = prepare_midi(midi)?;
    midi_to_brseq(prepared.path(), output)
}

/// Converts a MIDI file directly to a Wii Music BRSEQ sequence file,
/// skipping any preparation or modification. Use when the MIDI is already
/// compatible and you want to preserve it exactly as-is.
///
/// # Errors
/// Returns [`WmError`] if conversion or file I/O fails.
pub fn convert_to_sequence_raw(midi: &Path, output: &Path) -> Result<(), WmError> {
    midi_to_brseq(midi, output)
}

fn midi_to_brseq(midi: &Path, output: &Path) -> Result<(), WmError> {
    let midi_bytes = std::fs::read(midi)?;
    let rseq = brsar::Rseq::from_midi(&midi_bytes)?;
    let brseq_bytes = rseq.to_bytes()?;
    std::fs::write(output, &brseq_bytes)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use midly::num::{u4, u15, u28};
    use midly::{Header, MetaMessage, Timing, TrackEvent};
    use std::error::Error;

    fn two_track_midi() -> Vec<u8> {
        let smf = Smf {
            header: Header {
                format: Format::Parallel,
                timing: Timing::Metrical(u15::from(0x01E0)),
            },
            tracks: vec![
                vec![
                    TrackEvent {
                        delta: u28::from(0),
                        kind: TrackEventKind::Midi {
                            channel: u4::from(1),
                            message: MidiMessage::NoteOn {
                                key: u7::from(60),
                                vel: u7::from(100),
                            },
                        },
                    },
                    TrackEvent {
                        delta: u28::from(0x78),
                        kind: TrackEventKind::Midi {
                            channel: u4::from(1),
                            message: MidiMessage::NoteOn {
                                key: u7::from(60),
                                vel: u7::from(0),
                            },
                        },
                    },
                    TrackEvent {
                        delta: u28::from(0),
                        kind: TrackEventKind::Meta(MetaMessage::EndOfTrack),
                    },
                ],
                vec![
                    TrackEvent {
                        delta: u28::from(0),
                        kind: TrackEventKind::Midi {
                            channel: u4::from(2),
                            message: MidiMessage::NoteOn {
                                key: u7::from(64),
                                vel: u7::from(90),
                            },
                        },
                    },
                    TrackEvent {
                        delta: u28::from(0),
                        kind: TrackEventKind::Meta(MetaMessage::EndOfTrack),
                    },
                ],
            ],
        };
        let mut bytes = Vec::new();
        smf.write_std(&mut bytes).unwrap();
        bytes
    }

    fn write_midi_tempfile(bytes: &[u8]) -> NamedTempFile {
        let mut f = Builder::new().suffix(".mid").tempfile().unwrap();
        f.write_all(bytes).unwrap();
        f.as_file_mut().flush().unwrap();
        f
    }

    #[test]
    fn test_prepare_midi_single_track_channel_zero() -> Result<(), Box<dyn Error>> {
        let f = write_midi_tempfile(&two_track_midi());
        let out = prepare_midi(f.path())?;
        let bytes = std::fs::read(out.path())?;
        let result = Smf::parse(&bytes)?;
        assert_eq!(result.header.format, Format::SingleTrack);
        assert_eq!(result.tracks.len(), 1);
        for event in &result.tracks[0] {
            if let TrackEventKind::Midi { channel, .. } = &event.kind {
                assert_eq!(u8::from(*channel), 0);
            }
        }
        Ok(())
    }

    #[test]
    fn test_prepare_midi_note_on_vel_zero_becomes_note_off() -> Result<(), Box<dyn Error>> {
        let f = write_midi_tempfile(&two_track_midi());
        let out = prepare_midi(f.path())?;
        let bytes = std::fs::read(out.path())?;
        let result = Smf::parse(&bytes)?;
        for event in &result.tracks[0] {
            if let TrackEventKind::Midi { message, .. } = &event.kind {
                if let MidiMessage::NoteOn { vel, .. } = message {
                    assert_ne!(u8::from(*vel), 0, "NoteOn(vel=0) must become NoteOff");
                }
            }
        }
        Ok(())
    }

    #[test]
    fn test_prepare_midi_does_not_modify_original() -> Result<(), Box<dyn Error>> {
        let bytes = two_track_midi();
        let f = write_midi_tempfile(&bytes);
        let _out = prepare_midi(f.path())?;
        assert_eq!(
            std::fs::read(f.path())?,
            bytes,
            "original file must be unchanged"
        );
        Ok(())
    }
}
