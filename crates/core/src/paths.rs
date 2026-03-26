use std::path::PathBuf;

/// Resolved filesystem paths passed into `wm_core` at startup.
/// `tools_dir` must already point to the platform-specific tool folder —
/// in dev this means `workspace/tools/{platform}/`, in release the packager
/// has already placed only the current platform's tools in `tools/`.
/// `wm_core` never detects the current platform itself.
#[derive(Clone, Debug)]
pub struct WmPaths {
    /// Platform-specific tool directory containing `wiimms/` and `sequence_cmd/`
    /// subdirectories. Caller is responsible for platform resolution.
    pub tools_dir: PathBuf,
    /// Directory containing shared assets (`save/`, `fonts/`, `icons/`).
    pub res_dir: PathBuf,
    /// Directory for config files (`settings.ini`).
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

    /// Path to a tool binary. `name` must include the subfolder prefix,
    /// e.g. `"wiimms/wszst"` or `"sequence_cmd/GotaSequenceCmd"`.
    /// `.exe` is appended automatically on Windows.
    #[must_use]
    pub fn tool(&self, name: &str) -> PathBuf {
        self.tools_dir.join(tool_binary(name))
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

/// In dev builds, returns the platform-specific subdirectory under `workspace/tools/`.
/// Use this when constructing `WmPaths` in dev mode — the caller passes the result as `tools_dir`.
///
/// In release builds the packager already placed only the current platform's tools
/// in `tools/`, so no subdirectory is needed.
#[must_use]
pub fn dev_platform_tools_subdir() -> &'static str {
    if cfg!(target_os = "windows") {
        "windows"
    } else if cfg!(target_os = "macos") {
        "macos"
    } else {
        "linux"
    }
}

/// Appends `.exe` on Windows, returns name unchanged on other platforms.
#[must_use]
pub fn tool_binary(name: &str) -> String {
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
    fn test_platform_subdir_valid() {
        let p = dev_platform_tools_subdir();
        assert!(["windows", "macos", "linux"].contains(&p));
    }

    #[test]
    fn test_tool_path_is_simple_join() {
        let paths = WmPaths::new("/tools", "/res", "/config");
        let wszst = paths.tool("wiimms/wszst");
        let s = wszst.to_str().unwrap();
        assert!(s.contains("wiimms"));
        assert!(s.contains("wszst"));
    }

    #[test]
    fn test_config_dir_not_empty() {
        assert!(!default_config_dir().as_os_str().is_empty());
    }
}
