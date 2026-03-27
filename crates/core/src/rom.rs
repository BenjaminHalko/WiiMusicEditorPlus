use crate::{
    paths::WmPaths,
    shell::run_tool,
    types::{Region, WmError},
};
use std::path::Path;

const BOOT_BIN_REL_PATH: &str = "DATA/sys/boot.bin";
const GAME_ID_LENGTH: usize = 0x06;
const REGION_PREFIX_LENGTH: usize = 0x04;

/// # Errors
/// Returns `WmError::Tool` if wit fails, `WmError::Io` on filesystem errors.
pub fn extract_rom(paths: &WmPaths, iso_path: &Path, output_dir: &Path) -> Result<(), WmError> {
    let iso = iso_path.to_string_lossy().into_owned();
    let output = output_dir.to_string_lossy().into_owned();
    run_tool(paths, "wiimms/wit", &["cp", "--fst", &iso, &output])?;
    Ok(())
}

/// Detect game region from the extracted ROM folder's disc header.
/// Reads the game ID from DATA/sys/boot.bin (first 6 bytes).
///
/// # Errors
/// Returns `WmError::Io` if boot.bin can't be read, `WmError::UnsupportedRegion` for unknown IDs.
pub fn detect_region(rom_folder: &Path) -> Result<Region, WmError> {
    let boot_bin_path = rom_folder.join(BOOT_BIN_REL_PATH);
    let boot_bin = std::fs::read(boot_bin_path)?;
    detect_region_from_bytes(&boot_bin)
}

fn detect_region_from_bytes(boot_bin: &[u8]) -> Result<Region, WmError> {
    if boot_bin.len() < GAME_ID_LENGTH {
        return Err(WmError::UnsupportedRegion(
            "boot.bin shorter than game ID header".to_string(),
        ));
    }

    let game_id = &boot_bin[..GAME_ID_LENGTH];
    let region = match &game_id[..REGION_PREFIX_LENGTH] {
        b"R64E" => Region::US,
        b"R64P" => Region::EU,
        b"R64J" => Region::JP,
        b"R64K" => Region::KR,
        _ => {
            return Err(WmError::UnsupportedRegion(
                String::from_utf8_lossy(game_id).into_owned(),
            ));
        }
    };

    Ok(region)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_detect_region_from_bytes() {
        assert!(matches!(
            detect_region_from_bytes(b"R64E01"),
            Ok(Region::US)
        ));
        assert!(matches!(
            detect_region_from_bytes(b"R64P01"),
            Ok(Region::EU)
        ));
        assert!(matches!(
            detect_region_from_bytes(b"R64J01"),
            Ok(Region::JP)
        ));
        assert!(matches!(
            detect_region_from_bytes(b"R64K01"),
            Ok(Region::KR)
        ));
    }

    #[test]
    fn test_detect_region_from_bytes_unknown() {
        let err = detect_region_from_bytes(b"R64X01");
        assert!(matches!(err, Err(WmError::UnsupportedRegion(_))));
    }
}
