# AI Agent Reference: iso

Purpose: Wii/GC disc image extraction (WBFS/ISO) wrapping the `nod` crate.

## Public API

- `extract(source: &Path, dest: &Path) -> Result<(), IsoError>`: Extracts all files from a disc image.
- `extract_with_progress(source, dest, on_progress: Fn(f32)) -> Result<(), IsoError>`: Extraction with a progress callback (0.0 to 1.0).

## Output Layout

Extraction produces a Dolphin-compatible directory structure:

- **`dest/disc/`**: Physical disc-level metadata.
  - `header.bin` — raw disc header.
  - `region.bin` — Wii region data (Wii only).
- **`dest/sys/`**: Core partition executable data.
  - `boot.bin`, `bi2.bin`, `apploader.img`, `main.dol`, `fst.bin`.
- **`dest/ticket.bin`**: Partition ticket (Wii only).
- **`dest/tmd.bin`**: Title metadata (Wii only).
- **`dest/cert.bin`**: Certificate chain (Wii only).
- **`dest/h3.bin`**: H3 hash table (Wii only).
- **`dest/files/`**: Full game FST filesystem content.

## Dependency

- This crate wraps the `nod` crate for native disc image handling.
- Supported image formats: `.iso`, `.wbfs`.
- Uses `nod` version `2.0.0-alpha.6`.
