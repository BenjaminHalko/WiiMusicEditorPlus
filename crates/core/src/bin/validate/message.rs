use std::path::{Path, PathBuf};

use super::Results;

fn find_message_txt(rom_folder: &Path) -> Option<PathBuf> {
    let files_dir = resolve_base(rom_folder).join("files");
    for entry in std::fs::read_dir(&files_dir).ok()?.flatten() {
        let candidate = entry.path().join("Message/message.d/new_music_message.txt");
        if candidate.is_file() {
            return Some(candidate);
        }
    }
    None
}

fn find_message_carc(rom_folder: &Path) -> Option<PathBuf> {
    let files_dir = resolve_base(rom_folder).join("files");
    for entry in std::fs::read_dir(&files_dir).ok()?.flatten() {
        let candidate = entry.path().join("Message/message.carc");
        if candidate.is_file() {
            return Some(candidate);
        }
    }
    None
}

fn resolve_base(path: &Path) -> PathBuf {
    if path.join("sys").join("main.dol").is_file() {
        return path.to_path_buf();
    }

    let data = path.join("DATA");
    if data.join("sys").join("main.dol").is_file() {
        return data;
    }

    path.to_path_buf()
}

pub(super) fn test_message(r: &mut Results, rom_folder: &Path) {
    println!("\n=== Section 6: Message Text ===");

    // Snapshot message.carc before any disk writes so the ROM folder stays
    // idempotent across consecutive validate runs.
    let carc_snapshot: Option<(PathBuf, Vec<u8>)> =
        find_message_carc(rom_folder).and_then(|p| std::fs::read(&p).ok().map(|b| (p, b)));

    match wm_core::message::extract(rom_folder) {
        Err(e) => {
            r.fail("message extract", &e.to_string());
            return;
        }
        Ok(()) => r.ok("message extract", "carc+bmg decode succeeded"),
    }

    let Some(txt_path) = find_message_txt(rom_folder) else {
        r.fail("find message.txt", "could not locate decoded text file");
        return;
    };

    match wm_core::message::parse_text_file(&txt_path) {
        Err(e) => r.fail("message parse_text_file", &e.to_string()),
        Ok(entries) => {
            r.ok(
                "message parse_text_file",
                &format!("{} entries", entries.len()),
            );
            let has_known = entries
                .iter()
                .any(|entry| entry.text.contains("Night Music") || entry.text.contains("Mii"));
            if has_known {
                r.ok(
                    "message known song names present",
                    "found expected song names",
                );
            } else {
                r.fail(
                    "message known song names present",
                    "no recognizable song names found",
                );
            }
        }
    }

    match wm_core::message::encode(rom_folder) {
        Err(e) => r.fail("message encode", &e.to_string()),
        Ok(()) => r.ok("message encode", "bmg+carc encode succeeded"),
    }

    // Verify each song's BMG name ID resolves to the expected name (uses original bytes)
    if let Some((_, ref original_bytes)) = carc_snapshot {
        match carc::WiiMessages::from_bytes(original_bytes) {
            Err(e) => r.fail("song name BMG IDs", &e.to_string()),
            Ok(msgs) => {
                let mut mismatches = Vec::new();
                for song in wm_core::data::SONG_LIST {
                    if song.bmg_name_id() == 0 {
                        continue;
                    }
                    match msgs.entries().iter().find(|e| e.id == song.bmg_name_id()) {
                        None => mismatches.push(format!(
                            "{}: id {:#x} not found",
                            song.name,
                            song.bmg_name_id()
                        )),
                        Some(entry) if entry.text != song.name => mismatches.push(format!(
                            "{:#x}: expected {:?}, got {:?}",
                            song.bmg_name_id(),
                            song.name,
                            entry.text
                        )),
                        Some(_) => {}
                    }
                }
                if mismatches.is_empty() {
                    r.ok("song name BMG IDs", "all song names match");
                } else {
                    r.fail("song name BMG IDs", &mismatches.join("; "));
                }
            }
        }
    }

    // In-memory round-trip using carc::WiiMessages directly
    if let Some(carc_path) = find_message_carc(rom_folder) {
        match std::fs::read(&carc_path) {
            Err(e) => r.fail("carc read", &e.to_string()),
            Ok(bytes) => match carc::WiiMessages::from_bytes(&bytes) {
                Err(e) => r.fail("WiiMessages::from_bytes", &e.to_string()),
                Ok(msgs) => {
                    let count = msgs.entries().len();
                    r.ok("WiiMessages in-memory parse", &format!("{count} entries"));
                    match msgs.to_bytes() {
                        Err(e) => r.fail("WiiMessages::to_bytes", &e.to_string()),
                        Ok(reencoded) => match carc::WiiMessages::from_bytes(&reencoded) {
                            Err(e) => r.fail("WiiMessages round-trip", &e.to_string()),
                            Ok(reparsed) if reparsed.entries().len() == count => r.ok(
                                "WiiMessages binary round-trip",
                                &format!("{count} entries preserved"),
                            ),
                            Ok(_) => r.fail("WiiMessages round-trip", "entry count mismatch"),
                        },
                    }
                }
            },
        }
    }

    if let Some((carc_path, original_bytes)) = carc_snapshot {
        let _ = std::fs::write(&carc_path, &original_bytes);
    }
}
