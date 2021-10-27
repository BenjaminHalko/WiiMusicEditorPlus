#!/bin/bash

~/.local/bin/pyinstaller -F -w --noconfirm --clean --noupx WiiMusicEditorPlus.py
rm -r dist/Helper
cp -r crossplatformhelpers/Linux/Helper dist/Helper
tar -a -C dist -cf dist/WiiMusicEditorPlus-Linux.zip WiiMusicEditorPlus Helper