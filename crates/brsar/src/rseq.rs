use std::collections::{BTreeSet, HashMap};

use midly::num::{u4, u7, u15, u24, u28};
use midly::{
    Format, Header, MetaMessage, MidiMessage, PitchBend, Smf, Timing, TrackEvent, TrackEventKind,
};

use crate::BrsarError;

const RSEQ_HEADER_SIZE: usize = 0x20;
const BLOCK_ALIGN: usize = 0x20;
const DATA_HEADER_SIZE: usize = 0x0C;
const PPQN_MIDI: u16 = 960;
const TIMEBASE_DEFAULT: u16 = 48;

const CMD_WAIT: u8 = 0x80;
const CMD_PROGRAM_CHANGE: u8 = 0x81;
const CMD_OPEN_TRACK: u8 = 0x88;
const CMD_JUMP: u8 = 0x89;
const CMD_CALL: u8 = 0x8A;
const CMD_TIMEBASE: u8 = 0xB0;
const CMD_ENV_HOLD: u8 = 0xB1;
const CMD_MONOPHONIC: u8 = 0xB2;
const CMD_BIQUAD_TYPE: u8 = 0xB4;
const CMD_BIQUAD_VALUE: u8 = 0xB5;
const CMD_PAN: u8 = 0xC0;
const CMD_VOLUME: u8 = 0xC1;
const CMD_MAIN_VOLUME: u8 = 0xC2;
const CMD_TRANSPOSE: u8 = 0xC3;
const CMD_PITCH_BEND: u8 = 0xC4;
const CMD_BEND_RANGE: u8 = 0xC5;
const CMD_PRIO: u8 = 0xC6;
const CMD_NOTE_WAIT: u8 = 0xC7;
const CMD_TIE: u8 = 0xC8;
const CMD_PORTA: u8 = 0xC9;
const CMD_MOD_DEPTH: u8 = 0xCA;
const CMD_MOD_SPEED: u8 = 0xCB;
const CMD_MOD_TYPE: u8 = 0xCC;
const CMD_MOD_RANGE: u8 = 0xCD;
const CMD_PORTA_SW: u8 = 0xCE;
const CMD_PORTA_TIME: u8 = 0xCF;
const CMD_ATTACK: u8 = 0xD0;
const CMD_DECAY: u8 = 0xD1;
const CMD_SUSTAIN: u8 = 0xD2;
const CMD_RELEASE: u8 = 0xD3;
const CMD_LOOP_START: u8 = 0xD4;
const CMD_VOLUME2: u8 = 0xD5;
const CMD_SURROUND_PAN: u8 = 0xD7;
const CMD_LPF_CUTOFF: u8 = 0xD8;
const CMD_FX_SEND_A: u8 = 0xD9;
const CMD_FX_SEND_B: u8 = 0xDA;
const CMD_MAIN_SEND: u8 = 0xDB;
const CMD_INIT_PAN: u8 = 0xDC;
const CMD_DAMPER: u8 = 0xDF;
const CMD_MOD_DELAY: u8 = 0xE0;
const CMD_TEMPO: u8 = 0xE1;
const CMD_SWEEP_PITCH: u8 = 0xE3;
const CMD_EXTENDED: u8 = 0xF0;
const CMD_ENV_RESET: u8 = 0xFB;
const CMD_LOOP_END: u8 = 0xFC;
const CMD_RETURN: u8 = 0xFD;
const CMD_ALLOCATE_TRACK: u8 = 0xFE;
const CMD_FIN: u8 = 0xFF;

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Rseq {
    pub sequence_data: Vec<u8>,
    pub labels: Vec<(String, u32)>,
}

impl Rseq {
    /// Parse a full RSEQ binary file.
    ///
    /// # Errors
    /// Returns `BrsarError::Decode` when the file structure or block layout is invalid.
    pub fn from_bytes(data: &[u8]) -> Result<Self, BrsarError> {
        if data.len() < RSEQ_HEADER_SIZE {
            return Err(BrsarError::Decode(
                "RSEQ file shorter than header".to_owned(),
            ));
        }
        if &data[0x00..0x04] != b"RSEQ" {
            return Err(BrsarError::Decode("invalid RSEQ magic".to_owned()));
        }

        let bom = read_u16_be(data, 0x04)?;
        if bom != 0xFEFF {
            return Err(BrsarError::Decode(format!(
                "invalid BOM {bom:#06x}, expected 0xFEFF"
            )));
        }
        let version = read_u16_be(data, 0x06)?;
        if version != 0x0100 {
            return Err(BrsarError::Decode(format!(
                "unsupported RSEQ version {version:#06x}"
            )));
        }

        let file_size = usize::try_from(read_u32_be(data, 0x08)?)
            .map_err(|_| BrsarError::Decode("RSEQ file size does not fit usize".to_owned()))?;
        if file_size > data.len() {
            return Err(BrsarError::Decode(format!(
                "RSEQ header file size {file_size:#x} exceeds input length {:#x}",
                data.len()
            )));
        }

        let header_size = usize::from(read_u16_be(data, 0x0C)?);
        let block_count = read_u16_be(data, 0x0E)?;
        if header_size != RSEQ_HEADER_SIZE || block_count != 0x0002 {
            return Err(BrsarError::Decode(
                "RSEQ header layout is not NW4R-standard".to_owned(),
            ));
        }

        let data_block_offset = usize::try_from(read_u32_be(data, 0x10)?)
            .map_err(|_| BrsarError::Decode("DATA block offset too large".to_owned()))?;
        let data_block_size = usize::try_from(read_u32_be(data, 0x14)?)
            .map_err(|_| BrsarError::Decode("DATA block size too large".to_owned()))?;
        let labl_block_offset = usize::try_from(read_u32_be(data, 0x18)?)
            .map_err(|_| BrsarError::Decode("LABL block offset too large".to_owned()))?;
        let labl_block_size = usize::try_from(read_u32_be(data, 0x1C)?)
            .map_err(|_| BrsarError::Decode("LABL block size too large".to_owned()))?;

        let sequence_data = parse_data_block(data, data_block_offset, data_block_size)?;
        let labels = parse_labl_block(data, labl_block_offset, labl_block_size)?;

        Ok(Self {
            sequence_data,
            labels,
        })
    }

    /// Serialize to a full RSEQ binary file.
    ///
    /// # Errors
    /// Returns `BrsarError::Encode` when a size/offset overflows the RSEQ field sizes.
    pub fn to_bytes(&self) -> Result<Vec<u8>, BrsarError> {
        let data_block = build_data_block(&self.sequence_data)?;
        let labl_block = build_labl_block(&self.labels)?;

        let data_offset = RSEQ_HEADER_SIZE;
        let labl_offset = data_offset
            .checked_add(data_block.len())
            .ok_or_else(|| BrsarError::Encode("RSEQ block offset overflow".to_owned()))?;
        let file_size = labl_offset
            .checked_add(labl_block.len())
            .ok_or_else(|| BrsarError::Encode("RSEQ file size overflow".to_owned()))?;

        let mut out = vec![0x00_u8; RSEQ_HEADER_SIZE];
        out[0x00..0x04].copy_from_slice(b"RSEQ");
        out[0x04..0x06].copy_from_slice(&0xFEFF_u16.to_be_bytes());
        out[0x06..0x08].copy_from_slice(&0x0100_u16.to_be_bytes());
        out[0x08..0x0C].copy_from_slice(
            &u32::try_from(file_size)
                .map_err(|_| BrsarError::Encode("RSEQ file size exceeds u32".to_owned()))?
                .to_be_bytes(),
        );
        out[0x0C..0x0E].copy_from_slice(&0x0020_u16.to_be_bytes());
        out[0x0E..0x10].copy_from_slice(&0x0002_u16.to_be_bytes());
        out[0x10..0x14].copy_from_slice(
            &u32::try_from(data_offset)
                .map_err(|_| BrsarError::Encode("DATA offset exceeds u32".to_owned()))?
                .to_be_bytes(),
        );
        out[0x14..0x18].copy_from_slice(
            &u32::try_from(data_block.len())
                .map_err(|_| BrsarError::Encode("DATA size exceeds u32".to_owned()))?
                .to_be_bytes(),
        );
        out[0x18..0x1C].copy_from_slice(
            &u32::try_from(labl_offset)
                .map_err(|_| BrsarError::Encode("LABL offset exceeds u32".to_owned()))?
                .to_be_bytes(),
        );
        out[0x1C..0x20].copy_from_slice(
            &u32::try_from(labl_block.len())
                .map_err(|_| BrsarError::Encode("LABL size exceeds u32".to_owned()))?
                .to_be_bytes(),
        );

        out.extend_from_slice(&data_block);
        out.extend_from_slice(&labl_block);
        Ok(out)
    }

    /// Convert raw MIDI bytes to an RSEQ. No normalization is performed.
    ///
    /// # Errors
    /// Returns `BrsarError::Midi` for invalid MIDI and `BrsarError::Encode` for
    /// unsupported track layout or offset overflow.
    pub fn from_midi(midi: &[u8]) -> Result<Self, BrsarError> {
        let smf = Smf::parse(midi).map_err(|err| BrsarError::Midi(err.to_string()))?;
        let division = match smf.header.timing {
            Timing::Metrical(ppqn) => u16::from(ppqn),
            Timing::Timecode(_, _) => {
                return Err(BrsarError::Midi(
                    "SMPTE timecode MIDI is not supported for RSEQ conversion".to_owned(),
                ));
            }
        };
        if division == 0 {
            return Err(BrsarError::Midi(
                "MIDI division must be non-zero".to_owned(),
            ));
        }

        let mut track_bytes = Vec::with_capacity(smf.tracks.len());
        for track in &smf.tracks {
            let seq = encode_track_to_sequence(track, division)?;
            track_bytes.push(seq);
        }

        let mut sequence_data = Vec::new();
        if track_bytes.len() > 1 {
            if track_bytes.len() > 16 {
                return Err(BrsarError::Encode(
                    "RSEQ AllocateTrack only supports up to 16 tracks".to_owned(),
                ));
            }
            let mut mask: u16 = 0;
            for index in 0..track_bytes.len() {
                mask |= 1_u16 << index;
            }
            sequence_data.push(CMD_ALLOCATE_TRACK);
            sequence_data.extend_from_slice(&mask.to_be_bytes());

            for track_number in 1..track_bytes.len() {
                let track_u8 = u8::try_from(track_number)
                    .map_err(|_| BrsarError::Encode("track number exceeds u8".to_owned()))?;
                sequence_data.extend_from_slice(&[CMD_OPEN_TRACK, track_u8, 0x00, 0x00, 0x00]);
            }
        }

        let mut track_offsets = Vec::with_capacity(track_bytes.len());
        for bytes in &track_bytes {
            track_offsets.push(sequence_data.len());
            sequence_data.extend_from_slice(bytes);
        }

        if track_bytes.len() > 1 {
            #[allow(clippy::needless_range_loop)]
            for track_number in 1..track_bytes.len() {
                let patch_offset = 3 + (track_number - 1) * 5;
                let track_offset = track_offsets[track_number];
                let off_u32 = u32::try_from(track_offset)
                    .map_err(|_| BrsarError::Encode("track offset exceeds u32".to_owned()))?;
                if off_u32 > 0x00FF_FFFF {
                    return Err(BrsarError::Encode(
                        "track offset exceeds RSEQ u24 range".to_owned(),
                    ));
                }
                sequence_data[patch_offset] = ((off_u32 >> 16) & 0xFF) as u8;
                sequence_data[patch_offset + 1] = ((off_u32 >> 8) & 0xFF) as u8;
                sequence_data[patch_offset + 2] = (off_u32 & 0xFF) as u8;
            }
        }

        Ok(Self {
            sequence_data,
            labels: vec![("SMF_sequence_Begin".to_owned(), 0)],
        })
    }

    /// Convert this RSEQ back to standard MIDI bytes.
    ///
    /// # Errors
    /// Returns `BrsarError::Decode` for malformed sequence commands and
    /// `BrsarError::Midi` when MIDI output cannot be serialized.
    pub fn to_midi(&self) -> Result<Vec<u8>, BrsarError> {
        let mut track_starts = vec![0_usize];
        collect_track_starts(&self.sequence_data, 0, &mut track_starts)?;
        track_starts.sort_unstable();
        track_starts.dedup();

        let mut tracks = Vec::with_capacity(track_starts.len());
        let mut tempo_events = Vec::new();
        for (index, start) in track_starts.iter().copied().enumerate() {
            let channel = u8::try_from(index & 0x0F)
                .map_err(|_| BrsarError::Decode("track channel overflow".to_owned()))?;
            let mut events = decode_track(&self.sequence_data, start, channel, &mut tempo_events)?;
            events.sort_by_key(|ev| ev.tick);
            let mut track = to_delta_track(events);
            track.push(TrackEvent {
                delta: u28::from(0_u32),
                kind: TrackEventKind::Meta(MetaMessage::EndOfTrack),
            });
            tracks.push(track);
        }

        if tracks.is_empty() {
            tracks.push(vec![TrackEvent {
                delta: u28::from(0_u32),
                kind: TrackEventKind::Meta(MetaMessage::EndOfTrack),
            }]);
        }

        if let Some(primary) = tracks.first_mut() {
            tempo_events.sort_by_key(|ev| ev.tick);
            let mut merged = from_delta_track(primary)?;
            merged.extend(tempo_events);
            merged.sort_by_key(|ev| ev.tick);
            *primary = to_delta_track(merged);
            primary.push(TrackEvent {
                delta: u28::from(0_u32),
                kind: TrackEventKind::Meta(MetaMessage::EndOfTrack),
            });
        }

        let format = if tracks.len() > 1 {
            Format::Parallel
        } else {
            Format::SingleTrack
        };
        let smf = Smf {
            header: Header {
                format,
                timing: Timing::Metrical(u15::from(PPQN_MIDI)),
            },
            tracks,
        };

        let mut out = Vec::new();
        smf.write_std(&mut out)
            .map_err(|err| BrsarError::Midi(err.to_string()))?;
        Ok(out)
    }
}

#[derive(Clone)]
struct AbsoluteEvent {
    tick: u32,
    kind: TrackEventKind<'static>,
}

fn parse_data_block(data: &[u8], offset: usize, size: usize) -> Result<Vec<u8>, BrsarError> {
    let end = offset
        .checked_add(size)
        .ok_or_else(|| BrsarError::Decode("DATA block range overflow".to_owned()))?;
    if end > data.len() || size < DATA_HEADER_SIZE {
        return Err(BrsarError::Decode("DATA block out of bounds".to_owned()));
    }

    let block = &data[offset..end];
    if &block[0x00..0x04] != b"DATA" {
        return Err(BrsarError::Decode("DATA block magic mismatch".to_owned()));
    }
    let declared_size = usize::try_from(read_u32_be(block, 0x04)?)
        .map_err(|_| BrsarError::Decode("DATA block size too large".to_owned()))?;
    if declared_size != size {
        return Err(BrsarError::Decode("DATA block size mismatch".to_owned()));
    }

    let data_offset = usize::try_from(read_u32_be(block, 0x08)?)
        .map_err(|_| BrsarError::Decode("DATA payload offset too large".to_owned()))?;
    if data_offset < DATA_HEADER_SIZE || data_offset > block.len() {
        return Err(BrsarError::Decode(
            "DATA payload offset out of range".to_owned(),
        ));
    }

    let mut payload = block[data_offset..].to_vec();
    while payload.last().is_some_and(|byte| *byte == 0x00) {
        payload.pop();
    }
    Ok(payload)
}

fn parse_labl_block(
    data: &[u8],
    offset: usize,
    size: usize,
) -> Result<Vec<(String, u32)>, BrsarError> {
    let end = offset
        .checked_add(size)
        .ok_or_else(|| BrsarError::Decode("LABL block range overflow".to_owned()))?;
    if end > data.len() || size < 0x0C {
        return Err(BrsarError::Decode("LABL block out of bounds".to_owned()));
    }

    let block = &data[offset..end];
    if &block[0x00..0x04] != b"LABL" {
        return Err(BrsarError::Decode("LABL block magic mismatch".to_owned()));
    }
    let declared_size = usize::try_from(read_u32_be(block, 0x04)?)
        .map_err(|_| BrsarError::Decode("LABL block size too large".to_owned()))?;
    if declared_size != size {
        return Err(BrsarError::Decode("LABL block size mismatch".to_owned()));
    }

    let count = usize::try_from(read_u32_be(block, 0x08)?)
        .map_err(|_| BrsarError::Decode("LABL count too large".to_owned()))?;
    let mut cursor = 0x0C;
    let mut labels = Vec::with_capacity(count);
    for _ in 0..count {
        if cursor + 8 > block.len() {
            return Err(BrsarError::Decode("LABL entry header truncated".to_owned()));
        }
        let label_offset = read_u32_be(block, cursor)?;
        cursor += 4;
        let name_len = usize::try_from(read_u32_be(block, cursor)?)
            .map_err(|_| BrsarError::Decode("LABL name length too large".to_owned()))?;
        cursor += 4;
        if cursor + name_len > block.len() {
            return Err(BrsarError::Decode("LABL name bytes truncated".to_owned()));
        }
        let name_bytes = &block[cursor..cursor + name_len];
        let name = String::from_utf8(name_bytes.to_vec())
            .map_err(|_| BrsarError::Decode("LABL name is not UTF-8".to_owned()))?;
        cursor += name_len;
        labels.push((name, label_offset));
    }
    Ok(labels)
}

fn build_data_block(payload: &[u8]) -> Result<Vec<u8>, BrsarError> {
    let mut block = Vec::new();
    block.extend_from_slice(b"DATA");
    block.extend_from_slice(&0_u32.to_be_bytes());
    block.extend_from_slice(&(DATA_HEADER_SIZE as u32).to_be_bytes());
    block.extend_from_slice(payload);
    align_bytes(&mut block, BLOCK_ALIGN);
    let size = u32::try_from(block.len())
        .map_err(|_| BrsarError::Encode("DATA block exceeds u32".to_owned()))?;
    block[0x04..0x08].copy_from_slice(&size.to_be_bytes());
    Ok(block)
}

fn build_labl_block(labels: &[(String, u32)]) -> Result<Vec<u8>, BrsarError> {
    let mut block = Vec::new();
    block.extend_from_slice(b"LABL");
    block.extend_from_slice(&0_u32.to_be_bytes());
    block.extend_from_slice(
        &u32::try_from(labels.len())
            .map_err(|_| BrsarError::Encode("label count exceeds u32".to_owned()))?
            .to_be_bytes(),
    );
    for (name, offset) in labels {
        let name_bytes = name.as_bytes();
        block.extend_from_slice(&offset.to_be_bytes());
        block.extend_from_slice(
            &u32::try_from(name_bytes.len())
                .map_err(|_| BrsarError::Encode("label name length exceeds u32".to_owned()))?
                .to_be_bytes(),
        );
        block.extend_from_slice(name_bytes);
    }
    align_bytes(&mut block, BLOCK_ALIGN);
    let size = u32::try_from(block.len())
        .map_err(|_| BrsarError::Encode("LABL block exceeds u32".to_owned()))?;
    block[0x04..0x08].copy_from_slice(&size.to_be_bytes());
    Ok(block)
}

fn align_bytes(buf: &mut Vec<u8>, align: usize) {
    let remainder = buf.len() % align;
    if remainder != 0 {
        buf.resize(buf.len() + (align - remainder), 0x00);
    }
}

#[allow(clippy::too_many_lines)]
fn encode_track_to_sequence(
    track: &[TrackEvent<'_>],
    division: u16,
) -> Result<Vec<u8>, BrsarError> {
    let mut absolute_events = Vec::with_capacity(track.len());
    let mut abs_tick: u64 = 0;
    for event in track {
        abs_tick = abs_tick
            .checked_add(u64::from(event.delta.as_int()))
            .ok_or_else(|| BrsarError::Encode("MIDI absolute tick overflow".to_owned()))?;
        let tick_u32 = u32::try_from(abs_tick)
            .map_err(|_| BrsarError::Encode("MIDI absolute tick exceeds u32".to_owned()))?;
        absolute_events.push((tick_u32, event.kind));
    }

    let mut note_off_map: HashMap<(u8, u8, usize), u32> = HashMap::new();
    for (index, (tick, kind)) in absolute_events.iter().enumerate() {
        if let TrackEventKind::Midi { channel, message } = kind {
            match message {
                MidiMessage::NoteOff { key, .. } => {
                    let channel_u8 = u8::from(*channel);
                    let key_u8 = u8::from(*key);
                    for earlier in (0..index).rev() {
                        if let Some((
                            start_tick,
                            TrackEventKind::Midi {
                                channel: start_channel,
                                message:
                                    MidiMessage::NoteOn {
                                        key: start_key,
                                        vel: start_vel,
                                    },
                            },
                        )) = absolute_events.get(earlier)
                            && u8::from(*start_vel) > 0
                            && u8::from(*start_channel) == channel_u8
                            && u8::from(*start_key) == key_u8
                        {
                            note_off_map
                                .entry((channel_u8, key_u8, earlier))
                                .or_insert(*tick.max(start_tick));
                            break;
                        }
                    }
                }
                MidiMessage::NoteOn { key, vel } if u8::from(*vel) == 0x00 => {
                    let channel_u8 = u8::from(*channel);
                    let key_u8 = u8::from(*key);
                    for earlier in (0..index).rev() {
                        if let Some((
                            start_tick,
                            TrackEventKind::Midi {
                                channel: start_channel,
                                message:
                                    MidiMessage::NoteOn {
                                        key: start_key,
                                        vel: start_vel,
                                    },
                            },
                        )) = absolute_events.get(earlier)
                            && u8::from(*start_vel) > 0
                            && u8::from(*start_channel) == channel_u8
                            && u8::from(*start_key) == key_u8
                        {
                            note_off_map
                                .entry((channel_u8, key_u8, earlier))
                                .or_insert(*tick.max(start_tick));
                            break;
                        }
                    }
                }
                _ => {}
            }
        }
    }

    let mut sequence = Vec::new();
    sequence.extend_from_slice(&[CMD_NOTE_WAIT, 0x00]);

    let mut last_tick = 0_u32;
    let mut max_note_end = 0_u32;

    for (index, (tick, kind)) in absolute_events.iter().enumerate() {
        match kind {
            TrackEventKind::Midi { channel, message } => match message {
                MidiMessage::NoteOn { key, vel } if u8::from(*vel) > 0x00 => {
                    emit_wait(&mut sequence, tick.saturating_sub(last_tick), division);
                    last_tick = *tick;

                    let key_u8 = u8::from(*key);
                    let vel_u8 = u8::from(*vel);
                    let off_tick = note_off_map
                        .get(&(u8::from(*channel), key_u8, index))
                        .copied()
                        .unwrap_or(*tick);
                    let len_ticks = off_tick.saturating_sub(*tick);
                    let seq_len = midi_to_seq_ticks(len_ticks, division);

                    sequence.push(key_u8);
                    sequence.push(vel_u8);
                    write_vlq(&mut sequence, seq_len);
                    max_note_end = max_note_end.max(off_tick);
                }
                MidiMessage::ProgramChange { program } => {
                    emit_wait(&mut sequence, tick.saturating_sub(last_tick), division);
                    last_tick = *tick;
                    sequence.extend_from_slice(&[CMD_PROGRAM_CHANGE, u8::from(*program)]);
                }
                MidiMessage::PitchBend { bend } => {
                    emit_wait(&mut sequence, tick.saturating_sub(last_tick), division);
                    last_tick = *tick;
                    let scaled = f64::from(bend.as_int()) / 8192.0;
                    let val = (scaled * 127.0).round().clamp(-128.0, 127.0) as i8;
                    sequence.extend_from_slice(&[CMD_PITCH_BEND, val as u8]);
                }
                MidiMessage::Controller { controller, value } => {
                    if let Some((cmd, param)) = controller_to_rseq(*controller, *value) {
                        emit_wait(&mut sequence, tick.saturating_sub(last_tick), division);
                        last_tick = *tick;
                        sequence.extend_from_slice(&[cmd, param]);
                    }
                }
                _ => {}
            },
            TrackEventKind::Meta(MetaMessage::Tempo(tempo)) => {
                emit_wait(&mut sequence, tick.saturating_sub(last_tick), division);
                last_tick = *tick;
                let micros = tempo.as_int();
                if micros != 0 {
                    let bpm_u32 = 60_000_000_u32 / micros;
                    let bpm = u16::try_from(bpm_u32.min(u32::from(u16::MAX)))
                        .map_err(|_| BrsarError::Encode("tempo BPM does not fit u16".to_owned()))?;
                    sequence.push(CMD_TEMPO);
                    sequence.extend_from_slice(&bpm.to_be_bytes());
                }
            }
            _ => {}
        }
    }

    if max_note_end > last_tick {
        emit_wait(&mut sequence, max_note_end - last_tick, division);
    }
    sequence.push(CMD_FIN);
    Ok(sequence)
}

fn controller_to_rseq(controller: u7, value: u7) -> Option<(u8, u8)> {
    let cc = u8::from(controller);
    let val = u8::from(value);
    match cc {
        1 => Some((CMD_MOD_DEPTH, val)),
        3 => Some((CMD_INIT_PAN, val)),
        7 => Some((CMD_VOLUME, val)),
        9 => Some((CMD_SURROUND_PAN, val)),
        10 => Some((CMD_PAN, val)),
        11 => Some((CMD_VOLUME2, val)),
        12 => Some((CMD_MAIN_VOLUME, val)),
        13 => Some((CMD_TRANSPOSE, val.wrapping_sub(0x40))),
        14 => Some((CMD_PRIO, val)),
        20 => Some((CMD_BEND_RANGE, val)),
        21 => Some((CMD_MOD_SPEED, val)),
        22 => Some((CMD_MOD_TYPE, val)),
        23 => Some((CMD_MOD_RANGE, val)),
        30 => Some((CMD_BIQUAD_TYPE, val)),
        31 => Some((CMD_BIQUAD_VALUE, val)),
        64 => Some((CMD_DAMPER, u8::from(val >= 64))),
        65 => Some((CMD_PORTA_SW, u8::from(val >= 64))),
        68 => Some((CMD_MONOPHONIC, u8::from(val >= 64))),
        79 => Some((CMD_ENV_HOLD, val)),
        84 => Some((CMD_PORTA, val)),
        85 => Some((CMD_ATTACK, val)),
        86 => Some((CMD_DECAY, val)),
        87 => Some((CMD_SUSTAIN, val)),
        88 => Some((CMD_RELEASE, val)),
        89 => Some((CMD_LOOP_START, val)),
        90 => Some((CMD_LOOP_END, 0x00)),
        91 => Some((CMD_FX_SEND_A, val)),
        92 => Some((CMD_FX_SEND_B, val)),
        95 => Some((CMD_MAIN_SEND, val)),
        _ => None,
    }
}

fn emit_wait(buffer: &mut Vec<u8>, delta_ticks: u32, division: u16) {
    if delta_ticks == 0 {
        return;
    }
    let seq_ticks = midi_to_seq_ticks(delta_ticks, division);
    if seq_ticks != 0 {
        buffer.push(CMD_WAIT);
        write_vlq(buffer, seq_ticks);
    }
}

fn midi_to_seq_ticks(midi_ticks: u32, division: u16) -> u32 {
    (midi_ticks
        .saturating_mul(u32::from(TIMEBASE_DEFAULT))
        .saturating_add(u32::from(division) / 2))
        / u32::from(division)
}

fn seq_to_midi_ticks(seq_ticks: u32, timebase: u16) -> u32 {
    if timebase == 0 {
        return 0;
    }
    (seq_ticks
        .saturating_mul(u32::from(PPQN_MIDI))
        .saturating_add(u32::from(timebase) / 2))
        / u32::from(timebase)
}

fn collect_track_starts(
    data: &[u8],
    start: usize,
    starts: &mut Vec<usize>,
) -> Result<(), BrsarError> {
    if start >= data.len() {
        return Err(BrsarError::Decode(
            "track start offset out of range".to_owned(),
        ));
    }
    let mut cursor = start;
    while cursor < data.len() {
        let opcode = data[cursor];
        cursor += 1;
        match opcode {
            0x00..=0x7F => {
                cursor += 1;
                let (_, consumed) = read_vlq_at(data, cursor)?;
                cursor += consumed;
            }
            CMD_WAIT => {
                let (_, consumed) = read_vlq_at(data, cursor)?;
                cursor += consumed;
            }
            CMD_OPEN_TRACK => {
                if cursor + 4 > data.len() {
                    return Err(BrsarError::Decode("OpenTrack truncated".to_owned()));
                }
                let offset = read_u24_be(data, cursor + 1)?;
                let offset_usize = usize::try_from(offset)
                    .map_err(|_| BrsarError::Decode("OpenTrack offset too large".to_owned()))?;
                starts.push(offset_usize);
                cursor += 4;
            }
            CMD_JUMP | CMD_CALL => {
                cursor += 3;
            }
            CMD_ALLOCATE_TRACK | CMD_MOD_DELAY | CMD_TEMPO | CMD_SWEEP_PITCH => {
                cursor += 2;
            }
            CMD_EXTENDED => {
                cursor += 4;
            }
            CMD_FIN | CMD_RETURN => break,
            CMD_LOOP_END | CMD_ENV_RESET => {}
            _ => {
                if opcode == CMD_PROGRAM_CHANGE || (0xB0..=0xDF).contains(&opcode) {
                    cursor += 1;
                } else {
                    return Err(BrsarError::Decode(format!(
                        "unsupported opcode while collecting tracks: {opcode:#04x}"
                    )));
                }
            }
        }
    }
    Ok(())
}

#[allow(clippy::too_many_lines)]
fn decode_track(
    data: &[u8],
    start: usize,
    channel: u8,
    tempo_out: &mut Vec<AbsoluteEvent>,
) -> Result<Vec<AbsoluteEvent>, BrsarError> {
    let mut events = Vec::new();
    let mut visited = BTreeSet::new();
    let mut stack = Vec::new();
    let mut cursor = start;
    let mut ticks = 0_u32;
    let mut timebase = TIMEBASE_DEFAULT;
    let mut note_wait = true;

    while cursor < data.len() {
        if !visited.insert((cursor, ticks, timebase, note_wait)) {
            break;
        }

        let opcode = data[cursor];
        cursor += 1;
        match opcode {
            0x00..=0x7F => {
                if cursor >= data.len() {
                    return Err(BrsarError::Decode("note velocity missing".to_owned()));
                }
                let note = opcode;
                let velocity = data[cursor];
                cursor += 1;
                let (duration, consumed) = read_vlq_at(data, cursor)?;
                cursor += consumed;
                let duration_ticks = seq_to_midi_ticks(duration, timebase);

                events.push(AbsoluteEvent {
                    tick: ticks,
                    kind: TrackEventKind::Midi {
                        channel: u4::from(channel & 0x0F),
                        message: MidiMessage::NoteOn {
                            key: u7::from(note.min(0x7F)),
                            vel: u7::from(velocity.min(0x7F)),
                        },
                    },
                });
                events.push(AbsoluteEvent {
                    tick: ticks.saturating_add(duration_ticks),
                    kind: TrackEventKind::Midi {
                        channel: u4::from(channel & 0x0F),
                        message: MidiMessage::NoteOff {
                            key: u7::from(note.min(0x7F)),
                            vel: u7::from(0),
                        },
                    },
                });
                if note_wait {
                    ticks = ticks.saturating_add(duration_ticks);
                }
            }
            CMD_WAIT => {
                let (duration, consumed) = read_vlq_at(data, cursor)?;
                cursor += consumed;
                ticks = ticks.saturating_add(seq_to_midi_ticks(duration, timebase));
            }
            CMD_PROGRAM_CHANGE => {
                let program = *data
                    .get(cursor)
                    .ok_or_else(|| BrsarError::Decode("ProgramChange missing value".to_owned()))?;
                cursor += 1;
                events.push(AbsoluteEvent {
                    tick: ticks,
                    kind: TrackEventKind::Midi {
                        channel: u4::from(channel & 0x0F),
                        message: MidiMessage::ProgramChange {
                            program: u7::from(program.min(0x7F)),
                        },
                    },
                });
            }
            CMD_OPEN_TRACK => {
                if cursor + 4 > data.len() {
                    return Err(BrsarError::Decode("OpenTrack truncated".to_owned()));
                }
                cursor += 4;
            }
            CMD_JUMP => {
                let offset = read_u24_be(data, cursor)?;
                cursor = usize::try_from(offset)
                    .map_err(|_| BrsarError::Decode("Jump offset too large".to_owned()))?;
            }
            CMD_CALL => {
                let offset = read_u24_be(data, cursor)?;
                cursor += 3;
                stack.push(cursor);
                cursor = usize::try_from(offset)
                    .map_err(|_| BrsarError::Decode("Call offset too large".to_owned()))?;
            }
            CMD_TIMEBASE => {
                let val = *data
                    .get(cursor)
                    .ok_or_else(|| BrsarError::Decode("Timebase missing value".to_owned()))?;
                cursor += 1;
                timebase = u16::from(val.max(1));
            }
            CMD_ENV_HOLD => {
                emit_cc(&mut events, ticks, channel, 79, data, &mut cursor)?;
            }
            CMD_MONOPHONIC => {
                let val = read_u8(data, &mut cursor)?;
                emit_controller_value(&mut events, ticks, channel, 68, bool_to_midi(val));
            }
            CMD_BIQUAD_TYPE => {
                emit_cc(&mut events, ticks, channel, 30, data, &mut cursor)?;
            }
            CMD_BIQUAD_VALUE => {
                emit_cc(&mut events, ticks, channel, 31, data, &mut cursor)?;
            }
            CMD_PAN => emit_cc(&mut events, ticks, channel, 10, data, &mut cursor)?,
            CMD_VOLUME => emit_cc(&mut events, ticks, channel, 7, data, &mut cursor)?,
            CMD_MAIN_VOLUME => emit_cc(&mut events, ticks, channel, 12, data, &mut cursor)?,
            CMD_TRANSPOSE => {
                let value = read_u8(data, &mut cursor)?;
                emit_controller_value(&mut events, ticks, channel, 13, value.wrapping_add(0x40));
            }
            CMD_PITCH_BEND => {
                let raw = read_i8(data, &mut cursor)?;
                let bend = ((f64::from(raw) / 127.0) * 8192.0)
                    .round()
                    .clamp(-8192.0, 8191.0) as i16;
                events.push(AbsoluteEvent {
                    tick: ticks,
                    kind: TrackEventKind::Midi {
                        channel: u4::from(channel & 0x0F),
                        message: MidiMessage::PitchBend {
                            bend: PitchBend::from_int(bend),
                        },
                    },
                });
            }
            CMD_BEND_RANGE => emit_cc(&mut events, ticks, channel, 20, data, &mut cursor)?,
            CMD_PRIO => emit_cc(&mut events, ticks, channel, 14, data, &mut cursor)?,
            CMD_NOTE_WAIT => {
                note_wait = read_u8(data, &mut cursor)? != 0;
            }
            CMD_TIE => {
                let _ = read_u8(data, &mut cursor)?;
            }
            CMD_PORTA => emit_cc(&mut events, ticks, channel, 84, data, &mut cursor)?,
            CMD_MOD_DEPTH => emit_cc(&mut events, ticks, channel, 1, data, &mut cursor)?,
            CMD_MOD_SPEED => emit_cc(&mut events, ticks, channel, 21, data, &mut cursor)?,
            CMD_MOD_TYPE => emit_cc(&mut events, ticks, channel, 22, data, &mut cursor)?,
            CMD_MOD_RANGE => emit_cc(&mut events, ticks, channel, 23, data, &mut cursor)?,
            CMD_PORTA_SW => {
                let val = read_u8(data, &mut cursor)?;
                emit_controller_value(&mut events, ticks, channel, 65, bool_to_midi(val));
            }
            CMD_PORTA_TIME => emit_cc(&mut events, ticks, channel, 5, data, &mut cursor)?,
            CMD_ATTACK => emit_cc(&mut events, ticks, channel, 85, data, &mut cursor)?,
            CMD_DECAY => emit_cc(&mut events, ticks, channel, 86, data, &mut cursor)?,
            CMD_SUSTAIN => emit_cc(&mut events, ticks, channel, 87, data, &mut cursor)?,
            CMD_RELEASE => emit_cc(&mut events, ticks, channel, 88, data, &mut cursor)?,
            CMD_LOOP_START => emit_cc(&mut events, ticks, channel, 89, data, &mut cursor)?,
            CMD_VOLUME2 => emit_cc(&mut events, ticks, channel, 11, data, &mut cursor)?,
            CMD_SURROUND_PAN => emit_cc(&mut events, ticks, channel, 9, data, &mut cursor)?,
            CMD_LPF_CUTOFF => emit_cc(&mut events, ticks, channel, 74, data, &mut cursor)?,
            CMD_FX_SEND_A => emit_cc(&mut events, ticks, channel, 91, data, &mut cursor)?,
            CMD_FX_SEND_B => emit_cc(&mut events, ticks, channel, 92, data, &mut cursor)?,
            CMD_MAIN_SEND => emit_cc(&mut events, ticks, channel, 95, data, &mut cursor)?,
            CMD_INIT_PAN => emit_cc(&mut events, ticks, channel, 3, data, &mut cursor)?,
            CMD_DAMPER => {
                let val = read_u8(data, &mut cursor)?;
                emit_controller_value(&mut events, ticks, channel, 64, bool_to_midi(val));
            }
            CMD_MOD_DELAY => {
                let value = read_i16_be(data, cursor)?;
                cursor += 2;
                let cc_val = value.clamp(0, 127) as u8;
                emit_controller_value(&mut events, ticks, channel, 26, cc_val);
            }
            CMD_TEMPO => {
                let bpm = u32::from(read_u16_be(data, cursor)?);
                cursor += 2;
                if bpm != 0 {
                    let micros = (60_000_000_u32 / bpm).max(1);
                    tempo_out.push(AbsoluteEvent {
                        tick: ticks,
                        kind: TrackEventKind::Meta(MetaMessage::Tempo(u24::from(micros))),
                    });
                }
            }
            CMD_SWEEP_PITCH => {
                let _ = read_i16_be(data, cursor)?;
                cursor += 2;
            }
            CMD_EXTENDED => {
                let ext = read_u8(data, &mut cursor)?;
                let var_num = read_u8(data, &mut cursor)?;
                let value = read_i16_be(data, cursor)?;
                cursor += 2;
                if ext == 0x80 {
                    let cc = match var_num {
                        0 => Some(16),
                        1 => Some(17),
                        2 => Some(18),
                        3 => Some(19),
                        32 => Some(80),
                        33 => Some(81),
                        34 => Some(82),
                        35 => Some(83),
                        _ => None,
                    };
                    if let Some(cc_num) = cc {
                        let cc_val = value.clamp(0, 127) as u8;
                        emit_controller_value(&mut events, ticks, channel, cc_num, cc_val);
                    }
                }
            }
            CMD_ENV_RESET | CMD_LOOP_END => {}
            CMD_RETURN => {
                if let Some(ret) = stack.pop() {
                    cursor = ret;
                } else {
                    break;
                }
            }
            CMD_ALLOCATE_TRACK => {
                cursor += 2;
            }
            CMD_FIN => break,
            _ => {
                return Err(BrsarError::Decode(format!(
                    "unsupported opcode in track decode: {opcode:#04x}"
                )));
            }
        }
    }

    Ok(events)
}

fn emit_cc(
    out: &mut Vec<AbsoluteEvent>,
    tick: u32,
    channel: u8,
    controller: u8,
    data: &[u8],
    cursor: &mut usize,
) -> Result<(), BrsarError> {
    let value = read_u8(data, cursor)?;
    emit_controller_value(out, tick, channel, controller, value);
    Ok(())
}

fn emit_controller_value(
    out: &mut Vec<AbsoluteEvent>,
    tick: u32,
    channel: u8,
    controller: u8,
    value: u8,
) {
    out.push(AbsoluteEvent {
        tick,
        kind: TrackEventKind::Midi {
            channel: u4::from(channel & 0x0F),
            message: MidiMessage::Controller {
                controller: u7::from(controller.min(0x7F)),
                value: u7::from(value.min(0x7F)),
            },
        },
    });
}

fn to_delta_track(events: Vec<AbsoluteEvent>) -> Vec<TrackEvent<'static>> {
    let mut last_tick = 0_u32;
    let mut out = Vec::with_capacity(events.len());
    for ev in events {
        let delta = ev.tick.saturating_sub(last_tick);
        last_tick = ev.tick;
        out.push(TrackEvent {
            delta: u28::from(delta),
            kind: ev.kind,
        });
    }
    out
}

fn from_delta_track(track: &[TrackEvent<'static>]) -> Result<Vec<AbsoluteEvent>, BrsarError> {
    let mut out = Vec::with_capacity(track.len());
    let mut tick = 0_u32;
    for ev in track {
        tick = tick
            .checked_add(ev.delta.as_int())
            .ok_or_else(|| BrsarError::Decode("MIDI delta accumulation overflow".to_owned()))?;
        if !matches!(ev.kind, TrackEventKind::Meta(MetaMessage::EndOfTrack)) {
            out.push(AbsoluteEvent {
                tick,
                kind: ev.kind,
            });
        }
    }
    Ok(out)
}

fn read_u8(data: &[u8], cursor: &mut usize) -> Result<u8, BrsarError> {
    let value = *data
        .get(*cursor)
        .ok_or_else(|| BrsarError::Decode("unexpected EOF while reading u8".to_owned()))?;
    *cursor += 1;
    Ok(value)
}

fn read_i8(data: &[u8], cursor: &mut usize) -> Result<i8, BrsarError> {
    Ok(read_u8(data, cursor)? as i8)
}

fn read_u16_be(data: &[u8], offset: usize) -> Result<u16, BrsarError> {
    let bytes = data
        .get(offset..offset + 2)
        .ok_or_else(|| BrsarError::Decode("unexpected EOF while reading u16".to_owned()))?;
    Ok(u16::from_be_bytes([bytes[0], bytes[1]]))
}

fn read_i16_be(data: &[u8], offset: usize) -> Result<i16, BrsarError> {
    Ok(read_u16_be(data, offset)? as i16)
}

fn read_u24_be(data: &[u8], offset: usize) -> Result<u32, BrsarError> {
    let bytes = data
        .get(offset..offset + 3)
        .ok_or_else(|| BrsarError::Decode("unexpected EOF while reading u24".to_owned()))?;
    Ok((u32::from(bytes[0]) << 16) | (u32::from(bytes[1]) << 8) | u32::from(bytes[2]))
}

fn read_u32_be(data: &[u8], offset: usize) -> Result<u32, BrsarError> {
    let bytes = data
        .get(offset..offset + 4)
        .ok_or_else(|| BrsarError::Decode("unexpected EOF while reading u32".to_owned()))?;
    Ok(u32::from_be_bytes([bytes[0], bytes[1], bytes[2], bytes[3]]))
}

fn write_vlq(out: &mut Vec<u8>, value: u32) {
    let mut stack = [0_u8; 5];
    let mut val = value;
    let mut index = 0;

    stack[index] = (val & 0x7F) as u8;
    index += 1;
    val >>= 7;

    while val > 0 {
        stack[index] = ((val & 0x7F) as u8) | 0x80;
        index += 1;
        val >>= 7;
    }

    for byte in stack[..index].iter().rev() {
        out.push(*byte);
    }
}

fn read_vlq_at(data: &[u8], start: usize) -> Result<(u32, usize), BrsarError> {
    let mut value = 0_u32;
    let mut consumed = 0_usize;
    loop {
        let byte = *data
            .get(start + consumed)
            .ok_or_else(|| BrsarError::Decode("unexpected EOF while reading VLQ".to_owned()))?;
        consumed += 1;
        value = value
            .checked_shl(7)
            .ok_or_else(|| BrsarError::Decode("VLQ shift overflow".to_owned()))?
            | u32::from(byte & 0x7F);
        if byte & 0x80 == 0 {
            break;
        }
        if consumed >= 5 {
            return Err(BrsarError::Decode("VLQ too long".to_owned()));
        }
    }
    Ok((value, consumed))
}

const fn bool_to_midi(value: u8) -> u8 {
    if value == 0 { 0 } else { 0x7F }
}

#[cfg(test)]
mod tests {
    use super::*;
    use midly::{Timing, num::u28};

    #[test]
    fn rseq_file_round_trip() {
        let rseq = Rseq {
            sequence_data: vec![CMD_NOTE_WAIT, 0x00, 60, 100, 0x30, CMD_FIN],
            labels: vec![("SMF_test_Begin".to_owned(), 0)],
        };
        let bytes = rseq.to_bytes().expect("serialize rseq");
        let parsed = Rseq::from_bytes(&bytes).expect("parse rseq");
        assert_eq!(parsed.sequence_data, rseq.sequence_data);
        assert_eq!(parsed.labels, rseq.labels);
    }

    #[test]
    fn midi_to_rseq_and_back_round_trip_smoke() {
        let smf = Smf {
            header: Header {
                format: Format::SingleTrack,
                timing: Timing::Metrical(u15::from(0x01E0)),
            },
            tracks: vec![vec![
                TrackEvent {
                    delta: u28::from(0_u32),
                    kind: TrackEventKind::Midi {
                        channel: u4::from(0),
                        message: MidiMessage::ProgramChange {
                            program: u7::from(5),
                        },
                    },
                },
                TrackEvent {
                    delta: u28::from(0_u32),
                    kind: TrackEventKind::Midi {
                        channel: u4::from(0),
                        message: MidiMessage::NoteOn {
                            key: u7::from(60),
                            vel: u7::from(100),
                        },
                    },
                },
                TrackEvent {
                    delta: u28::from(480_u32),
                    kind: TrackEventKind::Midi {
                        channel: u4::from(0),
                        message: MidiMessage::NoteOff {
                            key: u7::from(60),
                            vel: u7::from(0),
                        },
                    },
                },
                TrackEvent {
                    delta: u28::from(0_u32),
                    kind: TrackEventKind::Meta(MetaMessage::EndOfTrack),
                },
            ]],
        };

        let mut midi_bytes = Vec::new();
        smf.write_std(&mut midi_bytes).expect("write midi");

        let rseq = Rseq::from_midi(&midi_bytes).expect("midi->rseq");
        let midi_back = rseq.to_midi().expect("rseq->midi");
        let reparsed = Smf::parse(&midi_back).expect("parse output midi");

        assert_eq!(reparsed.tracks.len(), 1);
        assert!(reparsed.tracks[0].iter().any(|event| matches!(
            event.kind,
            TrackEventKind::Midi {
                message: MidiMessage::NoteOn { .. },
                ..
            }
        )));
    }
}
