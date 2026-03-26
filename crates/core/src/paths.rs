use std::path::PathBuf;

/// Resolved filesystem paths passed from the editor to `wm_core` at startup.
/// The editor constructs this using compile-time env vars (dev) or
/// exe-relative paths (release). `wm_core` never resolves paths itself.
#[derive(Clone, Debug)]
pub struct WmPaths {
    /// Directory containing platform tool binaries (`wit`, `wszst`, `wbmgt`, `GotaSequenceCmd`).
    /// Layout: `tools/{platform}/{wiimms,sequence_cmd}/`
    pub tools_dir: PathBuf,
    /// Directory containing shared assets (save/, fonts/, icons/).
    pub res_dir: PathBuf,
    /// Directory for config files (settings.ini).
    pub config_dir: PathBuf,
}

impl WmPaths {
    pub fn new(
        tools_dir: impl Into<PathBuf>,
        res_dir: impl Into<PathBuf>,
        config_dir: impl Into<PathBuf>,
    ) -> Self {
        Self {
            tools_dir: tools_dir.into(),
            res_dir: res_dir.into(),
            config_dir: config_dir.into(),
        }
    }

    /// Path to a specific tool binary by name (e.g. `"wszst"`, `"wit"`, `"wbmgt"`, `"GotaSequenceCmd"`).
    /// Searches `wiimms/` then `sequence_cmd/` subdirectories.
    #[must_use]
    pub fn tool(&self, name: &str) -> PathBuf {
        let platform = current_platform();
        let binary = tool_binary(name);

        let wiimms = self.tools_dir.join(platform).join("wiimms").join(&binary);
        if wiimms.exists() {
            return wiimms;
        }

        self.tools_dir
            .join(platform)
            .join("sequence_cmd")
            .join(binary)
    }

    /// Path to a save template file by name (e.g. `"RPMusic.dat"`).
    #[must_use]
    pub fn save_file(&self, name: &str) -> PathBuf {
        self.res_dir.join("save").join(name)
    }

    /// Path to `settings.ini`.
    #[must_use]
    pub fn settings_file(&self) -> PathBuf {
        self.config_dir.join("settings.ini")
    }
}

/// Returns the platform subdirectory name used under tools/.
fn current_platform() -> &'static str {
    if cfg!(target_os = "windows") {
        "windows"
    } else if cfg!(target_os = "macos") {
        "macos"
    } else {
        "linux"
    }
}

/// Appends .exe on Windows.
fn tool_binary(name: &str) -> String {
    if cfg!(target_os = "windows") {
        format!("{name}.exe")
    } else {
        name.to_string()
    }
}

/// Returns the platform-appropriate config directory for Wii Music Editor.
/// - macOS: `~/Library/Application Support/WiiMusicEditor`
/// - Windows: `%APPDATA%/WiiMusicEditor`
/// - Linux: `~/.config/WiiMusicEditor`
#[must_use]
pub fn default_config_dir() -> PathBuf {
    if cfg!(target_os = "macos") {
        let home = std::env::var("HOME").unwrap_or_default();
        PathBuf::from(home).join("Library/Application Support/WiiMusicEditor")
    } else if cfg!(target_os = "windows") {
        let appdata = std::env::var("APPDATA").unwrap_or_default();
        PathBuf::from(appdata).join("WiiMusicEditor")
    } else {
        let home = std::env::var("HOME").unwrap_or_default();
        PathBuf::from(home).join(".config/WiiMusicEditor")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_platform_name() {
        let p = current_platform();
        assert!(["windows", "macos", "linux"].contains(&p));
    }

    #[test]
    fn test_tool_path_structure() {
        let paths = WmPaths::new("/tools", "/res", "/config");
        let wszst = paths.tool("wszst");
        let path = wszst.to_str().unwrap();
        assert!(path.contains("wiimms") || path.contains("sequence_cmd"));
    }

    #[test]
    fn test_config_dir_not_empty() {
        let dir = default_config_dir();
        assert!(!dir.as_os_str().is_empty());
    }
}
