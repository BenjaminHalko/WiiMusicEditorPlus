use std::path::Path;
use wm_core::rom::extract_rom;

use super::Results;

pub(super) fn test_rom_extraction(r: &mut Results, wbfs_path: &Path) {
    println!("\n=== Section 4: ROM Extraction ===");

    let temp_dir = match tempfile::TempDir::new() {
        Ok(d) => d,
        Err(e) => {
            r.fail("ROM extraction (create temp dir)", &e.to_string());
            return;
        }
    };

    let output_dir = temp_dir.path().join("extracted");

    match extract_rom(wbfs_path, &output_dir) {
        Ok(()) => {
            r.ok(
                "extract_rom",
                &format!("extracted to {}", output_dir.display()),
            );

            let dol_path = output_dir.join("sys/main.dol");
            if dol_path.is_file() {
                r.ok("extracted main.dol exists", &dol_path.display().to_string());
            } else {
                r.fail(
                    "extracted main.dol exists",
                    &format!("{} not found", dol_path.display()),
                );
            }

            let brsar_path = output_dir.join("files/Sound/MusicStatic/rp_Music_sound.brsar");
            if brsar_path.is_file() {
                r.ok("extracted BRSAR exists", &brsar_path.display().to_string());
            } else {
                r.fail(
                    "extracted BRSAR exists",
                    &format!("{} not found", brsar_path.display()),
                );
            }

            let file_count = count_files(&output_dir);
            r.ok("extracted file count", &format!("{file_count} files"));
        }
        Err(e) => r.fail("extract_rom", &e.to_string()),
    }
}

fn count_files(dir: &Path) -> usize {
    let mut count = 0;
    if let Ok(entries) = std::fs::read_dir(dir) {
        for entry in entries.flatten() {
            let path = entry.path();
            if path.is_dir() {
                count += count_files(&path);
            } else {
                count += 1;
            }
        }
    }
    count
}
