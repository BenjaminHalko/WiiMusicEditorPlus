#!/bin/bash

cd "`dirname "$0"`"
pyinstaller -F -w --noconfirm --clean --noupx WiiMusicEditorPlus.py
echo "removing old helper"
rm -r dist/Helper
echo "copying helper"
cp -r crossplatformhelpers/Linux/Helper dist/Helper
echo "creating .zip"
tar -a -C dist -cf dist/WiiMusicEditorPlus-Mac.zip WiiMusicEditorPlus.app Helper
echo "done"