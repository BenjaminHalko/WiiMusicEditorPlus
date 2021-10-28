from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QDialog
from settings_ui import Ui_Settings
from editor import ProgramPath

def LoadSetting(section,key,default):
	global ProgramPath
	ini = configparser.ConfigParser()
	ini.read(ProgramPath+'/settings.ini')
	if(ini.has_option(section, key)):
		if(type(default) == str):
			return ini[section][key]
		else:
			return int(ini[section][key])
	else:
		return default

def SaveSetting(section,key,value):
	global ProgramPath
	ini = configparser.ConfigParser()
	ini.read(ProgramPath+'/settings.ini')
	if(not ini.has_section(section)):
		ini.add_section(section)
	ini.set(section,key,str(value))
	with open(ProgramPath+'/settings.ini', 'w') as inifile:
		ini.write(inifile)

regionSelected = LoadSetting("Settings","DefaultRegion",0)

class SettingsWindow(QDialog,Ui_Settings):
    def __init__(self):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.setWindowModality(Qt.ApplicationModal)
        self.setupUi(self)

        self.RegionBox.setCurrentIndex(editor.regionSelected)
        self.RegionBox.currentIndexChanged.connect(self.RegionChange)

        self.show()
        self.exec()

    def RegionChange(self):
        editor.regionSelected = self.RegionBox.currentIndex()
        SaveSetting("Settings","DefaultRegion",editor.regionSelected)