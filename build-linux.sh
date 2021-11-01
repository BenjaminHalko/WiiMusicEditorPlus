#!/bin/bash

rm -r __pycache__
echo "PyInstalling"
~/.local/bin/pyinstaller -F -w --noconfirm --clean --noupx WiiMusicEditorPlus.py
rm -r dist/Helper
cp -r crossplatformhelpers/Linux/Helper dist/Helper
cp crossplatformhelpers/Version.txt dist/Helper/Update
cd dist
zip -r WiiMusicEditorPlus-Linux.zip WiiMusicEditorPlus Helper