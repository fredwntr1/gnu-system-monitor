#!/usr/bin/env bash

for CurrentCard in /sys/kernel/debug/dri/?/ ; do
    cd $CurrentCard && pwd
done
