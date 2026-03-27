use std::io::Write;

use midly::num::{u4, u7, u15, u28};
use midly::{Format, Header, MetaMessage, MidiMessage, Smf, Timing, TrackEvent, TrackEventKind};

use super::Results;

#[allow(clippy::too_many_lines)]
pub(super) fn test_midi(r: &mut Results) {
    println!("\n=== Section 7: MIDI ===");

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
                            vel: u7::from(80),
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

    let mut midi_bytes = Vec::new();
    if let Err(e) = smf.write_std(&mut midi_bytes) {
        r.fail("midi build synthetic", &e.to_string());
        return;
    }

    let mut midi_file = match tempfile::Builder::new().suffix(".mid").tempfile() {
        Ok(file) => file,
        Err(e) => {
            r.fail("midi create tempfile", &e.to_string());
            return;
        }
    };

    if let Err(e) = midi_file
        .write_all(&midi_bytes)
        .and_then(|()| midi_file.as_file_mut().flush())
    {
        r.fail("midi write tempfile", &e.to_string());
        return;
    }

    // Test prepare_midi (with fixes)
    match wm_core::midi::prepare_midi(midi_file.path()) {
        Err(e) => {
            r.fail("midi prepare_midi", &e.to_string());
            return;
        }
        Ok(prepared) => {
            r.ok(
                "midi prepare_midi",
                "2-track\u{2192}single-track, channel 0, NoteOn(vel=0)\u{2192}NoteOff",
            );

            // Test convert_to_sequence (with prepare)
            let output = prepared.path().with_extension("brseq");
            if let Err(e) = wm_core::midi::convert_to_sequence(midi_file.path(), &output) {
                r.fail("midi convert_to_sequence", &e.to_string());
            } else {
                let size = std::fs::metadata(&output).map_or(0, |m| m.len());
                r.ok(
                    "midi convert_to_sequence",
                    &format!(".brseq = {size} bytes"),
                );
            }

            // Test convert_to_sequence_raw (without prepare)
            let output_raw = prepared.path().with_extension("raw.brseq");
            if let Err(e) = wm_core::midi::convert_to_sequence_raw(midi_file.path(), &output_raw) {
                r.fail("midi convert_to_sequence_raw", &e.to_string());
            } else {
                let size = std::fs::metadata(&output_raw).map_or(0, |m| m.len());
                r.ok(
                    "midi convert_to_sequence_raw",
                    &format!(".brseq = {size} bytes"),
                );
            }
        }
    }

    // Test brsar::Rseq::from_midi directly (native, no GotaSequenceCmd)
    match brsar::Rseq::from_midi(&midi_bytes) {
        Err(e) => r.fail("brsar::Rseq::from_midi", &e.to_string()),
        Ok(rseq) => match rseq.to_bytes() {
            Err(e) => r.fail("brsar::Rseq::to_bytes", &e.to_string()),
            Ok(bytes) if !bytes.is_empty() => r.ok(
                "brsar::Rseq from_midi+to_bytes",
                &format!("{} bytes RSEQ", bytes.len()),
            ),
            Ok(_) => r.fail("brsar::Rseq from_midi+to_bytes", "empty output"),
        },
    }
}
