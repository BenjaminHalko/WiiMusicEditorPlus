import logging

from wii_music_editor.data.songs import SongClass, SongType, song_list
from wii_music_editor.data.styles import StyleInstruments, Style
from wii_music_editor.editor.brsar import BrsarGroup
from wii_music_editor.editor.dol import MainDol
from wii_music_editor.editor.midi import Midi
from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.utils.preferences import preferences


def __replace_song(song: bytearray, group_index: int, item_index: int):
    if len(song) > 0:
        rom_folder.brsar.replace_song(song, group_index, item_index)
    else:
        song = rom_folder.brsarBackup.get_song(group_index, item_index)
        rom_folder.brsar.replace_song(song, group_index, item_index)


def replace_song(song: SongClass, score_midi: Midi, song_midi: Midi):
    logging.info(f"Replacing song: {song.name}")
    if preferences.normalize_midi:
        score_midi.normalize()
        if score_midi != song_midi:
            song_midi.normalize()

    # Patch Brsar
    if song.song_type == SongType.Regular:
        __replace_song(song_midi.data, BrsarGroup.Regular, song.mem_order * 2)
        __replace_song(score_midi.data, BrsarGroup.Regular, song.mem_order * 2 + 1)
    elif song.song_type == SongType.Maestro:
        __replace_song(song_midi.data, BrsarGroup.Maestro, song.mem_order + 2)
    elif song.song_type == SongType.Hand_Bell:
        __replace_song(song_midi.data, BrsarGroup.Handbell, song.mem_order * 5 + 2)
        __replace_song(song_midi.data, BrsarGroup.Handbell, song.mem_order * 5 + 3)
        __replace_song(song_midi.data, BrsarGroup.Handbell, song.mem_order * 5 + 4)
        __replace_song(song_midi.data, BrsarGroup.Handbell, song.mem_order * 5 + 5)
        __replace_song(song_midi.data, BrsarGroup.Handbell, song.mem_order * 5 + 6)
    elif song.song_type == SongType.Menu:
        __replace_song(song_midi.data, BrsarGroup.Menu, 0)
        __replace_song(score_midi.data, BrsarGroup.Menu, 1)
        __replace_song(score_midi.data, BrsarGroup.Menu, 2)
        __replace_song(score_midi.data, BrsarGroup.Menu, 3)
        __replace_song(score_midi.data, BrsarGroup.Menu, 4)
        __replace_song(score_midi.data, BrsarGroup.Menu, 5)
        __replace_song(score_midi.data, BrsarGroup.Menu, 6)
    rom_folder.brsar.save()

    # Patch Main Dol
    if song.song_type != SongType.Menu:
        dol = MainDol(rom_folder.mainDolPath)
        dol.write_song_info(song, score_midi.length, dol.songSegmentLength)
        dol.write_song_info(song, score_midi.tempo, dol.songSegmentTempo)
        dol.write_song_info(song, score_midi.time_signature, dol.songSegmentTimeSignature, 0x01)
        dol.save()


def replace_song_text(song: SongClass, name: str, description: str, genre: str):
    logging.info(f"Changing text for song: {song.name}")
    index = song.mem_order
    if (rom_folder.text.songs[index] != name or rom_folder.text.descriptions[index] != description or
            rom_folder.text.genres[index] != genre):
        rom_folder.text.change_name(song, [name, description, genre])


def get_original_song(song: SongClass) -> tuple[Midi, Midi, str, str, str, int, int, int]:
    # Main Dol
    length = 0
    tempo = 0
    time_signature = 4
    if song.song_type != SongType.Menu:
        dol = rom_folder.mainDolBackup
        length = dol.read_song_info(song, dol.songSegmentLength)
        tempo = dol.read_song_info(song, dol.songSegmentTempo)
        time_signature = dol.read_song_info(song, dol.songSegmentTimeSignature, 0x01)

    return (
        Midi(None),
        Midi(None),
        rom_folder.textBackup.songs[song.list_order],
        rom_folder.textBackup.descriptions[song.list_order],
        rom_folder.textBackup.genres[song.list_order],
        length,
        tempo,
        time_signature
    )


def replace_style(style: Style, instruments: StyleInstruments):
    logging.info(f"Replacing style: {style.name}")
    rom_folder.styles[style.list_order] = instruments.copy()
    rom_folder.mainDol.set_style(style.style_id, instruments)
    rom_folder.mainDol.save()


def replace_style_text(style: Style, name: str):
    logging.info(f"Changing style name: {style.name}")
    rom_folder.text.change_name(style, [name])


def replace_default_style(song: SongClass, style: Style):
    logging.info(f"Changing default style for song '{song.name}' to '{style.name}'")
    rom_folder.default_styles[song.list_order] = style.style_id
    rom_folder.mainDol.write_song_info(song, style.style_id, rom_folder.mainDol.songSegmentDefaultStyle)
    rom_folder.mainDol.save()
