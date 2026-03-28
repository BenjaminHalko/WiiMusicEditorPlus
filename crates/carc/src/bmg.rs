use crate::SzsError;
use crate::archive::{align_up, read_u16_at, read_u32_at};

const BMG_MAGIC: &[u8; 8] = b"MESGbmg1";

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct BmgEntry {
    pub id: u32,
    pub attr: u16,
    pub text: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Bmg {
    pub entries: Vec<BmgEntry>,
    encoding: u8,
    inf_item_size: u16,
    inf_unknown_0c: u32,
    has_mid: bool,
    mid_unknown_0a: u16,
    mid_unknown_0c: u32,
    header_unknown: [u8; 15],
    inf_attrs_raw: Vec<Vec<u8>>,
}

impl Bmg {
    /// Parses a BMG message file image.
    ///
    /// # Errors
    /// Returns `SzsError::InvalidMagic` for a bad header and `SzsError::InvalidBmg`
    /// for truncated or malformed sections.
    #[allow(clippy::too_many_lines, clippy::similar_names)]
    pub fn from_bytes(data: &[u8]) -> Result<Self, SzsError> {
        if data.len() < 0x20 {
            return Err(SzsError::InvalidBmg("BMG shorter than header".to_string()));
        }
        if &data[0..8] != BMG_MAGIC {
            let magic = read_u32_at(data, 0).unwrap_or_default();
            return Err(SzsError::InvalidMagic(magic));
        }

        let file_size = read_u32_at(data, 0x08)
            .ok_or_else(|| SzsError::InvalidBmg("Missing file size".to_string()))?
            as usize;
        if file_size > data.len() {
            return Err(SzsError::InvalidBmg(format!(
                "Header file size {file_size:#x} exceeds input length {:#x}",
                data.len()
            )));
        }

        let n_sections = read_u32_at(data, 0x0C)
            .ok_or_else(|| SzsError::InvalidBmg("Missing section count".to_string()))?
            as usize;
        let encoding = data[0x10];
        let mut header_unknown = [0_u8; 15];
        header_unknown.copy_from_slice(&data[0x11..0x20]);

        #[allow(clippy::type_complexity)]
        let mut inf: Option<(u16, u16, u32, Vec<u32>, Vec<Vec<u8>>)> = None;
        let mut dat_payload: Option<Vec<u8>> = None;
        let mut mid: Option<(u16, u16, u32, Vec<u32>)> = None;

        let mut off: usize = 0x20;
        for _ in 0..n_sections {
            if off.checked_add(8).is_none_or(|v| v > data.len()) {
                return Err(SzsError::InvalidBmg(
                    "Section header out of range".to_string(),
                ));
            }

            let section_magic = &data[off..off + 4];
            let section_size = read_u32_at(data, off + 4)
                .ok_or_else(|| SzsError::InvalidBmg("Missing section size".to_string()))?
                as usize;

            if section_size < 8 {
                return Err(SzsError::InvalidBmg(
                    "Section size smaller than header".to_string(),
                ));
            }

            let section_end = off
                .checked_add(section_size)
                .ok_or_else(|| SzsError::InvalidBmg("Section size overflow".to_string()))?;
            if section_end > data.len() {
                return Err(SzsError::InvalidBmg(
                    "Section extends beyond input".to_string(),
                ));
            }

            match section_magic {
                b"INF1" => {
                    if section_size < 0x10 {
                        return Err(SzsError::InvalidBmg("INF1 too small".to_string()));
                    }

                    let n_msg = read_u16_at(data, off + 8)
                        .ok_or_else(|| SzsError::InvalidBmg("INF1 missing n_msg".to_string()))?;
                    let inf_item_size = read_u16_at(data, off + 10)
                        .ok_or_else(|| SzsError::InvalidBmg("INF1 missing inf_size".to_string()))?;
                    let unknown_0c = read_u32_at(data, off + 12).ok_or_else(|| {
                        SzsError::InvalidBmg("INF1 missing unknown_0c".to_string())
                    })?;

                    if inf_item_size < 4 {
                        return Err(SzsError::InvalidBmg(format!(
                            "INF1 item size too small: {inf_item_size}"
                        )));
                    }

                    let table_len = usize::from(n_msg)
                        .checked_mul(usize::from(inf_item_size))
                        .ok_or_else(|| {
                            SzsError::InvalidBmg("INF1 table size overflow".to_string())
                        })?;
                    let table_start = off + 0x10;
                    let table_end = table_start.checked_add(table_len).ok_or_else(|| {
                        SzsError::InvalidBmg("INF1 table end overflow".to_string())
                    })?;
                    if table_end > section_end {
                        return Err(SzsError::InvalidBmg(
                            "INF1 table exceeds section size".to_string(),
                        ));
                    }

                    let mut offsets = Vec::with_capacity(usize::from(n_msg));
                    let mut attrs = Vec::with_capacity(usize::from(n_msg));
                    let step = usize::from(inf_item_size);

                    for index in 0..usize::from(n_msg) {
                        let item_off = table_start + index * step;
                        let dat_offset = read_u32_at(data, item_off).ok_or_else(|| {
                            SzsError::InvalidBmg("INF1 item missing DAT offset".to_string())
                        })?;
                        offsets.push(dat_offset);
                        attrs.push(data[item_off + 4..item_off + step].to_vec());
                    }

                    inf = Some((n_msg, inf_item_size, unknown_0c, offsets, attrs));
                }
                b"DAT1" => {
                    dat_payload = Some(data[off + 8..section_end].to_vec());
                }
                b"MID1" => {
                    if section_size < 0x10 {
                        return Err(SzsError::InvalidBmg("MID1 too small".to_string()));
                    }

                    let n_msg = read_u16_at(data, off + 8)
                        .ok_or_else(|| SzsError::InvalidBmg("MID1 missing n_msg".to_string()))?;
                    let unknown_0a = read_u16_at(data, off + 10).ok_or_else(|| {
                        SzsError::InvalidBmg("MID1 missing unknown_0a".to_string())
                    })?;
                    let unknown_0c = read_u32_at(data, off + 12).ok_or_else(|| {
                        SzsError::InvalidBmg("MID1 missing unknown_0c".to_string())
                    })?;
                    let ids_len = usize::from(n_msg).checked_mul(4).ok_or_else(|| {
                        SzsError::InvalidBmg("MID1 IDs size overflow".to_string())
                    })?;
                    let ids_start = off + 0x10;
                    let ids_end = ids_start
                        .checked_add(ids_len)
                        .ok_or_else(|| SzsError::InvalidBmg("MID1 IDs end overflow".to_string()))?;
                    if ids_end > section_end {
                        return Err(SzsError::InvalidBmg(
                            "MID1 IDs exceed section size".to_string(),
                        ));
                    }

                    let mut ids = Vec::with_capacity(usize::from(n_msg));
                    for index in 0..usize::from(n_msg) {
                        let id_off = ids_start + index * 4;
                        let id = read_u32_at(data, id_off)
                            .ok_or_else(|| SzsError::InvalidBmg("MID1 missing ID".to_string()))?;
                        ids.push(id);
                    }
                    mid = Some((n_msg, unknown_0a, unknown_0c, ids));
                }
                _ => {}
            }

            off = section_end;
        }

        let (inf_n_msg, inf_item_size, inf_unknown_0c, dat_offsets, inf_attrs_raw) =
            inf.ok_or_else(|| SzsError::InvalidBmg("Missing INF1 section".to_string()))?;
        let dat_payload =
            dat_payload.ok_or_else(|| SzsError::InvalidBmg("Missing DAT1 section".to_string()))?;

        let mut entries = Vec::with_capacity(usize::from(inf_n_msg));
        for index in 0..usize::from(inf_n_msg) {
            let dat_offset = usize::try_from(dat_offsets[index]).map_err(|_| {
                SzsError::InvalidBmg(format!("DAT1 offset too large: {}", dat_offsets[index]))
            })?;
            let text = decode_utf16be_cstr(&dat_payload, dat_offset)?;

            let attr = inf_attrs_raw[index]
                .get(0..2)
                .map_or(0, |slice| u16::from_be_bytes([slice[0], slice[1]]));

            entries.push(BmgEntry { id: 0, attr, text });
        }

        let (has_mid, mid_unknown_0a, mid_unknown_0c) =
            if let Some((mid_n_msg, u0a, u0c, ids)) = mid {
                if mid_n_msg != inf_n_msg {
                    return Err(SzsError::InvalidBmg(format!(
                        "MID1 count {mid_n_msg} does not match INF1 count {inf_n_msg}"
                    )));
                }
                for (entry, id) in entries.iter_mut().zip(ids) {
                    entry.id = id;
                }
                (true, u0a, u0c)
            } else {
                for (index, entry) in entries.iter_mut().enumerate() {
                    entry.id = u32::try_from(index)
                        .map_err(|_| SzsError::InvalidBmg("Message index overflow".to_string()))?;
                }
                (false, 0, 0)
            };

        Ok(Self {
            entries,
            encoding,
            inf_item_size,
            inf_unknown_0c,
            has_mid,
            mid_unknown_0a,
            mid_unknown_0c,
            header_unknown,
            inf_attrs_raw,
        })
    }

    /// Serializes the message file back to bytes.
    ///
    /// # Errors
    /// Returns `SzsError::InvalidBmg` if counts or section sizes overflow.
    pub fn to_bytes(&self) -> Result<Vec<u8>, SzsError> {
        let n_msg_u16 = u16::try_from(self.entries.len())
            .map_err(|_| SzsError::InvalidBmg("Too many entries for BMG".to_string()))?;

        if self.inf_item_size < 4 {
            return Err(SzsError::InvalidBmg(format!(
                "INF1 item size too small: {}",
                self.inf_item_size
            )));
        }

        let mut dat_payload = vec![0x00, 0x00];
        let mut dat_offsets = Vec::with_capacity(self.entries.len());
        for entry in &self.entries {
            let offset = u32::try_from(dat_payload.len())
                .map_err(|_| SzsError::InvalidBmg("DAT1 payload too large".to_string()))?;
            dat_offsets.push(offset);

            for unit in entry.text.encode_utf16() {
                dat_payload.extend_from_slice(&unit.to_be_bytes());
            }
            dat_payload.extend_from_slice(&0_u16.to_be_bytes());
        }

        let mut inf_body = Vec::new();
        inf_body.extend_from_slice(&n_msg_u16.to_be_bytes());
        inf_body.extend_from_slice(&self.inf_item_size.to_be_bytes());
        inf_body.extend_from_slice(&self.inf_unknown_0c.to_be_bytes());

        let attr_len = usize::from(self.inf_item_size - 4);
        for (index, entry) in self.entries.iter().enumerate() {
            inf_body.extend_from_slice(&dat_offsets[index].to_be_bytes());

            let mut attrs = if let Some(raw) = self.inf_attrs_raw.get(index) {
                let mut copy = raw.clone();
                copy.resize(attr_len, 0);
                copy
            } else {
                vec![0_u8; attr_len]
            };

            if attr_len >= 2 {
                attrs[0..2].copy_from_slice(&entry.attr.to_be_bytes());
            }
            inf_body.extend_from_slice(&attrs);
        }

        let inf_section = make_section(*b"INF1", inf_body)?;
        let dat_section = make_section(*b"DAT1", dat_payload)?;

        let mid_section = if self.has_mid {
            let mut body = Vec::new();
            body.extend_from_slice(&n_msg_u16.to_be_bytes());
            body.extend_from_slice(&self.mid_unknown_0a.to_be_bytes());
            body.extend_from_slice(&self.mid_unknown_0c.to_be_bytes());
            for entry in &self.entries {
                body.extend_from_slice(&entry.id.to_be_bytes());
            }
            Some(make_section(*b"MID1", body)?)
        } else {
            None
        };

        let n_sections = if mid_section.is_some() { 3_u32 } else { 2_u32 };
        let mut out = vec![0_u8; 0x20];
        out[0..8].copy_from_slice(BMG_MAGIC);
        out[0x0C..0x10].copy_from_slice(&n_sections.to_be_bytes());
        out[0x10] = self.encoding;
        out[0x11..0x20].copy_from_slice(&self.header_unknown);

        out.extend_from_slice(&inf_section);
        out.extend_from_slice(&dat_section);
        if let Some(mid) = mid_section {
            out.extend_from_slice(&mid);
        }

        let file_size = u32::try_from(out.len())
            .map_err(|_| SzsError::InvalidBmg("Serialized BMG too large".to_string()))?;
        out[0x08..0x0C].copy_from_slice(&file_size.to_be_bytes());

        Ok(out)
    }

    /// Updates a message entry's text by index.
    ///
    /// # Errors
    /// Returns `SzsError::IndexOutOfRange` if `index` is not valid.
    pub fn set_text(&mut self, index: usize, text: &str) -> Result<(), SzsError> {
        let entry = self
            .entries
            .get_mut(index)
            .ok_or(SzsError::IndexOutOfRange { index })?;
        entry.text = text.to_string();
        Ok(())
    }

    #[must_use]
    pub fn to_text(&self) -> String {
        use std::fmt::Write as _;
        let mut out = String::new();
        for entry in &self.entries {
            let escaped = entry.text.replace('\n', "\\n").replace('\r', "\\r");
            let _ = write!(
                out,
                "  {:06x} @{:04x} {}\r\n",
                entry.id, entry.attr, escaped
            );
        }
        out
    }

    /// Parses Wiimms text format into a BMG structure.
    ///
    /// # Errors
    /// Returns `SzsError::InvalidBmg` when a line has the wrong layout or bad
    /// hex data.
    pub fn from_text(text: &str) -> Result<Self, SzsError> {
        let mut entries = Vec::new();

        for (line_no, line) in text.lines().enumerate() {
            if line.is_empty() {
                continue;
            }

            let line = line.trim_end_matches('\r');

            let bytes = line.as_bytes();
            if bytes.len() < 9 || bytes[0] != b' ' || bytes[1] != b' ' {
                return Err(SzsError::InvalidBmg(format!(
                    "Invalid text format on line {}",
                    line_no + 1
                )));
            }

            // Find " @" to locate end of ID field (ID can be 4–8 hex digits)
            let Some(at_rel) = line[2..].find(" @") else {
                return Err(SzsError::InvalidBmg(format!(
                    "Missing ' @' separator on line {}",
                    line_no + 1
                )));
            };
            let id_end = 2 + at_rel;
            let id_hex = &line[2..id_end];
            if id_hex.is_empty() || !id_hex.bytes().all(|b| b.is_ascii_hexdigit()) {
                return Err(SzsError::InvalidBmg(format!(
                    "Invalid ID hex on line {}",
                    line_no + 1
                )));
            }

            let rest = &line[id_end + 2..]; // skip " @"
            if rest.len() < 5 || rest.as_bytes()[4] != b' ' {
                return Err(SzsError::InvalidBmg(format!(
                    "Invalid attr field on line {}",
                    line_no + 1
                )));
            }
            let attr_hex = &rest[..4];
            if !attr_hex.bytes().all(|b| b.is_ascii_hexdigit()) {
                return Err(SzsError::InvalidBmg(format!(
                    "Invalid attr hex on line {}",
                    line_no + 1
                )));
            }
            let text_raw = &rest[5..];

            let id = u32::from_str_radix(id_hex, 16).map_err(|e| {
                SzsError::InvalidBmg(format!("Invalid id on line {}: {e}", line_no + 1))
            })?;
            let attr = u16::from_str_radix(attr_hex, 16).map_err(|e| {
                SzsError::InvalidBmg(format!("Invalid attr on line {}: {e}", line_no + 1))
            })?;

            entries.push(BmgEntry {
                id,
                attr,
                text: text_raw.replace("\\n", "\n").replace("\\r", "\r"),
            });
        }

        let inf_item_size = 8_u16;
        let inf_attrs_raw = entries
            .iter()
            .map(|entry| {
                let mut attrs = vec![0_u8; usize::from(inf_item_size - 4)];
                attrs[0..2].copy_from_slice(&entry.attr.to_be_bytes());
                attrs
            })
            .collect();

        Ok(Self {
            entries,
            encoding: 2,
            inf_item_size,
            inf_unknown_0c: 0,
            has_mid: true,
            mid_unknown_0a: 0,
            mid_unknown_0c: 0,
            header_unknown: [0_u8; 15],
            inf_attrs_raw,
        })
    }
}

fn decode_utf16be_cstr(data: &[u8], start: usize) -> Result<String, SzsError> {
    if start >= data.len() {
        return Err(SzsError::InvalidBmg(format!(
            "String offset out of range: {start:#x}"
        )));
    }
    if !start.is_multiple_of(2) {
        return Err(SzsError::InvalidBmg(format!(
            "String offset is not UTF-16 aligned: {start:#x}"
        )));
    }

    let mut units = Vec::new();
    let mut off = start;
    loop {
        if off + 2 > data.len() {
            return Err(SzsError::InvalidBmg(
                "Unterminated UTF-16 string".to_string(),
            ));
        }
        let unit = u16::from_be_bytes([data[off], data[off + 1]]);
        if unit == 0 {
            break;
        }
        units.push(unit);
        off += 2;
    }

    String::from_utf16(&units).map_err(SzsError::from)
}

fn make_section(magic: [u8; 4], mut body: Vec<u8>) -> Result<Vec<u8>, SzsError> {
    let min_size = 8_usize
        .checked_add(body.len())
        .ok_or_else(|| SzsError::InvalidBmg("Section size overflow".to_string()))?;
    let section_size = align_up(min_size, 0x20);

    body.resize(section_size - 8, 0);
    let mut section = Vec::with_capacity(section_size);
    section.extend_from_slice(&magic);
    section.extend_from_slice(
        &u32::try_from(section_size)
            .map_err(|_| SzsError::InvalidBmg("Section too large".to_string()))?
            .to_be_bytes(),
    );
    section.extend_from_slice(&body);
    Ok(section)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn bmg_binary_round_trip_preserves_fields() {
        let mut bmg =
            Bmg::from_text("  c80000 @015f A Little Night Music\r\n  c80001 @0160 Mii Channel\r\n")
                .expect("from text");
        bmg.mid_unknown_0a = 0x1000;
        bmg.mid_unknown_0c = 0x1234_5678;
        bmg.inf_unknown_0c = 0x89AB_CDEF;
        bmg.header_unknown = [0xAA; 15];

        let bytes = bmg.to_bytes().expect("serialize bmg");
        let reparsed = Bmg::from_bytes(&bytes).expect("parse bmg");

        assert_eq!(reparsed.entries, bmg.entries);
        assert_eq!(reparsed.encoding, 2);
        assert_eq!(reparsed.inf_item_size, 8);
        assert_eq!(reparsed.inf_unknown_0c, 0x89AB_CDEF);
        assert!(reparsed.has_mid);
        assert_eq!(reparsed.mid_unknown_0a, 0x1000);
        assert_eq!(reparsed.mid_unknown_0c, 0x1234_5678);
        assert_eq!(reparsed.header_unknown, [0xAA; 15]);
    }

    #[test]
    fn bmg_set_text_updates_entry() {
        let mut bmg = Bmg::from_text("  c80000 @0000 Old\r\n").expect("from text");
        bmg.set_text(0, "New Song Name").expect("set text");
        assert_eq!(bmg.entries[0].text, "New Song Name");
        assert!(matches!(
            bmg.set_text(4, "x").expect_err("out of range"),
            SzsError::IndexOutOfRange { .. }
        ));
    }

    #[test]
    fn bmg_text_round_trip() {
        let text = "  c80000 @0000 A Little Night Music\r\n  c80001 @0010 Mii Channel\r\n";
        let bmg = Bmg::from_text(text).expect("from text");
        assert_eq!(bmg.to_text(), text);
    }
}
