#!/bin/bash

rm -r __pycache__
echo "PyInstalling"
pyinstaller -F -w --noconfirm --clean --noupx -n Program WiiMusicEditorPlus.py
mkdir dist/WiiMusicEditorPlus
mv dist/Program dist/WiiMusicEditorPlus/WiiMusicEditorPlus
rm -r dist/WiiMusicEditorPlus/Helper
cp -r crossplatformhelpers/Linux/Helper dist/WiiMusicEditorPlus/Helper
cp crossplatformhelpers/Version.txt dist/Helper/Update
mv dist/WiiMusicEditorPlusProgram dist/WiiMusicEditorPlus/WiiMusicEditorPlus
cd dist
zip -r WiiMusicEditorPlus-Linux.zip WiiMusicEditorPlus