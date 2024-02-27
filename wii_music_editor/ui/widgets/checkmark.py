from PySide6.QtWidgets import QCheckBox

from wii_music_editor.utils.save import save_setting


class Checkmark:
    __widget: QCheckBox
    __prefObject: object
    __category: str
    __setting: str
    __callback: callable

    def __init__(self, checkmark: QCheckBox, category: str, setting: str, pref_object: object = None,
                 callback: callable = None):
        self.__widget = checkmark
        self.__category = category
        self.__setting = setting
        self.__prefObject = pref_object
        self.__callback = callback
        if pref_object is not None:
            self.__widget.setChecked(getattr(self.__prefObject, self.__setting))

        # On click
        self.__widget.clicked.connect(self.clicked)

    def clicked(self):
        clicked = self.__widget.isChecked()
        save_setting(self.__category, self.__setting, clicked)
        setattr(self.__prefObject, self.__setting, clicked)
        if self.__callback is not None:
            self.__callback()
