def main():
    from wii_music_editor.utils.logger import setup_logger
    setup_logger()

    import logging
    from pathlib import Path

    from PySide6.QtGui import QIcon, QFontDatabase
    from PySide6.QtWidgets import QApplication

    from wii_music_editor.ui.first_setup import FirstSetupWindow
    from wii_music_editor.ui.main_window import MainWindow
    from wii_music_editor.utils.pathUtils import paths
    from wii_music_editor.utils.save import savePath

    app = QApplication()
    app.setWindowIcon(QIcon(str(paths.includeAll / "icon" / "icon.png")))
    QFontDatabase.addApplicationFont(str(paths.includeAll / "fonts" / "contb.ttf"))
    QFontDatabase.addApplicationFont(str(paths.includeAll / "fonts" / "contm.ttf"))

    # First Setup
    if not Path(f"{savePath}/settings.ini").is_file():
        logging.info("Starting First Setup")
        FirstSetupWindow(app)

    # Main Window
    MainWindow()
    app.exec()
