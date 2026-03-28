use std::fs;
use std::path::Path;

use crate::{
    data::{SONG_LIST, STYLE_LIST},
    dol::{
        MainDol, SONG_SEGMENT_DEFAULT_STYLE, SONG_SEGMENT_LENGTH, SONG_SEGMENT_TEMPO,
        SONG_SEGMENT_TIME_SIGNATURE,
    },
    rom_folder::RomFolder,
    types::{SongType, WmError},
};

/// Restores all songs to their backup state.
///
/// # Errors
///
/// Returns [`WmError`] when a backup file is missing or any I/O operation fails.
pub fn revert_all_songs(rom_folder: &mut RomFolder) -> Result<(), WmError> {
    let brsar_backup = rom_folder.brsar_backup_path();
    let brsar_active = RomFolder::brsar_path(&rom_folder.base);
    ensure_backup_exists(&brsar_backup, "BRSAR")?;
    fs::copy(&brsar_backup, &brsar_active)?;
    rom_folder.brsar = fs::read(&brsar_active)?;

    let backup_dol = load_backup_dol(rom_folder)?;
    let mut active_dol = MainDol::parse(rom_folder.main_dol.clone());

    for song in SONG_LIST {
        let length = backup_dol.read_song_info(song, SONG_SEGMENT_LENGTH as u8);
        let tempo = backup_dol.read_song_info(song, SONG_SEGMENT_TEMPO as u8);
        let time_sig = backup_dol.read_song_info(song, SONG_SEGMENT_TIME_SIGNATURE as u8);
        active_dol.write_song_info(song, SONG_SEGMENT_LENGTH as u8, length);
        active_dol.write_song_info(song, SONG_SEGMENT_TEMPO as u8, tempo);
        active_dol.write_song_info(song, SONG_SEGMENT_TIME_SIGNATURE as u8, time_sig);
    }

    rom_folder.main_dol = active_dol.as_bytes().to_vec();
    fs::write(
        RomFolder::main_dol_path(&rom_folder.base),
        &rom_folder.main_dol,
    )?;
    Ok(())
}

/// Restores all style instruments to their backup state.
///
/// # Errors
///
/// Returns [`WmError`] when a backup file is missing or any I/O operation fails.
pub fn revert_all_styles(rom_folder: &mut RomFolder) -> Result<(), WmError> {
    let backup_dol = load_backup_dol(rom_folder)?;
    let mut active_dol = MainDol::parse(rom_folder.main_dol.clone());

    for (index, _style) in STYLE_LIST.iter().enumerate() {
        let instruments = backup_dol.read_style_instruments(index);
        active_dol.write_style_instruments(index, &instruments);
    }

    rom_folder.main_dol = active_dol.as_bytes().to_vec();
    fs::write(
        RomFolder::main_dol_path(&rom_folder.base),
        &rom_folder.main_dol,
    )?;
    Ok(())
}

/// Restores all default-style assignments to their backup state.
///
/// # Errors
///
/// Returns [`WmError`] when a backup file is missing or any I/O operation fails.
pub fn revert_all_default_styles(rom_folder: &mut RomFolder) -> Result<(), WmError> {
    let backup_dol = load_backup_dol(rom_folder)?;
    let mut active_dol = MainDol::parse(rom_folder.main_dol.clone());

    for song in SONG_LIST {
        if song.song_type != SongType::Menu {
            let style_id = backup_dol.read_song_info(song, SONG_SEGMENT_DEFAULT_STYLE as u8);
            active_dol.write_song_info(song, SONG_SEGMENT_DEFAULT_STYLE as u8, style_id);
        }
    }

    rom_folder.main_dol = active_dol.as_bytes().to_vec();
    fs::write(
        RomFolder::main_dol_path(&rom_folder.base),
        &rom_folder.main_dol,
    )?;
    Ok(())
}

/// Restores text data to its backup state by copying `message.carc.backup`.
///
/// # Errors
///
/// Returns [`WmError`] when the backup file is missing or I/O operations fail.
pub fn revert_all_text(rom_folder: &mut RomFolder) -> Result<(), WmError> {
    let message_dir = locate_message_dir(&rom_folder.text_dir)?;
    let message_carc = message_dir.join("message.carc");
    let message_carc_backup = message_dir.join("message.carc.backup");
    ensure_backup_exists(&message_carc_backup, "message.carc")?;
    fs::copy(&message_carc_backup, &message_carc)?;
    Ok(())
}

/// Restores everything (DOL, BRSAR, text) to backup state and reloads
/// in-memory state in [`RomFolder`].
///
/// # Errors
///
/// Returns [`WmError`] when any backup file is missing or I/O operations fail.
pub fn revert_all(rom_folder: &mut RomFolder) -> Result<(), WmError> {
    let dol_backup = rom_folder.dol_backup_path();
    let dol_active = RomFolder::main_dol_path(&rom_folder.base);
    ensure_backup_exists(&dol_backup, "main.dol")?;
    fs::copy(&dol_backup, &dol_active)?;

    let brsar_backup = rom_folder.brsar_backup_path();
    let brsar_active = RomFolder::brsar_path(&rom_folder.base);
    ensure_backup_exists(&brsar_backup, "BRSAR")?;
    fs::copy(&brsar_backup, &brsar_active)?;

    let message_dir = locate_message_dir(&rom_folder.text_dir)?;
    let message_carc = message_dir.join("message.carc");
    let message_carc_backup = message_dir.join("message.carc.backup");
    ensure_backup_exists(&message_carc_backup, "message.carc")?;
    fs::copy(&message_carc_backup, &message_carc)?;

    rom_folder.brsar = fs::read(&brsar_active)?;
    rom_folder.main_dol = fs::read(&dol_active)?;
    Ok(())
}

fn load_backup_dol(rom_folder: &RomFolder) -> Result<MainDol, WmError> {
    let backup_path = rom_folder.dol_backup_path();
    ensure_backup_exists(&backup_path, "main.dol")?;
    let data = fs::read(backup_path)?;
    Ok(MainDol::parse(data))
}

fn ensure_backup_exists(path: &Path, label: &str) -> Result<(), WmError> {
    if !path.is_file() {
        return Err(WmError::Io(std::io::Error::new(
            std::io::ErrorKind::NotFound,
            format!("{label} backup not found at {}", path.display()),
        )));
    }
    Ok(())
}

fn locate_message_dir(text_dir: &Path) -> Result<std::path::PathBuf, WmError> {
    let message_dir = text_dir.join("Message");
    if message_dir.is_dir() {
        return Ok(message_dir);
    }
    Err(WmError::Io(std::io::Error::new(
        std::io::ErrorKind::NotFound,
        format!("Message directory not found under {}", text_dir.display()),
    )))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::types::Region;

    const TEST_DOL_SIZE: usize = 0x005A_0AEC + 0x2000;

    fn setup_test_rom() -> (tempfile::TempDir, RomFolder) {
        let temp = tempfile::tempdir().expect("create tempdir");
        let root = temp.path();

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

        let dol_data = vec![0x00_u8; TEST_DOL_SIZE];
        fs::write(sys_dir.join("main.dol"), &dol_data).expect("write main.dol");
        fs::write(sys_dir.join("main.dol.backup"), &dol_data).expect("write dol backup");

        let brsar_data = vec![0xAA_u8; 0x100];
        fs::write(sound_dir.join("rp_Music_sound.brsar"), &brsar_data).expect("write brsar");
        fs::write(sound_dir.join("rp_Music_sound.brsar.backup"), &brsar_data)
            .expect("write brsar backup");

        fs::write(message_dir.join("message.carc"), b"active").expect("write message.carc");
        fs::write(message_dir.join("message.carc.backup"), b"backup")
            .expect("write message.carc backup");

        let rom = RomFolder {
            path: root.to_path_buf(),
            base: root.join("DATA"),
            region: Region::US,
            brsar: brsar_data,
            main_dol: dol_data,
            text_dir: root.join("DATA").join("files").join("US"),
            source_rom_path: None,
        };

        (temp, rom)
    }

    #[test]
    fn revert_all_songs_restores_from_backup() {
        let (_temp, mut rom) = setup_test_rom();
        let song = &SONG_LIST[0];

        let mut dol = MainDol::parse(rom.main_dol.clone());
        dol.write_song_info(song, SONG_SEGMENT_LENGTH as u8, 0xDEAD_BEEF);
        dol.write_song_info(song, SONG_SEGMENT_TEMPO as u8, 0xCAFE_BABE);
        dol.write_song_info(song, SONG_SEGMENT_TIME_SIGNATURE as u8, 0x0000_0007);
        rom.main_dol = dol.as_bytes().to_vec();
        fs::write(RomFolder::main_dol_path(&rom.base), &rom.main_dol).expect("write modified dol");

        let check = MainDol::parse(rom.main_dol.clone());
        assert_eq!(
            check.read_song_info(song, SONG_SEGMENT_LENGTH as u8),
            0xDEAD_BEEF
        );

        revert_all_songs(&mut rom).expect("revert should succeed");

        let restored = MainDol::parse(rom.main_dol.clone());
        assert_eq!(
            restored.read_song_info(song, SONG_SEGMENT_LENGTH as u8),
            0x0000_0000
        );
        assert_eq!(
            restored.read_song_info(song, SONG_SEGMENT_TEMPO as u8),
            0x0000_0000
        );
        assert_eq!(
            restored.read_song_info(song, SONG_SEGMENT_TIME_SIGNATURE as u8),
            0x0000_0000
        );
    }

    #[test]
    fn revert_all_styles_restores_from_backup() {
        let (_temp, mut rom) = setup_test_rom();

        let mut dol = MainDol::parse(rom.main_dol.clone());
        let modified = crate::types::StyleInstruments([0x01, 0x02, 0x03, 0x04, 0x05, 0x06]);
        dol.write_style_instruments(0, &modified);
        rom.main_dol = dol.as_bytes().to_vec();
        fs::write(RomFolder::main_dol_path(&rom.base), &rom.main_dol).expect("write modified dol");

        revert_all_styles(&mut rom).expect("revert should succeed");

        let restored = MainDol::parse(rom.main_dol.clone());
        let instruments = restored.read_style_instruments(0);
        assert_eq!(
            instruments,
            crate::types::StyleInstruments([0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        );
    }

    #[test]
    fn revert_all_default_styles_restores_from_backup() {
        let (_temp, mut rom) = setup_test_rom();
        let song = SONG_LIST
            .iter()
            .find(|s| s.song_type != SongType::Menu)
            .expect("song with default style");

        let mut dol = MainDol::parse(rom.main_dol.clone());
        dol.write_song_info(song, SONG_SEGMENT_DEFAULT_STYLE as u8, 0x0000_00FF);
        rom.main_dol = dol.as_bytes().to_vec();
        fs::write(RomFolder::main_dol_path(&rom.base), &rom.main_dol).expect("write modified dol");

        revert_all_default_styles(&mut rom).expect("revert should succeed");

        let restored = MainDol::parse(rom.main_dol.clone());
        assert_eq!(
            restored.read_song_info(song, SONG_SEGMENT_DEFAULT_STYLE as u8),
            0x0000_0000
        );
    }

    #[test]
    fn revert_all_text_restores_message_carc() {
        let (_temp, mut rom) = setup_test_rom();
        let message_dir = locate_message_dir(&rom.text_dir).expect("message dir");

        fs::write(message_dir.join("message.carc"), b"modified").expect("modify message.carc");

        revert_all_text(&mut rom).expect("revert_all_text should succeed");

        let content = fs::read(message_dir.join("message.carc")).expect("read restored");
        assert_eq!(content, b"backup");
    }

    #[test]
    fn revert_all_restores_all_files() {
        let (_temp, mut rom) = setup_test_rom();

        rom.brsar = vec![0xFF_u8; 0x200];
        fs::write(RomFolder::brsar_path(&rom.base), &rom.brsar).expect("write modified brsar");
        rom.main_dol[0] = 0xFF;
        fs::write(RomFolder::main_dol_path(&rom.base), &rom.main_dol).expect("write modified dol");

        revert_all(&mut rom).expect("revert_all should succeed");

        assert_eq!(rom.brsar.len(), 0x100);
        assert_eq!(rom.brsar[0], 0xAA);
        assert_eq!(rom.main_dol[0], 0x00);
        let message_dir = locate_message_dir(&rom.text_dir).expect("message dir");
        let message = fs::read(message_dir.join("message.carc")).expect("read message.carc");
        assert_eq!(message, b"backup");
    }

    #[test]
    fn missing_backup_returns_error() {
        let temp = tempfile::tempdir().expect("create tempdir");
        let root = temp.path();
        let sys_dir = root.join("DATA").join("sys");
        let sound_dir = root
            .join("DATA")
            .join("files")
            .join("Sound")
            .join("MusicStatic");
        fs::create_dir_all(&sys_dir).expect("create sys dir");
        fs::create_dir_all(&sound_dir).expect("create sound dir");

        fs::write(sys_dir.join("main.dol"), vec![0x00_u8; TEST_DOL_SIZE]).expect("write main.dol");
        fs::write(sound_dir.join("rp_Music_sound.brsar"), vec![0x00_u8; 0x10])
            .expect("write brsar");

        let mut rom = RomFolder {
            path: root.to_path_buf(),
            base: root.join("DATA"),
            region: Region::US,
            brsar: vec![0x00_u8; 0x10],
            main_dol: vec![0x00_u8; TEST_DOL_SIZE],
            text_dir: root.join("DATA").join("files").join("US"),
            source_rom_path: None,
        };

        assert!(revert_all_songs(&mut rom).is_err());
    }
}
