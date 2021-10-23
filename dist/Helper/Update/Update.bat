@echo off

cd "%~dp0"
cd..
cd..
timeout 1
:loop
move "%~dp0NewProgram.exe" WiiMusicEditorPlus.exe
if exist "%~dp0NewProgram.exe" goto loop
START WiiMusicEditorPlus.exe