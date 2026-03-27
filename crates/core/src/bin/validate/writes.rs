use std::path::Path;
use wm_core::{
    data::{SONG_LIST, STYLE_LIST},
    types::StyleInstruments,
};

use super::Results;
use super::reads::{load_brsar, load_dol};

pub(super) fn test_brsar_writes(r: &mut Results, rom_folder: &Path) {
    println!("\n=== Section 2: BRSAR Write / Manipulation ===");

    let mut brsar = match load_brsar(rom_folder) {
        Ok(b) => b,
        Err(e) => {
            r.fail("BRSAR load for write tests", &e);
            return;
        }
    };

    let original = match brsar.get_song(0) {
        Ok(d) => d,
        Err(e) => {
            r.fail("BRSAR get_song(0) for write test", &e.to_string());
            return;
        }
    };

    if original.is_empty() {
        r.fail(
            "BRSAR replace_song round-trip",
            "original song is empty, cannot test",
        );
        return;
    }

    let mut modified = original.clone();
    modified[0] ^= 0xFF;

    if let Err(e) = brsar.replace_song(0, &modified) {
        r.fail("BRSAR replace_song (write modified)", &e.to_string());
        return;
    }

    match brsar.get_song(0) {
        Ok(readback) => {
            if readback == modified {
                r.ok(
                    "BRSAR replace_song (verify modified)",
                    &format!("{} bytes, first byte flipped", readback.len()),
                );
            } else {
                r.fail(
                    "BRSAR replace_song (verify modified)",
                    &format!(
                        "data mismatch: expected first byte {:#04x}, got {:#04x}",
                        modified[0],
                        readback.first().copied().unwrap_or(0)
                    ),
                );
            }
        }
        Err(e) => {
            r.fail("BRSAR get_song after replace", &e.to_string());
            return;
        }
    }

    if let Err(e) = brsar.replace_song(0, &original) {
        r.fail("BRSAR replace_song (restore original)", &e.to_string());
        return;
    }

    match brsar.get_song(0) {
        Ok(readback) => {
            if readback == original {
                r.ok(
                    "BRSAR replace_song (verify restored)",
                    &format!("{} bytes, matches original", readback.len()),
                );
            } else {
                r.fail(
                    "BRSAR replace_song (verify restored)",
                    "restored data does not match original",
                );
            }
        }
        Err(e) => r.fail("BRSAR get_song after restore", &e.to_string()),
    }
}

pub(super) fn test_dol_writes(r: &mut Results, rom_folder: &Path) {
    println!("\n=== Section 3: DOL Write / Manipulation ===");

    let mut dol = match load_dol(rom_folder) {
        Ok(d) => d,
        Err(e) => {
            r.fail("DOL load for write tests", &e);
            return;
        }
    };

    let original_instruments = dol.read_style_instruments(0);
    let test_instruments = StyleInstruments([1, 2, 3, 4, 5, 6]);

    dol.write_style_instruments(0, &test_instruments);
    let readback = dol.read_style_instruments(0);

    if readback == test_instruments {
        r.ok(
            "DOL write_style_instruments (verify written)",
            &format!("{:?}", readback.0),
        );
    } else {
        r.fail(
            "DOL write_style_instruments (verify written)",
            &format!("expected {:?}, got {:?}", test_instruments.0, readback.0),
        );
    }

    dol.write_style_instruments(0, &original_instruments);
    let restored = dol.read_style_instruments(0);

    if restored == original_instruments {
        r.ok(
            "DOL write_style_instruments (verify restored)",
            &format!("{:?}", restored.0),
        );
    } else {
        r.fail(
            "DOL write_style_instruments (verify restored)",
            &format!(
                "expected {:?}, got {:?}",
                original_instruments.0, restored.0
            ),
        );
    }

    let song = &SONG_LIST[0];
    let original_val = dol.read_song_info(song, 0);

    dol.write_song_info(song, 0, 0xDEAD_BEEF);
    let readback_val = dol.read_song_info(song, 0);

    if readback_val == 0xDEAD_BEEF {
        r.ok(
            "DOL write_song_info (verify written)",
            &format!("{readback_val:#010x}"),
        );
    } else {
        r.fail(
            "DOL write_song_info (verify written)",
            &format!("expected 0xDEADBEEF, got {readback_val:#010x}"),
        );
    }

    dol.write_song_info(song, 0, original_val);
    let restored_val = dol.read_song_info(song, 0);

    if restored_val == original_val {
        r.ok(
            "DOL write_song_info (verify restored)",
            &format!("{restored_val:#010x}"),
        );
    } else {
        r.fail(
            "DOL write_song_info (verify restored)",
            &format!("expected {original_val:#010x}, got {restored_val:#010x}"),
        );
    }

    let mut patched_dol = match load_dol(rom_folder) {
        Ok(d) => d,
        Err(e) => {
            r.fail("DOL load for style patch test", &e);
            return;
        }
    };
    let backup_dol = patched_dol.clone();
    patched_dol.remove_style_execution(&backup_dol);

    let mut mismatches = Vec::new();
    for (index, style) in STYLE_LIST.iter().enumerate() {
        let got = patched_dol.read_style_instruments(index);
        if got != style.instruments {
            mismatches.push(format!(
                "style {} '{}': expected {:?}, got {:?}",
                index, style.name, style.instruments.0, got.0
            ));
        }
    }

    if mismatches.is_empty() {
        r.ok(
            "DOL remove_style_execution — all styles match STYLE_LIST",
            &format!("{} styles verified", STYLE_LIST.len()),
        );
    } else {
        r.fail(
            "DOL remove_style_execution — style mismatch",
            &mismatches.join(", "),
        );
    }
}
