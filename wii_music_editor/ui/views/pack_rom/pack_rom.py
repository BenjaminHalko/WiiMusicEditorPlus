from os import path, remove
from pathlib import Path
from shutil import copyfile, move

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QFileDialog

from wii_music_editor.ui.views.error_handler.error_handler import ShowError
from wii_music_editor.ui.views.pack_rom.pack_rom_ui import Ui_Packrom
from wii_music_editor.ui.views.success.success import SuccessWindow
from wii_music_editor.utils import paths


class PackRomWindow(QDialog, Ui_Packrom):
    def __init__(self):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setupUi(self)
        self.CreateRom.clicked.connect(self.MakeRom)
        self.show()
        self.exec()

    def MakeRom(self):
        file = QFileDialog()
        file.setFileMode(QFileDialog.FileMode.AnyFile)
        file.setAcceptMode(QFileDialog.FileMode.AcceptSave)
        if self.RomTypeWbfs.isChecked():
            file.setNameFilter(self.tr("Wii Backup File System") + " (*.wbfs)")
        else:
            file.setNameFilter("iso (*.iso)")
        if file.exec():
            try:
                file_path = file.selectedFiles()[0]
                if self.RomTypeWbfs.isChecked():
                    file_type = ".wbfs"
                else:
                    file_type = ".iso"
                if path.exists(file_path):
                    remove(file_path)
                if (Path(file_path).suffix != file_type): file_path = file_path + file_type
                args = [HelperPath() + '/Wiimms/wit', 'cp', paths.loadedFilePath, file_path]
                if self.RomTypeWbfs.isChecked():
                    args.append('--wbfs')
                if self.PatchMainDolCheckbox.isChecked():
                    copyfile(GetMainDolPath(), GetMainDolPath() + ".tmp")
                    PatchMainDol()
                Run(args)
                if self.PatchMainDolCheckbox.isChecked():
                    remove(GetMainDolPath())
                    move(GetMainDolPath() + ".tmp", GetMainDolPath())
                self.close()
                SuccessWindow(self.tr("Rom Successfuly Packed!"))
            except Exception as e:
                self.close()
                ShowError(self.tr("Could not pack rom"), str(e))
