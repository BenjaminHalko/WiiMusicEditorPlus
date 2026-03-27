mod brsar;
mod rseq;

pub use brsar::Brsar;
pub use rseq::Rseq;

#[derive(Debug, thiserror::Error)]
pub enum BrsarError {
    #[error("BRSAR parse error at offset {offset:#x}: {message}")]
    Parse { offset: usize, message: String },
    #[error("RSEQ encode error: {0}")]
    Encode(String),
    #[error("RSEQ decode error: {0}")]
    Decode(String),
    #[error("MIDI error: {0}")]
    Midi(String),
}
