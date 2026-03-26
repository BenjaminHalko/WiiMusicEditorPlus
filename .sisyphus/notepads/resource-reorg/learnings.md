### Learnings
- `git mv` preserves history cleanly for bulk resource renames.
- UI-only assets (fonts, app icons) should live in the editor crate, while shared/save/tool assets stay in core.
- `cargo check --workspace` stayed green after the resource move.
