use crate::SzsError;
use crate::archive::Carc;
use crate::bmg::{Bmg, BmgEntry};

const MESSAGE_BMG_FILENAME: &str = "new_music_message.bmg";

/// A Wii Music message archive: a Yaz0-compressed CARC archive containing a BMG file.
///
/// Combines [`Carc`] and [`Bmg`] so callers never need the double-conversion manually.
#[derive(Clone, Debug)]
pub struct WiiMessages {
    carc: Carc,
    bmg: Bmg,
}

impl WiiMessages {
    /// Decodes a `.carc` archive and parses the embedded `new_music_message.bmg`.
    ///
    /// # Errors
    /// Returns [`SzsError`] if decompression, U8 parsing, or BMG parsing fails, or if
    /// `new_music_message.bmg` is absent from the archive.
    pub fn from_bytes(data: &[u8]) -> Result<Self, SzsError> {
        let carc = Carc::from_bytes(data)?;
        let bmg_bytes = carc
            .get(MESSAGE_BMG_FILENAME)
            .ok_or(SzsError::FileNotFound)?;
        let bmg = Bmg::from_bytes(bmg_bytes)?;
        Ok(Self { carc, bmg })
    }

    /// Encodes the (possibly modified) BMG back into the archive and Yaz0-compresses it.
    ///
    /// # Errors
    /// Returns [`SzsError`] if BMG serialization or Yaz0 encoding fails.
    pub fn to_bytes(&self) -> Result<Vec<u8>, SzsError> {
        let bmg_bytes = self.bmg.to_bytes()?;
        let mut updated = self.carc.clone();
        updated.insert(MESSAGE_BMG_FILENAME.to_string(), bmg_bytes);
        updated.to_bytes()
    }

    /// Returns a slice of all message entries.
    #[must_use]
    pub fn entries(&self) -> &[BmgEntry] {
        &self.bmg.entries
    }

    /// Updates a message entry's text by index.
    ///
    /// # Errors
    /// Returns [`SzsError::IndexOutOfRange`] if `index` is out of bounds.
    pub fn set_text(&mut self, index: usize, text: &str) -> Result<(), SzsError> {
        self.bmg.set_text(index, text)
    }

    /// Renders all entries in Wiimms BMG text format (CRLF line endings).
    #[must_use]
    pub fn to_text(&self) -> String {
        self.bmg.to_text()
    }

    /// Replaces all BMG entries by parsing Wiimms BMG text format.
    ///
    /// # Errors
    /// Returns [`SzsError::InvalidBmg`] if the text is malformed.
    pub fn set_from_text(&mut self, text: &str) -> Result<(), SzsError> {
        self.bmg.entries = Bmg::from_text(text)?.entries;
        Ok(())
    }
}
