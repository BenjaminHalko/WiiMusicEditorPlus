#!/bin/bash

~/.local/bin/pyinstaller -F -w --noconfirm --clean --noupx WiiMusicEditorPlus.py
rm -r dist/Helper
cp -r crossplatformhelpers/Linux/Helper dist/Helper
cd dist
zip -r WiiMusicEditorPlus-Linux.zip WiiMusicEditorPlus Helper