#!/bin/bash
sleep 1
rm $1
mv WiiMusicEditorPlus/WiiMusicEditorPlus $1
xdg-open "$1"