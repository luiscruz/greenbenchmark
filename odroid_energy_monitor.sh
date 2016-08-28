#!/bin/sh

UpdatePeriod=263808 #real sensor update period in us
#UpdatePeriod=1000000
ResultsFilename="/sdcard/energy/energy_log.csv"
SENSOR_ARM="4-0040"
SENSOR_MEM="4-0041"
SENSOR_G3D="4-0044"
SENSOR_KFC="4-0045"

echo "timestamp,armW,memW,g3dW,kfcW,temperature,dumb" > "$ResultsFilename"

#enable
echo 1 > /sys/bus/i2c/drivers/INA231/4-0040/enable
echo 1 > /sys/bus/i2c/drivers/INA231/4-0041/enable
echo 1 > /sys/bus/i2c/drivers/INA231/4-0044/enable
echo 1 > /sys/bus/i2c/drivers/INA231/4-0045/enable



while usleep $UpdatePeriod
do
    printf "$(date +%s),"
    cat \
        "/sys/bus/i2c/drivers/INA231/$SENSOR_ARM/sensor_W" \
        "/sys/bus/i2c/drivers/INA231/$SENSOR_MEM/sensor_W" \
        "/sys/bus/i2c/drivers/INA231/$SENSOR_G3D/sensor_W" \
        "/sys/bus/i2c/drivers/INA231/$SENSOR_KFC/sensor_W" \
        "/sys/devices/virtual/thermal/thermal_zone0/temp" \
    | tr "\n" ","
    echo
done >> "$ResultsFilename"
