use crate::{
    checksum::verify_checksum,
    paths::WmPaths,
    rom::{detect_region, extract_rom},
    types::{Region, WmError},
};
use std::path::{Path, PathBuf};

const DATA_DIR: &str = "DATA";
const SYS_DIR: &str = "sys";
const FILES_DIR: &str = "files";
const SOUND_DIR: &str = "Sound";
const MUSIC_STATIC_DIR: &str = "MusicStatic";

// Known SHA1 hashes for the US region extracted files.
// These are used by verify_main_dol() and verify_brsar() to detect ROM modifications.
// TODO: Add known hashes for EU, JP, KR regions when available.
pub const HASH_US_MAIN_DOL: &str = "a9ab9a8a8f14aa58d9bf4e05d72d29115ec589ab";
pub const HASH_US_BRSAR: &str = "fad7f8920eb956ba1fc1000e997d150dc28a1232";
pub const HASH_US_MESSAGE_US: &str = "45ac82faefe600965d863a2090502c4ffc7177f5";
pub const HASH_US_MESSAGE_FR: &str = "9b91ded8efa5b906f2ade135a993e9751451ccf5";
pub const HASH_US_MESSAGE_SP: &str = "57f0539871fe6fca5d49aa6c397e5412e01aa8d9";
const MAIN_DOL_NAME: &str = "main.dol";
const BRSAR_NAME: &str = "rp_Music_sound.brsar";
const BACKUP_SUFFIX: &str = ".backup";
const ISO_EXT: &str = "iso";
const WBFS_EXT: &str = "wbfs";

#[derive(Clone, Debug)]
pub struct RomFolder {
    pub path: PathBuf,
    pub region: Region,
    pub brsar: Vec<u8>,
    pub main_dol: Vec<u8>,
    pub text_dir: PathBuf,
    source_rom_path: Option<PathBuf>,
}

impl RomFolder {
    pub fn load(path: &Path, paths: &WmPaths) -> Result<Self, WmError> {
        let (folder_path, source_rom_path) = if path.is_file() {
            let output_dir = path.with_extension("");
            extract_rom(paths, path, &output_dir)?;
            (output_dir, Some(path.to_path_buf()))
        } else {
            (path.to_path_buf(), None)
        };

        let main_dol_path = Self::main_dol_path(&folder_path);
        let brsar_path = Self::brsar_path(&folder_path);

        if !main_dol_path.is_file() || !brsar_path.is_file() {
            return Err(WmError::Io(std::io::Error::new(
                std::io::ErrorKind::NotFound,
                "missing required ROM files",
            )));
        }

        let region = detect_region(&folder_path)?;
        if region != Region::US {
            log::warn!("Loading non-US ROM region: {region:?}");
        }

        let brsar = std::fs::read(&brsar_path)?;
        let main_dol = std::fs::read(&main_dol_path)?;

        Ok(Self {
            path: folder_path.clone(),
            region,
            brsar,
            main_dol,
            text_dir: folder_path.join(DATA_DIR).join(FILES_DIR),
            source_rom_path,
        })
    }

    pub fn create_backups(&self) -> Result<(), WmError> {
        let main_dol_path = Self::main_dol_path(&self.path);
        let brsar_path = Self::brsar_path(&self.path);
        let dol_backup_path = self.dol_backup_path();
        let brsar_backup_path = self.brsar_backup_path();

        if !dol_backup_path.exists() {
            std::fs::copy(main_dol_path, dol_backup_path)?;
        }

        if !brsar_backup_path.exists() {
            std::fs::copy(brsar_path, brsar_backup_path)?;
        }

        Ok(())
    }

    pub fn verify(&self, expected_hash: &str) -> Result<bool, WmError> {
        let rom_image_path = self
            .source_rom_path
            .as_deref()
            .or_else(|| Self::rom_image_candidate(&self.path));

        let path = rom_image_path.ok_or_else(|| {
            WmError::Io(std::io::Error::new(
                std::io::ErrorKind::NotFound,
                "rom image path unavailable for checksum verification",
            ))
        })?;

        verify_checksum(path, expected_hash)
    }

    #[must_use]
    pub fn brsar_backup_path(&self) -> PathBuf {
        Self::brsar_path(&self.path).with_file_name(format!("{BRSAR_NAME}{BACKUP_SUFFIX}"))
    }

    #[must_use]
    pub fn dol_backup_path(&self) -> PathBuf {
        Self::main_dol_path(&self.path).with_file_name(format!("{MAIN_DOL_NAME}{BACKUP_SUFFIX}"))
    }

    fn main_dol_path(rom_folder: &Path) -> PathBuf {
        rom_folder.join(DATA_DIR).join(SYS_DIR).join(MAIN_DOL_NAME)
    }

    fn brsar_path(rom_folder: &Path) -> PathBuf {
        rom_folder
            .join(DATA_DIR)
            .join(FILES_DIR)
            .join(SOUND_DIR)
            .join(MUSIC_STATIC_DIR)
            .join(BRSAR_NAME)
    }

    fn rom_image_candidate(path: &Path) -> Option<&Path> {
        if path.is_file() {
            let extension = path.extension()?.to_string_lossy();
            if extension.eq_ignore_ascii_case(ISO_EXT) || extension.eq_ignore_ascii_case(WBFS_EXT) {
                return Some(path);
            }
        }

        None
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;

    #[test]
    fn test_backup_paths() {
        let temp = tempfile::tempdir().expect("tempdir should be created");
        let rom = RomFolder {
            path: temp.path().to_path_buf(),
            region: Region::US,
            brsar: Vec::new(),
            main_dol: Vec::new(),
            text_dir: temp.path().join(DATA_DIR).join(FILES_DIR),
            source_rom_path: None,
        };

        assert_eq!(
            rom.dol_backup_path(),
            temp.path()
                .join(DATA_DIR)
                .join(SYS_DIR)
                .join(format!("{MAIN_DOL_NAME}{BACKUP_SUFFIX}"))
        );
        assert_eq!(
            rom.brsar_backup_path(),
            temp.path()
                .join(DATA_DIR)
                .join(FILES_DIR)
                .join(SOUND_DIR)
                .join(MUSIC_STATIC_DIR)
                .join(format!("{BRSAR_NAME}{BACKUP_SUFFIX}"))
        );
    }

    #[test]
    fn test_create_backups_does_not_overwrite_existing() {
        let temp = tempfile::tempdir().expect("tempdir should be created");
        let main_dol_path = temp.path().join(DATA_DIR).join(SYS_DIR).join(MAIN_DOL_NAME);
        let brsar_path = temp
            .path()
            .join(DATA_DIR)
            .join(FILES_DIR)
            .join(SOUND_DIR)
            .join(MUSIC_STATIC_DIR)
            .join(BRSAR_NAME);

        std::fs::create_dir_all(
            main_dol_path
                .parent()
                .expect("main.dol parent should exist"),
        )
        .expect("create main.dol parent directory");
        std::fs::create_dir_all(brsar_path.parent().expect("brsar parent should exist"))
            .expect("create brsar parent directory");

        std::fs::write(&main_dol_path, b"main").expect("write main.dol");
        std::fs::write(&brsar_path, b"brsar").expect("write brsar");

        let rom = RomFolder {
            path: temp.path().to_path_buf(),
            region: Region::US,
            brsar: Vec::new(),
            main_dol: Vec::new(),
            text_dir: temp.path().join(DATA_DIR).join(FILES_DIR),
            source_rom_path: None,
        };

        rom.create_backups()
            .expect("initial backup creation should succeed");

        let mut existing_dol_backup = std::fs::OpenOptions::new()
            .write(true)
            .truncate(true)
            .open(rom.dol_backup_path())
            .expect("open dol backup for overwrite");
        existing_dol_backup
            .write_all(b"custom")
            .expect("write custom dol backup");

        rom.create_backups()
            .expect("second backup creation should not overwrite");

        let dol_backup = std::fs::read(rom.dol_backup_path()).expect("read dol backup");
        assert_eq!(dol_backup, b"custom");
    }
}
