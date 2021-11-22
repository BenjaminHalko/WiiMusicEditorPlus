#!/bin/bash
sleep 1
rm -r $1
mv "~/Library/Application Support/WiiMusicEditorPlus.app" $1
open $1