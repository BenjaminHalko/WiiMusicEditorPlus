@echo off
pyinstaller -F -w --icon=Icon/icon.ico --add-data crossplatformhelpers/Windows/Helper;Helper WiiMusicEditorPlus.py
tar -a -C dist -cf dist\WiiMusicEditorPlus-Windows.zip WiiMusicEditorPlus.exe