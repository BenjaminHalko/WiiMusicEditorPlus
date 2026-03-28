use std::fs;
use std::path::{Path, PathBuf};

use crate::types::WmError;

const MESSAGE_ARCHIVE_NAME: &str = "message.carc";

/// Finds the first `message.carc` under a `files/` directory (any region).
///
/// # Errors
/// Returns `WmError::Parse` if no `message.carc` is found.
pub(crate) fn find_message_carc(text_dir: &Path) -> Result<PathBuf, WmError> {
    let candidate = text_dir.join("Message").join(MESSAGE_ARCHIVE_NAME);
    if candidate.is_file() {
        return Ok(candidate);
    }
    Err(WmError::Parse {
        file: text_dir.display().to_string(),
        offset: 0,
        message: "message.carc not found".to_string(),
    })
}
const MESSAGE_FOLDER_NAME: &str = "message.d";
const MESSAGE_TEXT_NAME: &str = "new_music_message.txt";
const CUSTOM_QUICKJAM_NEEDLE: &str = "  b200 @015f /\r\n";
const CUSTOM_QUICKJAM_PATCHES: [&str; 12] = [
    "  b200 @015f [/,4b] = Default\r\n",
    "  b201 @0160 [/,4b] = Rock\r\n",
    "  b202 @0161 [/,4b] = March\r\n",
    "  b203 @0162 [/,4b] = Jazz\r\n",
    "  b204 @0163 [/,4b] = Latin\r\n",
    "  b205 @0164 [/,4b] = Reggae\r\n",
    "  b206 @0165 [/,4b] = Hawaiian\r\n",
    "  b207 @0166 [/,4b] = Electronic\r\n",
    "  b208 @0167 [/,4b] = Classical\r\n",
    "  b209 @0168 [/,4b] = Tango\r\n",
    "  b20a @0169 [/,4b] = Pop\r\n",
    "  b20b @016a [/,4b] = Japanese\r\n",
];

#[derive(Clone, Debug, PartialEq)]
pub struct TextEntry {
    pub offset: String,
    pub attr: String,
    pub text: String,
}

/// Extracts and decodes `message.carc` into `message.d/new_music_message.txt`.
///
/// # Errors
/// Returns an error if the message directory cannot be resolved or
/// filesystem operations fail.
pub fn extract(text_dir: &Path) -> Result<(), WmError> {
    let message_dir = resolve_message_dir(text_dir)?;
    let message_archive = message_dir.join(MESSAGE_ARCHIVE_NAME);
    let extracted_dir = message_dir.join(MESSAGE_FOLDER_NAME);

    if extracted_dir.is_dir() {
        fs::remove_dir_all(&extracted_dir)?;
    }

    let carc_bytes = fs::read(&message_archive)?;
    let messages = carc::WiiMessages::from_bytes(&carc_bytes)
        .map_err(|e| WmError::Io(std::io::Error::other(e.to_string())))?;

    fs::create_dir_all(&extracted_dir)?;
    let txt_path = extracted_dir.join(MESSAGE_TEXT_NAME);
    fs::write(&txt_path, messages.to_text())?;

    Ok(())
}

/// Encodes `message.d/new_music_message.txt` and recreates `message.carc`.
///
/// # Errors
/// Returns an error if the message directory cannot be resolved or
/// filesystem operations fail.
pub fn encode(text_dir: &Path) -> Result<(), WmError> {
    let message_dir = resolve_message_dir(text_dir)?;
    let extracted_dir = message_dir.join(MESSAGE_FOLDER_NAME);
    let message_txt = extracted_dir.join(MESSAGE_TEXT_NAME);
    let message_archive = message_dir.join(MESSAGE_ARCHIVE_NAME);

    let txt = fs::read_to_string(&message_txt)?;
    let carc_bytes = fs::read(&message_archive)?;
    let mut messages = carc::WiiMessages::from_bytes(&carc_bytes)
        .map_err(|e| WmError::Io(std::io::Error::other(e.to_string())))?;
    messages
        .set_from_text(&txt)
        .map_err(|e| WmError::Io(std::io::Error::other(e.to_string())))?;
    fs::write(
        &message_archive,
        messages
            .to_bytes()
            .map_err(|e| WmError::Io(std::io::Error::other(e.to_string())))?,
    )?;

    if extracted_dir.is_dir() {
        fs::remove_dir_all(extracted_dir)?;
    }

    Ok(())
}

/// Parses positional BMG text lines into structured entries.
///
/// # Errors
/// Returns an error when the file cannot be read as UTF-8 text.
pub fn parse_text_file(path: &Path) -> Result<Vec<TextEntry>, WmError> {
    let content = fs::read_to_string(path)?;
    let mut entries = Vec::new();

    for line in content.split_inclusive('\n') {
        let trimmed = line.trim_end_matches(['\r', '\n']);
        if let Some(entry) = parse_line(trimmed) {
            entries.push(entry);
        }
    }

    Ok(entries)
}

/// Writes entries back to Wiimms text format with CRLF line endings.
///
/// # Errors
/// Returns an error when the output file cannot be written.
pub fn write_text_file(entries: &[TextEntry], path: &Path) -> Result<(), WmError> {
    let mut output = String::new();
    for entry in entries {
        output.push_str("  ");
        output.push_str(&entry.offset);
        output.push(' ');
        output.push_str(&entry.attr);
        output.push(' ');
        output.push_str(&entry.text);
        output.push_str("\r\n");
    }
    fs::write(path, output)?;
    Ok(())
}

/// Fixes malformed `QuickJam` custom style names in decoded message text.
///
/// # Errors
/// Returns an error when the message file cannot be read or written.
pub fn fix_message_file(path: &Path) -> Result<(), WmError> {
    let content = fs::read_to_string(path)?;
    let mut lines: Vec<String> = content
        .split_inclusive('\n')
        .map(std::string::ToString::to_string)
        .collect();

    if let Some(start) = lines.iter().position(|line| line == CUSTOM_QUICKJAM_NEEDLE) {
        let end = start.saturating_add(CUSTOM_QUICKJAM_PATCHES.len());
        if end <= lines.len() {
            for (index, patch) in CUSTOM_QUICKJAM_PATCHES.iter().enumerate() {
                lines[start + index] = (*patch).to_string();
            }
        }
    }

    fs::write(path, lines.concat())?;
    Ok(())
}

fn parse_line(line: &str) -> Option<TextEntry> {
    let bytes = line.as_bytes();
    if bytes.len() < 9 || bytes[0] != b' ' || bytes[1] != b' ' {
        return None;
    }
    let at_rel = line[2..].find(" @")?;
    let id_end = 2 + at_rel;
    let id_hex = &line[2..id_end];
    if id_hex.is_empty() || !id_hex.bytes().all(|b| b.is_ascii_hexdigit()) {
        return None;
    }
    let rest = &line[id_end + 1..]; // starts at '@'
    if rest.len() < 6 || rest.as_bytes()[5] != b' ' {
        return None;
    }
    let attr = &rest[..5]; // "@YYYY"
    if !rest[1..5].bytes().all(|b| b.is_ascii_hexdigit()) {
        return None;
    }
    Some(TextEntry {
        offset: id_hex.to_string(),
        attr: attr.to_string(),
        text: rest[6..].to_string(),
    })
}

fn resolve_message_dir(text_dir: &Path) -> Result<PathBuf, WmError> {
    let message_dir = text_dir.join("Message");
    if message_dir.is_dir() {
        return Ok(message_dir);
    }
    Err(WmError::Parse {
        file: text_dir.display().to_string(),
        offset: 0x0,
        message: "Message directory not found".to_string(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_text_round_trip() {
        let sample = "  c80000 @0000 A Little Night Music\r\n  c80001 @0000 Mii Channel\r\n";
        let dir = tempfile::TempDir::new().unwrap();
        let path = dir.path().join("test.txt");
        std::fs::write(&path, sample).unwrap();
        let entries = parse_text_file(&path).unwrap();
        assert_eq!(entries.len(), 2);
        assert_eq!(entries[0].offset, "c80000");
        assert_eq!(entries[0].text, "A Little Night Music");
        write_text_file(&entries, &path).unwrap();
        let entries2 = parse_text_file(&path).unwrap();
        assert_eq!(entries, entries2);
    }

    #[test]
    fn test_fix_message_file_patches_custom_quickjam_block() {
        let dir = tempfile::TempDir::new().unwrap();
        let path = dir.path().join("message.txt");
        let input = concat!(
            "  b200 @015f /\r\n",
            "  b201 @0160 /\r\n",
            "  b202 @0161 /\r\n",
            "  b203 @0162 /\r\n",
            "  b204 @0163 /\r\n",
            "  b205 @0164 /\r\n",
            "  b206 @0165 /\r\n",
            "  b207 @0166 /\r\n",
            "  b208 @0167 /\r\n",
            "  b209 @0168 /\r\n",
            "  b20a @0169 /\r\n",
            "  b20b @016a /\r\n"
        );
        std::fs::write(&path, input).unwrap();

        fix_message_file(&path).unwrap();

        let output = std::fs::read_to_string(path).unwrap();
        assert!(output.contains("  b200 @015f [/,4b] = Default\r\n"));
        assert!(output.contains("  b20b @016a [/,4b] = Japanese\r\n"));
    }

    #[test]
    fn test_parse_line_too_short() {
        let dir = tempfile::TempDir::new().unwrap();
        let path = dir.path().join("short.txt");
        std::fs::write(&path, "  c800\r\n").unwrap();

        let entries = parse_text_file(&path).unwrap();
        assert!(entries.is_empty());
    }

    #[test]
    fn test_parse_line_wrong_format() {
        let dir = tempfile::TempDir::new().unwrap();
        let path = dir.path().join("wrong.txt");
        std::fs::write(&path, "  c80000 X0000 Some Text\r\n").unwrap();

        let entries = parse_text_file(&path).unwrap();
        assert!(entries.is_empty());
    }

    #[test]
    fn test_parse_line_valid_boundary() {
        let dir = tempfile::TempDir::new().unwrap();
        let path = dir.path().join("boundary.txt");
        std::fs::write(&path, "  c80000 @0000 X\r\n").unwrap();

        let entries = parse_text_file(&path).unwrap();
        assert_eq!(entries.len(), 1);
        assert_eq!(entries[0].offset, "c80000");
        assert_eq!(entries[0].attr, "@0000");
        assert_eq!(entries[0].text, "X");
    }
}
