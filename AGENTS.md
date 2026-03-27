# AI Agent Reference: Wii Music Editor

This document serves as a guide for AI agents and developers working on the Rust rewrite of Wii Music Editor. It outlines the project's domain, architecture, and core binary formats.

## Project Overview

Wii Music Editor is a desktop application written in Rust using the Iced framework. It is designed for modding the 2008 Nintendo Wii title "Wii Music".

**Core Capabilities:**
- Replacing in-game songs with custom MIDI files.
- Editing style and instrument configurations.
- Modifying in-game text (BMG format).
- Extracting game ROMs natively using the `nod` crate.
- Exporting Riivolution patches for console playback.

## Workspace Architecture

The project is organized as a Cargo workspace with five crates:

- **`carc`**: Low-level Yaz0/U8 (CARC) and BMG message format handlers.
- **`brsar`**: BRSAR sound archive and RSEQ binary sequence handlers, including MIDI↔RSEQ conversion.
- **`iso`**: Wii/GC disc image extraction wrapper for the `nod` crate.
- **`wm_core`**: The logic library containing binary parsers and domain models. No GUI or hardcoded runtime paths.
- **`editor`**: The Iced GUI binary producing the `wii-music-editor` executable.

## BRSAR Format Reference

The BRSAR is the primary sound archive for Wii Music. It uses big-endian (PowerPC) byte order.

### Navigation Hierarchy

The file structure follows a reference-based tree:
`Root` → `Groups` → `Collections` → `Sounds` → `Files`

### Core Operations

- **Section References**: Use `section_reference(offset)` to read the 4-byte big-endian value at a given location to jump to the next structure.
- **Offset Shifting**: When replacing data (e.g., a song), all downstream offsets must be updated. Use `increment_value(offset, delta)` to shift these values.
- **Song Indices**: Item indices are calculated based on song category:
  - Regular Songs: `mem_order * 2`
  - Maestro Songs: `mem_order + 2`
  - Handbell Songs: `mem_order * 5 + 2`

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

1. **Import**: Read user `.mid` via `midly`.
2. **Normalize**: Map all channels to 0, merge tracks into a single track, and convert `NoteOn` with 0 velocity to `NoteOff`.
3. **Convert**: Native conversion to `.brseq` format via `brsar::Rseq::from_midi()`.

## Text Pipeline

1. **Extract**: Load `message.carc` using `carc::WiiMessages::from_bytes()`.
2. **Access**: Programmatic editing via `entries()` or exporting to Wiimms text format via `to_text()`.
3. **Parse**: Lines follow the pattern `  [id_hex] @[attr_hex] [text]`. IDs range from 4 to 8 hex digits. Use " @" for parsing.
4. **Pack**: Encode modified entries back to `.carc` via `carc::WiiMessages::to_bytes()`.

## Development Conventions

- **Byte Order**: Always big-endian (`#[br(big)]`) for binary formats.
- **Hex Literals**: All binary values use hex literals (`0x59C520` not `5883168`). Decimal is for counts or loop indices only.
- **Safety**: Library code returns `Result<T, WmError>`. No `unwrap()`.
- **Documentation**: All public `Result`-returning functions require an `# Errors` documentation section.
- **Path Handling**: `WmPaths` or `RomFolder` handles runtime paths. Core logic should not bake in local file system paths.
- **Backups**: Create `.backup` files once. Never overwrite an existing backup to avoid data loss.

## Key Commands

```bash
cargo check                        # Validate compilation
cargo test                         # Execute test suite
cargo clippy -- -Dwarnings         # Run lints (strict)
cargo fmt -- --check               # Verify formatting
cargo run -p editor                # Launch the application
cargo run -p wm_core --bin validate # Run developer validation tool
```
