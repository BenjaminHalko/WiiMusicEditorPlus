from pathlib import Path
from shutil import copyfile

from wii_music_editor.editor.gecko import CreateGct
from wii_music_editor.editor.region import BasedOnRegion
from wii_music_editor.utils.paths import paths


def PatchMainDol(dol_path="", gecko_path=""):
    if dol_path == "":
        dol_path = str(paths.mainDolPath)
        if not Path(dol_path + ".backup").exists():
            copyfile(dol_path, dol_path + ".backup")

    if gecko_path == "":
        gecko_path = str(paths.geckoPath)

    gct = False
    if Path(gecko_path).suffix != ".gct":
        CreateGct(paths.savepath / BasedOnRegion(gameIds) + ".gct", gecko_path)
        gecko_path = SavePath() + "/" + BasedOnRegion(gameIds) + ".gct"
        gct = True
    Run([HelperPath() + '/Wiimms/wstrt', 'patch', dolPath, '--add-section', geckoPath, '--force'])
    if (gct): os.remove(geckoPath)