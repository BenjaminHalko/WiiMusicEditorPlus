from wii_music_editor.data.songs import SongClass, SongType, song_list
from wii_music_editor.data.styles import StyleInstruments
from wii_music_editor.editor.brsar import Brsar, BrsarGroup
from wii_music_editor.editor.dol import MainDol, MainDolOffsets, get_song_offset
from wii_music_editor.editor.message import TextClass
from wii_music_editor.editor.midi import Midi
from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.utils.preferences import preferences


def __replace_song(brsar: Brsar, backup_brsar: Brsar, song: bytearray, group_index: int, item_index: int):
    if len(song) > 0:
        brsar.replace_song(song, group_index, item_index)
    else:
        song = backup_brsar.get_song(group_index, item_index)
        brsar.replace_song(song, group_index, item_index)


def replace_song(song: SongClass, score_midi: Midi, song_midi: Midi):
    if preferences.normalize_midi:
        score_midi.normalize()
        if score_midi != song_midi:
            song_midi.normalize()

    # Patch Brsar
    brsar = Brsar(rom_folder.brsarPath)
    backup_brsar = Brsar(rom_folder.brsarBackupPath)
    if song.song_type == SongType.Regular:
        __replace_song(brsar, backup_brsar, song_midi.data, BrsarGroup.Regular, song.mem_order * 2)
        __replace_song(brsar, backup_brsar, score_midi.data, BrsarGroup.Regular, song.mem_order * 2 + 1)
    elif song.song_type == SongType.Maestro:
        __replace_song(backup_brsar, song_midi.data, BrsarGroup.Maestro, song.mem_order + 2)
    elif song.song_type == SongType.Hand_Bell:
        __replace_song(brsar, backup_brsar, song_midi.data, BrsarGroup.Handbell, song.mem_order * 5 + 2)
        __replace_song(brsar, backup_brsar, song_midi.data, BrsarGroup.Handbell, song.mem_order * 5 + 3)
        __replace_song(brsar, backup_brsar, song_midi.data, BrsarGroup.Handbell, song.mem_order * 5 + 4)
        __replace_song(brsar, backup_brsar, song_midi.data, BrsarGroup.Handbell, song.mem_order * 5 + 5)
        __replace_song(brsar, backup_brsar, song_midi.data, BrsarGroup.Handbell, song.mem_order * 5 + 6)
    elif song.song_type == SongType.Menu:
        __replace_song(brsar, backup_brsar, song_midi.data, BrsarGroup.Menu, 0)
        __replace_song(brsar, backup_brsar, score_midi.data, BrsarGroup.Menu, 1)
        __replace_song(brsar, backup_brsar, score_midi.data, BrsarGroup.Menu, 2)
        __replace_song(brsar, backup_brsar, score_midi.data, BrsarGroup.Menu, 3)
        __replace_song(brsar, backup_brsar, score_midi.data, BrsarGroup.Menu, 4)
        __replace_song(brsar, backup_brsar, score_midi.data, BrsarGroup.Menu, 5)
        __replace_song(brsar, backup_brsar, score_midi.data, BrsarGroup.Menu, 6)
    brsar.save()

    # Patch Main Dol
    if song.song_type != SongType.Menu:
        dol = MainDol(rom_folder.mainDolPath)
        offset = get_song_offset(song)
        dol.write(score_midi.length, offset + MainDolOffsets.songSegmentLength)
        dol.write(score_midi.tempo, offset + MainDolOffsets.songSegmentTempo)
        dol.write(score_midi.time_signature, offset + MainDolOffsets.songSegmentTimeSignature, 0x01)
        dol.save()


def replace_song_text(index: int, name: str, description: str, genre: str):
    if (rom_folder.text.songs[index] != name or rom_folder.text.descriptions[index] != description or
            rom_folder.text.genres[index] != genre):
        rom_folder.text.change_name(index, [name, description, genre])


def replace_style(index: int, style: StyleInstruments):
    rom_folder.mainDol.set_style(index, style)
    rom_folder.mainDol.save()


def replace_style_text(index: int, name: str):
    rom_folder.text.change_name(index, [name])


def get_original_song(index: int) -> tuple[Midi, Midi, str, str, str, int, int, int]:
    song = song_list[index]
    text = TextClass(rom_folder.messagePath, "message.carc.backup")

    # Main Dol
    length = 0
    tempo = 0
    time_signature = 4
    if song.song_type != SongType.Menu:
        dol = MainDol(rom_folder.mainDolBackupPath)
        dolOffset = get_song_offset(song)
        length = dol.read(dolOffset + MainDolOffsets.songSegmentLength)
        tempo = dol.read(dolOffset + MainDolOffsets.songSegmentTempo)
        time_signature = dol.read(dolOffset + MainDolOffsets.songSegmentTimeSignature, 0x01)

    return (
        Midi(None),
        Midi(None),
        text.songs[index],
        text.descriptions[index],
        text.genres[index],
        length,
        tempo,
        time_signature
    )
