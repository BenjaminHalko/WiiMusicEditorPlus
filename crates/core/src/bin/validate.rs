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

use std::path::{Path, PathBuf};
use std::process;
use wm_core::{
    brsar::Brsar,
    checksum::sha1_file,
    data::SONG_LIST,
    dol::MainDol,
    paths::{dev_platform_tools_subdir, WmPaths},
    rom::{detect_region, extract_rom},
    rom_folder::{
        RomFolder, HASH_US_BRSAR, HASH_US_MAIN_DOL, HASH_US_MESSAGE_FR, HASH_US_MESSAGE_SP,
        HASH_US_MESSAGE_US,
    },
    types::{Region, StyleInstruments},
};

struct Results {
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

    fn ok(&mut self, label: &str, detail: &str) {
        println!("  [PASS] {label} — {detail}");
        self.passed += 1;
    }

    fn fail(&mut self, label: &str, detail: &str) {
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

fn make_paths() -> WmPaths {
    let workspace_root = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .and_then(Path::parent)
        .expect("cannot resolve workspace root")
        .to_path_buf();
    let tools = workspace_root
        .join("tools")
        .join(dev_platform_tools_subdir());
    WmPaths::new(&tools, "/res", "/config")
}

fn load_brsar(rom_folder: &Path) -> Result<Brsar, String> {
    let path = rom_folder.join("DATA/files/Sound/RPMusicCommon/rp_Ssn_sound.brsar");
    let data = std::fs::read(&path).map_err(|e| format!("read {}: {e}", path.display()))?;
    Brsar::parse(data).map_err(|e| e.to_string())
}

fn load_dol(rom_folder: &Path) -> Result<MainDol, String> {
    let path = rom_folder.join("DATA/sys/main.dol");
    let data = std::fs::read(&path).map_err(|e| format!("read {}: {e}", path.display()))?;
    Ok(MainDol::parse(data))
}

fn test_reads(r: &mut Results, rom_folder: &Path, paths: &WmPaths) {
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

    match RomFolder::load(rom_folder, paths) {
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

fn test_brsar_writes(r: &mut Results, rom_folder: &Path) {
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

fn test_dol_writes(r: &mut Results, rom_folder: &Path) {
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
}

fn test_rom_extraction(r: &mut Results, wbfs_path: &Path, paths: &WmPaths) {
    println!("\n=== Section 4: ROM Extraction ===");

    let temp_dir = match tempfile::TempDir::new() {
        Ok(d) => d,
        Err(e) => {
            r.fail("ROM extraction (create temp dir)", &e.to_string());
            return;
        }
    };

    let output_dir = temp_dir.path().join("extracted");

    match extract_rom(paths, wbfs_path, &output_dir) {
        Ok(()) => {
            r.ok(
                "extract_rom",
                &format!("extracted to {}", output_dir.display()),
            );

            let dol_path = output_dir.join("DATA/sys/main.dol");
            if dol_path.is_file() {
                r.ok("extracted main.dol exists", &dol_path.display().to_string());
            } else {
                r.fail(
                    "extracted main.dol exists",
                    &format!("{} not found", dol_path.display()),
                );
            }

            let brsar_path = output_dir.join("DATA/files/Sound/RPMusicCommon/rp_Ssn_sound.brsar");
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

fn test_checksums(r: &mut Results, rom_folder: &Path) {
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

    let dol = rom_folder.join("DATA/sys/main.dol");
    let brsar = rom_folder.join("DATA/files/Sound/MusicStatic/rp_Music_sound.brsar");
    let msg_us = rom_folder.join("DATA/files/US/Message/message.carc");
    let msg_fr = rom_folder.join("DATA/files/FU/Message/message.carc");
    let msg_sp = rom_folder.join("DATA/files/SU/Message/message.carc");

    check_hash(r, "main.dol SHA1", &dol, HASH_US_MAIN_DOL);
    check_hash(r, "rp_Music_sound.brsar SHA1", &brsar, HASH_US_BRSAR);
    check_hash(r, "message.carc (US) SHA1", &msg_us, HASH_US_MESSAGE_US);
    check_hash(r, "message.carc (FR) SHA1", &msg_fr, HASH_US_MESSAGE_FR);
    check_hash(r, "message.carc (SP) SHA1", &msg_sp, HASH_US_MESSAGE_SP);
}

fn test_message(r: &mut Results, rom_folder: &Path, paths: &WmPaths) {
    println!("\n=== Section 6: Message Text ===");

    match wm_core::message::extract(paths, rom_folder) {
        Err(e) => {
            r.fail("message extract", &e.to_string());
            return;
        }
        Ok(()) => r.ok("message extract", "wszst+wbmgt succeeded"),
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

    match wm_core::message::encode(paths, rom_folder) {
        Err(e) => r.fail("message encode", &e.to_string()),
        Ok(()) => r.ok("message encode", "wbmgt+wszst succeeded"),
    }
}

fn find_message_txt(rom_folder: &Path) -> Option<PathBuf> {
    let files_dir = rom_folder.join("DATA/files");
    for entry in std::fs::read_dir(&files_dir).ok()?.flatten() {
        let candidate = entry.path().join("Message/message.d/new_music_message.txt");
        if candidate.is_file() {
            return Some(candidate);
        }
    }
    None
}

fn test_midi(r: &mut Results, paths: &WmPaths) {
    use std::io::Write;

    use midly::num::{u15, u28, u4, u7};
    use midly::{
        Format, Header, MetaMessage, MidiMessage, Smf, Timing, TrackEvent, TrackEventKind,
    };

    println!("\n=== Section 7: MIDI ===");

    let smf = Smf {
        header: Header {
            format: Format::Parallel,
            timing: Timing::Metrical(u15::from(0x01E0)),
        },
        tracks: vec![
            vec![
                TrackEvent {
                    delta: u28::from(0),
                    kind: TrackEventKind::Midi {
                        channel: u4::from(1),
                        message: MidiMessage::NoteOn {
                            key: u7::from(60),
                            vel: u7::from(100),
                        },
                    },
                },
                TrackEvent {
                    delta: u28::from(0x78),
                    kind: TrackEventKind::Midi {
                        channel: u4::from(1),
                        message: MidiMessage::NoteOn {
                            key: u7::from(60),
                            vel: u7::from(0),
                        },
                    },
                },
                TrackEvent {
                    delta: u28::from(0),
                    kind: TrackEventKind::Meta(MetaMessage::EndOfTrack),
                },
            ],
            vec![
                TrackEvent {
                    delta: u28::from(0),
                    kind: TrackEventKind::Midi {
                        channel: u4::from(2),
                        message: MidiMessage::NoteOn {
                            key: u7::from(64),
                            vel: u7::from(80),
                        },
                    },
                },
                TrackEvent {
                    delta: u28::from(0),
                    kind: TrackEventKind::Meta(MetaMessage::EndOfTrack),
                },
            ],
        ],
    };

    let mut midi_bytes = Vec::new();
    if let Err(e) = smf.write_std(&mut midi_bytes) {
        r.fail("midi build synthetic", &e.to_string());
        return;
    }

    let mut midi_file = match tempfile::Builder::new().suffix(".mid").tempfile() {
        Ok(file) => file,
        Err(e) => {
            r.fail("midi create tempfile", &e.to_string());
            return;
        }
    };

    if let Err(e) = midi_file
        .write_all(&midi_bytes)
        .and_then(|()| midi_file.as_file_mut().flush())
    {
        r.fail("midi write tempfile", &e.to_string());
        return;
    }

    // Test prepare_midi (with fixes)
    match wm_core::midi::prepare_midi(midi_file.path()) {
        Err(e) => {
            r.fail("midi prepare_midi", &e.to_string());
            return;
        }
        Ok(prepared) => {
            r.ok(
                "midi prepare_midi",
                "2-track→single-track, channel 0, NoteOn(vel=0)→NoteOff",
            );

            // Test convert_to_sequence (with prepare)
            let output = prepared.path().with_extension("brseq");
            match wm_core::midi::convert_to_sequence(paths, midi_file.path(), &output) {
                Err(e) => r.fail("midi convert_to_sequence", &e.to_string()),
                Ok(()) => {
                    let size = std::fs::metadata(&output).map_or(0, |m| m.len());
                    r.ok(
                        "midi convert_to_sequence",
                        &format!(".brseq = {size} bytes"),
                    );
                }
            }

            // Test convert_to_sequence_raw (without prepare)
            let output_raw = prepared.path().with_extension("raw.brseq");
            match wm_core::midi::convert_to_sequence_raw(paths, midi_file.path(), &output_raw) {
                Err(e) => r.fail("midi convert_to_sequence_raw", &e.to_string()),
                Ok(()) => {
                    let size = std::fs::metadata(&output_raw).map_or(0, |m| m.len());
                    r.ok(
                        "midi convert_to_sequence_raw",
                        &format!(".brseq = {size} bytes"),
                    );
                }
            }
        }
    }
}

fn main() {
    let cli = parse_args();
    let paths = make_paths();
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
            match extract_rom(&paths, wbfs, &cli.rom_folder) {
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

    test_reads(&mut r, &cli.rom_folder, &paths);
    test_brsar_writes(&mut r, &cli.rom_folder);
    test_dol_writes(&mut r, &cli.rom_folder);

    if let Some(ref wbfs) = cli.wbfs_file {
        if wbfs.is_file() {
            test_rom_extraction(&mut r, wbfs, &paths);
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

    test_checksums(&mut r, &cli.rom_folder);
    test_message(&mut r, &cli.rom_folder, &paths);
    test_midi(&mut r, &paths);

    println!("\n=== Results ===");
    println!("  Passed: {}", r.passed);
    println!("  Failed: {}", r.failed);

    if r.failed > 0 {
        process::exit(1);
    }
}
