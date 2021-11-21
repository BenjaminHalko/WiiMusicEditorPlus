#!/bin/bash
sleep 1
rm -r %1
mv "$(dirname $0)/WiiMusicEditorPlus/WiiMusicEditorPlus.app" "%1
open %1