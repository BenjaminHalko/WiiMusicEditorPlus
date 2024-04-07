import logging
import os
import subprocess
from shutil import copytree

from wii_music_editor.data.region import dolphin_save_ids
from wii_music_editor.editor.rom_folder import rom_folder
from wii_music_editor.ui.confirm import ConfirmDialog
from wii_music_editor.ui.error_handler import ShowError
from wii_music_editor.ui.success import SuccessWindow
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
                logging.info("Starting Dolphin...")
                subprocess.Popen(cmd, env=env)
            except Exception as e:
                ShowError(tr("error", "Unable to launch Dolphin"),
                          tr("error", "Check the Dolphin path in the settings") + "\n" + str(e))
    else:
        ShowError(tr("error", "Using Mac"),
                  tr("error", "Dolphin must be run manually\n(run the main.dol located in your Wii Music folder)"))


def CopySaveFileToDolphin():
    if paths.dolphinSave is None:
        ShowError(tr("error", "Unable to add save file"),
                  tr("error", "Dolphin path not specified.\nGo to settings to add a Dolphin path"))
    else:
        try:
            if ConfirmDialog(tr("confirm", "Are you sure you want to overwrite your save file?")):
                logging.info("Copying save file to Dolphin")
                path = paths.dolphinSave/"title"/"00010000"/dolphin_save_ids[rom_folder.region]/"data"
                copytree(paths.includeAll/"save", path, dirs_exist_ok=True)
                SuccessWindow(tr("success", "Save file successfully added to Dolphin"))
        except Exception as e:
            ShowError(tr("error", "Unable to add save file"), str(e))

