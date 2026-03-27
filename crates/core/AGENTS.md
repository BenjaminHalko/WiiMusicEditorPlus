# AI Agent Reference: wm_core

Purpose: `wm_core` library containing all domain logic for Wii Music modding. No GUI or hardcoded runtime paths are allowed in this crate.

## Core Modules

- **`message`**: Handles `WiiMessages` (BMG) loading/saving from the ROM folder. Provides an extract/encode workflow for external text editors.
- **`dol`**: Manages reading and writing song and style configurations within the `main.dol` executable.
- **`brsar`**: Domain-specific wrapper for `brsar::Brsar`.
- **`midi`**: Prepares and converts MIDI files to the game's RSEQ format.
- **`rom`**: Manages ROM-level operations like region detection and extraction using the `iso` crate.
- **`rom_folder`**: The `RomFolder` struct acts as a primary interface for the game's file hierarchy.
  - Owns `brsar` and `main.dol` data.
  - Provides path helpers (e.g., `main_dol_path`, `brsar_path`).
  - `resolve_base()` correctly handles both `path/sys/main.dol` and `path/DATA/sys/main.dol` layouts.
- **`editor`**: Provides high-level song and style replacement operations, including BRSAR group index formulas.
- **`archive`**: Handles importing and exporting custom song packages (ZIP format).
- **`riivolution`**: Generates Riivolution XML patches for playing mods on a console.
- **`reset`**: Allows reverting individual songs or styles to their original ROM values.
- **`checksum`**: Performs SHA1 hashing for file integrity checks (e.g., verifying a clean ROM).

## Developer Validation Tool

The `validate` binary is a developer-only non-destructive test tool.

- **Usage**: `cargo run -p wm_core --bin validate [ROM_FOLDER] [WBFS_FILE]`
- **Capabilities**: Exercises the full read/write surface of the library.
- **Safety**: Automatically snapshots and restores any modified files during the test run.
- **Extraction Test**: If a WBFS path is provided, it will also test the extraction process.
