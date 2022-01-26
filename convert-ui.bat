@echo off

set /p namepath=Path of .ui file: 
for %%f in ("%namepath%") do set name=%%~nf

pyuic5 -o %name%_ui.py %name%.ui