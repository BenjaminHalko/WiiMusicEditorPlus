mod archive;
mod bmg;
mod messages;

pub use archive::Carc;
pub use bmg::{Bmg, BmgEntry};
pub use messages::WiiMessages;

#[derive(Debug, thiserror::Error)]
pub enum SzsError {
    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),
    #[error("UTF-16 decode error: {0}")]
    Utf16(#[from] std::string::FromUtf16Error),
    #[error("Invalid archive/file magic: {0:#010x}")]
    InvalidMagic(u32),
    #[error("Invalid U8 archive: {0}")]
    InvalidU8(String),
    #[error("Invalid BMG: {0}")]
    InvalidBmg(String),
    #[error("Compression/decompression failed: {0}")]
    Compression(String),
    #[error("File not found")]
    FileNotFound,
    #[error("Index out of range: {index}")]
    IndexOutOfRange { index: usize },
}
