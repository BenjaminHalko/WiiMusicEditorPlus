from wii_music_editor.data.region import regionNames
from wii_music_editor.utils.save import load_setting, save_setting

regionSelected = load_setting("Settings", "DefaultRegion", 0)
romLanguage = []
romLanguageNumber = [load_setting("Settings", "RomLanguage", 0)] * 4


def BasedOnRegion(region_array):
    return region_array[regionSelected]


for i in range(4):
    try:
        if romLanguageNumber[i] >= len(regionNames[i]):
            romLanguageNumber[i] = 0
        romLanguage.append(regionNames[i][romLanguageNumber[i]])
    except Exception as e:
        save_setting("Settings", "RomLanguage", 0)
        romLanguageNumber[i] = 0
        romLanguage.append(regionNames[i][0])
        print(e)
