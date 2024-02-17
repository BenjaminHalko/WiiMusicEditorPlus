from pathlib import Path

from wii_music_editor.data.styles import style_list
from wii_music_editor.editor.dol import MainDolOffsets

with open("wii_music_editor/editor/styles.txt", "r") as file:
    lines = file.readlines()


def getOffset(hexoffset: int):
    hex_offset = hex(hexoffset).removeprefix("0x")
    for line in lines:
        if hex_offset in line:
            r = line.split(" ")[-1].replace(";\n", "").split("x")[-1].zfill(2).upper()
            if r == "FFFFFFFF":
                return "0xFF"
            return "0x"+r


types = [
    "Global",
    "SongSpecific",
    "QuickJam",
    "Menu"
]


if __name__ == "__main__":
    for style in style_list:
        offset = 0x8059A658 + style.style_id * MainDolOffsets.styleSegmentSize

        print(f"Style(StyleType.{types[style.style_type.value]}, '{style.name}', {hex(style.style_id)},\n    {getOffset(offset+MainDolOffsets.styleSegmentMelody)}, {getOffset(offset+MainDolOffsets.styleSegmentHarmony)}, {getOffset(offset+MainDolOffsets.styleSegmentChord)}, {getOffset(offset+MainDolOffsets.styleSegmentBass)}, {getOffset(offset+MainDolOffsets.styleSegmentPerc1)}, {getOffset(offset+MainDolOffsets.styleSegmentPerc2)}),")
