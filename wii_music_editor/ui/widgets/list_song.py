from types import NoneType

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem

from wii_music_editor.data.songs import SongType, song_list, SongClass
from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.ui.widgets.list_parent import ListParent


class SongListWidget(ListParent):
    songs: list[SongClass]

    def __init__(self, widget):
        super().__init__(widget)
        self.songs = []
        self.reset()

    def reset(self, types: list[SongType] = NoneType, only_allow: int = -1):
        super().reset()
        self.songs.clear()
        song_type_names = [
            "Regular",
            "Maestro",
            "Hand Bell",
            "Menu"
        ]
        for i, song in enumerate(song_list):
            if i == 0 or song.song_type != song_list[i - 1].song_type:
                self.addHeader(f"-------- {song_type_names[song.song_type.value]} --------")
            if types is NoneType or song.song_type in types:
                item = QListWidgetItem()
                text = song.name
                if ((len(rom_folder.text.songs) > i) and (
                        song.song_type != SongType.Regular or rom_folder.text.songs[i] != text) and (
                        song.song_type != SongType.Maestro or
                        rom_folder.text.songs[i] != text[:-14]) and (
                        song.song_type != SongType.Hand_Bell or rom_folder.text.songs[i] != text[:-19])
                        and (song.song_type != SongType.Menu)):
                    text = rom_folder.text.songs[i]
                item.setText(text)
                if only_allow != -1 and i != only_allow:
                    item.setFlags(item.flags() & Qt.ItemIsSelectable)
                self.widget.addItem(item)
                self.songs.append(song)
        if only_allow != -1:
            self.setRow(only_allow)

    def getSong(self) -> SongClass:
        return self.songs[self._getRow()]
