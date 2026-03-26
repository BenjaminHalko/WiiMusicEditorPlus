use crate::types::WmError;
use sha1::{Digest, Sha1};
use std::path::Path;

/// # Errors
/// Returns `WmError::Io` if the file cannot be read.
pub fn sha1_file(path: &Path) -> Result<String, WmError> {
    let data = std::fs::read(path)?;
    let hash = Sha1::digest(&data);
    Ok(format!("{hash:x}"))
}

/// # Errors
/// Returns `WmError::Io` if the file cannot be read, or `WmError::ChecksumMismatch` if hashes differ.
pub fn verify_checksum(path: &Path, expected: &str) -> Result<bool, WmError> {
    let actual = sha1_file(path)?;
    if actual == expected {
        Ok(true)
    } else {
        Err(WmError::ChecksumMismatch {
            expected: expected.to_string(),
            actual,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;

    #[test]
    fn test_sha1_known_value() {
        let mut f = tempfile::NamedTempFile::new().unwrap();
        f.write_all(b"hello\n").unwrap();
        let hash = sha1_file(f.path()).unwrap();
        assert_eq!(hash, "f572d396fae9206628714fb2ce00f72e94f2258f");
    }

    #[test]
    fn test_verify_checksum_match() {
        let mut f = tempfile::NamedTempFile::new().unwrap();
        f.write_all(b"hello\n").unwrap();
        assert!(verify_checksum(f.path(), "f572d396fae9206628714fb2ce00f72e94f2258f").is_ok());
    }

    #[test]
    fn test_verify_checksum_mismatch() {
        let mut f = tempfile::NamedTempFile::new().unwrap();
        f.write_all(b"hello\n").unwrap();
        let result = verify_checksum(f.path(), "0000000000000000000000000000000000000000");
        assert!(matches!(result, Err(WmError::ChecksumMismatch { .. })));
    }

    #[test]
    fn test_sha1_nonexistent_file() {
        let result = sha1_file(std::path::Path::new("/nonexistent/file.bin"));
        assert!(matches!(result, Err(WmError::Io(_))));
    }
}
