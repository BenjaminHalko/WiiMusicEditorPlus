#!/bin/bash

cd "`dirname "$0"`"
pyinstaller -F --noconfirm -n Program --icon=Icon/icon.ico --add-data crossplatformhelpers/Mac/Helper;Helper WiiMusicEditorPlus.py
mkdir dist/WiiMusicEditorPlus
mv dist/Program dist/WiiMusicEditorPlus/WiiMusicEditorPlus
echo "creating app"
/usr/local/bin/platypus -y -R -B -i 'Icon/icon.icns'  -a 'WiiMusicEditorPlus'  -o 'None'  -p '/bin/sh'  -f 'dist/WiiMusicEditorPlus/WiiMusicEditorPlus' macscript.sh dist/WiiMusicEditorPlus/WiiMusicEditorPlus.app
echo "creating .zip"
rm dist/WiiMusicEditorPlus-Mac.zip
tar -a -C dist -cf dist/WiiMusicEditorPlus-Mac.zip WiiMusicEditorPlus/WiiMusicEditorPlus.app
echo "done"