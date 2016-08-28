#!/bin/sh
PACKAGE=$1
APK=$2

adb uninstall $PACKAGE
adb install $APK
adb shell monkey -p $PACKAGE --pct-syskeys 0 1
