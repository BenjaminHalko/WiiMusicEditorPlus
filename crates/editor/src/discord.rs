use discord_rich_presence::{DiscordIpc, DiscordIpcClient, activity::Activity};

const CLIENT_ID: &str = "931329572793540618";

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DiscordState {
    Idle,
    ModdingWiiMusic,
    SongEditor,
    StyleEditor,
    TextEditor,
    DefaultStyleEditor,
    CreatingRiivolutionPatch,
}

impl DiscordState {
    fn as_str(self) -> &'static str {
        match self {
            Self::Idle => "Idle",
            Self::ModdingWiiMusic => "ModdingWiiMusic",
            Self::SongEditor => "SongEditor",
            Self::StyleEditor => "StyleEditor",
            Self::TextEditor => "TextEditor",
            Self::DefaultStyleEditor => "DefaultStyleEditor",
            Self::CreatingRiivolutionPatch => "CreatingRiivolutionPatch",
        }
    }
}

pub struct DiscordPresence {
    rpc: Option<DiscordIpcClient>,
}

impl DiscordPresence {
    pub fn new() -> Self {
        let rpc = match DiscordIpcClient::new(CLIENT_ID) {
            Ok(mut client) => {
                if client.connect().is_ok() {
                    Some(client)
                } else {
                    None
                }
            }
            Err(_) => None,
        };

        Self { rpc }
    }

    pub fn update(&mut self, state: DiscordState) {
        if let Some(client) = self.rpc.as_mut() {
            let _ = client.set_activity(
                Activity::new()
                    .state(state.as_str())
                    .details("Wii Music Editor"),
            );
        }
    }

    pub fn disconnect(&mut self) {
        if let Some(client) = self.rpc.as_mut() {
            let _ = client.close();
        }

        self.rpc = None;
    }
}
