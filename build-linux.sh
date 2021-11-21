#!/bin/bash

pyinstaller -F -w --noconfirm -n Program --add-data crossplatformhelpers/Linux/Helper;Helper --icon=Icon/icon.ico WiiMusicEditorPlus.py
mkdir dist/WiiMusicEditorPlus
mv dist/Program dist/WiiMusicEditorPlus/WiiMusicEditorPlus
mv dist/WiiMusicEditorPlusProgram dist/WiiMusicEditorPlus/WiiMusicEditorPlus
cd dist
rm WiiMusicEditorPlus-Linux.zip
zip -r WiiMusicEditorPlus-Linux.zip WiiMusicEditorPlus/WiiMusicEditorPlus WiiMusicEditorPlus/Helper