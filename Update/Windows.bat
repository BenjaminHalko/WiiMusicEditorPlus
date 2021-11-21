@echo off

timeout 1
del "%1WiiMusicEditorPlus.exe"
move "%~dp0NewProgram.exe" "%1WiiMusicEditorPlus.exe"
START "%1WiiMusicEditorPlus.exe"