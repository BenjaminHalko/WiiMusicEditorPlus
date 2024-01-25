from wii_music_editor.editor.openData import LoadType, loadedFile
from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.utils.osUtils import currentSystem
from wii_music_editor.utils.paths import paths
from wii_music_editor.utils.translate import tr


def LoadDolphin(menu):
    if currentSystem != "Mac":
        if loadedFile.type != LoadType.Rom:
            ShowError(tr("error", "Unable to launch Dolphin"), tr("error", "Loaded file must be a complete rom"))
        elif paths.dolphin is None:
            ShowError(tr("error", "Unable to launch Dolphin"),
                      tr("error", "Dolphin path not specified.\nGo to settings to add a Dolphin path"))
        else:
            try:
                if (os.path.isfile(GetGeckoPath()) and load_setting("Settings", "CopyCodes", True)):
                    dir = GetDolphinSave()
                    if (os.path.isdir(dir)):
                        if (os.path.isfile(dir + "/GameSettings/" + BasedOnRegion(gameIds) + ".ini")):
                            if (
                                    not os.path.isfile(
                                        dir + "/GameSettings/" + BasedOnRegion(gameIds) + ".backup.ini")):
                                copyfile(dir + "/GameSettings/" + BasedOnRegion(gameIds) + ".ini",
                                         dir + "/GameSettings/" + BasedOnRegion(gameIds) + ".backup.ini")
                            os.remove(dir + "/GameSettings/" + BasedOnRegion(gameIds) + ".ini")
                        copyfile(GetGeckoPath(), dir + "/GameSettings/" + BasedOnRegion(gameIds) + ".ini")
                if (load_setting("Settings", "DolphinEnableCheats", True)):
                    ini = ConfigParser()
                    if (currentSystem == "Linux"):
                        config = os.path.expanduser('~/.config/dolphin-emu/')
                    else:
                        config = GetDolphinSave() + "/Config/"
                    ini.read(config + "Dolphin.ini")
                    ini.set("Core", "EnableCheats", "True")
                    with open(config + "Dolphin.ini", "w") as inifile:
                        ini.write(inifile)
                cmd = [editor.dolphinPath, '-e', editor.file.path + '/sys/main.dol']

                if (not menu): cmd.insert(1, "-b")

                env = os.environ
                if (currentSystem == "Windows"): env["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.dirname(
                    editor.dolphinPath) + '/QtPlugins/platforms/'
                subprocess.Popen(cmd, env=env)
            except Exception as e:
                ShowError(self.tr("Unable to launch Dolphin"),
                          self.tr("Check the Dolphin path in the settings") + "\n" + str(e))
    else:
        ShowError(self.tr("Using Mac"),
                  self.tr("Dolphin must be run manually\n(run the main.dol located in your Wii Music folder)"),
                  self)