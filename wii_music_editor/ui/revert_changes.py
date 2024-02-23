from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from wii_music_editor.editor.reset import revert_all, revert_all_songs, revert_all_styles, revert_all_default_styles, \
    revert_all_text
from wii_music_editor.services.discord import discord_presence, DiscordState
from wii_music_editor.ui.windows.revert_changes_ui import Ui_Revert


class RevertChangesWindow(QDialog, Ui_Revert):
    def __init__(self):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setupUi(self)

        self.SelectButton.clicked.connect(lambda: self.select_all(True))
        self.DeselectButton.clicked.connect(lambda: self.select_all(False))
        self.PatchButton.clicked.connect(self.revert)
        self.Songs.clicked.connect(self.is_patchable)
        self.Styles.clicked.connect(self.is_patchable)
        self.DefaultStyles.clicked.connect(self.is_patchable)
        self.Text.clicked.connect(self.is_patchable)
        self.PatchButton.setEnabled(False)

        discord_presence.update(DiscordState.RevertingChanges)
        self.show()
        self.exec()
        discord_presence.update(DiscordState.ModdingWiiMusic)

    def is_patchable(self):
        self.PatchButton.setEnabled(self.Songs.isChecked() or self.Styles.isChecked()
                                    or self.DefaultStyles.isChecked() or self.Text.isChecked())

    def select_all(self, select):
        self.Songs.setChecked(select)
        self.Styles.setChecked(select)
        self.DefaultStyles.setChecked(select)
        self.Text.setChecked(select)
        self.PatchButton.setEnabled(select)

    def revert(self):
        if (self.Songs.isChecked() and self.Styles.isChecked()
                and self.DefaultStyles.isChecked() and self.Text.isChecked()):
            revert_all()
        else:
            if self.Songs.isChecked():
                revert_all_songs()
            if self.Styles.isChecked():
                revert_all_styles()
            if self.DefaultStyles.isChecked():
                revert_all_default_styles()
            if self.Text.isChecked():
                revert_all_text()
        self.PatchButton.setEnabled(False)
