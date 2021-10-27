#!/bin/bash

~/.local/bin/pyinstaller -F -w --noconfirm --clean --noupx WiiMusicEditorPlus.py
rm -r dist/Helper
cp -r crossplatformhelpers/Linux/Helper dist/Helper
tar -C dist -cf dist/WiiMusicEditorPlus-Linux.tar.gz WiiMusicEditorPlus Helper