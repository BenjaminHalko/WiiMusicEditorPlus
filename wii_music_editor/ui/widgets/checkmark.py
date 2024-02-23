from wii_music_editor.utils.save import save_setting


def Checkmark(checkmark, category, setting):
    save_setting(category, setting, (checkmark.checkState() == 2))
