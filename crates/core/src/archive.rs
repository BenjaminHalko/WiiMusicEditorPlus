use crate::rom_folder::RomFolder;
use crate::types::WmError;
use std::fs;
use std::io::{Read, Write};
use std::path::Path;
use zip::write::SimpleFileOptions;
use zip::{ZipArchive, ZipWriter};

const MAIN_DOL_NAME: &str = "main.dol";
const BRSAR_NAME: &str = "rp_Music_sound.brsar";
const MESSAGE_CARC_NAME: &str = "message.carc";

fn zip_err(e: zip::result::ZipError) -> WmError {
    match e {
        zip::result::ZipError::Io(io_err) => WmError::Io(io_err),
        other => WmError::Io(std::io::Error::new(
            std::io::ErrorKind::InvalidData,
            other.to_string(),
        )),
    }
}

fn locate_message_carc(text_dir: &Path) -> Result<std::path::PathBuf, WmError> {
    for entry in fs::read_dir(text_dir)? {
        let region_path = entry?.path();
        let candidate = region_path.join("Message").join(MESSAGE_CARC_NAME);
        if candidate.is_file() {
            return Ok(candidate);
        }
    }
    Err(WmError::Io(std::io::Error::new(
        std::io::ErrorKind::NotFound,
        format!("message.carc not found under {}", text_dir.display()),
    )))
}

/// Packs the three modifiable ROM files into a ZIP archive.
///
/// The ZIP contains `main.dol`, `rp_Music_sound.brsar`, and `message.carc`.
/// The first two are read from the in-memory fields of `rom`; the message
/// archive is read from disk by scanning `rom.text_dir`.
///
/// # Errors
/// Returns `WmError::Io` if the archive cannot be created, a source file cannot
/// be read, or ZIP writing fails.
pub fn export_zip(rom: &RomFolder, output_path: &Path) -> Result<(), WmError> {
    let file = fs::File::create(output_path)?;
    let mut zip = ZipWriter::new(file);
    let options = SimpleFileOptions::default();

    zip.start_file(MAIN_DOL_NAME, options).map_err(zip_err)?;
    zip.write_all(&rom.main_dol)?;

    zip.start_file(BRSAR_NAME, options).map_err(zip_err)?;
    zip.write_all(&rom.brsar)?;

    let message_path = locate_message_carc(&rom.text_dir)?;
    let message_data = fs::read(&message_path)?;
    zip.start_file(MESSAGE_CARC_NAME, options)
        .map_err(zip_err)?;
    zip.write_all(&message_data)?;

    zip.finish().map_err(zip_err)?;
    Ok(())
}

/// Extracts files from a ZIP archive and applies them to the given `RomFolder`.
///
/// Recognized files (matched case-insensitively):
/// - `main.dol` → updates `rom.main_dol` and writes to disk
/// - `rp_Music_sound.brsar` → updates `rom.brsar` and writes to disk
/// - `message.carc` → writes to the on-disk message archive location
///
/// Unrecognized files are silently skipped.
///
/// # Errors
/// Returns `WmError::Io` if the input archive cannot be opened, entries cannot
/// be read, or output files cannot be written.
pub fn import_zip(path: &Path, rom: &mut RomFolder) -> Result<(), WmError> {
    let file = fs::File::open(path)?;
    let mut archive = ZipArchive::new(file).map_err(zip_err)?;

    for i in 0..archive.len() {
        let mut entry = archive.by_index(i).map_err(zip_err)?;
        let entry_name = entry.name().to_string();

        let file_name = match std::path::Path::new(&entry_name)
            .file_name()
            .and_then(|f| f.to_str())
        {
            Some(name) => name.to_string(),
            None => continue,
        };

        let mut data = Vec::new();
        entry.read_to_end(&mut data)?;

        if file_name.eq_ignore_ascii_case(MAIN_DOL_NAME) {
            rom.main_dol = data;
            fs::write(RomFolder::main_dol_path(&rom.base), &rom.main_dol)?;
        } else if file_name.eq_ignore_ascii_case(BRSAR_NAME) {
            rom.brsar = data;
            fs::write(RomFolder::brsar_path(&rom.base), &rom.brsar)?;
        } else if file_name.eq_ignore_ascii_case(MESSAGE_CARC_NAME) {
            let message_path = locate_message_carc(&rom.text_dir)?;
            fs::write(&message_path, &data)?;
        }
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::types::Region;

    fn setup_rom_dir(root: &Path) -> RomFolder {
        let sys_dir = root.join("DATA").join("sys");
        let sound_dir = root
            .join("DATA")
            .join("files")
            .join("Sound")
            .join("MusicStatic");
        let message_dir = root.join("DATA").join("files").join("US").join("Message");

        fs::create_dir_all(&sys_dir).expect("create sys dir");
        fs::create_dir_all(&sound_dir).expect("create sound dir");
        fs::create_dir_all(&message_dir).expect("create message dir");

        let dol_data = vec![0xDE, 0xAD, 0xBE, 0xEF];
        let brsar_data = vec![0xCA, 0xFE, 0xBA, 0xBE];
        let message_data = vec![0x01, 0x02, 0x03, 0x04];

        fs::write(sys_dir.join("main.dol"), &dol_data).expect("write main.dol");
        fs::write(sound_dir.join("rp_Music_sound.brsar"), &brsar_data).expect("write brsar");
        fs::write(message_dir.join("message.carc"), &message_data).expect("write message.carc");

        RomFolder {
            path: root.to_path_buf(),
            base: root.join("DATA"),
            region: Region::US,
            main_dol: dol_data,
            brsar: brsar_data,
            text_dir: root.join("DATA").join("files"),
            source_rom_path: None,
        }
    }

    #[test]
    fn round_trip_export_import() {
        let temp = tempfile::tempdir().expect("create tempdir");
        let rom = setup_rom_dir(temp.path());

        let zip_path = temp.path().join("export.zip");
        export_zip(&rom, &zip_path).expect("export should succeed");
        assert!(zip_path.is_file());

        // Modify ROM to prove import restores original state
        let mut modified_rom = rom.clone();
        modified_rom.main_dol = vec![0xFF];
        modified_rom.brsar = vec![0xFF];
        let message_path = locate_message_carc(&modified_rom.text_dir).expect("find message.carc");
        fs::write(&message_path, &[0xFF]).expect("modify message.carc");

        import_zip(&zip_path, &mut modified_rom).expect("import should succeed");

        // In-memory fields restored
        assert_eq!(modified_rom.main_dol, rom.main_dol);
        assert_eq!(modified_rom.brsar, rom.brsar);

        // On-disk files restored
        let restored_message =
            fs::read(locate_message_carc(&modified_rom.text_dir).expect("find message.carc"))
                .expect("read restored message.carc");
        assert_eq!(restored_message, vec![0x01, 0x02, 0x03, 0x04]);

        let restored_dol =
            fs::read(RomFolder::main_dol_path(&modified_rom.base)).expect("read dol");
        assert_eq!(restored_dol, rom.main_dol);

        let restored_brsar =
            fs::read(RomFolder::brsar_path(&modified_rom.base)).expect("read brsar");
        assert_eq!(restored_brsar, rom.brsar);
    }

    #[test]
    fn import_invalid_zip_returns_error() {
        let temp = tempfile::tempdir().expect("create tempdir");
        let mut rom = setup_rom_dir(temp.path());

        let bad_zip = temp.path().join("bad.zip");
        fs::write(&bad_zip, b"this is not a zip file").expect("write bad zip");

        let result = import_zip(&bad_zip, &mut rom);
        assert!(result.is_err());
    }

    #[test]
    fn import_zip_skips_unrecognized_files() {
        let temp = tempfile::tempdir().expect("create tempdir");
        let mut rom = setup_rom_dir(temp.path());
        let original_dol = rom.main_dol.clone();
        let original_brsar = rom.brsar.clone();

        // Create a ZIP with only an unrecognized file
        let zip_path = temp.path().join("unknown.zip");
        let file = fs::File::create(&zip_path).expect("create zip file");
        let mut zip = ZipWriter::new(file);
        let options = SimpleFileOptions::default();
        zip.start_file("unknown.bin", options).expect("start file");
        zip.write_all(&[0xAA, 0xBB]).expect("write data");
        zip.finish().expect("finish zip");

        import_zip(&zip_path, &mut rom).expect("import should succeed");

        // State unchanged
        assert_eq!(rom.main_dol, original_dol);
        assert_eq!(rom.brsar, original_brsar);
    }
}
