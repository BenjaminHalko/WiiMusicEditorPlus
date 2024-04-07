import hashlib
import logging
from pathlib import Path
from shutil import copyfile

from wii_music_editor.data.region import region_messages, RegionType, get_message_type
from wii_music_editor.data.songs import song_list
from wii_music_editor.data.styles import style_list, StyleInstruments
from wii_music_editor.editor.brsar import Brsar
from wii_music_editor.editor.dol import MainDol
from wii_music_editor.editor.message import TextClass
from wii_music_editor.editor.rom import ConvertRom
from wii_music_editor.utils.checksum import sha1checksum
from wii_music_editor.utils.preferences import preferences


def create_backup(path: Path) -> Path:
    backup_path = Path(f"{path}.backup")
    if not backup_path.exists():
        copyfile(path, backup_path)
        logging.info(f"Created backup: {backup_path}")
    return backup_path


class RomFolder:
    __mainDolHashes = [
        "a9ab9a8a8f14aa58d9bf4e05d72d29115ec589ab",
        "",
        "",
        "",
    ]
    __brsarHashes = [
        "fad7f8920eb956ba1fc1000e997d150dc28a1232",
        "",
        "",
        "",
    ]
    __messageHashes = {
        "us": "45ac82faefe600965d863a2090502c4ffc7177f5",
        "fu": "9b91ded8efa5b906f2ade135a993e9751451ccf5",
        "su": "57f0539871fe6fca5d49aa6c397e5412e01aa8d9",
        "en": "",
        "fr": "",
        "sp": "",
        "ge": "",
        "it": "",
        "jp": "",
        "kr": "",
    }

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
    region: int = -1

    def load(self, folder: str):
        logging.info(f"Loading Rom: {folder}")
        self.loaded = False
        # Set Rom Folder
        folder_path = Path(folder)
        if not folder_path.is_dir():
            try:
                folder_path = ConvertRom(folder_path)
            except Exception as e:
                logging.error(f"Could not convert rom: {e}")
                return
        self.folderPath = folder_path

        # Set Region
        for i, region in enumerate(region_messages):
            if (self.folderPath / "files" / region[0] / "Message").is_dir():
                self.region = i
                logging.info(f"Region: {region[0]}")
                break

        # Set Paths
        self.mainDolPath = self.folderPath / "sys" / "main.dol"
        self.brsarPath = self.folderPath / "files" / "Sound" / "MusicStatic" / "rp_Music_sound.brsar"

        # Create backups
        try:
            self.brsarBackupPath = create_backup(self.brsarPath)
            self.mainDolBackupPath = create_backup(self.mainDolPath)
        except Exception as e:
            logging.error(f"Error creating backups: {e}")
            return

        # Load Brsar
        try:
            self.brsar = Brsar(self.brsarPath)
            self.brsarBackup = Brsar(self.brsarBackupPath)
        except Exception as e:
            logging.error(f"Error loading brsar: {e}")
            return

        # Load Styles
        try:
            self.mainDol = MainDol(self.mainDolPath)
            self.mainDolBackup = MainDol(self.mainDolBackupPath)
            self.load_styles()
            self.load_default_styles()
        except Exception as e:
            logging.error(f"Error loading main.dol: {e}")
            return

        # Load Text
        self.load_text()
        try:
            self.load_text()
        except Exception as e:
            logging.error(f"Error loading text: {e}")
            return
        self.loaded = True

    def load_text(self):
        message_type = get_message_type(self.region, preferences.rom_language)
        logging.info(f"Loaded langauge: {message_type}")
        self.messagePath = self.folderPath / "files" / message_type / "Message"
        create_backup(self.messagePath / "message.carc")
        self.text = TextClass(self.messagePath)
        self.textBackup = TextClass(self.messagePath, "message.carc.backup")

    def load_styles(self):
        for i, style in enumerate(style_list):
            self.styles[i] = self.mainDol.get_style(style.style_id)

    def load_default_styles(self):
        for i, song in enumerate(song_list):
            if song.default_style != -1:
                self.default_styles[i] = self.mainDol.read_song_info(
                    song, self.mainDol.songSegmentDefaultStyle)

    def verify_main_dol(self) -> bool:
        mainTargetHash = self.__mainDolHashes[self.region]
        if mainTargetHash == "":
            return True
        mainHash = sha1checksum(self.mainDolBackupPath)
        return mainTargetHash == mainHash

    def verify_brsar(self) -> bool:
        brsarTargetHash = self.__brsarHashes[self.region]
        if brsarTargetHash == "":
            return True
        brsarHash = hashlib.sha1(self.brsarBackup.data).hexdigest()
        return brsarTargetHash == brsarHash

    def verify_message(self) -> bool:
        messageTargetHash = self.__messageHashes[self.messagePath.parent.stem.lower()]
        if messageTargetHash == "":
            return True
        with open(self.messagePath / "message.carc.backup", "rb") as message:
            messageHash = hashlib.sha1(message.read()).hexdigest()
        return messageTargetHash == messageHash


rom_folder = RomFolder()
