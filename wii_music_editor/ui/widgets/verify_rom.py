from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.ui.warning import show_warning
from wii_music_editor.ui.widgets.translate import tr


def verify_rom_folder():
    if rom_folder.loaded:
        not_verified = []
        if not rom_folder.verify_main_dol():
            not_verified.append("main_dol")
        if not rom_folder.verify_brsar():
            not_verified.append("brsar")
        if not rom_folder.verify_message():
            not_verified.append("message")

        if not_verified:
            show_warning(tr("warning", "The following backup files have been modified:\n" +
                            ", ".join(not_verified) + "\n" +
                            "It is recommended to re-dump from the .iso."), "checksum")
