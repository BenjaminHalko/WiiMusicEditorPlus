use crate::{paths::WmPaths, types::WmError};
use std::path::PathBuf;
use std::process::Output;

/// Runs an external tool binary and returns the captured process output.
///
/// # Errors
/// Returns [`WmError::Io`] if the tool cannot be spawned or its permissions
/// cannot be adjusted, and [`WmError::Tool`] if it exits unsuccessfully.
pub fn run_tool(paths: &WmPaths, tool: &str, args: &[&str]) -> Result<Output, WmError> {
    let tool_path = paths.tool(tool);
    set_executable(&tool_path)?;

    let output = std::process::Command::new(&tool_path).args(args).output()?;

    if output.status.success() {
        Ok(output)
    } else {
        let stderr = String::from_utf8_lossy(&output.stderr).into_owned();
        Err(WmError::Tool {
            tool: tool.to_string(),
            stderr,
        })
    }
}

fn set_executable(path: &PathBuf) -> Result<(), WmError> {
    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        let mut perms = std::fs::metadata(path)?.permissions();
        perms.set_mode(perms.mode() | 0o111);
        std::fs::set_permissions(path, perms)?;
    }
    let _ = path;
    Ok(())
}

/// Returns a `WmPaths` pointing at the workspace `tools/{platform}/` directory.
/// Only valid in dev/test builds — uses `CARGO_MANIFEST_DIR` to locate the workspace root.
#[cfg(test)]
fn dev_test_paths() -> WmPaths {
    use crate::paths::dev_platform_tools_subdir;
    let tools = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap() // crates/
        .parent()
        .unwrap() // workspace root
        .join("tools")
        .join(dev_platform_tools_subdir());
    WmPaths::new(tools, "/res", "/config")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_invalid_tool_returns_error() {
        let paths = WmPaths::new("/nonexistent/tools", "/res", "/config");
        assert!(run_tool(&paths, "nonexistent_tool_xyz", &[]).is_err());
    }

    #[test]
    fn test_wszst_runs() {
        let output = run_tool(&dev_test_paths(), "wiimms/wszst", &["--version"]).unwrap();
        assert!(output.status.success());
    }

    #[test]
    fn test_wit_runs() {
        let output = run_tool(&dev_test_paths(), "wiimms/wit", &["--version"]).unwrap();
        assert!(output.status.success());
    }

    #[test]
    fn test_wbmgt_runs() {
        let output = run_tool(&dev_test_paths(), "wiimms/wbmgt", &["--version"]).unwrap();
        assert!(output.status.success());
    }
}
