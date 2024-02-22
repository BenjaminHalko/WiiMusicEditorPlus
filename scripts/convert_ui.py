from pathlib import Path
import subprocess


def convert():
    root_dir = (Path(__file__).parent / "..").resolve()
    template_dir = root_dir / "ui_templates"
    output_dir = root_dir / 'wii_music_editor' / 'ui' / "windows"
    for file in template_dir.iterdir():
        if file.suffix != ".ui":
            continue
        print("Converting file:", file)
        result = subprocess.run(["pyside6-uic", file],  stdout=subprocess.PIPE)
        with open(output_dir / (file.stem + "_ui.py"), "w") as f:
            f.write(result.stdout.decode().replace('import resources_rc', 'from . import resources_rc'))

    print("Converting resources")
    subprocess.call(["pyside6-rcc", template_dir / "resources.qrc", "-o", output_dir / "resources_rc.py"])


if __name__ == "__main__":
    convert()
