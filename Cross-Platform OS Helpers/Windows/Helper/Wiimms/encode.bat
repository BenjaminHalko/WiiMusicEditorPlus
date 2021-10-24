@echo off

"%~dp0wbmgt.exe" encode %1\message.d\new_music_message.txt
del %1\message.d\new_music_message.txt
del %1\message.carc
"%~dp0wszst.exe" create %1\message.d --dest %1\message.carc
rmdir /s /q %1\message.d