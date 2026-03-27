use std::{
    fs,
    io::{self, copy},
    path::Path,
};

use nod::{
    common::PartitionKind,
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

    let disc = DiscReader::new(source, &DiscOptions::default()).map_err(IsoError::Open)?;
    let mut partition = disc
        .open_partition_kind(PartitionKind::Data, &PartitionOptions::default())
        .map_err(IsoError::Partition)?;
    let meta = partition.meta().map_err(IsoError::Partition)?;
    let fst = meta
        .fst()
        .map_err(|message| IsoError::Partition(nod::Error::DiscFormat(message.to_string())))?;

    let sys_dir = dest.join("sys");
    fs::create_dir_all(&sys_dir)?;
    fs::write(sys_dir.join("boot.bin"), meta.raw_boot.as_ref())?;
    fs::write(sys_dir.join("bi2.bin"), meta.raw_bi2.as_ref())?;
    fs::write(sys_dir.join("apploader.img"), meta.raw_apploader.as_ref())?;
    fs::write(sys_dir.join("main.dol"), meta.raw_dol.as_ref())?;
    fs::write(sys_dir.join("fst.bin"), meta.raw_fst.as_ref())?;

    let files_dir = dest.join("files");
    fs::create_dir_all(&files_dir)?;

    #[allow(clippy::items_after_statements)]
    const SYS_FILE_COUNT: usize = 5;
    let total_files = fst.num_files() + SYS_FILE_COUNT;
    if total_files == SYS_FILE_COUNT {
        on_progress(1.0);
        return Ok(());
    }
    on_progress(SYS_FILE_COUNT as f32 / total_files as f32);

    let mut files_done = SYS_FILE_COUNT;
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
