#!/bin/bash
sleep 1
rm "$(dirname $0)/../../WiiMusicEditorPlus"
mv "$(dirname $0)/NewProgram" "$(dirname $0)/../../WiiMusicEditorPlus"
open "$(dirname $0)/../../WiiMusicEditorPlus"