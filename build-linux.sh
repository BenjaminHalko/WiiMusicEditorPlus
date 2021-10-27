#!/bin/bash

/home/ubuntu/.local/bin/pyinstaller -F -w --noconfirm --noupx WiiMusicEditorPlus.py
rm -r dist/Helper
cp -r crossplatformhelpers/Linux/Helper dist/Helper
tar -C dist -cf dist/WiiMusicEditorPlus-Linux.tar.gz WiiMusicEditorPlus Helper