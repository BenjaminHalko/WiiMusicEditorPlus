#!/bin/bash

cd "`dirname "$0"`"
#pyinstaller -F -w --noconfirm --add-data images:images WiiMusicEditorPlus.py
py2applet --make-setup WiiMusicEditorPlus.py
rm -rf build dist
python3 setup.py py2app
echo "removing old helper"
rm -r dist/Helper
echo "copying helper"
cp -r crossplatformhelpers/Linux/Helper dist/Helper
echo "creating .zip"
tar -a -C dist -cf dist/WiiMusicEditorPlus-Mac.zip WiiMusicEditorPlus.app Helper
echo "done"