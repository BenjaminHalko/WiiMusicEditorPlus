use std::path::{Path, PathBuf};

use wm_core::{rom_folder::RomFolder, types::Language};

use crate::{discord::DiscordPresence, settings};

const SECTION: &str = "Preferences";
const KEY_ROM_FOLDER: &str = "RomFolder";
const KEY_DOLPHIN_PATH: &str = "DolphinPath";
const KEY_LANGUAGE: &str = "Language";
const KEY_FALLBACK_REGION: &str = "FallbackRegion";
const KEY_DISCORD_RPC: &str = "DiscordRPC";
const KEY_UNSAFE_MODE: &str = "UnsafeMode";
const KEY_NORMALIZE_MIDI: &str = "NormalizeMidi";

pub struct AppState {
    pub rom: Option<RomFolder>,
    pub settings_path: PathBuf,
    pub discord: DiscordPresence,
    pub language: i32,
    pub fallback_region: i32,
}

impl AppState {
    pub fn new() -> Self {
        Self {
            rom: None,
            settings_path: platform_settings_path(),
            discord: DiscordPresence::new(),
            language: 0,
            fallback_region: 0,
        }
    }

    pub fn load_rom_path(&self) -> String {
        settings::load_setting(&self.settings_path, SECTION, KEY_ROM_FOLDER, "")
    }

    pub fn load_dolphin_path(&self) -> String {
        settings::load_setting(&self.settings_path, SECTION, KEY_DOLPHIN_PATH, "")
    }

    pub fn load_language(&self) -> i32 {
        settings::load_setting(&self.settings_path, SECTION, KEY_LANGUAGE, "0")
            .parse()
            .unwrap_or(0)
    }

    pub fn load_fallback_region(&self) -> i32 {
        settings::load_setting(&self.settings_path, SECTION, KEY_FALLBACK_REGION, "0")
            .parse()
            .unwrap_or(0)
    }

    pub fn load_discord_rpc(&self) -> bool {
        settings::load_setting(&self.settings_path, SECTION, KEY_DISCORD_RPC, "false") == "true"
    }

    pub fn load_unsafe_mode(&self) -> bool {
        settings::load_setting(&self.settings_path, SECTION, KEY_UNSAFE_MODE, "false") == "true"
    }

    pub fn load_normalize_midi(&self) -> bool {
        settings::load_setting(&self.settings_path, SECTION, KEY_NORMALIZE_MIDI, "false") == "true"
    }

    pub fn save_settings(
        &self,
        rom_path: &str,
        dolphin_path: &str,
        language: i32,
        fallback_region: i32,
        discord_rpc: bool,
        unsafe_mode: bool,
        normalize_midi: bool,
    ) {
        let _ = settings::save_setting(&self.settings_path, SECTION, KEY_ROM_FOLDER, rom_path);
        let _ =
            settings::save_setting(&self.settings_path, SECTION, KEY_DOLPHIN_PATH, dolphin_path);
        let _ = settings::save_setting(
            &self.settings_path,
            SECTION,
            KEY_LANGUAGE,
            &language.to_string(),
        );
        let _ = settings::save_setting(
            &self.settings_path,
            SECTION,
            KEY_FALLBACK_REGION,
            &fallback_region.to_string(),
        );
        let _ = settings::save_setting(
            &self.settings_path,
            SECTION,
            KEY_DISCORD_RPC,
            if discord_rpc { "true" } else { "false" },
        );
        let _ = settings::save_setting(
            &self.settings_path,
            SECTION,
            KEY_UNSAFE_MODE,
            if unsafe_mode { "true" } else { "false" },
        );
        let _ = settings::save_setting(
            &self.settings_path,
            SECTION,
            KEY_NORMALIZE_MIDI,
            if normalize_midi { "true" } else { "false" },
        );
    }

    /// Attempts to load a ROM from `path`. On success the ROM is stored in
    /// `self.rom` and the folder path is returned. On failure the ROM is left
    /// as `None` and `None` is returned.
    pub fn try_load_rom(&mut self, path: &str) -> Option<String> {
        if path.is_empty() {
            return None;
        }
        let p = Path::new(path);
        if !p.exists() {
            return None;
        }
        match RomFolder::load(p, Language::from_index(self.language), |_| {}) {
            Ok(rom) => {
                let label = rom.path.display().to_string();
                self.rom = Some(rom);
                Some(label)
            }
            Err(e) => {
                log::warn!("failed to load ROM at {path}: {e}");
                None
            }
        }
    }
}

fn platform_settings_path() -> PathBuf {
    let dir = if cfg!(target_os = "macos") {
        std::env::var("HOME")
            .ok()
            .map(|h| PathBuf::from(h).join("Library/Application Support/WiiMusicEditor"))
    } else if cfg!(target_os = "windows") {
        std::env::var("APPDATA")
            .ok()
            .map(|a| PathBuf::from(a).join("WiiMusicEditor"))
    } else {
        std::env::var("HOME")
            .ok()
            .map(|h| PathBuf::from(h).join(".config/WiiMusicEditor"))
    };
    dir.unwrap_or_else(|| PathBuf::from("."))
        .join("settings.ini")
}
