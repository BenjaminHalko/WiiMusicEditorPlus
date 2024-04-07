import os
from configparser import ConfigParser
from pathlib import Path

from wii_music_editor.utils.osUtils import choose_from_os

# Save
savePath = Path(choose_from_os([
    '~/AppData/Local/WiiMusicEditorPlus',
    '~/Library/Application Support/WiiMusicEditorPlus',
    '~/.local/share/WiiMusicEditorPlus'
])).expanduser()
if not savePath.is_dir():
    os.mkdir(savePath)


def load_setting(section: str, key: str, default: str or int or bool) -> str or int or bool:
    ini = ConfigParser()
    ini.read(savePath/'settings.ini')
    if ini.has_option(section, key):
        if type(default) is not int and type(default) is not bool:
            return ini[section][key]
        else:
            if ini[section][key] == "True":
                return True
            elif ini[section][key] == "False":
                return False
            return int(ini[section][key])
    else:
        return default


def save_setting(section: str, key: str, value: str or int or bool):
    ini = ConfigParser()
    ini.read(savePath/'settings.ini')
    if not ini.has_section(section):
        ini.add_section(section)
    ini.set(section, key, str(value))
    with open(savePath/'settings.ini', 'w') as inifile:
        ini.write(inifile)
