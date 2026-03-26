# AI Agent Reference: Wii Music Editor Plus

This document serves as a guide for AI agents and developers working on the Rust rewrite of Wii Music Editor Plus. It outlines the project's domain, architecture, and core binary formats.

## Project Overview

Wii Music Editor Plus is a desktop application written in Rust using the Iced framework. It is designed for modding the 2008 Nintendo Wii title "Wii Music".

**Core Capabilities:**
- Replacing in-game songs with custom MIDI files.
- Editing style and instrument configurations.
- Modifying in-game text (BMG format).
- Extracting and patching game ROMs via `wit`.
- Exporting Riivolution patches for console playback.

**Workspace Architecture:**
The project is organized as a Cargo workspace with two main crates:
- `wm_core`: The logic library containing binary parsers, external tool wrappers, and domain models.
- `editor`: The GUI binary producing the `wii-music-editor` executable.

## Workspace Structure

```
rust-rewrite/
  tools/{windows,macos,linux}/{wiimms,sequence_cmd}/
  res/{icons,fonts,save}/
  i18n/en-US/ui.ftl
  crates/
    core/
      build.rs     # bakes WME_TOOLS_DIR + WME_RES_DIR at compile time
      src/
    editor/
      src/
```

## BRSAR Format Reference

The BRSAR (`RARC` container variation) is the primary sound archive for Wii Music. It uses big-endian (PowerPC) byte order.

### Navigation Hierarchy
The file structure follows a reference-based tree:
`Root` → `Groups` → `Collections` → `Sounds` → `Files`

### Core Operations
- **Section References:** Use `section_reference(offset)` to read the 4-byte big-endian value at a given location to jump to the next structure.
- **Offset Shifting:** When replacing data (e.g., a song), all downstream offsets must be updated. Use `increment_value(offset, delta)` to shift these values.
- **Song Indices:** Item indices are calculated based on song category:
  - Regular Songs: `mem_order * 2`
  - Maestro Songs: `mem_order + 2`
  - Handbell Songs: `mem_order * 5 + 2`
  - Menu Music: Fixed index based on internal list.

All structures must be parsed with `#[br(big)]` to ensure correct byte order.

## DOL Format Reference

The `main.dol` file contains the game's executable code and static data.

### Important Offsets
- `0x59C520`: Song Segment (Regular)
- `0x5A00EC`: Song Segment (Maestro)
- `0x5A0AEC`: Song Segment (Handbell)
- `0x596DAC`: Song Segment (Menu)
- `0x596758`: Style Segment
- `0x36F9A4` to `0x3701CC`: Style Execution Code Range
- `0x3D4ACC` to `0x3D4B64`: Default Style Code Range

### Data Offsets within Segments
- `+0x20`: Time Signature
- `+0x24`: Song Length
- `+0x28`: Tempo
- `+0x48`: Default Style

### Style Patching
The `remove_style_execution()` function is critical for allowing custom styles. It scans the range `0x36F9A4`–`0x3701CC` and replaces any byte `>= 0x90` with `0x38110000` (`li r0, 0` in PowerPC), effectively NOP-ing the dynamic style logic so the editor's static values take precedence.

## MIDI Pipeline

1. **Import:** Read user `.mid` via `midly`.
2. **Normalize:**
   - Map all channels to 0.
   - Merge all tracks into a single track.
   - Convert `NoteOn` with 0 velocity to `NoteOff`.
3. **Export:** Save temporary MIDI.
4. **Convert:** Shell out to `GotaSequenceCmd` to produce the `.brseq` format used by the game.

## Text Pipeline

1. **Extract:** Use `wszst` to extract `message.carc` into a `.bmg` file.
2. **Decode:** Use `wbmgt` to decode `.bmg` into a custom text format.
3. **Parse:** Lines follow the pattern `[hex_id] @[offset] [text]`. Use position-based parsing.
4. **Pack:** Re-encode via `wbmgt` and re-pack into `.carc` via `wszst`.

## Development Conventions

- **Byte Order:** Always big-endian (`#[br(big)]`).
- **Safety:** Library code returns `Result<T, WmError>`. No `unwrap()`.
- **Sentinels:** Instrument `67` is represented as `0xFFFFFFFF` in the DOL.
- **Backups:** Create `.backup` files once; never overwrite an existing backup to avoid data loss.

## Key Commands

```bash
cargo check                        # Validate compilation
cargo test                         # Execute test suite
cargo clippy -- -Dwarnings         # Run lints (strict)
cargo fmt -- --check               # Verify formatting
cargo run -p editor                # Launch the application
```
