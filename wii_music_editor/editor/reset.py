from shutil import copyfile

from wii_music_editor.data.songs import song_list
from wii_music_editor.data.styles import style_list, StyleType
from wii_music_editor.editor.brsar import Brsar
from wii_music_editor.editor.dol import MainDol
from wii_music_editor.editor.message import TextClass
from wii_music_editor.editor.rom_folder import rom_folder


def revert_all_songs():
    copyfile(rom_folder.backup_brsarPath, rom_folder.brsarPath)
    rom_folder.brsar = Brsar(rom_folder.brsarPath)
    for song in song_list:
        length = rom_folder.mainDolBackup.read_song_info(song, rom_folder.mainDol.songSegmentLength)
        tempo = rom_folder.mainDolBackup.read(song, rom_folder.mainDol.songSegmentTempo)
        time_signature = rom_folder.mainDolBackup.read(song, rom_folder.mainDol.songSegmentTimeSignature, 0x01)
        name = rom_folder.textBackup.songs[song.mem_order]
        description = rom_folder.textBackup.descriptions[song.mem_order]
        genre = rom_folder.textBackup.genres[song.mem_order]
        rom_folder.mainDol.write_song_info(song, length, rom_folder.mainDol.songSegmentLength)
        rom_folder.mainDol.write_song_info(song, tempo, rom_folder.mainDol.songSegmentTempo)
        rom_folder.mainDol.write_song_info(song, time_signature, rom_folder.mainDol.songSegmentTimeSignature, 0x01)
        rom_folder.text.change_name(song, [name, description, genre], False)
    rom_folder.text.encode()
    rom_folder.mainDol.save()


def revert_all_styles():
    for style in style_list:
        instruments = rom_folder.mainDolBackup.get_style(style.style_id)
        if style.style_type == StyleType.Global:
            name = rom_folder.textBackup.styles[style.style_id]
            rom_folder.text.change_name(style, [name], False)
        rom_folder.styles[style.list_order] = instruments.copy()
        rom_folder.mainDol.set_style(style.style_id, instruments)
    rom_folder.text.encode()
    rom_folder.mainDol.save()
    rom_folder.load_styles()


def revert_all_default_styles():
    for song in song_list:
        if song.default_style != -1:
            style_id = rom_folder.mainDolBackup.read_song_info(song, rom_folder.mainDol.songSegmentDefaultStyle)
            rom_folder.mainDol.write_song_info(song, style_id, rom_folder.mainDol.songSegmentDefaultStyle)
    rom_folder.mainDol.save()
    rom_folder.load_default_styles()


def revert_all_text():
    copyfile(rom_folder.messagePath / "message.carc.backup", rom_folder.messagePath / "message.carc")
    rom_folder.text = TextClass(rom_folder.messagePath, "message.carc")


def revert_all():
    copyfile(rom_folder.mainDolBackupPath, rom_folder.mainDolPath)
    copyfile(rom_folder.brsarBackupPath, rom_folder.brsarPath)
    copyfile(rom_folder.messagePath / "message.carc.backup", rom_folder.messagePath / "message.carc")
    rom_folder.brsar = Brsar(rom_folder.brsarPath)
    rom_folder.mainDol = MainDol(rom_folder.mainDolPath)
    rom_folder.text = TextClass(rom_folder.messagePath, "message.carc")
    rom_folder.load_styles()
    rom_folder.load_default_styles()
