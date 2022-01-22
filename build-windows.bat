@echo off
pyinstaller -F -w --add-data crossplatformhelpers/Windows/Helper;Helper --icon icon/icon.ico --add-data translations/translations;translations WiiMusicEditorPlus.py
tar -a -C dist -cf dist\WiiMusicEditorPlus-Windows.zip WiiMusicEditorPlus.exe