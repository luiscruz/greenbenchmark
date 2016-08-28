#!/bin/sh
CurrentTime=$(date "+%Y_%m_%d-%H_%M")
NAME="k9mail"
NAME="writely-pro"
NAME=${1:-$NAME}

PACKAGE="com.fsck.k9"
PACKAGE="me.writeily"
PACKAGE=${2:-$PACKAGE}

APK="apks/k9mail.apk"
APK="apks/writely-pro.apk"
APK=${3:-$APK}

# APK="/Users/luiscruz/dev/check_android_projects/tmp/k9mail/k-9/k9mail/build/outputs/apk/k9mail-debug.apk"
# TEST_SCRIPT="tests/k9mail.py"
TEST_DATA="writely-pro_cache.json"
TEST_DATA=${4:-$TEST_DATA}
ODROID_ENERGY_LOG_DIR="/sdcard/energy"
LOG_ENERGY=true

ResultsDir="$(pwd)/results/${NAME}_${CurrentTime}"
ResultsEventFile="$ResultsDir/event_log.csv"
ResultsEnergyFile="$ResultsDir/energy_log.csv"

mkdir "${ResultsDir}"

function get_timestamp
{
    # gdate '+%s.%3N'
    adb shell 'date +%s' | tr  -d '\r'
}

function log_event
{
		tput bel #beep
		echo "---- $1 ----"
    echo "$(get_timestamp),$1">> "$ResultsEventFile"
}
echo "timestamp,event" > "$ResultsEventFile"

log_event "Started"

# Start logging energy
if $LOG_ENERGY ; then
adb push "$(pwd)/odroid_energy_monitor.sh" "$ODROID_ENERGY_LOG_DIR"
adb shell "sh ${ODROID_ENERGY_LOG_DIR}/odroid_energy_monitor.sh" &
ENERGY_LOGGER_PID=$!
echo "Energy $ENERGY_LOGGER_PID"
fi

adb shell "rm -rf sdcard/writeily" # specific for writeilypro
log_event "UninstallApp"
adb uninstall $PACKAGE
log_event "InstallApp"
adb install $APK


log_event "Reset BatteryStats"
adb shell dumpsys batteryinfo --reset
# read -p "Interaction script is about to start. Reset energy meter and press any key to continue..."
#open app
log_event "OpenApp"
adb shell monkey -p $PACKAGE --pct-syskeys 0 1
# wait until next minute
#sleep $((60 - $(get_timestamp) % 60))

#run AndroidViewClient tests
log_event "InteractionStarted"
python run_cached_script.py "tests/$TEST_DATA"
log_event "InteractionEnded"


if $LOG_ENERGY ; then
# Stop logging energy
kill $ENERGY_LOGGER_PID
wait $ENERGY_LOGGER_PID 2>/dev/null # hack to supress termination output
adb pull "$ODROID_ENERGY_LOG_DIR/energy_log.csv" "$(pwd)"
mv "energy_log.csv" "$ResultsEnergyFile"
fi

adb shell dumpsys batteryinfo > "$ResultsDir/batterystats.txt"

log_event "End"
# echo "Energy log ended. Register energy meter data and press any key to exit..."
# if [ -t 0 ]; then stty -echo -icanon -icrnl time 0 min 0; fi
# while [ -z "$key" ]; do
# 	tput bel
# 	sleep 1
# 	read key
# done
# if [ -t 0 ]; then stty sane; fi
