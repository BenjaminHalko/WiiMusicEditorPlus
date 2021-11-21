@echo on

timeout 1
del %1
move "%~dp0WiiMusicEditorPlus\WiiMusicEditorPlus.exe" %1
