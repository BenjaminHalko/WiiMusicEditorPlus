use indexmap::IndexMap;

use crate::SzsError;

const YAZ0_MAGIC: u32 = 0x5961_7A30;
const U8_MAGIC: u32 = 0x55AA_382D;
const U8_ALIGN: usize = 0x20;

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Carc {
    files: IndexMap<String, Vec<u8>>,
}

impl Carc {
    /// Parses a CARC/U8 archive image.
    ///
    /// # Errors
    /// Returns `SzsError::InvalidMagic` for an unexpected header, `SzsError::InvalidU8`
    /// for truncated input, and `SzsError::Compression` if Yaz0 decoding fails.
    pub fn from_bytes(data: &[u8]) -> Result<Self, SzsError> {
        let magic = read_u32_at(data, 0)
            .ok_or_else(|| SzsError::InvalidU8("Archive shorter than 4 bytes".to_string()))?;

        let raw = match magic {
            YAZ0_MAGIC => szs::decode(data).map_err(|e| SzsError::Compression(e.to_string()))?,
            U8_MAGIC => data.to_vec(),
            other => return Err(SzsError::InvalidMagic(other)),
        };

        let files = parse_u8_archive(&raw)?;
        Ok(Self { files })
    }

    /// Serializes the archive back to bytes.
    ///
    /// # Errors
    /// Returns `SzsError::Compression` if Yaz0 encoding fails or
    /// `SzsError::InvalidU8` if the archive structure is invalid.
    pub fn to_bytes(&self) -> Result<Vec<u8>, SzsError> {
        let raw = serialize_u8_archive(&self.files)?;
        szs::encode(&raw, szs::EncodeAlgo::MKW).map_err(|e| SzsError::Compression(e.to_string()))
    }

    #[must_use]
    pub fn get(&self, name: &str) -> Option<&[u8]> {
        self.files.get(name).map(Vec::as_slice)
    }

    pub fn insert(&mut self, name: String, data: Vec<u8>) {
        self.files.insert(name, data);
    }

    pub fn files(&self) -> impl Iterator<Item = (&str, &[u8])> {
        self.files
            .iter()
            .map(|(name, data)| (name.as_str(), data.as_slice()))
    }
}

#[derive(Clone, Debug)]
struct U8Node {
    is_dir: bool,
    name_off: usize,
    offset: u32,
    size: u32,
}

#[derive(Clone, Debug)]
struct U8NodeBuilder {
    is_dir: bool,
    name: String,
    offset: u32,
    size: u32,
    file_data: Option<Vec<u8>>,
}

#[derive(Default)]
struct DirBuild {
    dirs: IndexMap<String, DirBuild>,
    files: IndexMap<String, Vec<u8>>,
    order: Vec<DirChild>,
}

#[derive(Clone)]
enum DirChild {
    Dir(String),
    File(String),
}

fn parse_u8_archive(data: &[u8]) -> Result<IndexMap<String, Vec<u8>>, SzsError> {
    if data.len() < 0x20 {
        return Err(SzsError::InvalidU8(
            "U8 archive shorter than header".to_string(),
        ));
    }

    let magic =
        read_u32_at(data, 0).ok_or_else(|| SzsError::InvalidU8("U8 missing magic".to_string()))?;
    if magic != U8_MAGIC {
        return Err(SzsError::InvalidMagic(magic));
    }

    let node_off = read_u32_at(data, 0x04)
        .ok_or_else(|| SzsError::InvalidU8("U8 missing node offset".to_string()))?;
    let fst_size = read_u32_at(data, 0x08)
        .ok_or_else(|| SzsError::InvalidU8("U8 missing FST size".to_string()))?;

    let node_off = usize::try_from(node_off)
        .map_err(|_| SzsError::InvalidU8("U8 node offset too large".to_string()))?;
    let fst_size = usize::try_from(fst_size)
        .map_err(|_| SzsError::InvalidU8("U8 FST size too large".to_string()))?;

    let fst_end = node_off
        .checked_add(fst_size)
        .ok_or_else(|| SzsError::InvalidU8("U8 FST end overflow".to_string()))?;
    if fst_end > data.len() {
        return Err(SzsError::InvalidU8("U8 FST exceeds input".to_string()));
    }
    if node_off.checked_add(12).is_none_or(|v| v > fst_end) {
        return Err(SzsError::InvalidU8("U8 missing root node".to_string()));
    }

    let root = parse_u8_node(data, node_off)?;
    if !root.is_dir {
        return Err(SzsError::InvalidU8(
            "U8 root node is not a directory".to_string(),
        ));
    }

    let node_count = usize::try_from(root.size)
        .map_err(|_| SzsError::InvalidU8("U8 node count too large".to_string()))?;
    if node_count == 0 {
        return Err(SzsError::InvalidU8("U8 node count is zero".to_string()));
    }

    let node_bytes = node_count
        .checked_mul(12)
        .ok_or_else(|| SzsError::InvalidU8("U8 node table size overflow".to_string()))?;
    let string_start = node_off
        .checked_add(node_bytes)
        .ok_or_else(|| SzsError::InvalidU8("U8 string table start overflow".to_string()))?;
    if string_start > fst_end {
        return Err(SzsError::InvalidU8(
            "U8 string table start beyond FST".to_string(),
        ));
    }

    let mut nodes = Vec::with_capacity(node_count);
    for index in 0..node_count {
        let off = node_off + index * 12;
        if off + 12 > fst_end {
            return Err(SzsError::InvalidU8("U8 node table truncated".to_string()));
        }
        nodes.push(parse_u8_node(data, off)?);
    }

    let mut files = IndexMap::new();
    collect_u8_files(data, &nodes, string_start, fst_end, 0, "", &mut files)?;

    Ok(files)
}

fn collect_u8_files(
    source: &[u8],
    nodes: &[U8Node],
    string_start: usize,
    string_end: usize,
    dir_index: usize,
    prefix: &str,
    out: &mut IndexMap<String, Vec<u8>>,
) -> Result<(), SzsError> {
    let dir = nodes
        .get(dir_index)
        .ok_or_else(|| SzsError::InvalidU8("Directory node index out of range".to_string()))?;
    if !dir.is_dir {
        return Err(SzsError::InvalidU8("Expected directory node".to_string()));
    }

    let end = usize::try_from(dir.size)
        .map_err(|_| SzsError::InvalidU8("Directory end index too large".to_string()))?;
    if end > nodes.len() || end <= dir_index {
        return Err(SzsError::InvalidU8("Invalid directory range".to_string()));
    }

    let mut index = dir_index + 1;
    while index < end {
        let node = &nodes[index];
        let name = read_u8_name(source, string_start, string_end, node.name_off)?;
        let path = if prefix.is_empty() {
            name.to_string()
        } else {
            format!("{prefix}/{name}")
        };

        if node.is_dir {
            let next = usize::try_from(node.size)
                .map_err(|_| SzsError::InvalidU8("Directory next index too large".to_string()))?;
            if next <= index || next > end {
                return Err(SzsError::InvalidU8(
                    "Invalid directory subtree bounds".to_string(),
                ));
            }

            collect_u8_files(source, nodes, string_start, string_end, index, &path, out)?;
            index = next;
        } else {
            let data_off = usize::try_from(node.offset)
                .map_err(|_| SzsError::InvalidU8("File offset too large".to_string()))?;
            let data_size = usize::try_from(node.size)
                .map_err(|_| SzsError::InvalidU8("File size too large".to_string()))?;
            let data_end = data_off
                .checked_add(data_size)
                .ok_or_else(|| SzsError::InvalidU8("File end overflow".to_string()))?;
            if data_end > source.len() {
                return Err(SzsError::InvalidU8(format!(
                    "File '{path}' extends beyond archive"
                )));
            }

            out.insert(path, source[data_off..data_end].to_vec());
            index += 1;
        }
    }

    Ok(())
}

fn parse_u8_node(data: &[u8], offset: usize) -> Result<U8Node, SzsError> {
    let type_name = read_u32_at(data, offset)
        .ok_or_else(|| SzsError::InvalidU8("Node missing type/name".to_string()))?;
    let node_type = (type_name >> 24) as u8;
    let name_off = (type_name & 0x00FF_FFFF) as usize;

    let offset_field = read_u32_at(data, offset + 4)
        .ok_or_else(|| SzsError::InvalidU8("Node missing offset".to_string()))?;
    let size_field = read_u32_at(data, offset + 8)
        .ok_or_else(|| SzsError::InvalidU8("Node missing size".to_string()))?;

    match node_type {
        0 | 1 => Ok(U8Node {
            is_dir: node_type == 1,
            name_off,
            offset: offset_field,
            size: size_field,
        }),
        _ => Err(SzsError::InvalidU8(format!(
            "Invalid node type: {node_type}"
        ))),
    }
}

fn read_u8_name(
    data: &[u8],
    string_start: usize,
    string_end: usize,
    name_off: usize,
) -> Result<&str, SzsError> {
    let start = string_start
        .checked_add(name_off)
        .ok_or_else(|| SzsError::InvalidU8("String offset overflow".to_string()))?;
    if start >= string_end {
        return Err(SzsError::InvalidU8(
            "String offset out of range".to_string(),
        ));
    }

    let rel_end = data[start..string_end]
        .iter()
        .position(|&byte| byte == 0)
        .ok_or_else(|| SzsError::InvalidU8("Missing string terminator".to_string()))?;
    std::str::from_utf8(&data[start..start + rel_end])
        .map_err(|_| SzsError::InvalidU8("Invalid UTF-8 path name".to_string()))
}

fn serialize_u8_archive(files: &IndexMap<String, Vec<u8>>) -> Result<Vec<u8>, SzsError> {
    let mut root = DirBuild::default();
    for (path, data) in files {
        insert_path(&mut root, path, data.clone())?;
    }

    let mut nodes = Vec::new();
    emit_dir_nodes(&root, "", 0, &mut nodes)?;

    let mut string_table = vec![0_u8];
    let mut name_offsets = Vec::with_capacity(nodes.len());
    for (index, node) in nodes.iter().enumerate() {
        if index == 0 {
            name_offsets.push(0_u32);
            continue;
        }

        let name_off = u32::try_from(string_table.len())
            .map_err(|_| SzsError::InvalidU8("String table too large".to_string()))?;
        name_offsets.push(name_off);
        string_table.extend_from_slice(node.name.as_bytes());
        string_table.push(0);
    }

    let node_table_size = nodes
        .len()
        .checked_mul(12)
        .ok_or_else(|| SzsError::InvalidU8("Node table size overflow".to_string()))?;
    let fst_size = node_table_size
        .checked_add(string_table.len())
        .ok_or_else(|| SzsError::InvalidU8("FST size overflow".to_string()))?;

    let header_size = 0x20_usize;
    let data_off = align_up(
        header_size
            .checked_add(fst_size)
            .ok_or_else(|| SzsError::InvalidU8("Data offset overflow".to_string()))?,
        U8_ALIGN,
    );

    let mut running_data_off = data_off;
    for node in &mut nodes {
        if let Some(file_data) = &node.file_data {
            running_data_off = align_up(running_data_off, U8_ALIGN);
            node.offset = u32::try_from(running_data_off)
                .map_err(|_| SzsError::InvalidU8("File offset exceeds u32".to_string()))?;
            node.size = u32::try_from(file_data.len())
                .map_err(|_| SzsError::InvalidU8("File size exceeds u32".to_string()))?;
            running_data_off = running_data_off
                .checked_add(file_data.len())
                .ok_or_else(|| SzsError::InvalidU8("Archive data size overflow".to_string()))?;
        }
    }

    let mut out = vec![0_u8; data_off];

    out[0..4].copy_from_slice(&U8_MAGIC.to_be_bytes());
    out[4..8].copy_from_slice(&(0x20_u32).to_be_bytes());
    out[8..12].copy_from_slice(
        &u32::try_from(fst_size)
            .map_err(|_| SzsError::InvalidU8("FST size exceeds u32".to_string()))?
            .to_be_bytes(),
    );
    out[12..16].copy_from_slice(
        &u32::try_from(data_off)
            .map_err(|_| SzsError::InvalidU8("Data offset exceeds u32".to_string()))?
            .to_be_bytes(),
    );

    let nodes_start = 0x20;
    for (index, node) in nodes.iter().enumerate() {
        let node_off = nodes_start + index * 12;
        let node_type = u32::from(node.is_dir);
        let type_name = (node_type << 24) | (name_offsets[index] & 0x00FF_FFFF);
        out[node_off..node_off + 4].copy_from_slice(&type_name.to_be_bytes());
        out[node_off + 4..node_off + 8].copy_from_slice(&node.offset.to_be_bytes());
        out[node_off + 8..node_off + 12].copy_from_slice(&node.size.to_be_bytes());
    }

    let strings_start = nodes_start + node_table_size;
    out[strings_start..strings_start + string_table.len()].copy_from_slice(&string_table);

    for node in &nodes {
        if let Some(file_data) = &node.file_data {
            let start = usize::try_from(node.offset)
                .map_err(|_| SzsError::InvalidU8("Serialized file offset too large".to_string()))?;
            let end = start
                .checked_add(file_data.len())
                .ok_or_else(|| SzsError::InvalidU8("Serialized file end overflow".to_string()))?;
            if out.len() < end {
                out.resize(end, 0);
            }
            out[start..end].copy_from_slice(file_data);
        }
    }

    Ok(out)
}

fn insert_path(root: &mut DirBuild, path: &str, data: Vec<u8>) -> Result<(), SzsError> {
    let parts: Vec<&str> = path.split('/').filter(|part| !part.is_empty()).collect();
    if parts.is_empty() {
        return Err(SzsError::InvalidU8("Empty file path".to_string()));
    }

    let (dirs, file_name) = parts.split_at(parts.len() - 1);
    let mut cur = root;
    for seg in dirs {
        let seg = (*seg).to_string();
        if !cur.dirs.contains_key(&seg) {
            cur.order.push(DirChild::Dir(seg.clone()));
            cur.dirs.insert(seg.clone(), DirBuild::default());
        }
        cur = cur
            .dirs
            .get_mut(&seg)
            .ok_or_else(|| SzsError::InvalidU8("Missing directory after insertion".to_string()))?;
    }

    let file_name = file_name[0].to_string();
    if !cur.files.contains_key(&file_name) {
        cur.order.push(DirChild::File(file_name.clone()));
    }
    cur.files.insert(file_name, data);
    Ok(())
}

fn emit_dir_nodes(
    dir: &DirBuild,
    name: &str,
    parent_index: u32,
    out: &mut Vec<U8NodeBuilder>,
) -> Result<u32, SzsError> {
    let index = u32::try_from(out.len())
        .map_err(|_| SzsError::InvalidU8("Too many U8 nodes".to_string()))?;
    out.push(U8NodeBuilder {
        is_dir: true,
        name: name.to_string(),
        offset: parent_index,
        size: 0,
        file_data: None,
    });

    for child in &dir.order {
        match child {
            DirChild::Dir(child_name) => {
                let child_dir = dir.dirs.get(child_name).ok_or_else(|| {
                    SzsError::InvalidU8(format!("Missing child dir '{child_name}' in order list"))
                })?;
                emit_dir_nodes(child_dir, child_name, index, out)?;
            }
            DirChild::File(file_name) => {
                let file_data = dir.files.get(file_name).ok_or_else(|| {
                    SzsError::InvalidU8(format!("Missing file '{file_name}' in order list"))
                })?;
                out.push(U8NodeBuilder {
                    is_dir: false,
                    name: file_name.clone(),
                    offset: 0,
                    size: 0,
                    file_data: Some(file_data.clone()),
                });
            }
        }
    }

    let end = u32::try_from(out.len())
        .map_err(|_| SzsError::InvalidU8("Too many U8 nodes".to_string()))?;
    out[index as usize].size = end;
    Ok(end)
}

pub(crate) const fn align_up(value: usize, align: usize) -> usize {
    let mask = align - 1;
    (value + mask) & !mask
}

pub(crate) fn read_u16_at(data: &[u8], offset: usize) -> Option<u16> {
    let bytes = data.get(offset..offset + 2)?;
    Some(u16::from_be_bytes([bytes[0], bytes[1]]))
}

pub(crate) fn read_u32_at(data: &[u8], offset: usize) -> Option<u32> {
    let bytes = data.get(offset..offset + 4)?;
    Some(u32::from_be_bytes([bytes[0], bytes[1], bytes[2], bytes[3]]))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn carc_round_trip_and_modify() {
        let mut files = IndexMap::new();
        files.insert("new_music_message.bmg".to_string(), vec![1, 2, 3]);
        files.insert("sub/other.bin".to_string(), vec![4, 5, 6, 7]);

        let archive = serialize_u8_archive(&files).expect("serialize raw u8");
        let compressed = szs::encode(&archive, szs::EncodeAlgo::MKW).expect("encode yaz0");

        let mut carc = Carc::from_bytes(&compressed).expect("decode carc");
        assert_eq!(carc.get("new_music_message.bmg"), Some(&[1, 2, 3][..]));
        assert_eq!(carc.get("sub/other.bin"), Some(&[4, 5, 6, 7][..]));

        carc.insert("sub/other.bin".to_string(), vec![9, 9]);

        let out = carc.to_bytes().expect("re-encode carc");
        let reparsed = Carc::from_bytes(&out).expect("reparse carc");
        assert_eq!(reparsed.get("sub/other.bin"), Some(&[9, 9][..]));
    }

    #[test]
    fn carc_invalid_magic() {
        let err = Carc::from_bytes(b"NOTU8").expect_err("must reject bad magic");
        assert!(matches!(err, SzsError::InvalidMagic(_)));
    }
}
