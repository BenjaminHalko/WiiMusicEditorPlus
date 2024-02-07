def CreateGeckoCode(self):
    global lastFileDirectory
    file = QtWidgets.QFileDialog()
    file.setFileMode(QtWidgets.QFileDialog.AnyFile)
    file.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
    file.setNameFilter("Geckocodes (*.ini)")
    file.setViewMode(QtWidgets.QFileDialog.Detail)
    file.setDirectory(lastFileDirectory)
    if file.exec_():
        editor.file.path = file.selectedFiles()[0]
        if (pathlib.Path(editor.file.path).suffix != ".ini"): editor.file.path = editor.file.path + ".ini"
        lastFileDirectory = os.path.dirname(editor.file.path)
        SaveSetting("Paths", "LastLoadedPath", lastFileDirectory)
        openfile = open(editor.file.path, "w")
        openfile.write("")
        openfile.close()
        PrepareFile()
        SaveSetting("Paths", "CurrentLoadedFile", editor.file.path)
        self.MP_LoadedFile_Path.setText(editor.file.path)
        self.MP_LoadedFile_Label.setText(self.tr('Currently Loaded File:'))
        return True
    return False