#!/bin/bash

cd "`dirname "$0"`"
rm -r dist/WiiMusicEditorPlus
pyinstaller -F -w -d all --noconfirm --icon=Icon/icon.ico WiiMusicEditorPlus.py
rm dist/WiiMusicEditorPlus
mkdir dist/WiiMusicEditorPlus
mv dist/WiiMusicEditorPlus.app dist/WiiMusicEditorPlus/
echo "copying helper"
cp -r crossplatformhelpers/Mac/Helper dist/WiiMusicEditorPlus/Helper
cp crossplatformhelpers/Version.txt dist/WiiMusicEditorPlus/Helper/Update
echo "creating .zip"
tar -a -C dist -cf dist/WiiMusicEditorPlus-Mac.zip WiiMusicEditorPlus/WiiMusicEditorPlus.app WiiMusicEditorPlus/Helper
echo "done"