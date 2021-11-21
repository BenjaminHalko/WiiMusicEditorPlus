#!/bin/bash

cd "`dirname "$0"`"
pyinstaller -F --noconfirm -n Program --add-data crossplatformhelpers/Linux/Helper:Helper --icon=Icon/icon.ico WiiMusicEditorPlus.py
mkdir dist/WiiMusicEditorPlus
mv dist/Program dist/WiiMusicEditorPlus/WiiMusicEditorPlus
echo "creating app"
/usr/local/bin/platypus -y -B -R -i 'Icon/icon.icns'  -a 'WiiMusicEditorPlus'  -o 'None'  -p '/bin/sh'  -f 'dist/WiiMusicEditorPlus/WiiMusicEditorPlus' -f 'crossplatformhelpers/Mac/Helper' macscript.sh dist/WiiMusicEditorPlus/WiiMusicEditorPlus.app
echo "creating .zip"
rm dist/WiiMusicEditorPlus-Mac.zip
tar -a -C dist -cf dist/WiiMusicEditorPlus-Mac.zip WiiMusicEditorPlus/WiiMusicEditorPlus.app
echo "done"