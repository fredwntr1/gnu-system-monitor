#!/usr/bin/env python3
import sys
import subprocess


vendor = "glxinfo | grep 'renderer string:' | awk '{print $4}'"
display_vendor = subprocess.check_output(vendor, shell=True).strip()
display_vendor = repr(display_vendor)
permissions = "chmod -R a+rX /sys/kernel/debug"

if display_vendor == repr('AMD'):
    subprocess.check_output(permissions, shell=True)
else:
    sys.exit()

