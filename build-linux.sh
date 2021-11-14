#!/bin/bash

pyinstaller -F -w --noconfirm -n Program --icon=Icon/icon.ico WiiMusicEditorPlus.py
mkdir dist/WiiMusicEditorPlus
mv dist/Program dist/WiiMusicEditorPlus/WiiMusicEditorPlus
rm -r dist/WiiMusicEditorPlus/Helper
cp -r crossplatformhelpers/Linux/Helper dist/WiiMusicEditorPlus/Helper
cp crossplatformhelpers/Version.txt dist/WiiMusicEditorPlus/Helper/Update
mv dist/WiiMusicEditorPlusProgram dist/WiiMusicEditorPlus/WiiMusicEditorPlus
cd dist
rm WiiMusicEditorPlus-Linux.zip
zip -r WiiMusicEditorPlus-Linux.zip WiiMusicEditorPlus