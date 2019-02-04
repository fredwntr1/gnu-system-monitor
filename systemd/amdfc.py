#!/usr/bin/env python3
import sys
import os
import subprocess


vendor = "glxinfo | grep 'renderer string:' | awk '{print $4}'"
display_vendor = subprocess.check_output(vendor, shell=True).strip()
display_vendor = repr(display_vendor)
change_perms = "find / -type f -name 'pwm1*' -exec chmod 777 {} \;"

if display_vendor == repr('AMD'):
    subprocess.check_output(change_perms, shell=True)
else:
    sys.exit()
