@echo off

cd "%~dp0"
cd..
cd..
timeout 1
del WiiMusicEditorPlus.exe
move "%~dp0NewProgram.exe" WiiMusicEditorPlus.exe
START WiiMusicEditorPlus.exe