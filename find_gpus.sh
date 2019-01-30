#!/usr/bin/env bash


for CurrentCard in /sys/class/drm/card?/ ; do
    for CurrentMonitor in "$CurrentCard"device/hwmon/hwmon?/ ; do
        cd $CurrentMonitor && pwd
done
done