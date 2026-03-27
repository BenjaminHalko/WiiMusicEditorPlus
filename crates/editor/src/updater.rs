use self_update::backends::github::Update;
use thiserror::Error;

const REPO_OWNER: &str = "BenjaminHalko";
const REPO_NAME: &str = "WiiMusicEditorPlus";
const BIN_NAME: &str = "wii-music-editor";

#[derive(Debug, Clone)]
pub struct UpdateInfo {
    pub version: String,
    pub download_url: String,
    pub body: String,
}

#[derive(Debug, Error)]
pub enum UpdateError {
    #[error("network error: {0}")]
    Network(String),
    #[error("parse error: {0}")]
    Parse(String),
    #[error("apply error: {0}")]
    Apply(String),
}

/// Returns `Ok(None)` if already up-to-date. Blocking I/O — call from `Command::perform`.
pub fn check_for_update(current_version: &str) -> Result<Option<UpdateInfo>, UpdateError> {
    let updater = Update::configure()
        .repo_owner(REPO_OWNER)
        .repo_name(REPO_NAME)
        .bin_name(BIN_NAME)
        .current_version(current_version)
        .build()
        .map_err(|e| UpdateError::Network(e.to_string()))?;

    let latest = updater
        .get_latest_release()
        .map_err(|e| UpdateError::Network(e.to_string()))?;

    let current_clean = current_version.trim_start_matches('v');
    let latest_clean = latest.version.trim_start_matches('v');

    let is_newer = self_update::version::bump_is_greater(current_clean, latest_clean)
        .map_err(|e| UpdateError::Parse(e.to_string()))?;

    if !is_newer {
        return Ok(None);
    }

    let target = self_update::get_target();
    let download_url = latest
        .assets
        .iter()
        .find(|a| a.name.contains(target))
        .or_else(|| latest.assets.first())
        .map(|a| a.download_url.clone())
        .ok_or_else(|| UpdateError::Parse("no release assets found for current platform".into()))?;

    Ok(Some(UpdateInfo {
        version: latest.version,
        download_url,
        body: latest.body.unwrap_or_default(),
    }))
}

/// Blocking I/O — call from `Command::perform`.
pub fn download_and_apply(update: &UpdateInfo) -> Result<(), UpdateError> {
    let tag = if update.version.starts_with('v') {
        update.version.clone()
    } else {
        format!("v{}", update.version)
    };

    Update::configure()
        .repo_owner(REPO_OWNER)
        .repo_name(REPO_NAME)
        .bin_name(BIN_NAME)
        .target_version_tag(&tag)
        .current_version("0.0.0")
        .no_confirm(true)
        .show_download_progress(false)
        .build()
        .map_err(|e| UpdateError::Apply(e.to_string()))?
        .update()
        .map_err(|e| UpdateError::Apply(e.to_string()))?;

    Ok(())
}
