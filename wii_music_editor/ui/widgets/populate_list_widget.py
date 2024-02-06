from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem

from wii_music_editor.data.songs import songList, SongType
from wii_music_editor.utils.translate import tr


def populate_song_list(widget: QListWidget, types: list[SongType] or None = None, only_allow: int = -1):
    widget.clear()
    for i, song in enumerate(songList):
        if types is None or song.SongType in types:
            item = QListWidgetItem()
            text = song.Name
            if (AllowType(LoadType.Carc) and len(editor.textFromTxt[0]) > i) and (
                    song.SongType != SongType.Regular or editor.textFromTxt[0][i] != Songs[i].Name) and (
                    song.SongType != SongType.Maestro or editor.textFromTxt[0][i] != Songs[i].Name[0:len(
                Songs[i].Name) - 14:1]) and (
                    Songs[i].SongType != SongTypeValue.Handbell or editor.textFromTxt[0][i] != Songs[i].Name[0:len(
                Songs[i].Name) - 19:1]) and (Songs[i].SongType != SongTypeValue.Menu):
                text = editor.textFromTxt[0][i]
                if song.SongType == SongType.Maestro:
                    text = f"{text} ({tr('ui', 'Mii Maestro')})"
                if song.SongType == SongType.Hand_Bell:
                    text = f"{text} ({tr('ui', 'Mii Maestro')})"
            item.setText(text)
            if only_allow != -1 and i != only_allow:
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            widget.addItem(item)
    if only_allow != -1:
        widget.setCurrentRow(only_allow)
