#!/bin/sh
sleep 1
rm -r $1
mv "/Users/$(id -un)/Library/Application Support/WiiMusicEditorPlus/WiiMusicEditorPlus.app" $1
open $1