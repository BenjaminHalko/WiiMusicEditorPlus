@echo off
pyinstaller -w --noconfirm --add-data crossplatformhelpers/Windows/Helper;Helper --icon icon/icon.ico --add-data translations/translations;translations WiiMusicEditorPlus.py
tar -a -C dist -cf dist\WiiMusicEditorPlus-Windows.zip WiiMusicEditorPlus