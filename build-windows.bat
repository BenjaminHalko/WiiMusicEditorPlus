@echo off
pyinstaller -F -w --icon=Icon/icon.ico --add-data crossplatformhelpers/Windows/Helper;Helper WiiMusicEditorPlus.py

move "%~dp0dist\WiiMusicEditorPlus.exe" "%~dp0dist\WiiMusicEditorPlus\WiiMusicEditorPlus.exe"
tar -a -C dist -cf dist\WiiMusicEditorPlus-Windows.zip WiiMusicEditorPlus/WiiMusicEditorPlus.exe