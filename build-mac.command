#!/bin/bash

cd "`dirname "$0"`"
py2applet WiiMusicEditorPlus.py
mkdir WiiMusicEditorPlus
rm -r WiiMusicEditorPlus/Helper
cp -r crossplatformhelpers/Mac/Helper WiiMusicEditorPlus/Helper
cp crossplatformhelpers/Version.txt WiiMusicEditorPlus/Helper/Update
mv WiiMusicEditorPlus.app WiiMusicEditorPlus/
tar -a -cf WiiMusicEditorPlus-Mac.zip WiiMusicEditorPlus
echo "done"