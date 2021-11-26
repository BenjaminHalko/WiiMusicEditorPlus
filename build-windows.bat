@echo off
pyinstaller -F -w --add-data crossplatformhelpers/Windows/Helper;Helper WiiMusicEditorPlus.py
tar -a -C dist -cf dist\WiiMusicEditorPlus-Windows.zip WiiMusicEditorPlus.exe