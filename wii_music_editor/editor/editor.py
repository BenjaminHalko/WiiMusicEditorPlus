from wii_music_editor.data.songs import SongClass, SongType
from wii_music_editor.editor.brsar import Brsar, BrsarGroup
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

    # Apply Gecko Patches
    patches = []
    if preferences.rapper_crash_fix:
        patches.append(Patch('Rapper Crash Fix', rapperPatches[rom_folder.region]))
    if song.SongType != SongType.Menu:
        gct_offset = gctRegionOffsets[rom_folder.region]
        length_hex = format(score_midi.length, 'x').zfill(8)
        tempo_hex = format(score_midi.tempo, 'x').zfill(8)
        length_code = f'0{format(song.MemOffset+gct_offset+6, "x")} {length_hex}\n'
        tempo_code = f'0{format(song.MemOffset+gct_offset+10, "x")} {tempo_hex}\n'


def replace_song_text(index: int, name: str, description: str, genre: str):
    if (rom_folder.text.songs[index] != name or rom_folder.text.descriptions[index] != description or
            rom_folder.text.genres[index] != genre):
        rom_folder.text.change_name(index, [name, description, genre])
