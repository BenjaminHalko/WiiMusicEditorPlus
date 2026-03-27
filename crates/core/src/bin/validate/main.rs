//! Developer validation tool for `wm_core`.
//!
//! Exercises the full read/write surface of the library against a real
//! extracted Wii Music ROM folder, printing clear PASS/FAIL results.
//!
//! ```text
//! Usage: validate [ROM_FOLDER] [WBFS_FILE]
//!
//!   ROM_FOLDER   Path to extracted Wii Music ROM folder (default: auto-detect sibling ../R64E01)
//!   WBFS_FILE    Path to Wii Music .wbfs/.iso file for extraction test (optional)
//!
//! Examples:
//!   cargo run -p wm_core --bin validate
//!   cargo run -p wm_core --bin validate -- /path/to/R64E01
//!   cargo run -p wm_core --bin validate -- /path/to/R64E01 /path/to/R64E01.wbfs
//! ```

mod checksums;
mod extraction;
mod message;
mod midi;
mod reads;
mod writes;

use std::path::{Path, PathBuf};
use std::process;
use wm_core::rom::extract_rom;

pub struct Results {
    passed: u32,
    failed: u32,
}

impl Results {
    fn new() -> Self {
        Self {
            passed: 0,
            failed: 0,
        }
    }

    pub fn ok(&mut self, label: &str, detail: &str) {
        println!("  [PASS] {label} — {detail}");
        self.passed += 1;
    }

    pub fn fail(&mut self, label: &str, detail: &str) {
        println!("  [FAIL] {label} — {detail}");
        self.failed += 1;
    }
}

const USAGE: &str = "\
Usage: validate [ROM_FOLDER] [WBFS_FILE]

  ROM_FOLDER   Path to extracted Wii Music ROM folder (default: auto-detect sibling ../R64E01)
  WBFS_FILE    Path to Wii Music .wbfs/.iso file for extraction test (optional)

Examples:
  cargo run -p wm_core --bin validate
  cargo run -p wm_core --bin validate -- /path/to/R64E01
  cargo run -p wm_core --bin validate -- /path/to/R64E01 /path/to/R64E01.wbfs";

struct CliArgs {
    rom_folder: PathBuf,
    wbfs_file: Option<PathBuf>,
}

fn parse_args() -> CliArgs {
    let args: Vec<String> = std::env::args().skip(1).collect();

    if args.iter().any(|a| a == "--help" || a == "-h") {
        println!("{USAGE}");
        process::exit(0);
    }

    let rom_folder = if let Some(first) = args.first() {
        PathBuf::from(first)
    } else {
        let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        manifest
            .parent()
            .and_then(Path::parent)
            .and_then(Path::parent)
            .map_or_else(
                || {
                    eprintln!("error: cannot auto-detect ROM folder from CARGO_MANIFEST_DIR");
                    eprintln!("{USAGE}");
                    process::exit(1);
                },
                |p| p.join("R64E01"),
            )
    };

    let wbfs_file = args.get(1).map(PathBuf::from);

    CliArgs {
        rom_folder,
        wbfs_file,
    }
}

fn main() {
    let cli = parse_args();
    let mut r = Results::new();

    println!("validate — wm_core developer validation tool");
    println!("ROM folder: {}", cli.rom_folder.display());
    if let Some(ref wbfs) = cli.wbfs_file {
        println!("WBFS file:  {}", wbfs.display());
    }

    // If the ROM folder doesn't exist but a WBFS was provided, extract it first.
    if !cli.rom_folder.is_dir() {
        if let Some(ref wbfs) = cli.wbfs_file {
            println!("\nROM folder not found — extracting from WBFS...");
            match extract_rom(wbfs, &cli.rom_folder) {
                Ok(()) => println!("Extraction complete: {}\n", cli.rom_folder.display()),
                Err(e) => {
                    eprintln!("error: extraction failed — {e}");
                    process::exit(1);
                }
            }
        } else {
            eprintln!(
                "error: ROM folder does not exist and no WBFS provided for extraction: {}",
                cli.rom_folder.display()
            );
            eprintln!("{USAGE}");
            process::exit(1);
        }
    }

    reads::test_reads(&mut r, &cli.rom_folder);
    writes::test_brsar_writes(&mut r, &cli.rom_folder);
    writes::test_dol_writes(&mut r, &cli.rom_folder);

    if let Some(ref wbfs) = cli.wbfs_file {
        if wbfs.is_file() {
            extraction::test_rom_extraction(&mut r, wbfs);
        } else {
            eprintln!(
                "warning: WBFS file does not exist, skipping extraction test: {}",
                wbfs.display()
            );
        }
    } else {
        println!("\n=== Section 4: ROM Extraction ===");
        println!("  [SKIP] No WBFS_FILE argument provided");
    }

    checksums::test_checksums(&mut r, &cli.rom_folder);
    message::test_message(&mut r, &cli.rom_folder);
    midi::test_midi(&mut r);

    println!("\n=== Results ===");
    println!("  Passed: {}", r.passed);
    println!("  Failed: {}", r.failed);

    if r.failed > 0 {
        process::exit(1);
    }
}
// This is temporary, will be removed
