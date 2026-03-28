# AI Agent Reference: editor

Purpose: Slint-based GUI binary for the Wii Music Editor.

## Architecture

- **Framework**: Built with the Slint GUI framework (declarative `.slint` files, compiled via `build.rs`).
- **Main Executable**: Produces the `wii-music-editor` binary.
- **Entry Point**: `ui/app-window.slint` — declares `AppWindow`, the `Screen` enum, and all per-editor properties and callbacks.
- **Build Script**: `build.rs` calls `slint_build::compile_with_config` with `DefaultTranslationContext::None`.

## UI Structure

- `ui/app-window.slint` — root `AppWindow` component; owns all properties and routes navigation via the `Screen` enum.
- `ui/main-menu.slint` — 3×3 Wii-channel grid home screen.
- `ui/bottom-bar.slint` — persistent bottom bar (back button / nav arrows).
- Per-editor screens: `song-editor.slint`, `style-editor.slint`, `text-editor.slint`, `default-style-editor.slint`, `remove-songs.slint`, `pack-rom.slint`, `riivolution.slint`, `revert-changes.slint`, `app-settings.slint`.

## Rust-Side Wiring

Slint is single-threaded. Share mutable state between callbacks with `Rc<RefCell<T>>`:

```rust
let state = Rc::new(RefCell::new(AppState::new()));
let app_weak = app.as_weak();
app.on_cfg_browse_rom({
    let state = state.clone();
    let app_weak = app_weak.clone();
    move || { /* ... */ }
});
```

Property setters: `app.set_<property>(value)`. Getters: `app.get_<property>()`. Callback registration: `app.on_<callback>(closure)`.

## Submodules

- **`app_state`**: `AppState` struct — owns `Option<RomFolder>`, settings path, `DiscordPresence`.
- **`discord`**: Discord Rich Presence integration (`DiscordPresence::new()`, `update(state)`, `disconnect()`).
- **`updater`**: Automatic application updates via `self_update`.
- **`external_editor`**: Launches the system text editor for BMG message files.
- **`settings`**: INI read/write (`load_setting`, `save_setting`) — backward compatible with Python v1/v2.

## Internationalization (i18n)

- **Gettext**: Strings are marked `@tr("…")` inline in `.slint` files. No separate string-ID lookup.
- **Runtime**: `slint::init_translations!(path)` loads `.mo` files from `{path}/{locale}/LC_MESSAGES/editor.mo`. Falls back to the source string when no `.mo` is present (development default).
- **Extraction**: `slint-tr-extractor --no-default-translation-context ui/*.slint -o i18n/editor.pot`, then `msgcat --no-location` to strip line references.
- **Crowdin**: Source is `i18n/editor.pot`; translations are `i18n/{locale}/LC_MESSAGES/editor.po`. CI auto-regenerates the `.pot` on `.slint` changes and skips the Crowdin sync when strings are unchanged.
