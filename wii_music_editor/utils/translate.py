from PyQt6.QtCore import QTranslator, QLocale

from wii_music_editor.utils.helper.paths import translationPath
from wii_music_editor.utils.helper.save import save_setting, load_setting


lang = load_setting("Settings", "Language", 0)
languageList = ["en", "fr", "sp", "ge", "it", "jp", "kr"]
translator = None


def changeLanguage(app, new_lang=None):
    global lang, translator

    if new_lang is not None:
        lang = new_lang
        save_setting("Settings", "Language", lang)

    if translator is not None:
        app.removeTranslator(translator)
        translator = None

    if lang != 0:
        translator = QTranslator()
        translator.load(QLocale(), f"${translationPath}/{languageList[lang]}.qm")
        app.installTranslator(translator)
