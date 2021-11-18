#!/bin/bash

cd "`dirname "$0"`"
pyinstaller -F --noconfirm -n Program --icon=Icon/icon.ico WiiMusicEditorPlus.py
mkdir dist/WiiMusicEditorPlus
mv dist/Program dist/WiiMusicEditorPlus/WiiMusicEditorPlus
echo "removing old helper"
rm -r dist/WiiMusicEditorPlus/Helper
echo "creating app"
/usr/local/bin/platypus -B -i 'Icon/icon.icns' -a 'WiiMusicEditorPlus' -o 'None' -p '/bin/sh'   '/Users/benjamin/Desktop/WiiMusicEditorPlus/dist/WiiMusicEditorPlus/WiiMusicEditorPlus'
echo "copying helper"
cp -r crossplatformhelpers/Mac/Helper dist/WiiMusicEditorPlus/Helper
cp crossplatformhelpers/Version.txt dist/WiiMusicEditorPlus/Helper/Update
echo "creating .zip"
rm dist/WiiMusicEditorPlus-Mac.zip
tar -a -C dist -cf dist/WiiMusicEditorPlus-Mac.zip WiiMusicEditorPlus/WiiMusicEditorPlus WiiMusicEditorPlus/Helper
echo "done"