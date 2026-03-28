slint::include_modules!();

use std::{
    path::PathBuf,
    sync::{Arc, Mutex},
};

mod app_state;
#[allow(dead_code)]
mod discord;
#[allow(dead_code)]
mod external_editor;
mod settings;
#[allow(dead_code)]
mod updater;

use app_state::AppState;
use wm_core::{rom_folder::RomFolder, types::Language};

fn load_rom_async(
    app_weak: slint::Weak<AppWindow>,
    state: Arc<Mutex<AppState>>,
    new_rom_path: &str,
) {
    let Some(app) = app_weak.upgrade() else {
        return;
    };

    let previous_path = app.get_cfg_rom_path().to_string();
    let (language, dolphin_path, fallback_region, discord_rpc, unsafe_mode, normalize_midi) = {
        let s = state.lock().expect("state");
        (
            s.language,
            s.load_dolphin_path(),
            s.fallback_region,
            s.load_discord_rpc(),
            s.load_unsafe_mode(),
            s.load_normalize_midi(),
        )
    };

    app.set_cfg_rom_path(new_rom_path.into());
    app.set_loading_visible(true);
    app.set_loading_progress(-1.0);
    app.set_loading_message("Loading ROM...".into());

    let path = PathBuf::from(new_rom_path);
    let lang = Language::from_index(language);

    std::thread::spawn(move || {
        let last_pct = std::cell::Cell::new(0u32);
        let weak_prog = app_weak.clone();

        let result = RomFolder::load(&path, lang, move |progress| {
            let new_pct = (progress * 200.0) as u32;
            if new_pct == last_pct.get() {
                return;
            }
            last_pct.set(new_pct);
            let weak_prog = weak_prog.clone();
            slint::invoke_from_event_loop(move || {
                if let Some(a) = weak_prog.upgrade() {
                    a.set_loading_progress(progress);
                }
            })
            .ok();
        });

        app_weak
            .upgrade_in_event_loop(move |app| {
                app.set_loading_visible(false);
                match result {
                    Ok(rom) => {
                        let folder_path = rom.path.display().to_string();
                        let mut s = state.lock().expect("state");
                        s.rom = Some(rom);
                        s.save_settings(
                            &folder_path,
                            &dolphin_path,
                            language,
                            fallback_region,
                            discord_rpc,
                            unsafe_mode,
                            normalize_midi,
                        );
                        drop(s);
                        app.set_cfg_rom_path(folder_path.clone().into());
                        app.set_rom_label(folder_path.into());
                    }
                    Err(e) => {
                        app.set_cfg_rom_path(previous_path.into());
                        app.set_dialog_title("Error".into());
                        app.set_dialog_message(e.to_string().into());
                        app.set_dialog_type(DialogType::Error);
                        app.set_dialog_visible(true);
                    }
                }
            })
            .ok();
    });
}

#[allow(clippy::too_many_lines)]
fn main() -> Result<(), slint::PlatformError> {
    slint::init_translations!(concat!(env!("CARGO_MANIFEST_DIR"), "/i18n/"));
    let app = AppWindow::new()?;
    let state = Arc::new(Mutex::new(AppState::new()));

    let startup_label = {
        let mut s = state.lock().expect("state");
        let rom_path = s.load_rom_path();
        let dolphin_path = s.load_dolphin_path();
        let language = s.load_language();
        let fallback_region = s.load_fallback_region();

        s.language = language;
        s.fallback_region = fallback_region;

        app.set_cfg_rom_path(rom_path.clone().into());
        app.set_cfg_dolphin_path(dolphin_path.into());
        app.set_cfg_language(language);
        app.set_cfg_fallback_region(fallback_region);
        app.set_cfg_discord_rpc(s.load_discord_rpc());
        app.set_cfg_unsafe_mode(s.load_unsafe_mode());
        app.set_cfg_normalize_midi(s.load_normalize_midi());

        s.try_load_rom(&rom_path)
            .unwrap_or_else(|| "No ROM loaded".to_string())
    };
    app.set_rom_label(startup_label.into());

    if state.lock().expect("state").rom.is_none() {
        app.set_current_screen(Screen::FirstSetup);
    }

    app.on_fs_browse_rom({
        let app_weak = app.as_weak();
        move || {
            if let Some(path) = rfd::FileDialog::new()
                .add_filter("ROM", &["iso", "wbfs"])
                .pick_file()
                && let Some(a) = app_weak.upgrade()
            {
                a.set_fs_rom_path(path.display().to_string().into());
                a.set_fs_continue_enabled(true);
            }
        }
    });

    app.on_fs_browse_rom_folder({
        let app_weak = app.as_weak();
        move || {
            if let Some(path) = rfd::FileDialog::new().pick_folder()
                && let Some(a) = app_weak.upgrade()
            {
                a.set_fs_rom_path(path.display().to_string().into());
                a.set_fs_continue_enabled(true);
            }
        }
    });

    app.on_fs_continue({
        let state = Arc::clone(&state);
        let app_weak = app.as_weak();
        move || {
            let Some(a) = app_weak.upgrade() else { return };
            let rom_path = a.get_fs_rom_path().to_string();
            let settings_path = state.lock().expect("state").settings_path.clone();
            let _ = settings::save_setting(&settings_path, "Preferences", "RomFolder", &rom_path);
            load_rom_async(app_weak.clone(), Arc::clone(&state), &rom_path);
            a.set_current_screen(Screen::MainMenu);
        }
    });

    app.on_cfg_browse_rom({
        let state = Arc::clone(&state);
        let app_weak = app.as_weak();
        move || {
            if let Some(path) = rfd::FileDialog::new()
                .add_filter("ROM", &["iso", "wbfs"])
                .pick_file()
            {
                load_rom_async(
                    app_weak.clone(),
                    Arc::clone(&state),
                    &path.display().to_string(),
                );
            }
        }
    });

    app.on_cfg_browse_rom_folder({
        let state = Arc::clone(&state);
        let app_weak = app.as_weak();
        move || {
            if let Some(path) = rfd::FileDialog::new().pick_folder() {
                load_rom_async(
                    app_weak.clone(),
                    Arc::clone(&state),
                    &path.display().to_string(),
                );
            }
        }
    });

    app.on_cfg_browse_dolphin({
        let state = Arc::clone(&state);
        let app_weak = app.as_weak();
        move || {
            if let Some(path) = rfd::FileDialog::new().pick_file() {
                let path_str = path.display().to_string();
                let settings_path = state.lock().expect("state").settings_path.clone();
                let _ =
                    settings::save_setting(&settings_path, "Preferences", "DolphinPath", &path_str);
                if let Some(a) = app_weak.upgrade() {
                    a.set_cfg_dolphin_path(path_str.into());
                }
            }
        }
    });

    app.on_cfg_language_changed({
        let state = Arc::clone(&state);
        move |v| {
            let mut s = state.lock().expect("state");
            s.language = v;
            let _ = settings::save_setting(
                &s.settings_path.clone(),
                "Preferences",
                "Language",
                &v.to_string(),
            );
        }
    });

    app.on_cfg_region_changed({
        let state = Arc::clone(&state);
        move |v| {
            let mut s = state.lock().expect("state");
            s.fallback_region = v;
            let _ = settings::save_setting(
                &s.settings_path.clone(),
                "Preferences",
                "FallbackRegion",
                &v.to_string(),
            );
        }
    });

    app.on_cfg_discord_rpc_changed({
        let state = Arc::clone(&state);
        move |v| {
            let s = state.lock().expect("state");
            let _ = settings::save_setting(
                &s.settings_path,
                "Preferences",
                "DiscordRPC",
                if v { "true" } else { "false" },
            );
        }
    });

    app.on_cfg_unsafe_mode_changed({
        let state = Arc::clone(&state);
        move |v| {
            let s = state.lock().expect("state");
            let _ = settings::save_setting(
                &s.settings_path,
                "Preferences",
                "UnsafeMode",
                if v { "true" } else { "false" },
            );
        }
    });

    app.on_cfg_normalize_midi_changed({
        let state = Arc::clone(&state);
        move |v| {
            let s = state.lock().expect("state");
            let _ = settings::save_setting(
                &s.settings_path,
                "Preferences",
                "NormalizeMidi",
                if v { "true" } else { "false" },
            );
        }
    });

    app.on_dialog_confirmed(|| {});
    app.on_dialog_dismissed(|| {});

    app.run()
}
