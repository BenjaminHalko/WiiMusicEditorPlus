from PySide6.QtCore import QTranslator, QLocale
from PySide6.QtWidgets import QApplication

from wii_music_editor.utils.pathUtils import paths
from wii_music_editor.utils.save import save_setting, load_setting

lang = load_setting("Settings", "Language", 0)
languageList = ["en", "fr", "sp", "ge", "it", "jp", "kr"]
translator = QTranslator()


def tr(context: str, source_text: str) -> str:
    if lang == 0 or True:
        return source_text
    return translator.translate(context, source_text)


def changeLanguage(app: QApplication, new_lang: int = None):
    global lang, translator

    if new_lang is not None:
        lang = new_lang
        save_setting("Settings", "Language", lang)

    app.removeTranslator(translator)

    if lang != 0:
        translator.load(QLocale(), f"${paths.translation}/{languageList[lang]}.qm")
        app.installTranslator(translator)
