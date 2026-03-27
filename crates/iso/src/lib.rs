use std::{
    fs,
    io::{self, copy, Read, Seek},
    path::Path,
};

use nod::{
    common::PartitionKind,
    disc::BOOT_SIZE,
    read::{DiscOptions, DiscReader, PartitionOptions},
};

#[derive(Debug, thiserror::Error)]
pub enum IsoError {
    #[error("Failed to open disc image: {0}")]
    Open(nod::Error),
    #[error("Failed to read partition: {0}")]
    Partition(nod::Error),
    #[error("Failed to extract file '{path}': {source}")]
    Extract { path: String, source: io::Error },
    #[error("I/O error: {0}")]
    Io(#[from] io::Error),
}

/// Extract all files from a Wii/GameCube disc image to `dest`.
///
/// # Errors
/// Returns `IsoError::Open` if the disc image cannot be opened.
/// Returns `IsoError::Partition` if the data partition cannot be read.
/// Returns `IsoError::Extract` if a file cannot be written to disk.
pub fn extract(source: &Path, dest: &Path) -> Result<(), IsoError> {
    extract_with_progress(source, dest, |_| {})
}

/// Extract with a progress callback receiving values from 0.0 to 1.0.
///
/// # Errors
/// Same as `extract`.
pub fn extract_with_progress(
    source: &Path,
    dest: &Path,
    on_progress: impl Fn(f32),
) -> Result<(), IsoError> {
    fs::create_dir_all(dest)?;

    let mut disc = DiscReader::new(source, &DiscOptions::default()).map_err(IsoError::Open)?;

    // --- Disc-level metadata ---
    let disc_dir = dest.join("disc");
    fs::create_dir_all(&disc_dir)?;

    let mut meta_file_count: usize = 0;

    // disc/header.bin — raw disc header from the physical disc layer.
    disc.seek(io::SeekFrom::Start(0))
        .map_err(|source| IsoError::Extract {
            path: "disc/header.bin".into(),
            source,
        })?;
    let mut header_buf = vec![0u8; BOOT_SIZE];
    disc.read_exact(&mut header_buf)
        .map_err(|source| IsoError::Extract {
            path: "disc/header.bin".into(),
            source,
        })?;
    fs::write(disc_dir.join("header.bin"), &header_buf)?;
    meta_file_count += 1;

    // disc/region.bin — Wii region data (absent on GameCube).
    if let Some(region) = disc.region() {
        fs::write(disc_dir.join("region.bin"), region)?;
        meta_file_count += 1;
    }

    // --- Partition data ---
    let mut partition = disc
        .open_partition_kind(PartitionKind::Data, &PartitionOptions::default())
        .map_err(IsoError::Partition)?;
    let meta = partition.meta().map_err(IsoError::Partition)?;
    let fst = meta
        .fst()
        .map_err(|message| IsoError::Partition(nod::Error::DiscFormat(message.to_string())))?;

    // sys/ — core partition contents.
    let sys_dir = dest.join("sys");
    fs::create_dir_all(&sys_dir)?;
    fs::write(sys_dir.join("boot.bin"), meta.raw_boot.as_ref())?;
    fs::write(sys_dir.join("bi2.bin"), meta.raw_bi2.as_ref())?;
    fs::write(sys_dir.join("apploader.img"), meta.raw_apploader.as_ref())?;
    fs::write(sys_dir.join("main.dol"), meta.raw_dol.as_ref())?;
    fs::write(sys_dir.join("fst.bin"), meta.raw_fst.as_ref())?;
    meta_file_count += 5;

    // Wii partition metadata (absent on GameCube).
    if let Some(ticket) = &meta.raw_ticket {
        fs::write(dest.join("ticket.bin"), ticket.as_ref())?;
        meta_file_count += 1;
    }
    if let Some(tmd) = &meta.raw_tmd {
        fs::write(dest.join("tmd.bin"), tmd.as_ref())?;
        meta_file_count += 1;
    }
    if let Some(cert) = &meta.raw_cert_chain {
        fs::write(dest.join("cert.bin"), cert.as_ref())?;
        meta_file_count += 1;
    }
    if let Some(h3) = &meta.raw_h3_table {
        fs::write(dest.join("h3.bin"), h3.as_ref())?;
        meta_file_count += 1;
    }

    // --- Game filesystem ---
    let files_dir = dest.join("files");
    fs::create_dir_all(&files_dir)?;

    let total_files = fst.num_files() + meta_file_count;
    if total_files == meta_file_count {
        on_progress(1.0);
        return Ok(());
    }
    on_progress(meta_file_count as f32 / total_files as f32);

    let mut files_done = meta_file_count;
    for (_, node, path) in fst.iter() {
        let target = files_dir.join(&path);
        if node.is_dir() {
            fs::create_dir_all(&target)?;
            continue;
        }

        if let Some(parent) = target.parent() {
            fs::create_dir_all(parent).map_err(|source| IsoError::Extract {
                path: path.clone(),
                source,
            })?;
        }

        let mut reader = partition
            .open_file(node)
            .map_err(|source| IsoError::Extract {
                path: path.clone(),
                source,
            })?;
        let mut file = fs::File::create(&target).map_err(|source| IsoError::Extract {
            path: path.clone(),
            source,
        })?;
        copy(&mut reader, &mut file).map_err(|source| IsoError::Extract {
            path: path.clone(),
            source,
        })?;

        files_done += 1;
        on_progress(files_done as f32 / total_files as f32);
    }

    Ok(())
}
