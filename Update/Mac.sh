#!/bin/bash
sleep 1
rm -r "%1WiiMusicEditorPlus.app"
mv "$(dirname $0)/NewProgram.app" "%1WiiMusicEditorPlus.app"
open "%1WiiMusicEditorPlus.app"