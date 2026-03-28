use std::path::{Path, PathBuf};

use brsar::Brsar;
use wm_core::{data::SONG_LIST, dol::MainDol, rom::detect_region, rom_folder::RomFolder};

use super::Results;

pub(super) fn load_brsar(rom_folder: &Path) -> Result<Brsar, String> {
    let path = resolve_base(rom_folder)
        .join("files")
        .join("Sound")
        .join("MusicStatic")
        .join("rp_Music_sound.brsar");
    let data = std::fs::read(&path).map_err(|e| format!("read {}: {e}", path.display()))?;
    Brsar::parse(data).map_err(|e| e.to_string())
}

pub(super) fn load_dol(rom_folder: &Path) -> Result<MainDol, String> {
    let path = resolve_base(rom_folder).join("sys").join("main.dol");
    let data = std::fs::read(&path).map_err(|e| format!("read {}: {e}", path.display()))?;
    Ok(MainDol::parse(data))
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

pub(super) fn test_reads(r: &mut Results, rom_folder: &Path) {
    println!("\n=== Section 1: Read Operations ===");

    match detect_region(rom_folder) {
        Ok(region) => r.ok("detect_region", &format!("{region:?}")),
        Err(e) => r.fail("detect_region", &e.to_string()),
    }

    match load_brsar(rom_folder) {
        Ok(brsar) => match brsar.get_song(0) {
            Ok(song) => r.ok(
                "BRSAR parse + get_song(0)",
                &format!("{} bytes", song.len()),
            ),
            Err(e) => r.fail("BRSAR get_song(0)", &e.to_string()),
        },
        Err(e) => r.fail("BRSAR parse", &e),
    }

    match load_dol(rom_folder) {
        Ok(dol) => {
            let inst = dol.read_style_instruments(0);
            r.ok("DOL read_style_instruments(0)", &format!("{:?}", inst.0));
        }
        Err(e) => r.fail("DOL parse", &e),
    }

    match load_dol(rom_folder) {
        Ok(dol) => {
            let val = dol.read_song_info(&SONG_LIST[0], 0);
            r.ok(
                "DOL read_song_info(song[0], seg 0)",
                &format!("{val:#010x}"),
            );
        }
        Err(e) => r.fail("DOL parse for song_info", &e),
    }

    match RomFolder::load(rom_folder, wm_core::types::Language::English, |_| {}) {
        Ok(rf) => r.ok(
            "RomFolder::load",
            &format!(
                "region={:?}, brsar={} bytes, dol={} bytes",
                rf.region,
                rf.brsar.len(),
                rf.main_dol.len()
            ),
        ),
        Err(e) => r.fail("RomFolder::load", &e.to_string()),
    }
}
