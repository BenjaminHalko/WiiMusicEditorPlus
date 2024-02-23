from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.ui.warning import show_warning
from wii_music_editor.ui.widgets.translate import tr


def verify_rom_folder():
    if not rom_folder.verify_main_dol():
        show_warning(tr("warning", "The main.dol backup has a different checksum than the original." +
                        "It is recommended to re-dump from the .iso."), "checksum")
    if not rom_folder.verify_brsar():
        show_warning(tr("warning", "The brsar backup has a different checksum than the original." +
                        "It is recommended to re-dump from the .iso."), "checksum")
    if not rom_folder.verify_message():
        show_warning(tr("warning", "The message backup has a different checksum than the original." +
                        "It is recommended to re-dump from the .iso."), "checksum")
