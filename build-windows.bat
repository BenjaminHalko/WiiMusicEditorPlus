@echo off
pyinstaller -F -w -i icon.ico WiiMusicEditorPlus.py

rmdir /s /q "dist/WiiMusicEditorPlus/Helper"
xcopy /E /H /C /I "crossplatformhelpers\Windows\Helper" "dist\WiiMusicEditorPlus\Helper"
xcopy "crossplatformhelpers\Version.txt" "dist\WiiMusicEditorPlus\Helper\Update"
move "%~dp0dist\WiiMusicEditorPlus.exe" "%~dp0dist\WiiMusicEditorPlus\WiiMusicEditorPlus.exe"
tar -a -C dist -cf dist\WiiMusicEditorPlus-Windows.zip WiiMusicEditorPlus