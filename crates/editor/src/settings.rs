// Settings persistence — INI-based, backward compatible with v1/v2 Python settings.ini
// Python used `configparser.ConfigParser` which writes standard INI; the `ini` crate wraps the same parser.

use std::collections::HashMap;
use std::path::Path;

use ini::configparser::ini::Ini;

/// All settings from an INI file, keyed by section then key.
/// Values are `None` for valueless keys (e.g. `key_without_equals`).
pub type IniMap = HashMap<String, HashMap<String, Option<String>>>;

/// Loads a setting from an INI file. Returns `default` if the file
/// doesn't exist, can't be parsed, or the key is missing.
#[must_use]
pub fn load_setting(path: &Path, section: &str, key: &str, default: &str) -> String {
    let mut config = Ini::new();
    if config.load(path.to_string_lossy().as_ref()).is_err() {
        return default.to_string();
    }
    config
        .get(section, key)
        .unwrap_or_else(|| default.to_string())
}

/// Saves a setting to an INI file, creating the file if it doesn't exist.
///
/// # Errors
/// Returns an error if the file cannot be written.
pub fn save_setting(path: &Path, section: &str, key: &str, value: &str) -> Result<(), String> {
    let mut config = Ini::new();
    let _ = config.load(path.to_string_lossy().as_ref());
    config.set(section, key, Some(value.to_string()));

    if let Some(parent) = path.parent() {
        std::fs::create_dir_all(parent).map_err(|e| e.to_string())?;
    }

    config
        .write(path.to_string_lossy().as_ref())
        .map_err(|e| e.to_string())
}

/// Loads all settings from an INI file as a nested structure.
/// Returns empty map if file doesn't exist or can't be parsed.
#[must_use]
pub fn load_all(path: &Path) -> IniMap {
    let mut config = Ini::new();
    config
        .load(path.to_string_lossy().as_ref())
        .unwrap_or_default()
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    fn temp_settings(dir: &TempDir) -> std::path::PathBuf {
        dir.path().join("settings.ini")
    }

    #[test]
    fn test_roundtrip() {
        let dir = TempDir::new().unwrap();
        let path = temp_settings(&dir);
        save_setting(&path, "TestSection", "key", "hello").unwrap();
        let val = load_setting(&path, "TestSection", "key", "default");
        assert_eq!(val, "hello");
    }

    #[test]
    fn test_missing_file_returns_default() {
        let dir = TempDir::new().unwrap();
        let path = temp_settings(&dir);
        let val = load_setting(&path, "Missing", "key", "fallback");
        assert_eq!(val, "fallback");
    }

    #[test]
    fn test_missing_key_returns_default() {
        let dir = TempDir::new().unwrap();
        let path = temp_settings(&dir);
        save_setting(&path, "Section", "other", "x").unwrap();
        let val = load_setting(&path, "Section", "missing_key", "fallback");
        assert_eq!(val, "fallback");
    }

    #[test]
    fn test_corrupted_file_returns_default() {
        let dir = TempDir::new().unwrap();
        let path = temp_settings(&dir);
        std::fs::write(&path, b"NOT\x00VALID\xFFINI\x01CONTENT").unwrap();
        let val = load_setting(&path, "Section", "key", "fallback");
        assert_eq!(val, "fallback");
    }

    #[test]
    fn test_creates_parent_dirs() {
        let dir = TempDir::new().unwrap();
        let path = dir.path().join("nested/deep/settings.ini");
        save_setting(&path, "S", "k", "v").unwrap();
        assert!(path.exists());
    }
}
