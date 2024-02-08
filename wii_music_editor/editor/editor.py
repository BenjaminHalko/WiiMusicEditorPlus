from wii_music_editor.data.songs import SongClass, SongType
from wii_music_editor.editor.brsar import Brsar, BrsarGroup
from wii_music_editor.editor.midi import Midi
from wii_music_editor.editor.rom_folder import RomFolder


def replace_song(rom_folder: RomFolder, song: SongClass, score_midi: Midi, song_midi: Midi, normalize: bool):
    if normalize:
        score_midi.normalize()
        if score_midi != song_midi:
            song_midi.normalize()

    brsar = Brsar(rom_folder.brsarPath)
    if song.SongType == SongType.Regular:
        brsar.replace_song(song_midi.data, BrsarGroup.Regular, song.MemOrder * 2)
        brsar.replace_song(score_midi.data, BrsarGroup.Regular, song.MemOrder * 2 + 1)
    elif song.SongType == SongType.Maestro:
        brsar.replace_song(song_midi.data, BrsarGroup.Maestro, song.MemOrder + 2)
    elif song.SongType == SongType.Hand_Bell:
        brsar.replace_song(song_midi.data, BrsarGroup.Handbell, song.MemOrder * 5 + 2)
        brsar.replace_song(song_midi.data, BrsarGroup.Handbell, song.MemOrder * 5 + 3)
        brsar.replace_song(song_midi.data, BrsarGroup.Handbell, song.MemOrder * 5 + 4)
        brsar.replace_song(song_midi.data, BrsarGroup.Handbell, song.MemOrder * 5 + 5)
        brsar.replace_song(song_midi.data, BrsarGroup.Handbell, song.MemOrder * 5 + 6)
    elif song.SongType == SongType.Menu:
        brsar.replace_song(song_midi.data, BrsarGroup.Menu, 0)
        brsar.replace_song(score_midi.data, BrsarGroup.Menu, 1)
        brsar.replace_song(score_midi.data, BrsarGroup.Menu, 2)
        brsar.replace_song(score_midi.data, BrsarGroup.Menu, 3)
        brsar.replace_song(score_midi.data, BrsarGroup.Menu, 4)
        brsar.replace_song(score_midi.data, BrsarGroup.Menu, 5)
        brsar.replace_song(score_midi.data, BrsarGroup.Menu, 6)
    brsar.save()
