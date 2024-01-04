from configparser import ConfigParser
from wii_music_editor.utils.helper import paths


def load_setting(section, key, default):
    ini = ConfigParser()
    ini.read(paths.savePath + '/settings.ini')
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


def save_setting(section, key, value):
    ini = ConfigParser()
    ini.read(paths.savePath + '/settings.ini')
    if not ini.has_section(section):
        ini.add_section(section)
    ini.set(section, key, str(value))
    with open(paths.savePath + '/settings.ini', 'w') as inifile:
        ini.write(inifile)
