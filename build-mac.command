#!/bin/bash

cd "`dirname "$0"`"
pyinstaller -F --noconfirm --clean --noupx WiiMusicEditorPlus.py
mv dist/WiiMusicEditorPlusProgram dist/WiiMusicEditorPlus
echo "removing old helper"
rm -r dist/WiiMusicEditorPlus/Helper
echo "copying helper"
cp -r crossplatformhelpers/Mac/Helper dist/WiiMusicEditorPlus/Helper
cp crossplatformhelpers/Version.txt dist/Helper/Update
mv dist/WiiMusicEditorPlusProgram dist/WiiMusicEditorPlus/WiiMusicEditorPlus
echo "creating .zip"
tar -a -C dist -cf dist/WiiMusicEditorPlus-Mac.zip WiiMusicEditorPlus
echo "done"