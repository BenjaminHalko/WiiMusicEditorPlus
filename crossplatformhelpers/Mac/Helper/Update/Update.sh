#!/bin/bash
sleep 1
rm -r "$(dirname $0)/../../WiiMusicEditorPlus.app"
mv "$(dirname $0)/NewProgram.app" "$(dirname $0)/../../WiiMusicEditorPlus.app"
open "$(dirname $0)/../../WiiMusicEditorPlus.app"