# AI Agent Reference: editor

Purpose: Iced-based GUI binary for the Wii Music Editor.

## Architecture

- **Framework**: Built with the Iced Rust GUI framework.
- **Main Executable**: Produces the `wii-music-editor` binary.

## Submodules

- **`discord`**: Implements Discord Rich Presence integration.
- **`updater`**: Handles automatic application updates.
- **`external_editor`**: Launches the system-configured text editor for editing BMG message files.

## Internationalization (i18n)

- **Fluent**: Uses the Project Fluent system for translations (`.ftl` files).
- **Type Safety**: Keys are validated at compile time using the `fl!()` macro.
- **Renaming**: Renaming a key in a translation file without updating the code will cause a compile error.
