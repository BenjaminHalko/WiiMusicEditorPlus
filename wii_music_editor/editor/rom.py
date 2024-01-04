from pathlib import Path

from wii_music_editor.editor.gecko import CreateGct
from wii_music_editor.ui.views.error_handler.error_handler import ShowError
from wii_music_editor.utils import paths


def PatchMainDol(dol_path="", gecko_path=""):
    if dol_path == "":
        dol_path = paths.mainDolPath
        if not Path(dol_path + ".backup").exists():
            copyfile(dolPath, dol_path + ".backup")

    if gecko_path == "":
        gecko_path = paths.geckoPath

    gct = False
    if Path(gecko_path).suffix != ".gct":
        CreateGct(paths.savePath / + BasedOnRegion(gameIds) + ".gct", geckoPath)
        geckoPath = SavePath() + "/" + BasedOnRegion(gameIds) + ".gct"
        gct = True
    Run([HelperPath() + '/Wiimms/wstrt', 'patch', dolPath, '--add-section', geckoPath, '--force'])
    if (gct): os.remove(geckoPath)


def ConvertRom():
	try:
		Run([HelperPath()+'/Wiimms/wit','cp','--fst',file.path,os.path.dirname(file.path)+"/"+os.path.splitext(os.path.basename(file.path))[0]])
		if(os.path.isdir(os.path.dirname(file.path).replace('\\','/')+'/'+os.path.splitext(os.path.basename(file.path))[0]+'/DATA')):
			file.path = os.path.dirname(file.path).replace('\\','/')+'/'+os.path.splitext(os.path.basename(file.path))[0]+'/DATA'
		else:
			file.path = os.path.dirname(file.path).replace('\\','/')+'/'+os.path.splitext(os.path.basename(file.path))[0]
		file.type = LoadType.Rom
	except Exception as e:
		ShowError("Could not extract rom", str(e))





