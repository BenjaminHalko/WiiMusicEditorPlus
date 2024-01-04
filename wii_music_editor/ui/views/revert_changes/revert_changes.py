from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog

from wii_music_editor.ui.views.revert_changes.revert_changes_ui import Ui_Revert


class RevertChangesWindow(QDialog ,Ui_Revert):
    def __init__(self):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint,False)
        self.setupUi(self)

        self.SelectButton.clicked.connect(lambda: self.SelectAll(True))
        self.DeselectButton.clicked.connect(lambda: self.SelectAll(False))
        self.PatchButton.clicked.connect(self.Revert)

        self.show()
        self.exec()

    def SelectAll(self ,select):
        self.Songs.setChecked(select)
        self.Styles.setChecked(select)
        self.Text.setChecked(select)
        self.MainDol.setChecked(select)

    def Revert(self):
        sections = []
        if(path.isfile(editor.file.path +"/Changes.ini") and LoadSetting("Settings" ,"RemoveChangesFromChangesINI"
                                                                           ,True)):
            ini = ConfigParser()
            ini.read(editor.file.pat h +"/Changes.ini")
            sections = ini.sections()

        i f(self.Songs.isChecked()):
            try:
                i f(path.isfile(GetGeckoPath())):
                    codes = open(GetGeckoPath())
                    textlines = codes.readlines()
                    codes.close()
                    linenum = 0
                    while linenum < len(textlines):
                        i f('Song' in textlines[linenum]):
                            textlines.pop(linenum)
                            whil e(len(textlines) > linenum) and \
                                    (textlines[linenum][0].isnumeric() or textlines[linenum][0].isalpha()):
                                textlines.pop(linenum)
                        else:
                            linenum = linenum + 1
                    codes = open(GetGeckoPath(), 'w')
                    codes.writelines(textlines)
                    codes.close()
                copyfile(GetBrsarPath() + ".backup", GetBrsarPath())
                for section in sections:
                    if (RecordType.Song in section): ini.remove_section(section)
            except Exception as e:
                ShowError(self.tr("Could not revert songs"), str(e), self)
        if (self.Text.isChecked()):
            try:
                copyfile(GetMessagePath() + "/message.carc.backup", GetMessagePath() + "/message.carc")
                if (path.isfile(GetMessagePath() + '/message.d/new_music_message.txt')): remove(
                    GetMessagePath() + '/message.d/new_music_message.txt')
                GetSongNames()
                for section in sections:
                    if (RecordType.TextSong in section or RecordType.TextStyle in section): ini.remove_section(section)
            except Exception as e:
                ShowError(self.tr("Could not revert message file"), str(e), self)
        if (self.Styles.isChecked()):
            try:
                codes = open(GetGeckoPath())
                textlines = codes.readlines()
                codes.close()
                linenum = 0
                while linenum < len(textlines):
                    if ('Style' in textlines[linenum]):
                        textlines.pop(linenum)
                        while (len(textlines) > linenum) and (
                                textlines[linenum][0].isnumeric() or textlines[linenum][0].isalpha()):
                            textlines.pop(linenum)
                    else:
                        linenum = linenum + 1
                codes = open(GetGeckoPath(), 'w')
                codes.writelines(textlines)
                codes.close()
                for section in sections:
                    if (RecordType.Style in section or RecordType.DefaultStyle in section): ini.remove_section(section)
            except Exception as e:
                ShowError(self.tr("Could not revert styles"), str(e), self)
        if (self.MainDol.isChecked()):
            try:
                copyfile(GetMainDolPath() + ".backup", GetMainDolPath())
                for section in sections:
                    if (RecordType.RemoveSong in section or RecordType.MainDol in section): ini.remove_section(section)
            except Exception as e:
                ShowError(self.tr("Could not revert main.dol"), str(e), self)
        if (path.isfile(editor.file.path + "/Changes.ini") and LoadSetting("Settings", "RemoveChangesFromChangesINI",
                                                                           True)):
            with open(editor.file.path + "/Changes.ini", 'w') as inifile:
                ini.write(inifile)
        self.close()
        SuccessWindow(self.tr("Files Reverted!"))