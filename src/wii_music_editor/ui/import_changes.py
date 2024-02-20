from configparser import ConfigParser

from PySide6.QtCore import QThread, pyqtSignal


class Import(QThread):
    progress = pyqtSignal(int, int)
    done = pyqtSignal()
    error = pyqtSignal(str, str)
    recordfile = "null"

    def run(self):
        ini = ConfigParser()
        ini.read(self.recordfile)
        sections = ini.sections()
        self.waiting = False
        for section in sections:
            try:
                self.progress.emit(sections.index(section), len(sections))
                action, name = section.split("-")
                if (action == RecordType.Song):
                    brseqInfo = [0, 0]
                    brseqLength = [0, 0]
                    if (load_setting("Settings", "NormalizeMidi", False)):
                        midiInfo = LoadMidi(ini.get(section, "midisong"), int(ini.get(section, "tempo")))
                    else:
                        midiInfo = LoadMidi(ini.get(section, "midisong"))
                    brseqInfo[0] = midiInfo[0]
                    brseqLength[0] = midiInfo[1]

                    if (ini.get(section, "midiscore") != ""):
                        if (load_setting("Settings", "NormalizeMidi", False)):
                            midiInfo = LoadMidi(ini.get(section, "midiscore"), int(ini.get(section, "tempo")))
                        else:
                            midiInfo = LoadMidi(ini.get(section, "midiscore"))
                    brseqInfo[1] = midiInfo[0]
                    brseqLength[1] = midiInfo[1]

                    PatchBrsar(int(name), brseqInfo, brseqLength, int(ini.get(section, "tempo")),
                               int(ini.get(section, "length")), int(ini.get(section, "timesignature")))
                elif (action == RecordType.Style):
                    patchInfo = '0' + format(Styles[int(name)].MemOffset + BasedOnRegion(gctRegionOffsetsStyles),
                                             "x") + " 00000018\n"
                    for i in range(3):
                        if (int(ini.get(section, str(i * 2))) == len(Instruments) - 1):
                            num1 = "ffffffff"
                        else:
                            num1 = format(int(ini.get(section, str(i * 2))), "x")
                        if (int(ini.get(section, str(i * 2 + 1))) == len(Instruments) - 1):
                            num2 = "ffffffff"
                        else:
                            num2 = format(int(ini.get(section, str(i * 2 + 1))), "x")
                        patchInfo = patchInfo + "0" * (8 - len(num1)) + num1 + " " + "0" * (8 - len(num2)) + num2 + "\n"
                    AddPatch(Styles[int(name)].Name + " Style Patch", patchInfo)
                elif (action == RecordType.TextSong):
                    ChangeName(int(name),
                               [ini.get(section, "name"), ini.get(section, "desc"), ini.get(section, "genre")])
                elif (action == RecordType.TextStyle):
                    ChangeName(int(name), ini.get(section, "name"))
                elif (action == RecordType.MainDol):
                    PatchMainDol(geckoPath=ini.get(section, "geckopath"))
                elif (action == RecordType.RemoveSong):
                    file = open(GetMainDolPath(), "r+b")
                    for song in ini.get(section, "songs").split(","):
                        file.seek(0x59C574 + 0xBC * Songs[int(song.replace("[", "").replace("]", ""))].MemOrder)
                        file.write(bytes.fromhex('ffffffffffff'))
                    file.close()
                elif (action == RecordType.DefaultStyle):
                    AddPatch(Songs[int(name)].Name + ' Default Style Patch',
                             '0' + format(Songs[int(name)].MemOffset + BasedOnRegion(gctRegionOffsets) + 42,
                                          'x') + ' 000000' + Styles[int(ini.get(section, "style"))].StyleId + '\n')
            except Exception as e:
                self.error.emit(self.tr("Could not import change") + " " + section, str(e))
                self.waiting = True
                while self.waiting: w = 0
        self.done.emit()


class ImportChangesWindow(QDialog, Ui_Import):
    def __init__(self, file):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setupUi(self)
        self.file = file

        self.importthread = Import()
        self.importthread.progress.connect(self.reportProgress)
        self.importthread.done.connect(self.finish)
        self.importthread.error.connect(self.error)
        self.importthread.recordfile = file
        self.importthread.start()

        self.show()
        self.exec()

    def finish(self):
        self.Progress.setValue(100)
        self.Label.setText(self.tr("Finished Importing Changes"))

    def reportProgress(self, value, total):
        self.Progress.setValue((value - 1) / total * 100)
        self.Label.setText(self.tr("Importing Change {} out of {}".format(value, total)))

    def error(self, error, message):
        ShowError(error, message, self)
        self.importthread.waiting = False
