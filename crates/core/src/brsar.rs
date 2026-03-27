use crate::types::WmError;

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Brsar {
    data: Vec<u8>,
    info_section_offset: usize,
}

#[derive(Clone, Debug, Eq, PartialEq)]
struct GroupItemEntry {
    entry_offset: usize,
    rseq_offset: usize,
    rseq_size: usize,
}

#[derive(Clone, Debug, Eq, PartialEq)]
struct GroupDataEntry {
    entry_offset: usize,
    rseq_offset: usize,
    items: Vec<GroupItemEntry>,
}

const BRSAR_MAGIC: u32 = 0x5253_4152;

const HEADER_FILE_LENGTH_OFFSET: usize = 0x08;
const HEADER_INFO_SECTION_OFFSET: usize = 0x18;
const HEADER_FILE_SECTION_OFFSET: usize = 0x20;

const INFO_GROUP_TABLE_REF_OFFSET: usize = 0x28;

const REFERENCE_VALUE_OFFSET: usize = 0x04;
const REFERENCE_STRIDE: usize = 0x08;

const GROUP_DATA_RSEQ_OFFSET_FIELD: usize = 0x10;
const GROUP_DATA_RSEQ_SIZE_FIELD: usize = 0x14;
const GROUP_DATA_RWAR_OFFSET_FIELD: usize = 0x18;
const GROUP_DATA_ITEM_TABLE_REF_FIELD: usize = 0x20;

const GROUP_ITEM_TABLE_COUNT_FIELD: usize = 0x00;
const GROUP_ITEM_TABLE_ENTRIES_FIELD: usize = 0x04;

const GROUP_ITEM_RSEQ_OFFSET_FIELD: usize = 0x04;
const GROUP_ITEM_RSEQ_SIZE_FIELD: usize = 0x08;

const U32_SIZE: usize = 0x04;
const INFO_REFERENCE_BASE_BIAS: usize = 0x08;

impl Brsar {
    #[allow(clippy::missing_errors_doc)]
    pub fn parse(data: Vec<u8>) -> Result<Self, WmError> {
        if data.len() < HEADER_FILE_SECTION_OFFSET + U32_SIZE {
            return Err(Self::parse_error(
                0x00,
                "file too small for BRSAR header fields",
            ));
        }

        let mut magic_bytes = [0x00_u8; U32_SIZE];
        magic_bytes.copy_from_slice(&data[0x00..U32_SIZE]);
        if u32::from_be_bytes(magic_bytes) != BRSAR_MAGIC {
            return Err(Self::parse_error(
                0x00,
                "invalid BRSAR magic (expected RSAR)",
            ));
        }

        let info_section_offset = {
            let mut offset_bytes = [0x00_u8; U32_SIZE];
            offset_bytes.copy_from_slice(
                &data[HEADER_INFO_SECTION_OFFSET..HEADER_INFO_SECTION_OFFSET + U32_SIZE],
            );
            usize::try_from(u32::from_be_bytes(offset_bytes)).map_err(|_| {
                Self::parse_error(
                    HEADER_INFO_SECTION_OFFSET,
                    "INFO section offset does not fit usize",
                )
            })?
        };

        if info_section_offset + U32_SIZE > data.len() {
            return Err(Self::parse_error(
                HEADER_INFO_SECTION_OFFSET,
                "INFO section offset points outside file",
            ));
        }

        Ok(Self {
            data,
            info_section_offset,
        })
    }

    #[must_use]
    pub fn read_u32(&self, offset: usize) -> u32 {
        let mut bytes = [0x00_u8; U32_SIZE];
        bytes.copy_from_slice(&self.data[offset..offset + U32_SIZE]);
        u32::from_be_bytes(bytes)
    }

    pub fn write_u32(&mut self, offset: usize, value: u32) {
        self.data[offset..offset + U32_SIZE].copy_from_slice(&value.to_be_bytes());
    }

    #[must_use]
    pub fn section_reference(&self, offset: usize) -> usize {
        let section_offset = self.read_u32(offset) as usize;
        section_offset + self.info_section_offset + INFO_REFERENCE_BASE_BIAS
    }

    pub fn increment_value(&mut self, offset: usize, delta: i64) {
        let current = i128::from(self.read_u32(offset));
        let updated = current + i128::from(delta);
        if updated.is_negative() || updated > i128::from(u32::MAX) {
            return;
        }
        self.write_u32(offset, updated as u32);
    }

    #[allow(clippy::missing_errors_doc)]
    pub fn get_song(&self, item: usize) -> Result<Vec<u8>, WmError> {
        let groups = self.parse_groups()?;
        let (group_index, item_index) = Self::resolve_item(&groups, item)?;

        let group = &groups[group_index];
        let item_entry = &group.items[item_index];
        let rseq_offset = group.rseq_offset + item_entry.rseq_offset;
        let rseq_end = rseq_offset
            .checked_add(item_entry.rseq_size)
            .ok_or_else(|| Self::parse_error(item_entry.entry_offset, "song range overflow"))?;

        if rseq_end > self.data.len() {
            return Err(Self::parse_error(
                item_entry.entry_offset,
                "song range points outside file",
            ));
        }

        Ok(self.data[rseq_offset..rseq_end].to_vec())
    }

    #[allow(clippy::missing_errors_doc)]
    pub fn replace_song(&mut self, item: usize, new_data: &[u8]) -> Result<(), WmError> {
        let groups = self.parse_groups()?;
        let (group_index, item_index) = Self::resolve_item(&groups, item)?;

        let group = &groups[group_index];
        let item_entry = &group.items[item_index];
        let rseq_offset = group.rseq_offset + item_entry.rseq_offset;
        let rseq_end = rseq_offset
            .checked_add(item_entry.rseq_size)
            .ok_or_else(|| Self::parse_error(item_entry.entry_offset, "song range overflow"))?;

        if rseq_end > self.data.len() {
            return Err(Self::parse_error(
                item_entry.entry_offset,
                "song range points outside file",
            ));
        }

        let old_size_i64 = i64::try_from(item_entry.rseq_size)
            .map_err(|_| Self::parse_error(item_entry.entry_offset, "old song size too large"))?;
        let new_size_i64 = i64::try_from(new_data.len())
            .map_err(|_| Self::parse_error(item_entry.entry_offset, "new song size too large"))?;
        let increment_amount = new_size_i64 - old_size_i64;

        self.data
            .splice(rseq_offset..rseq_end, new_data.iter().copied());

        self.increment_value(
            group.entry_offset + GROUP_DATA_RSEQ_SIZE_FIELD,
            increment_amount,
        );
        self.increment_value(
            group.entry_offset + GROUP_DATA_RWAR_OFFSET_FIELD,
            increment_amount,
        );
        self.increment_value(
            item_entry.entry_offset + GROUP_ITEM_RSEQ_SIZE_FIELD,
            increment_amount,
        );

        for later_item in group.items.iter().skip(item_index + 0x01) {
            self.increment_value(
                later_item.entry_offset + GROUP_ITEM_RSEQ_OFFSET_FIELD,
                increment_amount,
            );
        }

        for later_group in groups.iter().skip(group_index + 0x01) {
            self.increment_value(
                later_group.entry_offset + GROUP_DATA_RSEQ_OFFSET_FIELD,
                increment_amount,
            );
            self.increment_value(
                later_group.entry_offset + GROUP_DATA_RWAR_OFFSET_FIELD,
                increment_amount,
            );
        }

        self.increment_value(HEADER_FILE_LENGTH_OFFSET, increment_amount);
        Ok(())
    }

    #[must_use]
    pub fn as_bytes(&self) -> &[u8] {
        &self.data
    }

    fn parse_groups(&self) -> Result<Vec<GroupDataEntry>, WmError> {
        let group_table_ref_value = self.read_u32_checked(
            self.info_section_offset + INFO_GROUP_TABLE_REF_OFFSET + REFERENCE_VALUE_OFFSET,
            "INFO.group_table reference",
        )?;
        let group_table_offset = self.info_section_offset
            + INFO_REFERENCE_BASE_BIAS
            + usize::try_from(group_table_ref_value).map_err(|_| {
                Self::parse_error(self.info_section_offset, "group table offset too large")
            })?;

        let group_count = usize::try_from(self.read_u32_checked(
            group_table_offset + GROUP_ITEM_TABLE_COUNT_FIELD,
            "group table count",
        )?)
        .map_err(|_| Self::parse_error(group_table_offset, "group count too large"))?;

        let mut groups = Vec::with_capacity(group_count);
        for group_index in 0x00..group_count {
            let group_ref_offset = group_table_offset
                + GROUP_ITEM_TABLE_ENTRIES_FIELD
                + group_index * REFERENCE_STRIDE;
            let group_entry_offset =
                self.section_reference(group_ref_offset + REFERENCE_VALUE_OFFSET);

            let group_rseq_offset = usize::try_from(self.read_u32_checked(
                group_entry_offset + GROUP_DATA_RSEQ_OFFSET_FIELD,
                "group rseq offset",
            )?)
            .map_err(|_| Self::parse_error(group_entry_offset, "group rseq offset too large"))?;

            let item_table_entry_offset = self.section_reference(
                group_entry_offset + GROUP_DATA_ITEM_TABLE_REF_FIELD + REFERENCE_VALUE_OFFSET,
            );
            let item_count = usize::try_from(self.read_u32_checked(
                item_table_entry_offset + GROUP_ITEM_TABLE_COUNT_FIELD,
                "group item count",
            )?)
            .map_err(|_| {
                Self::parse_error(item_table_entry_offset, "group item count too large")
            })?;

            let mut items = Vec::with_capacity(item_count);
            for item_index in 0x00..item_count {
                let item_ref_offset = item_table_entry_offset
                    + GROUP_ITEM_TABLE_ENTRIES_FIELD
                    + item_index * REFERENCE_STRIDE;
                let item_entry_offset =
                    self.section_reference(item_ref_offset + REFERENCE_VALUE_OFFSET);

                let item_rseq_offset = usize::try_from(self.read_u32_checked(
                    item_entry_offset + GROUP_ITEM_RSEQ_OFFSET_FIELD,
                    "item rseq offset",
                )?)
                .map_err(|_| Self::parse_error(item_entry_offset, "item rseq offset too large"))?;

                let item_rseq_size = usize::try_from(self.read_u32_checked(
                    item_entry_offset + GROUP_ITEM_RSEQ_SIZE_FIELD,
                    "item rseq size",
                )?)
                .map_err(|_| Self::parse_error(item_entry_offset, "item rseq size too large"))?;

                items.push(GroupItemEntry {
                    entry_offset: item_entry_offset,
                    rseq_offset: item_rseq_offset,
                    rseq_size: item_rseq_size,
                });
            }

            groups.push(GroupDataEntry {
                entry_offset: group_entry_offset,
                rseq_offset: group_rseq_offset,
                items,
            });
        }

        Ok(groups)
    }

    fn resolve_item(groups: &[GroupDataEntry], item: usize) -> Result<(usize, usize), WmError> {
        let mut cursor = 0x00_usize;
        for (group_index, group) in groups.iter().enumerate() {
            if item < cursor + group.items.len() {
                return Ok((group_index, item - cursor));
            }
            cursor += group.items.len();
        }

        Err(Self::parse_error(
            0x00,
            "song item index out of range for all groups",
        ))
    }

    fn read_u32_checked(&self, offset: usize, context: &str) -> Result<u32, WmError> {
        let end = offset
            .checked_add(U32_SIZE)
            .ok_or_else(|| Self::parse_error(offset, "offset arithmetic overflow"))?;
        if end > self.data.len() {
            return Err(Self::parse_error(
                offset,
                &format!("out-of-bounds read while parsing {context}"),
            ));
        }

        Ok(self.read_u32(offset))
    }

    fn parse_error(offset: usize, message: &str) -> WmError {
        WmError::Parse {
            file: "BRSAR".to_owned(),
            offset,
            message: message.to_owned(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_MAGIC_OFFSET: usize = 0x00;
    const TEST_INFO_OFFSET: usize = 0x40;
    const TEST_GROUP_TABLE_OFFSET: usize = 0x80;
    const TEST_GROUP_ENTRY_OFFSET: usize = 0xA0;
    const TEST_ITEM_TABLE_OFFSET: usize = 0xC0;
    const TEST_ITEM_ENTRY_OFFSET: usize = 0xE0;
    const TEST_SONG_OFFSET: usize = 0x140;
    const TEST_INITIAL_SONG_SIZE: usize = 0x04;

    fn write_u32_to(buf: &mut [u8], offset: usize, value: u32) {
        buf[offset..offset + U32_SIZE].copy_from_slice(&value.to_be_bytes());
    }

    fn make_synthetic_brsar() -> Vec<u8> {
        let file_size: usize = 0x200;
        let mut data = vec![0x00_u8; file_size];

        write_u32_to(&mut data, TEST_MAGIC_OFFSET, BRSAR_MAGIC);
        write_u32_to(
            &mut data,
            HEADER_FILE_LENGTH_OFFSET,
            u32::try_from(file_size).expect("synthetic file size fits u32"),
        );
        write_u32_to(
            &mut data,
            HEADER_INFO_SECTION_OFFSET,
            u32::try_from(TEST_INFO_OFFSET).expect("offset fits u32"),
        );
        write_u32_to(&mut data, HEADER_FILE_SECTION_OFFSET, 0x120_u32);

        write_u32_to(
            &mut data,
            TEST_INFO_OFFSET + INFO_GROUP_TABLE_REF_OFFSET + REFERENCE_VALUE_OFFSET,
            u32::try_from(TEST_GROUP_TABLE_OFFSET - TEST_INFO_OFFSET - INFO_REFERENCE_BASE_BIAS)
                .expect("group table ref fits u32"),
        );

        write_u32_to(
            &mut data,
            TEST_GROUP_TABLE_OFFSET + GROUP_ITEM_TABLE_COUNT_FIELD,
            0x01,
        );
        write_u32_to(
            &mut data,
            TEST_GROUP_TABLE_OFFSET + GROUP_ITEM_TABLE_ENTRIES_FIELD + REFERENCE_VALUE_OFFSET,
            u32::try_from(TEST_GROUP_ENTRY_OFFSET - TEST_INFO_OFFSET - INFO_REFERENCE_BASE_BIAS)
                .expect("group entry ref fits u32"),
        );

        write_u32_to(
            &mut data,
            TEST_GROUP_ENTRY_OFFSET + GROUP_DATA_RSEQ_OFFSET_FIELD,
            u32::try_from(TEST_SONG_OFFSET).expect("song offset fits u32"),
        );
        write_u32_to(
            &mut data,
            TEST_GROUP_ENTRY_OFFSET + GROUP_DATA_RSEQ_SIZE_FIELD,
            u32::try_from(TEST_INITIAL_SONG_SIZE).expect("song size fits u32"),
        );
        write_u32_to(
            &mut data,
            TEST_GROUP_ENTRY_OFFSET + GROUP_DATA_RWAR_OFFSET_FIELD,
            0x180_u32,
        );
        write_u32_to(
            &mut data,
            TEST_GROUP_ENTRY_OFFSET + GROUP_DATA_ITEM_TABLE_REF_FIELD + REFERENCE_VALUE_OFFSET,
            u32::try_from(TEST_ITEM_TABLE_OFFSET - TEST_INFO_OFFSET - INFO_REFERENCE_BASE_BIAS)
                .expect("item table ref fits u32"),
        );

        write_u32_to(
            &mut data,
            TEST_ITEM_TABLE_OFFSET + GROUP_ITEM_TABLE_COUNT_FIELD,
            0x01,
        );
        write_u32_to(
            &mut data,
            TEST_ITEM_TABLE_OFFSET + GROUP_ITEM_TABLE_ENTRIES_FIELD + REFERENCE_VALUE_OFFSET,
            u32::try_from(TEST_ITEM_ENTRY_OFFSET - TEST_INFO_OFFSET - INFO_REFERENCE_BASE_BIAS)
                .expect("item entry ref fits u32"),
        );

        write_u32_to(
            &mut data,
            TEST_ITEM_ENTRY_OFFSET + GROUP_ITEM_RSEQ_OFFSET_FIELD,
            0x00,
        );
        write_u32_to(
            &mut data,
            TEST_ITEM_ENTRY_OFFSET + GROUP_ITEM_RSEQ_SIZE_FIELD,
            u32::try_from(TEST_INITIAL_SONG_SIZE).expect("song size fits u32"),
        );

        data[TEST_SONG_OFFSET..TEST_SONG_OFFSET + TEST_INITIAL_SONG_SIZE]
            .copy_from_slice(&[0x11, 0x22, 0x33, 0x44]);

        data
    }

    #[test]
    fn test_read_write_u32() {
        let mut data = vec![0x00_u8; 0x20];
        let val: u32 = 0xDEAD_BEEF;
        data[0x08..0x0C].copy_from_slice(&val.to_be_bytes());
        let brsar = Brsar {
            data,
            info_section_offset: 0x00,
        };
        assert_eq!(brsar.read_u32(0x08), 0xDEAD_BEEF);
    }

    #[test]
    fn test_increment_value() {
        let mut data = vec![0x00_u8; 0x10];
        let initial: u32 = 0x0000_1000;
        data[0x04..0x08].copy_from_slice(&initial.to_be_bytes());
        let mut brsar = Brsar {
            data,
            info_section_offset: 0x00,
        };
        brsar.increment_value(0x04, 0x100);
        assert_eq!(brsar.read_u32(0x04), 0x0000_1100);
    }

    #[test]
    fn test_synthetic_round_trip_replace_song() {
        let data = make_synthetic_brsar();
        let mut brsar = Brsar::parse(data).expect("synthetic parse must succeed");

        let original = brsar.get_song(0x00).expect("song should exist");
        assert_eq!(original, vec![0x11, 0x22, 0x33, 0x44]);

        let replacement = vec![0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF];
        brsar
            .replace_song(0x00, &replacement)
            .expect("replace should succeed");

        let reparsed = Brsar::parse(brsar.as_bytes().to_vec()).expect("re-parse should succeed");
        assert_eq!(
            reparsed.get_song(0x00).expect("song should exist"),
            replacement
        );
        assert_eq!(
            reparsed.read_u32(HEADER_FILE_LENGTH_OFFSET),
            0x0000_0202,
            "file length should increase by replacement delta",
        );
        assert_eq!(
            reparsed.read_u32(TEST_GROUP_ENTRY_OFFSET + GROUP_DATA_RSEQ_SIZE_FIELD),
            0x0000_0006,
        );
        assert_eq!(
            reparsed.read_u32(TEST_ITEM_ENTRY_OFFSET + GROUP_ITEM_RSEQ_SIZE_FIELD),
            0x0000_0006,
        );
    }
}
