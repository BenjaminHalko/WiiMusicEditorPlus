from math import floor

with open("wii_music_editor/editor/styles.txt") as f:
    styles = f.read().splitlines()

styles = [style.strip("DAT_").strip(";").replace("0x", "").split(" = ") for style in styles]

for i in range(len(styles)):
    amount = int(styles[i][0], 16) - 0x8059A65C
    styles[i].append((amount % 0x24) / 4)
    styles[i].append(f"0x{format(floor(amount / 0x24), "x")}")

styles = sorted(styles, key=lambda x: x[2])
styles = sorted(styles, key=lambda x: int(x[3].replace("0x", ""), 16))

with open("wii_music_editor/editor/styles_formatted.txt", "w") as f:
    for style in styles:
        f.write(str(style)+"\n")
