# Coding Guidelines: Wii Music Editor

This document defines the architectural and stylistic standards for the Wii Music Editor Rust rewrite. Adherence ensures consistency, safety, and reliability when handling legacy binary formats.

## 1. Naming Conventions

### Type Descriptions
Types should describe their role in the domain, not the data structure they use. Avoid suffixes like `Object`, `Struct`, or `Map`.
- **Good:** `SongEntry`, `StyleConfiguration`, `InstrumentMap`
- **Bad:** `SongObject`, `StyleStruct`, `InstrumentHashMap`

### Module Prefixes
Do not prefix types with the crate name or module name. Use module-qualified names if needed at the call site.
- **Good:** `StyleType` inside `wm_core::style`
- **Bad:** `WmStyleType` or `CoreStyleType`

### Constructors and Conversions
Follow standard Rust naming for object creation:
- `new(...)`: Default constructor.
- `from_bytes(data: &[u8])`: Parsing from raw data.
- `into_inner(self)`: Consuming conversion.

### Magic Numbers and Offsets
Never use raw literals for binary offsets or stride values.
- **Good:** `const SONG_SEGMENT_STRIDE: usize = 0xBC;`
- **Bad:** `let offset = base + 0xBC * index;`

## 2. Type Design

### Concrete Implementation
Prefer concrete types over traits unless multiple implementations are genuinely required. Wii Music's formats are stable and unlikely to change.
- **Good:** `struct BrsarParser`
- **Bad:** `trait SoundArchive { fn get_song(&self); }` if only BRSAR implements it.

### States and Flags
Use `Option<T>` or `Result<T, E>` instead of boolean flags to represent state.
- **Good:** `handles: Option<FileHandles>`
- **Bad:** `has_handles: bool, handles: FileHandles`

### Newtype Wrappers
Use newtypes for domain-specific IDs to prevent accidental mixing of values.
- **Good:** `struct InstrumentId(u8);`, `struct SongId(u16);`
- **Bad:** Using raw `u8` or `u16` for everything.

### Invariants
Keep fields private by default. Use constructors and setters to maintain data invariants (e.g., ensuring a BRSAR offset is always within file bounds).

### Derived Traits
Include standard derives in alphabetical order:
- `#[derive(Clone, Debug, Default, Eq, PartialEq)]`
- Add `Copy` only for small, POD (Plain Old Data) types.

## 3. Code Style

### Formatting and Imports
Use `cargo fmt` for formatting. Group imports logically:
1. `std`
2. External crates (`binrw`, `iced`, `midly`)
3. Workspace crates (`wm_core`)
4. Module-local imports (`use super::*;`)

### Documentation
Document traits and public APIs. For implementation blocks, only document behavior that deviates from expectations.
- **Focus:** Explain **WHY** a specific operation is performed, not **WHAT** the code is doing.
- **Bad:** `// Reads 4 bytes`
- **Good:** `// BRSAR uses 4-byte big-endian offsets for section references to navigate the hierarchy.`

## 4. Error Handling

### Propagation and Context
Use the `?` operator for error propagation. All fallible operations in `wm_core` must return `Result<T, WmError>`.
- **`WmError`:** A central enum covering I/O, parsing, tool execution, and domain violations.
- **Parsing Errors:** Include the file path and the offset where the error occurred in the error context.

### Avoid Panic
- **`unwrap()`:** Forbidden in library code. Use `.expect("...")` only if the failure is logically impossible (e.g., parsing a hardcoded constant).
- **Silent Failures:** Never swallow errors. If data is missing but non-critical, log it via `tracing::warn!`.

## 5. Binary Parsing Conventions

### Hex Literals (Non-Negotiable)
All values with binary significance MUST be written in hex. This includes offsets, magic numbers, sizes, masks, flags, and sentinel values.
```rust
// CORRECT
const SONG_SEGMENT_OFFSET: u32 = 0x59C5_20;
const BRSAR_MAGIC: u32 = 0x5253_4152; // "RSAR"
const NO_INSTRUMENT: u32 = 0xFFFF_FFFF;

// WRONG — never use decimal for binary values
const SONG_SEGMENT_OFFSET: u32 = 5883168;
const NO_INSTRUMENT: u32 = 4294967295;
```
Decimal is only acceptable for pure counts/indices with no binary significance (e.g. `SONG_COUNT: usize = 61`).

### Byte Order (Non-Negotiable)
Wii (PowerPC) is big-endian. All `binrw` structs MUST use the `#[br(big)]` attribute.
- **Check:** Double-check every struct for `#[br(big)]` or `#[binrw::br(big)]`.

### Offset Documentation
Every constant offset must be documented with a comment explaining what it points to in the DOL or BRSAR.
```rust
/// Points to the beginning of the regular song data segment in main.dol.
const SONG_REGULAR_OFFSET: u32 = 0x59C520;
```

### Validation and Round-trips
- **Magic Bytes:** Always verify magic headers (e.g., `RSAR`, `BMG `) during parsing.
- **Bounds Checking:** Validate offsets before seeking to prevent memory issues or crashes.
- **Testing:** Every parser should have a round-trip test: `Data -> Parse -> Modify -> Write -> Parse` must yield consistent results.

## 6. UI Patterns (Iced)

### View Decomposition
Break the UI into small, reusable view functions or components.
- Each page (Song, Style, Text) gets its own module.
- Use `Message` enum variants that accurately describe user intent.
- Avoid passing around the entire `App` state; pass only the required slice.

### State Management
- Keep logic in `wm_core` and only keep UI-specific state in the `editor` binary.
- Use `Command` to handle async operations like file loading or external tool execution.
- Update the UI only in the `update()` function.

## 7. Internationalization (I18n)

### Fluent Syntax
Use the Project Fluent (`.ftl`) format for all user-facing strings.
- Keys must be lowercase and hyphenated: `song-editor-title`.
- Do not hardcode strings in the UI code.
- Use variables in Fluent for dynamic data (e.g., `{ $count } songs loaded`).

### Workflow
1. Add key to `i18n/en-US/ui.ftl`.
2. Access via the `i18n` module in the editor binary.
3. Ensure fallback logic works for missing translations.

## 8. Testing Strategy

### Unit Testing
Place unit tests in a `tests` module at the bottom of the source file.
```rust
#[cfg(test)]
mod tests {
    use super::*;
    // ... tests ...
}
```

### Integration and Hardware Tests
Tests requiring real game data belong in the `validate` developer binary, not in `#[cfg(test)]` modules.
- Unit tests use only synthetic, minimal binary fixtures — never real game files.
- **No `#[ignore]`** — if a test cannot run without external data, it goes in `validate` instead.
- Run integration tests via: `cargo run -p wm_core --bin validate -- <ROM_FOLDER>`.
- **Never commit copyrighted game files to the repository.**

### Edge Cases
Always test:
- Empty archives.
- Truncated files.
- Max-length strings in BMG.
- Invalid song indices.

## 9. Workspace and Dependencies

- Add a dependency to a **crate's own `Cargo.toml`** unless two or more crates share it.
- Only promote a dependency to `[workspace.dependencies]` when it is used by multiple crates.
- Lint levels are inherited workspace-wide: `[lints] workspace = true`.
- Avoid `pub use crate::*`. Be explicit about re-exports.
- Use `pub(crate)` for internal logic not intended for the UI layer.

## 10. DOL Patching Specifics

### Code Safety
When patching executable code in `main.dol` (e.g., style execution removal), ensure the byte range matches the expected signature before overwriting. This prevents corruption if the user provides a modified or different version of the game.

### Instrumentation
Instrument 67 is a sentinel value (`0xFFFFFFFF`). Ensure the `InstrumentId` type handles this conversion safely without overflow or sign-extension bugs.

## 11. Native Format Crates

All game format operations use native Rust crates — no external tool binaries:
- **`iso`**: Wii disc extraction via the `nod` crate.
- **`carc`**: Yaz0/U8 archive and BMG message format.
- **`brsar`**: BRSAR sound archive and MIDI→RSEQ conversion.

Do not add shell-out calls or external tool dependencies. If a format operation is missing, implement it natively in the appropriate crate.

## 12. Patch Generation (Riivolution)

### XML Generation
Generate Riivolution XML files using a structured builder in `wm_core/src/riivolution.rs`.
- Use the `quick-xml` crate for robust generation.
- Ensure all file paths in the XML are correctly relative to the SD card root.
- Add descriptive names for each patch section to help the end-user.

### Integrity Checks
- Before generating a patch, verify that all modified files (BRSAR, DOL, BMG) exist.
- Compare the modified file sizes against the originals if necessary for compatibility.
- Log the generation process to help debug issues reported by users.
