# AI Agent Reference: brsar

Purpose: BRSAR sound archive editing + RSEQ binary sequence + MIDI↔RSEQ conversion.

## Public API

- `Brsar`: Low-level parser for the BRSAR sound archive.
- `Rseq`: High-level representation of a binary sequence, including MIDI conversion.

### BRSAR Navigation

- The BRSAR follows a reference-based hierarchy: `Root` → `Groups` → `Collections` → `Sounds` → `Files`.
- Parsing uses the `binrw` crate with `#[br(big)]` for big-endian PowerPC byte order.
- **Offsets Shifting**: When data (like a song) is replaced, all downstream offsets must be updated using `increment_value(offset, delta)`.

### Song Index Formulas

- **Regular Songs**: `mem_order * 2`
- **Maestro Songs**: `mem_order + 2`
- **Handbell Songs**: `mem_order * 5 + 2`

## RSEQ and MIDI Pipeline

- `Rseq::from_midi(midi_bytes)`: Converts raw MIDI bytes into the game's `.brseq` format.
- `Rseq::to_midi()`: Converts a binary sequence back to MIDI for external editing.

### MIDI Conversion Details

- Channels are normalized to 0.
- All tracks are merged into a single track (unless multiple tracks are required for `AllocateTrack`).
- `NoteOn(vel=0)` is internally converted to `NoteOff` to match RSEQ semantics.
- PPQN is typically normalized to 960 (MIDI) or 48 (RSEQ timebase).
- Supports standard MIDI controllers (Modulation, Pan, Volume, etc.) and program changes.
- The `midly` crate is used for MIDI file parsing and serialization.
