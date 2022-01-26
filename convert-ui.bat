@echo off

if [%1]==[] (set name=WiiMusicPlus) else (set name=%~n1)

pyuic5 -o %name%_ui.py %name%.ui