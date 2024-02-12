from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QListWidget, QListWidgetItem

from wii_music_editor.data.instruments import instrumentList
from wii_music_editor.data.songs import song_list, SongType
from wii_music_editor.data.styles import styleList
from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.utils.preferences import preferences
from wii_music_editor.utils.translate import tr


def populate_song_list(widget: QListWidget, types: list[SongType] or None = None, only_allow: int = -1):
    widget.clear()
    for i, song in enumerate(song_list):
        if types is None or song.SongType in types:
            item = QListWidgetItem()
            text = song.Name
            if ((len(rom_folder.text.songs) > i) and (
                    song.SongType != SongType.Regular or rom_folder.text.songs[i] != song.Name) and (
                    song.SongType != SongType.Maestro or
                    rom_folder.text.songs[i] != song.Name[:len(song.Name) - 14]) and (
                    song.SongType != SongType.Hand_Bell or rom_folder.text.songs[i] != song.Name[:len(song.Name) - 19])
                    and (song.SongType != SongType.Menu)):
                text = rom_folder.text.songs[i]
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


def populate_style_list(widget: QListWidget, only_allow: int = -1):
    widget.clear()
    for i, style in enumerate(styleList):
        item = QListWidgetItem()
        extraText = ""
        if rom_folder.styles[i] != style.style:
            extraText = f" ~[{tr('ui', 'Replaced')}]~"
        if (len(rom_folder.text.styles) > i):
            item.setText(rom_folder.text.styles[i] + extraText)
        else:
            item.setText(style.name + extraText)
        if only_allow != -1 and i != only_allow:
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        widget.addItem(item)
    if only_allow != -1:
        widget.setCurrentRow(only_allow)


def populate_instrument_list(widget: QListWidget, percussion: bool = False, menu: bool = False):
    widget.clear()
    if not percussion:
        instruments = instrumentList[:40]
    else:
        instruments = instrumentList[40:-1]
    normalRange = instruments
    if preferences.unsafe_mode or not percussion:
        instruments = instrumentList

    for i, inst in enumerate(instruments):
        item = QListWidgetItem()
        item.setText(inst.Name)
        if menu and not inst.InMenu:
            if preferences.unsafeMode:
                item.setForeground(QColor("#cf1800"))
            else:
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        if i not in normalRange:
            item.setForeground(QColor("#cf1800"))
        widget.addItem(item)

    item = QListWidgetItem()
    item.setText(instrumentList[-1].Name)
    if menu:
        if preferences.unsafeMode:
            item.setForeground(QColor("#cf1800"))
        else:
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
    widget.addItem(item)
