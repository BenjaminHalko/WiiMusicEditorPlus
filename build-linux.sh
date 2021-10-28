#!/bin/bash

rm -r __pycache__
echo "PyInstalling"
~/.local/bin/pyinstaller -F -w --noconfirm --clean --noupx WiiMusicEditorPlus.py
rm -r dist/Helper
cp -r crossplatformhelpers/Linux/Helper dist/Helper
cd dist
chmod +x Helper/Update/Update.sh
zip -r WiiMusicEditorPlus-Linux.zip WiiMusicEditorPlus Helper