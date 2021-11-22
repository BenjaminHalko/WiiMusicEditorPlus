#!/bin/bash

cd "`dirname "$0"`"
pyinstaller -F --add-data crossplatformhelpers/Mac/Helper:Helper --icon=Icon/icon.ico WiiMusicEditorPlus.py
echo "creating app"
/usr/local/bin/platypus -y -B -R -i 'Icon/icon.icns'  -a 'WiiMusicEditorPlus'  -o 'None'  -p '/bin/sh'  -f 'dist/WiiMusicEditorPlus' macscript.sh dist/WiiMusicEditorPlus.app
echo "creating .zip"
rm dist/WiiMusicEditorPlus-Mac.zip
tar -a -C dist -cf dist/WiiMusicEditorPlus-Mac.zip WiiMusicEditorPlus.app
echo "done"