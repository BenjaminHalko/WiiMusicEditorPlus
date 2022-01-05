#!/bin/bash

~/.local/bin/pyinstaller -F -w --noconfirm --add-data crossplatformhelpers/Linux/Helper:Helper --add-data translations/translations:translations --icon=Icon/icon.ico WiiMusicEditorPlus.py
cd dist
rm WiiMusicEditorPlus-Linux.zip
zip -r WiiMusicEditorPlus-Linux.zip WiiMusicEditorPlus

