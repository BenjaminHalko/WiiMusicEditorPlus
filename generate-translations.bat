@echo off

setlocal EnableDelayedExpansion
set files=

for %%f in (*.py) DO call :concat %%f
pylupdate5%files% -noobsolete -ts translations/jp.ts translations/kr.ts translations/en.ts translations/fr.ts translations/sp.ts translations/ge.ts translations/it.ts
goto :eof

:concat
set files=%files% %1
goto :eof