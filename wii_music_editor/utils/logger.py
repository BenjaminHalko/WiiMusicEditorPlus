import logging
import os
import sys

from wii_music_editor.utils.save import savePath
from wii_music_editor.utils.version import GetCurrentVersion


def is_debug():
    return "--debug" in sys.argv


def setup_logger():
    if (savePath/"log.txt").is_file():
        if (savePath/"log.old.txt").is_file():
            os.remove(savePath/"log.old.txt")
        os.rename(savePath/"log.txt", savePath/"log.old.txt")
    log = logging.getLogger()
    hStErr = logging.StreamHandler(sys.stderr)
    hStOut = logging.StreamHandler(sys.stdout)
    hStErr.setLevel('ERROR')
    hStOut.setLevel('DEBUG')
    log.setLevel('NOTSET')
    hStOut.addFilter(lambda x: x.levelno < logging.ERROR)
    logging.basicConfig(
        level=logging.DEBUG if is_debug() else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(savePath/"log.txt"),
            hStOut,
            hStErr,
        ]
    )

    # Start logging
    logging.info("Starting Wii Music Editor...")
    version = GetCurrentVersion()
    if version != "":
        logging.info(f"Version: {version}")
    else:
        logging.warning("Version: Could not be found")
    logging.info(f"Python Version: {sys.version.split()[0]}")
