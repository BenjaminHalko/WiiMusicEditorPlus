@echo off
pyinstaller -F -w --add-data images;images WiiMusicEditorPlus.py
rmdir /s /q "dist/Helper"
xcopy /E /H /C /I "crossplatformhelpers/Windows/Helper" "dist/Helper"
tar -a -C dist -cf dist/WiiMusicEditorPlus-Windows.zip WiiMusicEditorPlus.exe Helper