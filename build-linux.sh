#!/bin/bash

rm -r __pycache__
echo "PyInstalling"
~/.local/bin/pyinstaller -F -w --noconfirm --clean --noupx WiiMusicEditorPlus.py
mv dist/WiiMusicEditorPlusProgram dist/WiiMusicEditorPlus
rm -r dist/WiiMusicEditorPlus/Helper
cp -r crossplatformhelpers/Linux/Helper dist/WiiMusicEditorPlus/Helper
cp crossplatformhelpers/Version.txt dist/Helper/Update
mv dist/WiiMusicEditorPlusProgram dist/WiiMusicEditorPlus/WiiMusicEditorPlus
cd dist
zip -r WiiMusicEditorPlus-Linux.zip WiiMusicEditorPlus