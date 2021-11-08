#!/bin/bash

cd "`dirname "$0"`"
py2applet WiiMusicEditorPlus.py
rm -r WiiMusicEditorPlus
mkdir WiiMusicEditorPlus
cp -r crossplatformhelpers/Mac/Helper WiiMusicEditorPlus/Helper
cp crossplatformhelpers/Version.txt WiiMusicEditorPlus/Helper/Update
mv WiiMusicEditorPlus.app WiiMusicEditorPlus/
tar -a -cf WiiMusicEditorPlus-Mac.zip WiiMusicEditorPlus
echo "done"