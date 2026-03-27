use std::path::Path;
use std::process::{Child, Command};

use thiserror::Error;

#[derive(Debug, Error)]
pub enum EditorError {
    #[error("no suitable text editor found")]
    NotFound,
    #[error("failed to spawn editor: {0}")]
    SpawnFailed(String),
    #[error("failed to wait for editor to close: {0}")]
    WaitFailed(String),
}

pub struct EditorHandle {
    child: Child,
}

impl EditorHandle {
    /// Blocks until the editor process exits.
    ///
    /// Must be called off the main thread in an Iced app (e.g. via `Command::perform`).
    ///
    /// # Errors
    /// Returns `EditorError::WaitFailed` if waiting on the process fails.
    pub fn wait_for_close(mut self) -> Result<(), EditorError> {
        self.child
            .wait()
            .map_err(|e| EditorError::WaitFailed(e.to_string()))?;
        Ok(())
    }
}

/// Launches the platform-appropriate text editor for `file_path`.
///
/// | Platform | Command |
/// |----------|---------|
/// | macOS    | `open -e <file>` |
/// | Windows  | `notepad <file>` |
/// | Linux    | `xdg-open <file>` (fallback: `gedit`) |
///
/// # Errors
/// Returns `EditorError::SpawnFailed` if the editor cannot be launched, or
/// `EditorError::NotFound` on Linux when no supported editor is available.
pub fn launch_editor(file_path: &Path) -> Result<EditorHandle, EditorError> {
    let child = spawn_platform_editor(file_path)?;
    Ok(EditorHandle { child })
}

fn spawn_platform_editor(file_path: &Path) -> Result<Child, EditorError> {
    if cfg!(target_os = "macos") {
        Command::new("open")
            .arg("-e")
            .arg(file_path)
            .spawn()
            .map_err(|e| EditorError::SpawnFailed(e.to_string()))
    } else if cfg!(target_os = "windows") {
        Command::new("notepad")
            .arg(file_path)
            .spawn()
            .map_err(|e| EditorError::SpawnFailed(e.to_string()))
    } else {
        match Command::new("xdg-open").arg(file_path).spawn() {
            Ok(child) => Ok(child),
            Err(_) => match Command::new("gedit").arg(file_path).spawn() {
                Ok(child) => Ok(child),
                Err(_) => Err(EditorError::NotFound),
            },
        }
    }
}
