<img src="https://user-images.githubusercontent.com/73490201/147893121-3ed1ae74-5f3e-45ca-b5d4-2d6a4285a508.png" width="700">

[![Discord](https://img.shields.io/discord/931335263509151846?color=5865F2&label=discord&logo=discord&logoColor=white)](https://discord.gg/NC3wYAeCDs)
![Current Version](https://img.shields.io/badge/dynamic/json?label=version&query=%24.0.tag_name&url=https%3A%2F%2Fapi.github.com%2Frepos%2FBenjaminHalko%2FWiiMusicEditorPlus%2Freleases)
[![Crowdin](https://badges.crowdin.net/wii-music-editor/localized.svg)](https://crowdin.com/project/wii-music-editor)

## Installation
[Download](https://www.python.org/downloads/) and install Python 3.8 or later.

## Bug Reports / Help
If you encounter any bugs or need help, please join the [Discord server](https://discord.gg/NC3wYAeCDs) and ask for help in the `#editor-help` channel.

## Development

### Requirements:

- [Rust](https://rustup.rs)

### Setup

Clone the repo

```bash
git clone -b dev-rust https://github.com/BenjaminHalko/WiiMusicEditorPlus.git
cd WiiMusicEditorPlus
```

Install the SLint viewer (optional)

```bash
cargo install slint-viewer
```

### Running the Editor

```bash
cargo run -p editor
```

### UI Development

```bash
slint-viewer crates/editor/ui/app-window.slint
```
