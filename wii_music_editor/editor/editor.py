from wii_music_editor.data.songs import SongClass, SongType
from wii_music_editor.editor.brsar import Brsar, BrsarGroup
from wii_music_editor.editor.dol import MainDol, MainDolOffsets
from wii_music_editor.editor.gecko import rapperPatches, AddPatch, Patch, gctRegionOffsets
from wii_music_editor.editor.midi import Midi
from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.utils.preferences import preferences


def replace_song(song: SongClass, score_midi: Midi, song_midi: Midi):
    if preferences.normalize_midi:
        score_midi.normalize()
        if score_midi != song_midi:
            song_midi.normalize()

    # Patch Brsar
    brsar = Brsar(rom_folder.brsarPath)
    if song.song_type == SongType.Regular:
        brsar.replace_song(song_midi.data, BrsarGroup.Regular, song.mem_order * 2)
        brsar.replace_song(score_midi.data, BrsarGroup.Regular, song.mem_order * 2 + 1)
    elif song.song_type == SongType.Maestro:
        brsar.replace_song(song_midi.data, BrsarGroup.Maestro, song.mem_order + 2)
    elif song.song_type == SongType.Hand_Bell:
        brsar.replace_song(song_midi.data, BrsarGroup.Handbell, song.mem_order * 5 + 2)
        brsar.replace_song(song_midi.data, BrsarGroup.Handbell, song.mem_order * 5 + 3)
        brsar.replace_song(song_midi.data, BrsarGroup.Handbell, song.mem_order * 5 + 4)
        brsar.replace_song(song_midi.data, BrsarGroup.Handbell, song.mem_order * 5 + 5)
        brsar.replace_song(song_midi.data, BrsarGroup.Handbell, song.mem_order * 5 + 6)
    elif song.song_type == SongType.Menu:
        brsar.replace_song(song_midi.data, BrsarGroup.Menu, 0)
        brsar.replace_song(score_midi.data, BrsarGroup.Menu, 1)
        brsar.replace_song(score_midi.data, BrsarGroup.Menu, 2)
        brsar.replace_song(score_midi.data, BrsarGroup.Menu, 3)
        brsar.replace_song(score_midi.data, BrsarGroup.Menu, 4)
        brsar.replace_song(score_midi.data, BrsarGroup.Menu, 5)
        brsar.replace_song(score_midi.data, BrsarGroup.Menu, 6)
    brsar.save()

    # Patch Main Dol
    if song.song_type != SongType.Menu:
        offset = MainDolOffsets.songSegmentRegularOffset
        if song.song_type == SongType.Maestro:
            offset = MainDolOffsets.songSegmentMaestroOffset
        elif song.song_type == SongType.Hand_Bell:
            offset = MainDolOffsets.songSegmentHandBellOffset
        elif song.song_type == SongType.Menu:
            offset = MainDolOffsets.songSegmentMenuOffset
        offset += song.mem_order * MainDolOffsets.songSegmentSize

        dol = MainDol(rom_folder.mainDolPath)
        dol.write(score_midi.length, offset + MainDolOffsets.songSegmentLength)
        dol.write(score_midi.tempo, offset + MainDolOffsets.songSegmentTempo)
        dol.write(score_midi.time_signature, offset + MainDolOffsets.songSegmentTimeSignature, 0x01)
        dol.save()


def replace_song_text(index: int, name: str, description: str, genre: str):
    if (rom_folder.text.songs[index] != name or rom_folder.text.descriptions[index] != description or
            rom_folder.text.genres[index] != genre):
        rom_folder.text.change_name(index, [name, description, genre])


def replace_style(index: int, style: list[int]):
    main_dol = MainDol(rom_folder.mainDolPath)
    main_dol.remove_style_execution()
    main_dol.set_style(index, style)
    main_dol.save()


def replace_style_text(index: int, name: str):
    rom_folder.text.change_name(index, [name])
