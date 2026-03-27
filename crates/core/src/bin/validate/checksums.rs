use std::path::{Path, PathBuf};
use wm_core::{
    checksum::sha1_file,
    rom::detect_region,
    rom_folder::{
        HASH_US_BRSAR, HASH_US_MAIN_DOL, HASH_US_MESSAGE_FR, HASH_US_MESSAGE_SP, HASH_US_MESSAGE_US,
    },
    types::Region,
};

use super::Results;

fn check_hash(r: &mut Results, label: &str, path: &Path, expected: &str) {
    match sha1_file(path) {
        Err(e) => r.fail(label, &e.to_string()),
        Ok(actual) if actual == expected => r.ok(label, "hash matches"),
        Ok(actual) => r.fail(
            label,
            &format!("expected {expected}\n           got      {actual}"),
        ),
    }
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

pub(super) fn test_checksums(r: &mut Results, rom_folder: &Path) {
    println!("\n=== Section 5: File Checksums ===");

    let region = match detect_region(rom_folder) {
        Ok(region) => region,
        Err(e) => {
            r.fail("detect_region for checksums", &e.to_string());
            return;
        }
    };

    if region != Region::US {
        println!("  [SKIP] No known hashes for {region:?} region — TODO");
        return;
    }

    let base = resolve_base(rom_folder);
    let dol = base.join("sys/main.dol");
    let brsar = base.join("files/Sound/MusicStatic/rp_Music_sound.brsar");
    let msg_us = base.join("files/US/Message/message.carc");
    let msg_fr = base.join("files/FU/Message/message.carc");
    let msg_sp = base.join("files/SU/Message/message.carc");

    check_hash(r, "main.dol SHA1", &dol, HASH_US_MAIN_DOL);
    check_hash(r, "rp_Music_sound.brsar SHA1", &brsar, HASH_US_BRSAR);
    check_hash(r, "message.carc (US) SHA1", &msg_us, HASH_US_MESSAGE_US);
    check_hash(r, "message.carc (FR) SHA1", &msg_fr, HASH_US_MESSAGE_FR);
    check_hash(r, "message.carc (SP) SHA1", &msg_sp, HASH_US_MESSAGE_SP);
}
