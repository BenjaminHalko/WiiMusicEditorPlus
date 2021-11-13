#!/bin/bash

cd "`dirname "$0"`"
pyinstaller -F --noconfirm -n Program WiiMusicEditorPlus.py
mkdir dist/WiiMusicEditorPlus
mv dist/Program dist/WiiMusicEditorPlus/WiiMusicEditorPlus
echo "removing old helper"
rm -r dist/WiiMusicEditorPlus/Helper
echo "copying helper"
cp -r crossplatformhelpers/Mac/Helper dist/WiiMusicEditorPlus/Helper
cp crossplatformhelpers/Version.txt dist/WiiMusicEditorPlus/Helper/Update
echo "creating .zip"
tar -a -C dist -cf dist/WiiMusicEditorPlus-Mac.zip WiiMusicEditorPlus/WiiMusicEditorPlus WiiMusicEditorPlus/Helper
mv dist/WiiMusicEditorPlus-Mac.zip ~/Desktop
echo "done"