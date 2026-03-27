# AI Agent Reference: carc

Purpose: Yaz0/U8 (CARC) archive + BMG message format + `WiiMessages` high-level API.

## Public API

The `carc` crate provides three primary types:

- `Carc`: Handles U8 archives, including Yaz0 compression/decompression.
- `Bmg`: Low-level parser and serializer for the BMG message format.
- `WiiMessages`: High-level API combining `Carc` and `Bmg` for Wii Music `message.carc` files.

### WiiMessages API

- `from_bytes(data: &[u8]) -> Result<Self, SzsError>`: Decodes a `.carc` and parses the embedded `new_music_message.bmg`.
- `to_bytes() -> Result<Vec<u8>, SzsError>`: Encodes the (modified) BMG and Yaz0-compresses it back into a CARC archive.
- `entries() -> &[BmgEntry]`: Returns all message entries.
- `set_text(index: usize, text: &str) -> Result<(), SzsError>`: Updates an entry's text by index.
- `to_text() -> String`: Renders all entries in Wiimms BMG text format (CRLF).
- `set_from_text(text: &str) -> Result<(), SzsError>`: Replaces all entries by parsing Wiimms BMG text.

Callers should use index-based access for programmatic editing rather than text round-trips to avoid overhead.

## BMG Format Gotchas

- **Magic**: The header magic is `b"MESGbmg1"` (lowercase `bmg`), NOT `b"MESGBMG1"`.
- **IDs**: Message IDs are not always 6 hex digits. They can range from 4 to 8 digits (e.g., `0x186a000`). Parse by searching for the ` @` separator in text format.
- **Empty Entries**: Entries can have empty text. The minimum line length in Wiimms format is 15 characters.
- **Escaping**: Embedded `\n` and `\r` in entry text are escaped as literal `\n` and `\r` strings in the text format.

## Archive Implementation

- `Carc` wraps Yaz0-compressed U8 archives.
- Decompression and U8 parsing are implemented in pure Rust.
- Encoding uses the `szs` crate for Yaz0 compression.

## Testing Policy

Unit tests use only synthetic fixtures — never real game files. Tests that need a real ROM folder live in the `validate` binary (`crates/core/src/bin/validate/`), not here. Do not add `#[ignore]` tests or hardcoded absolute paths to this crate.
