from pathlib import Path
from shutil import copyfile

from wii_music_editor.data.styles import styleList
from wii_music_editor.editor.gecko import CreateGct
from wii_music_editor.editor.region import BasedOnRegion
from wii_music_editor.utils.pathUtils import paths


class MainDolOffsets:
    songSegmentOffset = 0x59C520
    songSegmentSize = 0xBC
    songSegmentTimeSignature = 0x20
    songSegmentLength = 0x24
    songSegmentTempo = 0x28

    styleSegmentOffset = 0x596758
    styleSegmentSize = 0x24
    styleSegmentMelody = 0x04
    styleSegmentHarmony = 0x08
    styleSegmentChord = 0x0C
    styleSegmentBass = 0x10
    styleSegmentPerc1 = 0x14
    styleSegmentPerc2 = 0x18

    styleCodeBegin = 0x36F9A4
    styleCodeEnd = 0x3701CC


class MainDol:
    mainDolPath: Path
    data: bytearray

    def __init__(self, path: Path):
        self.mainDolPath = path
        with open(self.mainDolPath, "rb") as file:
            self.data = bytearray(file.read())

    def write(self, data: int, offset: int, length: int = 4):
        self.data[offset:offset + length] = data.to_bytes(length, "big")

    def save(self):
        with open(self.mainDolPath, "wb") as file:
            file.write(self.data)

    def set_style(self, index: int, style: list[int]):
        offset = MainDolOffsets.styleSegmentOffset + index * MainDolOffsets.styleSegmentSize
        self.write(style[0], offset + MainDolOffsets.styleSegmentMelody)
        self.write(style[1], offset + MainDolOffsets.styleSegmentHarmony)
        self.write(style[2], offset + MainDolOffsets.styleSegmentChord)
        self.write(style[3], offset + MainDolOffsets.styleSegmentBass)
        self.write(style[4], offset + MainDolOffsets.styleSegmentPerc1)
        self.write(style[5], offset + MainDolOffsets.styleSegmentPerc2)

    def remove_style_execution(self):
        replaced = False

        # Removes the style execution code
        for i in range(MainDolOffsets.styleCodeBegin, MainDolOffsets.styleCodeEnd, 4):
            if self.data[i] != b'\x38':
                self.data[i:i + 4] = b'\x38\x00\x00\x00'
                replaced = True

        if replaced:
            for style in styleList:
                self.set_style(style.style_id, style.style)


def PatchMainDol(dol_path="", gecko_path=""):
    if dol_path == "":
        dol_path = str(paths.mainDolPath)
        if not Path(dol_path + ".backup").exists():
            copyfile(dol_path, dol_path + ".backup")

    if gecko_path == "":
        gecko_path = str(paths.geckoPath)

    gct = False
    if Path(gecko_path).suffix != ".gct":
        CreateGct(paths.savepath / BasedOnRegion(gameIds) + ".gct", gecko_path)
        gecko_path = SavePath() + "/" + BasedOnRegion(gameIds) + ".gct"
        gct = True
    Run([HelperPath() + '/Wiimms/wstrt', 'patch', dolPath, '--add-section', geckoPath, '--force'])
    if (gct): os.remove(geckoPath)