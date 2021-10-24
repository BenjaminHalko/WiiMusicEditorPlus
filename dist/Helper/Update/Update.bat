@echo off

cd "%~dp0"
cd..
cd..
timeout 1
:loop
del WiiMusicEditorPlus.exe
if exist WiiMusicEditorPlus.exe goto loop
move "%~dp0NewProgram.exe" WiiMusicEditorPlus.exe
START WiiMusicEditorPlus.exe