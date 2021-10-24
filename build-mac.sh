#!/bin/bash

pyinstaller -F -w --add-data images:images WiiMusicEditorPlus.py
rm -r dist/Helper
cp -r crossplatformhelpers/Linux/Helper dist/Helper
tar -a -C dist -cf dist/WiiMusicEditorPlus-Mac.zip WiiMusicEditorPlus.app Helper