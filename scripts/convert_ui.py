import os
from pathlib import Path
from subprocess import call


def convert():
    root_dir = (Path(__file__).parent / "..").resolve()
    template_dir = root_dir / 'wii_music_editor' / "templates"
    resource_dir = root_dir / 'wii_music_editor' / "resources"
    output_dir = root_dir / 'wii_music_editor' / 'ui' / "windows"
    for file in template_dir.iterdir():
        print("Converting file:", file)
        call(["pyside6-uic", file, "-o", output_dir / f"{file.stem}_ui.py"])

    print("Converting resources")
    call(["pyside6-rcc", resource_dir / "resources.qrc", "-o", root_dir / "resources_rc.py"])
