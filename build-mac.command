#!/bin/bash

cd "`dirname "$0"`"
pyinstaller --noconfirm --add-data crossplatformhelpers/Mac/Helper:Helper --add-data translations/translations:translations --icon=Icon/icon.ico app.py
echo "creating app"
/usr/local/bin/platypus -y -B -R -i 'Icon/icon.icns'  -a 'app'  -o 'None'  -p '/bin/sh'  -f 'dist/app' macscript.sh dist/app.app
echo "creating .zip"
rm dist/app-Mac.zip
tar -a -C dist -cf dist/app-Mac.zip app.app
echo "done"