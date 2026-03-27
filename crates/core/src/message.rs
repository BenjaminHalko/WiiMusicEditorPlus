use std::fs;
use std::path::{Path, PathBuf};

use crate::paths::WmPaths;
use crate::shell::run_tool;
use crate::types::WmError;

const MESSAGE_ARCHIVE_NAME: &str = "message.carc";
const MESSAGE_FOLDER_NAME: &str = "message.d";
const MESSAGE_BMG_NAME: &str = "new_music_message.bmg";
const MESSAGE_TEXT_NAME: &str = "new_music_message.txt";
const WSZST_SETUP_NAME: &str = "wszst-setup.txt";
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
/// Returns an error if the message directory cannot be resolved, external tools
/// fail, or filesystem operations fail.
pub fn extract(paths: &WmPaths, rom_folder: &Path) -> Result<(), WmError> {
    let message_dir = resolve_message_dir(rom_folder)?;
    let message_archive = message_dir.join(MESSAGE_ARCHIVE_NAME);
    let extracted_dir = message_dir.join(MESSAGE_FOLDER_NAME);

    if extracted_dir.is_dir() {
        fs::remove_dir_all(&extracted_dir)?;
    }

    let message_archive_arg = message_archive.to_string_lossy().into_owned();
    let wszst_args = ["extract", message_archive_arg.as_str()];
    run_tool(paths, "wiimms/wszst", &wszst_args)?;

    let setup_file = extracted_dir.join(WSZST_SETUP_NAME);
    remove_if_exists(&setup_file)?;

    let message_bmg = extracted_dir.join(MESSAGE_BMG_NAME);
    let message_bmg_arg = message_bmg.to_string_lossy().into_owned();
    let wbmgt_args = ["decode", message_bmg_arg.as_str()];
    run_tool(paths, "wiimms/wbmgt", &wbmgt_args)?;

    remove_if_exists(&message_bmg)?;
    Ok(())
}

/// Encodes `message.d/new_music_message.txt` and recreates `message.carc`.
///
/// # Errors
/// Returns an error if the message directory cannot be resolved, external tools
/// fail, or filesystem operations fail.
pub fn encode(paths: &WmPaths, rom_folder: &Path) -> Result<(), WmError> {
    let message_dir = resolve_message_dir(rom_folder)?;
    let extracted_dir = message_dir.join(MESSAGE_FOLDER_NAME);
    let message_txt = extracted_dir.join(MESSAGE_TEXT_NAME);
    let message_archive = message_dir.join(MESSAGE_ARCHIVE_NAME);

    let message_txt_arg = message_txt.to_string_lossy().into_owned();
    let wbmgt_args = ["encode", message_txt_arg.as_str()];
    run_tool(paths, "wiimms/wbmgt", &wbmgt_args)?;

    remove_if_exists(&message_txt)?;
    remove_if_exists(&message_archive)?;

    let extracted_dir_arg = extracted_dir.to_string_lossy().into_owned();
    let message_archive_arg = message_archive.to_string_lossy().into_owned();
    let wszst_args = [
        "create",
        extracted_dir_arg.as_str(),
        "--dest",
        message_archive_arg.as_str(),
    ];
    run_tool(paths, "wiimms/wszst", &wszst_args)?;

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
    if line.len() < 16 {
        return None;
    }

    let bytes = line.as_bytes();
    if bytes[0] != b' '
        || bytes[1] != b' '
        || bytes[8] != b' '
        || bytes[9] != b'@'
        || bytes[14] != b' '
    {
        return None;
    }

    if !bytes[2..8].iter().all(u8::is_ascii_hexdigit) {
        return None;
    }
    if !bytes[10..14].iter().all(u8::is_ascii_hexdigit) {
        return None;
    }

    Some(TextEntry {
        offset: line[2..8].to_string(),
        attr: line[9..14].to_string(),
        text: line[15..].to_string(),
    })
}

fn remove_if_exists(path: &Path) -> Result<(), WmError> {
    if path.exists() {
        fs::remove_file(path)?;
    }
    Ok(())
}

fn resolve_message_dir(rom_folder: &Path) -> Result<PathBuf, WmError> {
    if rom_folder.join(MESSAGE_ARCHIVE_NAME).is_file() {
        return Ok(rom_folder.to_path_buf());
    }

    let files_dir = rom_folder.join("files");
    if !files_dir.is_dir() {
        return Err(WmError::Parse {
            file: rom_folder.display().to_string(),
            offset: 0x0,
            message: "Could not locate files/ directory for message.carc".to_string(),
        });
    }

    let mut found = None;
    for region_entry in fs::read_dir(files_dir)? {
        let region_path = region_entry?.path();
        let candidate = region_path.join("Message");
        if candidate.join(MESSAGE_ARCHIVE_NAME).is_file() {
            found = Some(candidate);
            break;
        }
    }

    found.ok_or_else(|| WmError::Parse {
        file: rom_folder.display().to_string(),
        offset: 0x0,
        message: "Could not locate region Message/message.carc".to_string(),
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
