import os
import subprocess

from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.utils.osUtils import currentSystem, SystemType
from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.ui.widgets.translate import tr


def LoadDolphin(menu):
    if currentSystem != "Mac":
        if paths.dolphin is None:
            ShowError(tr("error", "Unable to launch Dolphin"),
                      tr("error", "Dolphin path not specified.\nGo to settings to add a Dolphin path"))
        else:
            try:
                cmd = [paths.dolphin, '-e', rom_folder.mainDolPath]

                if not menu:
                    cmd.insert(1, "-b")

                env = os.environ
                if currentSystem == SystemType.Windows:
                    env["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.dirname(paths.dolphin) + '/QtPlugins/platforms/'
                subprocess.Popen(cmd, env=env)
            except Exception as e:
                ShowError(self.tr("Unable to launch Dolphin"),
                          self.tr("Check the Dolphin path in the settings") + "\n" + str(e))
    else:
        ShowError(self.tr("Using Mac"),
                  self.tr("Dolphin must be run manually\n(run the main.dol located in your Wii Music folder)"),
                  self)