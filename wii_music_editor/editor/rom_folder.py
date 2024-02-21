from pathlib import Path
from shutil import copyfile

from wii_music_editor.data.region import region_messages, RegionType, get_message_type
from wii_music_editor.data.songs import song_list
from wii_music_editor.data.styles import style_list, StyleInstruments
from wii_music_editor.editor.brsar import Brsar
from wii_music_editor.editor.dol import MainDol
from wii_music_editor.editor.message import TextClass
from wii_music_editor.editor.rom import ConvertRom
from wii_music_editor.utils.preferences import preferences


def create_backup(path: Path) -> Path:
    backup_path = Path(f"{path}.backup")
    if not backup_path.exists():
        copyfile(path, backup_path)
    return backup_path


class RomFolder:
    folderPath: Path
    mainDolPath: Path
    brsarPath: Path
    messagePath: Path
    brsarBackupPath: Path
    mainDolBackupPath: Path

    loaded = False
    brsar: Brsar
    brsarBackup: Brsar
    mainDol: MainDol
    mainDolBackup: MainDol
    styles: list[StyleInstruments] = [None for _ in style_list]
    default_styles: list[int] = [0 for _ in song_list]
    text: TextClass
    textBackup: TextClass
    region: int = RegionType.US

    def load(self, folder: str):
        self.loaded = False
        # Set Rom Folder
        folder_path = Path(folder)
        if not folder_path.is_dir():
            folder_path = ConvertRom(folder_path)
            if folder_path is None:
                print("Could not convert rom")
                return
        self.folderPath = folder_path

        # Set Region
        for i, region in enumerate(region_messages):
            if (self.folderPath / "files" / region[0] / "Message").is_dir():
                self.region = i
                break

        # Set Paths
        self.mainDolPath = self.folderPath / "sys" / "main.dol"
        self.brsarPath = self.folderPath / "files" / "Sound" / "MusicStatic" / "rp_Music_sound.brsar"
        self.messagePath = self.folderPath / "files" / get_message_type(self.region, preferences.language) / "Message"

        # Create backups
        self.brsarBackupPath = create_backup(self.brsarPath)
        self.mainDolBackupPath = create_backup(self.mainDolPath)
        create_backup(self.messagePath / "message.carc")

        # Load Brsar
        self.brsar = Brsar(self.brsarPath)
        self.brsarBackup = Brsar(self.brsarBackupPath)

        # Load Styles
        self.mainDol = MainDol(self.mainDolPath)
        self.mainDolBackup = MainDol(self.mainDolBackupPath)
        self.load_styles()
        self.load_default_styles()

        # Load Text
        self.text = TextClass(self.messagePath)
        self.textBackup = TextClass(self.messagePath, "message.carc.backup")
        self.loaded = True

    def load_styles(self):
        for i, style in enumerate(style_list):
            self.styles[i] = self.mainDol.get_style(style.style_id)

    def load_default_styles(self):
        for i, song in enumerate(song_list):
            if song.default_style != -1:
                self.default_styles[i] = self.mainDol.read_song_info(
                    song, self.mainDol.songSegmentDefaultStyle)


rom_folder = RomFolder()
