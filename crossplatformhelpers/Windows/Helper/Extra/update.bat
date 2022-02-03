@echo off

timeout 1
tar --verbose -xf "%~dp0downloaded.zip" -C %~p1\..
del "%~dp0downloaded.zip"
start "" %1